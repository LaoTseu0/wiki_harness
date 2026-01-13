# 2.1.1 Embeddings

> **Leçon de la section [2.1 v0.0.1 — le RAG à la main](../2.1-v0.0.1-rag-a-la-main.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ✅ acquis — [01_embeddings.py](01_embeddings.py)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Un embedding projette un texte dans un **espace vectoriel où « proche »
= « sémantiquement similaire »**. C'est le socle du RAG et de bien plus
(recherche sémantique, classification, recommandation, détection
d'anomalies). Ici : `nomic-embed-text` via Ollama, 768 dimensions,
vecteurs normalisés.

## Le savoir

- **Ce que c'est** : un modèle (transformer encodeur) qui lit le texte
  et sort un vecteur dense de taille fixe — 768 dimensions ici, quelle
  que soit la longueur d'entrée. Deux textes de sens voisin donnent
  des vecteurs d'angle faible.
- **Norme = 1** : les vecteurs sortent normalisés (‖v‖ = 1, vérifié
  dans le script). Conséquence directe : la similarité cosinus se
  réduit au produit scalaire
  ([2.1.2](../2.1.2-similarite-cosinus/2.1.2-similarite-cosinus.md)).
- **L'API** : `POST /api/embed` chez Ollama (celui du script) — même
  mécanique que le chat : HTTP + JSON. Attention : le legacy
  `/api/embeddings` renvoie des vecteurs **non normalisés** — la
  norme = 1 constatée ici est une propriété de l'endpoint récent
  autant que du modèle, et tout le raccourci cos = produit scalaire
  ([2.1.2](../2.1.2-similarite-cosinus/2.1.2-similarite-cosinus.md))
  en dépend.
- **Asymétrie requête/document** : les modèles de la famille nomic
  attendent des préfixes de tâche (`search_document:` /
  `search_query:`) — encoder une question et un document ne sont pas
  la même tâche. À vérifier pour chaque modèle d'embeddings.
- **Pourquoi « proche = similaire » tient** : le modèle est entraîné
  par contraste (rapprocher les paires liées, écarter les autres) —
  et il casse là où le contraste manquait à l'entraînement :
  négations, nombres et dates se ressemblent souvent plus qu'ils ne
  devraient. À garder en tête au debug retrieval : certains échecs
  sont des limites de l'espace, pas du code.
- **Le paysage** ([roadmap couche 2](../../../roadmap.md)) : ouverts
  (sentence-transformers, Jina, nomic) vs API (OpenAI, Cohere,
  Gemini) ; dimension et qualité varient — mais **jamais mélanger deux
  modèles dans un même index** : leurs espaces sont incompatibles.

## En pratique

[01_embeddings.py](01_embeddings.py) : appel httpx, vérification
de la norme, premières intuitions en comparant des paires de phrases
proches/lointaines. Constat du 20 juillet : `nomic-embed-text` à puller
sur jarvis-central (seul Qwen3 4B présent).

## Pièges connus

- Changer de modèle d'embeddings sans tout ré-indexer : les distances
  inter-modèles n'ont aucun sens — l'index entier est à reconstruire.
- Embedder des textes plus longs que la fenêtre du modèle : troncature
  silencieuse → le vecteur ne représente que le début du texte (lien
  direct avec le [chunking](../2.1.3-chunking/2.1.3-chunking.md)).
- Comparer des normes : l'information est dans la *direction* du
  vecteur normalisé, pas dans sa longueur.
- Mélanger `/api/embed` et `/api/embeddings` (legacy) dans une même
  chaîne : l'un normalise, l'autre non — scores faussés sans erreur
  visible.

## Question d'entretien

> « Citez des cas d'usage des embeddings au-delà du RAG. »
> Recherche sémantique, déduplication, classification (le vecteur
> comme features), clustering de tickets, recommandation, détection
> d'anomalies — le RAG n'est qu'un consommateur parmi d'autres.

## Références

- Carte modèle `nomic-embed-text` (préfixes de tâche, fenêtre)
- [Schéma 01_pipeline_rag](../../schemas/01_pipeline_rag.png)
