# Dogfooding

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la promotion](promotion.md) — le mécanisme par lequel
  une étape dépose une brique, et son critère du deuxième usage ;
  [l'architecture modulaire](architecture-modulaire.md) — les frontières entre
  briques, puisque c'est exactement ce que le dogfooding met à l'épreuve.
- **Débloque** : [sortie précoce et semver](sortie-precoce-semver.md), qui a
  besoin de consommateurs pour que « ne pas casser » veuille dire quelque
  chose ; et le droit de faire évoluer une interface sur autre chose qu'une
  intuition.

## L'essentiel

Le framework n'a pas d'utilisateurs imaginaires : **ses utilisateurs sont les
autres domaines de ce dépôt**. Chaque domaine consomme les briques existantes
et fait remonter ce qui manque — le framework évolue sous la pression d'usages
réels, jamais sur spéculation.

La thèse est plus forte qu'un conseil de méthode : la **friction ressentie à
l'appel est une information qu'aucune relecture de la brique ne produit**. Une
interface se juge depuis le site d'appel, pas depuis sa définition, et c'est
pourquoi son auteur est le plus mal placé pour l'évaluer.

Cette leçon ne dit pas *comment* on extrait une brique — c'est
[la promotion](promotion.md) — ni comment on publie le changement, qui est
[sortie précoce et semver](sortie-precoce-semver.md). Elle dit d'où vient le
signal qui déclenche l'un et l'autre.

## Le savoir

### Ce que la friction révèle, et que la lecture ne révèle pas

Une brique lue seule paraît toujours cohérente : elle a été écrite d'un bloc,
avec ses raisons en tête. Ce qu'on ne peut pas voir de l'intérieur, c'est
l'**écart entre sa forme et la forme du site d'appel** — l'appelant a déjà ses
données dans un certain état, et la brique en demande un autre.

Cet écart se manifeste par des signes concrets, tous observables dans le code
appelant plutôt que dans la brique :

- **des lignes d'adaptation avant chaque appel** — reconstruire un dictionnaire,
  ré-ordonner une liste, ré-emballer un résultat. Chaque ligne d'adaptation
  répétée sur deux sites est une portion de la brique qui manque.
- **un paramètre toujours passé à la même valeur.** Il n'aurait pas dû être un
  paramètre, ou sa valeur par défaut est fausse.
- **un retour qu'on déballe toujours pareil.** La brique rend trop, ou pas au
  bon niveau.
- **un contournement.** Le plus grave, et le seul qui ne laisse aucune trace si
  personne ne l'écrit.

Aucun de ces quatre signes n'est visible en relisant la brique. Les quatre sont
évidents en relisant l'appelant.

### Le contrat, et le levier qu'il constitue

Le contrat de dogfooding a deux clauses : interdiction de recoder ce qu'une
brique fait déjà, obligation de signaler ce qu'elle fait mal.

- **Où il agit** : au moment d'écrire un domaine, pas au moment d'écrire le
  framework. C'est un réflexe de consommateur.
- **À quelle fréquence** : à chaque fois qu'un besoin ressemble à une brique
  existante.
- **Ce qu'il propage** : les signalements accumulés deviennent le seul ordre du
  jour légitime des évolutions du framework. Rien d'autre n'a le droit de le
  faire bouger.
- **Ce qui l'annule** : le contournement silencieux. Un domaine qui recode « pour
  aller vite » et ne le dit pas ne produit pas une dette locale — il **détruit
  le signal**, et le framework continue de croire son interface bonne. Le
  contournement est acceptable ; le contournement tu ne l'est pas.

### Qui décide qu'une brique change

Pas « l'auteur du framework », ce qui ne nomme rien. Ce qui décide est
l'**accumulation de signalements écrits quelque part de consultable** — sans
support matériel, la règle est un vœu, parce que la friction s'oublie en deux
jours et que celui qui la ressent est occupé à autre chose.

Le support importe moins que son existence, mais il doit avoir trois
propriétés : être écrit au moment de la friction et non après coup, nommer le
site d'appel concret, et être relu à un moment défini. Sans la troisième, il
devient un cimetière.

### Deux causes pour « personne n'utilise la brique »

Le symptôme se lit pareil — le domaine a écrit son propre code — et les
corrections sont opposées.

- **La brique ne convient pas.** L'interface demande un état que l'appelant n'a
  pas, ou rend un résultat qu'il doit défaire. Correction : changer la brique.
- **Le domaine ignorait qu'elle existe.** Correction : rien à changer dans le
  code ; c'est le catalogue des briques qui est en cause.

Ce qui les distingue, en une question à celui qui a écrit le domaine : *qu'as-tu
écrit à la place, et l'as-tu écrit après avoir regardé la brique ?* La réponse
tranche immédiatement, et se pose avant toute modification — refaire une
interface qui n'avait jamais été essayée est le pire des deux gaspillages.

### L'ordre de consommation prévu

Chaque domaine consomme ce qui existe et fait remonter ce qui manque :

| Domaine | Consommerait | Ferait évoluer |
|---|---|---|
| [retrieval](../retrieval/rag-a-la-main.md) | client LLM, contexte | la brique retrieval, les evals |
| [agent](../agent/garde-fous.md) | client, outils, boucle | mémoire, garde-fous |
| [MCP](../mcp/serveur.md) | outils, retrieval | l'exposition d'outils par un protocole |
| [inférence](../inference/deploiement.md) | client — comme second backend | [providers](providers.md), routage coût/latence |
| [production](../production/observabilite.md) | toutes | l'observabilité, les traces |

Ce tableau est un plan, pas un état. Sa valeur est de désigner, pour chaque
brique, **qui sera le deuxième usage** — la seule information dont la
[promotion](promotion.md) a besoin pour ne pas deviner une interface.

## Quand c'est la bonne réponse

**Faire remonter** quand la friction se répète sur un deuxième site d'appel.
Une gêne unique peut venir du site, pas de la brique.

**Contourner et le dire** quand la correction dépasse le temps disponible. Le
contournement documenté garde le signal intact ; c'est un report, pas un abandon.

**Ne rien faire** quand la friction vient de ce que l'appelant fait quelque
chose d'inhabituel. Toute gêne ne mérite pas une évolution de l'interface :
élargir une brique pour un cas unique la rend moins bonne pour les autres, et
c'est le mécanisme exact par lequel une interface se dégrade en s'améliorant.

## Ce qu'on ne saura pas faire

Le dogfooding **n'a pas encore eu lieu**, et c'est le fait le plus important de
cette leçon. Les deux briques montées —
[`llm/ollama.py`](../../src/framework/llm/ollama.py) et
[`contexte.py`](../../src/framework/contexte.py) — n'ont à ce jour aucun
consommateur : hors du framework lui-même, seuls leurs tests les importent. Les
scripts de `etapes/` sont autonomes par construction, chacun se lisant seul avec
sa leçon.

Ce que ça laisse entièrement ouvert : on ne sait pas si `Reponse` porte les
bons champs, si `compacter` reçoit ses dépendances dans le bon ordre, ni si
`tronquer` a la bonne unité — le nombre de messages plutôt qu'un budget de
tokens. Ces trois questions **ne se répondent pas par relecture**, ce qui est
précisément la thèse de la leçon appliquée à elle-même.

Le premier consommateur réel est identifié : le domaine
[retrieval](../retrieval/rag-a-la-main.md), qui appelle un modèle à chaque
génération de réponse. Tant qu'il n'a pas consommé le client, tout ce qui est
écrit ici sur la qualité des briques est une hypothèse.

## Se tester

1. Un domaine a recodé un appel HTTP au lieu d'utiliser le client promu. Quelles
   sont les deux causes possibles, et quelle question posez-vous avant de
   toucher au code ?
   *Réussi si* la réponse sépare « la brique ne convient pas » de « son
   existence était ignorée », et pose la question qui tranche — qu'a-t-il écrit
   à la place, et avait-il regardé la brique ?
2. Vous relisez un domaine et voyez quatre lignes de préparation identiques
   avant chaque appel à une brique. Qu'est-ce que ça vous dit, et sur quoi ?
   *Réussi si* la réponse identifie une portion manquante de la brique — et
   note que le diagnostic vient du site d'appel, jamais de la brique.
3. Un collègue propose d'ajouter un paramètre à une brique pour couvrir un cas
   particulier qu'il vient de rencontrer une fois. Que répondez-vous ?
   *Réussi si* la réponse exige un deuxième site d'appel, et sait dire ce que
   coûte l'élargissement : une brique moins nette pour tous les autres appelants.

## À retenir

- La friction au site d'appel est une information qu'aucune relecture de la
  brique ne produit ; son auteur est le plus mal placé pour la voir.
- Quatre signes concrets, tous chez l'appelant : lignes d'adaptation répétées,
  paramètre toujours à la même valeur, retour toujours déballé pareil,
  contournement.
- Le contournement silencieux ne crée pas une dette locale, il détruit le
  signal — c'est ce qui annule tout le mécanisme.
- « Personne n'utilise la brique » a deux causes opposées ; une seule question
  au consommateur les sépare.
- À ce jour, aucun domaine ne consomme les briques montées : tout jugement sur
  leur qualité reste une hypothèse.

## Références

- [Architecture modulaire](architecture-modulaire.md) — les briques que les
  domaines consommeront, et leur état réel
- [`src/framework/README.md`](../../src/framework/README.md) — ce qui est monté,
  contre quoi se vérifie toute affirmation d'usage
