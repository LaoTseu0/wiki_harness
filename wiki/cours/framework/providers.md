# Providers — le backend commutable

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la promotion](promotion.md) — et précisément son
  critère « l'interface attend le deuxième usage concret », qui est la raison
  pour laquelle rien de ce qui suit n'est encore écrit ;
  [les embeddings](../retrieval/embeddings.md) — un texte devient un point dans
  un espace **défini par les poids du modèle**. Cette seconde propriété porte
  toute la leçon : c'est elle qui rend la génération commutable et les
  embeddings non.
- **Débloque** : [l'évolutivité](evolutivite.md), dont un provider est le cas
  d'école ; [le routage](routage-multi-agentique.md), qui suppose plusieurs
  backends disponibles pour arbitrer entre eux ; les evals comparatives, qui
  n'ont de sens qu'à backend commutable.

## L'essentiel

Un *provider* est l'abstraction qui rend le backend d'inférence remplaçable
par configuration : local ou distant, sans toucher au code appelant. La thèse
de la leçon n'est pas qu'il faut en écrire une — c'est que **l'abstraction n'a
pas la même valeur selon la capacité**, et que traiter génération et embeddings
comme deux implémentations du même contrat est une faute qui se paie à
l'indexation.

La génération commute librement : deux modèles rendent du texte, comparable
sans précaution. Les embeddings ne commutent pas : deux modèles rendent des
vecteurs de deux espaces différents, et rien n'avertit qu'on les compare.

Rien de ce qui suit n'est écrit dans
[`src/framework/`](../../src/framework/README.md), et c'est délibéré — voir
*Ce qu'on ne saura pas faire*. Cette leçon décide de la forme, pas du calendrier.
Elle ne couvre pas le *choix* d'un backend selon la tâche, qui est
[le routage](routage-multi-agentique.md), ni l'exposition d'une brique en HTTP,
qui est [le service](service.md).

## Le savoir

### Une interface par capacité, pas une par fournisseur

Le découpage naturel — « un objet Ollama, un objet OpenAI » — est le mauvais.
Il oblige chaque implémentation à tout couvrir, alors qu'aucun déploiement réel
n'utilise le même fournisseur pour tout : générer en local et embarquer les
vecteurs d'un modèle spécialisé est le cas ordinaire, pas l'exception.

Le découpage utile est donc **par capacité** : générer, embarquer, et plus tard
re-classer. Chacune est un contrat étroit, avec son propre jeu
d'implémentations, et rien n'oblige la même adresse à servir les trois.

### Ce que « normaliser aux frontières » veut dire concrètement

La règle s'énonce vite et se viole tout aussi vite : les types échangés —
un message, une réponse — sont **les nôtres**, et les particularités de chaque
fournisseur se règlent *à l'intérieur* de son implémentation.

Le test qui la rend vérifiable : *une signature qui nomme un fournisseur a
déjà échoué*. Un paramètre `options` transmis tel quel parce qu'Ollama l'accepte
oblige chaque implémentation suivante à simuler la sémantique d'Ollama, ou à
l'ignorer en silence — ce qui est pire, l'appelant croyant régler quelque chose.
La normalisation coûte au moment de l'écriture ; l'absence de normalisation
coûte à chaque implémentation ajoutée, indéfiniment.

Les particularités à absorber sont connues et concrètes : les préfixes de tâche
que réclament certains modèles d'[embeddings](../retrieval/embeddings.md), la
forme des appels d'outils, le nom des compteurs de tokens.

### L'asymétrie qui gouverne tout : les embeddings ne commutent pas

C'est le point non évident, et le seul qui change une décision d'architecture.

Un embedding n'est pas une description du texte : c'est un **point dans un
espace dont la géométrie vient des poids du modèle**. Deux modèles produisent
deux espaces sans relation — pas deux systèmes de coordonnées convertibles,
deux espaces distincts. La [similarité cosinus](../retrieval/similarite-cosinus.md)
entre un vecteur de l'un et un vecteur de l'autre se **calcule** sans erreur et
ne **signifie** rien.

Trois conséquences en découlent directement :

- changer de modèle d'embeddings impose de **ré-indexer le corpus entier** ; ce
  n'est pas une optimisation reportable, c'est la condition pour que l'index
  ait un sens ;
- la panne est **silencieuse**. Aucune exception, aucune dimension incompatible
  si les tailles coïncident — seulement des résultats de recherche devenus
  arbitraires. Rien dans la pile ne peut la détecter, parce qu'il n'y a rien à
  détecter : l'opération est légale ;
- donc l'index doit **mémoriser le modèle qui l'a produit**, et le refus doit
  être posé au démarrage, avant la première requête. C'est la seule barrière
  possible, et elle ne peut pas venir de l'abstraction provider : elle vient de
  l'index.

La génération, elle, n'a pas ce problème. Changer de modèle change la qualité
des réponses, ce qui se voit, se mesure et se compare — pas leur
interprétabilité.

### Le commutateur de configuration, avec sa portée

- **Où il agit** : à la construction des briques, au démarrage du processus.
  Jamais dans le corps d'un appel — un provider qu'on choisit par requête n'est
  plus une configuration, c'est [du routage](routage-multi-agentique.md), et
  les deux ne se règlent pas au même endroit.
- **À quelle fréquence** : une fois. C'est ce qui permet de le valider une fois
  aussi, en échouant au démarrage plutôt qu'au centième appel.
- **Ce qu'il propage** : tout ce qui est en aval — le format des réponses, le
  coût, la latence, la confidentialité des données envoyées. Le dernier point
  est le plus facile à oublier : commuter la génération vers une API distante
  fait sortir le contenu des prompts du réseau local, ce qu'aucun test ne
  signale.
- **Ce qui l'annule** : un index construit avec un autre modèle d'embeddings.
  Le verrou index ↔ modèle doit refuser le démarrage ; sans lui, le
  commutateur « fonctionne » et le système est faux.

### Qui décide, quand il y a plusieurs implémentations

Dire « la config choisit le provider » escamote la pièce. Ce qui choisit est
une **fonction de construction** qui lit une valeur validée — un modèle de
configuration typé, pas un `os.environ` lu au vol — et rend l'implémentation
correspondante. Elle est le seul endroit du code qui connaît la liste des
implémentations ; partout ailleurs, on ne manipule que le contrat.

La conséquence pratique est un test : si un `import` de `OllamaProvider`
apparaît ailleurs que dans cette fonction, la commutabilité est déjà perdue,
quelle que soit la config.

## Quand c'est la bonne réponse

**Abstraire** quand un deuxième backend est *réel* — installé, appelé, testé.
Le cas identifié ici en est un : une API compatible OpenAI couvre à la fois
[vLLM](../inference/vllm-sur-rtx-2060.md) en local et la plupart des offres
distantes, ce qui fait un contrat pour deux usages franchement différents. Le
deuxième usage est ce qui révèle quelles parties du contrat étaient en réalité
la forme d'Ollama.

**Ne pas abstraire** tant qu'il n'y en a qu'un. C'est la situation actuelle, et
la [promotion](promotion.md) donne la raison : un contrat écrit à une seule
implémentation décrit cette implémentation. Le nom générique donne l'illusion
d'un choix qui n'existe pas.

**Ne pas abstraire non plus** quand la variation ne porte pas sur le backend
mais sur la tâche. Un modèle rapide pour trier, un modèle lent pour rédiger,
n'est pas une affaire de provider : c'est un arbitrage par requête, donc
[du routage](routage-multi-agentique.md). Les confondre produit une
configuration qui doit changer en cours d'exécution — le signe qu'on s'est
trompé de couche.

## Ce qu'on ne saura pas faire

Cette leçon décide d'une **forme**, pas d'un code. Rien n'est écrit dans
`src/framework/` : il n'y a qu'un client Ollama, sans contrat au-dessus, parce
que le deuxième backend n'a pas encore tourné. Tant que c'est le cas, on ne sait
pas lesquelles des propriétés énoncées ci-dessus résistent au contact — et
l'expérience de la promotion est que ce sont rarement celles qu'on croit.

Trois questions resteront ouvertes jusque-là, et aucune ne se tranche par
raisonnement :

- le contrat est-il synchrone ou asynchrone ? Le choix contamine tout l'appelant
  et ne se change pas après coup sans réécrire les consommateurs.
- que devient une capacité qu'un backend n'a pas — une erreur au démarrage, une
  valeur absente, une émulation ?
- les compteurs de tokens, qui n'ont pas le même nom ni la même définition d'un
  fournisseur à l'autre, sont-ils normalisables sans mentir ?

Ce qui promouvrait cette leçon en leçon « refaire » : le jour où deux backends
tournent réellement, une étape qui rejoue les mêmes evals sur les deux et
compare qualité, coût et confidentialité — le tableau que la leçon annonce sans
pouvoir le produire.

## Se tester

1. Un collègue veut « juste tester » un autre modèle d'embeddings sur l'index
   existant, sans ré-indexer, « pour voir ». Que se passe-t-il exactement, et
   pourquoi est-ce plus grave qu'une erreur ?
   *Réussi si* la réponse dit que le calcul aboutit sans lever, que les
   résultats deviennent arbitraires, et rattache ça à l'absence de relation
   entre les deux espaces — pas à une « perte de précision ».
2. Les réponses d'un RAG se sont dégradées après une bascule de configuration.
   Deux causes possibles : lesquelles, et que regardez-vous en premier ?
   *Réussi si* la réponse sépare « le modèle de génération a changé » de
   « l'espace d'embeddings a changé », et va inspecter les **chunks remontés**
   plutôt que les réponses — les chunks discriminent, les réponses non.
3. On vous propose une interface `Provider` unique avec `chat()` et `embed()`,
   une classe par fournisseur. Quelle objection, et sur quel cas concret ?
   *Réussi si* l'objection porte sur le découpage par fournisseur plutôt que
   par capacité, et cite le cas ordinaire : générer ici, embarquer avec un
   modèle spécialisé ailleurs.

## À retenir

- Un contrat par **capacité** (générer, embarquer), pas un par fournisseur :
  aucun déploiement réel n'utilise le même backend pour tout.
- Normaliser aux frontières : une signature qui nomme un fournisseur a déjà
  échoué.
- La génération commute, les embeddings non — deux modèles définissent deux
  espaces sans relation, et la comparaison entre eux se calcule sans erreur.
- La panne d'embeddings est silencieuse : d'où le verrou index ↔ modèle, posé
  au démarrage, et qui appartient à l'index, pas au provider.
- Une seule implémentation ne justifie aucun contrat ; le deuxième backend est
  ce qui révèle ce qui n'était que la forme du premier.

## Références

- Pydantic Settings — la configuration validée au démarrage, plutôt que lue au
  vol dans l'environnement
- `typing.Protocol` — le contrat structurel, sans héritage, quand il sera temps
  de l'écrire
- La spécification d'API OpenAI — non pour elle-même, mais parce qu'elle est
  devenue le dénominateur commun que la plupart des backends acceptent
