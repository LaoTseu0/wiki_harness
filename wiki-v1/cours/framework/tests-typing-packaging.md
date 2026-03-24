# Tests, typing, packaging

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la promotion](promotion.md) — et son constat que
  rendre testable déplace la frontière entre transport et logique ;
  [clean code](clean-code.md) — les pratiques dont cette leçon prend le versant
  vérification. Une notion se pose ici, et elle porte toute la première moitié :
  un système est **non déterministe** quand deux exécutions identiques peuvent
  donner deux résultats. C'est le cas de tout ce qui traverse un
  [tirage](../fondamentaux/sampling.md), et ce n'est pas le cas du reste.
- **Débloque** : le droit de promouvoir une brique — sans ce dispositif, « la
  leçon est acquise » n'a pas de preuve ; [sortie précoce et
  semver](sortie-precoce-semver.md), qui a besoin de tests verts comme
  déclencheur.

## L'essentiel

Il n'y a pas de domaine « qualité » séparé : ce qui suit est la **porte
d'entrée** du framework, ce qu'une brique doit tenir pour monter.

La difficulté propre à ce dépôt tient en une phrase : le cœur du système est
non déterministe, et on ne peut pas écrire d'assertion sur une sortie qui
change à chaque appel. La thèse de la leçon est qu'il n'y a pas là de fatalité
mais une **erreur de découpage** — la quasi-totalité du code écrit ici est
parfaitement déterministe, et le non-déterminisme entre par un point unique et
nommable. Le tester revient à savoir où passe ce point, et à ne jamais mélanger
les deux côtés dans la même suite.

Cette leçon ne couvre pas les pratiques elles-mêmes — annoter, valider,
documenter sont [clean code](clean-code.md) — ni la mesure de la qualité des
réponses, qui est [les evals](../retrieval/evals.md). Elle couvre le dispositif
qui les constate.

## Le savoir

### Trois étages, parce qu'ils n'ont pas le même verdict

Le découpage utile n'est pas par vitesse — la vitesse en découle — mais par
**nature du verdict** : que signifie exactement un échec ?

- **Unitaires.** Sur le cœur déterministe : découpage de documents, similarité
  sur des valeurs connues, fusion de listes classées, analyse d'un flux. Sans
  réseau. Un échec signifie *le code est faux*, sans ambiguïté. C'est le seul
  étage dont le verdict soit binaire, et c'est ce qui lui donne sa valeur.
- **Intégration.** La chaîne complète sur un corpus minuscule et dédié, avec le
  modèle simulé. Un échec signifie *le branchement est faux* — les pièces sont
  bonnes séparément et ne s'emboîtent pas.
- **Evals comme tests.** L'assertion porte sur un score comparé à une référence.
  Un échec signifie *quelque chose a bougé*, et pas nécessairement dans le code
  — c'est le seul étage dont le verdict demande une enquête.

Ces trois verdicts n'appellent pas la même réaction, et c'est pourquoi ils ne
peuvent pas vivre dans la même exécution. Un marqueur les sépare, pour lancer le
rapide sans le lent.

### Où se pose la simulation, et pourquoi il n'y a qu'un seul endroit

Le non-déterminisme entre dans le système à un endroit précis : l'appel au
modèle. C'est donc **à la frontière du provider** que la simulation se pose, et
ce choix n'est pas une commodité.

Le raisonnement se fait par élimination, et il vaut pour n'importe quel système
à cœur aléatoire :

- **plus haut** — simuler la brique de retrieval entière, par exemple — laisse
  le non-déterminisme à l'intérieur de ce qu'on teste, et le test redevient
  instable ;
- **plus bas** — simuler la couche HTTP — oblige à fabriquer des réponses
  réalistes du serveur, donc à réimplémenter sa forme dans les tests ; le jour
  où elle change, les tests passent toujours et le code est cassé.

La frontière du provider est l'unique point où l'on remplace *exactement* la
source d'aléa, sans emporter de logique ni singer un protocole. C'est là que
l'abstraction de [providers](providers.md) se paie, et c'est un argument plus
solide que la commutabilité elle-même : même sans jamais changer de backend, la
frontière est ce qui rend le reste testable.

### Ce que coûte réellement un test instable

Un test qui échoue une fois sur dix ne coûte pas dix pour cent du temps : il
coûte **la confiance dans toute la suite**. Le mécanisme est humain et parfaitement
prévisible — au troisième échec sans cause, l'échec cesse d'être lu comme un
signal et devient un bruit qu'on relance. À partir de ce moment, les vrais
échecs passent inaperçus au milieu des faux, et la suite entière ne vaut plus
rien.

C'est pourquoi la règle « les tests rapides ne parlent jamais au modèle » n'est
pas une préférence de performance. Un seul test probabiliste laissé dans l'étage
rapide suffit à détruire la propriété qui fait la valeur de cet étage : *rouge
signifie cassé*.

### Le seuil d'eval, avec sa portée

- **Où il agit** : dans l'assertion d'un test marqué, comparant un score à une
  référence enregistrée.
- **À quelle fréquence** : avant une publication, pas à chaque commit — il
  demande le vrai corpus et du calcul.
- **Ce qu'il propage** : il transforme une mesure en garde-fou, et rend une
  régression visible sans qu'on ait à y penser.
- **Ce qui l'annule** : une référence enregistrée sans son contexte. Un seuil
  n'a de sens qu'accompagné du modèle exact, du matériel et de l'état du corpus
  qui l'ont produit — sans quoi il mesure la dérive de l'environnement autant
  que celle du code. L'annule aussi un seuil qu'on abaisse quand il échoue :
  le garde-fou devient alors un enregistreur.

### Deux causes pour une eval au rouge

Symptôme unique — le score est passé sous la référence — et deux origines qui
n'appellent pas la même réaction :

- **le code a régressé**, ce que le test existe pour attraper ;
- **l'environnement a bougé** — modèle mis à jour, serveur d'inférence changé,
  corpus ré-indexé. Aucun de ces trois n'est capturé par l'état du dépôt, et
  c'est le même angle mort que [le tag git](sortie-precoce-semver.md).

Ce qui les sépare : rejouer la référence sur le code **d'avant**. Si l'ancien
code ne reproduit plus son ancien score, la cause est extérieure. Sans cette
contre-épreuve, on corrige un code qui n'avait rien.

### Le layout `src/` est un test, pas une convention de rangement

Ranger le code sous un dossier dédié plutôt qu'à la racine a un effet mécanique
et un seul : le répertoire courant n'est plus sur le chemin d'import. Les
`import framework...` ne peuvent donc plus résoudre par accident depuis
l'arborescence des sources — ils ne résolvent que si le paquet est **réellement
déclaré et installé**.

C'est ce qui attrape la panne classique : un module oublié dans la déclaration
du paquet, qui fonctionne chez son auteur et manque à l'installation. Sans
`src/`, cette faute est invisible jusqu'au premier consommateur extérieur.

Le corollaire est important ici : mettre le dossier des sources sur le chemin
d'import par configuration — ce que fait `pythonpath` pour les tests — rend
l'exécution commode et **désactive exactement la propriété qu'on vient de
décrire**. Les deux réglages coexistent sans conflit apparent, et seul un test
lancé depuis une installation réelle constate la différence.

## Quand c'est la bonne réponse

**Écrire les trois étages** quand la brique a un consommateur extérieur. C'est
lui qui rend l'installabilité et la non-régression observables.

**Se contenter des unitaires** tant que la brique n'a que ses propres tests.
L'étage intégration teste un branchement ; sans deuxième pièce à brancher, il
teste l'appel d'une fonction par elle-même.

**Ne pas écrire d'eval** avant d'avoir un jeu de cas dont on sait dire ce qu'une
bonne réponse serait. Un seuil posé sur un jeu bricolé mesure le bricolage, et
il faudra le croire.

## Ce qu'on ne saura pas faire

Le dispositif décrit ici n'existe qu'au premier étage. `wiki/tests/` contient
deux fichiers, tous deux unitaires, sur les deux seules briques montées. Il n'y
a **ni étage d'intégration, ni eval en test, ni marqueur** déclaré dans
[`pyproject.toml`](../../../pyproject.toml) — donc rien à séparer pour
l'instant, ce qui est cohérent, mais rien de ce qui précède n'a été éprouvé.

Le point le plus net est celui du packaging : le paquet déclare bien un layout
`src/`, mais les tests l'atteignent par `pythonpath` plutôt que par une
installation. La propriété d'honnêteté du layout n'est donc **pas exercée
aujourd'hui** — une déclaration de paquet incomplète passerait sans être vue.
Le constat ne se fera qu'au premier `pip install -e .` suivi d'une exécution
des tests depuis un clone neuf.

Ce qui promouvrait cette leçon en leçon « refaire » : un premier consommateur
extérieur, l'étage d'intégration qu'il rend possible, et une référence d'eval
enregistrée **avec** son contexte matériel — le jour où
[les evals du RAG](../retrieval/evals.md) auront tourné.

## Se tester

1. Un test de la suite rapide échoue une fois sur dix. Quel est son coût réel,
   et pourquoi n'est-il pas proportionnel à sa fréquence d'échec ?
   *Réussi si* la réponse porte sur la confiance dans la suite entière — au
   bout de quelques faux rouges, plus personne ne lit les rouges — et pas sur
   le temps perdu à relancer.
2. On vous propose de simuler la brique de retrieval pour tester le RAG de bout
   en bout. Quelle objection, et où poseriez-vous la simulation ?
   *Réussi si* la réponse note que le non-déterminisme resterait à l'intérieur
   du périmètre testé, et replace la simulation à la frontière du provider —
   le seul point qui remplace la source d'aléa sans emporter de logique.
3. Une eval passe au rouge après un commit qui ne touche pas au retrieval.
   Qu'est-ce que vous faites avant de chercher dans le code ?
   *Réussi si* la réponse rejoue la référence sur le code d'avant, pour séparer
   une régression d'une dérive de l'environnement — modèle, serveur ou corpus.

## À retenir

- Le découpage des tests se fait par nature du verdict, pas par vitesse : un
  échec unitaire dit « le code est faux », un échec d'eval dit « quelque chose
  a bougé ».
- Le non-déterminisme entre par un point unique ; la simulation se pose là, ni
  plus haut où elle laisse l'aléa dedans, ni plus bas où elle singe un protocole.
- Un test instable coûte la confiance dans toute la suite, pas le temps de le
  relancer.
- Un seuil d'eval sans son contexte matériel mesure la dérive de
  l'environnement autant que celle du code.
- Le layout `src/` est un test d'installabilité — et le mettre sur le chemin
  d'import par configuration désactive ce test sans rien signaler.

## Références

- Doc pytest, les marqueurs — le mécanisme qui sépare les étages à l'exécution
- Doc packaging Python, layouts `src/` et plat — en lisant ce que le premier
  empêche, plutôt que ce qu'il range
- [Clean code](clean-code.md) — les pratiques que ce dispositif constate
