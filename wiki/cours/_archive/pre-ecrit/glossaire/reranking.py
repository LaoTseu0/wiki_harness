"""
reranking.py — re-ordonner le top-k avec un modele plus precis.

Le retrieval rapide (vecteurs, BM25) est volontairement grossier : il
ramene 20 candidats en millisecondes, mais leur ORDRE est approximatif
(un bi-encoder encode question et document separement — leur
interaction fine est perdue). Le re-ranking relit chaque paire
(question, chunk) ENSEMBLE et re-trie. Pattern entonnoir :
rappel d'abord, precision ensuite.

Ici, la version "zero dependance nouvelle" : le LLM-as-reranker.
Qwen3 note chaque paire de 0 a 10, en sortie CONTRAINTE (le format
d'Ollama, lecon 1.1.5 — sans schema, les notes arrivent en prose).
Lent mais parfait pour comprendre ; la version production
(cross-encoder dedie type bge-reranker) arrive en 2.2.3.

Mesure : le RANG du bon fichier avant/apres re-ranking, sur les 12
questions du jeu d'evals du module 2.

Prerequis : index.db du module 2 construit (04_indexer.py).
"""

import json
import sqlite3
import sys
from pathlib import Path

import httpx

M2 = Path(__file__).resolve().parents[3] / "02-homelab-rag"
sys.path.insert(0, str(M2))

from rag_commun import BASE, MODELE_CHAT, OLLAMA, embedder, similarite_cosinus

JEU = M2 / "evals" / "questions.json"
TOP_RAPPEL = 20   # largeur du rappel (l'entree de l'entonnoir)
TOP_FINAL = 5     # ce qu'on garde apres re-ranking

# Sortie contrainte : une note entiere, rien d'autre (lecon 1.1.5 —
# demander poliment une note produit de la prose autour).
SCHEMA_NOTE = {
    "type": "object",
    "properties": {"note": {"type": "integer", "minimum": 0, "maximum": 10}},
    "required": ["note"],
}


def charger_chunks() -> list[dict]:
    if not BASE.exists():
        raise SystemExit("index.db absent — lance d'abord 04_indexer.py (module 2)")
    con = sqlite3.connect(BASE)
    lignes = con.execute(
        "SELECT fichier, titre, texte, vecteur FROM chunks"
    ).fetchall()
    con.close()
    return [
        {"fichier": f, "titre": t, "texte": x, "vecteur": json.loads(v)}
        for f, t, x, v in lignes
    ]


def rappel_vecteurs(question: str, chunks: list[dict], k: int) -> list[dict]:
    """L'etage rapide : top-k par similarite cosinus (bi-encoder)."""
    v_q = embedder(question)
    scores = [(similarite_cosinus(v_q, c["vecteur"]), c) for c in chunks]
    scores.sort(key=lambda e: e[0], reverse=True)
    return [c for _, c in scores[:k]]


def noter_paire(question: str, chunk: dict) -> int:
    """L'etage precis : le LLM lit question ET chunk ensemble."""
    reponse = httpx.post(
        f"{OLLAMA}/api/chat",
        json={
            "model": MODELE_CHAT,
            "messages": [
                {
                    "role": "system",
                    "content": "Note de 0 a 10 la pertinence de l'extrait "
                    "pour repondre a la question. 10 = contient la reponse, "
                    "0 = sans rapport. Ne note pas le style, note la "
                    "presence de l'information.",
                },
                {
                    "role": "user",
                    "content": f"Question : {question}\n\n"
                    f"Extrait ({chunk['fichier']} > {chunk['titre']}) :\n"
                    f"{chunk['texte'][:1500]}",
                },
            ],
            "stream": False,
            "format": SCHEMA_NOTE,
            "options": {"temperature": 0, "seed": 42, "num_predict": 50},
        },
        timeout=120,
    )
    reponse.raise_for_status()
    return json.loads(reponse.json()["message"]["content"])["note"]


def reranker(question: str, candidats: list[dict]) -> list[dict]:
    """Re-trie les candidats par note LLM (l'ordre vecteurs est perdu)."""
    notes = [(noter_paire(question, c), c) for c in candidats]
    notes.sort(key=lambda e: e[0], reverse=True)
    return [c for _, c in notes]


def rang_du_fichier(liste: list[dict], fichier: str) -> int | None:
    """Position (1-indexee) du premier chunk du bon fichier, ou None."""
    for i, chunk in enumerate(liste, start=1):
        if chunk["fichier"] == fichier:
            return i
    return None


if __name__ == "__main__":
    chunks = charger_chunks()
    questions = json.loads(JEU.read_text(encoding="utf-8"))

    print(f"rappel top-{TOP_RAPPEL} vecteurs -> re-ranking LLM -> "
          f"top-{TOP_FINAL}\n")
    print(f"{'AVANT':>5} {'APRES':>5}  question")
    print("-" * 64)

    gagnes = perdus = 0
    for cas in questions:
        candidats = rappel_vecteurs(cas["question"], chunks, TOP_RAPPEL)
        avant = rang_du_fichier(candidats, cas["fichier_attendu"])
        re_tries = reranker(cas["question"], candidats)
        apres = rang_du_fichier(re_tries, cas["fichier_attendu"])

        # Le re-ranker ne peut pas sauver un document hors rappel : si
        # avant est None, elargir TOP_RAPPEL, pas accuser le re-ranker.
        if avant and apres:
            if apres < avant:
                gagnes += 1
            elif apres > avant:
                perdus += 1
        print(f"{str(avant or '-'):>5} {str(apres or '-'):>5}  "
              f"{cas['question'][:50]}")

    print("-" * 64)
    print(f"rangs ameliores : {gagnes}  |  degrades : {perdus}")
    print("\nA MESURER : le delta reel sur ce corpus. Si le delta est nul")
    print("(petit corpus bien chunke, ca arrive), la lecon 2.2.3 dit quoi")
    print("en faire : un composant sans delta se retire — et se raconte.")
