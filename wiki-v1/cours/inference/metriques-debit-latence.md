# Débit et latence

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [un benchmark honnête](benchmark.md) — que les métriques
  se fixent avant de mesurer et voyagent avec leurs conditions ; cette leçon
  choisit *lesquelles*. [Attention et KV cache](../fondamentaux/attention-et-kv-cache.md)
  — le découpage prefill/decode, qui est ce que ces métriques mesurent chacune
  d'un côté.
- **Débloque** : [la charge concurrente](charge-concurrente.md), qui fait
  diverger celle des trois métriques que la concurrence révèle — le débit
  agrégé.

## L'essentiel

Deux familles de métriques, deux expériences utilisateur distinctes : la
**latence du premier token** (TTFT — le chat « répond vite ») et le **débit de
génération** (tokens/s — la réponse « s'écrit vite »). Les confondre rend tout
benchmark illisible, parce qu'un serveur peut exceller à l'une et décevoir à
l'autre.

La thèse à retenir : ces deux métriques par requête ne suffisent pas. La
grandeur qui décide sous charge est une **troisième**, le débit *agrégé*, que ni
l'une ni l'autre ne montre — une flotte de requêtes lentes individuellement peut
produire un excellent débit total. Mesurer la mauvaise des trois est la façon la
plus commune de conclure de travers.

Cette leçon ne redonne pas le mécanisme prefill/decode — il est aux
[fondamentaux](../fondamentaux/attention-et-kv-cache.md) — ni la façon de
fabriquer la charge, qui est [la charge concurrente](charge-concurrente.md).

## Le savoir

### Chaque phase se lit dans une métrique

Les deux phases d'une requête ([attention et KV cache](../fondamentaux/attention-et-kv-cache.md))
se projettent chacune sur une métrique, et c'est ce qui les rend mesurables
séparément :

- le **prefill** — lire tout le prompt d'un bloc, borné par le calcul —
  détermine le **TTFT** : le temps jusqu'au premier token ;
- le **decode** — produire les tokens un par un, borné par la bande passante
  mémoire — détermine les **tokens/s de génération**.

Cette correspondance n'est pas décorative : elle dit *où* agir. Un TTFT
mauvais est un problème de prefill (prompt trop long, pas de cache de préfixe) ;
un débit de génération mauvais est un problème de decode (bande passante, taille
du modèle). Diagnostiquer sans séparer les deux, c'est soigner au hasard.

### Les métriques à collecter, et la grandeur système

Par requête, trois chiffres, horodatés sur le flux :

- **TTFT** — de l'envoi au premier morceau du stream ;
- **tokens/s de génération** — tokens générés ÷ (dernier token − premier token),
  le premier token *exclu* du dénominateur ;
- **latence totale** — pour l'expérience de bout en bout.

Et côté système, la métrique que les précédentes ne contiennent pas : le **débit
agrégé** — tokens/s toutes requêtes confondues. C'est elle qui mesure la
*capacité* du serveur, et c'est elle que la concurrence fera diverger d'un moteur
à l'autre.

### La discipline statistique : la queue, pas la moyenne

Une moyenne seule ment sur l'expérience réelle, parce qu'elle dilue les cas
lents dans les cas rapides. Or c'est le cas lent que l'utilisateur ressent :
personne ne vit la moyenne, on vit sa propre requête, et une sur vingt suffit à
donner l'impression d'un service lent.

D'où la règle : **médiane et p95**, jamais la moyenne seule. Le p95 — le seuil
que 95 % des requêtes battent — est la mesure de la queue, celle qui décrit le
pire ordinaire. Avec, deux garde-fous mécaniques : au moins une dizaine de
mesures par point pour que le p95 signifie quelque chose, et le warm-up exclu —
le premier appel inclut le chargement du modèle chez Ollama et n'est pas
représentatif.

### Les conditions à figer, chacune pour une raison

[Publier les conditions](benchmark.md) est la règle ; voici la liste et pourquoi
chaque élément y est :

- **même modèle et quantisation notée** (AWQ vs GGUF, [vLLM sur RTX 2060](vllm-sur-rtx-2060.md))
  — un format change la qualité et la vitesse ;
- **même longueur de prompt** — le TTFT en dépend directement, et les templates
  de chat diffèrent d'un moteur à l'autre : compter les tokens du prompt *rendus
  par chaque API*, pas les caractères ;
- **même `max_tokens`** — le decode s'arrête sinon à des longueurs différentes ;
- **température fixée** et **un seul moteur sur le GPU** — sinon on mesure le
  bruit de tirage et le partage de VRAM en plus du moteur.

### Deux causes pour un débit de génération qui semble mauvais

Symptôme identique — les tokens/s sont bas — et deux origines :

- **La mesure est contaminée.** Le TTFT est compté dans le dénominateur : le
  temps d'attente du premier token écrase le débit réel de génération. Les deux
  métriques se mélangent. Correction : séparer les phases dans le calcul.
- **Le decode est réellement lent.** Le modèle est gros, ou la bande passante
  saturée. Correction : c'est un problème d'inférence, pas de mesure.

Ce qui les distingue : recalculer les tokens/s en excluant le TTFT du
dénominateur. Si le chiffre remonte, c'était la contamination ; s'il reste bas,
le decode est en cause.

## Quand c'est la bonne réponse

**Mesurer le TTFT** quand l'usage est interactif — un chat, un assistant. C'est
l'attente perçue, et elle prime sur le débit.

**Mesurer le débit agrégé** quand la question est la capacité — combien
d'utilisateurs la carte tient. Les métriques par requête ne répondent pas à
cette question.

**Toujours médiane et p95, jamais la moyenne seule** — dès qu'il y a une queue,
et il y en a toujours une sous charge. Une moyenne suffit uniquement à décrire un
tirage sans conséquence, ce qui n'arrive pas ici.

## Ce qu'on ne saura pas faire

Aucune de ces métriques n'a été relevée dans ce dépôt : le module de mesure
n'est pas écrit, et les valeurs de TTFT ou de débit restent à produire. Cette
leçon dit quoi collecter et comment le traiter, pas ce que ça donne.

Ce que ça laisse ouvert : combien de mesures par point rendent le p95 stable sur
cette carte, et si la variance à forte concurrence exige davantage de salves —
deux questions qui ne se répondent qu'en voyant la dispersion réelle.

Ce qui promouvrait cette leçon en « refaire » : le module de mesure sous
`etapes/inference/`, produisant par requête un JSON brut (rejouable sans
re-mesurer) et, à part, les agrégats médiane/p95 — avec leurs conditions.

## Se tester

1. Un serveur affiche un excellent débit de génération par requête mais les
   utilisateurs trouvent le chat lent à démarrer. Quelle métrique regardez-vous,
   et pourquoi les deux ne se contredisent pas ?
   *Réussi si* la réponse va au TTFT (prefill), et distingue « répond vite » de
   « s'écrit vite » — deux phases, deux métriques.
2. On vous donne « 30 tokens/s » comme preuve qu'un moteur est rapide. Quelles
   deux choses exigez-vous avant d'y croire ?
   *Réussi si* la réponse réclame les conditions (au moins modèle/quantisation,
   longueur de prompt, concurrence) **et** une médiane + p95 plutôt qu'un chiffre
   nu.
3. Le débit de génération mesuré est étonnamment bas. Quelle erreur de mesure
   vérifiez-vous en premier ?
   *Réussi si* la réponse soupçonne le TTFT inclus dans le dénominateur et
   propose de recalculer en l'excluant avant d'accuser le moteur.

## À retenir

- TTFT et débit de génération sont deux expériences (répondre vite, s'écrire
  vite) et se projettent sur prefill et decode : un serveur peut exceller à l'une
  et décevoir à l'autre.
- La grandeur qui décide sous charge est le débit *agrégé*, qu'aucune métrique
  par requête ne montre.
- Médiane et p95, jamais la moyenne seule : on ne vit pas la moyenne, on vit sa
  propre requête, et le p95 décrit le pire ordinaire.
- Chaque condition publiée a une raison : longueur de prompt pour le prefill,
  `max_tokens` pour le decode, un moteur à la fois pour ne pas mesurer le partage
  de VRAM.

## Références

- [Attention et KV cache](../fondamentaux/attention-et-kv-cache.md)
  — prefill/decode, le mécanisme que ces métriques mesurent
- [Mécanismes vLLM](mecanismes-vllm.md)
  — pourquoi le decode est borné par la bande passante
- Doc métriques vLLM (`/metrics`, Prometheus) — pour croiser nos mesures avec
  celles qu'expose le moteur
