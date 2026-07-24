# Cadrage — le harnais et Hosef

Ce fichier fixe ce qu'on construit, en deux objets distincts. Il précède la [cartographie](cartographie.md) : c'est lui qui dit ce que chaque Parcours doit déposer.

## Le principe : des couches.

Cette V2 range par **couche du système**. Chaque Parcours est une couche, et une couche est **un seul niveau d'abstraction** : on ne mélange pas le tirage d'un token avec l'aiguillage entre agents. Les couches montent dans l'ordre où la compréhension se construit — la génération d'abord, l'orchestration en haut — et on ne redescend jamais : chaque Parcours suppose la couche du dessous acquise.

L'ordre est donc **cognitif** : on ne manipule une pièce qu'après avoir compris celle sur laquelle elle repose.

## La forme d'un Parcours

Un Parcours enseigne les **mécanismes** d'une couche — jamais un outil qu'on ne saurait pas refaire. Il se termine par deux sections fixes :

- **Cas pratique** — des exercices sur la couche, à faire, pas à lire.
- **Intégration** — la brique Hosef de la couche, déposée dans `/hosef/src`. C'est le retour au tout : la pièce comprise devient du code réutilisé.

Les notions listées sous chaque Parcours sont **exhaustives** : elles fixent ce que la rédaction devra couvrir, pour qu'aucune ne se perde. Une notion sans leçon propre part au glossaire ; aucune ne disparaît.
## Ce qui vient ensuite

Le squelette est fixé : douze Parcours, en couches, chacun d'un seul niveau d'abstraction, chacun fermé par un *Cas pratique* et une *Intégration*. Reste à dériver, Parcours par Parcours, chaque notion en leçon ou en entrée de glossaire, avec son en-tête complet — c'est là que le graphe devient vérifiable par `Hosef/outils/`. On construit un Parcours à la fois, dans l'ordre, en commençant par le 0.

- **Le terme technique est un lien** à sa première occurrence utile : vers la leçon qui le traite, sinon vers `glossaire/` (définition créée si absente). Le glossaire ne garde que ce qui n'a pas de leçon.

## Le transverse et le glossaire

Certaines notions ne sont pas une couche : elles traversent tout le projet. Elles ne forment pas un Parcours, elles se pratiquent à chaque *Intégration*.

- **Le terme technique est un lien** à sa première occurrence utile : vers la leçon qui le traite, sinon vers `glossaire/` (définition créée si absente). Le glossaire ne garde que ce qui n'a pas de leçon.

## Deux objets, pas un

**Le harnais** est la finalité : un assistant agentique complet, avant tout local, qui route entre plusieurs agents et tient une mémoire de plusieurs natures. C'est le produit.

**Hosef** — *Harness OS Framework* — est la bibliothèque sur laquelle le harnais est bâti. Elle ne connaît rien du harnais : elle expose des briques génériques — un client, une boucle, un registre d'outils, des mémoires, un routeur — que le harnais compose et configure.

## Le harnais — la finalité

Un assistant agentique complet, mono-utilisateur, auto-hébergé. « Complet » veut dire qu'il assure réellement les capacités suivantes, pas une démo de chacune :

- **Routage multi-agentique** — un superviseur oriente la tâche vers l'ouvrier compétent, et arbitre entre coût, latence et qualité.
- **Mémoire de plusieurs natures** — de travail, épisodique, sémantique, procédurale. C'est le cœur ; détaillé plus bas.
- **Boucle fiable** — retries, backoff, arrêt borné, reprise d'un outil non idempotent, garde-fous.
- **Outils natifs et distants** — un registre unique où un outil MCP est indiscernable d'un outil local.
- **Voix et vision** — entrées non-textuelles ramenées au même pipeline.
- **Observabilité** — chaque appel tracé, chaque coût chiffré, chaque trajectoire évaluable.
- **Persistance** — les sessions survivent au processus.

Ce que le harnais n'est **pas** : un service multi-tenant, une plateforme, un produit à vendre. Il sert une personne, sur sa machine. Cette limite fixe le périmètre.

## Hosef — la bibliothèque

Hosef expose une brique par couche du système. Chaque brique se dépose à la fin du Parcours qui en enseigne les mécanismes (section *Intégration*), dans `src/hosef/`. Ce tableau est le contrat entre le cours et le framework.

| Brique Hosef | Rôle | Déposée au Parcours |
|---|---|---|
| `generation` | tokeniser, compter, échantillonner, rendre le template | 0 · La génération |
| `client` | appeler le modèle, streamer, gérer l'erreur | 1 · Le transport |
| `context` | tenir la fenêtre : historique, budget, compaction | 2 · Le contexte |
| `control` | gabarits de prompt, sortie structurée validée | 3 · Le contrôle |
| `tools` | registre d'outils, dispatch — natif puis distant | 4–5 · Action, MCP |
| `memory` | magasins (vectoriel, stateful, graphe, wiki) + processus, rappel commun | 6 · La mémoire |
| `provider` | commuter local / cloud par config | 7 · Le substrat |
| `loop` · `guardrails` · `router` | la boucle, ses bornes, l'aiguillage multi-agent | 8 · L'orchestration |
| `observability` · `evals` · `judge` | tracer, chiffrer, juger, mesurer sans régression | 9 · L'exploitation |
| `io` | normaliser voix et vision vers le pipeline texte | 10 · Le multimodal |

Ce qui est **hors** Hosef : la personnalité du harnais, ses prompts système, sa topologie d'agents concrète, le câblage de ses mémoires. Hosef fournit le routeur ; le harnais décide qui sont les ouvriers.

## La mémoire — le cœur du harnais

La brique `memory` tient plusieurs `store` derrière une interface de rappel commune, plus les processus qui les maintiennent. Le détail vit dans [memoire.md](memoire.md) ; en bref :

- **Mémoire** — vectoriel (le sens), stateful (l'état exact), graphe temporel (liens datés, scoring, decay), wiki-LLM (connaissance auto-rédigée).
- **Processus** — scoring et decay, consolidation (le mode Dream), auto-apprentissage.
- **Degré zéro** — la mémoire de travail est la fenêtre elle-même : brique `context`, Parcours 2.

Hosef fournit les mémoires et les processus ; le harnais décide ce qu'il consolide, et quand lancer la consolidation.

## Ce que ça impose au cours

Deux conséquences, portées par la [cartographie](cartographie.md) :

1. **Chaque Parcours se termine par une *Intégration*** — la brique Hosef de sa couche. Le framework n'est pas un chapitre final : il sédimente couche par couche.
2. **Un Parcours de clôture assemble le harnais** — non un mécanisme neuf, mais la composition des briques Hosef en un assistant qui tourne : topologie d'agents, câblage des quatre mémoires, voix et vision, persistance.
