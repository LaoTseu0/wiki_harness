# Évolutivité sans friction

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [l'architecture modulaire](architecture-modulaire.md) —
  les briques et le sens de leurs dépendances ; [le function
  calling](../fondamentaux/function-calling.md) — et précisément que le
  catalogue d'outils est **du prompt**, re-transmis à chaque tour. Cette
  seconde propriété ressert plus bas : elle est la raison pour laquelle
  « ajouter un outil ne coûte rien » est faux, même quand le critère
  d'architecture est tenu.
- **Débloque** : l'ajout d'outils par le domaine [agent](../agent/garde-fous.md)
  sans toucher au cœur ; l'ajout d'un [provider](providers.md), qui est le même
  problème sur une autre brique.

## L'essentiel

Le critère d'architecture du framework tient en une phrase : **ajouter un
outil, un provider ou un agent doit se faire en créant un fichier, sans
modifier le cœur**. Si une extension demande d'éditer trois fichiers existants,
l'architecture a une dette.

L'intérêt de ce critère n'est pas d'être vrai — c'est d'être **vérifiable par
une commande**. Une architecture énoncée en principes se dégrade sans qu'on le
voie ; celle-ci se teste, donc elle se défend.

La leçon affirme aussi sa limite, qui est l'erreur symétrique : un point
d'extension écrit avant le besoin ne supprime pas la friction, il la déplace
dans le mécanisme d'extension lui-même. Elle ne couvre pas *où* une brique
atterrit — c'est [l'architecture modulaire](architecture-modulaire.md) — ni
*quand* on la publie, qui est [sortie précoce et semver](sortie-precoce-semver.md).

## Le savoir

### Le principe, et pourquoi il ne suffit pas de l'énoncer

« Ouvert à l'extension, fermé à la modification » — le O de SOLID. Énoncé seul,
c'est un vœu : tout le monde y souscrit, personne ne sait dire si son code le
respecte.

Ce qui le rend opérant est de le transformer en **observation** : après avoir
ajouté une extension, `git diff --stat` ne doit montrer que des fichiers
nouveaux. Aucun fichier existant modifié. C'est binaire, ça se lit en une
seconde, et ça ne se discute pas.

### Le mécanisme : un registre, et le vrai coût de chaque variante

Chaque type extensible a un point d'enregistrement unique. Trois façons de le
faire, et elles ne se valent pas — la question à leur poser est toujours la
même : *qu'est-ce qui garantit que le fichier neuf est lu ?*

- **L'import explicite d'un paquet.** Le fichier neuf est ajouté à une liste,
  ou le paquet est parcouru au démarrage. Simple, sans magie, et il **casse le
  critère** dans sa version liste — le fichier d'index compte comme une
  modification du cœur. Dans sa version parcours du dossier, il le tient.
- **Le décorateur.** L'enregistrement a lieu comme effet de bord de l'import du
  module. Le critère est tenu, au prix d'une dépendance à l'ordre des imports :
  un module jamais importé n'enregistre rien, et l'absence est silencieuse.
- **Les points d'entrée de packaging.** La découverte passe par les métadonnées
  installées. C'est la version qui marche pour des extensions écrites par des
  tiers, et elle impose une réinstallation à chaque ajout — donc elle est
  disproportionnée ici.

Le choix n'est pas « la plus élégante » mais la plus faible qui tienne le
critère, et c'est le parcours de dossier tant que toutes les extensions
vivent dans le même dépôt.

### Le registre global est un piège, et la raison n'est pas l'esthétique

Un registre global muable, importé partout, tient le critère et détruit la
testabilité — ce qui compte davantage.

Le mécanisme : l'état du registre dépend alors de **quels modules ont été
importés**, donc de l'ordre d'exécution. Deux tests qui enregistrent des outils
différents se contaminent selon leur ordre de passage, et le second échoue seul
mais passe quand on le lance isolément. C'est le mode de panne le plus coûteux
à diagnostiquer, parce que le symptôme accuse le mauvais test.

La correction est structurelle, pas cosmétique : le registre se **construit
explicitement au démarrage** et se passe en paramètre — la même règle que la
dépendance reçue plutôt qu'importée, vue à la [promotion](promotion.md).

### Ce que le critère ne mesure pas

Le critère porte sur le **coût de modification du code**. Il ne dit rien de
trois coûts qui, eux, augmentent bel et bien à chaque ajout, et les confondre
donne une fausse assurance :

- **le prompt.** Un outil de plus, c'est un schéma de plus dans le catalogue,
  re-transmis et re-facturé à chaque tour de chaque conversation
  ([function calling](../fondamentaux/function-calling.md)). Zéro friction de
  code, coût permanent en tokens.
- **la précision du choix.** Plus le catalogue est long, plus le modèle a
  d'occasions de se tromper d'outil. C'est une dégradation continue, sans seuil
  visible.
- **la surface d'attaque.** Chaque outil est une capacité de plus accordée au
  modèle. Le critère d'architecture est parfaitement satisfait par l'ajout
  d'un outil dangereux.

Ces trois-là ne sont pas des objections au critère : ce sont des grandeurs d'un
**autre niveau**, qu'aucun `git diff` ne verra jamais. Les ranger avec lui
serait précisément l'erreur — croire qu'une architecture propre rend l'ajout
gratuit.

### Le levier « point d'extension », avec sa portée

- **Où il agit** : au démarrage, à la construction du registre. Pas à
  l'exécution d'une requête.
- **À quelle fréquence** : une fois par processus.
- **Ce qu'il propage** : la disponibilité de l'extension partout où le registre
  est passé — donc, pour un outil, jusque dans le prompt de chaque appel.
- **Ce qui l'annule** : un `Enum` central, un `match` sur les noms, une
  validation de configuration qui liste les valeurs permises. Il suffit d'un
  seul de ces trois pour que le fichier neuf ne suffise plus, et c'est
  exactement ce que le test attrape.

## Quand c'est la bonne réponse

**Ouvrir un point d'extension** quand le deuxième cas concret existe et que le
troisième est certain. Les outils remplissent ce critère : il y en a déjà
quatre à l'étape d'agent, et le domaine agent en ajoutera.

**Ne pas en ouvrir** pour un type dont on n'a qu'une implémentation. Un
registre de providers avec une seule entrée n'est pas une extension possible,
c'est une indirection — et elle rend le code plus difficile à suivre pour
zéro capacité gagnée.

**Le remplacer par rien** quand la variation est rare et le nombre de cas
fermé. Trois stratégies de découpage connues d'avance ne demandent pas un
registre : un dictionnaire littéral les couvre, et il se lit en entier d'un
coup d'œil. La friction supposée n'apparaîtra jamais.

## Ce qu'on ne saura pas faire

Aucun registre n'existe dans [`src/framework/`](../../src/framework/README.md)
à ce jour, et le test d'architecture décrit ici n'a jamais tourné : ce sont
deux briques — `outils/`, `agent/` — qui ne sont pas encore promues. Le critère
est donc pour l'instant une **exigence posée d'avance**, pas un résultat.

Ce que ça laisse ouvert : on ne sait pas si le parcours de dossier suffira le
jour où les outils MCP arriveront, puisqu'un outil distant n'est pas un fichier
du dépôt mais une entrée découverte au démarrage d'une session. Il est possible
que la découverte statique et la découverte dynamique demandent deux mécanismes
au lieu d'un — auquel cas « un seul pattern à apprendre » tombe.

Ce qui promouvrait cette leçon en leçon « refaire » : l'écriture du registre et
du test d'architecture, avec un outil jouet ajouté dans un fichier neuf et un
`git diff --stat` qui ne montre que lui.

## Se tester

1. Votre framework accepte un nouveau provider en créant un seul fichier, mais
   ce provider doit aussi être ajouté à un `Enum` validé par la configuration.
   Le critère est-il tenu ?
   *Réussi si* la réponse dit non et sait dire pourquoi ça se voit : le
   `git diff --stat` montre un fichier existant modifié.
2. Un test d'outils passe seul et échoue dans la suite complète. Quelle
   hypothèse le registre rend-il probable, et quelle correction structurelle
   suit ?
   *Réussi si* la réponse cible l'état global dépendant de l'ordre des imports,
   et propose un registre construit au démarrage et passé en paramètre — pas un
   « nettoyage entre les tests ».
3. On vous dit : « l'architecture est bonne, ajouter un outil ne coûte rien ».
   Que corrigez-vous ?
   *Réussi si* la réponse distingue le coût de modification, qui est bien nul,
   d'au moins deux coûts qui ne le sont pas — tokens du catalogue à chaque
   tour, précision du choix, surface d'attaque.

## À retenir

- Le critère : une extension = un fichier neuf, zéro fichier existant modifié.
  Sa valeur vient de ce qu'il se vérifie par une commande.
- Le mécanisme le plus faible qui tienne le critère est le bon ; le parcours de
  dossier suffit tant que tout vit dans le même dépôt.
- Un registre global muable tient le critère et casse les tests : l'état dépend
  de l'ordre des imports, et l'échec accuse le mauvais test.
- Le critère ne mesure que le coût de code. Le prompt, la précision du choix et
  la surface d'attaque croissent quand même.
- Un `Enum` central, un `match` sur les noms ou une liste de valeurs permises
  annulent le critère à eux seuls.

## Références

- Le principe ouvert/fermé (SOLID) — pour l'énoncé, en gardant que c'est la
  version testable qui a de la valeur ici
- Les points d'entrée de packaging Python — la version industrielle du pattern,
  à situer pour savoir ce qu'on ne fait pas et pourquoi
