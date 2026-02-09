# LlamaIndex

> [carte du cours](../carte.md)

## L'essentiel

Refaire la chaîne complète en **LlamaIndex** — le framework « centré
RAG » du marché — et tenir un double registre : ce qu'il **apporte**
(vitesse, intégrations) et ce qu'il **cache** (prompts par défaut,
paramètres implicites). L'exercice n'est pas d'apprendre un outil :
c'est de mapper chaque abstraction sur le script maison qu'on a déjà
écrit.

## Le savoir

- **La table de correspondance** (le cœur de la leçon) :

  | Concept LlamaIndex | Notre v0.0.1/v0.0.2 |
  |---|---|
  | `SimpleDirectoryReader` | lecture des `.md` |
  | `Node` + parsers (`MarkdownNodeParser`) | [chunking](chunking.md) + métadonnées |
  | `OllamaEmbedding` | [embeddings](embeddings.md) httpx |
  | `VectorStoreIndex` + `QdrantVectorStore` | [indexation](indexation.md)/[Qdrant](migration-qdrant.md) |
  | `retriever` (+ `similarity_top_k`) | [recherche top-k](recherche-top-k.md) |
  | `node_postprocessors` (rerank) | [re-ranking](re-ranking-top-k.md) |
  | `query_engine` | [RAG complet](rag-complet.md) |

- **Ce que le framework cache — à documenter explicitement** : le
  **prompt de synthèse par défaut** (en anglais, sans notre grounding
  ni notre « je ne sais pas »), le chunking par défaut (1024/20 si on
  ne dit rien), le `response_mode` (compact/refine — plusieurs appels
  LLM sans qu'on le voie), les retries silencieux.
- **La règle du module** : chaque défaut caché est soit **repris en
  main** (prompts custom, parser markdown), soit **accepté et noté**.
  Le README liste les deux colonnes — c'est le livrable « ce que le
  framework apporte / cache » du sommaire.
- **À situer** : LangChain/LangGraph (chaînes et graphes généralistes),
  Haystack, RAGFlow ([roadmap couche 2](../_archive/roadmap.md)) — un
  paragraphe chacun, pas plus.

## En pratique

Réimplémenter la chaîne en LlamaIndex branchée sur le **même Qdrant**
et le **même modèle**, rejouer le jeu d'evals : l'écart avec la v0.0.2
mesure exactement l'effet des défauts du framework — chaque écart
s'explique ou se corrige.

## Pièges connus

- Laisser le prompt par défaut : les scores d'hallucination bougent et
  on accuse le framework — c'est le prompt qui a changé, pas la
  mécanique.
- Empiler les abstractions non comprises (`response_mode="tree_summarize"`)
  parce qu'un tutoriel le montrait : chaque option ajoutée doit avoir
  sa ligne d'ablation.
- Comparer LlamaIndex-avec-ses-défauts à notre chaîne réglée et
  conclure que « le framework est moins bon » : comparer à
  configuration égale, puis comparer les défauts.

## Se tester

> « Que vous apporte un framework RAG, et que vous cache-t-il ? »
> Apports : intégrations, vitesse de mise en œuvre, patterns éprouvés.
> Cachés : prompts par défaut, paramètres implicites, appels LLM
> multiples — et je peux le détailler parce que j'ai écrit chaque
> maillon à la main avant.

## Références

- Doc LlamaIndex (query engine, node parsers, vector stores)
- La [PROGRESSION du module](../_archive/journal/progression-fondamentaux.md) — le registre
  apports/cachés au fil de l'eau
