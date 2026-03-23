# Mini-boucle d'agent

> [carte du cours](../carte.md) · étape : [`07_agent.py`](../../etapes/fondamentaux/07_agent.py)

## Où ça s'emboîte

- **Processus** : [d'une tâche à un résultat](../_processus/boucle-outils.md)
- **L'étape ouverte** : `execution` · `renvoi` · `plafond` — entre une fonction résolue, sort soit un tour de plus, soit la main rendue à l'appelant

![[boucle-agent.canvas]]

## Prérequis et suites

- **Suppose acquis** : [le function calling](function-calling.md) — le cycle
  complet, et surtout que les arguments produits par le modèle sont des
  **entrées non fiables** ; [le fait stateless](chat-historique-contexte.md) —
  rien n'est conservé côté serveur, donc la requête entière repart à chaque
  tour. La première propriété ressert à chaque garde ci-dessous ; la seconde
  explique pourquoi une boucle d'agent coûte plus qu'un appel répété.
- **Débloque** : [le harnais](../agent/garde-fous.md), qui reprend ces trois
  gardes à l'échelle d'un vrai agent — interception systématique des appels et
  périmètre système ; et tout ce qui borne une boucle qu'on ne surveille pas.

## L'essentiel

Un agent n'est rien d'autre qu'une **boucle `while` autour du function
calling** : le modèle demande un outil, on exécute, on renvoie, on recommence —
jusqu'à ce qu'il réponde sans demander d'outil, ou qu'un plafond l'arrête. La
boucle de `07` est celle de `06`, copiée sans modification ; la seule ligne
nouvelle est la borne.

Ce qui change, ce n'est donc pas la mécanique, c'est la **nature des outils**.
Jusqu'ici ils lisaient une information ; maintenant ils écrivent sur le disque
et lancent des commandes. Le passage de « lire » à « agir » ne demande aucune
construction supplémentaire, et c'est exactement pour ça qu'il est dangereux :
rien dans le code ne signale qu'on a franchi la ligne.

Cette leçon ne couvre pas l'interception généralisée des appels — un point de
contrôle unique, indépendant des outils — qui est
[le hook `tool_call`](../agent/hook-tool-call.md), ni le confinement du
processus lui-même, qui est
[le conteneur à moindre privilège](../agent/conteneur-moindre-privilege.md).

## Le savoir

### Ce qui arrête la boucle n'est pas une décision du modèle

La condition de sortie s'énonce souvent « quand le modèle estime avoir
terminé ». Ce n'est pas ce que le code teste. Il teste **l'absence de la clé
`tool_calls`** dans le message rendu : `message.get("tool_calls")` est vide,
donc c'est la réponse finale. Un test mécanique sur un champ JSON, pas une
intention.

La différence est pratique. Un modèle qui produit du texte *et* un appel
d'outil dans le même message ne termine pas — le texte est ignoré comme
réponse et le tour continue. Un modèle qui rend un `tool_calls` vide plutôt
qu'absent termine ou non selon la façon dont le serveur a sérialisé le champ.
La sortie de boucle dépend d'un détail de forme, et c'est le genre de chose
qu'on ne trouve qu'en lisant la réponse brute.

Le second point de sortie est le `for ... else` de Python : le `else` d'une
boucle `for` ne s'exécute **que si la boucle est allée au bout sans `break`**.
C'est donc littéralement la branche « le plafond a été atteint », distincte de
toutes les autres sorties.

### Le plafond, avec sa portée

- **Où il agit** : à l'étape `plafond`, après chaque `renvoi`, avant de
  relancer une génération.
- **À quelle fréquence** : une fois par tour d'outil, et le compteur **repart
  à zéro à chaque message utilisateur**. Il borne un enchaînement d'outils, pas
  une conversation.
- **Ce qu'il propage** : rien vers le modèle. Le plafond coupe côté client ; le
  modèle n'apprend pas qu'il a été arrêté, et l'historique conserve sa dernière
  demande sans réponse. Au tour suivant, il lira une demande d'outil restée
  sans résultat — situation qu'aucune consigne ne lui a décrite.
- **Ce qui l'annule** : un modèle qui répond sans jamais demander d'outil. Le
  `break` tombe au premier tour et le plafond ne borne plus rien. Il ne borne
  pas non plus la longueur d'une seule génération — c'est `num_predict` — ni la
  durée d'un outil qui ne rend pas la main : c'est le `timeout` de
  `subprocess.run`. Trois bornes, trois échelles.

Cette dernière ligne est la plus utile à retenir. Un agent peut être bordé sur
le nombre de tours et rester bloqué indéfiniment sur un seul appel, ou terminer
en quelques tours après avoir produit une génération démesurée. Le plafond de
tours ne protège que d'un mode d'échec parmi trois.

### Les trois gardes, et ce que chacune ne couvre pas

**Le périmètre.** `chemin_securise()` joint le nom au dossier de travail,
appelle `resolve()`, puis vérifie avec `is_relative_to()` que le résultat est
resté sous la racine. L'ordre est ce qui compte : `resolve()` **applique** les
`..` et normalise les liens ; la vérification porte donc sur le chemin réel, pas
sur la chaîne demandée. Chercher `".." in nom` serait la version naïve, et elle
échoue sur deux entrées que celle-ci arrête — un chemin absolu, parce que
joindre un chemin absolu en `pathlib` **remplace** la base au lieu de s'y
ajouter, et un lien symbolique qui pointe hors du périmètre.

Ce que la garde ne couvre pas : ce qui se passe *dans* le périmètre. Un agent
qui écrase un fichier de travail est parfaitement dans son droit.

**La validation humaine.** `executer_commande()` affiche la commande et attend
une confirmation au clavier avant de lancer quoi que ce soit. Le point
non évident est le traitement du refus : il est renvoyé au modèle **comme un
résultat d'outil** — « Commande refusée par l'utilisateur ». Sans ce retour, le
modèle croit sa demande exécutée et continue sur une prémisse fausse. Un refus
silencieux est pire qu'un refus.

Ce que la garde ne couvre pas : elle porte sur un seul outil. Les trois autres
s'exécutent sans validation, dont celui qui écrit sur le disque. C'est un choix
d'étape, pas une position défendable en général — et c'est précisément la
limite que le [hook `tool_call`](../agent/hook-tool-call.md) lève, en déplaçant
le point de contrôle des outils vers la boucle.

**La borne.** Traitée ci-dessus.

À côté de ces trois-là, `lire_fichier` tronque au-delà de deux mille
caractères. Ce n'est **pas** une garde de sécurité et il ne faut pas la ranger
avec elles : elle protège la fenêtre de contexte, pas le système. Un fichier
énorme injecté tel quel évince l'historique ; c'est un problème de budget, dont
la conséquence est une réponse dégradée, pas une action non désirée.

### Les outils fiabilisent les données, pas le raisonnement

C'est le résultat le plus important de l'étape, et il va contre l'intuition qui
justifie les outils. Donner un outil au modèle garantit que la **donnée** qui
entre est exacte : l'heure vient de l'horloge, le listing vient du disque. Ça ne
garantit rien sur ce que le modèle fait de cette donnée ensuite, parce que
l'interprétation d'un résultat d'outil est, elle aussi, une génération
probabiliste.

Un résultat d'outil n'a aucun statut particulier dans le contexte : c'est un
message de plus, du texte parmi du texte. Il ne « prouve » rien au modèle. Cela
suffit à prédire qu'un agent puisse contredire un listing qu'il vient lui-même
de demander — et c'est ce qui a été observé (voir *Pièges*).

## En pratique

[07_agent.py](../../etapes/fondamentaux/07_agent.py) : un dossier de travail
dédié, quatre outils — lister, lire, écrire, exécuter une commande —, la
validation humaine sur le shell, et `MAX_TOURS`. `ecrire_fichier` est à écrire,
avec sa garde de chemin.

**À prédire avant de lancer** :

- « Crée un fichier puis relis-le moi » : combien de tours d'outils, et combien
  de messages en tout s'ajoutent à l'historique ?
- on demande de lire `../06_outils.py` : où exactement l'appel est-il arrêté,
  et **que voit le modèle** ? Formule-le avant de regarder la trace.
- on refuse une commande shell au clavier : que fait le modèle au tour suivant
  — réessaie-t-il, abandonne-t-il, propose-t-il autre chose ?
- on abaisse `MAX_TOURS` à 2 et on demande une tâche qui en réclame quatre :
  qu'est-ce qui s'affiche à la fin ? Regarde la dernière ligne du script et
  demande-toi ce que vaut `message['content']` quand la boucle a été coupée.

## Mesures

<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->

## Recomposer

**Ce que ça change à ce qu'on croyait savoir.** Le rôle `tool` du
[function calling](function-calling.md) paraissait un canal de retour privilégié
— la voie par laquelle du fait entre dans la conversation. La boucle montre
qu'il n'en est rien : c'est un message ordinaire, sans autorité particulière,
soumis à la même génération que le reste. Ce qui distingue un agent d'un chat
n'est donc pas qu'il « sait » des choses vraies, c'est qu'il peut **agir**, et
l'action est irréversible là où une phrase fausse ne l'est pas.

Le budget de contexte change aussi de nature. Dans un chat, il croît avec les
tours d'une conversation, à un rythme humain. Ici, un seul message utilisateur
peut déclencher dix tours d'outils, chacun ajoutant une demande et un résultat,
et chacun re-transmettant tout le préfixe : le contexte enfle **à l'intérieur
d'un tour**, sans que personne ne regarde.

**Ce qu'on peut prédire ailleurs.** Puisque le résultat d'un outil est du texte
ordinaire réinjecté dans le prompt, un fichier lu par l'agent peut contenir des
instructions que le modèle traitera comme des consignes. Aucune barrière ne
sépare la donnée de l'ordre — c'est structurel, pas un défaut d'implémentation.
Cela suffit à prédire la forme de
[l'injection indirecte](../mcp/prompt-injection-indirecte.md) avant d'en écrire
la leçon, et à savoir que la parade ne pourra pas être « mieux filtrer le
contenu lu ».

## Pièges connus

- **Rencontrés** :
  - *Le modèle a nié une suppression que le listing prouvait.* Il avait demandé
    l'exécution, la commande avait abouti, un listing ultérieur montrait le
    fichier absent — et il a soutenu le contraire. Symptôme : une affirmation
    en contradiction directe avec un résultat d'outil présent dans le même
    contexte. Ce n'est ni un bug d'outil ni une erreur d'exécution : c'est
    l'interprétation du résultat, qui reste probabiliste. D'où la règle
    transférable : **un outil fiabilise la donnée, jamais la conclusion** — ce
    qui exige de vérifier soi-même l'état du monde plutôt que de croire le
    compte rendu de l'agent.
  - *Le modèle a auto-corrigé `rm` en `del` selon la plateforme.* Comportement
    utile, et instructif sur ce que le catalogue ne dit pas : rien dans les
    descriptions n'annonçait le système hôte. La correction vient donc de ses
    connaissances générales, pas d'une information qu'on lui aurait fournie —
    donc elle n'est pas fiable, et elle échouera sur une plateforme moins
    représentée.
  - *Une faute de frappe dans un argument*, déjà rencontrée au
    [function calling](function-calling.md) : ici les conséquences se voient sur
    le disque.
  - *Contre-épreuve à faire.* Rejouer ces trois incidents sur un modèle
    nettement plus grand, pour séparer ce qui tient à la taille du modèle de ce
    qui tient à la nature de la boucle. Tant que ce n'est pas fait, « c'est
    parce que le modèle est petit » reste une hypothèse — et la conception ne
    doit pas s'y fier.
- **Anticipés** — non vérifiés à ce jour :
  - *Le message final peut être vide quand le plafond a coupé.* La dernière
    ligne du script affiche le contenu du dernier message ; or, si la boucle a
    été interrompue, ce message est celui qui portait des `tool_calls`, dont le
    contenu texte est en général vide. On verrait donc l'agent « ne rien
    répondre » alors que la trace de coupure, elle, s'affiche.
  - *Deux causes pour un agent qui ne répond pas.* Plafond atteint, ou réponse
    finale au contenu vide. La trace de coupure les sépare : elle n'apparaît que
    dans le premier cas.
  - *Les appels parallèles ne sont pas ordonnés vis-à-vis des gardes.* Si le
    modèle demande plusieurs outils dans un même message, ils sont exécutés en
    séquence dans la boucle interne, et une validation refusée n'empêche pas
    les suivants de s'exécuter.

## Se tester

1. Un agent tourne mais ne répond jamais rien à la fin. Deux mécanismes
   produisent cet écran : lesquels, et quelle ligne de la sortie les distingue ?
   *Réussi si* la réponse oppose le plafond atteint à une réponse finale de
   contenu vide, et nomme la trace de coupure comme critère — pas une intuition
   sur « le modèle a planté ».
2. Vous ajoutez un outil `supprimer_fichier`. `MAX_TOURS` est en place et le
   périmètre est vérifié. Qu'est-ce qui manque encore, et quelle garde
   existante faudrait-il étendre plutôt que dupliquer ?
   *Réussi si* la réponse note que la validation humaine ne couvre qu'un seul
   outil, et propose de déplacer le contrôle vers la boucle plutôt que de le
   recopier dans chaque outil destructeur.
3. On vous propose de remplacer la garde de chemin par un test `".." not in
   nom`, « plus simple à lire ». Donnez deux entrées que la version actuelle
   arrête et que celle-ci laisse passer.
   *Réussi si* la réponse cite un chemin absolu — en rappelant que le joindre
   remplace la base — et un lien symbolique, et explique que c'est `resolve()`
   avant la comparaison qui fait le travail.

## Ce que ça change dans le framework

Rien n'est promu, et pour une raison précise : la boucle tient en une quinzaine
de lignes, mais **sa forme n'est pas encore décidée**. Trois questions restent
ouvertes, et chacune changerait l'interface : le plafond est-il un nombre de
tours, un budget de tokens ou une durée ? La trace des appels est-elle un
`print` que la brique fait, ou un événement qu'elle rend à l'appelant ? Les
gardes s'insèrent-elles dans chaque outil, ou en un point unique avant le
dispatch ?

Promouvoir maintenant reviendrait à trancher les trois par défaut, sans le
deuxième usage qui départage. Ce deuxième usage est le domaine
[agent](../agent/garde-fous.md) tout entier, et la troisième question y trouve
déjà sa réponse — le point de contrôle unique.

Ce que la leçon dépose sans code : deux règles qui vaudront pour toute boucle
promue. La sortie de boucle se teste sur un champ, pas sur une intention. Et un
refus se rend au modèle, jamais avalé en silence.

## À retenir

- Un agent est la boucle du function calling, plus une borne. Ce qui change,
  c'est la nature des outils, pas la mécanique.
- La sortie de boucle est un test sur l'absence de `tool_calls` — mécanique,
  pas intentionnelle.
- Le plafond de tours, `num_predict` et le délai d'un outil bornent trois
  échelles différentes ; aucun ne remplace les autres.
- La garde de chemin fonctionne parce qu'elle normalise **avant** de comparer.
- Un refus non renvoyé au modèle le laisse croire sa demande exécutée.
- Les outils fiabilisent les données, jamais le raisonnement qui les lit.

## Références

- [securite.md §5 du homelab](../../../../homelab/architecture/securite.md) —
  les non-négociables d'origine, à confronter aux trois gardes de l'étape
- `pathlib` : `resolve()` et `is_relative_to()` — et la règle de jonction d'un
  chemin absolu, qui est la raison d'être de l'ordre des deux appels
- La clause `else` d'une boucle `for` en Python — rare, et exactement adaptée
  à la branche « plafond atteint »
