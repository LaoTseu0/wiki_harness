# v0.0.3 — LlamaIndex + outillage standard

> [carte du cours](../carte.md)

## Vue d'ensemble

Parler le vocabulaire du marché : refaire la chaîne dans un framework
(LlamaIndex), documenter ce qu'il apporte et ce qu'il **cache** — on
est en position de le voir, puisque chaque maillon caché a été écrit à
la main en [2.1](rag-a-la-main.md).
En parallèle, industrialiser les evals : jeu étendu, juge LLM, outils
standard (RAGAS/DeepEval), et les deux réponses d'entretien majeures
(tableau final, RAG vs fine-tuning).

## Contenu

- **[2.3.1 LlamaIndex](llamaindex.md)** —
      refaire la chaîne ; documenter apports et cachés
- **[2.3.2 LLM-as-judge](llm-as-judge.md)**
      — jeu étendu (~30 questions), **juge ≠ générateur**, choix
      documenté
- **[2.3.3 RAGAS / DeepEval](ragas-deepeval.md)**
      — passer le jeu dans l'outillage standard
- **[2.3.4 Tableau final](tableau-final.md)**
      — v0.0.1 → v0.0.2 → v0.0.3 dans le README
- **[2.3.5 RAG vs fine-tuning](rag-vs-fine-tuning.md)**
      — la réponse d'entretien, rédigée

## Synthèse

La v0.0.3 boucle la boucle du principe directeur : *à la main d'abord,
le framework ensuite* — et maintenant qu'on connaît chaque maillon, le
framework devient un choix éclairé, pas une boîte noire. Les evals
suivent le même mouvement : du script maison assumé vers l'outillage
que citent les offres, sans perdre la baseline. **Auto-contrôle** :
pour chaque abstraction LlamaIndex utilisée, savoir nommer le script
v0.0.1 qui fait la même chose.

## Livrable

Le tableau final trois générations dans le README + la réponse
RAG vs fine-tuning rédigée — les deux pièces d'entretien du module.
