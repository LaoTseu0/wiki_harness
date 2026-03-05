"""
hnsw_recall.py — mesurer ce que l'index approximatif rend (et coute).

HNSW rend la recherche vectorielle logarithmique mais APPROXIMATIVE :
la descente gloutonne du graphe multi-couches peut rater le vrai plus
proche voisin. La mesure honnete : le recall@5 — la proportion des
vrais top-5 (brute force, notre 05_rechercher du module 2) que l'index
retrouve — en fonction de efSearch, LE bouton rappel <-> latence.

Entree glossaire "comprendre et schematiser" : ce script est la partie
MESURE ; le schema commente (couches, autoroutes/rues, descente d'une
requete) accompagne la lecon 1.2.3.

Prerequis :
  - Qdrant deploye (module 2, lecon 2.2.1) et la collection migree ;
  - pip install qdrant-client.
Sur ~132 chunks, attendu : recall ~1.0 partout (l'index ne se justifie
qu'a l'echelle — c'est aussi une lecon). Valeurs : A MESURER.
"""

import json
import sqlite3
import sys
import time
from pathlib import Path

M2 = Path(__file__).resolve().parents[3] / "02-homelab-rag"
sys.path.insert(0, str(M2))

from rag_commun import BASE, embedder, similarite_cosinus

try:
    from qdrant_client import QdrantClient
except ImportError:
    raise SystemExit("qdrant-client absent — pip install qdrant-client "
                     "(et Qdrant deploye : lecon 2.2.1)")

QDRANT_URL = "http://192.168.1.57:6333"
COLLECTION = "homelab_doc"
VALEURS_EF = [16, 64, 256]
K = 5

QUESTIONS_TEST = [
    "Qu'est-ce qu'on avait decide pour le backup du NAS ?",
    "Quelle est l'adresse IP de jarvis-central ?",
    "Sur quel port l'API d'Ollama ecoute-t-elle ?",
    "Comment fonctionne le serveur git du homelab ?",
    "Quel GPU equipe jarvis-core ?",
]


def top_k_brute_force(v_question: list[float], chunks: list[dict]) -> set:
    """La verite terrain : comparer a TOUS les vecteurs (O(n), exact)."""
    scores = [(similarite_cosinus(v_question, c["vecteur"]), c["id"])
              for c in chunks]
    scores.sort(key=lambda e: e[0], reverse=True)
    return {cid for _, cid in scores[:K]}


def charger_chunks() -> list[dict]:
    if not BASE.exists():
        raise SystemExit("index.db absent — lance d'abord 04_indexer.py")
    con = sqlite3.connect(BASE)
    lignes = con.execute("SELECT id, vecteur FROM chunks").fetchall()
    con.close()
    return [{"id": i, "vecteur": json.loads(v)} for i, v in lignes]


if __name__ == "__main__":
    chunks = charger_chunks()
    client = QdrantClient(url=QDRANT_URL)
    vecteurs_questions = [(q, embedder(q)) for q in QUESTIONS_TEST]

    print(f"{len(chunks)} vecteurs | recall@{K} vs brute force\n")
    print(f"{'efSearch':>8} {'recall':>7} {'latence':>9}")
    print("-" * 30)

    for ef in VALEURS_EF:
        trouves = attendus = 0
        debut = time.perf_counter()
        for question, v_q in vecteurs_questions:
            verite = top_k_brute_force(v_q, chunks)
            # search_params : ef pilote la largeur d'exploration a la
            # requete — le compromis rappel/latence, a l'execution.
            resultat = client.query_points(
                COLLECTION,
                query=v_q,
                limit=K,
                search_params={"hnsw_ef": ef},
            )
            approx = {p.id for p in resultat.points}
            trouves += len(verite & approx)
            attendus += K
        latence_ms = (time.perf_counter() - debut) * 1000 / len(QUESTIONS_TEST)
        print(f"{ef:>8} {trouves / attendus:>7.3f} {latence_ms:>7.1f}ms")

    print("\nLecture (lecon 1.2.3) : un recall@5 de 0.98 = une requete sur")
    print("50 perd un bon document — a savoir AVANT de deboguer sa chaine.")
    print("Et sur ~132 chunks le brute force est deja instantane : l'index")
    print("se justifie a l'echelle, pas par principe.")
