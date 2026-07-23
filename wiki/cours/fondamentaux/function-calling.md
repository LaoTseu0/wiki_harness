# Function calling à la main

> [carte du cours](../carte.md) · étape : [`06_outils.py`](../../etapes/fondamentaux/06_outils.py)

## Où ça s'emboîte

- **Processus** : [d'une tâche à un résultat](../_processus/boucle-outils.md)
- **L'étape ouverte** : `emission` · `dispatch` — entre un schéma annoncé, sort un nom d'outil résolu en fonction Python

![[function-calling.canvas]]

## Prérequis et suites

- **Suppose acquis** : [le format messages](chat-historique-contexte.md) — la
  liste `[{role, content}]` renvoyée en entier à chaque tour, et le fait qu'il
  n'existe aucun état côté serveur ; [le template de chat](template-de-chat.md)
  — la liste de messages est aplatie en **un texte unique** avant d'atteindre le
  modèle. Ces deux propriétés resservent : la première explique pourquoi un
  résultat d'outil doit devenir un message pour exister au tour suivant, la
  seconde explique pourquoi un modèle dont le template ignore les outils ne
  peut pas en appeler, quoi qu'on envoie.
- **Débloque** : [la boucle d'agent](boucle-agent.md), qui n'est que la
  répétition bornée de ce cycle ; [le structured output](structured-output.md),
  qui traite le schéma pour lui-même ; [les outils MCP](../mcp/serveur.md), où
  la fonction Python appelée vit dans un autre processus.

## L'essentiel

Le modèle ne peut rien *faire* — il ne fait que générer du texte, comme au
premier appel HTTP. Le function calling est un **contrat de format** : on
annonce des outils en schéma JSON, le modèle produit un appel structuré, notre
code le résout et l'exécute, et le résultat redevient un message.

La thèse de la leçon est plus étroite que « le modèle appelle des outils » : à
aucun moment le modèle n'appelle quoi que ce soit. Trois pièces distinctes
décident, et les confondre est ce qui rend le tool calling magique — donc
indébogable. Cette leçon les sépare.

Elle ne couvre pas la **répétition** du cycle ni sa borne, qui sont
[la boucle d'agent](boucle-agent.md), ni ce que le schéma contraint réellement
pendant la génération, qui est [le structured output](structured-output.md).

## Le savoir

### Le cycle, en quatre pièces

1. **Annoncer** — chaque outil est un triplet nom + description + schéma JSON
   des paramètres, placé dans le champ `tools` de la requête.
2. **Émettre** — au lieu d'un contenu texte, le message rendu porte un
   `tool_calls` : un nom, et des arguments JSON.
3. **Résoudre et exécuter** — notre code cherche le nom dans un dictionnaire,
   et appelle la fonction Python correspondante avec les arguments déballés.
4. **Renvoyer** — la valeur de retour repart dans l'historique en message de
   rôle `tool`, et le tour suivant la voit.

Tout tient au niveau HTTP et JSON. Rien de ce cycle n'exige de bibliothèque.

### Qui décide, exactement

C'est le point que « le modèle choisit un outil » escamote. Trois pièces se
succèdent, et chacune peut être la coupable d'un comportement inattendu.

- **Le modèle décide qu'un appel est opportun** — et il en décide sur la seule
  base du texte qu'il lit : le nom et la description de l'outil, tels que le
  template les a inscrits dans le prompt. Il ne voit ni la signature Python, ni
  le code, ni ce que la fonction a fait la dernière fois.
- **Le serveur décide que ce texte *est* un appel.** Le modèle a produit des
  tokens ; c'est le serveur d'inférence qui, en suivant le template du modèle,
  reconnaît la portion balisée et la remonte dans un champ `tool_calls` du
  JSON de réponse plutôt que dans `content`. Le même flux de tokens, sous un
  template qui ne prévoit pas de section outils, ressort en texte ordinaire.
- **Notre code décide de ce qui s'exécute.** Le dictionnaire de dispatch
  (`FONCTIONS`) est la seule autorité : un nom absent du dictionnaire ne
  s'exécute pas, quoi qu'ait produit le modèle.

*Le modèle propose, le serveur transcrit, le code dispose.* Une explication qui
s'arrête à « le modèle appelle l'outil » ne permet de déboguer aucune des trois.

### La description est un levier, et c'est le seul

La description d'un outil n'est pas de la documentation : c'est **du prompt**.
Elle mérite donc d'être traitée comme tel, avec sa portée entière.

- **Où elle agit** : à l'étape `schema`, en amont de toute génération. Elle
  n'entre jamais dans l'exécution — une description mensongère décrira mal un
  outil qui fonctionnera parfaitement.
- **À quelle fréquence** : une fois par requête, donc **à chaque tour**. Le
  catalogue entier est re-transmis et re-facturé à chaque appel, exactement
  comme l'historique — c'est le coût fixe qu'un
  [prompt caching](../inference/prompt-caching.md) viserait en premier.
- **Ce qu'elle propage** : elle décide du choix entre outils, et elle décide
  aussi de la **forme des arguments** — le champ `description` d'un paramètre
  est ce sur quoi le modèle se règle pour formater une date, une expression ou
  un chemin. Un exemple dans la description vaut mieux qu'un paragraphe.
- **Ce qui l'annule** : un template de modèle sans section outils. Le champ
  `tools` est alors ignoré à la fusion, la description n'atteint jamais le
  modèle, et aucune rédaction ne rattrapera ça. `ollama show <modèle>
  --template` tranche en une commande.

### Le dispatch n'est pas au même niveau que les trois autres pièces

Les étapes 1, 2 et 4 sont des conventions de format : elles disent comment on
se parle. Le dictionnaire de dispatch, lui, est une **barrière de sécurité**, et
c'est une pièce d'un autre niveau glissée dans la même chaîne.

Sa propriété n'est pas d'aiguiller mais de **clore l'ensemble des possibles** :
l'univers des fonctions appelables est exactement l'ensemble de ses clés. Un
`getattr(module, nom)` ferait le même aiguillage et n'aurait pas cette
propriété — la différence n'apparaît que le jour où le nom généré n'est pas
celui qu'on attendait.

Les arguments, eux, restent des **entrées non fiables** au sens strict : ils
traversent la barrière sans être vérifiés. `calculer` le montre en petit — un
`eval()` non filtré exécuterait ce que le modèle a écrit. Le filtre de `06`
n'autorise qu'un jeu fermé de caractères ; c'est la même politique de
liste blanche qui reviendra en grand au
[périmètre de l'agent](../agent/garde-fous.md).

### ReAct, et ce que le function calling natif en retire

Le cycle est la boucle **ReAct** (*Reasoning + Acting*) industrialisée, à une
différence près qui s'entend rarement : le papier fait générer une trace de
raisonnement explicite (`Thought:`) **avant** chaque action, dans le texte
lui-même. Le function calling natif n'émet que l'action ; le raisonnement, s'il
existe, reste implicite ou se loge dans le contenu texte qui précède l'appel.

La conséquence est pratique : sur un modèle qui n'écrit rien avant son
`tool_calls`, on n'a **aucune trace** de pourquoi cet outil-là a été retenu. Un
mauvais choix d'outil ne se diagnostique alors que par l'extérieur — en
modifiant une description et en observant si le choix bascule.

## En pratique

[06_outils.py](../../etapes/fondamentaux/06_outils.py) : trois outils —
`heure_actuelle` (une information que le modèle ne *peut pas* savoir, ses
poids étant figés), `calculer` (un `eval()` sous liste blanche de caractères),
et `modeles_charges`, à écrire de bout en bout : requête HTTP, schéma JSON,
entrée de dispatch.

**À prédire avant de lancer** — chaque réponse se vérifie à l'écran, les
demandes et les résultats étant tracés à chaque tour :

- si on pose une question qui n'appelle aucun outil, combien de fois le cycle
  passe-t-il par `emission` ? Et si on en pose une qui en demande deux ?
- que devient l'historique après un appel d'outil : combien de messages ont
  été ajoutés, et de quels rôles ?
- on renomme `calculer` en `outil_2` sans toucher à sa description : le modèle
  l'appelle-t-il encore ? Et si on vide la description en gardant le nom ?
- on demande une expression contenant une lettre, par exemple `2 * pi` : que
  reçoit le modèle, et que fait-il de ce retour ?

## Mesures

<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->

## Recomposer

**Ce que ça change à ce qu'on croyait savoir.** Le rôle `tool` n'est pas une
quatrième catégorie de message à côté de `system`, `user` et `assistant` : c'est
la preuve que l'historique est le **seul canal** par lequel une information
entre dans le modèle. Un résultat qu'on n'ajoute pas à la liste n'a pas eu
lieu, quelle que soit la réalité du disque. Le fait stateless de
[chat, historique et contexte](chat-historique-contexte.md) cesse d'être une
particularité d'API pour devenir la contrainte qui structure toute la boucle.

De même, le champ `tools` prend sa place dans le budget de contexte : ce n'est
pas un paramètre de requête à côté du prompt, c'est **du prompt**, compté en
[tokens](tokenisation.md) comme le reste. Ajouter un outil coûte à chaque tour
de chaque conversation.

**Ce qu'on peut prédire ailleurs.** Si le catalogue est du prompt, alors le
nombre d'outils dégrade la précision du choix bien avant de saturer la fenêtre
— pour la même raison qu'un prompt trop chargé dilue une consigne. On peut
donc prédire que passé un certain nombre d'outils, un harnais devra les
présenter par sous-ensembles plutôt que tous à la fois, et que
[les outils MCP](../mcp/serveur.md) hériteront du problème sans le créer :
un outil distant coûte le même prompt qu'un outil local.

## Pièges connus

- **Rencontrés** :
  - *Le modèle s'est trompé dans un argument.* En demandant la création d'un
    fichier, il a produit un nom comportant une faute de frappe. L'outil a
    fonctionné — il a écrit le fichier demandé, au nom demandé. Rien dans la
    chaîne ne pouvait détecter l'écart : les arguments sont générés, donc
    faillibles au même titre que le texte, et un outil qui réussit ne dit rien
    de la justesse de ce qu'on lui a passé. La leçon transférable :
    **toute vérification de sens appartient à l'outil**, jamais au format.
- **Anticipés** — non vérifiés à ce jour :
  - *Le message de résultat n'est pas relié à sa demande.* Dans `06`, le
    résultat est ajouté par `{"role": "tool", "content": ...}` sans nom d'outil
    ni identifiant d'appel. Tant que le modèle ne demande qu'un outil à la
    fois, l'association est évidente ; avec plusieurs `tool_calls` dans le même
    message, elle devient positionnelle, donc fragile. Les API qui imposent un
    `tool_call_id` répondent exactement à ça.
  - *Une exception dans un outil arrête tout.* `fonction(**args)` n'est protégé
    par aucun `try`. Une fonction qui lève interrompt le script au lieu de
    rendre l'erreur au modèle — qui, lui, saurait souvent se corriger si on la
    lui donnait. Le retour d'erreur est une information, pas un échec.
  - *La boucle de résolution de `06` n'a pas de borne.* Le `while True` interne
    sort sur l'absence de `tool_calls` ; un modèle qui en redemande
    indéfiniment n'est arrêté par rien. C'est précisément ce que
    [la boucle d'agent](boucle-agent.md) ajoute.

## Se tester

1. Un modèle ne rend jamais de `tool_calls`, quelle que soit la question, alors
   que le champ `tools` est bien envoyé et que les descriptions sont soignées.
   Quelles sont les deux causes possibles, et quelle observation les sépare ?
   *Réussi si* la réponse distingue « le modèle a jugé l'outil inutile » de
   « le template n'a pas de section outils, le champ a été ignoré », et nomme
   une vérification qui tranche sans deviner — lire le template du modèle.
2. Vous ajoutez un outil `supprimer_fichier` au catalogue mais oubliez de
   l'ajouter au dictionnaire de dispatch. Que se passe-t-il si le modèle le
   demande, et pourquoi est-ce le bon comportement par défaut ?
   *Réussi si* la réponse dit que rien ne s'exécute et que le modèle reçoit un
   texte d'outil inconnu, et rattache ça à la propriété du dispatch : l'univers
   des fonctions appelables est l'ensemble de ses clés, pas ce qu'on a annoncé.
3. Le modèle affirme avoir consulté l'heure alors qu'aucune trace d'exécution
   n'apparaît. Deux mécanismes produisent ce même écran : lesquels, et que
   regardez-vous pour savoir lequel vous avez sous les yeux ?
   *Réussi si* la réponse oppose « le résultat n'a jamais été ajouté à
   l'historique » à « aucun appel n'a été émis, le modèle a produit une
   réponse plausible », et va lire la liste `messages` plutôt que l'écran.

## Ce que ça change dans le framework

Rien n'est promu, et c'est un choix daté, pas un oubli. Le catalogue et le
dispatch de `06` sont deux structures littérales — une liste de dictionnaires
et un dictionnaire de fonctions — dont l'écriture n'est pas ce qui coûte. Ce
qui coûterait, c'est de figer maintenant la forme d'un **registre d'outils**
alors qu'on n'en connaît qu'un usage : des fonctions locales, appelées en
direct, dans le processus courant.

Le deuxième usage concret est identifié et pas encore écrit : un outil
[MCP](../mcp/serveur.md), qui vit dans un autre processus et dont l'exécution
est une requête. C'est lui qui dira si le registre doit rendre une valeur ou
attendre, s'il porte un schéma ou sait le produire, et où se branchent les
gardes. L'écrire avant, c'est deviner l'interface — le critère de
[promotion](../framework/promotion.md) appliqué tel quel.

Ce que la leçon dépose en attendant est ailleurs : la **règle** que les
arguments sont des entrées non fiables, qui vaudra pour tout outil promu, quel
que soit son transport.

## À retenir

- Le function calling est un contrat de format ; le modèle ne fait jamais
  qu'écrire du texte.
- Trois pièces décident, et pas une : le modèle juge l'appel opportun, le
  serveur reconnaît l'appel dans les tokens produits, le dispatch clôt ce qui
  peut s'exécuter.
- La description est du prompt : re-transmise à chaque tour, elle décide du
  choix de l'outil et de la forme des arguments, et un template sans section
  outils l'annule entièrement.
- Le dictionnaire de dispatch est une barrière, pas un aiguillage : l'univers
  des fonctions appelables est l'ensemble de ses clés.
- Un résultat qui n'entre pas dans l'historique n'a pas eu lieu pour le modèle.

## Références

- Doc *tool use* d'Ollama et de la Claude Messages API — mêmes concepts, champs
  différents ; à lire en parallèle pour voir ce qui est du protocole et ce qui
  est du fournisseur
- `ollama show <modèle> --template` — le seul moyen de savoir si un modèle
  sait recevoir des outils
- Papier ReAct (Yao et al., 2022) — pour situer l'origine du pattern et voir
  la trace de raisonnement que le function calling natif a retirée
