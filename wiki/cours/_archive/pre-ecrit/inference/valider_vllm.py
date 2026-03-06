"""
valider_vllm.py — les trois verifications du deploiement (lecon 4.1.1).

vLLM deploye en conteneur (image vllm/vllm-openai, runtime nvidia,
--max-model-len 4096, modele 3B quantise AWQ), on valide dans l'ordre :

  1. /v1/models repond (l'API OpenAI-compatible est le contrat — notre
     backend commutable 2.4.2 basculera dessus sans changer de code) ;
  2. une completion aboutit (le modele genere vraiment) ;
  3. l'occupation VRAM se lit et se DECOMPOSE : vLLM PREALLOUE le KV
     cache dans --gpu-memory-utilization — une carte "pleine" au repos
     est normale, c'est la philosophie anti-Ollama (occuper pour le
     rendement multi-usagers vs charger/decharger pour le confort).

Chaque chiffre est note : ils alimentent le README du bench (4.3.2).
Rappel 6 Go : Ollama et vLLM ne tournent PAS en meme temps sur la
carte — verifier avec nvidia-smi avant de bencher.
"""

import subprocess

import httpx

VLLM_URL = "http://192.168.1.57:8000"


def verifier_modeles() -> str:
    reponse = httpx.get(f"{VLLM_URL}/v1/models", timeout=10)
    reponse.raise_for_status()
    modeles = [m["id"] for m in reponse.json()["data"]]
    print(f"1. /v1/models : {modeles}")
    return modeles[0]


def verifier_completion(modele: str) -> None:
    reponse = httpx.post(
        f"{VLLM_URL}/v1/chat/completions",
        json={
            "model": modele,
            "messages": [{"role": "user",
                          "content": "Reponds en un mot : ping ?"}],
            "max_tokens": 10,
        },
        timeout=120,
    )
    reponse.raise_for_status()
    d = reponse.json()
    print(f"2. completion : {d['choices'][0]['message']['content'].strip()!r} "
          f"({d['usage']['prompt_tokens']}+{d['usage']['completion_tokens']} "
          f"tokens)")


def verifier_vram() -> None:
    """nvidia-smi lisible en machine : occupation totale + par process.
    A decomposer a la main dans le README : poids du modele quantise
    (~2-2.5 Go pour un 3B AWQ) + KV cache prealloue (le reste de
    gpu-memory-utilization) + overhead."""
    resultat = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used,memory.total",
         "--format=csv,noheader"],
        capture_output=True, text=True, timeout=15,
    )
    if resultat.returncode != 0:
        print("3. nvidia-smi indisponible ici — a lire sur l'hote GPU")
        return
    print(f"3. VRAM : {resultat.stdout.strip()} "
          f"(prealloue par vLLM : normal que ce soit presque plein)")


if __name__ == "__main__":
    try:
        modele = verifier_modeles()
    except httpx.HTTPError as erreur:
        raise SystemExit(
            f"vLLM injoignable ({erreur}) — verifier le conteneur : logs de "
            f"demarrage (OOM ? baisser --max-model-len ou "
            f"gpu-memory-utilization AVANT de changer de modele — piege "
            f"4.1.1), et les options indisponibles sur Turing (FP8...)."
        )
    verifier_completion(modele)
    verifier_vram()
    print("\nDeploiement valide : noter chaque chiffre (modele, quantif,")
    print("max-model-len, VRAM) — ce sont les conditions a publier avec")
    print("le bench (4.2.1 : un chiffre sans conditions ne se compare a rien).")
