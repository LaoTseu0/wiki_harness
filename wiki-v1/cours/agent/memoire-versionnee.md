# Mémoire versionnée

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [le chat, l'historique et le contexte](../fondamentaux/chat-historique-contexte.md)
  — la fenêtre de contexte est **périssable** : elle se tronque, la session se
  ferme, l'état disparaît. Cette propriété est le point de départ de toute la
  leçon. [Le conteneur](conteneur-moindre-privilege.md) — le dépôt mémoire vit
  dans le périmètre de l'agent, pas à côté.
- **Débloque** : [le régime persistant](mode-rpc-sdk.md), où la session ne
  « finit » jamais et où la mémoire externe est ce qui rend la session jetable ;
  et la distinction avec le [RAG](../retrieval/rag-a-la-main.md), qui sert la
  connaissance documentaire.

## L'essentiel

La fenêtre de contexte étant périssable, la mémoire d'un agent doit vivre
**ailleurs** : des fichiers markdown dans un dépôt git, synchronisés par des
hooks de session — `pull` à l'ouverture, consolidation puis `commit` à la
fermeture. C'est le pattern « external memory » du context engineering.

La thèse : le versionnement n'est pas un confort ajouté au pattern, c'en est le
cœur. Il rend la mémoire **diffable, auditable, réversible** — et surtout, il
rend une pollution (une erreur consolidée, ou une injection) **révocable**, là où
une base opaque ne l'est pas. La mémoire d'un agent est du code, et se gouverne
comme du code.

Cette leçon ne couvre pas la connaissance documentaire volumineuse — c'est le
[RAG](../retrieval/rag-a-la-main.md) — ni la mécanique du régime persistant qui
la consomme en continu.

## Le savoir

### La mécanique des hooks de session

La convention OKF du homelab accroche la mémoire au cycle de vie de la session,
via deux hooks du harnais et un dépôt mémoire dédié.

- `session_start` → `git pull` puis chargement des fichiers pertinents dans le
  contexte initial.
- `session_shutdown` → l'agent **consolide** ce qu'il a appris dans les fichiers,
  puis `git commit` (et push).

Le dépôt est **séparé** du dépôt de code : la mémoire évolue à un autre rythme
que le programme, et mélanger les deux historiques rendrait chacun illisible.

### Ce qui va en mémoire, et ce qui n'y va pas

La frontière est ce qui distingue une mémoire d'une archive.

Y vont : les décisions et préférences durables, l'état des projets, les leçons
tirées d'incidents. N'y vont **pas** : le transcript brut (c'est du bruit), et ce
que la documentation du homelab sait déjà. Ce second interdit a une raison
mécanique — une mémoire qui **duplique sa source** dérive : la copie et
l'original divergent avec le temps, et on ne sait plus laquelle croire.

C'est aussi la frontière avec le RAG : la mémoire retient ce que l'agent a
**appris en agissant**, le RAG sert ce qui est **déjà écrit** ailleurs. Confondre
les deux, c'est soit noyer la mémoire de documentation, soit demander au RAG de
retenir des décisions qu'aucun document ne porte.

### Le protocole de consolidation, l'étape difficile

C'est un prompt, pas une routine — l'agent trie sa propre session.

1. Relire la session et lister des faits **pressentis**.
2. Filtrer par trois questions : durable ? absent de la doc *et* de la mémoire
   existante ? utile à la prochaine session ? Un « non » élimine.
3. En conflit avec l'existant, la version **datée la plus récente** l'emporte —
   l'ancienne reste dans l'historique git, elle n'est pas perdue, seulement
   dépassée.
4. Budget : quelques lignes par session, pas un compte rendu. La consolidation
   est une **sélection**, et son coût de qualité est directement ce qu'on écarte.

### Pourquoi git, précisément

Chaque propriété du versionnement répond à un besoin qu'une base opaque ne
couvre pas.

- **Audit** : `git log` répond à « pourquoi l'agent croit-il ça ? », et
  `git blame` **date** la croyance — on remonte à la session qui l'a inscrite.
- **Rollback** : une mémoire polluée — par erreur, ou par une
  [injection indirecte](../mcp/prompt-injection-indirecte.md) qui aurait écrit
  dans un fichier lu — se révoque par `revert`. Une base opaque ne rejoue pas son
  histoire à l'envers.
- **Le commit est un checkpoint** : la granularité *session* borne le rayon d'une
  pollution — on révoque une session, pas six mois de mémoire.

### La mémoire se recherche, elle ne se charge pas en bloc

Un **index court** chargé à chaque session, plus des fichiers thématiques chargés
**à la demande**. Le levier a sa portée : il agit à `session_start`, une fois par
ouverture, et ce qu'il propage est le contenu du contexte initial. Ce qui
l'annule : tout charger en bloc — la mémoire redevient alors exactement le
problème de contexte qu'elle devait résoudre, en pire, puisqu'elle grossit à
chaque session.

## Quand c'est la bonne réponse

**Une mémoire externe versionnée** dès que l'agent doit apprendre d'une session à
l'autre *et* qu'on veut pouvoir auditer ou révoquer ce qu'il a appris. Les deux
conditions comptent : sans la seconde, une base simple suffirait.

**Un RAG plutôt qu'une mémoire** pour la connaissance documentaire — volumineuse,
déjà écrite, qui n'a pas à être « apprise » mais retrouvée.

**Ne rien mémoriser** tant qu'une session suffit à la tâche. Tout mémoriser
« pour ne rien perdre » sature le contexte et noie le signal ; la valeur de la
mémoire est dans ce qu'elle **écarte**.

## Ce qu'on ne saura pas faire

On n'a pas la taille de mémoire à partir de laquelle le chargement commence à
saturer le contexte — ça se constate à l'usage, sur ce matériel et ce modèle.

Un conflit reste à trancher en situation : deux sessions **parallèles** qui
écrivent la mémoire produisent un conflit git. La parade se choisit — une seule
session écrivaine à la fois, ou des fichiers cloisonnés par domaine — mais le
choix n'est validé que confronté au cas réel.

Ce qui promouvrait cette leçon en « refaire » : des hooks `session_start` /
`session_shutdown` réels sous `wiki/etapes/agent/`, et un test de bout en bout —
apprendre un fait en session A, le retrouver en session B, le corriger en session
C, et lire l'historique pour vérifier que l'ancienne version y est restée.

## Se tester

1. Pourquoi git plutôt qu'une base dédiée pour la mémoire d'un agent ?
   *Réussi si* la réponse cite audit, rollback et blame, et insiste sur le point
   décisif : une pollution (erreur ou injection) se révoque par revert, là où une
   base opaque ne rejoue pas son histoire.
2. Distinguez ce qui va en mémoire de ce qui va au RAG, et dites pourquoi la
   frontière compte.
   *Réussi si* la réponse pose mémoire = appris en agissant (décisions,
   incidents), RAG = déjà écrit (la doc), et explique qu'une mémoire qui duplique
   la doc dérive de sa source.
3. On veut « tout mémoriser pour ne rien perdre ». Qu'est-ce que ça casse ?
   *Réussi si* la réponse voit que la mémoire enfle, le chargement sature le
   contexte et le signal se noie — et rappelle que la consolidation est une
   sélection, pas une archive.

## À retenir

- La fenêtre est périssable : la mémoire vit dans des fichiers, hors contexte, et
  se recharge à l'ouverture par un hook de session.
- Le versionnement git est le cœur du pattern, pas un bonus : il rend une
  pollution révocable, là où une base opaque ne l'est pas.
- La mémoire retient ce que l'agent a appris en agissant ; le RAG sert ce qui est
  déjà écrit. Dupliquer la doc en mémoire la fait dériver.
- La consolidation est une sélection — durable, absent de la doc et de la
  mémoire, utile ensuite —, quelques lignes par session.
- La mémoire se recherche via un index ; la charger en bloc recrée le problème de
  contexte qu'elle devait résoudre.

## Références

- La convention OKF du homelab
  ([architecture/jarvis.md](../../../../homelab/architecture/jarvis.md)) — les
  hooks de session et le dépôt mémoire dédié
