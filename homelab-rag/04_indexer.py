"""
04_indexer.py — construire l'index : chunk -> embedding -> SQLite.

Jusqu'ici on recalculait tout a chaque lancement. Ca ne passe pas a
l'echelle : embedder 132 chunks prend ~20 s, et on ne veut pas payer ce
prix a CHAQUE question. Solution : calculer les vecteurs UNE fois et les
STOCKER. C'est l'indexation — la moitie "hors ligne" du RAG (l'autre
moitie, la recherche, sera "en ligne", a chaque question).

Le magasin : SQLite. Une base de donnees dans UN fichier (index.db), sans
serveur a lancer (contrairement a Postgres). Le module `sqlite3` est
DANS la lib standard de Python — rien a installer. Analogie homelab :
c'est le "SQLite du RAG", le degre zero du magasin de vecteurs. En v2 on
le remplacera par Qdrant (un vrai moteur vectoriel, conteneur docker) —
mais on veut d'abord voir ce que Qdrant nous epargnera.

Naivete assumee de la v1 : on range chaque vecteur comme du TEXTE JSON
(json.dumps(liste) -> "[0.03, -0.006, ...]"). SQLite ne sait pas
comparer des vecteurs ; on relira tout en RAM pour chercher (05). C'est
exactement la limite que Qdrant leve.

Rappel securite (reflexe du module 1) : on n'ecrit JAMAIS une valeur
directement dans une requete SQL par f-string. On utilise des
PARAMETRES (les "?") : la valeur passe par un canal separe, jamais
interpretee comme du code. C'est la parade a l'injection SQL — la
version base de donnees du filtrage qu'on faisait sur les tool_calls.

    con.execute("INSERT INTO t (a, b) VALUES (?, ?)", (val_a, val_b))
                                          ^^^^^^          ^^^^^^^^^^^^
                                     trous nommes ?      valeurs a part

=== EXERCICE ===================================================
Completer la BOUCLE d'indexation dans indexer(). Tout le SQL
(connexion, creation de table, commit) est deja ecrit. Il te
reste le coeur : pour chaque chunk du corpus,
  1. calculer son embedding avec embedder(chunk["texte"])
  2. le serialiser en texte JSON avec json.dumps(vecteur)
  3. l'inserer avec con.execute(SQL_INSERT, (...4 valeurs...))
     dans l'ordre : fichier, titre, texte, vecteur_json

Prerequis : avoir recopie ta fonction decouper_en_sections() du
03 dans rag_commun.py (sinon charger_corpus() leve une erreur).

Attendu a l'execution : "132 chunks indexes", fichier index.db
d'environ 1,6 Mo cree a cote du script.
================================================================
"""

import json
import sqlite3

from rag_commun import BASE, charger_corpus, embedder

SQL_CREER = """
CREATE TABLE chunks (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    fichier TEXT,
    titre   TEXT,
    texte   TEXT,
    vecteur TEXT
)
"""
SQL_INSERT = "INSERT INTO chunks (fichier, titre, texte, vecteur) VALUES (?, ?, ?, ?)"


def indexer() -> int:
    """(Re)construit l'index SQLite. Renvoie le nombre de chunks indexes."""
    corpus = charger_corpus()

    # connect() cree le fichier s'il n'existe pas. On repart de zero a
    # chaque lancement : l'index est un artefact reconstructible.
    con = sqlite3.connect(BASE)
    con.execute("DROP TABLE IF EXISTS chunks")
    con.execute(SQL_CREER)

    for i, chunk in enumerate(corpus, start=1):
        ...  # A COMPLETER : 1) vecteur = embedder(...)
        ...  #               2) vecteur_json = json.dumps(...)
        ...  #               3) con.execute(SQL_INSERT, (...))
        if i % 20 == 0:
            print(f"  indexe {i}/{len(corpus)}")

    # commit() = valider la transaction (rien n'est ecrit sur disque
    # avant). close() libere le fichier.
    con.commit()
    con.close()
    return len(corpus)


if __name__ == "__main__":
    n = indexer()
    taille_ko = BASE.stat().st_size / 1024
    print(f"\n{n} chunks indexes  (attendu 132)")
    print(f"index : {BASE.name}  ({taille_ko:.0f} Ko, attendu ~1600)")
