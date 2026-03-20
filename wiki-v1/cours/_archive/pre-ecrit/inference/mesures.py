"""
mesures.py — le module de mesure du bench : TTFT et tokens/s, separes.

Deux familles, deux experiences utilisateur (lecon 4.2.1) :
  - TTFT (time to first token) : le chat "repond vite" — determine par
    le PREFILL (tout le prompt traite d'un bloc, borne calcul) ;
  - tokens/s de generation : la reponse "s'ecrit vite" — determinee
    par le DECODE (token par token, borne bande passante memoire).

Le piege n.1 de la lecon est evite par construction : le TTFT n'entre
JAMAIS dans le denominateur des tokens/s (les deux phases sont
separees dans le calcul). Les bruts sont conserves en JSON : on peut
recalculer les agregats sans re-mesurer.

Ce module est importe par charge.py (4.2.2) — il parle aux DEUX API :
Ollama natif (/api/chat) et OpenAI-compatible (vLLM, /v1/...).
"""

import json
import statistics
import time

import httpx


def mesurer_requete_ollama(url: str, modele: str, prompt: str,
                           max_tokens: int = 200) -> dict:
    """Une requete streamee contre Ollama natif ; renvoie les bruts."""
    debut = time.perf_counter()
    premier_token = None
    tokens_generes = 0
    with httpx.stream(
        "POST", f"{url}/api/chat",
        json={"model": modele,
              "messages": [{"role": "user", "content": prompt}],
              "stream": True,
              "options": {"num_predict": max_tokens, "temperature": 0.7}},
        timeout=600,
    ) as reponse:
        for ligne in reponse.iter_lines():
            if not ligne:
                continue
            chunk = json.loads(ligne)
            if chunk["message"]["content"] and premier_token is None:
                premier_token = time.perf_counter()
            if chunk.get("done"):
                tokens_generes = chunk.get("eval_count", 0)
                tokens_prompt = chunk.get("prompt_eval_count", 0)
                break
    return _bruts(debut, premier_token, tokens_generes, tokens_prompt)


def mesurer_requete_openai(url: str, modele: str, prompt: str,
                           max_tokens: int = 200) -> dict:
    """La meme mesure contre une API OpenAI-compatible (vLLM)."""
    debut = time.perf_counter()
    premier_token = None
    morceaux = 0
    with httpx.stream(
        "POST", f"{url}/v1/chat/completions",
        json={"model": modele,
              "messages": [{"role": "user", "content": prompt}],
              "max_tokens": max_tokens, "stream": True, "temperature": 0.7},
        timeout=600,
    ) as reponse:
        for ligne in reponse.iter_lines():
            if not ligne or not ligne.startswith("data: "):
                continue
            corps = ligne[len("data: "):]
            if corps == "[DONE]":
                break
            delta = json.loads(corps)["choices"][0]["delta"]
            if delta.get("content"):
                if premier_token is None:
                    premier_token = time.perf_counter()
                morceaux += 1   # ~1 token par chunk SSE chez vLLM
    # Piege de la lecon : les templates de chat different entre
    # moteurs — les comptes exacts du prompt se relisent via l'API
    # non-streamee si besoin de comparer les prefills.
    return _bruts(debut, premier_token, morceaux, tokens_prompt=None)


def _bruts(debut, premier_token, tokens_generes, tokens_prompt) -> dict:
    fin = time.perf_counter()
    ttft = (premier_token - debut) if premier_token else None
    duree_decode = (fin - premier_token) if premier_token else None
    return {
        "ttft_s": ttft,
        "tokens_generes": tokens_generes,
        "tokens_prompt": tokens_prompt,
        # tokens/s de DECODE seul : (fin - premier token), jamais le TTFT.
        "tokens_par_s": (tokens_generes / duree_decode
                         if duree_decode and tokens_generes else None),
        "latence_totale_s": fin - debut,
    }


def agreger(bruts: list[dict]) -> dict:
    """Jamais une moyenne seule : mediane + p95 (la queue de latence
    est ce que vivent les utilisateurs). n >= 10 mesures par point."""
    def stats(cle):
        valeurs = sorted(b[cle] for b in bruts if b[cle] is not None)
        if not valeurs:
            return None
        return {
            "mediane": statistics.median(valeurs),
            "p95": valeurs[min(len(valeurs) - 1,
                               int(0.95 * (len(valeurs) - 1)))],
            "n": len(valeurs),
        }
    return {"ttft_s": stats("ttft_s"), "tokens_par_s": stats("tokens_par_s"),
            "latence_totale_s": stats("latence_totale_s")}


if __name__ == "__main__":
    # Auto-test : une mesure contre l'Ollama du homelab (warm-up exclu :
    # le premier appel charge le modele — piege de la lecon).
    URL, MODELE = "http://192.168.1.57:11434", "qwen3:4b-instruct-2507-q4_K_M"
    prompt = "Explique en trois phrases ce qu'est le KV cache."
    mesurer_requete_ollama(URL, MODELE, prompt, max_tokens=30)  # warm-up
    bruts = [mesurer_requete_ollama(URL, MODELE, prompt) for _ in range(3)]
    print(json.dumps(bruts, indent=2))
    print(json.dumps(agreger(bruts), indent=2))
