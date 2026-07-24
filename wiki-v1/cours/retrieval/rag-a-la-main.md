# v0.0.1 — le RAG entièrement à la main

> [carte du cours](../carte.md)

## Vue d'ensemble

Construire la chaîne RAG complète **sans framework** — chunking →
embedding → stockage → retrieval → génération citée — pour comprendre
chaque maillon avant de l'outiller. Le projet : « qu'est-ce qu'on avait
décidé pour le backup du NAS ? » → réponse sourcée depuis les `.md` du
homelab. Les sept leçons suivent l'ordre du pipeline : les cinq
premières construisent le « R » (retrieval), la sixième branche le
« G » (génération), la septième mesure le tout — et cette mesure est la
partie la plus valorisable du module.

## Contenu

- **[Embeddings](embeddings.md)** —
      texte → vecteur 768 dims via Ollama, norme = 1
- **[Similarité cosinus](similarite-cosinus.md)**
      — produit scalaire, normes, angle — écrite par Anthony
- **[Chunking](chunking.md)** — découper
      les `.md` par sections, source en métadonnée
- **[Indexation](indexation.md)** —
      pipeline chunk → embedding → SQLite
- **[Recherche top-k](recherche-top-k.md)**
      — question → embedding → top-k (le « R » de RAG)
- **[RAG complet](rag-complet.md)** —
      retrieval → prompt avec contexte → réponse citée
- **[Evals](evals.md)** — jeu de questions,
      score déterministe, baseline chiffrée

> **Baseline provisoire mesurée** : retrieval 7/12, génération 7/12,
> zéro hallucination — le point de départ chiffré que la
> [v0.0.2](qdrant.md)
> devra battre. Précision de méthode : « zéro hallucination » se fonde
> sur la correspondance **question par question** (les cinq échecs de
> génération sont les cinq échecs de retrieval), pas sur l'égalité des
> totaux — deux 7/12 portant sur des questions différentes n'auraient
> rien prouvé.

## Synthèse

La chaîne se recompose en une phrase : *des textes découpés (2.1.3)
projetés en vecteurs (2.1.1) et stockés (2.1.4) permettent de retrouver
les passages proches d'une question (2.1.2, 2.1.5), qu'on injecte dans
le prompt pour une réponse sourcée (2.1.6) — et rien de tout cela ne
compte sans mesure (2.1.7).* Quand le RAG répondra mal, le diagnostic
suivra la même chaîne, maillon par maillon.
**Auto-contrôle** : savoir dire quel maillon on accuserait en premier
devant un score retrieval de 7/12 (indice : jamais le modèle).

## Références

- Schémas du pipeline : [_schemas/retrieval/](../_schemas/retrieval)
- Bibliothèque commune : [rag_commun.py](../../etapes/retrieval/rag_commun.py)
- Jeu d'evals : [evals/questions.json](../../etapes/retrieval/evals/questions.json)
