"""
vlm_local.py — faire "voir" un modele sur la RTX 2060.

Techniquement, c'est un appel LLM avec une IMAGE dans le message
(champ `images`, base64, chez Ollama) : le client du framework s'etend
d'un champ, pas d'un paradigme (lecon 7.2.1). La nouveaute est le
BUDGET : l'encodeur de vision transforme l'image en tokens visuels —
l'image consomme du contexte et de la VRAM, en fonction de sa
RESOLUTION.

Les deux usages a demontrer + la mesure :
  1. DESCRIPTION d'une photo (la resolution peut etre reduite) ;
  2. OCR d'un document scanne (l'OCR a besoin de nettete) ;
  3. la MEME image a deux resolutions : latence + tokens compares —
     le tableau "ce qui tient en 6 Go" du module.

Prerequis : un VLM pulle sur Ollama (qwen2.5vl:3b ou llava) — et le
rappel de la lecon : le VLM et le pipeline vocal partagent les 6 Go,
ils ne tournent pas forcement en meme temps.

Usage : python vlm_local.py photo.jpg [describe|ocr]
"""

import base64
import io
import sys
import time
from pathlib import Path

import httpx

OLLAMA_URL = "http://192.168.1.57:11434"
MODELE_VLM = "qwen2.5vl:3b"   # a ajuster selon ce qui tient en 6 Go

PROMPTS = {
    "describe": "Decris cette image en francais, en 3 phrases maximum.",
    "ocr": "Transcris TOUT le texte visible dans cette image, "
           "fidelement, sans commenter. Si un passage est illisible, "
           "ecris [illisible].",
}


def encoder_image(chemin: Path, cote_max: int | None = None) -> str:
    """Image -> base64, avec redimensionnement optionnel : reduire
    l'image reduit les tokens visuels et la VRAM (piege de la lecon :
    la pleine resolution fait exploser les deux)."""
    donnees = chemin.read_bytes()
    if cote_max is not None:
        try:
            from PIL import Image
        except ImportError:
            print("(Pillow absent : pas de redimensionnement — "
                  "pip install pillow)", file=sys.stderr)
            return base64.b64encode(donnees).decode()
        image = Image.open(io.BytesIO(donnees))
        image.thumbnail((cote_max, cote_max))
        tampon = io.BytesIO()
        image.convert("RGB").save(tampon, format="JPEG", quality=90)
        donnees = tampon.getvalue()
    return base64.b64encode(donnees).decode()


def interroger(image_b64: str, prompt: str) -> dict:
    debut = time.perf_counter()
    reponse = httpx.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODELE_VLM,
            "messages": [{
                "role": "user",
                "content": prompt,
                "images": [image_b64],   # LA nouveaute : un champ
            }],
            "stream": False,
            "options": {"temperature": 0, "num_predict": 500},
        },
        timeout=300,
    )
    reponse.raise_for_status()
    d = reponse.json()
    return {
        "texte": d["message"]["content"],
        "tokens_prompt": d.get("prompt_eval_count", 0),  # tokens visuels inclus
        "latence_s": time.perf_counter() - debut,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage : python vlm_local.py <image> [describe|ocr]")
    chemin = Path(sys.argv[1])
    tache = sys.argv[2] if len(sys.argv) > 2 else "describe"
    prompt = PROMPTS[tache]

    # La mesure de la lecon : deux resolutions, memes questions.
    print(f"tache : {tache} | modele : {MODELE_VLM}\n")
    for etiquette, cote in [("reduite (768px)", 768), ("pleine", None)]:
        resultat = interroger(encoder_image(chemin, cote), prompt)
        print(f"--- resolution {etiquette} ---")
        print(f"tokens prompt (image incluse) : {resultat['tokens_prompt']} | "
              f"latence : {resultat['latence_s']:.1f}s")
        print(f"{resultat['texte'][:400]}\n")

    print("A completer avec nvidia-smi pendant l'appel : le tableau")
    print("'ce qui tient en 6 Go' (poids + encodeur vision + KV gonfle")
    print("par les tokens visuels). Et pour l'OCR de documents critiques :")
    print("un VLM hallucine sans signal d'erreur — garde-fous en 7.3.1.")
