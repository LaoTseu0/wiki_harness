# Cadrage — le harnais et HOSeF

Ce fichier fixe ce qu'on construit, en deux objets distincts. Il précède la [cartographie](cartographie.md) : c'est lui qui dit ce que chaque Parcours doit déposer.

## Deux objets, pas un

**Le harnais** est la finalité : un assistant agentique complet, local d'abord, qui route entre plusieurs agents et tient une mémoire de plusieurs natures. C'est le produit.

**Hosef** — *Harness OS Framework* — est la librairie sur laquelle le harnais est bâti. Elle ne connaît rien du harnais : elle expose des briques génériques — un client, une boucle, un registre d'outils, des mémoires, un routeur — que le harnais compose et configure.

> React est à une application dynamique ce que HOSeF est à un harnais : la librairie ne décide pas *ce qu'*on construit, elle rend le *comment* tenable.

HOSeF est l'étape intermédiaire du projet ; le harnais est le but. Le cours construit HOSeF brique par brique, puis assemble le harnais avec.

## Le harnais — la finalité

Un assistant agentique complet, mono-utilisateur, auto-hébergé. « Complet » veut dire qu'il tient les capacités suivantes pour de vrai, pas une démo de chacune :

- **Routage multi-agentique** — un superviseur oriente la tâche vers l'ouvrier compétent, et arbitre entre coût, latence et qualité.
- **Mémoire de plusieurs natures** — de travail, épisodique, sémantique, procédurale. C'est le cœur ; détaillé plus bas.
- **Boucle fiable** — retries, backoff, arrêt borné, reprise d'un outil non idempotent, garde-fous.
- **Outils natifs et distants** — un registre unique où un outil MCP est indiscernable d'un outil local.
- **Voix et vision** — entrées non-textuelles ramenées au même pipeline.
- **Observabilité** — chaque appel tracé, chaque coût chiffré, chaque trajectoire évaluable.
- **Persistance** — les sessions survivent au processus.

Ce que le harnais n'est **pas** : un service multi-tenant, une plateforme, un produit à vendre. Il sert une personne, sur sa machine. Cette borne tient le périmètre.

## Hosef — la librairie

Hosef expose une brique par couche du système. Chaque brique se dépose à la fin du Parcours qui en enseigne les mécanismes (section *Intégration*), dans `src/hosef/`. Ce tableau est le contrat entre le cours et le framework.

| Brique HOSeF | Rôle | Déposée au Parcours |
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

Ce qui est **hors** HOSeF : la personnalité du harnais, ses prompts système, sa topologie d'agents concrète, le câblage de ses mémoires. HOSeF fournit le routeur ; le harnais décide qui sont les ouvriers. Comme React fournit l'état, pas votre modèle de données.

## La mémoire — le cœur du harnais

La brique `memory` tient plusieurs magasins derrière une interface de rappel commune, plus les processus qui les maintiennent. Le détail vit dans [memoire.md](memoire.md) ; en bref :

- **Magasins** — vectoriel (le sens), stateful (l'état exact), graphe temporel (liens datés, scoring, decay), wiki-LLM (connaissance auto-rédigée).
- **Processus** — scoring et decay, consolidation (le mode Dream), auto-apprentissage.
- **Degré zéro** — la mémoire de travail est la fenêtre elle-même : brique `context`, Parcours 2.

HOSeF fournit les magasins et les processus ; le harnais décide ce qu'il consolide, et quand il rêve.

## Ce que ça impose au cours

Deux conséquences, portées par la [cartographie](cartographie.md) :

1. **Chaque Parcours se termine par une *Intégration*** — la brique HOSeF de sa couche. Le framework n'est pas un chapitre final : il sédimente couche par couche.
2. **Un Parcours de clôture assemble le harnais** — non un mécanisme neuf, mais la composition des briques HOSeF en un assistant qui tourne : topologie d'agents, câblage des quatre mémoires, voix et vision, persistance.
