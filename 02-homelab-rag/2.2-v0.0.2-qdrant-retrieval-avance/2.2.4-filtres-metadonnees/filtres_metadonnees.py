"""
filtres_metadonnees.py — restreindre la recherche a un perimetre.

Chercher "backup" dans TOUTE la doc quand on sait que la reponse vit
dans architecture/ est un handicap volontaire. Les filtres Qdrant
s'appliquent PENDANT la traversee HNSW (pre-filtering), pas apres —
et pour rester rapides sur les champs filtres souvent, on declare un
INDEX DE PAYLOAD (piege de la lecon : filtrer un champ non indexe est
correct... mais scanne).

Le champ "dossier" a ete pose au moment de la migration (2.2.1) —
les metadonnees se decident au chunking, pas apres coup.

Demonstration des trois cas de la lecon :
  1. filtre explicite (parametre — ce que la 2.4.1 exposera en API) ;
  2. filtre trop zele -> top-k vide -> FALLBACK sans filtre (le piege
     "un filtre deduit doit pouvoir s'elargir") ;
  3. effet precision/rappel : la meme question avec et sans filtre.

Prerequis : Qdrant + collection migree (2.2.1), qdrant-client.
"""

import sys
from pathlib import Path

MODULE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE))

from rag_commun import embedder

try:
    from qdrant_client import QdrantClient, models
except ImportError:
    raise SystemExit("qdrant-client absent — pip install qdrant-client")

QDRANT_URL = "http://192.168.1.57:6333"
COLLECTION = "homelab_doc"


def chercher(client: QdrantClient, question: str, k: int = 3,
             filtres: dict | None = None) -> list[tuple]:
    """La signature prevue par la brique retrieval du framework :
    chercher(question, k, filtres). filtres = {"dossier": "architecture"}.
    Fallback integre : si le filtre vide le top-k, on relance SANS
    filtre (et on le dit) plutot que de renvoyer zero resultat."""
    filtre_qdrant = None
    if filtres:
        filtre_qdrant = models.Filter(must=[
            models.FieldCondition(key=champ, match=models.MatchValue(value=valeur))
            for champ, valeur in filtres.items()
        ])
    resultat = client.query_points(
        COLLECTION, query=embedder(question), limit=k,
        query_filter=filtre_qdrant, with_payload=True,
    )
    if not resultat.points and filtres:
        print(f"   [filtre {filtres} -> 0 resultat : fallback sans filtre]")
        return chercher(client, question, k, filtres=None)
    return [
        (p.score, p.payload["fichier"], p.payload["titre"], p.payload["texte"])
        for p in resultat.points
    ]


if __name__ == "__main__":
    client = QdrantClient(url=QDRANT_URL)

    # L'index de payload : a declarer UNE fois par champ filtre souvent.
    client.create_payload_index(
        COLLECTION, field_name="dossier",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )
    print("index de payload declare sur 'dossier'\n")

    question = "Qu'est-ce qu'on avait decide pour le backup du NAS ?"

    print(f"Q: {question}\n\nSans filtre :")
    for score, fichier, titre, _ in chercher(client, question):
        print(f"   {score:.4f}  {fichier} > {titre}")

    print("\nFiltre dossier=architecture :")
    for score, fichier, titre, _ in chercher(
        client, question, filtres={"dossier": "architecture"}
    ):
        print(f"   {score:.4f}  {fichier} > {titre}")

    print("\nFiltre trop zele (dossier=backup, inexistant) :")
    for score, fichier, titre, _ in chercher(
        client, question, filtres={"dossier": "backup"}
    ):
        print(f"   {score:.4f}  {fichier} > {titre}")

    print("\nA faire ensuite (lecon 2.2.4) : ajouter au jeu d'evals 2-3")
    print("questions ou le filtre change la donne — filtrer ameliore la")
    print("precision mais peut tuer le rappel si le filtre est faux :")
    print("mesurer les DEUX dans le tableau de la 2.2.5.")
