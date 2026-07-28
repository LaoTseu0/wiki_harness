# Contrat du projet

Ce fichier définit ce que le dépôt construit, comment le cours transmet la
connaissance et sous quelle forme une pièce rejoint Praxis.

La hiérarchie des sources de vérité est :

1. [AGENTS.md](AGENTS.md) fixe les règles générales de langue, de rigueur et
   de travail ;
2. `REGLES.md` fixe le contrat propre au projet ;
3. [cartographie.md](cartographie.md) fixe l'ordre et la couverture du parcours ;
4. une leçon, un cas pratique ou une brique de code applique ces trois sources.

Une règle locale ne peut pas contredire une source placée au-dessus d'elle.

---

# Partie I · Ce que le projet construit

## La finalité d'apprentissage

Le cours s'adresse à un développeur full stack expérimenté en JavaScript, avec
des bases en Java et une pratique récente de Python.

L'apprenant retient particulièrement bien une information lorsqu'il peut la
replacer dans un schéma. La représentation visuelle n'est donc pas une
illustration facultative ajoutée après le texte : elle participe à la méthode
d'apprentissage et à la cohérence du référentiel.

Il poursuit trois résultats :

- comprendre les mécanismes qui relient un modèle de langage à un harnais
  agentique ;
- apprendre le Python nécessaire en construisant ces mécanismes ;
- faire émerger un assistant local réellement utilisé sur une infrastructure
  personnelle.

Le cours ne prépare pas une démonstration jetable. Chaque Parcours doit produire
une connaissance vérifiable et une pièce qui rapproche Mnémos d'un usage
quotidien.

## Deux objets

**Praxis** est la bibliothèque générique. Elle expose les contrats, clients,
outils, mémoires et mécanismes d'exécution appris pendant le parcours. Elle ne
connaît ni la personnalité, ni la topologie concrète, ni les appareils de
Mnémos.

**Mnémos** est l'assistant personnel construit sur Praxis. Il est local-first,
mono-utilisateur et auto-hébergé. Il peut employer un service cloud lorsqu'une
capacité locale manque, mais ce choix reste explicite et remplaçable.

Praxis fournit les mécanismes. Mnémos prend les décisions propres au produit :
agents disponibles, permissions, sources de mémoire, voix, appareils et
politiques d'exploitation.

## Ce que « maîtriser » veut dire

Le cours ouvre toute boîte noire dont le mécanisme change une décision de
conception, une limite, un risque ou une mesure.

Deux passages sont attendus :

1. reconstruire une version minimale du mécanisme ;
2. la confronter à une implémentation industrielle.

Reconstruire un sampler, un client streaming, une boucle d'outils ou un
checkpointer minimal appartient au parcours. Réécrire un pilote GPU, une pile
TLS ou un moteur de base de données n'y appartient pas. Dans ce second cas, la
leçon ouvre le contrat et les garanties de la dépendance, puis marque
explicitement la frontière.

Un outil ne tient jamais lieu de concept. Ollama, llama.cpp, vLLM, LangGraph,
Temporal ou Qdrant servent d'études de cas après l'explication du mécanisme
qu'ils matérialisent.

## L'ordre du parcours

La cartographie suit un **ordre de construction du harnais**. Cet ordre est
cognitif et pratique ; il ne prétend pas représenter une pile logicielle
strictement ascendante.

Un Parcours peut rouvrir une pièce rencontrée plus tôt lorsqu'il change de
niveau d'analyse. Le KV cache peut ainsi être expliqué pendant la génération,
puis mesuré pendant l'inférence locale.

Les notions de la cartographie sont exhaustives pour la version courante du
référentiel. Elles ne sont pas figées pour toujours. Une évolution étayée peut
modifier la cartographie et doit alors préserver les identifiants des leçons
déjà publiées ou documenter leur migration.

## La forme d'un Parcours

Chaque Parcours contient quatre résultats :

1. **Mécanismes** — les concepts à comprendre et leurs relations ;
2. **Reconstruction** — une version minimale écrite ou manipulée à la main ;
3. **Cas pratique** — une situation vérifiable sur le matériel ou les services
   du projet ;
4. **Intégration** — une brique testée déposée dans Praxis, ou l'assemblage
   explicite d'une brique déjà acquise.

À partir du premier client utilisable, chaque Parcours fait également progresser
un fil rouge de Mnémos. Le produit ne doit pas attendre le dernier Parcours pour
commencer à fonctionner.

## Local-first et comparaison

Le petit modèle local est le terrain principal :

- il rend les paramètres et les limites observables ;
- il permet de répéter les expériences ;
- il conserve les données personnelles dans l'infrastructure domestique ;
- il donne un usage concret aux mécanismes appris.

Une API cloud sert à éprouver les contrats, comparer une capacité ou fournir un
repli. Une abstraction n'efface pas les différences : contexte, streaming,
sorties structurées, outils, raisonnement et multimodal sont décrits comme des
capacités, pas comme les méthodes obligatoires d'un `Provider` universel.

## Connaissance stable et veille

La cartographie contient les mécanismes durables. Les fonctions mouvantes d'un
produit ou d'un protocole vivent dans `Wiki/veille/`.

Une entrée de veille porte :

- son statut : `stable`, `adopté`, `à comparer`, `émergent` ou `déprécié` ;
- une source primaire ;
- la version ou la date vérifiée ;
- le mécanisme concerné ;
- la décision : intégrer, attendre ou écarter.

Une nouveauté ne rejoint pas le cours parce qu'elle est populaire. Elle le
rejoint si elle modifie un mécanisme, un contrat, une garantie, une menace ou
une décision mesurable.

## Doctrine visuelle

Le cours suit une approche **holistique → analytique → holistique** :

1. voir l'ensemble complet ;
2. ouvrir une étape ou un élément et comprendre son mécanisme ;
3. replacer cette pièce dans l'ensemble et suivre ses relations.

Le texte et le schéma portent deux fonctions différentes. Le texte explique les
causes, les garanties et les limites. Le schéma conserve les positions, les
frontières et les relations. Aucun des deux ne remplace l'autre.

### Un processus

Un processus est une suite ordonnée de transformations qui possède un Input
global, un Output global et des étapes reliées par un flux de données ou de
contrôle.

Une architecture statique, une taxonomie ou une carte de concepts n'est pas
appelée « processus ». Elle peut recevoir un autre schéma, mais ne donne pas une
fausse étape précédente et une fausse étape suivante à une leçon.

Chaque processus est décrit une seule fois dans `generator/guardrails/schema/processus/`. Son fichier
`.canvas` complet constitue la source de vérité visuelle. Le registre
`generator/guardrails/schema/processus/index.md` fixe son identifiant, son nom, son Input, son Output
et son statut.

### Un sous-processus

Une étape trop dense peut ouvrir un autre Canvas canonique. L'Input et l'Output
du sous-processus raffinent alors l'Input et l'Output locaux de l'étape parente
sans les contredire.

Le nœud parent lie le sous-processus. Une leçon référence le niveau le plus
précis qui contient son mécanisme ; le processus parent reste la vue
holistique de recomposition.

### Un schéma non séquentiel

Une connaissance sans ordre temporel reçoit un schéma non séquentiel plutôt
qu'un faux processus. Sa source canonique vit dans
`generator/guardrails/schema/references/`. Le registre `generator/guardrails/schema/index.md` fixe son
identifiant, son type, sa portée et son statut.

Cinq types sont admis :

- **architecture** — les groupes représentent l'appartenance ou une frontière ;
  chaque arête nomme une dépendance, un appel, une lecture ou une production ;
- **carte de concepts** — chaque arête verbalise la relation entre deux notions ;
  la distance visuelle ne porte aucun sens non documenté ;
- **arbre de décision** — un nœud préfixé `DÉCISION` pose une question, chaque
  arête porte une condition et chaque feuille nomme l'issue ;
- **cycle de vie** — un nœud préfixé `ÉTAT` représente une situation stable et
  une arête nomme l'action ou l'événement qui provoque la transition ;
- **carte de responsabilités** — chaque nœud nomme un propriétaire, une donnée
  ou un contrat ; chaque arête qualifie la responsabilité échangée.

Une forme n'est jamais interprétée par ressemblance. Son sens vient de son type,
de son libellé et de la convention déclarée dans le registre.

### JSON Canvas

Les schémas utilisent JSON Canvas 1.0 et l'extension `.canvas`.

Un processus complet respecte ces conventions :

- les identifiants de nœuds et d'arêtes sont uniques et stables ;
- l'identifiant d'une étape est un slug lisible, réutilisé par le Frontmatter
  des leçons ;
- le flux principal se lit de gauche à droite ;
- une boucle de retour passe sous le flux principal ;
- une arête porte un libellé lorsque sa donnée ou sa condition n'est pas
  évidente ;
- un nœud contient un intitulé court ; le détail appartient à la leçon ;
- un nœud d'annotation commence par `note:` et ne fait pas partie du flux
  structurel ;
- la couleur ne porte jamais seule une information.

La palette des vues de leçon est stable :

- étape ouverte : violet, avec le préfixe `ÉTAPE OUVERTE` ;
- étape précédente : cyan, avec le préfixe `AMONT` ;
- étape suivante : vert, avec le préfixe `AVAL` ;
- autres étapes : style neutre.

Pour un schéma non séquentiel :

- élément ouvert : violet, avec le préfixe `ÉLÉMENT OUVERT` ;
- élément directement relié : cyan, avec le préfixe `RELATION DIRECTE` ;
- autres éléments : style neutre.

La couleur ne crée ni ordre ni causalité dans un schéma non séquentiel.

### Vue contextualisée d'une leçon

Une leçon liée à un processus déclare `processus` et `etape` dans son
Frontmatter. Une leçon liée à un schéma non séquentiel déclare `schema` et
`element`. Dans ce second cas, `processus` porte `aucun — <raison>` et `etape`
est absent.

L'outillage copie le Canvas canonique et retire ses annotations secondaires.
Pour un processus, il met en évidence l'étape ouverte, son amont et son aval.
Pour un autre schéma, il met en évidence l'élément ouvert et ses relations
directes.

La vue produite vit dans `generator/guardrails/schema/canvas/<id-de-leçon>.canvas`. Elle est
générée et ne se modifie jamais à la main. Une correction du flux se fait dans
le Canvas complet du processus, puis toutes les vues concernées sont
régénérées.

Chaque leçon possède un repère visuel : processus ou schéma non séquentiel. Elle
ne reçoit jamais un faux diagramme de flux pour satisfaire cette obligation.

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

## Praxis

Une brique est déposée à la fin du Parcours qui en ouvre les mécanismes.

| Brique Praxis | Rôle | Dépôt |
|---|---|---|
| `contracts` · `config` | types communs, configuration, erreurs | Préambule |
| `generation` | tokeniser, rendre un Template, échantillonner, arrêter | 0 |
| `inference` | décrire et mesurer un runtime local | 1 |
| `models` · `client` | contrats par capacité, transport et streaming | 2 |
| `context` · `sessions` | composer le contexte et persister les sessions | 3 |
| `control` | prompts, sorties contraintes et validation | 4 |
| `tools` · `permissions` · `approvals` | enregistrer, autoriser et exécuter une action | 5 |
| `mcp` | adapter des outils et ressources distants | 6 |
| `knowledge` · `retrieval` | ingérer, rechercher, reranker et citer | 7 |
| `memory` | écrire, retrouver, consolider et oublier | 8 |
| `loop` | exécuter une boucle mono-agent bornée | 9 |
| `state` · `checkpoints` · `workflow` · `effects` | persister et reprendre une exécution | 10 |
| `workspace` · `sandbox` · `skills` · `artifacts` | fournir un environnement d'action isolé | 11 |
| `agents` · `handoffs` · `router` | déléguer et coordonner plusieurs agents | 12 |
| `telemetry` · `evals` · `judge` | observer, rejouer et mesurer | 13 |
| `security` · `policy` · `audit` | imposer les frontières de confiance | 14 |
| `io` · `realtime` | porter la voix, la vision et les interruptions | 15 |

Le Parcours final assemble Mnémos. Il n'introduit aucun mécanisme de
persistance, de sécurité ou d'orchestration qui n'aurait pas été exercé
auparavant.

## Mnémos

La première version stable de Mnémos assure réellement :

- une conversation persistante ;
- une exécution locale par défaut ;
- des outils natifs et MCP derrière les mêmes politiques ;
- des approbations pour les effets sensibles ;
- une reprise après interruption ou redémarrage ;
- des tâches déclenchées par requête, événement ou horaire ;
- plusieurs natures de mémoire avec provenance et correction ;
- des sous-agents isolés et un état partagé explicite ;
- des entrées vocales et visuelles ;
- des traces, evals et journaux d'audit ;
- un mode dégradé lorsque le modèle, un outil ou le réseau manque ;
- une sauvegarde et une restauration documentées.

Mnémos n'est ni une plateforme multi-tenant, ni un produit commercial, ni un
prétexte pour distribuer prématurément chaque composant.

## Exigences transverses d'une Intégration

Une Intégration dépose :

- un contrat typé ;
- des erreurs définies ;
- des tests unitaires déterministes ;
- au moins un test d'intégration à la frontière réelle ;
- des mesures lorsque la propriété étudiée est quantitative ;
- des événements observables ;
- une analyse des effets de bord et des risques ;
- une configuration documentée ;
- les limites connues de la brique.

La sécurité et l'observabilité commencent avec la première frontière externe.
Leurs Parcours dédiés assemblent et éprouvent les mécanismes déjà déposés.

## Organisation du dépôt

| Chemin | Rôle |
|---|---|
| `generator/README.md` | point d'entrée de l'outillage de génération |
| `generator/guardrails/parcours/AGENTS.md` | règles générales de langue, de rigueur et de travail |
| `generator/guardrails/parcours/REGLES.md` | contrat pédagogique et éditorial du projet |
| `generator/guardrails/parcours/cartographie.md` | ordre et couverture du parcours |
| `Wiki/parcours/` | leçons rangées par Parcours |
| `generator/guardrails/parcours/modeles/` | gabarits éditoriaux à copier |
| `generator/guardrails/schema/processus/` | registre et Canvas complets des processus |
| `generator/guardrails/schema/references/` | Canvas canoniques non séquentiels |
| `Wiki/cas-pratique/` | exercices et expériences exécutables |
| `Wiki/corrections/` | réponses et corrections séparées des leçons |
| `Wiki/glossaire/` | définitions sans leçon propre |
| `Wiki/veille/` | état des techniques et protocoles mouvants |
| `generator/guardrails/schema/canvas/` | vues de leçon générées depuis les Canvas canoniques |
| `Praxis/` | bibliothèque générique et ses tests |
| `Mnemos/` | assistant concret et ses tests |
| `raw/` | sources brutes, non normatives |
| `generator/tools/` | contrôles et génération des schémas |

Le contenu de `raw/` ne rejoint jamais une leçon sans demande explicite et
validation. Une note brute peut contenir une piste, pas une vérité du cours.

Praxis et Mnémos possèdent chacun leur runtime Python, leur `pyproject.toml`,
leur environnement virtuel et leurs dépendances. Aucun environnement Python ne
vit à la racine.

Les identifiants de code suivent les conventions de l'écosystème Python. Les
commentaires et docstrings pédagogiques sont en français, encodés en UTF-8. Les
imports passent par les packages ; aucun `sys.path.insert` ne masque un
packaging incomplet.

---

# Partie II · Sous quelle forme une leçon rejoint le cours

## Un seul concept

Une leçon ouvre une seule pièce. Elle peut montrer ses relations, mais ne
réenseigne pas les pièces voisines. Une notion majeure possède sa propre leçon.
Une notion secondaire tient en quelques lignes ou rejoint le glossaire.

La cartographie fixe ce que chaque Parcours doit couvrir. Une notion ne peut pas
disparaître pendant la rédaction : elle devient une leçon, une partie
explicitement rattachée à une leçon, ou une entrée de glossaire.

## Cadrage d'un Parcours avant rédaction

Avant la première leçon d'un Parcours, sa rubrique de cartographie reçoit un
tableau `Découpage prévu`. Chaque ligne fixe :

- l'ordre et l'identifiant stable de la leçon ;
- son titre de travail ;
- son processus et son étape, ou `aucun — <raison>` ;
- son schéma et son élément lorsqu'elle n'ouvre pas un processus ;
- les connaissances qui lui sont exclusivement attribuées.

Le tableau est le contrat de génération des leçons. Le rédacteur ne déplace pas
une connaissance vers une autre leçon et n'élargit pas la couverture sans
modifier d'abord la cartographie.

Toutes les notions de la liste du Parcours possèdent exactement une destination
dans le tableau. Plusieurs leçons peuvent ouvrir la même étape lorsqu'elles
étudient des mécanismes distincts de cette étape. Un processus référencé doit
être au moins `cadré` dans `generator/guardrails/schema/processus/index.md`. Un schéma référencé doit
être au moins `cadré` dans `generator/guardrails/schema/index.md`.

## Frontmatter

Chaque leçon commence par :

```yaml
---
id: sampling
type: leçon
titre: Le sampling
parcours: 0-generation
statut: brouillon
tags: [generation, sampling]
created: 2026-07-24
updated: 2026-07-24
verified: 2026-07-24
processus: generation-token
etape: sampling
brique: generation
contrat: praxis.generation.Sampler
---
```

Une leçon sans processus remplace `etape` par le couple `schema`–`element` :

```yaml
processus: aucun — architecture statique du projet
schema: environnement-projet-python
element: environnement-virtuel
```

- `id` est stable et unique ;
- `parcours` correspond à une section de la cartographie ;
- `statut` vaut `brouillon`, `en-revue` ou `validé` ;
- `verified` date la dernière vérification des sources mouvantes ;
- `processus` correspond à un Canvas de `generator/guardrails/schema/processus/` ;
- `etape` correspond à un nœud stable de ce Canvas ;
- `schema` correspond à un Canvas de `generator/guardrails/schema/references/` ;
- `element` correspond à un nœud stable de ce schéma ;
- `brique` nomme la brique Praxis concernée ;
- `contrat` nomme l'API publique déposée ou vaut `aucun — <raison>`.

Une mise à jour éditoriale change `updated`. Une nouvelle vérification des
sources change `verified`.

Une leçon déclare exactement un couple de positionnement : `processus`–`etape`
ou `schema`–`element`.

## Squelette

Les fichiers `generator/guardrails/parcours/modeles/lecon.md` et
`generator/guardrails/parcours/modeles/lecon-schema.md` matérialisent les variantes processus et schéma
non séquentiel. Le modèle retenu est copié puis ses marqueurs sont remplacés ;
il n'est pas lui-même une leçon.

```markdown
---
<Frontmatter complet>
---

# Titre

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> cas pratique : [`sujet.py`](../../cas-pratique/...)

## Prérequis

## Savoir le situer

## Connaissances

## Reconstruction

## Décision et dépôt dans Praxis

## Limites et cas d'échec

## Se tester

## Mesures

## Références
```

`Mesures` est présent lorsque la leçon avance ou produit un résultat
quantitatif. Il est omis dans le cas contraire.

## Prérequis

Cette rubrique contient seulement les notions réellement nécessaires, sous
forme de liens courts.

Une dépendance non liée est soit posée sur place, soit ajoutée au glossaire,
soit reconnue comme lacune de la cartographie.

Les suites ne sont pas maintenues manuellement. Elles sont la relation inverse
des prérequis et sont calculées par l'outillage ou consultées par les backlinks
d'Obsidian.

## Savoir le situer

Pour une leçon de processus, la rubrique contient quatre éléments :

- **Processus** — nomme et lie le Canvas complet. Il donne l'Input initial,
  l'Output final et les grandes étapes sans rouvrir leurs mécanismes ;
- **Étape ouverte** — place la pièce dans la chaîne
  `étape précédente → étape ouverte → étape suivante`, puis donne son Input, son
  Output et la frontière exacte de sa responsabilité ;
- **L'essentiel** — énonce en une à trois phrases le mécanisme central qui
  explique la transformation de l'Input en Output ;
- **Recomposer** — replace la pièce dans le processus. Il précise ce qu'elle
  reçoit de l'amont, ce qu'elle garantit à l'aval et comment une modification
  ou une défaillance locale se propage.

Pour une leçon sans processus, les quatre fonctions cognitives restent les
mêmes, mais les deux premiers libellés deviennent :

- **Ensemble** — nomme le type du schéma, lie sa vue complète et explique sa
  règle de lecture ;
- **Élément ouvert** — nomme la pièce étudiée, ses relations directes et la
  frontière exacte de sa responsabilité ;
- **L'essentiel** — énonce en une à trois phrases son mécanisme ou sa
  responsabilité centrale ;
- **Recomposer** — replace la pièce dans l'ensemble et explique les relations
  qui seraient affectées par sa modification ou sa défaillance.

La rubrique ne redécrit pas tout le processus ou tout le schéma.

La rubrique applique à petite échelle la progression
holistique → analytique → holistique. Elle embarque la vue contextualisée
générée :

```markdown
![[<id-de-leçon>.canvas]]
```

Le Canvas complet reste accessible par le lien `Processus` ou `Ensemble`. La
vue embarquée sert à retrouver immédiatement la position de la pièce ouverte.

`Recomposer` est une opération cognitive : replacer la pièce dans le tout.
`Reconstruction` est une expérience exécutable : isoler puis observer le
mécanisme. Les deux rubriques ne sont pas interchangeables.

## Connaissances

Cette rubrique décompose les points clés attribués à la leçon par la
cartographie. Elle n'ajoute pas un panorama voisin pour donner une impression
de complétude.

Pour chaque point important, elle précise :

- où il agit ;
- quand et à quelle fréquence il agit ;
- ce qu'il modifie ou propage ;
- ce qui le rend inopérant ;
- son coût et sa limite lorsqu'ils influencent une décision.

Un nom d'outil apparaît après le mécanisme qu'il implémente.

## Reconstruction

La reconstruction est la plus petite expérience qui rend le mécanisme
observable. Elle peut être imparfaite et lente ; sa limite est explicitée.

Elle ne copie pas une bibliothèque sous une forme réduite. Elle isole la cause
que la leçon veut montrer.

## Décision et dépôt dans Praxis

Cette rubrique relie la connaissance au code :

- décision retenue ;
- alternatives considérées ;
- critère qui les départage ;
- coût accepté et condition qui ferait revoir la décision ;
- contrat créé ou modifié ;
- invariant ajouté ;
- erreur représentée ;
- tests qui prouvent le comportement ;
- dépendances autorisées.

Une leçon sans dépôt explique pourquoi elle prépare une pièce ultérieure.

## Limites et cas d'échec

Cette rubrique trace la frontière :

- ce que la reconstruction ne prouve pas ;
- ce que Praxis ne garantit pas encore ;
- la dépendance externe qui demeure ;
- la suite qui l'ouvrira ;
- les conditions qui font échouer ou invalident le mécanisme.

## Se tester

Cette rubrique contient trois à cinq questions qui obligent à récupérer et
manipuler la connaissance sans recopier la leçon :

- prédire le résultat d'une variation ;
- diagnostiquer une erreur ;
- comparer deux décisions ;
- expliquer une propagation dans le processus ;
- modifier une hypothèse ou une contrainte.

Les réponses vivent dans une correction séparée. Le cas pratique vérifie la
capacité d'exécution ; `Se tester` vérifie la compréhension du mécanisme.

## Mesures

Une mesure indique :

- l'hypothèse ;
- le matériel et les versions ;
- l'entrée et la charge ;
- la métrique ;
- plusieurs répétitions lorsque la variance compte ;
- le résultat brut ;
- l'interprétation autorisée.

Une valeur issue d'une documentation n'est pas présentée comme une mesure du
projet.

## Références

Les références pointent au plus près de l'affirmation qu'elles soutiennent.
Pour un protocole ou une API, la version est indiquée. Pour un comportement
observé, le dépôt, la version du logiciel et le protocole de reproduction sont
conservés.

Une leçon sur un sujet mouvant ne passe pas la relecture si ses sources
primaires n'ont pas été vérifiées récemment.

## Contrat d'un cas pratique

Un cas pratique donne :

- l'objectif observable ;
- les prérequis matériels et logiciels ;
- l'état initial ;
- les étapes à réaliser ;
- les résultats à conserver ;
- les critères de réussite ;
- les pannes ou variations à provoquer ;
- le nettoyage nécessaire.

Il ne donne pas immédiatement la solution complète. Une correction séparée
explique les mécanismes, pas seulement le code final.

## Liste de contrôle d'une leçon

Une leçon ne rejoint le parcours que si chaque réponse est positive :

1. Le Frontmatter est-il complet et cohérent ?
2. La leçon tient-elle sur un concept ?
3. Ses prérequis sont-ils disponibles et liés ?
4. Le processus et ses étapes voisines, ou l'ensemble et ses relations
   directes, sont-ils exacts ?
5. Toutes les notions exigées par la cartographie sont-elles couvertes quelque
   part ?
6. Chaque propriété importante porte-t-elle son mécanisme ?
7. Chaque levier porte-t-il sa portée et ses limites ?
8. La reconstruction isole-t-elle réellement le mécanisme ?
9. La décision Praxis nomme-t-elle ses alternatives et son critère ?
10. Si la leçon dépose un contrat, existe-t-il et ses invariants sont-ils
    testés ? Sinon, l'absence est-elle justifiée ?
11. Les questions de `Se tester` vérifient-elles autre chose qu'une récitation ?
12. Les mesures sont-elles reproductibles ?
13. Les sources sont-elles primaires, actuelles et précisément rattachées ?
14. La langue respecte-t-elle `AGENTS.md` ?
15. Le Canvas canonique, la pièce ouverte et la vue générée sont-ils cohérents ?

## Liste de contrôle d'un Parcours

Un Parcours n'est terminé que si :

1. chaque notion de la cartographie possède une destination ;
2. aucune notion majeure n'est enseignée à deux endroits ;
3. le graphe des prérequis ne contient pas de cycle accidentel ;
4. les processus et schémas référencés possèdent un Canvas complet et valide ;
5. les reconstructions s'assemblent dans l'Intégration ;
6. le cas pratique mobilise les mécanismes annoncés ;
7. les contrats Praxis et leurs tests existent ;
8. l'incrément du fil rouge Mnémos emploie réellement la brique.

## Contrôles du dépôt

Les contrôles automatisés vivent dans `generator/tools/`. Ils doivent à terme
vérifier :

- Frontmatter, identifiants et Parcours ;
- liens morts et fichiers orphelins ;
- notions de la cartographie sans destination ;
- briques et contrats Praxis inexistants ;
- rubriques obligatoires ;
- processus, schémas, références de la cartographie et vues Canvas périmées ;
- vocabulaire explicitement proscrit ;
- tests et dépendances entre briques Praxis.

Les Canvas se régénèrent et se vérifient avec :

```bash
python generator/tools/canvas.py
python generator/tools/canvas.py --verifier
```

Une autre commande n'est documentée comme disponible qu'après l'ajout de son
script.
