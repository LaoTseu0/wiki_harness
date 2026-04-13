# Règles — ce qu'on construit, et sous quelle forme une leçon rentre

Extension d'[AGENTS.md](../AGENTS.md), chargée avec lui. AGENTS.md. Il précède la [cartographie](cartographie.md), qui fixe l'ordre du parcours.
Ce chaque Parcours dépose (partie I) et la forme sous laquelle une leçon rentre (partie II).
La cartographie est l'**index** — c'est elle qui pointe vers le bas, on clique une rubrique et on tombe sur le cours

---

# Partie I · Ce qu'on construit

## Deux objets, pas un

**Le harnais** est la finalité : un assistant agentique complet, avant tout local, mono-utilisateur, auto-hébergé. Il route entre plusieurs agents et tient une mémoire de plusieurs natures. C'est le produit.

**Hosef** — *Harness OS Framework* — est la bibliothèque sur laquelle le harnais est bâti. Elle ne connaît rien du harnais : elle expose des briques génériques — un client, une boucle, un registre d'outils, des mémoires, un routeur — que le harnais compose et configure.

## Le principe : des couches

Cette V2 range par **couche du système**. Chaque Parcours est une couche, et une couche est **un seul niveau d'abstraction** : on ne mélange pas le tirage d'un token avec l'aiguillage entre agents. Les couches montent dans l'ordre où la compréhension se construit — la génération d'abord, l'orchestration en haut — et on ne redescend jamais : chaque Parcours suppose la couche du dessous acquise. L'ordre est **cognitif**.

## La forme d'un Parcours

Un Parcours enseigne les **mécanismes** d'une couche — jamais un outil qu'on ne saurait pas refaire. Il se termine par deux sections fixes :

- **Cas pratique** — des exercices sur la couche, à faire, pas à lire.
- **Intégration** — la brique Hosef de la couche, déposée dans `src/hosef/`. La pièce comprise devient du code réutilisé.

Les notions listées sous chaque Parcours dans la [cartographie](cartographie.md) sont **exhaustives** : elles fixent ce que la rédaction doit couvrir. Une notion sans leçon propre part au glossaire ; aucune ne disparaît. Le squelette est fixé — douze Parcours, en couches. On les dérive un à la fois, dans l'ordre, en commençant par le 0.

**Une seule exception à la règle « jamais un outil qu'on ne saurait pas refaire »** : au Parcours 1 (Le transport), le backend qui sert le modèle est consommé, jamais rebâti — construire un serveur d'inférence chargerait le référentiel sans rien apprendre du fil. Ollama sert d'exemple concret pour les endpoints et le streaming ; ses alternatives (llama.cpp, vLLM, LM Studio, TGI) sont citées pour ne pas orienter vers un seul outil. L'objet enseigné reste le transport — HTTP, endpoints, streaming, erreurs — pas le serveur.

## Le harnais — la finalité

« Complet » veut dire que le harnais assure réellement ces capacités, pas une démo de chacune :

- **Routage multi-agentique** — un superviseur oriente la tâche vers l'ouvrier compétent, et arbitre entre coût, latence et qualité.
- **Mémoire de plusieurs natures** — de travail, épisodique, sémantique, procédurale. C'est le cœur ; détaillé plus bas.
- **Boucle fiable** — retries, backoff, arrêt borné, reprise d'un outil non idempotent, garde-fous.
- **Outils natifs et distants** — un registre unique où un outil MCP est indiscernable d'un outil local.
- **Voix et vision** — entrées non-textuelles ramenées au même pipeline.
- **Observabilité** — chaque appel tracé, chaque coût chiffré, chaque trajectoire évaluable.
- **Persistance** — les sessions survivent au processus.

Ce que le harnais n'est **pas** : un service multi-tenant, une plateforme, un produit à vendre. Il sert une personne, sur sa machine — cette limite fixe le périmètre.

## Hosef — la bibliothèque

Une brique par couche, déposée à la fin du Parcours qui en enseigne les mécanismes (section *Intégration*), dans `hosef/src`. Ce tableau est le contrat entre le cours et le framework.

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

La brique `memory` tient plusieurs `store` derrière une interface de rappel commune, plus les processus qui les maintiennent. Détail dans [memoire.md](memoire.md) ; en bref :

- **Mémoire** — vectoriel (le sens), stateful (l'état exact), graphe temporel (liens datés, scoring, decay), wiki-LLM (connaissance auto-rédigée).
- **Processus** — scoring et decay, consolidation (le mode Dream), auto-apprentissage.
- **Degré zéro** — la mémoire de travail est la fenêtre elle-même : brique `context`, Parcours 2.

Hosef fournit les mémoires et les processus ; le harnais décide ce qu'il consolide, et quand.

## Ce que ça impose au cours

1. **Chaque Parcours se termine par une *Intégration*** — la brique Hosef de sa couche. Le framework sédimente couche par couche, il n'est pas un chapitre final.
2. **Un Parcours de clôture assemble le harnais** — non un mécanisme neuf, mais la composition des briques : topologie d'agents, câblage des quatre mémoires, voix et vision, persistance.

## Le transverse et le glossaire

Certaines notions ne sont pas une couche : elles traversent le projet et se pratiquent à chaque *Intégration*. Le terme technique est un **lien** à sa première occurrence utile — vers la leçon qui le traite, sinon vers `glossaire/` (définition créée si absente). Le glossaire ne garde que ce qui n'a pas de leçon.

---

# Partie II · Comment s'écrit une leçon

Un contrat, pas une leçon : une leçon qui ne le tient pas ne rentre pas. 

## Frontmatter

Chaque leçon s'ouvre sur un bloc de métadonnées. `promeut` pointe une brique réelle de `hosef/src`, et un contrôle échoue si elle ment. Le reste identifie et date : `id` (slug stable, unique), `type`, `titre`, `tags`, `created`, `updated`.

```yaml
---
id: sampling
type: leçon
titre: Le sampling
tags: [generation, sampling]
created: 2026-07-24
updated: 2026-07-24
promeut: hosef/sampling.py        # ou : aucune — <raison en une ligne>
---
```

## Les interdits

**Ne jamais inventer un vécu.** Un incident, une panne, une erreur ne se racontent que s'ils ont eu lieu. Pas d'anecdote plausible, pas de « on observe souvent que ».

## `Savoir le situer` et son schéma

La leçon ne décrit pas son schéma : elle déclare quel **processus** elle traverse et quelle **étape** elle ouvre. Deux lignes, jamais plus.

```markdown
## Savoir le situer

- **Processus** : [d'un texte à un token](../_processus/generation-token.md)
- **L'étape ouverte** : `sampler` — Input : des logits ; Output : un identifiant de token
- **L'essentiel**
- **Recomposer**

![[sampling.canvas]]
```

Le schéma se **génère**, il ne se dessine pas. Le processus est décrit une seule fois dans `_processus/` ; une mécanique fausse se corrige à un seul endroit. Un `.canvas` édité à la main sera écrasé. Une leçon « situer » sans processus n'a pas de schéma, et c'est normal.

```bash
python outils/canvas.py            # régénère tout
python outils/canvas.py --verifier # échoue si un schéma est périmé
```

## Le squelette

```markdown
---
<frontmatter complet>
---

# Titre

> [cartographie](../cartographie.md) · cas pratique : [`NN_sujet.py`](../cas-pratique/…)

## Prérequis et suites
---
## Savoir le situer
---
## Connaissances
---
## Ce que ça dépose dans Hosef
## Références
```

## Ce que contient chaque rubrique

Chaque rubrique a **un** travail. La liste de notions du Parcours ([cartographie](cartographie.md)) fixe l'exhaustif . La langue suit les conventions de langage AGENTS.md 

- **Titre / sous-titre** — nommer la pièce, un seul concept. Le sous-titre porte le lien vers la cartographie.
- **`Prérequis et suites`** — les prérequis en liens, les suites en liens, 5 mots max.
- **`Savoir le situer`** — quatre puces, dans l'ordre. `Processus` : le processus traversé, en lien, nommé sans redécrire la chaîne. `L'étape ouverte` : la signature (Input → Output). `L'essentiel` : la thèse, une à trois phrases vérifiables, portante et non introductive `Recomposer` : reposer la pièce dans son ensemble et en tiré une conclusion holistique.
- **`Connaissances`** — le corps : décomposer la pièce, couvrir **tous** les leviers que le référentiel liste. Contre chaque levier, sa **portée** (où il agit, à quelle fréquence, ce qu'il propage, ce qui l'annule). Une sous-notion majeure part en lien, une mineure tient en trois lignes ou file au glossaire.

## La liste de contrôle

Le versant vérification des rubriques ci-dessus. Chaque ligne se répond par oui ou non ; un seul non, la leçon repasse.

1. Le frontmatter est-il complet?
2. La leçon tient-elle sur **un** seul concept ?
3. `Savoir le situer` nomme-t-il un processus existant et une étape réelle, sans redécrire la chaîne ?
4. Le schéma se génère-t-il, et `--verifier` passe-t-il ?
5. Toute notion supposée connue est-elle liée à sa leçon, ou posée sur place en trois lignes , ou intégrer dans le glossaire le cas échéant ?
6. Toute propriété affirmée porte-t-elle son mécanisme, jamais l'adjectif-verdict seul ?
7. Chaque levier est-il donné avec sa portée — où il agit, à quelle fréquence, ce qu'il propage, ce qui l'annule ?
8. La langue tient-elle les conventions d'AGENTS.md — registre, une idée par phrase, aucune auto-référence ?
9. La leçon est elle complète sur le savoir ?
