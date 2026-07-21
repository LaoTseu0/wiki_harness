"""
reranking_topk.py — brancher l'entonnoir : rappel large, tri fin.

La theorie (bi-encoder vs cross-encoder) vit dans l'entree glossaire
1.2.2 — ici on BRANCHE et on MESURE. Deux implementations derriere la
MEME signature `rerank(question, candidats) -> candidats re-tries` :

  1. llm_reranker : Qwen3 note chaque paire 0-10, sortie contrainte —
     zero dependance nouvelle, lent, parfait pour comprendre
     (reutilise noter_paire() de l'entree glossaire 1.2.2) ;
  2. cross_encoder : bge-reranker-base via sentence-transformers —
     le choix "production" (quelques dizaines de ms par paire sur la
     RTX 2060). Absent ? le script le dit et continue avec le LLM.

Mesure de la lecon : le RANG du bon document avant/apres, et la
LATENCE ajoutee — le re-ranking est un achat de precision paye en
millisecondes, le tableau doit montrer les deux colonnes. A MESURER.
"""

import json
import sys
import time
from pathlib import Path

MODULE = Path(__file__).resolve().parents[2]
GLOSSAIRE = MODULE.parent / "01-llm-from-scratch" / "1.2-glossaire-executable"
sys.path.insert(0, str(MODULE))
sys.path.insert(0, str(GLOSSAIRE / "1.2.2-re-ranking"))

from reranking import charger_chunks, noter_paire, rappel_vecteurs

JEU = MODULE / "evals" / "questions.json"
TOP_RAPPEL = 20
TOP_FINAL = 5


def llm_reranker(question: str, candidats: list[dict]) -> list[dict]:
    """Implementation 1 : le LLM note chaque paire (glossaire 1.2.2)."""
    notes = [(noter_paire(question, c), c) for c in candidats]
    notes.sort(key=lambda e: e[0], reverse=True)
    return [c for _, c in notes]


def cross_encoder_reranker(question: str, candidats: list[dict]) -> list[dict]:
    """Implementation 2 : cross-encoder dedie (production).
    Attention au piege de la lecon : verifier la fenetre du modele —
    un chunk tronque a son insu est juge sur son debut seulement."""
    from sentence_transformers import CrossEncoder  # import local : optionnel
    modele = CrossEncoder("BAAI/bge-reranker-base")
    paires = [(question, c["texte"][:2000]) for c in candidats]
    scores = modele.predict(paires)
    tries = sorted(zip(scores, candidats), key=lambda e: e[0], reverse=True)
    return [c for _, c in tries]


def rang(liste: list[dict], fichier: str) -> int | None:
    for i, chunk in enumerate(liste, start=1):
        if chunk["fichier"] == fichier:
            return i
    return None


if __name__ == "__main__":
    chunks = charger_chunks()
    questions = json.loads(JEU.read_text(encoding="utf-8"))

    implementations = {"llm": llm_reranker}
    try:
        import sentence_transformers  # noqa: F401 — test de presence
        implementations["cross-encoder"] = cross_encoder_reranker
    except ImportError:
        print("(sentence-transformers absent — seule l'implementation "
              "LLM sera mesuree ; pip install sentence-transformers "
              "pour la version production)\n")

    for nom, rerank in implementations.items():
        print(f"=== {nom} : rappel top-{TOP_RAPPEL} -> tri -> "
              f"top-{TOP_FINAL} ===")
        print(f"{'AVANT':>5} {'APRES':>5} {'ms':>7}  question")
        print("-" * 64)
        for cas in questions:
            candidats = rappel_vecteurs(cas["question"], chunks, TOP_RAPPEL)
            avant = rang(candidats, cas["fichier_attendu"])
            debut = time.perf_counter()
            re_tries = rerank(cas["question"], candidats)[:TOP_FINAL]
            latence_ms = (time.perf_counter() - debut) * 1000
            apres = rang(re_tries, cas["fichier_attendu"])
            print(f"{str(avant or '-'):>5} {str(apres or '-'):>5} "
                  f"{latence_ms:>7.0f}  {cas['question'][:44]}")
        print()

    print("Rappels de la lecon 2.2.3 : (1) le re-ranker ne sauve pas un")
    print("document hors rappel — elargir le top d'abord ; (2) un delta")
    print("nul sur ce corpus est un resultat, pas un echec : un composant")
    print("sans delta se retire, et ca se raconte en entretien.")
