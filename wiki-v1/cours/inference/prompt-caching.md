# Prompt caching

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [chat, historique et contexte](../fondamentaux/chat-historique-contexte.md)
  — que le modèle est stateless et que chaque appel renvoie donc tout le
  préfixe ; [attention et KV cache](../fondamentaux/attention-et-kv-cache.md) —
  le KV cache et le prefill, dont le prompt caching n'est que la réutilisation
  d'une requête à l'autre. Cette dernière propriété porte toute la leçon.
- **Débloque** : la viabilité économique d'un agent qui boucle avec un gros
  prompt système ; le réglage d'architecture *stable devant, variable derrière*
  que toute construction de prompt devra respecter.

## L'essentiel

Chaque appel re-paie tout le préfixe — system, outils, exemples — vu en
[chat, historique et contexte](../fondamentaux/chat-historique-contexte.md). Le
prompt caching évite de **recalculer ce préfixe stable** : le serveur conserve
l'état interne ([KV cache](../fondamentaux/attention-et-kv-cache.md)) du début du
prompt et ne retraite que ce qui change. Pour un agent qui boucle avec le même
prompt système, c'est l'économie dominante.

La thèse à retenir tient à une condition brutale : le cache marche par **préfixe
exact**. Un seul octet changé au début invalide tout ce qui suit — d'où une règle
d'architecture non négociable, *stable au début, variable à la fin*. Et une
frontière à ne pas franchir : ce n'est **pas** un cache de réponses. Le prefill
est économisé, la génération reste payée et reste probabiliste.

Cette leçon ne redonne pas le mécanisme du KV cache — il est aux
[fondamentaux](../fondamentaux/attention-et-kv-cache.md) — ni le choix du backend
qui l'assure, qui relève des [providers](../framework/providers.md).

## Le savoir

### Ce qui est caché, et pourquoi c'est la partie chère

Ce qui est caché : les clés/valeurs du préfixe. Leur re-calcul est précisément la
phase chère — le **prefill**
([attention et KV cache](../fondamentaux/attention-et-kv-cache.md)) ; les
réutiliser fait passer le coût du préfixe à ~0. Le gain n'est donc pas marginal :
il porte sur la phase la plus coûteuse d'un appel à long préambule, et il croît
avec la longueur du préfixe stable.

### Le préfixe exact est un levier, avec sa portée

- **Où il agit** : sur la partie initiale du prompt, celle que deux appels
  successifs partagent caractère pour caractère.
- **À quelle fréquence** : à chaque appel — le cache est consulté au tout début
  du prefill.
- **Ce qu'il propage** : le bénéfice se propage à tout ce qui suit le dernier
  caractère commun, et s'arrête net au premier caractère qui diffère. Le cache
  est un préfixe, pas un ensemble : il ne rattrape rien après la première
  divergence.
- **Ce qui l'annule** : un seul octet variable placé tôt. Un horodatage ou un
  identifiant de session dans le prompt système invalide le cache **à chaque
  appel**, silencieusement, et transforme une économie en coût plein permanent.

C'est ce levier qui impose la règle *stable devant, variable derrière* : mettre
en tête ce qui ne bouge pas (system, outils, exemples), en queue ce qui varie
(question, contexte du tour).

### Trois incarnations, une même mécanique

- **API cloud** (Claude : `cache_control`) : des points de cache explicites, le
  préfixe relu facturé à tarif réduit, un TTL limité — le taux exact se lit dans
  la grille du fournisseur et bouge.
- **Serveurs locaux** : Ollama n'a pas de « session » — `keep_alive` garde le
  modèle et son runner chargés, et le runner réutilise le KV du **dernier prompt
  traité** si le nouveau partage son préfixe. vLLM fait de l'*automatic prefix
  caching* multi-requêtes. Même mécanique, gratuite, bornée par la VRAM.
- **Multi-tours** : la conversation entière est un préfixe croissant — le cache
  transforme des coûts cumulés en O(n²) en ~O(n).

### Pourquoi le caching rend les agents viables

Un agent qui fait 30 tours avec 2 000 tokens de system et d'outils re-paierait,
sans cache, 30 × 2 000 = 60 000 tokens de prefill rien que pour le préambule
stable. Le caching ramène ce coût au premier tour seul. Ce n'est pas une
optimisation de confort : c'est ce qui fait la différence entre un agent qu'on
peut faire boucler et un agent dont chaque tour re-facture tout son harnais.

### Deux causes pour « le cache ne prend pas »

Symptôme identique — le TTFT reste froid appel après appel, aucun gain — et deux
origines distinctes :

- **Le préfixe change.** Un élément variable est placé tôt — horodatage,
  identifiant, outils sérialisés dans un ordre non déterministe (un dict non
  trié). Le préfixe exact est rompu à chaque appel. Correction : figer et
  sérialiser canoniquement le début du prompt.
- **Le cache est évincé.** Sur un serveur qui ne garde que le dernier prompt
  (Ollama), un appel intercalé au préfixe différent chasse le KV précédent — deux
  clients qui alternent s'évincent mutuellement. Correction : le préfixe est
  stable, mais le voisinage le détruit ; il faut un cache multi-requêtes (vLLM)
  ou éviter l'entrelacement.

Ce qui les distingue : envoyer deux fois le **même** prompt sans rien intercaler.
Si le second est chaud, le préfixe est bon et le problème était l'éviction ; s'il
reste froid, c'est le préfixe qui varie.

## Quand c'est la bonne réponse

**Compter sur le caching** quand un long préfixe stable se répète — une boucle
d'agent, un préambule figé, un few-shot réutilisé. C'est là que le gain est
maximal.

**Ne pas y compter** quand le début du prompt change à chaque appel : le gain est
alors nul par construction, et aucun réglage ne le récupère tant que la variable
est en tête.

**Ne pas le confondre avec un cache de réponses** : on économise le prefill, pas
la génération. Attendre d'un prompt caché une réponse identique ou gratuite est
une erreur de nature — la sortie reste tirée à chaque fois.

## Ce qu'on ne saura pas faire

L'exercice de chronométrage n'a pas tourné : aucun TTFT froid contre chaud n'a
été relevé dans ce dépôt, et l'asymétrie début/fin de prompt n'a pas été observée
ici — seulement déduite du mécanisme du préfixe exact. Les 60 000 tokens de
l'exemple sont un calcul, pas une mesure.

Ce que ça laisse ouvert : de combien le TTFT chute réellement entre froid et
chaud sur le modèle local, et à partir de quelle longueur de préfixe le gain
devient sensible — deux questions qui ne se répondent qu'en chronométrant.

Ce qui promouvrait cette leçon en « refaire » : une étape sous `etapes/inference/`
qui envoie deux fois un prompt d'environ 2 000 tokens à Ollama (modèle chargé,
sans client concurrent) et mesure TTFT froid vs chaud ; puis fait varier un mot
au début contre à la fin pour voir l'asymétrie ; puis intercale un prompt
différent pour constater l'éviction.

## Se tester

1. Un agent boucle avec un prompt système contenant l'heure courante en tête.
   Ses coûts ne baissent pas malgré le prompt caching activé. Pourquoi, et que
   corrigez-vous ?
   *Réussi si* la réponse identifie l'horodatage en tête comme rupture du préfixe
   exact à chaque appel, et déplace le variable en fin de prompt.
2. Le même prompt envoyé deux fois de suite est chaud au second envoi, mais dès
   qu'un autre client s'intercale il redevient froid. Quelle est la cause, et sur
   quel type de serveur ?
   *Réussi si* la réponse cite l'éviction par le dernier-prompt sur un serveur
   mono-slot (Ollama), et propose un cache multi-requêtes (vLLM) ou l'absence
   d'entrelacement.
3. On vous demande de réduire le coût d'un agent qui fait 50 appels avec le même
   prompt système. Par quoi commencez-vous, et qu'écartez-vous ?
   *Réussi si* la réponse commence par le prompt caching (préfixe stable en tête,
   points de cache ou serveur à prefix caching, TTFT mesuré avant/après) avant de
   discuter compaction ou modèle plus petit — et ne confond pas avec un cache de
   réponses.

## À retenir

- Le prompt caching réutilise le KV cache du préfixe : il économise le prefill,
  la phase chère, pas la génération, qui reste payée et probabiliste.
- Il marche par préfixe exact : un octet variable en tête l'annule à chaque
  appel — d'où *stable devant, variable derrière*.
- Trois incarnations, une mécanique : points de cache d'API cloud, prefix caching
  des serveurs locaux, préfixe croissant des multi-tours (O(n²) → O(n)).
- C'est ce qui rend un agent viable : sans lui, chaque tour re-facture tout le
  harnais système.
- « Le cache ne prend pas » a deux causes — préfixe qui varie, ou éviction par un
  prompt intercalé — que le double envoi sans intercalation sépare.

## Références

- Doc prompt caching de la Claude API (`cache_control`) — points de cache
  explicites, tarif réduit, TTL
- vLLM, « Automatic Prefix Caching » — la version locale, gratuite, multi-requêtes
- [Attention et KV cache](../fondamentaux/attention-et-kv-cache.md) — le prefill
  et le KV cache que le caching réutilise
