# Architecture modulaire

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la promotion](promotion.md) — ce qui fait qu'un bout de
  code mérite de monter, et le critère « l'interface attend le deuxième usage ».
  Une notion s'y ajoute et se pose ici, parce que toute la leçon repose
  dessus : un **cycle de dépendances** est le cas où A a besoin de B et B a
  besoin de A. Ce n'est pas une inélégance — c'est la preuve que A et B sont en
  réalité une seule pièce, qu'on ne peut ni tester ni remplacer séparément.
- **Débloque** : [l'évolutivité](evolutivite.md), qui traite d'ajouter *dans*
  une brique ; [les providers](providers.md), qui est le cas d'école d'une
  frontière ; [le dogfooding](dogfooding.md), qui dit d'où vient la pression
  qui fait bouger ces frontières.

## L'essentiel

Le framework se découpe en briques dont chacune a une interface étroite et un
remplaçant concevable : client LLM, contexte, outils, boucle, mémoire,
retrieval, evals. La règle tient en une ligne — **les dépendances vont dans un
seul sens**, et une brique n'appelle jamais une autre brique concrète.

La thèse qu'on peut contredire n'est pas « il faut découper », que personne ne
conteste. C'est que **le bon critère de découpe n'est pas le concept mais la
substituabilité** : deux choses appartiennent à la même brique si on ne peut
pas remplacer l'une sans que l'autre s'en aperçoive. Découper par thème produit
des frontières qui ont l'air justes et que le premier `import` traverse.

Cette leçon ne couvre pas ce qui se passe à l'intérieur d'une brique quand on
l'étend — c'est [l'évolutivité](evolutivite.md) — ni quand on publie le
résultat, qui est [sortie précoce et semver](sortie-precoce-semver.md).

## Le savoir

### Les sept briques, et l'état réel du dossier

| Brique | Ce qu'elle rend | État |
|---|---|---|
| client LLM | un appel, une réponse, un flux | montée — [`llm/ollama.py`](../../src/framework/llm/ollama.py) |
| contexte | tronquer, compacter une liste de messages | montée — [`contexte.py`](../../src/framework/contexte.py) |
| outils | déclarer, résoudre, exécuter | pas écrite — un seul usage à ce jour |
| boucle | mener une tâche à son terme, bornée | pas écrite — sa forme n'est pas décidée |
| mémoire | ce qui survit à une session | pas écrite — aucun usage encore |
| retrieval | d'une question à des passages | pas écrite — le domaine tourne en scripts |
| evals | d'un jeu de cas à des scores | pas écrite |

Deux sur sept. Ce n'est pas un retard : c'est le régime normal du dépôt, où
une brique n'existe qu'après sa leçon. Le tableau sert à savoir **ce qu'on
n'a pas le droit d'invoquer** comme s'il existait.

### Le sens des dépendances, et ce qui l'impose

Le sens autorisé : la boucle dépend des outils et du client ; le RAG dépend du
retrieval et du client. **Jamais l'inverse**, et jamais une brique vers une
autre brique *concrète*.

La raison n'est pas la pureté. Une dépendance qui remonte crée un cycle, et un
cycle a trois conséquences immédiates et vérifiables : la brique basse ne se
teste plus sans la haute ; elle ne se réutilise plus sans traîner la haute ;
et un changement dans la haute peut casser la basse, ce qu'aucune lecture de
la basse ne laissait prévoir.

Ce qui l'impose, concrètement : **rien**, tant que personne ne regarde. C'est
le point qu'il faut nommer plutôt que de faire confiance à la discipline. Le
sens des dépendances est une propriété du graphe d'imports, donc elle se
constate mécaniquement — la lire une fois par mois, ou l'assertion dans un
test, sont les deux seules formes qui tiennent. Une convention écrite dans un
fichier de conventions ne tient pas.

### Ce qui fait une frontière, et le test qui la valide

Le critère utile n'est pas « ça parle du même sujet » mais **ça se remplace
d'un bloc**. Le test : *puis-je nommer un remplaçant plausible, et savoir
exactement quels fichiers changeraient ?* Si la réponse est « un peu partout »,
la frontière est décorative.

Appliqué au dépôt : le client LLM passe le test — un autre backend, et seule
la construction change ([providers](providers.md)). La « mémoire » ne le passe
pas encore, parce qu'on ne sait pas si elle rend des messages, des faits ou des
documents ; nommer la brique ne suffit pas à l'avoir.

### L'interface est un levier, avec sa portée

- **Où elle agit** : au point de couture entre deux briques, à la construction.
- **À quelle fréquence** : une fois, à l'assemblage. Une interface qu'on
  consulte à chaque appel n'est plus une frontière, c'est un aiguillage.
- **Ce qu'elle propage** : sa forme contamine tous les appelants. Un contrat
  asynchrone rend asynchrone tout ce qui l'appelle, de proche en proche.
- **Ce qui l'annule** : une implémentation unique. Le contrat décrit alors
  cette implémentation, et le remplacement qu'il promet n'existe pas — c'est
  pourquoi `llm/` n'a **pas** de classe de base aujourd'hui.

### Deux causes pour « j'ai dû toucher trois fichiers »

Le symptôme est le même, les corrections sont opposées, et c'est l'erreur de
diagnostic la plus coûteuse de ce domaine.

- **La découpe est fausse.** Ce qu'on croyait deux briques n'en fait qu'une :
  les trois fichiers changent ensemble parce qu'ils changent *toujours*
  ensemble. La correction est de fusionner, pas d'ajouter un point d'extension.
- **Le point d'extension manque.** La découpe est juste, mais l'ajout passe par
  une liste centrale, un `Enum`, un `match` sur des noms. La correction est
  [l'évolutivité](evolutivite.md).

Ce qui les distingue : regarder l'**historique**. Si les trois fichiers ont
toujours été modifiés dans les mêmes commits, c'est une seule brique. S'ils
bougent d'habitude séparément et que seule cette extension-ci les réunit, c'est
le point d'extension qui manque.

### L'anti-modèle nommé, et pourquoi il n'est pas au même niveau

L'objet qui sait tout faire — la chaîne qui enchaîne prompt, retrieval, appel
et parsing derrière une méthode unique — est ce que cette architecture refuse.
Mais il faut le ranger correctement : ce n'est **pas** une septième brique mal
découpée, c'est un choix d'un autre niveau, celui de la *composition*. On
compose à la main, avec des pièces qu'on peut nommer, plutôt que de configurer
un objet qui compose pour nous.

Le coût est réel et s'assume : plus de lignes chez l'appelant, et personne pour
écrire les branchements à notre place. Ce qu'on achète : chaque étape reste
observable, et une panne se localise dans une pièce plutôt que dans une
configuration.

## Quand c'est la bonne réponse

**Découper** quand un remplaçant est nommable et qu'un deuxième consommateur
existe. Les deux conditions, pas une : un remplaçant sans consommateur donne
une abstraction spéculative, un consommateur sans remplaçant donne une
indirection inutile.

**Ne pas découper** tant qu'un seul appelant existe. Le code reste dans
l'étape, où il est lisible avec sa leçon.

**Fusionner** quand deux briques changent toujours ensemble. C'est le seul
mouvement de cette leçon qui va à contre-courant de l'intuition « plus modulaire
est mieux », et c'est souvent le bon.

## Ce qu'on ne saura pas faire

Cinq briques sur sept n'existent pas, donc le sens de leurs dépendances est
pour l'instant une **intention**, pas un constat. Aucun graphe d'imports n'a
été vérifié : avec deux modules dont un seul en importe un autre, il n'y a rien
à vérifier.

Trois questions restent ouvertes et ne se tranchent pas par raisonnement : où
se branchent les garde-fous — dans la brique boucle, ou en amont d'elle ? La
mémoire est-elle une brique ou une propriété de la boucle ? Le retrieval rend-il
des passages, ou un contexte déjà mis en forme — ce qui déciderait s'il dépend
du client LLM ou non ?

Ce qui promouvrait cette leçon en leçon « refaire » : le jour où trois briques
au moins se consomment, un test qui lit le graphe d'imports et échoue sur une
dépendance remontante. Tant qu'il n'existe pas, la règle du sens unique n'est
pas outillée.

## Se tester

1. Vous ajoutez une brique `memoire` qui, pour résumer d'anciens échanges,
   importe le client LLM. Est-ce une dépendance autorisée ?
   *Réussi si* la réponse ne tranche pas sur le sens seul mais demande **comment**
   elle l'obtient : importée, c'est un couplage à une brique concrète ; reçue en
   paramètre, c'est le schéma déjà retenu pour `compacter`.
2. Trois fichiers changent à chaque ajout d'un type de document. Deux
   diagnostics sont possibles : lesquels, et qu'allez-vous regarder ?
   *Réussi si* la réponse oppose « découpe fausse » à « point d'extension
   manquant » et propose de lire l'historique des commits pour trancher.
3. On vous propose d'écrire dès maintenant les sept modules vides avec leurs
   `Protocol`, « pour poser l'architecture ». Que répondez-vous ?
   *Réussi si* la réponse rattache le refus au nombre d'implémentations — un
   contrat écrit à zéro ou une implémentation ne décrit rien — et note qu'un
   dossier vide est une intention, pas une architecture.

## À retenir

- Le critère de découpe est la substituabilité, pas le thème : deux choses sont
  une brique si on ne peut pas remplacer l'une sans que l'autre le sache.
- Les dépendances vont dans un seul sens, et un cycle signifie que les deux
  briques n'en sont qu'une.
- Rien n'impose ce sens tant qu'aucun test ne lit le graphe d'imports.
- Une interface à implémentation unique décrit cette implémentation.
- « J'ai dû toucher trois fichiers » a deux causes opposées ; l'historique des
  commits les sépare.
- Deux briques sur sept existent — le reste est une intention, et se dit comme
  telle.

## Références

- [`src/framework/README.md`](../../src/framework/README.md) — l'état réel, qui
  fait foi contre toute description
- Le [routeur multi-modèles](../../../../homelab/architecture/router-multi-model.md)
  du homelab — une frontière déjà éprouvée ailleurs, à confronter à celle qu'on
  vise ici
- Le principe d'inversion des dépendances (le D de SOLID), et `typing.Protocol`
  qui l'exprime en Python sans héritage
