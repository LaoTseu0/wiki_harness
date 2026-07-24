# Sortie précoce et semver

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la promotion](promotion.md) — sans brique montée il n'y
  a rien à publier ; [le dogfooding](dogfooding.md) — sans consommateur,
  « ne pas casser » ne désigne rien. Une notion s'ajoute et se pose ici :
  la **surface publique** d'une bibliothèque est l'ensemble de ce que ses
  consommateurs importent et appellent. Elle ressert partout plus bas — c'est
  elle, et non le nombre de lignes changées, qui décide d'un numéro de version.
- **Débloque** : la comparaison de deux états du framework par les
  [evals](../retrieval/evals.md) ; le droit de refactorer l'intérieur d'une
  brique sans prévenir personne.

## L'essentiel

Pas de grand lancement final : le framework porte un numéro **dès les premières
briques promues**, puis avance par incréments. Publier tôt force à répondre à
une question qu'on peut sinon repousser indéfiniment — *qu'est-ce qui est
public ?* — et cette réponse est ce qui rend un refactoring sûr.

La thèse contestable de la leçon n'est pas « versionnez », mais ceci : **un
numéro de version ne certifie rien tout seul**. Il ne devient une information
que si l'on a d'abord défini la surface publique, et il ne rend deux mesures
comparables que si les grandeurs qu'il ne capture pas — le modèle, le corpus —
sont fixées par ailleurs. Un tag git est bien moins qu'un état reproductible.

Cette leçon ne couvre pas ce qui autorise une brique à monter — c'est
[la promotion](promotion.md) — ni comment on la teste, qui est
[tests, typing, packaging](tests-typing-packaging.md).

## Le savoir

### Les trois chiffres, et ce que le pré-1.0 en retire

MAJEUR.MINEUR.PATCH : incompatibilité, ajout compatible, correction. La règle
de décision est mécanique une fois la surface publique définie — *un
consommateur existant doit-il changer son code ?* Si oui, c'est le premier
chiffre, quelle que soit la taille du changement. Une correction d'une ligne qui
renomme un champ rendu est une incompatibilité ; une réécriture complète qui ne
change aucune signature ne l'est pas.

En pré-1.0, la spécification elle-même autorise à tout casser à chaque
incrément : `0.y.z` ne promet rien. C'est la nuance que la plupart des lecteurs
manquent, et elle a une conséquence pratique — **la garantie qu'on donne en
0.0.x est conventionnelle, pas normative**. Elle ne vaut donc que si elle est
écrite quelque part et tenue ; sinon, un consommateur qui épingle `0.0.3` n'a
aucun recours, et il a raison de ne pas nous faire confiance.

La convention retenue ici : `0.0.x` pour les briques qui arrivent, `0.x.0` pour
un jalon d'ensemble, et une cassure s'accompagne au minimum d'une note de
migration — la clause qui rend le pré-1.0 vivable.

### Ce qui est public, et pourquoi ça se décide avant

Tant que « public » n'est pas défini, chaque changement est potentiellement
cassant, donc on n'ose plus rien changer : c'est la paralysie qu'une version
est censée lever, et elle vient de l'absence de frontière, pas du versionnage.

La frontière a besoin d'un **support matériel**, pas d'une intention. Trois
formes s'additionnent : ce qu'un `__init__.py` réexporte, ce qui est nommé sans
préfixe de privé, et ce que les tests des consommateurs touchent. La troisième
est la plus honnête, parce qu'elle est la seule qui constate au lieu de
déclarer — et c'est aussi celle qui trahit qu'un attribut « interne » est
devenu public sans qu'on l'ait décidé.

### Le tag est un levier, avec sa portée

- **Où il agit** : sur un commit, qu'il rend citable et retrouvable.
- **À quelle fréquence** : une fois par publication.
- **Ce qu'il propage** : un consommateur peut épingler ; deux états du code
  deviennent comparables ; un `diff` entre deux tags devient l'explication d'un
  changement de comportement.
- **Ce qui l'annule** : un numéro non répercuté dans `pyproject.toml` — la
  version installée ment alors sur ce qu'elle contient, et c'est pire que pas
  de version du tout, parce qu'on lui fait confiance. Un tag déplacé produit le
  même effet en pire, l'ancien état devenant irretrouvable.

### Deux causes pour « le score a bougé entre deux versions »

C'est le piège de raisonnement le plus coûteux de cette leçon, parce qu'il se
déguise en rigueur. Un tag fixe **le code, et rien d'autre**. Un score d'evals
qui change entre deux tags a donc au moins deux origines :

- **le framework a changé** — c'est ce qu'on cherchait à mesurer, et le `diff`
  entre les tags l'explique ;
- **quelque chose hors du dépôt a changé** — les poids du modèle, sa version
  quantifiée, la version du serveur d'inférence, le corpus indexé. Aucun de ces
  quatre n'est capturé par un tag git.

Ce qui les distingue : rejouer l'ancien tag **maintenant**. Si le score ancien
ne se reproduit plus, la cause est extérieure au dépôt. Sans cette
contre-épreuve, « le score a bougé entre 0.0.3 et 0.0.4 » est une corrélation
qu'on présente comme un `diff`.

La conclusion à en tirer n'est pas de renoncer aux tags, mais de **consigner
avec chaque mesure ce que le tag ne fixe pas** : le modèle exact, le matériel,
l'état du corpus. C'est précisément ce que la rubrique `Mesures` de chaque leçon
demande, et la raison pour laquelle elle le demande.

### Le déclencheur, défini d'avance

Le déclencheur d'une publication se fixe **avant** d'y être, sinon il devient
« encore une brique » indéfiniment. Sa fonction n'est pas de garantir la
qualité mais de couper court à l'arbitrage : le jour venu, il n'y a rien à
décider.

Ce qui accompagne la publication tient en quatre gestes — tests verts, numéro
incrémenté dans `pyproject.toml`, note de changement en trois lignes, tag
annoté. La note se juge à un seul critère : elle sert à retrouver *quand* un
comportement a changé, pas à raconter le travail. Trois lignes factuelles y
suffisent, une page ne le fait pas mieux.

L'ensemble doit être assez court pour se faire sans y penser. Une procédure de
publication qui demande de s'organiser ne sera pas suivie, et un rythme de
publication non tenu vaut moins qu'une absence de versionnage — il donne des
numéros qui ne correspondent à rien.

## Quand c'est la bonne réponse

**Publier tôt** quand au moins un consommateur réel existe hors du framework.
La version sert à le protéger ; sans lui, elle ne protège personne.

**Attendre** tant que la surface publique n'est pas décidable. Poser un numéro
sur un ensemble dont on ne sait pas dire ce qui est public produit une promesse
qu'on cassera sans le savoir — et la crédibilité perdue ne se rattrape pas par
un incrément.

**Ne pas versionner du tout** ce qui n'a qu'un consommateur situé dans le même
dépôt et modifié dans le même commit. Là, le versionnage est une cérémonie :
l'appelant et l'appelé bougent ensemble, donc rien ne peut casser entre eux.
C'est la situation actuelle, et c'est pourquoi la suite est une intention.

## Ce qu'on ne saura pas faire

`pyproject.toml` déclare `0.0.1`, et **aucun tag git n'existe**. Rien de ce qui
précède n'a donc été éprouvé : pas de publication, pas de note de changement,
pas de deuxième tag à comparer au premier. La cohérence entre le numéro déclaré
et un état publié n'a jamais eu à être tenue.

Ce que ça laisse ouvert : on ne sait pas où passe la surface publique de
`llm/ollama.py` — `Reponse` en fait partie, mais `morceaux_ndjson`, importé par
les tests, est-il un détail d'implémentation ou un outil rendu ? La question ne
se tranchera qu'avec un consommateur extérieur, ce qui est exactement la
dépendance au [dogfooding](dogfooding.md).

Ce qui promouvrait cette leçon en leçon « refaire » : deux tags réels, et les
mêmes evals rejouées sur chacun **plus** une reprise de l'ancien tag pour
séparer ce qui vient du code de ce qui vient du reste.

## Se tester

1. Vous renommez un champ rendu par une brique, en une ligne, avec un test qui
   passe. Quel chiffre bougez-vous, et pourquoi la taille du changement
   n'intervient-elle pas ?
   *Réussi si* la réponse dit le chiffre majeur et rattache la décision à la
   seule question qui compte — un consommateur doit-il modifier son code ?
2. Les evals rendent un score différent entre deux tags. Un collègue conclut que
   le changement de code a dégradé le retrieval. Quelle contre-épreuve exigez-vous ?
   *Réussi si* la réponse demande de rejouer l'ancien tag maintenant, et nomme
   au moins deux grandeurs qu'un tag ne fixe pas — poids du modèle, version du
   serveur, corpus.
3. Un consommateur épingle `0.0.3` et vous reprochez d'avoir cassé son code en
   `0.0.4`. La spécification semver vous donne raison. Est-ce une bonne réponse ?
   *Réussi si* la réponse distingue ce que la spécification permet de ce que la
   convention interne promet, et note qu'une garantie non écrite ne vaut rien
   pour celui qui en dépend.

## À retenir

- Le chiffre majeur se décide sur une seule question — un consommateur
  doit-il changer son code — jamais sur la taille du changement.
- En pré-1.0, la spécification ne promet rien : la garantie qu'on donne est
  conventionnelle, donc elle doit être écrite pour valoir.
- Une version n'a de sens qu'après avoir défini la surface publique, et ce que
  les tests des consommateurs touchent la constate mieux qu'aucune déclaration.
- Un tag fixe le code et rien d'autre : ni les poids du modèle, ni le serveur,
  ni le corpus. Deux mesures entre deux tags ne sont pas comparables sans les
  avoir fixés par ailleurs.
- Un numéro non répercuté dans les métadonnées du paquet est pire que pas de
  numéro, parce qu'on lui fait confiance.

## Références

- semver.org — en lisant surtout la clause `0.y.z`, celle qui retire la
  garantie qu'on croit avoir
- *Keep a Changelog* — pour le format minimal, en gardant que la note sert à
  dater un changement de comportement, pas à raconter le travail
- [`pyproject.toml`](../../../pyproject.toml) — où le numéro doit être
  répercuté pour que la version installée ne mente pas
