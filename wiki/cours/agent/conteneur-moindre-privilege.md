# Conteneur et moindre privilège

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [le hook `tool_call`](hook-tool-call.md) — la couche fine
  au-dessus, et pourquoi elle est faillible : un appel qu'elle ne voit pas lui
  échappe. C'est ce trou que le conteneur ferme. [Le garde-fou
  d'ensemble](garde-fous.md) — le conteneur est le périmètre système du couple.
  La propriété d'entrées non fiables du [function calling](../fondamentaux/function-calling.md)
  ressert ici : on dimensionne les droits en supposant que l'agent tentera le
  pire.
- **Débloque** : [l'outil Home Assistant](outil-home-assistant.md), dont le token
  suit la même logique de moindre privilège que les montages ; [le régime
  persistant](mode-rpc-sdk.md), où le conteneur borne un processus qui vit des
  jours au lieu d'une session.

## L'essentiel

Le hook décide, le conteneur **borne**. Même si l'agent — ou une injection —
trouve un chemin que le hook ne voit pas, le processus ne *peut* physiquement
pas sortir de son périmètre : il ne lit pas un partage qui n'est pas monté, ne
joint pas un hôte hors de son réseau, n'écrit pas là où le volume ne le laisse
pas.

La thèse : appliqué à un agent, le **moindre privilège** signifie dimensionner
les droits sur la **tâche**, jamais sur la commodité. Ce que la tâche n'exige
pas n'existe pas pour le processus — et « aucun accès aux partages famille » est
la ligne rouge du homelab, garantie non par une permission bien réglée mais par
l'**absence** du montage.

Cette leçon ne couvre pas ce qui se passe *à l'intérieur* du périmètre — un
fichier de travail écrasé est légitime, c'est au hook d'y regarder — ni ne
prétend qu'un conteneur soit une sandbox parfaite : c'est de l'isolation de
namespace, pas une machine virtuelle.

## Le savoir

### Dimensionner sur la tâche, pas sur la commodité

L'agent Jarvis lit sa documentation, écrit son espace de travail, parle à Home
Assistant et à Ollama. Rien d'autre n'existe pour lui. Le principe se lit à
l'envers pour comprendre son intérêt : le **rayon d'une compromission est
exactement l'ensemble accordé**, ni plus ni moins. Chaque droit ajouté « au cas
où » agrandit ce rayon sans qu'aucune tâche ne le réclame.

### La traduction docker, poste par poste

Le moindre privilège n'est pas une intention, c'est une liste de réglages, et
chacun ferme une voie précise.

- **Filesystem** : volumes explicites (espace de travail en RW, documentation en
  RO), rootfs en lecture seule quand c'est possible (`--read-only` + tmpfs pour
  l'éphémère), et **jamais** de montage des partages famille. L'absence de
  montage est la seule garantie **absolue** : une permission peut être mal
  réglée, un montage qui n'existe pas ne se traverse pas.
- **Utilisateur** : non-root (`user:`), pas de `--privileged`, `cap_drop: [ALL]`
  puis réouverture des seules capabilities nécessaires. Retirer d'abord, rouvrir
  au besoin, plutôt que l'inverse.
- **Réseau** : réseau docker interne, egress limité aux seuls endpoints utiles
  (Home Assistant, Ollama). Un agent qui ne peut pas joindre l'extérieur ne peut
  pas **exfiltrer**, quelle que soit l'instruction qu'on lui injecte
  ([threat model Jarvis](../production/threat-model-jarvis.md)).
- **Ressources** : limites CPU et mémoire — un agent parti en boucle ne couche
  pas la machine hôte.

### Le conteneur ET le hook, chacun pour ce que l'autre rate

Le hook est fin mais logiciel : un motif oublié, un cas non prévu, et il laisse
passer. Le conteneur est grossier mais physique : il ne distingue pas une
écriture utile d'une écriture néfaste, mais il ne cède pas à un motif oublié. La
défense en profondeur tient parce que ces deux défaillances sont **sans cause
commune** — le hook rend l'abus improbable, le conteneur le rend impossible à
sortir du périmètre. Retirer l'un sous prétexte que l'autre existe, c'est
rouvrir le mode de défaillance que l'autre ne couvrait pas.

### Le moindre privilège vaut aussi pour les credentials

Un token est une capability comme un montage. Le token Home Assistant de
[l'outil `home_assistant`](outil-home-assistant.md) sera à périmètre limité —
utilisateur dédié non admin, liste blanche d'entités — exactement pour la même
raison que le partage famille n'est pas monté : ce que la tâche n'exige pas ne
doit pas être accordé, credentials compris.

### Le conteneur, avec sa portée

- **Où il agit** : autour du processus, dès son démarrage.
- **À quelle fréquence** : statique pour toute la vie du conteneur — il ne se
  décide pas par appel comme le hook, il est le cadre dans lequel les appels ont
  lieu.
- **Ce qu'il propage** : il borne tout ce que le processus tente, **hook
  compris** — si le hook a un bug, le conteneur tient quand même.
- **Ce qui l'annule** : un montage large ajouté « temporairement » pour
  déboguer, qui devient permanent ; le réseau par défaut de docker, qui ouvre
  l'egress complet (le moindre privilège réseau se **déclare**, il n'est pas le
  défaut) ; un `--privileged` ou un retour à root, qui rend `cap_drop` inutile.
  Et par nature, une évasion de namespace du noyau : la garantie du conteneur
  s'arrête là où commencerait celle d'une VM.

## Quand c'est la bonne réponse

**Toujours**, pour tout agent qui exécute des outils influencés par du contenu
non fiable. Le conteneur est le **plancher** : la couche qu'on ne retire jamais,
parce qu'elle borne ce que toutes les autres pourraient laisser passer.

**Une VM ou un runtime type gVisor** plutôt qu'un simple conteneur si la charge
est réellement hostile et multi-locataire — là, l'isolation de namespace ne
suffit plus. Pour un agent homelab unique, non-root, sans montage sensible et
sans egress, l'isolation de namespace est **proportionnée** : plus lourd serait
payé sans gain.

Le réflexe de débogage qui va avec : on débogue en **copiant dans** le
périmètre, jamais en l'élargissant. Le volume large « juste pour voir » est la
manière la plus courante d'annuler tout le confinement.

## Ce qu'on ne saura pas faire

On n'a pas, chiffré, le **rayon des dégâts** d'une compromission : il se constate
par un test d'évasion, pas par un raisonnement. Et l'isolation de namespace n'est
pas démontrée ici comme suffisante — elle est **assumée** proportionnée au
contexte, ce qui est un choix de menace, pas une preuve.

Ce qui promouvrait cette leçon en « refaire » : un `docker-compose.yml` sous
`wiki/etapes/agent/` — utilisateur non-root, `cap_drop: ALL`, volumes RO/RW
explicites, réseau interne, limites — accompagné d'un **test d'évasion** : depuis
le conteneur, tenter de lire un chemin famille et de joindre un domaine externe ;
les deux doivent échouer, et c'est cet échec qui remplace l'affirmation.

## Se tester

1. Votre agent est compromis par une injection. Quel est le rayon des dégâts ?
   *Réussi si* la réponse énumère le périmètre concret — l'espace de travail, les
   deux endpoints autorisés, le token HA limité — et conclut « rien d'autre, par
   construction : pas de montage, pas d'egress, pas de privilège ». Si on ne sait
   pas répondre à cette question, le confinement n'existe pas.
2. On monte « temporairement » un volume large pour déboguer un problème.
   Pourquoi est-ce le piège classique, et que faire à la place ?
   *Réussi si* la réponse note que le temporaire devient permanent et propose de
   copier les données de débogage *dans* le périmètre plutôt que d'élargir
   celui-ci.
3. « Le conteneur borne déjà tout, on peut retirer le hook. » Vrai ou faux, et
   pourquoi ?
   *Réussi si* la réponse refuse : le conteneur est grossier — il autorise tout
   ce qui est dans le périmètre, y compris écraser un fichier de travail — et
   c'est le hook qui rattrape le fin. Deux couvertures différentes, pas une
   redondance.

## À retenir

- Le hook décide, le conteneur borne : même un chemin que le hook ne voit pas ne
  mène nulle part hors du périmètre.
- On dimensionne les droits sur la tâche ; le rayon d'une compromission est
  exactement l'ensemble accordé.
- L'absence d'un montage est la seule garantie absolue — une permission se règle
  mal, un montage inexistant ne se traverse pas.
- Le moindre privilège réseau se déclare : le défaut docker ouvre l'egress
  complet, et un agent sans egress ne peut pas exfiltrer.
- Un conteneur est de l'isolation de namespace, pas une VM : d'où le hook au
  dessus et le non-root en dessous.

## Références

- [securite.md du homelab](../../../../homelab/architecture/securite.md) — la
  politique de moindre privilège d'origine
- Documentation docker : `user`, `cap_drop`, `--read-only`, réseaux internes —
  les réglages qui traduisent le principe en configuration
