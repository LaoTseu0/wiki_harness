"""
bm25.py — le retrieval lexical de reference, ecrit a la main.

BM25 classe des documents selon les mots EXACTS de la requete, sans
aucune semantique : "qdrant" ne matche que "qdrant". C'est l'inverse
des embeddings (module 2), aveugles aux termes rares mais forts sur
les paraphrases — d'ou la recherche hybride (2.2.2) qui combine les
deux.

La formule (Robertson & Zaragoza), terme a terme :

    score(D, Q) = somme, pour chaque terme t de Q, de
        IDF(t) * tf(t, D) * (k1 + 1)
                 / (tf(t, D) + k1 * (1 - b + b * |D| / avgdl))

  - IDF : un terme rare dans le corpus vaut plus (log du ratio) ;
  - k1 (~1.5) : SATURATION — le 10e "docker" d'un document vaut moins
    que le 1er (croissance en plateau, LA difference avec TF-IDF brut) ;
  - b (~0.75) : normalisation par la longueur du document (un long
    document contient mecaniquement plus d'occurrences).

L'exercice : comparer le top-5 BM25 au top-5 vecteurs sur les 12
questions du jeu d'evals du module 2 — et trouver une question ou
chacun bat l'autre (identifiants exacts vs paraphrases).

Prerequis : l'index SQLite du module 2 construit (04_indexer.py).
Piege connu (lecon 1.2.1) : tokenisation — sans lower() ni retrait de
la ponctuation, "Docker," ne matche pas "docker" et le score
s'effondre en silence.
"""

import json
import math
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

# Ce script vit dans le glossaire du module 1 mais travaille sur les
# donnees du module 2 (index + jeu d'evals) : on ajoute la racine du
# module 2 au chemin des imports pour reutiliser rag_commun.
M2 = Path(__file__).resolve().parents[3] / "02-homelab-rag"
sys.path.insert(0, str(M2))

from rag_commun import BASE, embedder, similarite_cosinus

JEU = M2 / "evals" / "questions.json"

K1 = 1.5
B = 0.75


def tokeniser(texte: str) -> list[str]:
    """Minuscules + decoupe sur tout ce qui n'est pas lettre/chiffre.
    On garde les chiffres : "11434" ou "4090" sont des termes utiles."""
    return re.findall(r"[a-z0-9_.]+", texte.lower())


def charger_chunks() -> list[dict]:
    """Relit l'index du module 2 : fichier, titre, texte, vecteur."""
    if not BASE.exists():
        raise SystemExit("index.db absent — lance d'abord 04_indexer.py (module 2)")
    con = sqlite3.connect(BASE)
    lignes = con.execute(
        "SELECT fichier, titre, texte, vecteur FROM chunks"
    ).fetchall()
    con.close()
    return [
        {
            "fichier": f,
            "titre": t,
            "texte": x,
            "vecteur": json.loads(v),
            "tokens": Counter(tokeniser(x)),
            "longueur": len(tokeniser(x)),
        }
        for f, t, x, v in lignes
    ]


def calculer_idf(chunks: list[dict]) -> dict[str, float]:
    """IDF de chaque terme : log((N - n + 0.5) / (n + 0.5) + 1).
    n = nombre de documents contenant le terme (pas ses occurrences)."""
    n_docs = len(chunks)
    presence = Counter()
    for chunk in chunks:
        presence.update(set(chunk["tokens"]))
    return {
        terme: math.log((n_docs - n + 0.5) / (n + 0.5) + 1)
        for terme, n in presence.items()
    }


def score_bm25(question: str, chunk: dict, idf: dict, avgdl: float) -> float:
    """La formule, terme a terme sur les tokens de la question."""
    score = 0.0
    for terme in tokeniser(question):
        tf = chunk["tokens"].get(terme, 0)
        if tf == 0 or terme not in idf:
            continue
        norme_longueur = 1 - B + B * chunk["longueur"] / avgdl
        score += idf[terme] * tf * (K1 + 1) / (tf + K1 * norme_longueur)
    return score


def top_k_bm25(question, chunks, idf, avgdl, k=5):
    scores = [(score_bm25(question, c, idf, avgdl), c) for c in chunks]
    scores.sort(key=lambda e: e[0], reverse=True)
    return scores[:k]


def top_k_vecteurs(question, chunks, k=5):
    v_q = embedder(question)
    scores = [(similarite_cosinus(v_q, c["vecteur"]), c) for c in chunks]
    scores.sort(key=lambda e: e[0], reverse=True)
    return scores[:k]


if __name__ == "__main__":
    chunks = charger_chunks()
    idf = calculer_idf(chunks)
    avgdl = sum(c["longueur"] for c in chunks) / len(chunks)
    questions = json.loads(JEU.read_text(encoding="utf-8"))

    print(f"{len(chunks)} chunks, avgdl = {avgdl:.0f} tokens\n")
    print(f"{'BM25':>4} {'VECT':>4}  question")
    print("-" * 64)

    bm25_ok = vect_ok = 0
    for cas in questions:
        attendu = cas["fichier_attendu"]
        dans_bm25 = any(
            c["fichier"] == attendu for _, c in
            top_k_bm25(cas["question"], chunks, idf, avgdl)
        )
        dans_vect = any(
            c["fichier"] == attendu for _, c in
            top_k_vecteurs(cas["question"], chunks)
        )
        bm25_ok += dans_bm25
        vect_ok += dans_vect
        marque = ""
        if dans_bm25 != dans_vect:
            marque = "  <-- les deux moteurs divergent ici"
        print(f"{'OK' if dans_bm25 else 'MISS':>4} "
              f"{'OK' if dans_vect else 'MISS':>4}  "
              f"{cas['question'][:48]}{marque}")

    n = len(questions)
    print("-" * 64)
    print(f"fichier attendu dans le top-5 :  BM25 {bm25_ok}/{n}  |  "
          f"vecteurs {vect_ok}/{n}")
    print("\nLecture attendue : les scores different sur des questions")
    print("DIFFERENTES — termes exacts (IP, ports, modeles) pour BM25,")
    print("paraphrases pour les vecteurs. C'est la raison d'etre de")
    print("l'hybride (2.2.2). Valeurs exactes : A MESURER a l'execution.")
