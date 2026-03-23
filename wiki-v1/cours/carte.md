# La carte du cours

> Refaire à la main chaque couche d'une application LLM — appel HTTP brut,
> sampling, outils, boucle d'agent, RAG, MCP, serveur d'inférence,
> observabilité — puis promouvoir ce qui a été compris dans un **framework
> maison** dont on maîtrise chaque ligne et sait dire *pourquoi* elle est là.
> Terrain : un petit modèle local, dont les pannes sont le matériau.

## Comment le repo est organisé

| Dossier                                               | Contenu                                                               |
| ----------------------------------------------------- | --------------------------------------------------------------------- |
| `cours/`                                              | la prose — un dossier par domaine, aucun numéro dans les chemins      |
| `etapes/`                                             | les scripts : une étape = un mécanisme, numérotés par domaine         |
| `src/framework/`                                      | le framework maison, sédiment des leçons acquises                     |
| [`cours/glossaire/`](glossaire/index.md)              | les termes qui n'ont pas de leçon                                     |
| [`cours/_processus/`](_processus/generation-token.md) | les chaînes techniques, décrites une seule fois et rendues en schémas |
| `cours/_archive/`                                     | ancienne version, incomplete et avec un français très mal formulé.    |

Trois règles :

1. **À la main d'abord, l'outil ensuite.** On ne débogue que ce qu'on a écrit.
2. **Un chapitre acquis laisse du code dans `src/framework/` ** si possible.   — le framework n'est pas un chapitre final, c'est le dépôt continu.
3. **Mesurer.** Un pipeline LLM sans évaluation chiffrée est une démo.

Un titre sans lien désigne une leçon prévue et pas encore écrite.

---

## Fondamentaux — le socle sans framework

L'anatomie de toute application LLM, en Python pur. Ce qui se passe à
l'intérieur d'un appel au modèle et de sa boucle immédiate — vrai quel que
soit l'usage qu'on en fera ensuite.

Construire :

- [Chat, historique et contexte](fondamentaux/chat-historique-contexte.md) —
  modèle stateless, streaming, troncature et compaction
- [Sampling](fondamentaux/sampling.md) —
  temperature, top-k, top-p, le tirage et la portée de la seed
- [Prompting](fondamentaux/prompting.md) —
  zero/few-shot, chain-of-thought, ReAct, prompt système
- [Function calling](fondamentaux/function-calling.md) —
  schémas JSON, parsing, exécution, renvoi
- [Boucle d'agent](fondamentaux/boucle-agent.md) —
  lire/écrire/exécuter dans une boucle, et les garde-fous que ça impose
- [Structured output](fondamentaux/structured-output.md) —
  décodage contraint, validation Pydantic, retry

Ouvrir la boîte noire — ce que le modèle voit et ce qu'il calcule :

- [Tokenisation](fondamentaux/tokenisation.md) — l'unité dans laquelle tout
  se compte : contexte, plafonds, coût
- [Le template de chat](fondamentaux/template-de-chat.md) — la liste de
  messages redevient le texte unique que le modèle lit vraiment
- [Attention et KV cache](fondamentaux/attention-et-kv-cache.md) — pourquoi
  le 1er token est lent, les suivants rapides, et le contexte cher

## Le framework maison — la colonne vertébrale

Il n'arrive pas à la fin : il se remplit à chaque leçon acquise. Sa place
ici, en deuxième, dit sa fonction — c'est là que les briques des autres
domaines viennent se déposer, et c'est de là qu'on les reprend.

Ce qu'on dépose, et comment :

- [Promotion](framework/promotion.md) — quand une leçon dépose du code, ce
  qu'elle dépose, et ce qui disqualifie une brique
- [Architecture modulaire](framework/architecture-modulaire.md) — briques
  enfichables : client LLM, outils, boucle, mémoire, retrieval, evals
- [Évolutivité sans friction](framework/evolutivite.md) — ajouter un outil ou
  un provider = un fichier, zéro modification du cœur
- [Sortie précoce et semver](framework/sortie-precoce-semver.md) — 0.0.1 dès
  les premières briques, incréments ensuite
- [Dogfooding](framework/dogfooding.md) — les autres domaines le consomment

Les briques transverses, celles qu'aucun domaine ne possède seul :

- [Providers](framework/providers.md) — l'abstraction du client LLM,
  local ou cloud, commutable par config
- [Service](framework/service.md) — exposer une brique en HTTP
- [Routage multi-agentique](framework/routage-multi-agentique.md) —
  superviseur/ouvriers, arbitrage coût/latence/qualité
- Evals — les trois familles, la non-régression, et pourquoi un score
  global unique ne répare rien
- [LLM-as-judge](framework/llm-as-judge.md) — juge ≠ générateur

Le craftsmanship, qui monte avec les leçons :

- [Clean code](framework/clean-code.md) — typing, Pydantic, pytest, packaging
- [Tests, typing, packaging](framework/tests-typing-packaging.md) — ce qu'une
  brique doit tenir pour être promue

## Agent — le harnais

Ce qui sépare une boucle `while` d'un harnais. Le domaine part de la
[boucle d'agent](fondamentaux/boucle-agent.md) des fondamentaux et lui ajoute
ce qui la rend tenable : ce qui la fiabilise, ce qui la nourrit sans la
noyer, ce qui la borne.

Fiabiliser la boucle :

- Fiabilité du client — timeout, retry, backoff, 429, coupure de stream en
  cours, et la ré-exécution d'un outil qui n'est pas idempotent
- Conception d'un outil — nom et description **sont du prompt** ; forme du
  résultat rendu au modèle, troncature d'une sortie énorme, erreurs
  actionnables
- Budget de contexte — qui occupe la fenêtre entre system, outils, historique
  et documents, et dans quel ordre on évince

Étendre la boucle :

- Sous-agents — contexte isolé, outils propres, rapport en retour ; à ne pas
  confondre avec le [routage](framework/routage-multi-agentique.md)
- Skills — divulgation progressive : donner une capacité sans payer son
  contexte tant qu'elle ne sert pas
- Les outils MCP dans la boucle — comment un outil distant devient
  indiscernable d'un outil natif dans le registre

Borner la boucle :

- [Garde-fous](agent/garde-fous.md) : [hook `tool_call`](agent/hook-tool-call.md) ·
  [conteneur et moindre privilège](agent/conteneur-moindre-privilege.md)
- [Outils et mémoire](agent/outils-et-memoire.md) :
  [outil Home Assistant](agent/outil-home-assistant.md) ·
  [mémoire versionnée](agent/memoire-versionnee.md)
- [Régimes d'agents](agent/regimes-agents.md) :
  [mode RPC/SDK](agent/mode-rpc-sdk.md) ·
  [quatre régimes, même boucle](agent/quatre-regimes.md) ·
  [note de conception](agent/note-de-conception.md)

Mesurer la boucle :

- Evals de trajectoire — la boucle termine-t-elle, le bon outil a-t-il été
  appelé, combien coûte une tâche

## Retrieval — [le RAG, mesuré](retrieval/rag-a-la-main.md)

D'abord [entièrement à la main](retrieval/rag-a-la-main.md) :

- [Embeddings](retrieval/embeddings.md) · [similarité cosinus](retrieval/similarite-cosinus.md)
  · [chunking](retrieval/chunking.md) · [indexation](retrieval/indexation.md)
  · [recherche top-k](retrieval/recherche-top-k.md) · [RAG complet](retrieval/rag-complet.md)
  · [evals du RAG](retrieval/evals.md)

Puis [outillé avec Qdrant](retrieval/qdrant.md) :

- [Migration Qdrant](retrieval/migration-qdrant.md) ·
  [retrieval hybride](retrieval/retrieval-hybride.md) ·
  [re-ranking du top-k](retrieval/re-ranking-top-k.md) ·
  [filtres métadonnées](retrieval/filtres-metadonnees.md) ·
  [evals comparatives](retrieval/evals-comparatives.md)
- Les mécaniques que Qdrant cache, à savoir refaire à la main :
  [BM25](retrieval/bm25.md) · [re-ranking](retrieval/re-ranking.md)
  *(bi-encoder vs cross-encoder)* · [HNSW](retrieval/hnsw.md)

Puis [avec l'outillage standard](retrieval/llamaindex-outillage.md) :

- [LlamaIndex](retrieval/llamaindex.md) ·
  [RAGAS / DeepEval](retrieval/ragas-deepeval.md) ·
  [tableau comparatif](retrieval/tableau-final.md) ·
  [RAG vs fine-tuning](retrieval/rag-vs-fine-tuning.md)

## MCP — [un serveur et un client](mcp/serveur.md)

- [Serveur MCP Python](mcp/serveur-mcp-python.md) ·
  [transports stdio et HTTP](mcp/transports-stdio-http.md) ·
  [intégration à un client existant](mcp/integration-claude-code.md)
- [Client MCP minimal](mcp/client-mcp-minimal.md) — `tools/list`, `tools/call`
- [Le handshake MCP](mcp/handshake-mcp.md) — le protocole sous le SDK
- [Le versant sécurité](mcp/securite.md) :
  [prompt injection indirecte](mcp/prompt-injection-indirecte.md)

## Inférence — [servir un modèle](inference/deploiement.md)

- Quantization — ce que coûte un poids, et ce qui tient vraiment sur la carte
- [vLLM sur RTX 2060](inference/vllm-sur-rtx-2060.md)
- [Benchmark vs Ollama](inference/benchmark.md) :
  [débit et latence](inference/metriques-debit-latence.md) ·
  [charge concurrente](inference/charge-concurrente.md)
- [Analyse](inference/analyse-et-verdict.md) :
  [mécanismes vLLM](inference/mecanismes-vllm.md) *(batching continu, KV cache,
  PagedAttention)* · [verdict](inference/verdict-ollama-vs-vllm.md)
- [Prompt caching](inference/prompt-caching.md) — ne pas re-payer le préfixe stable

## Production — [ce qui rend un pipeline exploitable](production/observabilite.md)

- [Observabilité](production/observabilite.md) :
  [Langfuse](production/langfuse-self-hoste.md) ·
  [tracer les appels](production/tracer-les-appels.md) ·
  [suivi des coûts](production/suivi-des-couts.md)
- [Sécurité](production/securite.md) :
  [OWASP Top 10 LLM](production/owasp-top-10-llm.md) ·
  [tests adversariaux](production/tests-adversariaux.md) ·
  [threat model](production/threat-model-jarvis.md)
- [Culture fine-tuning](production/culture-fine-tuning.md) :
  [ce qu'est LoRA](production/lora.md) et
  [le faire tourner](production/lora-sur-colab.md) — surtout, savoir quand ce
  n'est *pas* la réponse

## Multimodal — [capitaliser sur le pipeline vocal](multimodal/documenter-existant.md)

- [Étude de cas STT/TTS](multimodal/etude-de-cas-stt-tts.md) ·
  [anatomie d'un assistant vocal local](multimodal/post-anatomy.md)
- [Vision locale](multimodal/vision-locale.md) : [VLM local](multimodal/vlm-local.md)
- [Ouvertures](multimodal/ouvertures.md) : [caméra et OCR](multimodal/camera-et-ocr.md) ·
  [API cloud équivalentes](multimodal/api-cloud-equivalentes.md)
