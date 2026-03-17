# Chat CLI, historique et contexte

> [carte du cours](../carte.md) · étape : [`01_hello.py`](../../etapes/fondamentaux/01_hello.py)

## Où ça s'emboîte

- **Processus** : [d'un texte à un token](../_processus/generation-token.md)
- **L'étape ouverte** : `messages` — la liste côté client, renvoyée en entier à chaque tour et où le token généré est réinjecté

![[chat-historique-contexte.canvas]]

## Prérequis et suites

- **Suppose acquis** : rien du cours — c'est la première leçon du parcours. Un
  seul fait extérieur est nécessaire, et il se pose ici : une requête HTTP est
  **sans mémoire**. Le serveur traite ce qu'on lui envoie et oublie tout ; il
  n'existe aucun identifiant de session dans l'API de chat. Cette propriété
  ressert partout plus bas — c'est elle, et rien d'autre, qui rend le client
  responsable de l'historique.
- **Débloque** : [la tokenisation](tokenisation.md), qui donne l'unité dans
  laquelle le contexte se compte ; [le template de chat](template-de-chat.md),
  qui montre ce que devient la liste de messages avant d'atteindre le modèle ;
  [la boucle d'agent](boucle-agent.md), où le contexte enfle à l'intérieur d'un
  seul tour.

## L'essentiel

Un LLM est **stateless** : il ne se souvient de rien entre deux appels. « Avoir
une conversation » est une illusion reconstruite par le client — c'est *nous*
qui renvoyons l'historique entier à chaque tour, et le modèle qui reçoit à
chaque fois un texte qu'il découvre.

De ce fait unique découle tout le reste : le coût qui croît plus vite que la
conversation, la fenêtre qui finit par déborder, et le fait que la troncature
comme la compaction sont **notre** responsabilité, jamais celle du modèle.

Cette leçon ne couvre pas ce que coûte un token ni comment on le compte — c'est
[la tokenisation](tokenisation.md) — ni comment le serveur évite de recalculer
le préfixe qu'on lui renvoie, qui est
[attention et KV cache](attention-et-kv-cache.md).

## Le savoir

### Le format messages, et ce qu'il n'a pas

Une liste `[{role, content}]`, trois rôles : `system` pour le comportement,
`user`, `assistant`. L'API reçoit la liste complète et prédit le message
suivant. Il n'y a rien d'autre — pas d'identifiant de conversation, pas de
curseur, pas de « depuis le dernier appel ». Ce qui n'est pas dans la liste
n'existe pas.

C'est pourquoi la question « comment le modèle se souvient-il ? » n'a pas de
réponse : il ne se souvient pas. La pièce qui tient l'état est **la variable
Python côté client**, et elle est la seule.

### Le coût croît comme le carré du nombre de tours

Chaque tour renvoie tout le préfixe. Au tour *i*, on transmet donc l'équivalent
de *i* tours de texte. Le cumul sur *n* tours vaut 1 + 2 + … + n, soit
n(n+1)/2 — de l'ordre de n²/2. Doubler la longueur d'une conversation
quadruple à peu près le texte transmis depuis le début, alors que l'utilisateur
a l'impression d'avoir seulement parlé deux fois plus.

Ce n'est pas une mesure, c'est un calcul : il se redéduit du fait stateless
seul. Il explique à lui seul pourquoi
[le prompt caching](../inference/prompt-caching.md) existe, et pourquoi il vise
le **préfixe stable** plutôt que la fin de la conversation.

### Le streaming ne change pas ce qui est envoyé

En mode flux, la réponse arrive morceau par morceau — lignes NDJSON chez
Ollama, événements SSE chez les API cloud. La pièce qui décide du découpage
n'est ni le client ni le réseau : c'est le **serveur**, qui émet un objet par
token généré au moment où il le génère. Le client ne fait qu'accumuler.

Deux choses ne changent pas pour autant : la requête envoyée est la même, et le
coût aussi. Le streaming ne déplace que la **perception** — la latence du
premier token (TTFT) remplace l'attente de la réponse entière. Un chat qui
paraît deux fois plus rapide en flux a exactement le même débit total.

### Les deux réponses au débordement, avec leur portée

La fenêtre finit par être dépassée : system, historique, catalogue d'outils et
documents s'y empilent. Deux stratégies s'écrivent à la main, et elles ne
règlent pas le même problème.

**La troncature** — garder le message system, plus les *k* derniers messages.

- *Où elle agit* : côté client, sur la liste, juste avant l'envoi.
- *À quelle fréquence* : à chaque tour.
- *Ce qu'elle propage* : rien vers le modèle, qui n'a aucun moyen de savoir
  qu'on lui a retiré le début. Il répondra avec assurance sur un contexte
  amputé.
- *Ce qui l'annule* : une conversation plus courte que le seuil — la tranche
  reprend alors la liste entière, message system compris. C'est exactement le
  défaut trouvé à la promotion : reconcaténer le system devant une tranche qui
  le contient déjà le fait payer deux fois.

**La compaction** — résumer les anciens tours par un appel au modèle, et placer
le résumé en message system.

- *Où elle agit* : au même endroit, mais elle coûte **un appel au modèle**.
- *À quelle fréquence* : au franchissement d'un seuil, pas à chaque tour.
- *Ce qu'elle propage* : le résumé devient une source pour tous les tours
  suivants. Une erreur de résumé ne s'efface plus — elle est désormais du
  contexte, indistinguable du reste.
- *Ce qui l'annule* : un résumé qu'on redonne à résumer. Le résumé du résumé
  s'appauvrit à chaque passe, et la conversation dérive sans que rien ne le
  signale. La parade est structurelle : ne soumettre au modèle que les tours
  **nouveaux** depuis la dernière compaction, et transporter le résumé acquis à
  part.

« La compaction garde le sens » n'est pas une propriété, c'est une hypothèse à
vérifier : quelques questions de rappel posées avant et après — le fait du tour
2 survit-il ? — la transforment en constat. Sans ça, c'est une opinion.

### Compter, plutôt qu'estimer

Le modèle ne lit pas des mots, et aucune règle de trois sur les caractères ne
donne le bon compte. L'API rend les nombres exacts : `prompt_eval_count` et
`eval_count` chez Ollama, un par appel. Les afficher à chaque tour rend visible
la croissance quadratique décrite plus haut, au lieu de la laisser deviner.

## En pratique

[01_hello.py](../../etapes/fondamentaux/01_hello.py) : l'appel brut, sans
historique. Puis [02_chat.py](../../etapes/fondamentaux/02_chat.py) — la boucle
de chat et le compteur de tokens,
[03_stream.py](../../etapes/fondamentaux/03_stream.py) — le flux NDJSON, et
[05_contexte.py](../../etapes/fondamentaux/05_contexte.py) — `tronquer()` par
tranche, puis la compaction, avec la trace du résumé et son placement en
system.

**À prédire avant de lancer** :

- avec `01_hello.py`, on pose une question puis une seconde qui s'y réfère
  (« et en plus court ? »). Que répond le modèle, et pourquoi est-ce la bonne
  réponse de sa part ?
- dans `02_chat.py`, note `prompt_eval_count` aux tours 1, 2 et 3. La suite
  est-elle linéaire ? Écris ta prédiction chiffrée avant de regarder.
- dans `03_stream.py`, le total de tokens de la réponse est-il différent du
  mode non-flux ? Et le temps total ?
- dans `05_contexte.py`, lance une conversation assez longue pour déclencher
  deux compactions successives, puis pose une question sur le tout premier
  tour. Que reste-t-il ?

## Mesures

<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->

## Recomposer

**Ce que ça change à ce qu'on croyait savoir.** L'idée d'« assistant qui suit la
conversation » perd son sujet : il n'y a pas d'assistant qui suit, il y a une
liste qu'on renvoie. Ce déplacement a une conséquence immédiate sur la façon de
déboguer — devant un comportement bizarre, la première chose à regarder n'est
pas le modèle mais **la liste effectivement envoyée**, qui n'est presque jamais
celle qu'on croit.

**Ce qu'on peut prédire ailleurs.** Si le coût cumulé croît comme le carré du
nombre de tours et que rien n'est conservé côté serveur, alors toute
architecture qui multiplie les tours pour une seule tâche paiera ce carré sans
qu'un humain le voie passer. C'est déjà assez pour prédire deux choses avant
leurs leçons : qu'un [agent](boucle-agent.md) devra être borné en nombre de
tours autant qu'en tokens, et qu'un système qui injecte des documents dans le
prompt aura intérêt à les placer **après** le préfixe stable plutôt qu'avant,
faute de quoi il invalide à chaque tour tout ce qu'un
[cache de préfixe](../inference/prompt-caching.md) aurait pu réutiliser.

## Pièges connus

- **Rencontrés** :
  - *La troncature reprenait le message system en double.* Sur une conversation
    plus courte que le seuil, la tranche des k derniers messages contient déjà
    le system, qu'on reconcatène ensuite devant. Invisible à l'œil, immédiat
    dans un test à trois messages — trouvé en écrivant l'assertion, pas en
    relisant le script. Réflexe transférable : une fonction qui découpe se teste
    d'abord sur les entrées **plus petites que le découpage**.
  - *La compaction repartait de l'historique complet.* À la deuxième passe, le
    résumé précédent redevenait matière à résumer. La correction n'est pas un
    réglage mais un changement de structure : le résumé acquis est transporté à
    part.
- **Anticipés** — non vérifiés à ce jour :
  - *Deux causes pour « le bot a oublié le début ».* La troncature a retiré les
    messages, ou la compaction les a résumés en perdant le détail. Ce qui les
    sépare : lire le message system envoyé. S'il contient un résumé, c'est la
    seconde ; s'il est intact et que les tours anciens ont disparu, c'est la
    première.
  - *Deux causes pour « le bot a changé de ton ».* Le system a été jeté par la
    troncature, ou il a été **dilué** par un résumé qu'on lui a concaténé.
    Même symptôme, corrections opposées.
  - *Estimer les tokens avec `len(texte.split())`* — faux dès qu'il y a du
    code, des accents ou une autre langue. Les comptes de l'API sont gratuits.

## Se tester

1. Pourquoi l'API d'un LLM est-elle stateless, et qu'est-ce que ça implique
   pour votre application ?
   *Réussi si* la réponse nomme la conséquence économique — le préfixe est
   re-transmis et re-facturé — **et** la conséquence de responsabilité : la
   gestion du contexte est côté client, pas côté modèle.
2. Une conversation de 40 tours a coûté environ quatre fois plus de tokens
   cumulés qu'une conversation de 20 tours, à longueur de message égale.
   Est-ce attendu ? Justifiez sans invoquer de mesure.
   *Réussi si* la réponse refait le calcul n(n+1)/2 et conclut au facteur ~4,
   au lieu de répondre « oui, c'est connu ».
3. Vous ajoutez la compaction à un chat qui marchait. Les réponses deviennent
   subtilement moins bonnes au fil de la conversation, sans erreur visible.
   Quelle est l'hypothèse la plus probable, et quel test la confirme ?
   *Réussi si* la réponse cible la dérive cumulative — le résumé re-résumé — et
   propose un test de rappel sur un fait d'un tour ancien, pas une relecture du
   code.

## Ce que ça change dans le framework

C'est la leçon qui a ouvert [`src/framework/`](../../src/framework/README.md).
Deux briques en sont sorties :

- [`llm/ollama.py`](../../src/framework/llm/ollama.py) — l'appel et le flux. Ce
  que la promotion a changé : les comptes de tokens ne sont plus affichés puis
  perdus, ils remontent dans `Reponse`. Le fait économique de la leçon — chaque
  tour re-paye tout le préfixe — devient une donnée que l'appelant peut lire,
  au lieu d'une trace à l'écran.
- [`contexte.py`](../../src/framework/contexte.py) — `tronquer` et `compacter`.
  La compaction transporte le résumé acquis à part et ne soumet au modèle que
  les tours nouveaux : c'est le piège de dérive ci-dessus, corrigé dans la
  brique et non plus seulement signalé dans la prose.

Aucune interface de client n'a été écrite : un `Protocol` à une seule
implémentation décrirait Ollama, pas un contrat. Voir
[promotion](../framework/promotion.md).

## À retenir

- Le modèle ne se souvient de rien ; la pièce qui tient l'état est la liste
  `messages`, côté client.
- Le cumul des tokens croît comme n²/2 : doubler la conversation quadruple le
  texte transmis depuis le début.
- Le streaming change la perception, pas la requête ni le coût.
- Troncature et compaction ne règlent pas le même problème : l'une jette et ne
  coûte rien, l'autre résume et coûte un appel dont l'erreur devient du
  contexte définitif.
- Un résumé qu'on redonne à résumer dérive ; seul le transport à part de
  l'acquis l'évite.
- « Le résumé garde le sens » est une hypothèse tant qu'aucune question de
  rappel ne l'a vérifiée.

## Références

- Karpathy, « Intro to LLMs » — pour situer le modèle stateless dans
  l'ensemble
- Doc API Ollama : `/api/chat`, le streaming NDJSON, et les champs
  `prompt_eval_count` / `eval_count`
