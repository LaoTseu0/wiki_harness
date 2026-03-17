# Clean code production-grade

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la promotion](promotion.md) — le moment où ces
  pratiques s'appliquent, qui n'est ni pendant l'étape ni à la fin du parcours.
  Une notion se pose ici parce que tout repose dessus : en Python, une
  **annotation de type n'est pas vérifiée à l'exécution**. `x: int` n'empêche
  rien ; c'est une déclaration lue par des outils extérieurs, et par personne
  d'autre si aucun outil ne tourne. Cette propriété ressert deux fois plus bas.
- **Débloque** : [tests, typing et packaging](tests-typing-packaging.md), qui
  prend le versant vérification — ce qu'une brique doit *tenir* pour monter.
  Les deux leçons sont voisines et ne se recouvrent pas : ici les pratiques et
  ce que chacune détecte, là le dispositif qui les constate.

## L'essentiel

« Production-grade » a un sens précis et vérifiable : du code **qu'on peut
modifier sans se souvenir de pourquoi il est comme ça**. Ce n'est pas un
adjectif de qualité, c'est une propriété qui se teste — six mois plus tard, sur
soi-même.

La thèse de la leçon : chacune des pratiques ci-dessous est un **détecteur**
avec une sensibilité étroite et connue. Aucune n'améliore le code en général.
Les empiler « pour faire propre » sans savoir ce que chacune attrape produit du
cérémonial coûteux — et la conviction fausse d'être couvert.

Cette leçon ne couvre pas comment on constate que ces pratiques sont tenues —
c'est [tests, typing et packaging](tests-typing-packaging.md) — ni quand une
brique a le droit de monter, qui est [la promotion](promotion.md).

## Le savoir

### Le typage attrape les incohérences, jamais les erreurs de sens

Puisque l'annotation n'est pas vérifiée à l'exécution, elle ne fait rien seule.
Ce qui travaille est le **vérificateur**, qui relit le code et compare les
déclarations aux usages.

Ce qu'il attrape : un appel qui passe une liste là où un dictionnaire est
déclaré, un retour `None` non traité, un champ qui n'existe plus après un
renommage. Autrement dit, toute la classe des erreurs qui viennent d'un
changement fait à un endroit et pas à l'autre — la plus fréquente lors d'un
refactoring, et la plus pénible à trouver parce que le symptôme est loin de la
cause.

Ce qu'il n'attrape pas, et qu'aucune annotation ne pourra exprimer : qu'un `str`
attendu comme une URL reçoive un chemin de fichier. Les deux sont des `str`. La
question de savoir si la valeur est *la bonne* n'appartient pas au typage — elle
appartient à la validation, ci-dessous.

D'où la conséquence pratique, qui est la seule à retenir : **des annotations
jamais passées à un vérificateur mentent en silence**, et elles mentent d'autant
plus qu'on leur fait confiance. Annoter sans vérifier est strictement pire que
ne pas annoter, parce que le lecteur suivant les croira.

### La validation aux frontières déplace la panne vers sa cause

C'est le point que « valider les entrées » escamote. La valeur de la validation
n'est pas d'empêcher les données fausses d'exister — elles existeront de toute
façon. Elle est de **faire échouer le programme à l'endroit où la cause est
visible**.

Sans validation, une réponse de modèle à laquelle il manque un champ ne casse
pas à la réception : elle casse dix appels plus loin, dans une fonction qui n'y
est pour rien, avec un message qui accuse cette fonction. Le temps de débogage
n'est pas passé à corriger, il est passé à remonter. Avec une validation à la
frontière, l'échec nomme le champ manquant, au moment où il entre.

- **Où elle agit** : aux frontières — ce qui entre ou sort du framework :
  configuration, sortie de modèle, charge utile d'API. Pas à l'intérieur.
- **À quelle fréquence** : à chaque franchissement.
- **Ce qu'elle propage** : le droit, pour tout l'intérieur, de supposer les
  données conformes. C'est ce droit qu'on achète, et c'est ce qui permet aux
  structures internes de rester légères.
- **Ce qui l'annule** : valider aussi à l'intérieur — on paie deux fois et on
  perd la propriété, puisque plus aucune couche ne peut supposer. L'annule
  également une configuration qui accepte les champs inconnus là où il fallait
  les refuser : la validation passe, et la faute de frappe dans une clé de
  configuration devient silencieuse.

### La docstring est un contrat, et la pédagogie est ailleurs

Dans ce dépôt, la prose explicative vit dans le `.md` compagnon. La docstring
d'une brique n'a donc pas à enseigner : elle dit ce que la fonction garantit,
ce qu'elle suppose, et ce qu'elle fait des cas limites.

La raison est mécanique, pas stylistique : **rien ne vérifie une docstring**.
Une docstring qui explique un mécanisme se périme dès que le mécanisme change,
sans qu'aucun test n'échoue — et une explication périmée est plus nuisible
qu'absente. Un contrat, lui, se périme aussi, mais il se périme *avec le test
qui le vérifie*, donc le test le rattrape.

Les étapes de `etapes/` suivent la règle inverse, et c'est cohérent : leur
docstring **est** la pédagogie, parce qu'une étape existe pour être lue.

### Deux causes pour « les types sont faux »

Symptôme identique — le vérificateur ne dit rien alors que le code est
manifestement incohérent — et corrections opposées.

- **Rien ne tourne.** Aucun vérificateur n'est configuré ; les annotations n'ont
  jamais été relues par un outil.
- **Il tourne trop mollement.** Un réglage par défaut ignore les fonctions non
  annotées, les modules sans types, les `Any` implicites — et un fichier
  entièrement faux passe sans un mot.

Ce qui les sépare, en une commande : lancer le vérificateur en mode strict sur
un seul fichier. S'il crie, c'est le réglage ; s'il se tait toujours, c'est
qu'il ne tourne pas sur ce fichier.

### Pourquoi ces gestes se paient à la promotion, et pas après

L'argument habituel — « la qualité en continu coûte moins cher » — est vrai mais
mou. Le mécanisme précis est plus contraignant : un grand nettoyage de fin de
parcours se fait **sans filet**, parce que ce qui manque à du code non nettoyé
est justement ce qui protégerait le nettoyage. On refactore sans tests, en
s'appuyant sur des annotations que rien n'a vérifiées.

C'est pourquoi le moment est fixé : à la promotion, brique par brique, sur du
code qu'on vient de comprendre. L'ordre y est stable — annoter, modéliser les
frontières, écrire les tests, déclarer le paquet, relire la docstring comme un
contrat — et il n'est pas arbitraire : chaque geste rend le suivant vérifiable.

## Quand c'est la bonne réponse

**Appliquer les cinq gestes** à ce qui monte dans `src/framework/`. C'est du
code qui sera rappelé par du code qui ne connaît pas la leçon : il n'a que son
contrat pour se défendre.

**Ne pas les appliquer** aux scripts de `etapes/`. Une étape est faite pour
être lue et modifiée en la regardant tourner ; y ajouter des couches de
validation masquerait le mécanisme qu'elle existe pour montrer. Les constantes
en haut du fichier et les `print` y sont des qualités.

**Se contenter du typage** quand la donnée ne franchit aucune frontière — un
calcul interne entre deux fonctions du même module n'a rien à valider, et
Pydantic y ajouterait un coût par appel pour une garantie déjà donnée par le
vérificateur.

## Ce qu'on ne saura pas faire

Aucun vérificateur de types n'est configuré dans
[`pyproject.toml`](../../../pyproject.toml) à ce jour : les annotations des deux
briques montées n'ont donc jamais été relues par un outil. Par la propriété
posée en prérequis, elles sont pour l'instant de la documentation — exactement
le cas « rien ne tourne » décrit plus haut, sur ce dépôt même.

Ce que ça laisse ouvert : on ne sait pas si les signatures de
[`llm/ollama.py`](../../src/framework/llm/ollama.py) et de
[`contexte.py`](../../src/framework/contexte.py) sont cohérentes, seulement
qu'elles sont écrites. Et on ne saura pas non plus, tant qu'un consommateur
extérieur n'existe pas, si les docstrings tiennent comme contrats — un contrat
ne se juge que depuis l'appelant.

Ce qui promouvrait cette leçon en leçon « refaire » : la configuration d'un
vérificateur, son premier passage sur les briques existantes, et la liste de ce
qu'il aura trouvé — qui est le seul moyen de savoir ce que ces pratiques
valaient ici.

## Se tester

1. Un module est entièrement annoté et le vérificateur ne signale rien, alors
   qu'un appel passe visiblement le mauvais type. Deux causes : lesquelles, et
   quelle commande tranche ?
   *Réussi si* la réponse oppose « il ne tourne pas sur ce fichier » à « son
   réglage est trop permissif », et propose un passage en mode strict sur un
   seul fichier.
2. On vous propose de valider avec Pydantic à l'entrée de chaque fonction
   interne, « pour être sûr ». Qu'est-ce que ça coûte, et qu'est-ce que ça fait
   perdre ?
   *Réussi si* la réponse nomme le coût par appel **et** la propriété perdue :
   plus aucune couche ne peut supposer ses données conformes, ce qui était
   exactement ce que la validation aux frontières achetait.
3. Une fonction rend un objet dont un champ vaut `None` quand le serveur n'a
   pas renvoyé les compteurs. Où cette information doit-elle être écrite, et
   pourquoi pas ailleurs ?
   *Réussi si* la réponse la place dans la docstring comme clause de contrat et
   dans un test, en notant qu'une explication en prose ne serait rattrapée par
   rien le jour où le comportement changera.

## À retenir

- Chaque pratique est un détecteur à sensibilité étroite ; les empiler sans
  savoir ce que chacune attrape produit du cérémonial.
- Une annotation n'est pas vérifiée à l'exécution : annoter sans vérificateur
  est pire que ne pas annoter, parce que le lecteur suivant y croira.
- Le typage attrape les incohérences entre déclaration et usage ; il ne dira
  jamais qu'un `str` est la mauvaise chaîne.
- La validation aux frontières ne supprime pas les données fausses, elle
  déplace la panne à l'endroit où la cause est visible.
- Valider aussi à l'intérieur annule la propriété achetée en payant deux fois.
- La docstring est un contrat parce que rien ne vérifie une explication — un
  contrat, lui, se périme avec son test.

## Références

- mypy et pyright — deux vérificateurs, et surtout leurs réglages par défaut,
  qui sont ce qui décide de ce qu'ils voient
- Pydantic v2 — les modèles, et le réglage du traitement des champs inconnus,
  qui est le point où la validation se rend inoffensive sans prévenir
- [Tests, typing, packaging](tests-typing-packaging.md) — le versant qui
  constate, quand celle-ci décrit
