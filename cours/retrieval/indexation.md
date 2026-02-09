# Indexation

> [carte du cours](../carte.md) · étape : [`04_indexer.py`](../../etapes/retrieval/04_indexer.py)

## L'essentiel

L'indexation est le **pipeline batch** qui matérialise le corpus :
chunk → embedding → stockage. Ici, SQLite — assumé et suffisant pour
quelques centaines de chunks : le but de la v0.0.1 est de comprendre ce
qu'une base vectorielle fera à notre place en
[2.2.1](migration-qdrant.md).

## Le savoir

- **Le schéma minimal** : une table
  `chunks(id, fichier_source, section, texte, embedding)` — le vecteur
  sérialisé en JSON ou BLOB. Pas d'extension vectorielle : la recherche
  de la [2.1.5](recherche-top-k.md) se
  fera en Python, brute force.
- **Un pipeline batch, donc** ([roadmap couche 2](../_archive/roadmap.md) —
  « pipelines batch » est une compétence nommée) :
  - **reprise sur erreur** : l'appel d'embeddings peut échouer au chunk
    412 — le pipeline doit reprendre là où il s'est arrêté, pas tout
    refaire ;
  - **idempotence** : relancer l'indexation deux fois ne doit pas
    dupliquer les lignes (clé sur `fichier_source + section`, ou table
    reconstruite d'un bloc) ;
  - **détection de changement** : à terme, un hash du texte par chunk
    évite de re-embedder l'inchangé — l'embedding est la seule étape
    chère.
- **La séparation index/requête** : l'indexation tourne rarement
  (le corpus bouge peu), la recherche tourne tout le temps — deux
  scripts, deux rythmes, et c'est ce qui deviendra deux services.
- **Vérifications de sortie** : compter les chunks, vérifier la norme
  des vecteurs stockés, échantillonner 3 chunks et relire leur texte —
  un index silencieusement vide est le bug RAG le plus courant.

## En pratique

[04_indexer.py](../../etapes/retrieval/04_indexer.py) : itérer sur les chunks de
[2.1.3](chunking.md), embedder via
[2.1.1](embeddings.md), stocker en SQLite ;
afficher un rapport final (n fichiers, n chunks, durée).

## Pièges connus

- Stocker les floats en texte avec précision réduite (`str(v)`) : la
  similarité se dégrade silencieusement — sérialiser proprement (JSON
  complet ou BLOB de float32).
- Ré-indexer sans purger après un changement de chunking : anciens et
  nouveaux chunks cohabitent et polluent le top-k.
- `index.db` versionné par accident : c'est un artefact reconstructible
  — déjà couvert par le [.gitignore](../../.gitignore) du module.

## Se tester

> « Que doit garantir un pipeline d'ingestion RAG en production ? »
> Idempotence, reprise sur erreur, détection de changement (ne
> re-payer que le delta), validation de sortie (comptes, normes,
> échantillons) et traçabilité de la version du corpus — le mot-clé du
> marché est « pipeline batch avec reprise », pas « script ».

## Références

- [Schéma 03_indexation_sqlite](../_schemas/retrieval/03_indexation_sqlite.png)
- Doc SQLite (BLOB) — et, pour situer la suite : ce que Qdrant
  remplacera exactement
