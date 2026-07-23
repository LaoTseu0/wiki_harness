# Mode RPC/SDK

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [le service FastAPI](../framework/service.md) — exposer une
  brique en HTTP, le pattern du service ; [le chat, l'historique et le
  contexte](../fondamentaux/chat-historique-contexte.md) — le contexte s'accumule
  et rien n'est conservé côté serveur ; [la mémoire versionnée](memoire-versionnee.md)
  — ce qui rend une session jetable ; [le hook `tool_call`](hook-tool-call.md) —
  le human-in-the-loop, qui devra trouver ici sa forme asynchrone.
- **Débloque** : [le comparatif des régimes](quatre-regimes.md) sur l'axe du
  cycle de vie ; [la note de conception](note-de-conception.md), où le
  multi-sessions reste explicitement ouvert.

## L'essentiel

Jusqu'ici l'agent vit le temps d'une session interactive. Le mode RPC/SDK inverse
le rapport : un **service qui tient une session Pi ouverte**, pilotable par
programme — l'embryon d'agent *persistant*, celui qu'un événement domotique
pourra déclencher plutôt qu'un humain au clavier.

La thèse : la persistance ne change pas la boucle. Elle promeut trois choses de
**confort à nécessité** — la gestion de contexte, le human-in-the-loop
asynchrone, et la santé de session — parce qu'aucune ne peut plus s'appuyer sur
le fait qu'une session « finit » bientôt.

Cette leçon ne construit pas la plateforme : file de tâches, multi-sessions,
déclencheurs événementiels sont **hors scope**. Le but est de démontrer le
régime, pas de l'industrialiser.

## Le savoir

### Le changement de posture

On passe de « l'humain ouvre une session » à « la session attend des requêtes ».
Concrètement : un petit service — le pattern du [service FastAPI](../framework/service.md)
— possède une session Pi via son mode RPC/SDK et expose `POST /task` → réponse de
l'agent. La boucle interne est inchangée ; ce qui change, c'est qui l'appelle et
combien de temps elle vit.

### Le contexte s'accumule, donc gestion et mémoire deviennent obligatoires

Entre deux requêtes, le contexte **s'accumule** — c'est ce qui donne à l'agent sa
continuité, et c'est aussi ce qui finit par déborder. La question « quand
committer ? » n'a plus sa réponse évidente : si la session ne finit jamais, le
`session_shutdown` de la [mémoire versionnée](memoire-versionnee.md) ne se
déclenche jamais. La réponse est des **checkpoints périodiques** — et la mémoire
externe est ce qui rend la session jetable, donc ce qui autorise à la recycler
sans rien perdre.

### Le human-in-the-loop doit devenir asynchrone

Le [hook](hook-tool-call.md) vaut toujours pour les requêtes programmatiques.
Mais la validation humaine synchrone — la commande affichée, l'attente au clavier
— n'existe plus : personne n'est au clavier. Elle prend une forme asynchrone,
avec deux exigences.

- Une **file d'approbation avec TTL** : une approbation qui n'arrive pas à temps
  devient un **refus**, renvoyé au modèle comme une information — jamais un
  silence, sous peine de le laisser croire sa demande exécutée.
- Une **re-validation contre l'état courant** : une action approuvée tardivement
  se re-vérifie avant de s'exécuter. Approuver à H puis exécuter à H+6 sans
  re-vérifier est le piège propre à l'agent persistant — l'approbation portait sur
  un monde qui a peut-être changé.

### La santé de session, sur déclencheurs mesurables

Une session qui vit des jours **dérive** : le contexte enfle, l'état se charge.
On prévoit donc recyclage et résurrection propre, déclenchés par des seuils
**mesurables** — un plafond de tokens de contexte, un nombre de tâches traitées,
un taux d'erreurs d'outils qui monte — et non « au feeling ». La mémoire externe
est ce qui rend ce recyclage indolore : mourir ne coûte rien quand l'essentiel
est déjà consigné hors de la session.

### La persistance, avec sa portée

- **Où elle agit** : au niveau du service qui tient la session, pas dans la boucle
  interne.
- **À quelle fréquence** : le contexte s'accumule à chaque requête ; le checkpoint
  mémoire tombe toutes les *n* tâches.
- **Ce qu'elle propage** : le contexte accumulé sert les requêtes suivantes —
  partage voulu — mais dérive avec le temps si rien ne le borne.
- **Ce qui l'annule** : un recyclage régulier adossé à la mémoire externe. Une
  session qu'on peut tuer et ressusciter sans perte n'a plus d'enjeu de
  persistance — la continuité est passée dans la mémoire, pas dans la session
  vivante.

## Quand c'est la bonne réponse

**Persistant** quand un déclencheur non-humain justifie une session qui attend —
un événement domotique —, ou quand le contexte partagé entre requêtes a une
valeur réelle. **Éphémère** sinon : moins de surface d'erreur, pas de dérive à
surveiller, pas de human-in-the-loop asynchrone à concevoir.

Dans tous les cas persistants, une contrainte : **sérialiser les requêtes**. Une
session est un fil unique ; deux requêtes concurrentes s'entremêlent dans le même
contexte. Il faut une file d'attente explicite, et le dire — un parallélisme
implicite est un bug qui se manifeste tard.

## Ce qu'on ne saura pas faire

On n'a pas, chiffré, le seuil — en tokens ou en tâches — à partir duquel une
session dérive sur ce modèle et ce matériel ; c'est exactement le déclencheur de
recyclage qu'on ne peut pas fixer sans l'avoir mesuré.

Deux pièges restent anticipés, non vérifiés en situation : la **session
immortelle** — sans recyclage, le contexte finit par déborder ou dériver — et la
**perte du human-in-the-loop** en devenant service — les actions sensibles
doivent *attendre* une approbation, jamais être silencieusement refusées, ni pire,
accordées.

Ce qui promouvrait cette leçon en « refaire » : un service minimal sous
`wiki/etapes/agent/` — session Pi tenue ouverte, `POST /task`, checkpoint mémoire
toutes les *n* tâches, endpoint `/health` qui vérifie la session — et une démo de
trois tâches successives qui partagent le contexte.

## Se tester

1. Quelle différence entre un agent interactif et un agent persistant, et
   qu'est-ce qu'elle déplace ?
   *Réussi si* la réponse pointe le cycle de vie — session éphémère pilotée par
   l'humain contre service long-vivant piloté par événements — qui met la gestion
   de contexte, le human-in-the-loop et la santé de session au premier plan, la
   mémoire externe rendant les deux régimes compatibles.
2. Une action est approuvée à H et ne s'exécute qu'à H+6. Que faut-il faire avant
   de l'exécuter, et pourquoi ?
   *Réussi si* la réponse re-valide l'action contre l'état courant, parce que
   approuver n'est pas exécuter et que le monde a pu changer entre-temps.
3. Deux requêtes arrivent en même temps sur la session. Que se passe-t-il si on
   ne prévoit rien ?
   *Réussi si* la réponse voit qu'elles s'entremêlent dans un contexte unique
   (une session = un fil) et impose une file d'attente explicite.

## À retenir

- La persistance ne change pas la boucle ; elle promeut contexte, human-in-the-loop
  et santé de session de confort à nécessité.
- Une session qui ne finit jamais commit par checkpoints périodiques, pas à la
  fermeture.
- Le human-in-the-loop devient asynchrone : file d'approbation avec TTL, et
  re-validation contre l'état courant avant d'exécuter une approbation tardive.
- Le recyclage de session se déclenche sur des seuils mesurables ; la mémoire
  externe rend la session jetable.
- Une session est un fil unique : les requêtes concurrentes se sérialisent
  explicitement.

## Références

- Mode RPC/SDK du harnais Pi — la documentation qui décrit comment tenir une
  session ouverte et l'appeler par programme
- [Mémoire versionnée](memoire-versionnee.md) — la brique qui rend la session
  jetable, donc recyclable sans perte
