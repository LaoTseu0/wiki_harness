# Service — exposer une brique en HTTP

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [le structured output](../fondamentaux/structured-output.md)
  — un contrat de données validé, ici appliqué aux deux bords d'une route ;
  [l'architecture modulaire](architecture-modulaire.md) — la frontière entre
  une brique et ce qui l'appelle. Une notion se pose ici parce que la moitié de
  la leçon en dépend : une application asynchrone tourne sur une **boucle
  d'événements à un seul fil d'exécution**, qui ne peut faire avancer une
  requête que pendant qu'une autre attend. Cette propriété ressert deux fois
  plus bas.
- **Débloque** : l'appel du RAG par [un serveur MCP](../mcp/serveur-mcp-python.md) ;
  [l'observabilité](../production/observabilite.md), qui a besoin d'un point de
  passage unique pour tracer ; et toute intégration par un tiers qui n'importera
  jamais notre code.

## L'essentiel

Une brique cesse d'être un script qu'on lance et devient un **point d'entrée
HTTP** : une question entre, une réponse et ses sources sortent. C'est le mode
d'intégration ordinaire — rien de ce qui consomme un système LLM ne veut
l'importer.

La thèse à retenir n'est pas « exposer en HTTP est facile », ce qui est vrai et
sans intérêt. C'est qu'exposer **change le modèle de panne** : ce qui était une
exception lue par la personne qui a lancé le script devient un code de statut
interprété par un appelant distant qui ne connaît ni le code, ni la leçon. Toute
la conception d'un service tient à rendre cette interprétation possible.

Cette leçon ne couvre pas ce qui se passe *dans* le moteur d'inférence sous
charge — c'est [la charge concurrente](../inference/charge-concurrente.md) — ni
l'authentification et les quotas, qui sont hors périmètre tant que le service ne
sort pas du réseau local.

## Le savoir

### La route est mince, et la raison n'est pas esthétique

Une route valide, appelle la bibliothèque, sérialise. Rien d'autre. La logique
reste dans la brique.

Deux conséquences mécaniques, et ce sont elles qui font la règle :

- **du code dans une route ne se teste qu'en levant un serveur.** Il quitte donc
  l'étage rapide des tests et rejoint l'étage d'intégration, où le verdict est
  moins net ([tests, typing, packaging](tests-typing-packaging.md)) ;
- **du code dans une route n'est pas promouvable.** Il est lié au transport, donc
  inaccessible à tout appelant qui n'est pas une requête HTTP — y compris à un
  autre morceau du framework.

Le test qui tranche : si la fonction appelée par la route ne se laisse pas
appeler depuis un test sans réseau, la frontière est au mauvais endroit.

### Le contrat aux deux bords, et ce qu'il achète

L'entrée et la sortie sont des modèles validés. À l'entrée, la validation
transforme une requête malformée en refus immédiat qui **nomme le champ fautif**
— au lieu d'une panne plus loin dans la brique, qui accuserait la brique. C'est
la propriété déjà vue aux frontières dans [clean code](clean-code.md), appliquée
au bord le plus exposé qui soit, puisque l'appelant est hors de notre contrôle.

À la sortie, le contrat sert quelqu'un d'autre : il fixe ce sur quoi un appelant
distant a le droit de compter. C'est là que les champs se choisissent avec soin
— rendre les sources permet de citer, rendre les métriques d'un appel permet de
tracer sans instrumenter le client.

Effet secondaire non négligeable : une documentation d'API se génère à partir de
ces modèles. Elle est gratuite **et** elle ne peut pas mentir, puisqu'elle est
dérivée du code qui valide.

### L'asynchrone est un levier, avec sa portée

- **Où il agit** : sur les attentes réseau — l'appel au modèle, l'appel à la
  base vectorielle. Nulle part ailleurs.
- **À quelle fréquence** : à chaque attente, dans chaque requête en vol.
- **Ce qu'il propage** : le droit de servir d'autres requêtes pendant qu'une
  attend. C'est du **débit**, pas de la latence — une requête seule n'ira pas
  plus vite d'un iota.
- **Ce qui l'annule** : un client HTTP synchrone appelé depuis une route
  asynchrone. Il ne rend pas la main à la boucle pendant son attente, donc, par
  la propriété posée en prérequis, il **gèle toutes les autres requêtes** — y
  compris celles qui n'ont rien à voir. Un calcul lourd en pur Python dans une
  route produit exactement le même effet, pour la même raison.

Le cas d'annulation mérite d'être retenu tel quel : c'est la panne la plus
contre-intuitive du domaine, parce que le code paraît asynchrone et se comporte
comme s'il ne l'était pas — sans erreur, sans avertissement.

### Deux causes pour « le service s'effondre sous la charge »

Symptôme apparent identique — les temps de réponse explosent quand les
requêtes se croisent — et deux origines qui ne se corrigent pas au même étage :

- **le moteur d'inférence est saturé.** Il traite les requêtes à son rythme et
  la file s'allonge. Le problème est en aval du service, et sa correction
  appartient à [l'inférence](../inference/charge-concurrente.md).
- **la boucle d'événements est bloquée.** Un appel synchrone, ou un calcul, tient
  le fil et rien ne progresse.

Ce qui les distingue, et c'est un diagnostic gratuit : **interroger la route de
santé pendant l'incident**. Elle ne touche pas au modèle. Si elle répond vite,
la boucle tourne et le goulot est en aval ; si elle est lente elle aussi, le
service lui-même est bloqué. Un seul appel sépare deux corrections qui n'ont
rien en commun.

### Les codes de statut sont un message à l'appelant

Ils ne décrivent pas ce qui s'est passé chez nous, ils disent **qui doit agir**.
C'est le seul angle qui permet de choisir sans hésiter :

- une requête invalide dit à l'appelant *corrige ta requête, ne la rejoue pas
  telle quelle* ;
- un backend indisponible dit *ta requête était bonne, réessaie plus tard* — et
  c'est ce qui autorise un client à mettre en place une reprise ;
- une erreur interne dit *ne réessaie pas, ça ne servira à rien*.

Confondre les deux premiers a un coût concret : un appelant qui reçoit un refus
de validation là où le service était momentanément indisponible abandonnera une
requête qui aurait abouti.

À côté d'eux, la route de santé n'est **pas** de la même nature et ne se range
pas avec les routes métier : elle ne rend aucune donnée du domaine et existe
pour un consommateur non humain — un orchestrateur de conteneurs qui décide de
redémarrer ou non. C'est aussi ce qui la rend utilisable comme instrument de
diagnostic ci-dessus.

## Quand c'est la bonne réponse

**Exposer en HTTP** quand un consommateur ne peut pas importer le code : un
autre langage, un autre conteneur, un outil tiers. C'est le cas du serveur MCP
et de tout ce qui vient du homelab.

**Ne pas exposer** quand le seul consommateur est du Python du même dépôt.
L'appel direct est plus rapide, se teste sans serveur, et ne demande ni contrat
sérialisé ni gestion de panne réseau. Un service posé sur un usage interne
ajoute une couche de traduction et un mode de panne pour rien.

**Exposer plus tard** quand la brique n'est pas stable. Une interface HTTP
publiée est un contrat avec des appelants qu'on ne contrôle pas ; la changer
coûte bien plus cher que de changer une signature Python.

## Ce qu'on ne saura pas faire

Aucun service n'existe dans ce dépôt : il n'y a ni route, ni modèle d'API, ni
brique de retrieval à exposer — [le RAG](../retrieval/rag-a-la-main.md) tourne
en scripts. Tout ce qui précède est une conception, et notamment le diagnostic
par la route de santé n'a jamais été exercé sur un incident réel.

Ce que ça laisse ouvert, et qui ne se déduit pas : quels champs de métriques
valent d'être rendus par réponse, si le flux de tokens doit traverser la route
ou s'arrêter au service, et ce que doit faire le service quand le backend rend
une réponse partielle plutôt qu'une erreur franche. La troisième est la plus
délicate, parce qu'elle n'a pas de bonne réponse générale.

Ce qui promouvrait cette leçon en leçon « refaire » : le service écrit, et
surtout une mesure sous requêtes concurrentes qui sépare ce que fait la boucle
d'événements de ce que fait le moteur — les deux causes ci-dessus, distinguées
par des chiffres et non par un raisonnement.

## Se tester

1. Vous ajoutez une route asynchrone qui appelle le modèle avec un client
   synchrone. Que se passe-t-il quand deux requêtes arrivent ensemble, et
   pourquoi le code paraît-il pourtant correct ?
   *Réussi si* la réponse dit que la première gèle la seconde, rattache ça au
   fil unique de la boucle d'événements, et note qu'aucune erreur n'est levée.
2. Les temps de réponse explosent en charge. Quel appel faites-vous en premier,
   et qu'est-ce que chaque résultat vous apprend ?
   *Réussi si* la réponse interroge la route de santé et sait interpréter les
   deux cas : rapide, le goulot est dans le moteur ; lente, la boucle est
   bloquée.
3. Votre route contient trois lignes qui reformatent les sources avant de les
   rendre. Où doivent-elles aller, et quel est l'argument décisif ?
   *Réussi si* la réponse les déplace dans la bibliothèque en invoquant la
   testabilité sans serveur **ou** la promouvabilité — pas « c'est plus propre ».

## À retenir

- Exposer change le modèle de panne : une exception lue par son auteur devient
  un statut interprété par un appelant qui ne connaît pas le code.
- La route est mince pour deux raisons vérifiables : le code qui y reste ne se
  teste qu'avec un serveur, et ne peut pas être promu.
- La validation à l'entrée nomme le champ fautif au bord ; le contrat de sortie
  fixe ce sur quoi un tiers a le droit de compter.
- L'asynchrone achète du débit, jamais de la latence — et un client synchrone
  dans une route asynchrone gèle tout, sans erreur.
- Un statut dit qui doit agir : corriger, réessayer, ou renoncer.
- La route de santé n'est pas une route métier ; c'est aussi ce qui en fait le
  meilleur instrument de diagnostic sous charge.

## Références

- Doc FastAPI — les modèles Pydantic aux deux bords, la documentation générée,
  et les pages sur l'asynchrone, à lire pour le cas du client bloquant
- [Charge concurrente](../inference/charge-concurrente.md) — l'autre cause de
  l'effondrement sous charge, celle qui n'appartient pas au service
