# 2.1.5 Recherche top-k

> **Leçon de la section [2.1 v0.0.1 — le RAG à la main](../2.1-v0.0.1-rag-a-la-main.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir — [05_rechercher.py](05_rechercher.py)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Le « R » de RAG : embedder la **question**, la comparer à chaque chunk
indexé, garder les **k plus proches**. En v0.0.1 c'est un brute force
assumé — O(n) sur quelques centaines de chunks est instantané, et c'est
la référence exacte contre laquelle on jugera l'index approximatif de
Qdrant.

## Le savoir

- **La boucle** : question → embedding
  ([2.1.1](../2.1.1-embeddings/2.1.1-embeddings.md), avec le préfixe
  `search_query:` si le modèle le demande) → produit scalaire contre
  chaque vecteur ([2.1.2](../2.1.2-similarite-cosinus/2.1.2-similarite-cosinus.md))
  → tri → top-k avec scores et métadonnées.
- **Choisir k** : trop petit (3) = le bon chunk rate le coche dès que
  la question est large ; trop grand (20) = bruit injecté dans le
  prompt et contexte gaspillé. Point de départ raisonnable : k = 4-6,
  puis **régler avec les evals** ([2.1.7](../2.1.7-evals/2.1.7-evals.md)),
  jamais à l'intuition.
- **Le fossé sémantique requête/document** : une question (« comment on
  sauvegarde le NAS ? ») et une doc (« Backup : rsync quotidien vers… »)
  ne partagent parfois aucun mot — c'est exactement ce que l'embedding
  doit combler, et ce qu'on inspecte quand ça rate.
- **Seuil de score** : optionnel — et à manier en cohérence avec
  « seul l'ordre compte »
  ([2.1.2](../2.1.2-similarite-cosinus/2.1.2-similarite-cosinus.md)) :
  un seuil absolu sorti du chapeau n'a pas de sens, mais un seuil
  **calibré empiriquement** en a un — mesurer la distribution des
  meilleurs scores sur les questions du jeu (in-corpus) et sur
  quelques questions volontairement hors corpus, placer le seuil
  entre les deux. Il est propre au modèle et au corpus (à recalibrer
  si l'un change) et devient la matière première du « je ne sais
  pas » de [2.1.6](../2.1.6-rag-complet/2.1.6-rag-complet.md).
- **Ce que ça prépare** : cette fonction devient `chercher(question, k,
  filtres)` — la brique retrieval du
  [framework](../../../01-llm-from-scratch/1.3-framework-maison/1.3.1-architecture-modulaire/1.3.1-architecture-modulaire.md).

## En pratique

[05_rechercher.py](05_rechercher.py) : CLI qui prend une question,
affiche le top-k avec score, fichier source et premières lignes du
chunk — l'outil de debug n°1 de tout le module (avant même le RAG
complet).

## Pièges connus

- Oublier le préfixe de tâche côté requête alors que l'index l'a côté
  documents : les scores chutent, sans erreur visible.
- Déboguer la génération quand le retrieval est cassé : toujours
  inspecter le top-k **avant** d'accuser le prompt ou le modèle
  (démarche par couche, question d'entretien n°3).
- Trier tout le corpus pour prendre k éléments :
  `heapq.nlargest(k, ...)` suffit — détail, mais c'est le genre de
  détail qu'on voit en code review.

## Question d'entretien

> « Votre retrieval renvoie des chunks hors sujet : démarche ? »
> Inspecter le top-k réel sur 3-4 questions ratées ; vérifier préfixes
> de tâche, chunking (le bon passage existe-t-il ?), k ; comparer
> question reformulée vs originale — et seulement ensuite envisager
> hybride/re-ranking ([2.2](../../2.2-v0.0.2-qdrant-retrieval-avance/2.2-v0.0.2-qdrant-retrieval-avance.md)).

## Références

- [Schéma 04_recherche_topk](../../schemas/04_recherche_topk.png)
- `heapq.nlargest` (stdlib) — le tri partiel qui suffit
