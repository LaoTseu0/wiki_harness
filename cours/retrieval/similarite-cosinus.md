# Similarité cosinus

> [carte du cours](../carte.md) · étape : [`02_similarite.py`](../../etapes/retrieval/02_similarite.py)

## L'essentiel

La similarité cosinus mesure **l'angle entre deux vecteurs** — pas leur
distance. Deux textes proches en sens pointent dans la même direction
de l'espace d'embeddings, quelle que soit leur « longueur ». C'est la
métrique du RAG, et elle tient en trois lignes de Python.

## Le savoir

- **La formule** :

  ```
  cos(A, B) = (A · B) / (‖A‖ × ‖B‖)
  ```

  produit scalaire divisé par le produit des normes. Résultat dans
  [-1, 1] : 1 = même direction, 0 = orthogonaux (sans rapport),
  -1 = opposés (rare en pratique avec ces modèles).
- **La géométrie** (travaillée visuellement dans le script) : le
  produit scalaire projette un vecteur sur l'autre ; diviser par les
  normes ne garde que l'angle. Intuition 2D → valable en 768D.
- **Le raccourci qui compte** : sur des vecteurs **normalisés**
  (‖v‖ = 1, cas de [2.1.1](embeddings.md)),
  cosinus = produit scalaire tout court — trois multiplications-sommes,
  aucune racine carrée. C'est pour ça que les bases vectorielles
  proposent « dot » et « cosine » : sur du normalisé, c'est pareil.
- **En Python pur** :
  `sum(a * b for a, b in zip(v1, v2))` — l'expression génératrice du
  [PROGRESSION](../_archive/journal/progression-fondamentaux.md), écrite par Anthony.
- **Vs distance euclidienne** : sur vecteurs normalisés, les deux
  ordonnent pareil (‖A−B‖² = 2 − 2·cos) — le choix n'a d'importance
  que sur du non-normalisé.

## En pratique

[02_similarite.py](../../etapes/retrieval/02_similarite.py) : produit scalaire, normes
et angle écrits à la main, vérifiés sur des paires de phrases dont on
connaît la proximité attendue.

## Pièges connus

- Re-normaliser des vecteurs déjà normalisés « par sécurité » à chaque
  comparaison : inutile et coûteux sur tout un corpus.
- Interpréter les valeurs absolues : 0,72 n'est pas « 72 % pertinent » —
  seul l'**ordre** des scores compte, et l'échelle varie selon le
  modèle d'embeddings.
- Comparer des scores entre modèles d'embeddings différents : chaque
  espace a sa géométrie.

## Se tester

> « Pourquoi le cosinus plutôt que la distance euclidienne pour comparer
> des embeddings ? »
> On compare des directions sémantiques, pas des positions ; et sur
> vecteurs normalisés les deux sont équivalents — autant prendre le
> produit scalaire, le moins cher.

## Références

- [Schéma 04_recherche_topk](../_schemas/retrieval/04_recherche_topk.png) — la
  géométrie appliquée à la recherche
- 3Blue1Brown, algèbre linéaire (produit scalaire) — pour l'intuition
