# Outil home_assistant

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [le function calling à la main](../fondamentaux/function-calling.md)
  — schéma JSON, parsing, exécution, renvoi, et surtout que le nom et la
  description d'un outil **sont du prompt**. [Le conteneur et moindre
  privilège](conteneur-moindre-privilege.md) — le moindre privilège, qu'on
  applique ici au token. [Le hook `tool_call`](hook-tool-call.md) — la décision
  allow/ask, qui traitera différemment la lecture et l'action.
- **Débloque** : [le serveur MCP](../mcp/serveur-mcp-python.md), qui exposera le
  même homelab par un autre canal — même savoir-faire de périmètre, protocole
  différent ; [la mémoire versionnée](memoire-versionnee.md), l'autre capacité du
  groupe.

## L'essentiel

Premier outil custom **réel** qui *agit* : `home_assistant`, enregistré via
`pi.registerTool`, appelle l'API REST de Home Assistant avec un token à périmètre
limité. La mécanique est exactement celle du
[function calling](../fondamentaux/function-calling.md) — un schéma, un dispatch,
une exécution. Mais cette fois l'outil touche la maison.

La thèse : sur un outil qui agit, la **conception de l'outil est déjà de la
sécurité**. Le schéma restreint ce que le modèle peut *demander* avant même que
le hook ne décide s'il l'autorise — un enum d'entités et une séparation
lecture/action font, au niveau du prompt, une partie du travail que le hook fera
au niveau de l'exécution.

Cette leçon ne couvre pas la décision du hook (elle la suppose) ni le conteneur
où vit le token ; elle couvre la **forme** de l'outil.

## Le savoir

### L'API REST de HA, le minimum vital

Trois entrées suffisent : `GET /api/states` (toutes les entités et leurs états),
`GET /api/states/<entity_id>` (une entité), `POST /api/services/<domain>/<service>`
(une action — allumer, couper). L'authentification se fait par en-tête
`Authorization: Bearer <token>`, avec un *long-lived access token*. C'est tout ce
dont l'outil a besoin ; le reste de l'API ne sert pas ici.

### Le périmètre du token se construit hors de HA

Home Assistant ne scope pas finement ses tokens : un token vaut ce que vaut son
utilisateur. Le périmètre se construit donc en **deux couches**, à deux endroits
différents.

- **Côté HA — ce que le token *est*** : un utilisateur HA **dédié** à l'agent,
  **non admin**. Le token hérite de ses droits, et pas davantage.
- **Côté outil — ce que l'outil *fait* du token** : une **liste blanche**
  d'entités et de services. Les lampes du salon, oui ; la serrure, non — même si
  le token, techniquement, pourrait l'atteindre.

C'est le moindre privilège du conteneur appliqué aux credentials : ce que la
tâche n'exige pas n'est pas accordé, et l'absence de droit vaut mieux qu'un droit
qu'on se promet de ne pas utiliser.

### Le schéma restreint avant que le hook ne décide

Trois choix de conception font de la forme de l'outil une garde à part entière.

- **Deux outils plutôt qu'un couteau suisse** : `ha_lire` et `ha_agir`, séparés.
  La séparation n'est pas cosmétique — elle permet au [hook](hook-tool-call.md)
  de traiter la lecture en `allow` et l'action en `ask`. Un outil unique
  forcerait le hook à choisir un seul régime pour les deux.
- **Arguments énumérés** : `entity_id` est un enum **généré depuis la liste
  blanche**. Le modèle ne peut alors pas *inventer* une entité hors périmètre —
  la contrainte de forme du function calling devient une contrainte de sécurité,
  parce qu'une valeur hors enum ne se dispatche pas.
- **Réponses compactes** : `GET /api/states` complet sature la fenêtre — on
  filtre et on résume côté outil. Ce dernier point relève du **budget de
  contexte**, pas de la sécurité : à ne pas ranger avec les deux autres, sa
  conséquence est une réponse dégradée, pas une action non voulue.

### La conception de l'outil, avec sa portée

- **Où elle agit** : à l'étape `schema` du
  [processus](../_processus/boucle-outils.md) — le schéma joint à la requête — et
  à l'étape `execution` pour le filtrage de la réponse.
- **À quelle fréquence** : le schéma part à **chaque requête** (il fait partie du
  prompt) ; le filtrage à chaque appel de l'outil.
- **Ce qu'elle propage** : un enum restreint contamine tout l'aval — un
  `entity_id` hors liste ne franchit pas le `dispatch`. Une réponse non filtrée,
  à l'inverse, évince l'historique et dégrade les tours suivants.
- **Ce qui l'annule** : une description vague (« contrôle la maison ») — le modèle
  tentera des services non prévus ; un enum absent — il inventera des identifiants
  d'entités. La description **énonce le périmètre exact**, sinon la garde de forme
  n'existe pas.

## Quand c'est la bonne réponse

**Deux outils séparés** (lire / agir) dès que la lecture et l'action ont des
niveaux de risque différents — c'est-à-dire dès qu'agir a un effet de bord. La
séparation au niveau du schéma est ce qui rend la décision différenciée du hook
possible.

**Un outil unique** seulement si tout ce qu'il fait est au même niveau de risque,
ce qui est rare pour un outil qui touche le monde physique.

**Énumérer les arguments** dès que l'ensemble des valeurs valides est fini et
connu — presque toujours pour des entités domotiques. Quand il ne l'est pas, la
liste blanche reste côté outil, mais on perd la garde au niveau du schéma.

## Ce qu'on ne saura pas faire

On n'a pas mesuré, sur ce homelab, la taille d'une réponse `GET /api/states`
brute face à la même filtrée — c'est ce chiffre qui justifierait quantitativement
le résumé côté outil.

Un piège reste à vérifier qu'on ne l'a pas commis : le **token admin « pour que
ça marche »**. Le jour où l'agent est injecté, l'injection est admin de la
maison — le rayon de dégât est tout ce que l'utilisateur du token peut faire.

Ce qui promouvrait cette leçon en « refaire » : une étape sous
`wiki/etapes/agent/` enregistrant `ha_lire` et `ha_agir` via `pi.registerTool`,
token d'un utilisateur HA dédié stocké hors du code, et un test réel — « quelle
température au salon ? » puis « allume la lampe du bureau » avec la validation
humaine visible.

## Se tester

1. Un seul outil `home_assistant` qui lit *et* agit, ou deux outils séparés ?
   Justifiez.
   *Réussi si* la réponse sépare `ha_lire` (allow) de `ha_agir` (ask), et voit
   que la séparation au niveau du schéma est ce qui permet au hook de décider
   différemment des deux.
2. Home Assistant ne scope pas finement ses tokens. Comment limite-t-on quand
   même le périmètre ?
   *Réussi si* la réponse cite les deux couches — utilisateur HA dédié non admin
   (ce que le token est) et liste blanche côté outil (ce que l'outil en fait) —
   et l'enum d'entités qui empêche le modèle d'en inventer une hors liste.
3. Pourquoi renvoyer le JSON brut de `GET /api/states` au modèle est-il une
   erreur, et de quel type ?
   *Réussi si* la réponse identifie un problème de **budget de contexte** — des
   milliers de tokens d'attributs inutiles évincent l'historique — et non de
   sécurité, et corrige en filtrant côté outil.

## À retenir

- Sur un outil qui agit, la conception de l'outil est déjà de la sécurité : le
  schéma restreint ce que le modèle peut demander avant que le hook ne décide.
- Le périmètre du token se construit en deux couches : utilisateur HA dédié non
  admin, plus liste blanche côté outil.
- Séparer lecture et action en deux outils est ce qui permet allow sur l'une et
  ask sur l'autre.
- Un `entity_id` en enum généré depuis la liste blanche empêche le modèle
  d'inventer une entité hors périmètre.
- Filtrer la réponse relève du budget de contexte, pas de la sécurité — à ne pas
  ranger avec les gardes.

## Références

- Documentation de l'API REST de Home Assistant — states, services, long-lived
  access tokens
- [architecture/jarvis.md du homelab](../../../../homelab/architecture/jarvis.md)
