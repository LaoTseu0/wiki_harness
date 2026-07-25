# Recherche — mémoire d'agent et knowledge graphs agentiques (juillet 2026)

> Brute de recherche, à fusionner dans le Parcours 6 sur validation.
> Réserve : X (Twitter) n'a pas pu être lu directement (threads sous authentification).
> Ce qui suit vient de blogs, papiers et posts indexés qui citent le discours praticien
> (Karpathy, Zep, Mem0 nommés). Tendance fiable ; ce ne sont pas des tweets bruts.
> Les papiers arXiv sont cités par leur titre, pas tous ouverts en détail.

## Les tendances

### 1. La mémoire est une discipline à part entière
Benchmarks dédiés, trade-offs mesurés, écosystème. Marqueur : le rapport *State of AI
Agent Memory 2026* de Mem0.

### 2. Le RAG vectoriel « vanilla » échoue pour la mémoire d'agent
Raison structurelle, pas cosmétique. Le RAG vise de grands corpus hétérogènes ; la
mémoire d'agent porte sur des flux de dialogue bornés et corrélés. Partage :
le vectoriel gagne sur la proximité sémantique récente ; le graphe gagne dès qu'il
faut du multi-hop ou un ordre temporel précis.

### 3. Knowledge graphs temporels (Zep / Graphiti) — la vedette
Modèle bi-temporel : chaque fait porte quand il est devenu vrai, quand il a cessé de
l'être, et sa provenance. Quand un fait change, l'ancien n'est pas supprimé — sa
fenêtre de validité se ferme. Deux capacités neuves :
- raisonnement à une date (« que savait-on en janvier ? ») ;
- traçabilité de chaque réponse jusqu'à son épisode source.

### 4. « Agentic » knowledge graph — le glissement sémantique
Le graphe n'est plus une table de consultation passive : c'est l'espace sur lequel
l'agent planifie, agit, se critique et se souvient. L'agent écrit, indexe et relie
ses propres souvenirs.
- A-MEM — notes interconnectées, principe Zettelkasten, réorganisation continue.
- SAGE — moteur de graphe-mémoire auto-évolutif (novelty gate).
- HAGE — évolution du graphe pondéré par renforcement.
- MAGMA — multi-graphe : sépare la proximité associative de la structure causale
  (raisonner sur le pourquoi, pas seulement le quoi).
- SelfMem — mémoire auto-optimisante.

### 5. L'hybride est le standard de production
Vecteur + graphe + clé-valeur, pas l'un contre l'autre. Mem0 (~48k stars, Série A
24 M$ oct. 2025) combine vectoriel et couche graphe optionnelle ; limite reconnue :
absence de modèle temporel, là où Zep versionne les faits.

### 6. Nouvelle surface d'attaque — la contamination de mémoire
Empoisonner la mémoire long-terme est un sujet de sécurité en soi (MemGuard,
isolation d'écriture de GAM). Prolonge le fil sécurité du P5 et l'OWASP du P9.

## Les outils, filtre local-first

- **Graphiti** — open-source, 20k+ stars, knowledge graph temporel pour mémoire
  d'agent. Tourne hors-ligne sur **Neo4j**, **FalkorDB** ou **Kuzu**.
- **Kuzu** — base de graphe embarquée, « le SQLite du graphe ». Taillée pour un
  mono-utilisateur local.
- **neo4j-labs/agent-memory** — système mémoire graphe-natif signé Neo4j.
- **Mem0**, **Cognee** — couches mémoire hybrides auto-hébergeables.
- Lien au P5 : **Graphiti expose un serveur MCP v1.0** (nov. 2025). La mémoire comme
  outil distant, consommée via le protocole MCP.

## Correspondance avec la conception du projet (REGLES)

Le projet prévoit déjà quatre stores + des processus. La recherche 2026 les valide :

| Plan du projet (REGLES) | Écho dans la recherche |
|---|---|
| store vectoriel (le sens) | RAG vectoriel classique |
| store stateful (l'état exact) | clé-valeur des architectures hybrides |
| graphe temporel (liens datés, scoring, decay) | Zep / Graphiti bi-temporel |
| wiki-LLM (connaissance auto-rédigée) | mémoire auto-écrite (A-MEM, SelfMem) |
| processus : scoring, decay, consolidation (mode Dream), auto-apprentissage | mémoire auto-évolutive (SAGE, HAGE) |

## Tension à trancher pour le cours

Règle « aucun concept boîte noire » vs poids d'un moteur de graphe temporel complet.
Bâtir un Graphiti maison est lourd ; le consommer (comme Ollama au P1, Qdrant au
vectoriel) serait l'autre voie. Décision à prendre au moment de rédiger P6 /
memoire.md.

## Sources

- State of AI Agent Memory 2026 — https://mem0.ai/blog/state-of-ai-agent-memory-2026
- Temporal Knowledge Graph (Zep) — https://www.getzep.com/ai-agents/temporal-knowledge-graph/
- Zep: A Temporal KG Architecture for Agent Memory — https://arxiv.org/abs/2501.13956
- Graphiti (Neo4j) — https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/
- neo4j-labs/agent-memory — https://github.com/neo4j-labs/agent-memory
- Vector DBs vs Graph RAG for Agent Memory — https://machinelearningmastery.com/vector-databases-vs-graph-rag-for-agent-memory-when-to-use-which/
- Graphs Meet AI Agents (taxonomie) — https://arxiv.org/pdf/2506.18019
- Graph-Augmented LLM Agents (survey) — https://arxiv.org/pdf/2507.21407
- SAGE — https://arxiv.org/pdf/2605.12061
- Best AI Agent Memory Frameworks 2026 (Atlan) — https://atlan.com/know/best-ai-agent-memory-frameworks-2026/
