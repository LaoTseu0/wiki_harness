"""
05_rechercher.py — le "R" de RAG : retrouver les chunks pertinents.

C'est la moitie "en ligne" du RAG, jouee a CHAQUE question :
  1. embedder la question (meme espace que les chunks — 01)
  2. la comparer a TOUS les chunks (similarite_cosinus — 02)
  3. trier, garder les k meilleurs (le "top-k")

Point cle vu au 02 : on ne met pas de seuil absolu ("garder > 0.7"),
on prend les k mieux CLASSES. Ici k=3.

La naivete de la v1, en pleine lumiere : on charge les 132 vecteurs en
RAM et on calcule 132 cosinus, un par un. C'est un "scan lineaire" —
O(n). A 132 chunks, c'est instantane. A 1 million de chunks, c'est mort.
Qdrant (v2) utilise un index HNSW qui trouve les proches SANS tout
comparer — le saut qu'on veut pouvoir justifier en entretien.

=== EXERCICE ===================================================
Completer rechercher(). charger_index() (lecture SQLite) et
l'affichage sont fournis.

Spec de rechercher(question, index, k=3) :
  - index : liste de tuples (fichier, titre, texte, vecteur)
            deja chargee (vecteur = liste de floats)
  - etape 1 : v_question = embedder(question)
  - etape 2 : pour chaque (f, t, x, v) de l'index, calculer
              similarite_cosinus(v_question, v) et garder le tuple
              (score, fichier, titre, texte)
  - etape 3 : trier par score DECROISSANT, renvoyer les k premiers

Outils Python :
  - liste en comprehension : [(f(x), x) for x in truc]
  - tri : mande.sort(key=lambda e: e[0], reverse=True)
          -> trie la liste sur le 1er element du tuple, du + grand
             au + petit ; lambda = fonction anonyme (le "e => e[0]"
             de JS). Alternative : sorted(mande, key=..., reverse=True)
  - trancher : liste[:k] = les k premiers (slicing, vu au 05 du M1)

Attendu pour "backup du NAS" (scores a ~0.01 pres) :
  1. 0.816  backlog.md > NAS
  2. 0.778  architecture/nas.md > (intro)
  3. 0.758  serveurs/nas/installation.md > (intro)
================================================================
"""

import json
import sqlite3
import sys
from pathlib import Path

# Le script vit dans son dossier de lecon ; rag_commun.py reste a la
# racine du module (bibliotheque partagee). On ajoute cette racine au
# chemin de recherche des imports.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rag_commun import BASE, embedder, similarite_cosinus


def charger_index() -> list[tuple]:
    """Relit l'index SQLite en RAM : liste de (fichier, titre, texte, vecteur)."""
    if not BASE.exists():
        raise SystemExit("index.db absent — lance d'abord 04_indexer.py")
    con = sqlite3.connect(BASE)
    lignes = con.execute("SELECT fichier, titre, texte, vecteur FROM chunks").fetchall()
    con.close()
    # json.loads defait le json.dumps du 04 : le texte "[0.03, ...]"
    # redevient une vraie liste de floats.
    return [(f, t, x, json.loads(v)) for f, t, x, v in lignes]


def rechercher(question: str, index: list[tuple], k: int = 3) -> list[tuple]:
    """Renvoie les k chunks les plus proches : liste de (score, fichier, titre, texte)."""
    ...  # A COMPLETER (3 etapes : embedder, scorer tous, trier + [:k])


if __name__ == "__main__":
    index = charger_index()
    print(f"{len(index)} chunks charges depuis {BASE.name}\n")

    for question in [
        "Qu'est-ce qu'on avait decide pour le backup du NAS ?",
        "Quelle est l'adresse IP de jarvis-central ?",
        "Sur quel port l'API d'Ollama ecoute-t-elle ?",
    ]:
        print(f"Q: {question}")
        for score, fichier, titre, texte in rechercher(question, index):
            print(f"   {score:.4f}  {fichier} > {titre}")
        print()
