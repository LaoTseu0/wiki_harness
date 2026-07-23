# LLM-as-judge

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [les evals](../retrieval/evals.md) — pourquoi un score
  déterministe plafonne ; [le structured output](../fondamentaux/structured-output.md)
  — la sortie du juge est un schéma contraint, pas du texte à relire ;
  [le sampling](../fondamentaux/sampling.md), et précisément qu'une sortie est
  **tirée** dans une distribution. Cette dernière propriété est celle qu'on
  oublie ici, et elle ressert immédiatement : un juge est un générateur, donc
  ses notes sont tirées elles aussi.
- **Débloque** : l'extension d'un jeu de cas au-delà de ce qu'un humain peut
  noter ; les evals comparatives, qui ont besoin d'un critère stable pour
  ranger plusieurs configurations.

## L'essentiel

Les scores déterministes plafonnent vite : « la réponse contient-elle les
mots attendus » rate toute bonne réponse reformulée. Un **modèle juge** note
avec la souplesse qui manque — au prix d'un renversement qu'il faut regarder en
face : *l'instrument de mesure est fait de la même matière que ce qu'il
mesure*.

La thèse de la leçon : un juge non calibré n'est pas un instrument imprécis,
c'est un **générateur d'opinions à grande échelle**, et sa faute dominante
n'est pas le bruit mais le **biais**. La distinction commande tout le reste :
le bruit se dilue en augmentant le nombre de questions, le biais non — il se
répète, identique, à chaque question, et une moyenne sur trente cas le rend
plus crédible sans le corriger.

Cette leçon ne couvre pas la construction du jeu de cas, qui est
[les evals](../retrieval/evals.md), ni le choix du backend qui fera tourner le
juge — c'est [providers](providers.md).

## Le savoir

### Le juge est un générateur, avec toutes les conséquences

Dire « le juge attribue 3 sur 4 » escamote la pièce. Ce qui se passe : le
score est un **token tiré** dans une distribution, au terme du même parcours
que n'importe quelle génération. Trois conséquences, toutes vérifiables :

- **la note n'est pas reproductible par défaut.** Rejouer la même évaluation
  peut donner une autre note. Une eval dont le juge tire à température non
  nulle mesure sa propre variance autant que le système jugé ;
- **la reproductibilité est une configuration**, pas une propriété : il faut la
  poser explicitement du côté du juge, et le dire quand on publie un score ;
- **la sortie contrainte ne rend pas la note juste**, seulement lisible. Forcer
  un schéma `{score, justification}` garantit qu'on obtiendra un entier dans le
  bon intervalle — y compris quand le juge n'a aucune raison de préférer cet
  entier-là.

### Bruit et biais ne se corrigent pas au même endroit

C'est la distinction que la moyenne masque, et elle décide de ce qu'on doit
faire.

Le **bruit** — la même réponse notée 3 puis 4 — est symétrique et se dilue :
plus de questions, ou plusieurs passages moyennés, le réduisent. Il coûte du
calcul, pas de la validité.

Le **biais** est une préférence systématique. Il ne se dilue pas, parce qu'il
va toujours dans le même sens. Quatre sont documentés dans la littérature, et
chacun a sa parade, qui n'est jamais « plus de questions » :

- **auto-préférence** — un modèle sur-note ses propres productions. Parade : un
  juge d'une autre famille que le générateur.
- **verbosité** — les réponses longues sont mieux notées à contenu égal.
  Parade : un axe de la grille qui porte explicitement sur la concision, ou une
  consigne qui neutralise la longueur.
- **position** — en comparaison de deux réponses, la première est favorisée.
  Parade : randomiser l'ordre, et vérifier que le verdict tient quand on
  l'inverse.
- **complaisance** — sur une échelle large, le bas ne sert jamais. Parade :
  une échelle courte dont chaque échelon est **ancré** par une description
  observable (« contredit la source »), pas par un adjectif.

Le point commun des quatre parades : elles se posent dans la grille et dans le
protocole, avant de mesurer. Aucune ne se rattrape après coup.

### La grille est le levier, avec sa portée

- **Où elle agit** : dans le prompt du juge, à chaque cas évalué.
- **À quelle fréquence** : une fois par question et par axe. Un juge qui note
  quatre axes fait quatre jugements, pas un — c'est ce qui rend le diagnostic
  possible.
- **Ce qu'elle propage** : tout. La grille est la définition opérationnelle de
  « bonne réponse » pour l'ensemble du projet ; ce qu'elle omet ne sera jamais
  mesuré, et deviendra donc invisible dans toutes les décisions qui suivent.
- **Ce qui l'annule** : une grille vague. Sur « note la qualité de 1 à 10 », le
  juge n'a rien à quoi se référer et retombe sur ses préférences apprises —
  c'est-à-dire exactement sur les quatre biais ci-dessus. Une échelle non
  ancrée annule la grille aussi sûrement qu'une grille absente, en donnant des
  chiffres.

### Par axe, et surtout pas moyennés trop tôt

Moyenner les axes en un score unique détruit la seule chose qui rendait le juge
utile : la localisation de la panne. Une fidélité aux sources parfaite avec une
complétude au plancher désigne un problème de **retrieval** — les passages
remontés ne contenaient pas la réponse. La même paire moyennée donne un score
moyen, indistinguable d'un système médiocre partout, et oriente vers la
mauvaise correction.

La moyenne se calcule à la fin, pour communiquer. Elle ne se stocke jamais à la
place des axes.

### La calibration, et ce qu'elle mesure vraiment

Noter à la main une dizaine de réponses, puis comparer au juge. Si les verdicts
divergent nettement, la correction porte sur **la grille**, pas sur le juge : un
désaccord signale presque toujours un critère que l'humain applique sans
l'avoir écrit.

C'est le renversement utile de l'exercice. La calibration ne sert pas d'abord à
valider le juge, elle sert à **expliciter le critère humain** — qui, tant qu'il
reste implicite, ne peut être ni transmis, ni contesté, ni tenu dans le temps.

### Capacité avant identité

La règle « juge ≠ générateur » est une parade contre un seul biais, et elle
passe après une condition plus élémentaire : le juge doit être **capable** de
la tâche de jugement, qui est souvent plus difficile que la tâche jugée.

L'ordre des priorités est donc : capacité d'abord, altérité ensuite. Un petit
juge d'une autre famille respecte la lettre de la règle et note mal. Si un seul
modèle assez fort est disponible, un auto-jugement à grille serrée, annoncé
comme tel et calibré plus lourdement, vaut mieux qu'un juge faible — à condition
de le dire, puisque le biais d'auto-préférence est alors présent et connu.

### Deux causes pour une note basse

- **La réponse est mauvaise** — ce que l'eval cherche.
- **La grille demande la mauvaise chose** — typiquement une ressemblance de
  surface à la réponse attendue, quand une reformulation correcte devait passer.

Ce qui les sépare : lire la **justification**, qui est précisément ce pour quoi
on l'a exigée dans le schéma de sortie. Un juge qui écrit « la réponse ne
reprend pas les termes attendus » vient de dénoncer la grille, pas la réponse.
Sans ce champ, les deux causes sont indiscernables et on corrige au hasard.

## Quand c'est la bonne réponse

**Employer un juge** quand le critère de réussite est sémantique et que le jeu
de cas dépasse ce qu'on notera à la main à chaque itération. C'est le passage à
l'échelle qui le justifie : noter quelques dizaines de cas sur plusieurs
configurations n'est pas tenable manuellement.

**Ne pas en employer** quand un score déterministe suffit. Vérifier qu'une
source citée figure bien dans les passages remontés est une comparaison exacte :
y mettre un modèle ajoute du coût, de la variance et des biais pour remplacer
une égalité.

**Ne pas en employer non plus** avant d'avoir noté des cas à la main. Sans
échantillon de référence, on n'a aucun moyen de savoir si le juge mesure ce
qu'on croit — et un juge non calibré produira des chiffres cohérents entre eux,
donc convaincants, quelle que soit sa justesse.

## Ce qu'on ne saura pas faire

Aucun juge n'existe dans ce dépôt, et
[les evals du RAG](../retrieval/evals.md) n'ont pas tourné : tout ce qui
précède est un protocole, pas un résultat. Les quatre biais énumérés viennent de
la littérature citée en références — ils n'ont **pas** été observés ici, et la
leçon ne prétend pas le contraire.

Ce que ça laisse ouvert, et qui ne se déduit pas : de combien le juge divergera
d'une notation humaine sur ce corpus, quelle échelle sera assez ancrée pour ce
type de questions, et si un modèle exécutable sur le matériel local est
seulement capable de la tâche de jugement. Cette dernière question est la plus
sérieuse, parce qu'une réponse négative invalide l'approche entière ici.

Ce qui promouvrait cette leçon en leçon « refaire » : une grille écrite, un
échantillon noté à la main, et la comparaison des deux — avec l'écart, le
modèle juge et le matériel.

## Se tester

1. Vous augmentez le jeu de douze à trente questions pour « fiabiliser » les
   notes du juge. Qu'est-ce que ça corrige, qu'est-ce que ça ne corrige pas ?
   *Réussi si* la réponse distingue le bruit, qui se dilue, du biais, qui se
   répète — et note qu'une moyenne sur trente cas rend un biais plus crédible
   sans le réduire.
2. Le juge note 2 sur 4 une réponse que vous jugez correcte. Deux causes :
   lesquelles, et quel champ de sa sortie consultez-vous ?
   *Réussi si* la réponse oppose « la réponse est mauvaise » à « la grille
   demande une ressemblance de surface », et va lire la justification — pas
   seulement le score.
3. Deux exécutions de la même eval donnent deux scores. Bug ?
   *Réussi si* la réponse rattache l'écart au tirage — le juge est un
   générateur — et traite la reproductibilité comme une configuration à poser
   et à publier, pas comme une propriété acquise.

## À retenir

- Le juge est un générateur : ses notes sont tirées, donc non reproductibles
  tant qu'on ne l'a pas configuré pour, et la sortie contrainte rend la note
  lisible, jamais juste.
- Le bruit se dilue avec le nombre de cas, le biais non : les quatre biais
  connus se parent dans la grille et le protocole, avant de mesurer.
- Une échelle non ancrée annule la grille en donnant des chiffres.
- Les axes ne se moyennent pas avant d'avoir servi au diagnostic : fidélité
  haute et complétude basse désignent le retrieval.
- La calibration sert d'abord à expliciter le critère humain ; un désaccord
  corrige la grille, pas le juge.
- Capacité du juge avant altérité — un juge faible d'une autre famille respecte
  la règle et note mal.

## Références

- Zheng et al., « Judging LLM-as-a-Judge » (MT-Bench) — l'origine des biais
  énumérés ici, et leur mesure ; à lire pour savoir ce qui est établi et ce qui
  ne l'est pas
- [Les evals](../retrieval/evals.md) — le jeu de cas que le juge vient noter,
  et les scores déterministes qu'il complète sans les remplacer
