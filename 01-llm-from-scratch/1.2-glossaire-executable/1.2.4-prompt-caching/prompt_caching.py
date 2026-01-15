"""
prompt_caching.py — mesurer ce que le cache de prefixe economise.

Chaque appel re-paye le prefill de tout le prefixe (system, outils,
exemples) — vu en 1.1.1. Le prompt caching reutilise le KV cache deja
calcule pour un prefixe identique : le cout du prefixe stable tombe
a ~0. Trois experiences, chronometre en main (TTFT = time to first
token, mesure en streaming) :

  A. FROID vs CHAUD : le meme long prompt envoye deux fois de suite —
     le 2e TTFT doit s'effondrer (le prefill est reutilise).
  B. ASYMETRIE : changer un mot AU DEBUT (invalide tout) vs A LA FIN
     (n'invalide presque rien) — le cache marche par PREFIXE EXACT.
  C. EVICTION : intercaler un prompt different entre deux envois
     identiques — chez Ollama le "cache" est le KV du DERNIER prompt
     traite, pas une session : deux clients qui alternent s'evincent.

Prerequis : le modele deja charge (keep_alive), aucune autre requete
concurrente pendant la mesure. Valeurs : A MESURER (les ordres de
grandeur dependent du materiel).
"""

import json
import time

import httpx

OLLAMA_URL = "http://192.168.1.57:11434"
MODEL = "qwen3:4b-instruct-2507-q4_K_M"

# Un prefixe long et stable (~2000 tokens) : 200 lignes de pseudo-doc.
# En production ce serait le system prompt + les schemas d'outils.
PREFIXE = "\n".join(
    f"Article {i} : le serveur repond sur le port {1000 + i} et son "
    f"role est documente dans la section {i} du manuel interne."
    for i in range(200)
)


def mesurer_ttft(prompt: str) -> float:
    """Envoie le prompt en streaming, renvoie le TTFT en secondes."""
    debut = time.perf_counter()
    with httpx.stream(
        "POST",
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "options": {"num_predict": 20, "temperature": 0, "seed": 42},
        },
        timeout=300,
    ) as reponse:
        for ligne in reponse.iter_lines():
            if not ligne:
                continue
            chunk = json.loads(ligne)
            if chunk["message"]["content"]:
                return time.perf_counter() - debut  # premier token recu
            if chunk.get("done"):
                break
    return time.perf_counter() - debut


def question(texte_prefixe: str) -> str:
    return texte_prefixe + "\n\nSur quel port repond l'article 42 ?"


if __name__ == "__main__":
    print("A. Froid vs chaud (meme prompt, deux fois)")
    froid = mesurer_ttft(question(PREFIXE))
    chaud = mesurer_ttft(question(PREFIXE))
    print(f"   TTFT froid : {froid:.2f}s | chaud : {chaud:.2f}s | "
          f"gain x{froid / max(chaud, 0.001):.1f}\n")

    print("B. Asymetrie debut vs fin du prompt")
    # Un mot change AU DEBUT : le prefixe ne matche plus des le 1er
    # token -> tout le prefill est repaye.
    debut_change = mesurer_ttft(question("MODIFIE " + PREFIXE))
    # Re-chauffer le prefixe original avant le test "fin" :
    mesurer_ttft(question(PREFIXE))
    # Un mot change A LA FIN : tout le prefixe commun est reutilise.
    fin_change = mesurer_ttft(question(PREFIXE) + " Reponds en un mot.")
    print(f"   TTFT mot change au debut : {debut_change:.2f}s | "
          f"a la fin : {fin_change:.2f}s\n")

    print("C. Eviction par un prompt intercale")
    mesurer_ttft(question(PREFIXE))               # chauffe le prefixe
    mesurer_ttft("Raconte une blague courte.")    # evince le cache
    apres_eviction = mesurer_ttft(question(PREFIXE))
    print(f"   TTFT apres eviction : {apres_eviction:.2f}s "
          f"(attendu : proche du froid {froid:.2f}s — le cache etait "
          f"celui du DERNIER prompt, pas une session)\n")

    print("Lecon d'architecture (1.2.4) : stable au debut (system,")
    print("outils, exemples), variable a la fin (question du tour) —")
    print("et jamais de timestamp dans le system prompt.")
