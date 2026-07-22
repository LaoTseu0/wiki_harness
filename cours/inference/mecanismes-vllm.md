# Mécanismes vLLM

> [carte du cours](../carte.md)

## L'essentiel

Trois mécanismes expliquent toutes les courbes du bench : le **KV
cache** (pourquoi la mémoire est le goulot), le **batching continu**
(pourquoi vLLM encaisse la concurrence) et **PagedAttention**
(pourquoi vLLM loge plus de requêtes dans la même VRAM). Savoir les
raconter est exactement ce que la [roadmap](../_archive/roadmap.md) appelle
« expliquer les résultats ».

## Le savoir

- **KV cache** : à chaque token généré, l'attention relit les
  représentations clés/valeurs de *tous* les tokens précédents ; on
  les garde en VRAM plutôt que les recalculer. Conséquences :
  - le decode est borné par la **bande passante mémoire** (relire le
    cache) — d'où des tokens/s stables ;
  - chaque requête active occupe `2 (K et V) × couches × têtes_KV ×
    dim_tête × tokens × taille du type (2 octets en fp16)` — têtes
    **KV**, pas têtes d'attention : avec le GQA (Qwen3 en est), elles
    sont 4-8× moins nombreuses, et compter les têtes d'attention
    surestime le cache d'autant. La VRAM disponible **est** la
    capacité en concurrence
    ([4.1.1](vllm-sur-rtx-2060.md)) ;
  - même mécanique que le [prompt caching](../glossaire/prompt-caching.md) —
    ici intra-requête, là inter-requêtes.
- **Batching continu** (continuous batching) : le batching naïf attend
  que le lot entier finisse — le batch avance au rythme du plus lent.
  vLLM ordonnance **par itération** : à chaque pas de génération, les
  séquences finies sortent, les nouvelles entrent immédiatement. C'est
  ce qui fait grimper le débit agrégé sans faire exploser le TTFT
  ([4.2.2](charge-concurrente.md)).
- **PagedAttention** : allouer le KV cache en bloc contigu par requête
  (à la taille max possible) gaspille la VRAM en fragmentation. vLLM
  le découpe en **pages** de taille fixe allouées à la demande —
  l'idée de la mémoire virtuelle des OS appliquée à l'attention.
  Fragmentation quasi nulle → plus de requêtes simultanées dans les
  mêmes 6 Go.
- **La lecture des courbes** : le mur d'Ollama à n=5+ = file d'attente
  (pas de batching continu) ; l'érosion douce de vLLM = partage de la
  bande passante ; la cassure vLLM à n élevé = KV cache saturé
  (préemptions).

## En pratique

Annoter les courbes du bench mécanisme par mécanisme (une flèche =
une explication) — l'exercice force la compréhension et produit les
figures du post ([4.3.2](verdict-ollama-vs-vllm.md)).

## Pièges connus

- Réciter les mécanismes sans les relier aux courbes : l'entretien
  vérifie le lien mesure ↔ mécanisme, pas le vocabulaire.
- Croire que le batching augmente les tokens/s *par requête* : il
  augmente le débit *agrégé* — par requête, ça baisse légèrement
  (partage de bande passante).
- Attribuer tout à PagedAttention : c'est un optimiseur de *capacité*
  mémoire ; la réactivité sous charge vient du batching continu — deux
  mécanismes, deux effets.

## Se tester

> « Pourquoi vLLM tient-il la charge là où Ollama fait la queue ? »
> Batching continu (insertion par itération vs file), PagedAttention
> (KV cache paginé, fragmentation nulle → plus de requêtes en VRAM),
> et decode borné mémoire (le débit se partage) — courbes du bench à
> l'appui.

## Références

- Kwon et al., « Efficient Memory Management for LLM Serving with
  PagedAttention » (le papier vLLM)
- [Roadmap couche 1](../_archive/roadmap.md) — débit vs latence, KV cache
