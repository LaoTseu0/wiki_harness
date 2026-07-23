# Bases vectorielles & RAG — notes de synthèse

## 1. Qdrant

Base de données **vectorielle** open source (Apache 2.0), écrite en Rust. Stocke des *embeddings* et retrouve rapidement les plus similaires à un vecteur donné.

**Modèle de données** : une *collection* contient des *points* ; chaque point = 1 vecteur + un *payload* (métadonnées JSON). Requête = recherche par similarité (cosinus, produit scalaire, euclidien) + filtre optionnel sur le payload.

**Points forts**
- Filtrage pré-requête performant (son vrai différenciateur) : filtrer par métadonnées sans dégrader l'index HNSW
- Quantization native (scalaire, produit, binaire) → forte réduction de la RAM
- Recherche hybride (dense + sparse type BM25/SPLADE)
- Déploiement : Docker local, cluster distribué, ou SaaS (Qdrant Cloud)

### Quand l'utiliser

| Situation | Verdict |
|---|---|
| RAG / chatbot sur documentation d'entreprise | ✅ |
| Recherche sémantique, recommandation, images similaires | ✅ |
| Déduplication, détection d'anomalies, matching de profils | ✅ |
| Millions à milliards de vecteurs | ✅ |
| Filtres métier complexes + similarité | ✅ |
| Latence forte ou self-hosting (souveraineté) | ✅ |
| < ~100 000 vecteurs | ❌ → `pgvector` suffit |
| Prototype rapide | ❌ → Chroma ou FAISS en mémoire |
| Elasticsearch/Redis déjà en prod, besoin vectoriel secondaire | ❌ |

### Concurrents

| Catégorie | Solutions | Remarque |
|---|---|---|
| Bases vectorielles dédiées | Milvus/Zilliz, Weaviate, Vespa, Chroma, LanceDB | Milvus = le plus scalable mais lourd ; Weaviate = proche de Qdrant, modules d'embedding intégrés ; Vespa = puissant, courbe rude ; Chroma = ultra simple |
| SaaS managé | Pinecone, Qdrant Cloud, Zilliz Cloud | Pinecone = zéro ops, propriétaire, coûteux à l'échelle |
| Extensions de bases existantes | pgvector (Postgres), Elasticsearch/OpenSearch, Redis Vector, MongoDB Atlas Vector Search, Azure AI Search | Choix pragmatique si l'infra existe déjà |
| Bibliothèques | FAISS, hnswlib, ScaNN, Annoy | Pas des bases : ni persistance ni API, à embarquer dans le code |

**Positionnement de Qdrant** : performance + filtrage riche + open source + simple à déployer. Plus léger que Milvus, self-hostable contrairement à Pinecone, monte bien plus haut que pgvector.

---

## 2. « Nombre de vecteurs » : de quoi parle-t-on ?

Trois notions à ne pas confondre.

**1. Le nombre de vecteurs** — c'est le critère de choix de la base. = nombre de *chunks* indexés. Ex. : un PDF de 100 pages découpé en morceaux de ~500 tokens ≈ 300 vecteurs.

| Volume | Reco |
|---|---|
| 5 000 – 50 000 chunks (doc interne PME) | pgvector sans hésiter |
| 500 000 – 5 M (base de connaissances grand groupe) | Qdrant pertinent |
| 10 M+ (catalogue, archives, logs) | Base dédiée obligatoire |

**2. La dimension du vecteur** — la « longueur » d'un vecteur : 384 (MiniLM), 1536 (`text-embedding-3-small`), 3072 (`-large`). Dépend du modèle d'embedding, pas de la base. Joue sur la RAM, pas sur le choix pgvector vs Qdrant.

**3. La précision du RAG** — aucun rapport avec le choix de la base. Elle vient du chunking, du modèle d'embedding, du reranking, du prompt. Sur petit volume, pgvector et Qdrant renvoient quasiment les mêmes résultats.

**Ce qui change vraiment avec le volume : la latence.** pgvector + index HNSW tient jusqu'à quelques centaines de milliers de vecteurs ; au-delà, l'index ne tient plus confortablement en RAM. Le seuil de 100 000 est indicatif — le vrai déclencheur est « mes requêtes dépassent 200 ms et ça se voit ».

---

## 3. Quantization des embeddings

⚠️ À distinguer de la quantization du **LLM** (voir §4). Ici on compresse **les embeddings stockés dans l'index**. Les deux réglages sont indépendants.

**Principe** : un embedding = un tableau de float32. 1536 dims × 4 octets = **6 Ko/chunk** → ~6 Go pour 1 M de chunks, à garder en RAM. On réduit le nombre de bits par dimension en acceptant une perte.

| Type | Compression | Perte de recall typique |
|---|---|---|
| float16 / half | ×2 | quasi nulle |
| Scalaire (int8) | ×4 | 1–2 % |
| Product Quantization (PQ) | ×16 à ×64 | 5–15 %, très variable |
| Binaire (1 bit/dim) | ×32 | 5–10 %… ou catastrophique |

### Le rescoring — ce qui rend la quantization viable

1. **Oversampling** : chercher dans l'index quantizé et récupérer beaucoup plus de candidats que nécessaire (ex. 100 au lieu de 10). Rapide, faible empreinte mémoire.
2. **Rescoring** : recalculer le score exact de ces candidats avec les vecteurs float32 originaux (sur disque), garder le top 10.

→ 95–99 % de la qualité d'origine pour une fraction de la RAM. Qdrant le fait nativement (paramètres `oversampling` et `rescore`).

### Piège de la quantization binaire

Ne fonctionne bien que sur des embeddings de **grande dimension** (1536+) issus de modèles récents (OpenAI `text-embedding-3`, Cohere v3, certains Voyage). Sur un modèle 384 dims type MiniLM, le binaire détruit le signal → rester sur int8.

### Support par outil

- **Qdrant** : scalaire, produit, binaire en natif + rescoring intégré
- **pgvector** : `halfvec` (float16) et binaire via type `bit` + distance de Hamming ; rescoring à écrire soi-même en SQL (CTE de rerank)
- **Milvus / Weaviate** : PQ, SQ, binaire également

### Alternative souvent meilleure : Matryoshka

Certains modèles (OpenAI `text-embedding-3`, Nomic, quelques Voyage) sont entraînés en *Matryoshka Representation Learning* : on peut **tronquer** le vecteur (garder 512 dims sur 1536) en perdant très peu. Plus simple qu'une quantization, et combinable avec elle.

### Est-ce que ça vaut le coup ?

En dessous de quelques centaines de milliers de chunks : **non**. 100 000 vecteurs en 1536 dims = 600 Mo, ça tient partout. Ça devient utile quand l'index ne tient plus en RAM, ou quand la RAM est facturée au Go sur un service managé (passer de 24 Go à 6 Go change la facture).

---

## 4. Q4, Q4_K_M… (notation GGUF)

Notation issue de **llama.cpp / GGUF**. Concerne la quantization **des poids d'un LLM**, pas des embeddings → **n'a pas sa place dans le tableau du §3**.

- **Q** = quantized, **4** = 4 bits par poids (au lieu de 16)
- **K** = méthode « k-quants », plus maligne que la version historique
- **S / M / L** = small / medium / large, degré de finesse

`Q4_K_M` = compromis par défaut de la communauté : un modèle 7B passe de ~14 Go (fp16) à ~4 Go, dégradation à peine perceptible. `Q3` devient discutable, `Q2` casse vraiment le modèle.

**Correspondance indicative** : 4 bits/dimension = compression ×8, soit entre le scalaire int8 et le PQ. Mais en pratique personne ne quantize des embeddings en « Q4 » — les bases vectorielles proposent int8, PQ ou binaire, pas la nomenclature GGUF.

Dans un RAG, on peut très bien avoir un LLM en Q4_K_M **et** des embeddings en int8.

---

## 5. Les types de RAG

Par ordre de complexité croissante.

- **Naive RAG** — embed la question → top-k similarité → chunks dans le prompt. Sur une base propre et bien découpée, marche déjà correctement.
- **Hybrid search** — similarité vectorielle + lexicale (BM25), fusionnées par Reciprocal Rank Fusion. Rattrape la faiblesse du dense : noms propres, références produit, acronymes internes, codes d'erreur. Souvent le meilleur rapport gain/effort.
- **Rerank** — 50 candidats récupérés, rescorés finement par un cross-encoder (Cohere Rerank, BGE-reranker), on garde les 5 meilleurs. Gain de pertinence en général très net.
- **Query transformation** — retravailler la question avant de chercher : reformulations multiples, décomposition en sous-questions, ou **HyDE** (le LLM génère une réponse hypothétique et c'est *elle* qu'on embed — un faux document ressemble plus à un vrai document qu'une question).
- **Small-to-big / parent document** — indexer de petits chunks précis pour la recherche, renvoyer au LLM le paragraphe ou la section parente. Résout le dilemme « chunks petits = bonne recherche mais contexte amputé ».
- **Contextual retrieval** — avant indexation, un LLM ajoute à chaque chunk une phrase le resituant dans son document. Évite les chunks orphelins (« ce taux est passé à 3 % » sans savoir de quoi ni de quand).
- **Graph RAG** — graphe d'entités et de relations construit en amont. Utile pour les questions transverses (« quels thèmes récurrents dans ces 400 rapports ? »). Coûteux à construire.
- **Agentic RAG** — le LLM décide s'il doit chercher, où, et s'il recommence. Plus puissant, plus lent, plus cher, plus dur à déboguer.
- **Multimodal RAG** — indexer images, schémas, tableaux. Approches *late interaction* type ColPali/ColBERT.

**Ordre d'adoption recommandé**
naive → hybrid + rerank (couvrent l'immense majorité des besoins) → chunking amélioré (small-to-big ou contextual) → et seulement si les évaluations bloquent encore : graph ou agentic.

> **Piège classique** : empiler les techniques avant d'avoir un jeu de test. Sans une trentaine de questions-réponses de référence et une mesure de recall, impossible de savoir si le reranker améliore quoi que ce soit.

---

## 6. Vocabulaire : « candidat »

Un **candidat** est un résultat *intermédiaire* : un chunk jugé potentiellement pertinent à une étape donnée, pas encore validé comme réponse finale.

Le terme n'existe que parce que la recherche se fait en plusieurs étapes, en entonnoir :

```
100 000 chunks dans la base
        ↓  recherche vectorielle (rapide, approximative)
    50 candidats
        ↓  reranking (lent, précis)
    5 chunks retenus → envoyés au LLM
```

Logique constante : une première passe **rapide mais imprécise** dégrossit sur toute la base, une seconde passe **lente mais fine** trie un petit nombre d'éléments. On ne peut ni appliquer la méthode précise à 100 000 chunks (trop coûteux), ni se contenter de la rapide (pas assez juste).

| Contexte | Ce qui produit les candidats | Ce qui les filtre |
|---|---|---|
| Quantization + rescoring | recherche dans l'index compressé (100 candidats) | recalcul du score exact en float32 → top 10 |
| Reranking | recherche vectorielle (50 candidats) | cross-encoder → top 5 |
| Recherche hybride | vectoriel + BM25, chacun ses candidats | fusion RRF → top n |

**Synonymes** : *candidate set*, *candidate pool*, ou l'étape appelée **candidate generation** (par opposition au **ranking**). Vocabulaire hérité des systèmes de recommandation, où l'architecture « retrieval → ranking » est le schéma canonique.

**Paramètre lié** : `top_k` de récupération (nombre de candidats) vs `top_n` final (chunks envoyés au LLM). Ratio classique : 50 pour 5. Trop peu de candidats → le bon document n'est jamais vu par le reranker ; trop → latence payée pour rien.
