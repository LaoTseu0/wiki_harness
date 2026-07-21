# 2.2.1 Migration Qdrant

> **Leçon de la section [2.2 v0.0.2 — Qdrant + retrieval avancé](../2.2-v0.0.2-qdrant-retrieval-avance.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Remplacer le SQLite + brute force de la
[2.1.4](../../2.1-v0.0.1-rag-a-la-main/2.1.4-indexation/2.1.4-indexation.md)
par **Qdrant**, la base vectorielle self-hostable choisie au homelab —
un conteneur docker de plus, dans le style maison. Le marché dit
« pick one » : en connaître une à fond, savoir situer les autres.

## Le savoir

- **Le modèle de données Qdrant** :
  - **collection** = un index (une par corpus), déclarée avec la taille
    de vecteur (768) et la métrique (cosine — ou dot, équivalent sur
    nos vecteurs normalisés,
    [2.1.2](../../2.1-v0.0.1-rag-a-la-main/2.1.2-similarite-cosinus/2.1.2-similarite-cosinus.md)) ;
  - **point** = id + vecteur + **payload** (JSON libre) — le payload
    reçoit nos métadonnées de
    [chunking](../../2.1-v0.0.1-rag-a-la-main/2.1.3-chunking/2.1.3-chunking.md) :
    fichier_source, section, texte ;
  - opérations : `upsert` (idempotent par id — notre reprise sur
    erreur devient triviale), `search`/`query` (top-k), filtres sur
    payload ([2.2.4](../2.2.4-filtres-metadonnees/2.2.4-filtres-metadonnees.md)).
- **Sous le capot** : index **HNSW** — approximatif, réglé par
  m/ef ; tout est dans l'[entrée glossaire](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.3-hnsw/1.2.3-hnsw.md).
  Premier réflexe de validation : comparer le top-k Qdrant au top-k
  brute force v0.0.1 (recall@k attendu ≈ 1 sur un petit corpus).
- **Déploiement homelab** : conteneur officiel `qdrant/qdrant`, un
  volume pour `/qdrant/storage`, port 6333 (REST + dashboard) —
  cohérent avec les non-négociables réseau du homelab.
- **Le paysage à situer** ([roadmap couche 2](../../../roadmap.md)) :
  Chroma (embarqué, léger), FAISS (bibliothèque, pas un serveur),
  pgvector (le choix « déjà du Postgres »), Pinecone (SaaS), Weaviate,
  Milvus — savoir dire pourquoi Qdrant ici : self-hostable, léger,
  payloads filtrables, dashboard.

## En pratique

Migrer [04_indexer.py](../../2.1-v0.0.1-rag-a-la-main/2.1.4-indexation/04_indexer.py)
vers un upsert Qdrant (client Python officiel) et
[05_rechercher.py](../../2.1-v0.0.1-rag-a-la-main/2.1.5-recherche-top-k/05_rechercher.py)
vers `query_points` ; garder
le chemin SQLite en référence de non-régression le temps de valider le
recall.

## Pièges connus

- Recréer la collection sans re-vérifier taille/métrique : une
  collection en 384/euclid accepte vos points 768 normalisés… en se
  trompant silencieusement (erreur ou scores absurdes selon le cas).
- Payload sans le **texte** du chunk : le top-k renvoie des ids et il
  faut une deuxième base pour lire — tout mettre dans le payload.
- Oublier le volume docker : corpus ré-indexé à chaque redémarrage du
  conteneur.

## Question d'entretien

> « Pourquoi une base vectorielle plutôt que votre SQLite maison ? »
> Index ANN (HNSW) pour l'échelle, filtres payload intégrés, upsert
> idempotent, API réseau multi-clients — et savoir ajouter : « sur mon
> corpus actuel, le brute force suffisait ; j'ai migré pour l'hybride,
> les filtres, et la compétence marché ».

## Références

- Doc Qdrant : collections, points, query API
- [Roadmap couche 2](../../../roadmap.md) — le tableau des bases à
  situer
