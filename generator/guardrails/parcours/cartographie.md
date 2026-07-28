# Cartographie du cours

> Comprendre puis reconstruire les mécanismes qui relient un modèle de langage
> à un assistant agentique local. Chaque Parcours dépose une pièce générique
> dans **Praxis** et fait progresser **Mnémos**, l'assistant personnel qui
> l'emploie.

Le [contrat du projet](CADRAGE.md) fixe la méthode, les frontières et la forme
des leçons. Ce fichier fixe l'ordre de construction et la couverture du cours.

Chaque Parcours annonce aussi ses processus structurants. Le
[registre des processus](../schema/processus/index.md) en fixe les identifiants, les
frontières et l'état de cadrage. Les leçons emploient ensuite ces mêmes
identifiants pour se positionner visuellement sans recréer une version locale
du flux.

La progression est local-first. Un petit modèle et l'infrastructure domestique
servent de terrain. Les services cloud et les frameworks établis servent de
comparaison après la reconstruction du mécanisme.

---

## Préambule · Python pour construire Praxis

*La pièce : le langage et l'outillage nécessaires au reste du parcours.*

**Processus structurant** —
[[generator/guardrails/schema/processus/pipeline-evenements-async.canvas|`pipeline-evenements-async`]].

Ce préambule ne reprend pas les bases communes à tous les langages. Il traduit
vers Python les compétences d'un développeur JavaScript ou Java.

- environnements virtuels, `pyproject.toml`, dépendances et packaging ;
- modules, packages, imports et layout `src/` ;
- objets, `dataclass`, composition et protocoles structurels ;
- annotations de types, génériques et unions ;
- validation des données avec Pydantic ;
- exceptions, causes et taxonomie d'erreurs ;
- itérateurs, générateurs et flux ;
- `async` / `await`, tâches, itérateurs asynchrones et annulation ;
- context managers et gestion des ressources ;
- pytest, fixtures, doubles de test et tests asynchrones ;
- configuration, variables d'environnement et secrets ;
- logs structurés ;
- formats sérialisables et versions de schéma.

### Découpage prévu

| Ordre · identifiant | Leçon | Processus · étape | Schéma · élément | Connaissances attribuées |
|---|---|---|---|---|
| P.1 · `py-environnements-dependances` | [Environnements et dépendances](../../../Wiki/parcours/preambule-python/01-environnements-dependances.md) | `aucun — préparation du projet` | `environnement-projet-python` · `environnement-virtuel` | environnement virtuel, `pyproject.toml`, dépendances et packaging |
| P.2 · `py-modules-packages-imports` | Modules, packages et imports | `aucun — structure statique du code` | à cadrer | modules, packages, imports et layout `src/` |
| P.3 · `py-objets-contrats-types` | Modéliser des contrats en Python | `aucun — modèle structurel transversal` | à cadrer | objets, `dataclass`, composition, protocoles, annotations, génériques et unions |
| P.4 · `py-validation-donnees` | Valider les données | `pipeline-evenements-async` · `valider-evenement` | — | validation à la frontière avec Pydantic |
| P.5 · `py-exceptions-erreurs` | Représenter les échecs | `pipeline-evenements-async` · `signaler-erreur` | — | exceptions, causes et taxonomie d'erreurs |
| P.6 · `py-iterateurs-generateurs` | Produire un flux paresseux | `pipeline-evenements-async` · `produire-evenement` | — | itérateurs, générateurs et progression à la demande |
| P.7 · `py-coroutines-taches` | Coroutines et tâches | `pipeline-evenements-async` · `transformer-evenement` | — | `async`, `await`, tâches et ordonnancement coopératif |
| P.8 · `py-iterateurs-asynchrones` | Flux asynchrones | `pipeline-evenements-async` · `emettre-evenement` | — | itérateurs et générateurs asynchrones |
| P.9 · `py-annulation` | Annuler sans masquer | `pipeline-evenements-async` · `annuler-flux` | — | réception, propagation et limites de l'annulation |
| P.10 · `py-context-managers` | Durée de vie des ressources | `pipeline-evenements-async` · `fermer-ressources` | — | context managers synchrones et asynchrones, nettoyage garanti |
| P.11 · `py-configuration-secrets` | Configurer sans état global | `pipeline-evenements-async` · `configurer-pipeline` | — | configuration, variables d'environnement et secrets |
| P.12 · `py-tests` | Tester les frontières | `aucun — processus de vérification transversal` | à cadrer | pytest, fixtures, doubles de test et tests asynchrones |
| P.13 · `py-logs-structures` | Produire des logs structurés | `aucun — observabilité transversale` | à cadrer | événements de log, contexte et corrélation |
| P.14 · `py-serialisation-schemas` | Sérialiser des contrats durables | `aucun — contrat de données transversal` | à cadrer | formats sérialisables, version de schéma et compatibilité |

**Reconstruction** — écrire un pipeline asynchrone typé qui produit, transforme
et annule un flux d'événements.

**Cas pratique** — empaqueter le pipeline, le configurer sans constante globale
et le tester sans dépendre du réseau.

**Intégration** — `contracts`, `config` et l'infrastructure de tests de Praxis.

---

## 0 · De l'entrée textuelle au token suivant

*La pièce : le modèle comme fonction qui transforme une séquence en
distribution pour le prochain token.*

**Processus structurants** —
[[generator/guardrails/schema/processus/generation-token.canvas|`generation-token`]] et
[[generator/guardrails/schema/processus/inference-transformer.canvas|`inference-transformer`]].

- Unicode, bytes et limites d'un caractère ;
- tokenisation, BPE, SentencePiece et vocabulaire ;
- tokens de contrôle, BOS, EOS et fins de tour ;
- Template de chat : des messages au texte réellement lu ;
- détokenisation et fragments UTF-8 ;
- embeddings de tokens ;
- position, masque causal et RoPE ;
- Q, K, V et attention ;
- residual stream, normalisation et MLP ;
- projection finale, logits et softmax ;
- autorégression ;
- température, top-k, top-p et min-p ;
- argmax et génération greedy ;
- repetition penalty contre presence et frequency penalties ;
- seed, sources d'aléa et portée réelle de la reproductibilité ;
- EOS, stop sequences et budget de sortie ;
- prefill, decode et principe du KV cache ;
- fenêtre de contexte et croissance du coût.

### Découpage prévu

Le processus `generation-token` conserve le flux complet. Le processus
`inference-transformer` ouvre l'étape `inference` de ce premier processus sans
confondre le modèle avec toute la boucle de génération.

| Ordre · identifiant | Leçon | Processus · étape | Schéma · élément | Connaissances attribuées |
|---|---|---|---|---|
| 0.1 · `unicode-octets` | [Texte, Unicode et octets](../../../Wiki/parcours/0-generation/01-unicode-octets.md) | `aucun — représentation fondamentale du texte` | `representation-texte` · `point-code` | points de code, encodage, bytes et limites d'un caractère |
| 0.2 · `tokenisation-vocabulaire` | [Tokenisation et vocabulaire](../../../Wiki/parcours/0-generation/02-tokenisation-vocabulaire.md) | `generation-token` · `tokenisation` | — | BPE, SentencePiece, vocabulaire et relation texte–identifiants |
| 0.3 · `tokens-controle` | [Tokens de contrôle](../../../Wiki/parcours/0-generation/03-tokens-controle.md) | `generation-token` · `tokenisation` | — | BOS, EOS, fins de tour et portée des tokens spéciaux |
| 0.4 · `templates-chat` | [Le texte réellement lu par le modèle](../../../Wiki/parcours/0-generation/04-templates-chat.md) | `generation-token` · `chat-template` | — | rôles, délimiteurs et Template de chat |
| 0.5 · `embeddings-tokens` | [Embeddings de tokens](../../../Wiki/parcours/0-generation/05-embeddings-tokens.md) | `inference-transformer` · `embeddings-tokens` | — | projection des identifiants dans le residual stream |
| 0.6 · `position-rope` | [Représenter la position](../../../Wiki/parcours/0-generation/06-position-rope.md) | `inference-transformer` · `attention-causale` | — | position, portée de RoPE et variantes à ne pas confondre |
| 0.7 · `attention-causale` | [L'attention causale](../../../Wiki/parcours/0-generation/07-attention-causale.md) | `inference-transformer` · `attention-causale` | — | Q, K, V, masque causal et agrégation |
| 0.8 · `residual-normalisation` | [Residual stream et normalisation](../../../Wiki/parcours/0-generation/08-residual-normalisation.md) | `inference-transformer` · `residu-attention` | — | mises à jour résiduelles, pré-norm et propagation entre sous-blocs |
| 0.9 · `mlp-transformer` | [Le MLP d'une couche](../../../Wiki/parcours/0-generation/09-mlp-transformer.md) | `inference-transformer` · `mlp` | — | transformation par position et seconde mise à jour résiduelle |
| 0.10 · `projection-logits` | [De la représentation aux logits](../../../Wiki/parcours/0-generation/10-projection-logits.md) | `inference-transformer` · `projection-vocabulaire` | — | normalisation finale, projection vocabulaire et scores bruts |
| 0.11 · `logits-softmax` | [Des logits à une distribution](../../../Wiki/parcours/0-generation/11-logits-softmax.md) | `generation-token` · `logits` | — | softmax, normalisation numérique et interprétation probabiliste |
| 0.12 · `filtrage-distribution` | [Transformer la distribution](../../../Wiki/parcours/0-generation/12-filtrage-distribution.md) | `generation-token` · `transformation-logits` | — | température, top-k, top-p, min-p, pénalités et greedy |
| 0.13 · `sampling-reproductibilite` | [Tirer le prochain token](../../../Wiki/parcours/0-generation/13-sampling-reproductibilite.md) | `generation-token` · `sampling` | — | échantillonnage, seed, sources d'aléa et reproductibilité |
| 0.14 · `boucle-autoregressive` | [Réinjecter le token choisi](../../../Wiki/parcours/0-generation/14-boucle-autoregressive.md) | `generation-token` · `reinjection` | — | autorégression et croissance de la séquence |
| 0.15 · `detokenisation-fragments` | [Reconstruire le texte généré](../../../Wiki/parcours/0-generation/15-detokenisation-fragments.md) | `generation-token` · `detokenisation` | — | détokenisation incrémentale et fragments UTF-8 incomplets |
| 0.16 · `conditions-arret` | [Borner la génération](../../../Wiki/parcours/0-generation/16-conditions-arret.md) | `generation-token` · `condition-arret` | — | EOS, stop sequences, budget de sortie et raison d'arrêt |
| 0.17 · `prefill-decode-kv-cache` | [Prefill, decode et cache KV](../../../Wiki/parcours/0-generation/17-prefill-decode-kv-cache.md) | `generation-token` · `inference` | — | différence entre les phases, principe du cache et réutilisation |
| 0.18 · `fenetre-contexte-cout` | [Fenêtre de contexte et coût](../../../Wiki/parcours/0-generation/18-fenetre-contexte-cout.md) | `generation-token` · `ajout-token` | — | limite de contexte, croissance du coût et frontière de la mesure |

**Reconstruction** — suivre une entrée dans un petit modèle, observer les
logits, puis écrire le sampler et la condition d'arrêt.

**Cas pratique** — déformer une même distribution réglage par réglage et
reproduire une génération sous un environnement fixé.

**Intégration** — `generation` : tokenisation, Templates, comptage, sampling et
boucle autorégressive bornée.

---

## 1 · L'inférence locale

*La pièce : charger et servir le modèle sur le matériel disponible.*

**Processus structurant** — `service-inference-locale`.

- poids, paramètres et précision numérique ;
- formats Safetensors et GGUF ;
- quantification et compromis mémoire, vitesse, qualité ;
- calcul de la RAM et de la VRAM nécessaires ;
- CPU, GPU, accélérateurs et offload ;
- chargement du modèle et temps de chauffe ;
- prefill contre decode dans les mesures ;
- KV cache : taille, type et pression mémoire ;
- FlashAttention et réduction des mouvements mémoire ;
- batching statique et batching continu ;
- PagedAttention et gestion paginée du KV cache ;
- cache de préfixe ;
- décodage spéculatif ;
- parallélisme, concurrence et saturation ;
- TTFT, latence inter-token, débit, utilisation et mémoire ;
- Ollama comme première surface locale ;
- llama.cpp, vLLM et SGLang comme implémentations à comparer ;
- modèle dense et mixture of experts ;
- choix d'un runtime selon la charge du homelab ;
- culture de l'adaptation : quantification, distillation et LoRA, sans les
  confondre avec le RAG.

**Reconstruction** — calculer le budget mémoire d'un modèle, observer prefill et
decode, puis relier chaque métrique au mécanisme correspondant.

**Cas pratique** — servir le même modèle avec deux runtimes sous une charge
identique et expliquer les différences mesurées.

**Intégration** — `inference` : description d'un runtime local, inventaire de
ses capacités et protocole de benchmark.

---

## 2 · Transport, modèles et providers

*La pièce : le modèle comme capacité accessible au bout d'une frontière.*

**Processus structurant** — `requete-modele-streaming`.

- HTTP brut : requête, réponse, headers et corps ;
- authentification et conservation des secrets ;
- endpoints de complétion, chat, réponses et embeddings ;
- API native contre surface compatible ;
- requêtes synchrones et asynchrones ;
- streaming SSE, NDJSON et WebSocket ;
- événements de texte, raisonnement, outils, usage et fin ;
- assemblage des deltas ;
- backpressure et consommateur lent ;
- timeout de connexion, de lecture et d'exécution ;
- annulation et fermeture d'un flux ;
- réponse partielle et absence éventuelle de reprise ;
- erreurs réseau, protocole, fournisseur et modèle ;
- 429, `Retry-After`, backoff et jitter ;
- finish reason et comptage des tokens ;
- découverte et matrice de capacités ;
- normalisation à la frontière sans effacer les différences ;
- un contrat par capacité : génération, embeddings, reranking, STT, TTS,
  vision ;
- runtime local et service cloud derrière des adaptateurs distincts.

**Reconstruction** — écrire un client streaming sans SDK et rendre chaque
événement observable.

**Cas pratique** — employer successivement un endpoint natif, un endpoint
compatible et une API cloud ; provoquer timeout, 429 et coupure de flux.

**Intégration** — `models` et `client` : contrats canoniques, adaptateurs,
streaming et taxonomie d'erreurs.

---

## 3 · Conversation, session et context engineering

*La pièce : construire la vue bornée que le modèle reçoit à chaque inférence.*

**Processus structurant** — `construction-contexte`.

- le modèle est stateless entre deux appels ;
- différence entre contexte du modèle et état de session ;
- messages, rôles et contenus typés ;
- texte, image, audio, appel et résultat d'outil ;
- identité d'une session et ordre des événements ;
- historique complet contre contexte matérialisé ;
- instructions, outils, retrieval et historique dans le même budget ;
- comptage exact via la brique `generation` ;
- réserve de sortie et budgets par source ;
- sélection, priorité et provenance des éléments ;
- effets de position et « lost in the middle » ;
- fenêtre glissante, troncature et messages épinglés ;
- compaction et résumé ;
- information perdue par la compaction ;
- cache de prompt et préfixe stable ;
- stockage d'une session ;
- version et migration du format persistant ;
- suppression, rétention et export d'une session.

**Reconstruction** — séparer un journal de session de la fonction qui compose le
prochain contexte.

**Cas pratique** — maintenir une conversation longue, redémarrer le processus et
inspecter exactement les tokens envoyés au modèle après reprise.

**Intégration** — `context` et `sessions` : composition, budget, compaction et
persistance conversationnelle.

---

## 4 · Diriger et contraindre le modèle

*La pièce : augmenter la probabilité d'une sortie utile sans modifier les
poids.*

**Processus structurant** — `generation-structuree`.

- instruction système et portée réelle ;
- séparation entre instruction et donnée ;
- zero-shot, one-shot et few-shot ;
- exemples positifs, contre-exemples et ordre ;
- variables, Templates et versions de prompts ;
- modes de raisonnement et budget de raisonnement ;
- raisonnement visible contre état interne non exposé ;
- prefill de la réponse ;
- sortie libre, sortie structurée et outil ;
- JSON Schema ;
- décodage contraint par grammaire ;
- masquage des logits et `logit_bias` ;
- validation syntaxique et validation métier ;
- réparation, re-prompt et retry ;
- cas où une sortie valide reste sémantiquement fausse ;
- self-consistency et génération de plusieurs candidats ;
- évaluation d'une modification de prompt.

**Reconstruction** — contraindre à la main les tokens autorisés pour une petite
grammaire, puis valider un invariant que la grammaire ne peut pas exprimer.

**Cas pratique** — produire le même objet par prompt seul, validation avec
retry et décodage contraint ; comparer validité, contenu et coût.

**Intégration** — `control` : Templates, contraintes, validation et stratégie de
réparation.

---

## 5 · Outils, actions et approbations

*La pièce : transformer une proposition du modèle en effet contrôlé.*

**Processus structurant** — `execution-outil`.

- function calling natif et émulé ;
- le modèle propose un appel, l'exécuteur décide de l'action ;
- nom, description et schéma d'un outil ;
- schéma comme instruction adressée au modèle ;
- `tool_choice` ;
- parsing et validation des arguments ;
- identifiant d'appel et corrélation du résultat ;
- appels parallèles ;
- résultat structuré, fichier, image et contenu volumineux ;
- troncature et résumé d'un résultat ;
- erreur de validation, erreur attendue et erreur interne ;
- message d'erreur exploitable par le modèle ;
- effets de bord et classification lecture / écriture / destruction ;
- idempotence et clé d'idempotence ;
- résultat incertain après coupure ;
- timeout et annulation ;
- permissions et portée d'une capacité ;
- approbation humaine avant exécution ;
- décision ponctuelle contre permission durable ;
- revalidation des préconditions au moment de l'effet ;
- compensation lorsqu'un effet ne peut pas être annulé ;
- journal d'audit.

**Reconstruction** — écrire un registre, un dispatcher et une politique qui
sépare proposition, autorisation, exécution et résultat.

**Cas pratique** — lire l'état d'un service du homelab, proposer une
modification, attendre l'approbation, exécuter puis vérifier l'effet.

**Intégration** — `tools`, `permissions` et `approvals`.

---

## 6 · MCP

*La pièce : exposer et consommer des capacités distantes sans les confondre avec
le runtime de l'agent.*

**Processus structurant** — `connexion-mcp`.

- JSON-RPC 2.0 : requêtes, réponses, erreurs et notifications ;
- client, serveur et host ;
- initialisation et négociation de version ;
- négociation des capacités ;
- tools, resources et prompts ;
- inventaire, appel et changement de catalogue ;
- URI, lecture et abonnement d'une ressource ;
- pagination ;
- stdio et Streamable HTTP ;
- cycle de vie d'une connexion ;
- annulation et progression ;
- authentification et OAuth pour le transport HTTP ;
- elicitation et demande d'information à l'utilisateur ;
- tâches longues et extension de tâches durables ;
- compatibilité entre versions ;
- fonctions dépréciées et période de transition ;
- adaptateur vers le registre d'outils du Parcours 5 ;
- serveur tiers et frontière de confiance ;
- injection indirecte par une ressource ou un résultat ;
- tool poisoning par la description ;
- rug pull après approbation ;
- validation, filtrage et approbation côté host ;
- portée des credentials prêtés au serveur.

Les extensions MCP, MCP Apps et les fonctions dépréciées sont suivies dans la
veille. Elles ne deviennent pas le socle du client minimal sans besoin concret.

**Reconstruction** — écrire un serveur et un client minimaux, y compris le
handshake, `tools/list` et `tools/call`.

**Cas pratique** — exposer un outil natif en MCP, le consommer à travers le même
registre, puis simuler un changement de description et une coupure.

**Intégration** — `mcp` : client, serveur minimal et adaptateur vers `tools`.

---

## 7 · Retrieval et connaissance documentaire

*La pièce : retrouver des sources pertinentes avant de produire une réponse.*

**Processus structurants** — `ingestion-documentaire` et `retrieval-requete`.

- source, document, fragment et provenance ;
- ingestion, parsing et nettoyage ;
- documents structurés, pages, tableaux et code ;
- chunking fixe, sémantique et structurel ;
- recouvrement et contexte parent ;
- embeddings ;
- dimension, normalisation et similarité cosinus ;
- indexation ;
- recherche vectorielle top-k ;
- recherche lexicale et BM25 ;
- filtres de métadonnées ;
- recherche hybride et fusion des rangs ;
- reranking bi-encoder et cross-encoder ;
- HNSW et compromis rappel / latence / mémoire ;
- Qdrant comme store vectoriel concret ;
- pipeline RAG : retrouver, composer, répondre ;
- citations et rattachement de chaque affirmation à une source ;
- fraîcheur, suppression et réindexation ;
- GraphRAG et parcours multi-hop comme prolongement ;
- évaluation séparée du retrieval et de la génération ;
- rappel, précision, MRR, nDCG, fidélité et pertinence ;
- RAG contre contexte direct, outil ou fine-tuning.

**Reconstruction** — construire un petit index lexical puis vectoriel sans
framework RAG, fusionner les résultats et mesurer la récupération.

**Cas pratique** — interroger la documentation réelle du homelab avec citations
et diagnostiquer séparément une mauvaise récupération et une mauvaise réponse.

**Intégration** — `knowledge` et `retrieval` : ingestion, index, recherche,
reranking et provenance.

---

## 8 · La mémoire agentique

*La pièce : conserver une connaissance personnelle au-delà d'une session sans
la confondre avec l'état d'un workflow.*

**Processus structurant** — `memoire-agentique`.

- mémoire de travail : le contexte matérialisé du Parcours 3 ;
- mémoire de session ;
- mémoire épisodique ;
- mémoire sémantique ;
- mémoire procédurale ;
- état exact en clé-valeur ;
- index vectoriel pour le sens proche ;
- graphe pour les entités, relations et parcours ;
- wiki auto-écrit pour la connaissance inspectable ;
- événement, fait, préférence, procédure et observation ;
- décision d'écriture : quoi retenir et pourquoi ;
- extraction depuis une conversation ou un résultat d'outil ;
- provenance et niveau de confiance ;
- validité temporelle et évolution d'un fait ;
- correction explicite par l'utilisateur ;
- conflit entre souvenirs ;
- récupération selon la tâche ;
- scoring, fréquence, récence et importance ;
- consolidation ;
- decay et oubli ;
- déduplication ;
- isolation entre utilisateurs, agents et sources ;
- contamination et empoisonnement de mémoire ;
- sauvegarde, export et restauration ;
- évaluation de l'écriture, du rappel et de l'influence sur la réponse.

**Reconstruction** — définir des contrats distincts pour un épisode, un fait et
une procédure, puis tracer leur écriture et leur rappel.

**Cas pratique** — apprendre une préférence, enregistrer un événement daté,
corriger un fait devenu faux et prouver que l'ancienne version n'est plus
utilisée.

**Intégration** — `memory` : politiques d'écriture, stores spécialisés,
provenance, rappel, consolidation et oubli.

---

## 9 · La boucle mono-agent

*La pièce : transformer plusieurs appels isolés en une exécution bornée.*

**Processus structurant** — `boucle-agent`.

- différence entre workflow déterministe et agent qui choisit la suite ;
- état éphémère d'un run ;
- événement utilisateur, événement modèle et événement outil ;
- boucle observer / décider / agir / intégrer ;
- ReAct ;
- plan puis exécution ;
- réflexion et critique, avec leur coût ;
- étape et transition explicites ;
- outil, handoff et réponse finale comme issues d'un tour ;
- conditions d'arrêt ;
- budget de tours, tokens, temps et outils ;
- erreurs de transport, modèle, outil et politique ;
- erreur transitoire contre erreur définitive ;
- retry et backoff ;
- annulation propagée ;
- appels parallèles et collecte partielle ;
- hooks avant et après un appel ;
- trajectoire et journal d'événements ;
- déclenchement par requête, événement ou horaire ;
- limite d'une boucle conservée seulement en mémoire du processus.

**Reconstruction** — écrire la boucle comme une machine à états éphémère dont
chaque transition produit un événement inspectable.

**Cas pratique** — exécuter une tâche multi-étapes bornée, provoquer plusieurs
catégories d'erreurs et vérifier la condition d'arrêt.

**Intégration** — `loop` : runner mono-agent, budgets, transitions et hooks.

---

## 10 · État agentique et exécution durable

*La pièce : survivre aux attentes, aux interruptions et aux redémarrages sans
perdre la position ni répéter aveuglément les effets.*

**Processus structurant** — `workflow-durable`.

- processus stateless contre agent logiquement stateful ;
- contexte du modèle, session, run, workflow et mémoire ;
- identifiants de session, run, workflow, étape, tâche et appel ;
- état éphémère contre état durable ;
- schéma d'état typé ;
- sérialisation sûre ;
- version du schéma et migration ;
- état de contrôle : étape acquise et prochaine étape ;
- statuts d'une tâche ;
- snapshot contre journal d'événements ;
- checkpoint et frontière cohérente ;
- fréquence et coût des checkpoints ;
- écritures intermédiaires d'une branche parallèle ;
- interruption et attente d'une approbation ;
- pause sans conserver le processus vivant ;
- reprise depuis le dernier checkpoint ;
- retry d'une opération ;
- replay déterministe du workflow ;
- enregistrement des résultats non déterministes ;
- fork et exploration d'une trajectoire alternative ;
- time travel pour le diagnostic ;
- appel modèle et outil comme activités ;
- effets externes `at-least-once` et `at-most-once` ;
- absence de garantie générale « exactly once » ;
- clé d'idempotence ;
- journal d'effets, inbox et outbox ;
- résultat inconnu après une coupure ;
- compensation ;
- timer durable, échéance et tâche planifiée ;
- worker, file, lease et récupération d'un travail abandonné ;
- concurrence sur un même workflow ;
- approbation expirée et revalidation de l'autorité ;
- déploiement d'une nouvelle version avec workflows ouverts ;
- rétention, chiffrement et suppression de l'état ;
- SQLite pour la reconstruction locale ;
- Temporal, Restate, DBOS, Prefect et moteurs comparables comme confrontations
  industrielles.

**Reconstruction** — écrire un checkpointer SQLite et un journal d'effets pour
la boucle du Parcours 9.

**Cas pratique** — arrêter le processus avant et après chaque frontière
d'action, reprendre le workflow et démontrer qu'aucun effet confirmé n'est
répété. Forker ensuite un checkpoint sans modifier la trajectoire originale.

**Intégration** — `state`, `checkpoints`, `workflow` et `effects`.

---

## 11 · Workspace, sandbox et skills

*La pièce : donner à l'agent un environnement de travail sans lui donner la
machine entière.*

**Processus structurant** — `action-workspace`.

- différence entre contexte du modèle et workspace ;
- fichiers, répertoires et artefacts ;
- cycle de vie d'un workspace ;
- montage de données et copie de travail ;
- shell et exécution de code ;
- processus enfant ;
- limites CPU, mémoire, disque, temps et réseau ;
- conteneur, sandbox et isolation ;
- séparation des credentials et du code généré ;
- chemins autorisés ;
- artefact produit contre fichier temporaire ;
- snapshot et restauration d'un workspace ;
- skill comme procédure et ressources chargées à la demande ;
- divulgation progressive ;
- description courte contre contenu complet ;
- instructions globales, projet, agent et tâche ;
- hooks avant et après outil ;
- installation de dépendances ;
- nettoyage ;
- audit des fichiers et commandes.

**Reconstruction** — concevoir un workspace local avec une liste explicite de
capacités, puis charger une skill sans placer tout son contenu dans le contexte.

**Cas pratique** — faire produire un artefact par un sous-processus isolé,
interrompre l'exécution et reprendre avec le même workspace restauré.

**Intégration** — `workspace`, `sandbox`, `skills`, `artifacts` et `hooks`.

---

## 12 · Sous-agents, délégation et état partagé

*La pièce : répartir un travail sans créer une mémoire globale implicite.*

**Processus structurant** — `delegation-sous-agent`.

- déterminer quand un agent unique suffit ;
- agent utilisé comme outil ;
- handoff de contrôle ;
- superviseur et ouvriers ;
- routeur déterministe contre routeur piloté par modèle ;
- délégation et contrat de résultat ;
- contexte isolé d'un sous-agent ;
- état privé par invocation ;
- état conservé par thread seulement lorsqu'il est nécessaire ;
- namespace de checkpoint par agent et par invocation ;
- état parent et champs publics partagés ;
- propriétaire et producteurs d'un champ ;
- mise à jour partielle ;
- reducer ;
- associativité et déterminisme d'une fusion ;
- append-only, version et compare-and-swap ;
- conflit entre branches ;
- fan-out et fan-in ;
- concurrence et limite de parallélisme ;
- annulation propagée ;
- backpressure ;
- résultat partiel et échec d'un ouvrier ;
- boucle de délégation ;
- partage d'une observation contre partage de tout l'historique ;
- mémoire commune contre état de workflow partagé ;
- sécurité et autorité déléguée ;
- arbitrage qualité, délai, coût et confidentialité ;
- A2A comme protocole de culture pour des agents indépendants.

**Reconstruction** — exécuter deux sous-agents en parallèle avec des états
privés, puis fusionner seulement leurs résultats publics par un reducer défini.

**Cas pratique** — comparer un agent équipé de plusieurs skills avec un
superviseur et plusieurs ouvriers sur les mêmes tâches ; provoquer un conflit
d'écriture et un échec partiel.

**Intégration** — `agents`, `handoffs` et `router`, appuyés sur l'état durable du
Parcours 10.

---

## 13 · Observabilité et évaluations

*La pièce : rendre une trajectoire explicable, comparable et reproductible.*

**Processus structurant** — `evaluation-agent`.

- événement, log, métrique, trace et span ;
- corrélation session / workflow / run / agent / outil ;
- instrumentation du client modèle ;
- instrumentation des outils, MCP, retrieval et mémoire ;
- état et checkpoint dans une trace ;
- tokens d'entrée, sortie, cache et raisonnement ;
- TTFT, latence, durée d'outil et durée totale ;
- coût cloud et coût matériel local ;
- données sensibles dans les traces ;
- OpenTelemetry et conventions GenAI ;
- replay d'une trajectoire enregistrée ;
- test unitaire déterministe ;
- test de contrat ;
- test d'intégration ;
- eval de sortie ;
- eval de retrieval ;
- eval de mémoire ;
- eval de trajectoire ;
- eval de reprise après panne ;
- jeu de données et cas de non-régression ;
- exact match, critères, score et distribution ;
- LLM-as-judge ;
- biais, ordre et calibration du juge ;
- juge différent du générateur ;
- évaluation humaine ;
- comparaison de modèle, prompt, outil et architecture ;
- diagnostic avant fine-tuning ;
- alertes, tableaux de bord et SLO personnels.

**Reconstruction** — définir un format de trace indépendant d'un fournisseur,
puis calculer une eval à partir d'événements rejoués.

**Cas pratique** — retrouver la première décision fautive d'une trajectoire,
ajouter un cas de non-régression et vérifier la reprise d'un workflow interrompu.

**Intégration** — `telemetry`, `evals` et `judge`.

---

## 14 · Sécurité du harnais

*La pièce : empêcher qu'une donnée non fiable acquière silencieusement une
autorité durable.*

**Processus structurant** — `action-securisee`.

- actifs, adversaires et frontières de confiance ;
- threat model propre au homelab ;
- donnée, instruction, capacité et autorité ;
- prompt injection directe ;
- injection indirecte par page, document, outil ou mémoire ;
- goal hijacking ;
- tool poisoning ;
- excessive agency ;
- résultat d'outil non fiable ;
- exfiltration de secrets ;
- SSRF ;
- traversée de chemins ;
- commande shell et exécution de code ;
- dépendances et supply chain ;
- serveur MCP malveillant ou compromis ;
- empoisonnement du RAG ;
- empoisonnement de mémoire persistant ;
- confusion entre agents ;
- effet en cascade ;
- état partagé comme canal d'attaque ;
- checkpoint contenant des secrets ;
- approbation ancienne ou hors contexte ;
- moindre privilège ;
- séparation des credentials ;
- sandbox et isolation réseau ;
- allowlist et validation ;
- confirmation au moment de l'effet ;
- journal d'audit ;
- chiffrement, sauvegarde et restauration ;
- tests adversariaux ;
- détection, révocation et réponse à incident ;
- OWASP LLM et OWASP Agentic comme référentiels.

**Reconstruction** — tracer les flux de confiance depuis une donnée externe
jusqu'à un outil, une mémoire et un effet durable.

**Cas pratique** — attaquer Mnémos par un document, un outil MCP, une mémoire et
une commande ; vérifier chaque barrière et la révocation d'un état contaminé.

**Intégration** — `security`, `policy` et `audit`.

---

## 15 · Voix, vision et temps réel

*La pièce : porter plusieurs modalités sans les réduire prématurément à du
texte.*

**Processus structurant** — `interaction-temps-reel`.

- contenu multimodal typé ;
- image native contre OCR ;
- préparation, redimensionnement et métadonnées d'une image ;
- VLM local ;
- caméra, consentement et durée de conservation ;
- STT puis LLM puis TTS ;
- speech-to-speech ;
- formats audio, échantillonnage et encodage ;
- streaming audio ;
- détection d'activité vocale ;
- tours de parole ;
- interruption par l'utilisateur et barge-in ;
- echo cancellation ;
- événement temps réel et état de session ;
- appel d'outil pendant une conversation vocale ;
- approbation vocale et risque d'ambiguïté ;
- latence de bout en bout ;
- budget de tokens visuels et audio ;
- modèle local contre service cloud ;
- confidentialité des flux ;
- mode dégradé sans voix ou sans vision.

**Reconstruction** — produire un flux d'événements commun au texte, à l'audio et
à l'image sans perdre le média source.

**Cas pratique** — parler à Mnémos, l'interrompre pendant sa réponse, lui faire
analyser une image et reprendre la même session après une coupure.

**Intégration** — `io` et `realtime`.

---

## 16 · Mnémos

*La pièce : assembler sans introduire un mécanisme encore inconnu.*

**Processus structurant** — `cycle-mnemos`.

- personnalité et instructions propres à Mnémos ;
- contrats de confidentialité ;
- topologie concrète des agents ;
- choix entre skills et sous-agents ;
- modèles locaux et replis autorisés ;
- outils du homelab ;
- API domotique et appareils ;
- matrice des permissions et approbations ;
- sessions persistantes ;
- workflows durables ;
- tâches déclenchées par requête, horaire ou événement ;
- état partagé explicitement limité ;
- mémoire personnelle et procédures ;
- voix et vision ;
- interface Web, mobile ou terminal ;
- observabilité, evals et audit ;
- mode hors ligne et modes dégradés ;
- sauvegarde, restauration et migration ;
- mise à jour des modèles et des dépendances ;
- runbook d'exploitation ;
- critères d'acceptation quotidiens ;
- conversion des échecs réels en evals de non-régression.

**Reconstruction** — aucune nouvelle. Chaque mécanisme doit pointer vers le
Parcours qui l'a ouvert.

**Cas pratique** — utiliser Mnémos sur des tâches réelles du homelab, conserver
les trajectoires problématiques et fermer les régressions observées.

**Intégration** — Praxis atteint sa première version stable ; Mnémos devient
l'application qui l'éprouve chaque jour.

---

## Veille transversale

La veille suit sans désorganiser le parcours :

- évolutions de MCP et de ses extensions ;
- A2A et autres protocoles inter-agents ;
- computer use et nouveaux environnements d'exécution ;
- runtimes d'inférence et techniques de cache ;
- modèles de raisonnement, outils et multimodal ;
- moteurs d'exécution durable ;
- stores de mémoire temporelle et graphes ;
- standards d'observabilité GenAI ;
- nouvelles classes d'attaques agentiques.

Une entrée de veille ne devient une leçon que si elle change un mécanisme, un
contrat, une garantie ou une décision de conception de Praxis ou de Mnémos.
