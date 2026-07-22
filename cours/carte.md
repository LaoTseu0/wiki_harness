# Sommaire détaillé — Formation AI Engineer

> **Rôle de ce document** : table des matières sur trois niveaux du
> parcours complet. La stratégie, le marché et les justifications sont
> dans [roadmap.md](roadmap.md) ; ici, uniquement le *quoi* et le *dans
> quel ordre*. Document vivant, tenu en phase avec les PROGRESSION.md
> de chaque module.
> **Fil rouge** : chaque concept est d'abord écrit à la main (module 1),
> puis outillé (modules 2-7), et le tout converge vers un **framework
> maison** — l'aboutissement du parcours.
> **Convention transverse** : chaque script d'exercice a un `.md`
> compagnon court — docstring minimale dans le code.
> **Versionnage** : semver partout — tout livrable sort tôt en 0.0.1 et
> évolue incrémentalement ; les générations d'un projet sont des jalons
> successifs (0.0.1, 0.0.2…), jamais des réécritures fermées.
> **Ordre de passage** : 1 → 2 (6 en continu) → **5** → 3 → 4/7
> (le MCP avancé avant l'agent — décision du 21 juillet 2026).
> **Arborescence** : chaque section pointe vers son dossier
> `NN-module/x.y-section/` — le `.md` éponyme est le support du cours.
> **Légende** : ✅ acquis · 🔵 en cours · ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

---

## Module 1 — 01-llm-from-scratch : du socle au framework *(jamais fermé)*

### [1.1 Socle sans framework](01-llm-from-scratch/1.1-socle-sans-framework/1.1-socle-sans-framework.md) ✅ *(terminé le 20 juillet 2026)*

- ✅ [Chat CLI, historique et contexte](01-llm-from-scratch/1.1-socle-sans-framework/1.1.1-chat-cli-historique-contexte/1.1.1-chat-cli-historique-contexte.md)
  — streaming, gestion du contexte à la main (troncature, compaction)
- ✅ [Sampling et prompting](01-llm-from-scratch/1.1-socle-sans-framework/1.1.2-sampling-et-prompting/1.1.2-sampling-et-prompting.md)
  — temperature, top-k, top-p ; zero/few-shot, chain-of-thought
- ✅ [Function calling à la main](01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md)
  — schémas JSON, parsing, exécution, renvoi (= ReAct implémenté)
- ✅ [Mini-boucle d'agent](01-llm-from-scratch/1.1-socle-sans-framework/1.1.4-mini-boucle-agent/1.1.4-mini-boucle-agent.md)
  — pattern Pi : read/write/edit/bash dans une boucle while
- ✅ [Structured output](01-llm-from-scratch/1.1-socle-sans-framework/1.1.5-structured-output/1.1.5-structured-output.md)
  — extraction JSON validée Pydantic, retry sur JSON invalide

### [1.2 Glossaire exécutable](01-llm-from-scratch/1.2-glossaire-executable/1.2-glossaire-executable.md) *(continu, alimenté par les modules 2-7)*

- Règle d'entrée : un concept qu'un framework cache et qu'on ne saurait
  pas refaire en ~50 lignes → un exercice numéroté en Python pur ici,
  avec renvoi croisé depuis le module qui l'a introduit
- Entrées candidates déjà identifiées :
  - [**BM25**](01-llm-from-scratch/1.2-glossaire-executable/1.2.1-bm25/1.2.1-bm25.md) (retrieval lexical, ← module 2 v0.0.2) — implémentable à la main
  - [**Re-ranking**](01-llm-from-scratch/1.2-glossaire-executable/1.2.2-re-ranking/1.2.2-re-ranking.md) (ré-ordonner le top-k, ← module 2 v0.0.2)
  - [**HNSW**](01-llm-from-scratch/1.2-glossaire-executable/1.2.3-hnsw/1.2.3-hnsw.md) (l'index de Qdrant, ← module 2 v0.0.2) — version « comprendre
    et schématiser », pas implémenter
  - [**Prompt caching**](01-llm-from-scratch/1.2-glossaire-executable/1.2.4-prompt-caching/1.2.4-prompt-caching.md) (← couche 0 / module 3)
  - [**Handshake MCP**](01-llm-from-scratch/1.2-glossaire-executable/1.2.5-handshake-mcp/1.2.5-handshake-mcp.md) (`tools/list` / `tools/call`, ← module 5)
  - [**LoRA**](01-llm-from-scratch/1.2-glossaire-executable/1.2.6-lora/1.2.6-lora.md) (← module 6, culture)
- README anglais : « every entry is a runnable script » — pièce
  maîtresse du portfolio

### [1.3 Le framework maison](01-llm-from-scratch/1.3-framework-maison/1.3-framework-maison.md) *(release 0.0.1 dès les premières briques promues, puis semver en continu)*

- [**Architecture modulaire**](01-llm-from-scratch/1.3-framework-maison/1.3.1-architecture-modulaire/1.3.1-architecture-modulaire.md) : briques enfichables —
  client LLM (providers interchangeables), outils, boucle d'agent,
  mémoire, retrieval, evals
- [**Clean code production-grade**](01-llm-from-scratch/1.3-framework-maison/1.3.2-clean-code-production-grade/1.3.2-clean-code-production-grade.md) : typing, Pydantic, tests pytest,
  packaging, docstrings — le « software craftsmanship » des offres
- [**Évolutivité sans friction**](01-llm-from-scratch/1.3-framework-maison/1.3.3-evolutivite-sans-friction/1.3.3-evolutivite-sans-friction.md) : ajouter un outil, un provider ou un
  agent = un fichier, zéro modification du cœur
- [**Routage multi-agentique**](01-llm-from-scratch/1.3-framework-maison/1.3.4-routage-multi-agentique/1.3.4-routage-multi-agentique.md) : superviseur/ouvriers, routage
  coût/latence/qualité — le
  [routeur multi-modèles](../homelab/architecture/router-multi-model.md) devenu code
- [**Dogfooding**](01-llm-from-scratch/1.3-framework-maison/1.3.5-dogfooding/1.3.5-dogfooding.md) : les modules suivants (RAG, agent, MCP) consomment le
  framework — chaque module le fait évoluer
- [**Sortie précoce**](01-llm-from-scratch/1.3-framework-maison/1.3.6-sortie-precoce-semver/1.3.6-sortie-precoce-semver.md) : pas de big-bang final — 0.0.1 avec les premières
  briques (client LLM, outils, `rag_commun` promu), incréments ensuite

---

## Module 2 — 02-homelab-rag : le RAG complet, mesuré 🔵

### [2.1 v0.0.1 — le RAG entièrement à la main](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1-v0.0.1-rag-a-la-main.md) 🔵

- ✅ [01 Embeddings](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.1-embeddings/2.1.1-embeddings.md) : texte → vecteur 768 dims via Ollama, norme = 1
- ✅ [02 Similarité cosinus](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.2-similarite-cosinus/2.1.2-similarite-cosinus.md) : écrite par Anthony (produit scalaire,
  normes, angle) + géométrie visuelle
- ⚪ [03 Chunking](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.3-chunking/2.1.3-chunking.md) : découper les `.md` par sections, source en métadonnée
- ⚪ [04 Indexation](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.4-indexation/2.1.4-indexation.md) : pipeline chunk → embedding → SQLite
- ⚪ [05 Recherche](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.5-recherche-top-k/2.1.5-recherche-top-k.md) : question → embedding → top-k (le « R » de RAG)
- ⚪ [06 RAG complet](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.6-rag-complet/2.1.6-rag-complet.md) : retrieval → prompt avec contexte → réponse citée
- ⚪ [07 Evals](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.7-evals/2.1.7-evals.md) : jeu de questions, score déterministe, baseline chiffrée
  *(baseline provisoire mesurée : retrieval 7/12, génération 7/12,
  zéro hallucination)*

### [2.2 v0.0.2 — Qdrant + retrieval avancé](02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2-v0.0.2-qdrant-retrieval-avance.md) ⚪

- [Migration Qdrant](02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.1-migration-qdrant/2.2.1-migration-qdrant.md) (conteneur docker homelab)
- [Retrieval hybride](02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.2-retrieval-hybride/2.2.2-retrieval-hybride.md) : BM25 + vecteurs *(→ entrée glossaire BM25)*
- [Re-ranking du top-k](02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.3-re-ranking-top-k/2.2.3-re-ranking-top-k.md) *(→ entrée glossaire)*
- [Filtres métadonnées](02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.4-filtres-metadonnees/2.2.4-filtres-metadonnees.md) (par dossier, par type de doc)
- [Evals comparatives](02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.5-evals-comparatives/2.2.5-evals-comparatives.md) : tableau comparatif v0.0.1 → v0.0.2

### [2.3 v0.0.3 — LlamaIndex + outillage standard](02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3-v0.0.3-llamaindex-outillage-standard.md) ⚪

- [LlamaIndex](02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3.1-llamaindex/2.3.1-llamaindex.md) : refaire la chaîne ; documenter ce que le framework
  apporte / cache
- [LLM-as-judge](02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3.2-llm-as-judge/2.3.2-llm-as-judge.md) : jeu étendu (~30 questions) — **juge ≠
  générateur** (jamais Qwen3 4B jugeant Qwen3 4B), choix documenté
- [RAGAS / DeepEval](02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3.3-ragas-deepeval/2.3.3-ragas-deepeval.md) : passer le jeu dans l'outillage standard
- [Tableau final](02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3.4-tableau-final/2.3.4-tableau-final.md) v0.0.1 → v0.0.2 → v0.0.3 dans le README
- [RAG vs fine-tuning](02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3.5-rag-vs-fine-tuning/2.3.5-rag-vs-fine-tuning.md) : réponse d'entretien rédigée, pourquoi RAG ici

### [2.4 Service et craftsmanship](02-homelab-rag/2.4-service-et-craftsmanship/2.4-service-et-craftsmanship.md) ⚪ *(ajouté le 21 juillet 2026)*

- [**Service FastAPI**](02-homelab-rag/2.4-service-et-craftsmanship/2.4.1-service-fastapi/2.4.1-service-fastapi.md) : `POST /ask` → réponse +
  sources (réutilisé par le MCP du module 5, tracé au module 6)
- [**Backend commutable local/cloud**](02-homelab-rag/2.4-service-et-craftsmanship/2.4.2-backend-commutable/2.4.2-backend-commutable.md) par config : abstraction provider
  (future brique du framework, et la réponse à l'angle mort cloud)
- [**Tests, typing, packaging**](02-homelab-rag/2.4-service-et-craftsmanship/2.4.3-tests-typing-packaging/2.4.3-tests-typing-packaging.md) : pytest sur la chaîne (le 07 en est le germe),
  typing sur la bibliothèque commune, packaging à la promotion

---

## Module 5 — MCP : un serveur ET un client ⚪ *(passage avancé avant le module 3 — décision du 21 juillet 2026)*

### [5.1 Le serveur](05-homelab-mcp/5.1-serveur/5.1-serveur.md)

- [Serveur MCP Python](05-homelab-mcp/5.1-serveur/5.1.1-serveur-mcp-python/5.1.1-serveur-mcp-python.md) exposant le homelab en lecture : conteneurs,
  entités HA, recherche dans la doc (réutilise le module 2)
- [Transports stdio et HTTP](05-homelab-mcp/5.1-serveur/5.1.2-transports-stdio-http/5.1.2-transports-stdio-http.md) : stdio d'abord, HTTP ensuite
- [Intégration Claude Code](05-homelab-mcp/5.1-serveur/5.1.3-integration-claude-code/5.1.3-integration-claude-code.md) : branchement sur un client existant + doc

### [5.2 Le client](05-homelab-mcp/5.2-client/5.2-client.md)

- [Client MCP minimal](05-homelab-mcp/5.2-client/5.2.1-client-mcp-minimal/5.2.1-client-mcp-minimal.md) : découverte `tools/list`, appel `tools/call`
  *(→ entrée glossaire handshake MCP)*

### [5.3 Le versant sécurité](05-homelab-mcp/5.3-securite/5.3-securite.md)

- [Prompt injection indirecte](05-homelab-mcp/5.3-securite/5.3.1-prompt-injection-indirecte/5.3.1-prompt-injection-indirecte.md) : que se passe-t-il si un document indexé
  contient une instruction malveillante ? — à documenter (sujet d'entretien)

---

## Module 3 — jarvis-agent : l'agent maison sandboxé ⚪

### [3.1 Garde-fous et sécurité d'abord](03-jarvis-agent/3.1-garde-fous-et-securite/3.1-garde-fous-et-securite.md)

- [Hook `tool_call`](03-jarvis-agent/3.1-garde-fous-et-securite/3.1.1-hook-tool-call/3.1.1-hook-tool-call.md) : liste noire de commandes destructives
  + validation humaine (human-in-the-loop)
- [Conteneur et moindre privilège](03-jarvis-agent/3.1-garde-fous-et-securite/3.1.2-conteneur-moindre-privilege/3.1.2-conteneur-moindre-privilege.md) : aucun accès aux partages famille

### [3.2 Outils et mémoire](03-jarvis-agent/3.2-outils-et-memoire/3.2-outils-et-memoire.md)

- [Outil custom `home_assistant`](03-jarvis-agent/3.2-outils-et-memoire/3.2.1-outil-home-assistant/3.2.1-outil-home-assistant.md) (`pi.registerTool`) : API REST de HA,
  token à périmètre limité
- [Mémoire versionnée](03-jarvis-agent/3.2-outils-et-memoire/3.2.2-memoire-versionnee/3.2.2-memoire-versionnee.md) : hooks session → git pull/commit (convention OKF)
  = le pattern « external memory » du context engineering

### [3.3 Comparaison des régimes d'agents](03-jarvis-agent/3.3-comparaison-regimes-agents/3.3-comparaison-regimes-agents.md)

- (bonus) [Mode RPC/SDK](03-jarvis-agent/3.3-comparaison-regimes-agents/3.3.1-mode-rpc-sdk/3.3.1-mode-rpc-sdk.md) : service qui tient une session Pi ouverte —
  embryon d'agent persistant
- (bonus culture) [Quatre régimes, même boucle](03-jarvis-agent/3.3-comparaison-regimes-agents/3.3.2-quatre-regimes/3.3.2-quatre-regimes.md) : manuelle
  (module 1) / harnais Pi / SDK du marché (Claude Agent SDK ou OpenAI
  Agents SDK) / graphe **LangGraph**
- [Note de conception](03-jarvis-agent/3.3-comparaison-regimes-agents/3.3.3-note-de-conception/3.3.3-note-de-conception.md) dans `architecture/` + `.pi/` complet versionné

---

## Module 4 — Infra : vLLM et le métier de servir ⚪ *(parallélisable)*

### [4.1 Déploiement](04-ollama-vs-vllm-bench/4.1-deploiement/4.1-deploiement.md)

- [vLLM sur RTX 2060](04-ollama-vs-vllm-bench/4.1-deploiement/4.1.1-vllm-sur-rtx-2060/4.1.1-vllm-sur-rtx-2060.md) : conteneur, petit modèle adapté aux 6 Go

### [4.2 Benchmark documenté vs Ollama](04-ollama-vs-vllm-bench/4.2-benchmark-vs-ollama/4.2-benchmark-vs-ollama.md)

- [Métriques : débit et latence](04-ollama-vs-vllm-bench/4.2-benchmark-vs-ollama/4.2.1-metriques-debit-latence/4.2.1-metriques-debit-latence.md) : tokens/s, latence premier token
- [Charge concurrente](04-ollama-vs-vllm-bench/4.2-benchmark-vs-ollama/4.2.2-charge-concurrente/4.2.2-charge-concurrente.md) : 1 / 5 / 20 requêtes (script de charge maison)

### [4.3 Analyse et verdict](04-ollama-vs-vllm-bench/4.3-analyse-et-verdict/4.3-analyse-et-verdict.md)

- [Mécanismes vLLM](04-ollama-vs-vllm-bench/4.3-analyse-et-verdict/4.3.1-mecanismes-vllm/4.3.1-mecanismes-vllm.md) : batching continu, KV cache, PagedAttention
- [Verdict Ollama vs vLLM](04-ollama-vs-vllm-bench/4.3-analyse-et-verdict/4.3.2-verdict-ollama-vs-vllm/4.3.2-verdict-ollama-vs-vllm.md) : quand l'un suffit, quand l'autre se justifie

---

## Module 6 — Production : evals, traces, sécurité ⚪ *(transverse, démarre avec le module 2)*

### [6.1 Observabilité](06-production/6.1-observabilite/6.1-observabilite.md)

- [Langfuse self-hosté](06-production/6.1-observabilite/6.1.1-langfuse-self-hoste/6.1.1-langfuse-self-hoste.md) (un conteneur de plus)
- [Tracer les appels](06-production/6.1-observabilite/6.1.2-tracer-les-appels/6.1.2-tracer-les-appels.md) des modules 2 et 3 : latence, tokens
- [**Suivi des coûts**](06-production/6.1-observabilite/6.1.3-suivi-des-couts/6.1.3-suivi-des-couts.md) en continu (coût équivalent API pour le local)

### [6.2 Sécurité](06-production/6.2-securite/6.2-securite.md)

- [OWASP Top 10 for LLM Applications](06-production/6.2-securite/6.2.1-owasp-top-10-llm/6.2.1-owasp-top-10-llm.md) : lire et savoir restituer
- [Tests adversariaux](06-production/6.2-securite/6.2.2-tests-adversariaux/6.2.2-tests-adversariaux.md) sur son propre RAG/agent (injections dans les
  documents, dans les entrées) + documenter les défenses
- [Threat model Jarvis](06-production/6.2-securite/6.2.3-threat-model-jarvis/6.2.3-threat-model-jarvis.md) en vocabulaire métier

### [6.3 Culture fine-tuning](06-production/6.3-culture-fine-tuning/6.3-culture-fine-tuning.md)

- (option) [LoRA sur Colab](06-production/6.3-culture-fine-tuning/6.3.1-lora-sur-colab/6.3.1-lora-sur-colab.md) — savoir dire ce que c'est
  et quand c'est (rarement) la bonne réponse *(→ entrée glossaire)*

---

## Module 7 — Multimodal : capitaliser sur le pipeline vocal ⚪

### [7.1 Documenter l'existant en vocabulaire métier](07-multimodal/7.1-documenter-existant/7.1-documenter-existant.md)

- [Étude de cas STT/TTS](07-multimodal/7.1-documenter-existant/7.1.1-etude-de-cas-stt-tts/7.1.1-etude-de-cas-stt-tts.md) : latences par
  brique, choix des modèles, streaming Piper
- [Post « anatomy of a fully local voice assistant »](07-multimodal/7.1-documenter-existant/7.1.2-post-anatomy/7.1.2-post-anatomy.md)

### [7.2 Vision locale](07-multimodal/7.2-vision-locale/7.2-vision-locale.md)

- [VLM local](07-multimodal/7.2-vision-locale/7.2.1-vlm-local/7.2.1-vlm-local.md) via Ollama (Qwen-VL ou LLaVA) sur la RTX 2060 : décrire une
  photo, lire un document scanné, mesurer ce qui rentre en 6 Go

### [7.3 Ouvertures](07-multimodal/7.3-ouvertures/7.3-ouvertures.md)

- (bonus homelab) [Caméra et OCR](07-multimodal/7.3-ouvertures/7.3.1-camera-et-ocr/7.3.1-camera-et-ocr.md) : Caméra HA → « Jarvis, décris ce que tu vois » ;
  OCR des documents famille vers le NAS
- [API cloud équivalentes](07-multimodal/7.3-ouvertures/7.3.2-api-cloud-equivalentes/7.3.2-api-cloud-equivalentes.md) (vision GPT/Claude/Gemini,
  génération d'images, Whisper API)

---

## Transverse — Portfolio et employabilité *(en continu)*

### [P.1 Les repos publics](transverse-portfolio/p.1-repos-publics/p.1-repos-publics.md)

- [GitHub public](transverse-portfolio/p.1-repos-publics/p.1.1-github-public/p.1.1-github-public.md) en anglais ; chaque README : problème, architecture
  (un schéma), métriques, « ce que je referais autrement »
- [Extraction en repos dédiés](transverse-portfolio/p.1-repos-publics/p.1.2-extraction-repos/p.1.2-extraction-repos.md) (décision au fil de l'eau)

### [P.2 Écrire](transverse-portfolio/p.2-ecrire/p.2-ecrire.md)

- [Un post par module](transverse-portfolio/p.2-ecrire/p.2.1-un-post-par-module/p.2.1-un-post-par-module.md) (blog perso ou dev.to)
- [Veille Obsidian](transverse-portfolio/p.2-ecrire/p.2.2-veille-obsidian/p.2.2-veille-obsidian.md) (notes `type: watch`) → sujets de posts

### [P.3 Le pitch](transverse-portfolio/p.3-pitch/p.3-pitch.md)

- [La phrase](transverse-portfolio/p.3-pitch/p.3.1-la-phrase/p.3.1-la-phrase.md) : « assistant vocal + agentique 100 % local de A à Z, et je
  peux expliquer chaque couche sans framework »
- [Vocabulaire des offres](transverse-portfolio/p.3-pitch/p.3.2-vocabulaire-des-offres/p.3.2-vocabulaire-des-offres.md) : production-grade, human-in-the-loop,
  grounding, pipelines d'évaluation continue, gateway multi-modèles

### [P.4 En suspens](transverse-portfolio/p.4-en-suspens/p.4-en-suspens.md)

- [x] [Notions cloud](transverse-portfolio/p.4-en-suspens/p.4.1-notions-cloud/p.4.1-notions-cloud.md) — *arbitré le 21 juillet 2026* : version minimale
  via le backend commutable local/cloud du module 2 (§2.4) + situer
  AWS Bedrock / Azure OpenAI / Vertex AI
