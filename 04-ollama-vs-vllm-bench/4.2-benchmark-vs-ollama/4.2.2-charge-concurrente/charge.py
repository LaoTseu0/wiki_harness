"""
charge.py — le script de charge maison : 1, 5, 20 requetes simultanees.

LA mesure du module (lecon 4.2.2) : a une requete, Ollama et vLLM se
ressemblent ; a vingt, ils divergent — file d'attente (TTFT qui
explose) contre batching continu (debit agrege qui grimpe). n workers
asyncio lances en salve, chacun mesurant ses metriques (4.2.1) ;
asyncio et pas des threads : la charge est de l'I/O pur (attendre des
streams), asyncio.gather de n coroutines httpx est exact et leger.

Disciplines de la lecon, toutes dans ce fichier :
  - prompts legerement VARIES (un suffixe unique par requete) : sinon
    on mesure le prompt caching a son insu ;
  - PLUSIEURS salves par point (la variance a n=20 est enorme) ;
  - bruts JSON conserves, agregats calcules a part ;
  - un moteur A LA FOIS sur les 6 Go (verifier nvidia-smi avant).

Usage :
    python charge.py ollama    # bench de l'Ollama du homelab
    python charge.py vllm      # bench du vLLM deploye en 4.1.1
Sortie : charge_<moteur>.json (bruts + agregats par niveau de n).
Les courbes du README (TTFT p95, tokens/s par requete, debit agrege
en fonction de n) se tracent depuis ce JSON (matplotlib suffit).
"""

import asyncio
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "4.2.1-metriques-debit-latence"))
import mesures

MOTEURS = {
    "ollama": {"url": "http://192.168.1.57:11434",
               "modele": "qwen3:4b-instruct-2507-q4_K_M",
               "mesure": mesures.mesurer_requete_ollama},
    "vllm": {"url": "http://192.168.1.57:8000",
             "modele": "auto",   # relu depuis /v1/models au demarrage
             "mesure": mesures.mesurer_requete_openai},
}

NIVEAUX_CONCURRENCE = [1, 5, 20]
SALVES_PAR_NIVEAU = 3
MAX_TOKENS = 200

PROMPT_BASE = ("Explique en cinq phrases ce que fait un serveur "
               "d'inference LLM et pourquoi la memoire GPU est son "
               "goulot d'etranglement.")


async def une_requete(config: dict, numero: int) -> dict:
    """Une coroutine = un 'utilisateur'. Le suffixe unique evite de
    mesurer le cache de prefixe a son insu."""
    prompt = f"{PROMPT_BASE} (requete {numero})"
    # La mesure elle-meme est synchrone (httpx.stream) : on la pousse
    # dans un thread pour que les n 'utilisateurs' attendent VRAIMENT
    # en parallele.
    return await asyncio.to_thread(
        config["mesure"], config["url"], config["modele"], prompt, MAX_TOKENS
    )


async def une_salve(config: dict, n: int) -> dict:
    debut = time.perf_counter()
    bruts = await asyncio.gather(*(une_requete(config, i) for i in range(n)))
    duree = time.perf_counter() - debut
    total_tokens = sum(b["tokens_generes"] or 0 for b in bruts)
    return {
        "n": n,
        "bruts": bruts,
        # LA metrique que la concurrence fait diverger : le debit
        # AGREGE (tokens/s toutes requetes confondues).
        "debit_agrege_tokens_s": total_tokens / duree if duree else 0,
        "duree_salve_s": duree,
    }


async def bencher(nom: str) -> None:
    config = dict(MOTEURS[nom])
    if config["modele"] == "auto":
        import httpx
        config["modele"] = httpx.get(f"{config['url']}/v1/models",
                                     timeout=10).json()["data"][0]["id"]

    # Warm-up : le premier appel Ollama inclut le chargement du modele.
    await une_requete(config, -1)

    resultats = []
    for n in NIVEAUX_CONCURRENCE:
        for salve in range(SALVES_PAR_NIVEAU):
            r = await une_salve(config, n)
            resultats.append(r)
            agregat = mesures.agreger(r["bruts"])
            ttft = agregat["ttft_s"]
            print(f"n={n:>2} salve {salve + 1}/{SALVES_PAR_NIVEAU} : "
                  f"TTFT p95 {ttft['p95']:.2f}s | "
                  f"debit agrege {r['debit_agrege_tokens_s']:.0f} tok/s")

    sortie = Path(__file__).parent / f"charge_{nom}.json"
    sortie.write_text(json.dumps({
        "moteur": nom, "modele": config["modele"],
        "max_tokens": MAX_TOKENS, "salves": resultats,
        "conditions": "a completer : quantisation, max-model-len, "
                      "prompt tokens, LAN — un chiffre sans conditions "
                      "ne se compare a rien (4.2.1)",
    }, indent=2), encoding="utf-8")
    print(f"\nbruts ecrits : {sortie.name} — courbes attendues (4.2.2) :")
    print("TTFT p95 plat puis MUR chez Ollama (file d'attente) ;")
    print("degradation douce chez vLLM jusqu'a saturation du KV cache")
    print("(preemptions visibles dans ses logs). A MESURER.")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in MOTEURS:
        raise SystemExit(f"usage : python charge.py [{'|'.join(MOTEURS)}]")
    asyncio.run(bencher(sys.argv[1]))
