"""
migration_qdrant.py — du SQLite maison a une vraie base vectorielle.

Migration de la lecon 2.2.1 : les vecteurs deja calcules par
04_indexer.py (SQLite) partent dans Qdrant via `upsert`, et la
recherche passe de la boucle brute force a `query_points`. On garde le
chemin SQLite comme REFERENCE DE NON-REGRESSION : sur un petit corpus,
le top-k Qdrant doit etre identique au brute force (recall ~= 1) —
si ca bouge, c'est un bug (metrique, taille de vecteur, prefixes).

Points de la lecon appliques ici :
  - collection declaree avec taille (768) et metrique (cosine — dot
    serait equivalent sur nos vecteurs normalises, 2.1.2) ;
  - payload = fichier, titre, texte, dossier — TOUT ce qu'il faut pour
    lire les resultats sans deuxieme base (piege connu), et le champ
    "dossier" prepare les filtres de la 2.2.4 ;
  - upsert par id stable -> relancer le script est idempotent (la
    reprise sur erreur devient triviale).

Prerequis : conteneur qdrant/qdrant lance (port 6333, volume monte),
index.db construit, pip install qdrant-client.
"""

import json
import sqlite3
import sys
from pathlib import Path

MODULE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE))

from rag_commun import BASE, embedder

try:
    from qdrant_client import QdrantClient, models
except ImportError:
    raise SystemExit("qdrant-client absent — pip install qdrant-client")

QDRANT_URL = "http://192.168.1.57:6333"
COLLECTION = "homelab_doc"
DIMENSIONS = 768


def charger_sqlite() -> list[dict]:
    """L'index v0.0.1, source de la migration (vecteurs deja payes)."""
    if not BASE.exists():
        raise SystemExit("index.db absent — lance d'abord 04_indexer.py")
    con = sqlite3.connect(BASE)
    lignes = con.execute(
        "SELECT id, fichier, titre, texte, vecteur FROM chunks"
    ).fetchall()
    con.close()
    return [
        {"id": i, "fichier": f, "titre": t, "texte": x,
         "vecteur": json.loads(v)}
        for i, f, t, x, v in lignes
    ]


def migrer(client: QdrantClient, chunks: list[dict]) -> None:
    """Cree la collection et upsert tous les points (idempotent)."""
    client.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=models.VectorParams(
            size=DIMENSIONS, distance=models.Distance.COSINE,
        ),
    )
    client.upsert(
        collection_name=COLLECTION,
        points=[
            models.PointStruct(
                id=c["id"],
                vector=c["vecteur"],
                payload={
                    "fichier": c["fichier"],
                    "titre": c["titre"],
                    "texte": c["texte"],
                    # 1er segment du chemin ("architecture", "serveurs"...)
                    # : le champ des filtres metadonnees (2.2.4).
                    "dossier": c["fichier"].split("/")[0],
                },
            )
            for c in chunks
        ],
    )


def rechercher_qdrant(client: QdrantClient, question: str, k: int = 3):
    """Le remplacant de 05_rechercher : meme signature de sortie."""
    resultat = client.query_points(
        COLLECTION, query=embedder(question), limit=k, with_payload=True,
    )
    return [
        (p.score, p.payload["fichier"], p.payload["titre"], p.payload["texte"])
        for p in resultat.points
    ]


def verifier_recall(client: QdrantClient, chunks: list[dict]) -> None:
    """Non-regression : top-3 Qdrant == top-3 brute force ?"""
    sys.path.insert(0, str(MODULE / "2.1-v0.0.1-rag-a-la-main"
                           / "2.1.5-recherche-top-k"))
    from importlib import import_module
    _m05 = import_module("05_rechercher")

    index = _m05.charger_index()
    questions = json.loads(
        (MODULE / "evals" / "questions.json").read_text(encoding="utf-8")
    )
    identiques = 0
    for cas in questions:
        brute = {f for _, f, _, _ in _m05.rechercher(cas["question"], index, 3)}
        qdrant = {f for _, f, _, _ in rechercher_qdrant(client, cas["question"], 3)}
        identiques += brute == qdrant
    print(f"top-3 identiques au brute force : {identiques}/{len(questions)} "
          f"(attendu {len(questions)}/{len(questions)} sur ce corpus — "
          f"sinon, bug a chercher : metrique ? prefixes ?)")


if __name__ == "__main__":
    chunks = charger_sqlite()
    client = QdrantClient(url=QDRANT_URL)
    migrer(client, chunks)
    print(f"{len(chunks)} points upsertes dans '{COLLECTION}'\n")

    apercu = rechercher_qdrant(
        client, "Qu'est-ce qu'on avait decide pour le backup du NAS ?"
    )
    for score, fichier, titre, _ in apercu:
        print(f"   {score:.4f}  {fichier} > {titre}")
    print()
    verifier_recall(client, chunks)
