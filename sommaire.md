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
> mineurs (0.1.0, 0.2.0…), jamais des réécritures fermées.
> **Ordre de passage** : 1 → 2 (6 en continu) → **5** → 3 → 4/7
> (le MCP avancé avant l'agent — décision du 21 juillet 2026).
> **Légende** : ✅ acquis · 🔵 en cours · ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

---

## Module 1 — llm-from-scratch : du socle au framework *(jamais fermé)*

### 1.1 Socle sans framework ✅ *(terminé le 20 juillet 2026)*

- ✅ Chat CLI avec historique, streaming, gestion du contexte à la main
  (troncature, compaction)
- ✅ Paramètres de sampling expérimentés (temperature, top-k, top-p)
  et techniques de prompt (zero/few-shot, chain-of-thought)
- ✅ Function calling à la main : schémas JSON, parsing, exécution,
  renvoi (= ReAct implémenté)
- ✅ Mini-boucle d'agent (pattern Pi) : read/write/edit/bash dans une
  boucle while
- ✅ Structured output : extraction JSON validée Pydantic, retry sur
  JSON invalide

### 1.2 Glossaire exécutable *(continu, alimenté par les modules 2-7)*

- Règle d'entrée : un concept qu'un framework cache et qu'on ne saurait
  pas refaire en ~50 lignes → un exercice numéroté en Python pur ici,
  avec renvoi croisé depuis le module qui l'a introduit
- Entrées candidates déjà identifiées :
  - **BM25** (retrieval lexical, ← module 2 v2) — implémentable à la main
  - **Re-ranking** (ré-ordonner le top-k, ← module 2 v2)
  - **HNSW** (l'index de Qdrant, ← module 2 v2) — version « comprendre
    et schématiser », pas implémenter
  - **Prompt caching** (← couche 0 / module 3)
  - **Handshake MCP** (`tools/list` / `tools/call`, ← module 5)
  - **LoRA** (← module 6, culture)
- README anglais : « every entry is a runnable script » — pièce
  maîtresse du portfolio

### 1.3 Le framework maison *(release 0.0.1 dès les premières briques promues, puis semver en continu)*

- **Architecture modulaire** : découpage en briques enfichables —
  client LLM (providers interchangeables), outils, boucle d'agent,
  mémoire, retrieval, evals
- **Clean code production-grade** : typing, Pydantic, tests pytest,
  packaging, docstrings — le « software craftsmanship » des offres
- **Évolutivité sans friction** : ajouter un outil, un provider ou un
  agent = un fichier, zéro modification du cœur
- **Routage multi-agentique** : superviseur/ouvriers, routage
  coût/latence/qualité — le
  [routeur multi-modèles](../homelab/architecture/router-multi-model.md) devenu code
- **Dogfooding** : les modules suivants (RAG, agent, MCP) consomment le
  framework — chaque module le fait évoluer
- **Sortie précoce** : pas de big-bang final — 0.0.1 avec les premières
  briques (client LLM, outils, `rag_commun` promu), incréments ensuite

---

## Module 2 — homelab-rag : le RAG complet, mesuré 🔵

### 2.1 v1 — le RAG entièrement à la main 🔵

- ✅ 01 Embeddings : texte → vecteur 768 dims via Ollama, norme = 1
- ✅ 02 Similarité cosinus : écrite par Anthony (produit scalaire,
  normes, angle) + géométrie visuelle
- ⚪ 03 Chunking : découper les `.md` par sections, source en métadonnée
- ⚪ 04 Indexation : pipeline chunk → embedding → SQLite
- ⚪ 05 Recherche : question → embedding → top-k (le « R » de RAG)
- ⚪ 06 RAG complet : retrieval → prompt avec contexte → réponse citée
- ⚪ 07 Evals : jeu de questions, score déterministe, baseline chiffrée
  *(baseline provisoire mesurée : retrieval 7/12, génération 7/12,
  zéro hallucination)*

### 2.2 v2 — Qdrant + retrieval avancé ⚪

- Migration du stockage vers Qdrant (conteneur docker homelab)
- Retrieval hybride : BM25 + vecteurs *(→ entrée glossaire BM25)*
- Re-ranking du top-k *(→ entrée glossaire)*
- Filtres métadonnées (par dossier, par type de doc)
- Re-passage des evals : tableau comparatif v1 → v2

### 2.3 v3 — LlamaIndex + outillage standard ⚪

- Refaire la chaîne en LlamaIndex ; documenter ce que le framework
  apporte / cache
- Étendre le jeu d'evals (~30 questions) + LLM-as-judge — **juge ≠
  générateur** (jamais Qwen3 4B jugeant Qwen3 4B), choix documenté
- Passer les evals dans RAGAS ou DeepEval
- Tableau final v1 → v2 → v3 dans le README
- Réponse d'entretien rédigée : RAG vs fine-tuning, pourquoi RAG ici

### 2.4 Service et craftsmanship ⚪ *(ajouté le 21 juillet 2026)*

- Exposer le RAG en **service FastAPI** : `POST /ask` → réponse +
  sources (réutilisé par le MCP du module 5, tracé au module 6)
- **Backend commutable local/cloud** par config : abstraction provider
  (future brique du framework, et la réponse à l'angle mort cloud)
- Premiers **tests pytest** sur la chaîne (le 07 en est le germe),
  typing sur la bibliothèque commune, packaging à la promotion

---

## Module 5 — MCP : un serveur ET un client ⚪ *(passage avancé avant le module 3 — décision du 21 juillet 2026)*

### 5.1 Le serveur

- Serveur MCP Python exposant le homelab en lecture : conteneurs,
  entités HA, recherche dans la doc (réutilise le module 2)
- Transport stdio d'abord, HTTP ensuite
- Branchement sur un client existant (Claude Code) + doc d'intégration

### 5.2 Le client

- Client MCP minimal : découverte `tools/list`, appel `tools/call`
  *(→ entrée glossaire handshake MCP)*

### 5.3 Le versant sécurité

- Prompt injection indirecte : que se passe-t-il si un document indexé
  contient une instruction malveillante ? — à documenter (sujet d'entretien)

---

## Module 3 — jarvis-agent : l'agent maison sandboxé ⚪

### 3.1 Garde-fous et sécurité d'abord

- Extension Pi hook `tool_call` : liste noire de commandes destructives
  + validation humaine (human-in-the-loop)
- Conteneur dédié, moindre privilège, aucun accès aux partages famille

### 3.2 Outils et mémoire

- Outil custom `home_assistant` (`pi.registerTool`) : API REST de HA,
  token à périmètre limité
- Mémoire versionnée : hooks session → git pull/commit (convention OKF)
  = le pattern « external memory » du context engineering

### 3.3 Comparaison des régimes d'agents

- (bonus) Mode RPC/SDK : service qui tient une session Pi ouverte —
  embryon d'agent persistant
- (bonus culture) Le même mini-agent en quatre versions : manuelle
  (module 1) / harnais Pi / SDK du marché (Claude Agent SDK ou OpenAI
  Agents SDK) / graphe **LangGraph** — quatre régimes, même boucle
- Note de conception dans `architecture/` + `.pi/` complet versionné

---

## Module 4 — Infra : vLLM et le métier de servir ⚪ *(parallélisable)*

### 4.1 Déploiement

- vLLM en conteneur sur la RTX 2060, petit modèle adapté aux 6 Go

### 4.2 Benchmark documenté vs Ollama

- Tokens/s, latence premier token
- Comportement à 1 / 5 / 20 requêtes concurrentes (script de charge maison)

### 4.3 Analyse et verdict

- Expliquer les résultats : batching continu, KV cache, PagedAttention
- Rédiger : quand Ollama suffit, quand vLLM se justifie

---

## Module 6 — Production : evals, traces, sécurité ⚪ *(transverse, démarre avec le module 2)*

### 6.1 Observabilité

- Self-hoster Langfuse (un conteneur de plus)
- Tracer les appels des modules 2 et 3 : latence, tokens
- **Suivi des coûts en continu** (coût équivalent API pour le local)

### 6.2 Sécurité

- OWASP Top 10 for LLM Applications : lire et savoir restituer
- Test adversarial sur son propre RAG/agent (injections dans les
  documents, dans les entrées) + documenter les défenses
- Page « threat model » de l'agent Jarvis en vocabulaire métier

### 6.3 Culture fine-tuning

- (option) LoRA d'un petit modèle sur Colab — savoir dire ce que c'est
  et quand c'est (rarement) la bonne réponse *(→ entrée glossaire)*

---

## Module 7 — Multimodal : capitaliser sur le pipeline vocal ⚪

### 7.1 Documenter l'existant en vocabulaire métier

- Le pipeline vocal de Jarvis comme étude de cas STT/TTS : latences par
  brique, choix des modèles, streaming Piper
- Post « anatomy of a fully local voice assistant »

### 7.2 Vision locale

- VLM via Ollama (Qwen-VL ou LLaVA) sur la RTX 2060 : décrire une
  photo, lire un document scanné, mesurer ce qui rentre en 6 Go

### 7.3 Ouvertures

- (bonus homelab) Caméra HA → « Jarvis, décris ce que tu vois » ;
  OCR des documents famille vers le NAS
- Situer les API cloud équivalentes (vision GPT/Claude/Gemini,
  génération d'images, Whisper API)

---

## Transverse — Portfolio et employabilité *(en continu)*

### P.1 Les repos publics

- Un GitHub public en anglais ; chaque README : problème, architecture
  (un schéma), métriques, « ce que je referais autrement »
- Extraction des modules en repos dédiés (décision au fil de l'eau)

### P.2 Écrire

- Un post par module (blog perso ou dev.to)
- La veille consignée dans Obsidian (notes `type: watch`) → sujets de posts

### P.3 Le pitch

- Une phrase : « assistant vocal + agentique 100 % local de A à Z, et je
  peux expliquer chaque couche sans framework »
- Employer les termes des offres : production-grade, human-in-the-loop,
  grounding, pipelines d'évaluation continue, gateway multi-modèles

### P.4 En suspens

- [x] Notions cloud — *arbitré le 21 juillet 2026* : version minimale
  via le backend commutable local/cloud du module 2 (§2.4) + situer
  AWS Bedrock / Azure OpenAI / Vertex AI
