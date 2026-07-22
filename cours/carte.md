# La carte du cours

> Refaire à la main chaque couche d'une application LLM — appel HTTP brut,
> sampling, outils, boucle d'agent, RAG, MCP, serveur d'inférence,
> observabilité — puis promouvoir ce qui a été compris dans un **framework
> maison** dont on maîtrise chaque ligne et sait dire *pourquoi* elle est là.
> Terrain : un petit modèle local, dont les pannes sont le matériau.

## Comment le repo est organisé

| Dossier | Contenu |
|---|---|
| `cours/` | la prose — un dossier par domaine, aucun numéro dans les chemins |
| `etapes/` | les scripts : une étape = un mécanisme, numérotés par domaine |
| `src/framework/` | le framework maison, sédiment des leçons acquises |
| `cours/_archive/` | ce qui a été écrit avant d'être vécu, et le journal du parcours |

Trois règles :

1. **À la main d'abord, l'outil ensuite.** On ne débogue que ce qu'on a écrit.
2. **Une leçon acquise laisse du code dans `src/framework/`.** Sinon elle n'est
   pas finie — le framework n'est pas un chapitre final, c'est le dépôt continu.
3. **Mesurer.** Un pipeline LLM sans évaluation chiffrée est une démo.

---

## Fondamentaux — [le socle sans framework](fondamentaux/index.md)

L'anatomie de toute application LLM, en Python pur.

- [Chat, historique et contexte](fondamentaux/chat-historique-contexte.md) —
  modèle stateless, streaming, troncature et compaction
- [Sampling et prompting](fondamentaux/sampling-et-prompting.md) —
  temperature, top-k, top-p ; zero/few-shot, chain-of-thought
- [Function calling](fondamentaux/function-calling.md) —
  schémas JSON, parsing, exécution, renvoi
- [Boucle d'agent](fondamentaux/boucle-agent.md) —
  lire/écrire/exécuter dans une boucle, et les garde-fous que ça impose
- [Structured output](fondamentaux/structured-output.md) —
  décodage contraint, validation Pydantic, retry

Trois sujets de cette couche n'ont pas encore leur leçon, et ce sont les
derniers endroits où le parcours accepte une boîte noire : la
**tokenisation** (ce que coûte vraiment le français accentué ou un bloc
YAML), le **template de chat** (le texte que le modèle voit réellement) et
l'**attention / KV cache**.

## Retrieval — [le RAG, mesuré](retrieval/rag-a-la-main.md)

D'abord [entièrement à la main](retrieval/rag-a-la-main.md) :

- [Embeddings](retrieval/embeddings.md) · [similarité cosinus](retrieval/similarite-cosinus.md)
  · [chunking](retrieval/chunking.md) · [indexation](retrieval/indexation.md)
  · [recherche top-k](retrieval/recherche-top-k.md) · [RAG complet](retrieval/rag-complet.md)
  · [evals](retrieval/evals.md)

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
  [LLM-as-judge](retrieval/llm-as-judge.md) *(juge ≠ générateur)* ·
  [RAGAS / DeepEval](retrieval/ragas-deepeval.md) ·
  [tableau comparatif](retrieval/tableau-final.md) ·
  [RAG vs fine-tuning](retrieval/rag-vs-fine-tuning.md)

Enfin [en service](retrieval/service-et-craftsmanship.md) :

- [Service FastAPI](retrieval/service-fastapi.md) ·
  [backend commutable local/cloud](retrieval/backend-commutable.md) ·
  [tests, typing, packaging](retrieval/tests-typing-packaging.md)

## MCP — [un serveur et un client](mcp/serveur.md)

- [Serveur MCP Python](mcp/serveur-mcp-python.md) ·
  [transports stdio et HTTP](mcp/transports-stdio-http.md) ·
  [intégration à un client existant](mcp/integration-claude-code.md)
- [Client MCP minimal](mcp/client-mcp-minimal.md) — `tools/list`, `tools/call`
- [Le handshake MCP](mcp/handshake-mcp.md) — le protocole sous le SDK
- [Le versant sécurité](mcp/securite.md) :
  [prompt injection indirecte](mcp/prompt-injection-indirecte.md)

## Agent — [l'agent maison, sandboxé](agent/garde-fous.md)

- [Garde-fous](agent/garde-fous.md) : [hook `tool_call`](agent/hook-tool-call.md) ·
  [conteneur et moindre privilège](agent/conteneur-moindre-privilege.md)
- [Outils et mémoire](agent/outils-et-memoire.md) :
  [outil Home Assistant](agent/outil-home-assistant.md) ·
  [mémoire versionnée](agent/memoire-versionnee.md)
- [Régimes d'agents](agent/regimes-agents.md) :
  [mode RPC/SDK](agent/mode-rpc-sdk.md) ·
  [quatre régimes, même boucle](agent/quatre-regimes.md) ·
  [note de conception](agent/note-de-conception.md)

## Inférence — [servir un modèle](inference/deploiement.md)

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

---

## [Le framework maison](framework/index.md)

L'aboutissement, construit en continu et jamais d'un bloc.

- [Architecture modulaire](framework/architecture-modulaire.md) — briques
  enfichables : client LLM, outils, boucle, mémoire, retrieval, evals
- [Clean code](framework/clean-code.md) — typing, Pydantic, pytest, packaging
- [Évolutivité sans friction](framework/evolutivite.md) — ajouter un outil ou
  un provider = un fichier, zéro modification du cœur
- [Routage multi-agentique](framework/routage-multi-agentique.md) —
  superviseur/ouvriers, arbitrage coût/latence/qualité
- [Dogfooding](framework/dogfooding.md) — les autres domaines le consomment
- [Sortie précoce et semver](framework/sortie-precoce-semver.md) — 0.0.1 dès
  les premières briques, incréments ensuite
