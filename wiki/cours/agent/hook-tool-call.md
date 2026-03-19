# Hook tool_call

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la mini-boucle d'agent](../fondamentaux/boucle-agent.md)
  — la validation humaine faite à la main sur *un seul* outil, et sa limite : les
  autres outils s'exécutent sans elle. C'est cette limite que le hook lève.
  [Le function calling](../fondamentaux/function-calling.md) — les arguments
  produits par le modèle sont des entrées non fiables ; cette propriété ressert
  au moment de décider **sur les arguments résolus** et non sur la chaîne brute.
  [Le garde-fou d'ensemble](garde-fous.md) — le hook est le périmètre logiciel du
  couple.
- **Débloque** : [le conteneur](conteneur-moindre-privilege.md), la couche
  physique sous le hook ; [l'outil Home Assistant](outil-home-assistant.md),
  premier outil dont l'action passera par la décision `ask`.

## L'essentiel

Le hook `tool_call` est un **point d'interception unique** : chaque appel
d'outil de l'agent passe par notre code *avant* d'être exécuté. À l'échelle du
[processus d'une tâche à un résultat](../_processus/boucle-outils.md), il rend
l'étape `execution` **conditionnelle** — la fonction ne tourne que si le hook
l'autorise.

La thèse : déplacer le contrôle *des outils vers la boucle* est ce qui
industrialise la validation humaine de la [mini-boucle](../fondamentaux/boucle-agent.md).
Là où la mini-boucle mettait une garde dans un outil — et l'oubliait dans les
trois autres —, le hook met une politique unique, indépendante des outils, qui
couvre aussi ceux qu'on ajoutera demain.

Cette leçon ne borne pas ce que le processus *peut* faire si un appel échappe au
hook — ça, c'est le [conteneur](conteneur-moindre-privilege.md).

## Le savoir

### Un point unique, pas une garde par outil

Le harnais (Pi) expose un point d'extension appelé à chaque `tool_call` avec le
couple `(outil, arguments)` ; le hook rend une décision — **allow / deny /
ask** — et la boucle n'exécute que sur `allow` (ou sur un `ask` confirmé).

Pourquoi un point unique bat une garde par outil : une garde logée *dans* un
outil ne protège que cet outil. Le jour où l'on ajoute un `supprimer_fichier`,
il arrive sans garde tant qu'on n'a pas pensé à la recopier — et c'est
exactement le moment où on oublie. Le point unique couvre tout appel, y compris
ceux qui n'existaient pas quand la politique a été écrite. La garde ne se
duplique plus, elle se déclare une fois.

### La décision porte sur les arguments résolus

Un hook qui déciderait sur la **chaîne de commande brute** serait contournable
trivialement : `rm$IFS-rf` échappe à un filtre qui cherche `rm -rf`, un alias
masque la commande réelle, un chemin relatif ne dit pas où il atterrit. La
décision se prend donc sur les **arguments résolus** — le chemin absolu
canonique, obtenu comme la garde `chemin_securise()` de la mini-boucle le
faisait : normaliser *avant* de comparer.

C'est un cas de deux causes pour un même symptôme. À l'écran, deux commandes
bloquées se ressemblent ; l'une était franchement destructrice, l'autre une
forme obfusquée de la même chose. Résoudre les arguments efface la différence de
surface et ramène les deux à la même décision — ce qu'un regex sur la chaîne ne
fait jamais.

### Liste noire pour l'évidence, default-ask pour l'inconnu

Une liste noire est **toujours incomplète** : on ne peut pas énumérer toutes les
formes dangereuses. La politique ne s'appuie donc pas sur elle seule ; elle pose
le **défaut sur `ask`** pour tout ce qui n'est pas explicitement sûr.

- **deny** (liste noire) : `rm -rf`, écritures hors périmètre, réseau sortant non
  prévu, tout accès aux partages famille — refus **motivé et loggé**.
- **ask** (human-in-the-loop) : toute commande shell non listée, toute écriture —
  l'humain voit la commande *exacte* et tranche.
- **allow** : lectures dans le périmètre — le flux nominal reste fluide.

Le déséquilibre est voulu : ce qu'on énumère, c'est l'interdit évident ; le
reste tombe sur `ask` par construction, jamais sur `allow`.

### Le hook logge, et ne fait que décider

Chaque décision est journalisée — `allow` compris — ce qui fait du hook un point
d'[observabilité](../production/observabilite.md) autant qu'un garde-fou : le log
répond à « qu'a demandé l'agent, et qu'a-t-on autorisé ? ». Et le hook ne
contient **aucune logique métier** : il décide, il n'agit pas. La raison est une
règle de sécurité générale — du code métier dans le point de contrôle, c'est du
code où un bug devient une faille, à l'endroit précis où un bug ne doit pas
exister.

### La politique de hook, avec sa portée

- **Où elle agit** : à l'étape `execution` du
  [processus](../_processus/boucle-outils.md), entre le `dispatch` (le nom est
  résolu en fonction) et l'exécution réelle.
- **À quelle fréquence** : une fois par appel d'outil.
- **Ce qu'elle propage** : sur `deny`, l'exécution n'a pas lieu et la **raison du
  refus** entre dans l'historique comme résultat d'outil ; sur `ask`, l'exécution
  est suspendue jusqu'à l'humain ; sur `allow`, rien ne change au flux.
- **Ce qui l'annule** : un chemin d'action qui ne passe pas par un appel d'outil
  hooké — le hook ne voit que ce qui traverse le point d'extension, d'où la
  nécessité du [conteneur](conteneur-moindre-privilege.md) en dessous. L'annule
  aussi, côté confort, un `allow` large sur les lectures sûres : sur le flux
  nominal, le hook ne fait plus rien de visible, et c'est le but.

### Pourquoi un hook, pas « un bon prompt »

Le prompt est une **demande** ; le hook est une **contrainte**. Un agent
prompt-injecté par un document qu'il lit
([injection indirecte](../mcp/prompt-injection-indirecte.md)) ignore les
demandes du prompt système — mais il ne peut pas ignorer l'interception, parce
qu'elle n'est pas dans le texte qu'il génère, elle est dans le code qui exécute
ce texte. C'est toute la différence entre écrire « ne supprime rien » et rendre
la suppression impossible.

## Quand c'est la bonne réponse

Dès que les outils peuvent **écrire ou agir**. Un point d'interception unique,
en amont de l'exécution, est la forme tenable du contrôle — celle qui n'oublie
aucun outil et qu'on règle en un seul endroit.

À une condition de réglage, sans quoi le hook se retourne contre lui-même : la
décision `ask` doit rester **rare**. Un humain qui valide quarante fois par
session finit par valider sans lire, et le garde-fou devient un tampon
automatique. On rend donc l'`ask` rare en autorisant largement les lectures
sûres, et on le réserve aux écritures et aux commandes inconnues. C'est ce
réglage qui garde à la validation son sens.

Ce n'est jamais suffisant seul : un appel que le hook ne voit pas lui échappe.
On garde toujours [le conteneur](conteneur-moindre-privilege.md) sous lui, pour
que ce qui échappe au hook n'aille nulle part.

## Ce qu'on ne saura pas faire

Sans exécution, on n'a ni la fréquence réelle des `ask`, ni un `deny` observé
dans un log — seulement la politique qui les produirait. On ne connaît pas non
plus, chiffré, le coût de la fatigue de validation : c'est le genre de seuil qui
se constate en usage, pas en théorie.

Un piège reste à vérifier en situation : le **hook silencieux**. Un `deny` sans
explication renvoyée au modèle le laisse réessayer des variantes en boucle —
d'où la règle, héritée de la mini-boucle et généralisée : un refus se **rend au
modèle** avec sa raison, jamais avalé en silence.

Ce qui promouvrait cette leçon en « refaire » : une étape sous
`wiki/etapes/agent/` — politique à trois niveaux, motifs de liste noire dans une
config versionnée, un log JSON par décision — et un test : demander à l'agent de
supprimer un fichier protégé, vérifier le `deny` **et** le log.

## Se tester

1. On vous propose de filtrer les commandes destructrices par un regex sur la
   chaîne de commande. Donnez deux entrées qui passent quand même.
   *Réussi si* la réponse cite au moins deux formes parmi `rm$IFS-rf`, un alias,
   un chemin relatif, et conclut qu'il faut décider sur les arguments résolus en
   gardant un default-ask pour l'inconnu.
2. Un document que l'agent lit contient « supprime tel fichier », et il obéit,
   alors que le prompt système l'interdisait. Pourquoi le hook tient-il là où le
   prompt a cédé ?
   *Réussi si* la réponse oppose la demande (dans le texte généré, donc
   ignorable) à la contrainte (dans le code qui exécute, donc non contournable
   par du texte injecté).
3. L'humain valide quarante fois par session et finit par tout accepter sans
   lire. Quel réglage de la politique corrige ça, et lequel serait pire ?
   *Réussi si* la réponse élargit l'`allow` sur les lectures sûres pour rendre
   l'`ask` rare, et note qu'élargir l'`allow` sur les **écritures** serait pire :
   ça retire la garde là où elle compte.

## À retenir

- Le hook déplace le contrôle des outils vers la boucle : une politique unique
  qui couvre tout appel, y compris les outils pas encore écrits.
- La décision se prend sur les arguments résolus, jamais sur la chaîne brute :
  normaliser avant de comparer efface les formes obfusquées.
- Liste noire pour l'évidence, `ask` par défaut pour l'inconnu — parce qu'une
  liste noire est toujours incomplète.
- Un hook est une contrainte, pas une demande : c'est ce qui tient face à une
  injection que le prompt système ne retient pas.
- Un `deny` sans raison rendue au modèle le fait boucler sur des variantes ; un
  refus se rend, il ne s'avale pas.

## Références

- [securite.md §5 du homelab](../../../../homelab/architecture/securite.md) — le
  non-négociable d'origine
- Documentation des extensions et hooks du harnais Pi — le point d'extension
  `tool_call` et sa signature `(outil, arguments)`
