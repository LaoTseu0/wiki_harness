"""
retrieval_hybride.py — deux moteurs qui se trompent differemment.

Le retrieval vectoriel comprend "sauvegarde" ~= "backup" mais rate
"RTX 2060" ou "11434" (termes exacts) ; BM25 fait l'exact inverse.
L'hybride lance les DEUX recherches et fusionne les CLASSEMENTS par
RRF (Reciprocal Rank Fusion) :

    score(d) = somme sur chaque moteur de 1 / (K_RRF + rang_du_doc)

On fusionne des RANGS, pas des scores : BM25 et cosinus vivent sur des
echelles incomparables (additionner les scores bruts = une jambe
ecrase l'autre, piege de la lecon 2.2.2).

Renvoi croise assume : la mecanique BM25 est importee de l'entree
glossaire 1.2.1 (module 1) — ecrite une fois, reutilisee ici.

Mesure : les questions ratees par la baseline v0.0.1 (retrieval 7/12)
— combien l'hybride en repeche-t-il ? A MESURER.
"""

import json
import sys
from pathlib import Path

MODULE = Path(__file__).resolve().parents[2]
GLOSSAIRE_BM25 = (MODULE.parent / "01-llm-from-scratch"
                  / "1.2-glossaire-executable" / "1.2.1-bm25")
sys.path.insert(0, str(MODULE))
sys.path.insert(0, str(GLOSSAIRE_BM25))

from rag_commun import embedder, similarite_cosinus
from bm25 import calculer_idf, charger_chunks, score_bm25

JEU = MODULE / "evals" / "questions.json"
K_RRF = 60          # la constante standard de RRF (Cormack et al.)
TOP_PAR_MOTEUR = 20  # largeur de rappel de chaque jambe


def classement_bm25(question, chunks, idf, avgdl):
    scores = [(score_bm25(question, c, idf, avgdl), c) for c in chunks]
    scores.sort(key=lambda e: e[0], reverse=True)
    return [c for _, c in scores[:TOP_PAR_MOTEUR]]


def classement_vecteurs(question, chunks):
    v_q = embedder(question)
    scores = [(similarite_cosinus(v_q, c["vecteur"]), c) for c in chunks]
    scores.sort(key=lambda e: e[0], reverse=True)
    return [c for _, c in scores[:TOP_PAR_MOTEUR]]


def chercher_hybride(question: str, chunks, idf, avgdl, k: int = 5):
    """Les deux classements fusionnes par RRF, top-k final."""
    fusion: dict[int, float] = {}
    reference: dict[int, dict] = {}
    for classement in (
        classement_bm25(question, chunks, idf, avgdl),
        classement_vecteurs(question, chunks),
    ):
        for rang, chunk in enumerate(classement, start=1):
            cle = id(chunk)
            reference[cle] = chunk
            fusion[cle] = fusion.get(cle, 0.0) + 1 / (K_RRF + rang)
    tries = sorted(fusion.items(), key=lambda e: e[1], reverse=True)
    return [(score, reference[cle]) for cle, score in tries[:k]]


if __name__ == "__main__":
    chunks = charger_chunks()   # l'index SQLite, tokens BM25 inclus
    idf = calculer_idf(chunks)
    avgdl = sum(c["longueur"] for c in chunks) / len(chunks)
    questions = json.loads(JEU.read_text(encoding="utf-8"))

    print(f"{'VECT':>4} {'HYBR':>4}  question")
    print("-" * 64)
    vect_ok = hybride_ok = 0
    for cas in questions:
        attendu = cas["fichier_attendu"]
        top_vect = classement_vecteurs(cas["question"], chunks)[:5]
        dans_vect = any(c["fichier"] == attendu for c in top_vect)
        top_hybride = chercher_hybride(cas["question"], chunks, idf, avgdl)
        dans_hybride = any(c["fichier"] == attendu for _, c in top_hybride)
        vect_ok += dans_vect
        hybride_ok += dans_hybride
        repeche = "  <-- repeche par l'hybride" if (dans_hybride and
                                                    not dans_vect) else ""
        print(f"{'OK' if dans_vect else 'MISS':>4} "
              f"{'OK' if dans_hybride else 'MISS':>4}  "
              f"{cas['question'][:46]}{repeche}")

    n = len(questions)
    print("-" * 64)
    print(f"fichier attendu dans le top-5 : vecteurs {vect_ok}/{n} | "
          f"hybride {hybride_ok}/{n}")
    print("\nRappel du piege (2.2.2) : conclure sur un jeu sans questions")
    print("a termes exacts ne prouve rien — le jeu doit couvrir les deux")
    print("regimes de faiblesse. Et sur 12 questions, +/-1 point est du")
    print("bruit : regarder QUELLES questions basculent (2.2.5).")
