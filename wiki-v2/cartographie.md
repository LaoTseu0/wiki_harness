# Cartographie du cours

> Refaire à la main chaque couche d'une application LLM — de la génération d'un token jusqu'au harnais multi-agent — puis déposer ce qu'on a compris dans **HOSeF**, la librairie maison sur laquelle le harnais sera bâti. Terrain : un petit modèle local.

Ce fichier fixe l'ordre du parcours. La forme d'une leçon est dans [template.md](template.md) ; ce qu'on construit, dans [cadrage.md](cadrage.md).

## Le principe : des couches, pas une étagère ni un récit

La V1 rangeait par thème, sans ordre entre les dossiers — un plan de wiki, pas de cours. Une première V2 rangeait par récit de construction, mais le récit sautait d'un niveau d'abstraction à l'autre : on croisait la boucle d'agent avant de savoir ce qu'est un token.

Cette V2 range par **couche du système**. Chaque Parcours est une couche, et une couche est **un seul niveau d'abstraction** : on ne mélange pas le tirage d'un token avec l'aiguillage entre agents. Les couches montent dans l'ordre où la compréhension se construit — la génération d'abord, l'orchestration en haut — et on ne redescend jamais : chaque Parcours suppose la couche du dessous acquise.

L'ordre est donc **cognitif** : on ne manipule une pièce qu'après avoir compris celle sur laquelle elle repose.

## La forme d'un Parcours

Un Parcours enseigne les **mécanismes** d'une couche — jamais un outil qu'on ne saurait pas refaire. Il se termine par deux sections fixes :

- **Cas pratique** — des exercices sur la couche, à faire, pas à lire.
- **Intégration** — la brique HOSeF de la couche, déposée dans `src/hosef/`. C'est le retour au tout : la pièce comprise devient du code réutilisé.

Les notions listées sous chaque Parcours sont **exhaustives** : elles fixent ce que la rédaction devra couvrir, pour qu'aucune ne se perde. Une notion sans leçon propre part au glossaire ; aucune ne disparaît.

## Les Parcours

### 0 · La génération
*La couche : le modèle comme fonction qui, d'une suite de tokens, tire le suivant.*

- tokenisation — BPE / SentencePiece, vocabulaire, comptage
- template de chat — la liste de messages devient le texte unique lu par le modèle
- logits, softmax, distribution de probabilité
- autorégression — un token à la fois, réinjecté
- échantillonnage — température, top-k, top-p, min-p, repetition penalty
- la seed et sa portée ; les stop sequences
- attention et KV cache — premier token lent, suivants rapides
- fenêtre de contexte — le plafond, et pourquoi il coûte

**Cas pratique** — reproduire une génération déterministe ; tracer une distribution et la déformer réglage par réglage.
**Intégration** — `generation` : tokeniser, compteur de tokens, config d'échantillonnage, rendu de template.

### 1 · Le transport
*La couche : le modèle comme service au bout d'un fil.*

- HTTP brut — un POST, une réponse, sans SDK
- les endpoints — complétion vs chat
- streaming SSE — la réponse token par token
- codes et erreurs — 4xx / 5xx, corps d'erreur
- timeouts et coupures de flux

**Cas pratique** — un client streaming écrit à la main, qui survit à une coupure en cours de flux.
**Intégration** — `client` : appel, streaming, taxonomie d'erreurs.

### 2 · Le contexte
*La couche : la conversation comme état qu'on gère sous un plafond.*

- le modèle est sans mémoire (stateless)
- historique et rôles — system / user / assistant / tool
- construction du contexte — quoi mettre, dans quel ordre
- estimation des tokens ; le budget de contexte
- fenêtre glissante ; troncature
- compaction et résumé

**Cas pratique** — tenir une conversation longue sous un plafond fixe sans perdre le fil.
**Intégration** — `context` : gestionnaire de fenêtre et de budget, compaction.

### 3 · Le contrôle
*La couche : diriger ce que le modèle produit, sans toucher à ses poids.*

- prompting — zero-shot, few-shot
- chaîne de pensée ; ReAct
- prompt système — sa portée, ce qu'il ne garantit pas
- sortie structurée — JSON schema, grammaires
- décodage contraint — comment la contrainte s'applique au tirage
- validation (Pydantic) et retry

**Cas pratique** — forcer une sortie JSON valide sous contrainte, puis sans, et mesurer l'écart.
**Intégration** — `control` : gabarits de prompt, sortie structurée validée.

### 4 · L'action
*La couche : le modèle appelle des fonctions et lit leurs résultats.*

- function calling — le modèle émet un appel, pas une action
- schémas JSON d'outils ; parsing de l'appel
- exécution ; renvoi du résultat au modèle
- conception d'un outil — nom et description **sont** du prompt
- forme du résultat rendu ; troncature d'une sortie énorme
- erreurs actionnables ; idempotence

**Cas pratique** — un outil du schéma au renvoi, avec une erreur que le modèle sait rattraper.
**Intégration** — `tools` : registre et dispatch d'outils natifs.

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

Aucun mécanisme nouveau. On compose les briques HOSeF en un assistant qui tourne :

- la topologie d'agents concrète — qui sont les ouvriers, qui supervise
- le sous-système mémoire câblé — les quatre natures, ensemble
- voix et vision en entrée
- persistance des sessions
- garde-fous et observabilité branchés

**Cas pratique** — le harnais est le cas pratique.
**Intégration** — HOSeF atteint sa première version stable ; le harnais tourne dessus.

## Le transverse et le glossaire

Certaines notions ne sont pas une couche : elles traversent tout le projet. Elles ne forment pas un Parcours, elles se pratiquent à chaque *Intégration*.

- **Artisanat** — promotion (ce qui qualifie une brique), architecture modulaire, évolutivité sans friction, sortie précoce et semver, dogfooding, clean code, tests / typing / packaging.

Et ce qui n'a pas de mécanisme propre part au glossaire, sans se perdre : `transformers`, `argmax`, `MoE`, `Modelfile`, et les termes croisés en chemin.

## Ce qui vient ensuite

Le squelette est fixé : douze Parcours, en couches, chacun d'un seul niveau d'abstraction, chacun fermé par un *Cas pratique* et une *Intégration*. Reste à dériver, Parcours par Parcours, chaque notion en leçon ou en entrée de glossaire, avec son en-tête complet — c'est là que le graphe devient vérifiable par `outils/`. On construit un Parcours à la fois, dans l'ordre, en commençant par le 0.
