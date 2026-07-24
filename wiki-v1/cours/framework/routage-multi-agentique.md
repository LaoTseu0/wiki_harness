# Routage multi-agentique

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [les providers](providers.md) — plusieurs backends
  disponibles, sans quoi il n'y a rien à arbitrer, et surtout la distinction
  entre un choix de **configuration** (une fois au démarrage) et un choix **par
  requête**, qui est le sujet ici ; [la boucle d'agent](../fondamentaux/boucle-agent.md)
  — ce qu'est une session, son contexte et sa borne. Une propriété du
  [function calling](../fondamentaux/function-calling.md) ressert plus bas : un
  contexte chargé dilue les consignes et dégrade le choix, bien avant de
  saturer la fenêtre.
- **Débloque** : l'arbitrage coût/latence/qualité une fois plusieurs backends
  réels en place ; [l'observabilité](../production/observabilite.md), sans
  laquelle une décision de routage ne se défend pas.

## L'essentiel

Deux sujets voisins vivent ici, et les confondre est l'erreur ordinaire :
**router** — envoyer chaque requête au bon modèle selon le coût, la latence, la
qualité attendue et la sensibilité des données — et **orchestrer** — décomposer
une tâche entre plusieurs sessions.

La thèse : le routage mono-agent capte l'essentiel du gain pour une fraction de
la complexité, et la vraie justification du multi-agents n'est presque jamais le
parallélisme — c'est **l'isolation de contexte**. Tant qu'une seule session avec
un bon contexte suffit, l'orchestration n'ajoute que de la surface d'erreur.

Cette leçon ne couvre pas le choix d'un backend par configuration, qui est
[providers](providers.md), ni la mesure de ce que le routage rapporte, qui
demande [l'observabilité](../production/observabilite.md).

## Le savoir

### Router n'est pas configurer

La différence est de fréquence, et elle décide de l'endroit du code. Un
provider se choisit **une fois au démarrage** ; une route se choisit **à chaque
requête**, sur des critères qui dépendent de la requête elle-même.

Le signe qu'on s'est trompé de couche : une configuration qu'il faudrait
changer en cours d'exécution. Si l'on se surprend à vouloir « recharger la
config » selon le type de question, c'est du routage qu'on voulait.

Les critères d'entrée sont peu nombreux et tous observables avant l'appel :
complexité estimée de la tâche, taille de contexte nécessaire, sensibilité des
données — qui peut rendre un backend distant **interdit**, pas seulement cher —
et budget de latence acceptable.

### Trois politiques, et ce que chacune suppose

- **Par règles.** Une table de décision explicite sur le type de tâche ou la
  taille. Lisible, traçable, gratuite. Elle suppose qu'on sache classer une
  requête sans la traiter — ce qui est vrai plus souvent qu'on ne le croit.
- **Par classifieur.** Un petit modèle décide de la route. Elle suppose que
  classer soit franchement moins coûteux que traiter, sinon on paie deux fois.
- **Par escalade.** Essayer petit, recommencer avec plus gros en cas d'échec.
  C'est le meilleur rapport coût/qualité **sous une condition qui n'est presque
  jamais énoncée** : l'échec doit être détectable sans le gros modèle.

Cette condition mérite qu'on s'y arrête, parce qu'elle disqualifie l'escalade
dans beaucoup de cas où on la propose. Si savoir que la petite réponse est
mauvaise exige de demander au gros modèle, ou à un juge de sa taille, alors on
appelle le gros modèle à chaque requête **plus** le petit : l'escalade coûte
strictement plus cher que de ne pas router. Elle n'est rentable que quand
l'échec se constate mécaniquement — une extraction qui ne valide pas, un outil
qui refuse, un score déterministe sous un seuil.

### La politique de routage est un levier, avec sa portée

- **Où elle agit** : à l'entrée d'une requête, avant tout appel au modèle.
- **À quelle fréquence** : une fois par requête.
- **Ce qu'elle propage** : le coût, la latence, la qualité **et la
  confidentialité** de la réponse. Le dernier point est le seul irréversible :
  une donnée sortie du réseau local ne revient pas, et aucune correction de la
  table ne l'annule après coup.
- **Ce qui l'annule** : un trafic homogène. Si toutes les requêtes se
  ressemblent, il n'y a pas de variance à exploiter et la meilleure table est
  une constante. L'annule aussi une décision non tracée : sans le coût, la
  latence et la qualité enregistrés **par route**, on ne peut ni prouver que le
  routage rapporte, ni régler la table autrement qu'à l'intuition.

### Superviseur et ouvriers — et pourquoi c'est un autre niveau

L'orchestration n'est pas une quatrième politique de routage. C'est une pièce
d'un autre niveau : le routage choisit *qui traite une requête*, l'orchestration
**crée de nouvelles requêtes** qui n'existaient pas. Les ranger ensemble laisse
croire qu'on peut passer de l'un à l'autre par réglage.

Le schéma retenu : un superviseur décompose, des ouvriers traitent sans mémoire
partagée, le superviseur agrège. Deux niveaux, pas davantage, et un point
d'agrégation unique.

L'absence de mémoire partagée n'est pas de la prudence : c'est **la raison
d'être du découpage**. Chaque ouvrier reçoit un contexte minimal et ciblé, donc
ses consignes ne sont pas diluées par ce qui concerne les autres — la propriété
posée en prérequis. Une mémoire partagée reconstituerait exactement le contexte
encombré qu'on cherchait à éviter, en ajoutant l'orchestration par-dessus.

Le corollaire est le critère de décision : on découpe quand les sous-tâches ont
des **contextes disjoints**. Si elles ont besoin des mêmes informations, le
découpage coûte sans rien acheter.

### Deux causes pour « le routage n'apporte rien »

- **La table est mauvaise** — les critères ne prédisent pas la difficulté, et
  les requêtes complexes partent au petit modèle.
- **Le trafic est homogène** — il n'y a rien à séparer, et n'importe quelle
  table donne le même résultat que pas de table du tout.

Ce qui les sépare : regarder la **distribution des requêtes par route**. Si tout
part dans la même branche, c'est le trafic ; si la répartition est équilibrée
mais que la qualité ne suit pas, c'est la table. Sans traces par route, les deux
sont indiscernables — et c'est le cas le plus courant, parce que le traçage est
ce qu'on ajoute en dernier.

## Quand c'est la bonne réponse

**Router** dès que deux backends aux profils franchement différents existent et
que le trafic est hétérogène. C'est le gain le plus accessible du domaine.

**Orchestrer** quand une tâche se décompose en sous-tâches à contextes
disjoints, et que le résultat de chacune s'agrège mécaniquement. Les deux
conditions : sans la seconde, le superviseur doit interpréter, et il redevient
la session unique qu'on voulait éviter.

**Ne rien faire des deux** tant qu'une session bien construite suffit. Le
premier réflexe devant une tâche qui échoue n'est pas de la découper mais de
regarder ce qu'il y avait dans le contexte — l'orchestration ne répare pas un
mauvais prompt, elle le duplique.

## Ce qu'on ne saura pas faire

Rien n'existe : ni table de routage, ni superviseur, et un seul backend tourne
aujourd'hui. Le routage suppose [providers](providers.md), qui n'est pas écrit,
lui-même en attente d'un deuxième backend réel — la dépendance est donc longue,
et cette leçon est la plus éloignée de l'exécution de tout le domaine.

Ce que ça laisse ouvert, et qui ne se déduit pas : si un classifieur assez léger
pour être rentable est seulement disponible sur le matériel local ; quels
critères prédisent réellement la difficulté d'une question sur ce corpus ; et
si l'escalade trouvera des signaux d'échec mécaniques, ce qui conditionne toute
sa rentabilité.

Ce qui promouvrait cette leçon en leçon « refaire » : deux backends réels, un
jeu de requêtes hétérogène, et le coût comme la qualité mesurés **par route** —
sans quoi le gain du routage reste une affirmation.

## Se tester

1. On vous propose une escalade : petit modèle d'abord, gros modèle si la
   réponse est mauvaise. Quelle question posez-vous avant d'accepter ?
   *Réussi si* la réponse demande **comment l'échec est détecté**, et voit que
   si la détection exige le gros modèle, l'escalade coûte plus cher que
   l'absence de routage.
2. Une équipe veut découper une tâche en quatre agents « pour aller plus vite ».
   Quel critère appliquez-vous, et quelle est la vraie question ?
   *Réussi si* la réponse déplace le critère du parallélisme vers l'isolation
   de contexte, et demande si les sous-tâches ont des contextes disjoints.
3. Le routage est en place depuis un mois et personne ne sait dire s'il
   rapporte. Deux causes possibles pour ce constat : lesquelles, et que
   regardez-vous ?
   *Réussi si* la réponse distingue « table mauvaise » de « trafic homogène »,
   et va lire la distribution des requêtes par route — en notant qu'en
   l'absence de traces, aucune des deux ne peut être établie.

## À retenir

- Router se décide par requête, configurer se décide au démarrage : une config
  qu'on voudrait recharger en cours de route est un routage déguisé.
- L'escalade n'est rentable que si l'échec se détecte sans le gros modèle —
  sinon elle coûte plus que l'absence de routage.
- La confidentialité est le seul critère irréversible : une donnée partie ne
  revient pas.
- L'orchestration n'est pas une politique de routage : elle crée des requêtes
  au lieu de les aiguiller.
- L'absence de mémoire partagée entre ouvriers est la raison du découpage, pas
  une précaution — sinon on reconstitue le contexte encombré qu'on fuyait.
- Sans coût, latence et qualité tracés par route, « le routage rapporte » n'est
  pas une affirmation vérifiable.

## Références

- [router-multi-model.md](../../../../homelab/architecture/router-multi-model.md)
  du homelab — le raisonnement d'origine, à confronter à ce qui est écrit ici
- Les publications d'ingénierie sur les systèmes multi-agents — en cherchant
  surtout les cas où les auteurs disent avoir **renoncé** au découpage, plus
  instructifs que les réussites
