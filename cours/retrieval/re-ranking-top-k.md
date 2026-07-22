# 2.2.3 Re-ranking du top-k

> **Leçon de la section [2.2 v0.0.2 — Qdrant + retrieval avancé](../2.2-v0.0.2-qdrant-retrieval-avance.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir *(→ déclenche l'[entrée glossaire re-ranking](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.2-re-ranking/1.2.2-re-ranking.md))*
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Appliquer l'entonnoir *rappel d'abord, précision ensuite* à notre
chaîne : l'[hybride](../2.2.2-retrieval-hybride/2.2.2-retrieval-hybride.md)
ramène large (top-20), le re-ranker lit chaque paire
(question, chunk) **ensemble** et choisit le vrai top-5. La théorie
complète (bi-encoder vs cross-encoder) est dans
l'[entrée glossaire](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.2-re-ranking/1.2.2-re-ranking.md) —
ici, on branche et on mesure.

## Le savoir

- **Le branchement** : une étape de plus dans `chercher()` —
  `candidats = hybride(question, 20)` →
  `top5 = rerank(question, candidats)`. L'interface de la brique
  retrieval ne change pas : le re-ranking est un détail interne
  (l'architecture de
  [1.3.1](../../../01-llm-from-scratch/1.3-framework-maison/1.3.1-architecture-modulaire/1.3.1-architecture-modulaire.md)
  paye ici).
- **Deux implémentations à comparer sur ce module** :
  1. **cross-encoder dédié** (bge-reranker-base via
     sentence-transformers — tourne sur la RTX 2060, quelques dizaines
     de ms par paire) : le choix « production » ;
  2. **LLM-as-reranker** (Qwen3 note chaque paire 0-10, sortie
     contrainte [1.1.5](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.5-structured-output/1.1.5-structured-output.md)) :
     zéro dépendance nouvelle, plus lent — parfait pour comprendre.
- **Ce qu'on mesure** ([2.2.5](../2.2.5-evals-comparatives/2.2.5-evals-comparatives.md)) :
  le **rang du bon document** avant/après (MRR si on veut un chiffre
  unique), et la **latence ajoutée** — le re-ranking est un achat de
  précision payé en millisecondes, le tableau doit montrer les deux
  colonnes.
- **Interaction avec k** : re-ranker permet d'*élargir* le rappel
  (top-20 au lieu de top-6) sans polluer le prompt — c'est le couple
  (rappel large + tri fin) qui gagne, pas le re-ranker seul.

## En pratique

Ajouter `rerank()` à `rag_commun`, avec les deux implémentations
derrière la même signature ; rejouer le jeu d'evals dans les quatre
configurations (dense seul / hybride / dense+rerank / hybride+rerank) —
une ligne de tableau chacune.

## Pièges connus

- Re-ranker 20 candidats pour en garder 15 : l'entonnoir doit
  resserrer réellement, sinon c'est de la latence gratuite.
- Tronquer les chunks avant scoring (fenêtre du cross-encoder) sans le
  savoir : le re-ranker juge des débuts de chunks — vérifier la limite
  du modèle.
- Garder le re-ranker si le delta est nul sur les evals : sur un petit
  corpus bien chunké, ça arrive — un composant sans delta se retire
  (et ça aussi, ça se raconte en entretien).

## Question d'entretien

> « Où placez-vous le re-ranking dans votre chaîne et pourquoi pas sur
> tout le corpus ? »
> Après le retrieval rapide (rappel), sur 20-50 candidats seulement :
> le cross-encoder coûte un passage modèle par paire — l'entonnoir
> achète la précision là où elle compte, au prix marginal minimal.

## Références

- [Entrée glossaire re-ranking](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.2-re-ranking/1.2.2-re-ranking.md)
  — la mécanique bi- vs cross-encoder
- bge-reranker (BAAI) — le modèle self-hostable de référence
