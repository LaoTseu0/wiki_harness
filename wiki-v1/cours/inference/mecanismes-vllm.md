# Mécanismes vLLM

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [attention et KV cache](../fondamentaux/attention-et-kv-cache.md)
  — le cache, le prefill et le decode, dont cette leçon reprend la mécanique pour
  en tirer les conséquences côté serveur ; [la charge concurrente](charge-concurrente.md)
  — les courbes que ces mécanismes expliquent.
- **Débloque** : [l'analyse](analyse-et-verdict.md), qui exige de rattacher chaque
  cassure de courbe à l'un de ces mécanismes ; [le verdict](verdict-ollama-vs-vllm.md),
  dont les paramètres (concurrence, VRAM) sortent d'ici.

## L'essentiel

Trois mécanismes expliquent toutes les courbes du bench : le
**[KV cache](../fondamentaux/attention-et-kv-cache.md)** (pourquoi la mémoire est
le goulot), le **batching continu** (pourquoi vLLM encaisse la concurrence) et
**PagedAttention** (pourquoi vLLM loge plus de requêtes dans la même VRAM).
Savoir les raconter, c'est la différence entre *constater* un écart de
performance et l'*expliquer*.

La thèse, celle qu'on voit rater le plus souvent : ces trois mécanismes agissent
sur des grandeurs **différentes**, et les confondre mène à un mauvais
diagnostic. PagedAttention optimise la *capacité* mémoire ; la réactivité sous
charge vient du batching continu ; la stabilité du débit vient du decode borné
mémoire. Attribuer tout à un seul, c'est se tromper de correction.

Cette leçon ne redonne pas le mécanisme de base du KV cache — il est aux
[fondamentaux](../fondamentaux/attention-et-kv-cache.md) — ni la façon de tracer
les courbes, qui est [la charge concurrente](charge-concurrente.md).

## Le savoir

### KV cache : ce que le serving en fait

Le mécanisme — relire en VRAM les clés/valeurs du passé au lieu de les
recalculer — est celui des fondamentaux. Ce que le *serving* y ajoute, et que la
leçon de fond ne chiffrait pas :

- le decode est borné par la **bande passante mémoire** (relire le cache à chaque
  token) — d'où des tokens/s stables tant que la bande passante n'est pas
  partagée ;
- chaque requête active occupe `2 (K et V) × couches × têtes_KV × dim_tête ×
  tokens × taille du type (2 octets en fp16)` — têtes **KV**, pas têtes
  d'attention : avec le GQA (Qwen3 en est), elles sont 4 à 8× moins nombreuses,
  et compter les têtes d'attention surestime le cache d'autant. La VRAM
  disponible **est** la capacité en concurrence ([vLLM sur RTX 2060](vllm-sur-rtx-2060.md)) ;
- même mécanique que le [prompt caching](prompt-caching.md) — ici intra-requête,
  là inter-requêtes.

### Batching continu : ordonnancer par itération, pas par lot

Le batching naïf attend que le lot entier finisse : le lot avance au rythme de sa
requête la plus lente, et une requête arrivée en retard attend le prochain lot.
vLLM ordonnance **par itération** — à chaque pas de génération, les séquences
finies sortent et les nouvelles entrent immédiatement dans le lot en cours.

La conséquence est exactement la forme des courbes : le débit **agrégé** grimpe
avec la concurrence, sans que le TTFT explose, parce qu'une requête neuve n'attend
pas la fin des autres pour commencer. C'est ce mécanisme, et non PagedAttention,
qui produit la tenue de charge ([charge concurrente](charge-concurrente.md)).

### PagedAttention : la mémoire virtuelle appliquée au cache

Allouer le KV cache d'une requête en un bloc contigu, dimensionné à la longueur
maximale possible, gaspille la VRAM : une requête courte réserve autant qu'une
longue, et l'espace entre les blocs se fragmente. vLLM découpe le cache en
**pages** de taille fixe, allouées à la demande — l'idée de la mémoire virtuelle
des systèmes d'exploitation, portée à l'attention.

Résultat : fragmentation quasi nulle, donc plus de requêtes simultanées logées
dans les mêmes 6 Go. C'est un optimiseur de **capacité**, pas de réactivité —
distinction qui décide du diagnostic ci-dessous.

### Lire les courbes, mécanisme par mécanisme

Chaque trait des courbes se rattache à un mécanisme précis :

- le **mur d'Ollama** à forte concurrence = file d'attente, faute de batching
  continu ;
- l'**érosion douce** de vLLM = partage de la bande passante mémoire entre
  requêtes actives (le decode borné mémoire) ;
- la **cassure** de vLLM à *n* élevé = KV cache saturé, préemptions de séquences
  pour en admettre d'autres.

### L'erreur d'attribution, et ce qui la corrige

Le symptôme est un seul — « vLLM tient mieux la charge » — et la tentation est de
tout mettre sur PagedAttention parce que c'est le nom le plus mémorable. C'est
faux, et la faute coûte cher en diagnostic :

- la **réactivité** sous charge (le TTFT qui ne s'effondre pas) vient du
  **batching continu** ;
- la **capacité** (le nombre de requêtes logées) vient de **PagedAttention** ;
- la **stabilité** du débit par requête vient du **decode borné mémoire**.

Ce qui les distingue : demander *quelle grandeur bouge*. Si c'est le TTFT sous
charge, c'est le batching ; si c'est le nombre de requêtes avant saturation,
c'est PagedAttention ; si c'est les tokens/s d'une requête isolée, c'est la bande
passante. Trois mécanismes, trois effets, trois corrections.

## Quand c'est la bonne réponse

**Invoquer le batching continu** pour expliquer pourquoi la réactivité tient sous
charge — jamais pour expliquer combien de requêtes rentrent.

**Invoquer PagedAttention** pour expliquer la capacité mémoire — jamais pour
expliquer la tenue du TTFT.

**Invoquer le decode borné mémoire** pour expliquer la stabilité, et l'érosion,
du débit par requête — c'est le mécanisme qu'on oublie parce qu'il n'a pas de nom
de produit.

## Ce qu'on ne saura pas faire

Les courbes n'ont pas été produites : le rattachement de chaque cassure à son
mécanisme est une **prédiction**, pas une lecture de figures réelles. On sait
quel mécanisme *devrait* expliquer quel trait ; on ne l'a pas encore vérifié sur
des logs, notamment les préemptions qui signeraient la saturation du cache.

Ce que ça laisse ouvert : sur une carte Turing de 6 Go, il est possible que le
cache sature avant que le batching n'ait montré son plein effet — auquel cas
c'est PagedAttention et la capacité, plus que le batching, qui domineraient
l'histoire. L'ordre d'apparition des trois effets est une question empirique.

Ce qui promouvrait cette leçon en « refaire » : les courbes du bench annotées à
la main, une flèche par mécanisme, et la confirmation dans les logs de vLLM que
la cassure de débit coïncide bien avec les préemptions.

## Se tester

1. « Pourquoi vLLM tient-il la charge là où Ollama fait la queue ? » Quels
   mécanismes citez-vous, et lequel n'a *rien* à voir avec la réactivité ?
   *Réussi si* la réponse cite le batching continu (insertion par itération vs
   file) pour la réactivité et le decode borné mémoire pour le débit, et écarte
   PagedAttention de la réactivité — c'est un optimiseur de capacité.
2. On vous dit que le débit agrégé par requête *augmente* grâce au batching.
   Qu'est-ce qui cloche ?
   *Réussi si* la réponse corrige : le batching augmente le débit *agrégé*, mais
   par requête les tokens/s baissent légèrement (partage de bande passante).
3. La courbe de débit de vLLM casse à forte concurrence. À quel mécanisme
   rattachez-vous la cassure, et où le vérifiez-vous ?
   *Réussi si* la réponse pointe le KV cache saturé et les préemptions, et va les
   chercher dans les logs/métriques de vLLM.

## À retenir

- Trois mécanismes, trois grandeurs : batching continu → réactivité,
  PagedAttention → capacité, decode borné mémoire → stabilité du débit.
- Le mécanisme de base du KV cache est aux fondamentaux ; le serving y ajoute la
  bande passante, la formule VRAM (têtes KV, GQA) et la capacité = concurrence.
- Le batching continu ordonnance par itération : le débit agrégé monte sans faire
  exploser le TTFT.
- PagedAttention est la mémoire virtuelle appliquée au cache : fragmentation
  nulle, plus de requêtes dans la même VRAM.
- L'erreur d'attribution — tout mettre sur PagedAttention — se corrige en
  demandant quelle grandeur bouge.

## Références

- Kwon et al., « Efficient Memory Management for LLM Serving with PagedAttention »
  — le papier vLLM, pour PagedAttention et le batching continu
- [Attention et KV cache](../fondamentaux/attention-et-kv-cache.md) — le mécanisme
  de base dont cette leçon tire les conséquences serveur
