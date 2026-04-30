# Architecture agentique de référence

## Doctrine de l'état agentique

Le mot « état » ne désigne jamais un bloc indistinct. Le cours et Praxis
séparent les catégories suivantes.

### Contexte du modèle

Le contexte du modèle est la vue matérialisée envoyée pour une inférence :
instructions, messages, outils, données récupérées et résultats intermédiaires.
Il est éphémère et borné en tokens. Il ne constitue pas la source de vérité de
la session ou du workflow.

### État de session

L'état de session assure la continuité entre les tours d'une conversation. Il
porte l'identité de la session, son historique, ses résumés et les références
nécessaires pour reconstruire le prochain contexte.

Une session peut survivre au processus sans qu'un workflow soit en cours. Elle
ne mémorise pas à elle seule la position d'une exécution interrompue.

### État de run

Un run est une tentative bornée d'exécuter une demande. Son état porte les
événements produits, l'agent actif, les budgets consommés, les appels en cours,
les erreurs et les interruptions.

Un run peut rester éphémère. Dès qu'il doit reprendre après une attente ou un
redémarrage, les données nécessaires passent dans l'état durable du workflow.

### État de workflow

L'état de workflow décrit l'avancement durable d'une exécution :

- identifiants du workflow, du run et de la session ;
- version du schéma et version du code ;
- étape acquise et prochaine étape ;
- tâches prêtes, en cours, terminées ou en échec ;
- résultats déjà validés ;
- interruptions et approbations attendues ;
- délais, tentatives et budgets ;
- effets externes demandés, commencés, confirmés ou incertains.

La persistance du workflow permet la reprise après arrêt du processus. Elle ne
garantit pas à elle seule qu'un effet externe ne sera exécuté qu'une fois.

### État privé d'un agent

Un agent ou un sous-agent reçoit par défaut un état privé limité à son
invocation. Un état conservé entre plusieurs invocations doit répondre à un
besoin explicite.

Cette isolation réduit la contamination du contexte, les conflits entre tâches
parallèles et les dépendances cachées entre agents.

### État partagé

L'état partagé entre agents est un contrat, pas un dictionnaire mutable
accessible à tous.

Chaque champ partagé définit :

- son propriétaire ou ses producteurs autorisés ;
- son type ;
- sa portée et sa durée de vie ;
- sa règle de mise à jour ou de fusion ;
- son comportement en cas de concurrence ;
- sa visibilité pour le modèle et pour les outils.

Les mises à jour sont explicites, attribuées et rejouables. Les branches
parallèles utilisent des namespaces, des versions, des reducers associatifs ou
une résolution de conflit définie. Le dernier écrivain ne gagne pas par
accident.

### Mémoire longue durée

La mémoire conserve des éléments réutilisables au-delà d'une session :
préférences, épisodes, faits, procédures et relations. Elle possède ses propres
règles d'écriture, de provenance, de validité, de consolidation et d'oubli.

Une mémoire n'indique pas quelle étape d'un workflow doit reprendre. Un
checkpoint n'est pas une mémoire sémantique. Les deux peuvent employer le même
moteur de stockage sans devenir le même concept.

### État du monde extérieur

L'état d'un appareil, d'un service ou d'une base métier reste détenu par sa
source. Praxis en conserve au besoin une observation datée, jamais une copie
présumée actuelle.

Avant un effet irréversible, l'exécuteur revalide les préconditions et
l'autorité. Un état ou une approbation anciens ne valent pas indéfiniment.

## Checkpoints et reprise

Un checkpoint est un enregistrement cohérent à une frontière d'exécution. Il
contient ou référence :

- l'état durable nécessaire ;
- la position de contrôle ;
- les écritures acquises ;
- les tâches en attente ;
- les interruptions ;
- le journal des effets ;
- les versions nécessaires à la désérialisation et à la reprise.

Le cours distingue :

- **continuer** — reprendre depuis le dernier point acquis ;
- **retry** — tenter à nouveau une opération en échec ;
- **replay** — reconstruire l'état depuis un historique déterministe sans
  répéter les effets déjà enregistrés ;
- **fork** — créer une nouvelle trajectoire depuis un checkpoint antérieur.

Les appels au modèle, l'heure, le hasard, le réseau et les outils sont
non déterministes. Ils ne sont pas rejoués comme du simple code
d'orchestration : leur résultat est enregistré ou leur exécution est isolée
dans une activité.

Un effet externe utilise, selon sa nature :

- une clé d'idempotence ;
- une écriture transactionnelle ;
- un journal d'effets ou un outbox ;
- une sémantique explicite `at-most-once` ou `at-least-once` ;
- une vérification après résultat incertain ;
- une action compensatrice lorsqu'aucune idempotence n'est possible.

Les formats persistés sont versionnés et disposent d'une stratégie de
migration. Une nouvelle version de Praxis ne doit pas rendre silencieusement
ininterprétables les workflows encore ouverts.
