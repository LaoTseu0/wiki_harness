# Cartographie du cours

> Refaire à la main chaque couche d'une application LLM — de la génération d'un token jusqu'au harnais multi-agent — puis déposer ce qu'on a compris dans **Hosef**, la bibliothèque maison sur laquelle le harnais sera bâti. Terrain : un petit modèle local.

Ce fichier fixe l'ordre du parcours. Ce qu'on construit et la forme d'une leçon sont dans [REGLES.md](REGLES.md) — parties I et II.

## Les Parcours

### 0 · La génération
*La couche : le modèle comme fonction qui, d'une suite de tokens, tire le suivant.*

- tokenisation — BPE / SentencePiece, vocabulaire, comptage ; tokens de contrôle (rôles, début/fin de tour, BOS/EOS)
- template de chat — la liste de messages devient le texte unique lu par le modèle, par insertion des tokens de contrôle
- détokenisation — des tokens au texte ; un token byte-level peut couper un caractère UTF-8, donc un token seul n'est pas toujours affichable
- logits, softmax, distribution de probabilité
- autorégression — un token à la fois, réinjecté
- échantillonnage — température, top-k, top-p, min-p ; l'argmax (greedy) comme limite température → 0
- pénalités de répétition — repetition penalty (multiplicative sur les logits) vs presence / frequency (additives, comptées)
- la seed et sa portée ; l'arrêt de la boucle — EOS, stop sequences, `max_tokens`
- attention et KV cache — premier token lent, suivants rapides
- fenêtre de contexte — le plafond, et pourquoi il coûte
- Ajouter au glossaire — samplers exotiques (typical-p, mirostat, tail-free), beam search

**Cas pratique** — reproduire une génération déterministe ; tracer une distribution et la déformer réglage par réglage.
**Intégration** — `generation` : tokeniser et détokeniser, compteur de tokens, rendu de template, le sampler (logits → token) et sa config, la boucle autorégressive bornée.

### 1 · Le transport
*La couche : le modèle comme service au bout d'un fil.*

- le backend local — Ollama en exemple ; llama.cpp, vLLM, LM Studio, TGI en alternatives
- HTTP brut — un POST, une réponse, sans SDK ; en-têtes et authentification, de même forme en local et en cloud
- les endpoints — complétion vs chat ; API native et couche OpenAI-compatible, deux surfaces sur un même backend
- streaming — la réponse token par token ; deux formats, NDJSON natif vs SSE, et le réassemblage des deltas
- la forme de la réponse — le contenu, la raison d'arrêt, le comptage des tokens
- codes et erreurs — 4xx / 5xx, corps d'erreur ; détection du 429 et de Retry-After
- timeouts et coupures de flux
- Ajouter au glossaire — keep-alive et pooling de connexion, endpoints d'inventaire

**Cas pratique** — un client streaming écrit à la main, contre Ollama, qui survit à une coupure en cours de flux ; pointé tour à tour sur l'endpoint natif puis OpenAI-compatible.
**Intégration** — `client` : requête authentifiée, appel, streaming SSE et NDJSON, parsing de la réponse, taxonomie d'erreurs.

### 2 · Le contexte
*La couche : la conversation comme historique qu'on maintient sous un seuil de tokens.*

- le modèle est sans mémoire (stateless) — on renvoie tout l'historique à chaque tour ; le coût en tokens croît avec la conversation
- historique et rôles — system / user / assistant / tool
- construction du contexte — quoi mettre, dans quel ordre ; « lost in the middle », placer le critique en tête ou en fin
- comptage et budget — comptage exact via le tokenizer (brique `generation`, P0) ; partition du budget : système / historique / contexte récupéré / réserve pour la réponse
- éviction — comment couper (fenêtre glissante, troncature) et quoi sauver (le système ne s'évince pas, les tours récents priment, messages épinglés)
- compaction et résumé — compresser les vieux tours ; quand déclencher, ce que le résumé perd
- Ajouter au glossaire — « lost in the middle »

**Cas pratique** — tenir une conversation longue sous un seuil fixe sans perdre le fil.
**Intégration** — `context` : gestionnaire de fenêtre et de budget (partition + réserve de sortie), politique d'éviction, compaction.

### 3 · Le contrôle
*La couche : diriger ce que le modèle produit, sans toucher à ses poids.*

- prompting — zero-shot, few-shot ; le nombre et l'ordre des exemples comptent
- chaîne de pensée — faire produire le raisonnement avant la réponse
- prompt système — sa portée, ce qu'il ne garantit pas
- prefill de la réponse — commencer à la place du modèle pour forcer le format
- sortie structurée — deux voies : prompt seul sans garantie, décodage contraint valide par construction
- décodage contraint — masquage des logits par une grammaire ; logit_bias pour forcer ou bannir un token ; son coût sur le débit et le contenu
- validation et retry — Pydantic, re-prompt avec l'erreur ; inutile quand la sortie est contrainte
- Ajouter au glossaire — self-consistency, délimiteurs instruction/donnée

**Cas pratique** — forcer une sortie JSON valide sous contrainte, puis sans, et mesurer l'écart.
**Intégration** — `control` : gabarits de prompt, prefill, décodage contraint, sortie structurée validée.

### 4 · L'action
*La couche : le modèle appelle des fonctions et lit leurs résultats.*

- function calling — le modèle émet un appel, pas une action ; la sortie structurée la plus fiable, héritée du P3
- natif vs émulé — le modèle entraîné à l'appel, ou l'appel forcé par prompt et décodage contraint quand il ne sait pas
- schémas JSON d'outils — nom, description, paramètres ; parsing et validation de l'appel
- tool_choice — laisser choisir, forcer un outil, ou l'interdire
- le cycle d'un appel — l'assistant émet un ou plusieurs appels, on exécute, le rôle tool renvoie le résultat, l'assistant relit
- enchaîner les appels — la boucle appel → résultat → appel, jusqu'à la réponse finale
- conception d'un outil — nom et description **sont** du prompt
- forme du résultat rendu ; troncature d'une sortie énorme
- erreurs exploitables ; idempotence, et la reprise d'un appel non idempotent
- Ajouter au glossaire — appels parallèles, tool_call_id

**Cas pratique** — un outil du schéma au renvoi, avec une erreur que le modèle sait rattraper.
**Intégration** — `tools` : registre d'outils natifs, validation des arguments, dispatch, rendu du résultat.

### 5 · Les outils distants — MCP
*La couche : l'outil comme service distant, interchangeable.*

- le protocole MCP — `tools/list`, `tools/call`
- un serveur ; un client minimal
- le handshake sous le SDK
- transports — stdio, HTTP
- intégration à un client existant
- le versant sécurité — injection de prompt indirecte

**Cas pratique** — exposer un outil en MCP, puis le consommer comme s'il était natif.
**Intégration** — `tools` étendu : un outil distant indiscernable d'un natif dans le registre.

### 6 · La mémoire
*La couche : ce que l'agent sait au-delà de sa fenêtre.*

- embeddings ; similarité cosinus
- chunking ; indexation ; recherche top-k
- RAG complet — récupérer, injecter, répondre
- evals du RAG — rappel, précision, fidélité
- retrieval hybride ; BM25
- re-ranking — bi-encoder vs cross-encoder ; HNSW
- filtres métadonnées ; Qdrant
- outillage standard — LlamaIndex, RAGAS / DeepEval ; tableau comparatif
- les natures de mémoire — travail, épisodique, sémantique, procédurale
- mémoire versionnée
- RAG vs fine-tuning — quand ce n'est pas la réponse

**Cas pratique** — un RAG mesuré à la main, puis branché sur Qdrant ; ajouter une mémoire épisodique datée.
**Intégration** — `memory` : magasins de plusieurs natures derrière une interface de rappel, et la première famille d'evals.

### 7 · Le substrat
*La couche : servir soi-même le modèle qu'on consommait.*

- quantization — ce que coûte un poids, ce qui tient sur la carte
- vLLM — le servir
- batching continu ; PagedAttention ; KV cache partagé
- prompt caching — ne pas re-payer le préfixe stable
- benchmark — débit, latence, charge concurrente
- verdict — à quelles conditions un outil bat l'autre

**Cas pratique** — benchmarker deux backends sur la même charge, et lire l'écart.
**Intégration** — `provider` : abstraction local / cloud, commutable par config.

### 8 · L'orchestration
*La couche : le flot de contrôle par-dessus plusieurs appels.*

- la boucle d'agent — lire, écrire, exécuter ; la condition d'arrêt
- ReAct — raisonner / agir / observer, le patron que la boucle exécute
- garde-fous — hook `tool_call`, conteneur, moindre privilège
- fiabilité de la boucle — timeout, retry, backoff, 429, outil non idempotent
- sous-agents — contexte isolé, rapport en retour
- skills — divulgation progressive
- régimes d'agents — RPC / SDK, quatre régimes, même boucle
- routage multi-agentique — superviseur / ouvriers, arbitrage coût / latence / qualité
- evals de trajectoire — la boucle termine-t-elle, le bon outil est-il appelé

**Cas pratique** — une tâche multi-étapes bornée ; un superviseur qui route vers deux ouvriers et arbitre.
**Intégration** — `loop`, `guardrails`, `router`.

### 9 · L'exploitation
*La couche : rendre le système visible, mesurable, défendable.*

- observabilité — tracer les appels (Langfuse), suivi des coûts
- evals — les trois familles ; la non-régression ; pourquoi un score global unique ne répare rien
- LLM-as-judge — juge ≠ générateur
- sécurité — OWASP Top 10 LLM, tests adversariaux, threat model
- culture fine-tuning — LoRA, et surtout savoir quand ce n'est pas la réponse

**Cas pratique** — tracer et chiffrer une trajectoire complète ; écrire un juge-LLM et le mettre à l'épreuve.
**Intégration** — `observability`, `evals` (généralisé), `judge`.

### 10 · Le multimodal
*La couche : les entrées non-textuelles, ramenées au même pipeline.*

- étude de cas STT / TTS ; anatomie d'un assistant vocal local
- vision locale — VLM
- caméra et OCR
- équivalents cloud

**Cas pratique** — brancher la voix ou la vision sur le harnais existant.
**Intégration** — `io` : normaliser voix et image vers le pipeline texte.

### 11 · Le harnais
*Pas une couche neuve : l'assemblage de toutes les précédentes.*

Aucun mécanisme nouveau. On compose les briques Hosef en un assistant qui tourne :

- la topologie d'agents concrète — qui sont les ouvriers, qui supervise
- le sous-système mémoire câblé — les quatre natures, ensemble
- voix et vision en entrée
- persistance des sessions
- garde-fous et observabilité branchés

**Cas pratique** — le harnais est le cas pratique.
**Intégration** — Hosef atteint sa première version stable ; le harnais tourne dessus.


