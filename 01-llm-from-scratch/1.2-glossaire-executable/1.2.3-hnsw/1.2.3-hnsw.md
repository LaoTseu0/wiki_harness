# 1.2.3 HNSW

> **Leçon de la section [1.2 Glossaire exécutable](../1.2-glossaire-executable.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ entrée « comprendre et schématiser » (pas
> implémenter) — à produire avec la
> [2.2](../../../02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2-v0.0.2-qdrant-retrieval-avance.md)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Comparer une requête à chaque vecteur du corpus est O(n) — tenable pour
le RAG v0.0.1, impossible à l'échelle. HNSW (« Hierarchical Navigable
Small World ») est l'index qui rend la recherche vectorielle
**approximative mais logarithmique** — c'est lui qui tourne dans
Qdrant, et son compromis rappel/vitesse se règle.

## Le savoir

- **L'idée** : un graphe de proximité multi-couches, analogue à une
  skip-list. Couches hautes : peu de nœuds, liens longs (autoroutes).
  Couche 0 : tous les nœuds, liens courts (rues). La recherche part
  d'en haut, descend en se rapprochant gloutonnement, affine en bas.
- **« Small world »** : quelques liens longs suffisent à rendre
  n'importe quel nœud atteignable en peu de sauts (l'intuition des
  « six degrés de séparation »).
- **Approximatif** : la descente gloutonne peut rater le vrai plus
  proche voisin (optimum local) — on mesure alors le **recall@k** : la
  proportion des vrais top-k retrouvés.
- **Les 3 paramètres à connaître** :
  - `M` — nombre de liens par nœud (plus = meilleur rappel, plus de
    RAM) ;
  - `efConstruction` — largeur d'exploration à l'insertion (qualité du
    graphe, temps d'indexation) ;
  - `efSearch` — largeur d'exploration à la requête : **le** bouton
    rappel ↔ latence à l'exécution.
- **À situer** : FAISS propose aussi IVF (clustering) et PQ
  (compression) ; HNSW est le choix par défaut des bases serveur
  (Qdrant, Weaviate, pgvector).

## En pratique

L'entrée glossaire est un **schéma commenté** (couches, descente d'une
requête) + une mesure : sur le corpus du module 2, comparer brute force
vs HNSW de Qdrant — recall@5 et latence, en variant `efSearch`
(ex. 16 / 64 / 256).

## Pièges connus

- Croire l'index exact : un recall@5 de 0,98 signifie qu'une requête
  sur 50 perd un bon document — à savoir avant de déboguer sa chaîne.
- Indexer avant de choisir la métrique (cosinus vs dot) : l'index se
  construit pour une métrique donnée.
- Sur 200 chunks, HNSW n'apporte rien : le brute force est déjà
  instantané — l'index se justifie à l'échelle, pas par principe.

## Question d'entretien

> « Comment une base vectorielle trouve-t-elle les plus proches voisins
> sans tout comparer ? »
> Graphe navigable hiérarchique : descente gloutonne des couches
> longues-distances vers la couche dense, recherche approximative
> réglée par efSearch — compromis rappel/latence mesurable.

## Références

- Malkov & Yashunin, « Efficient and robust approximate nearest
  neighbor search using HNSW » (2016)
- Doc Qdrant, section indexing (paramètres m / ef)
