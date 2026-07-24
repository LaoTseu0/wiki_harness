# vLLM sur RTX 2060

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [servir un modèle](deploiement.md) — le budget
  `VRAM = poids + KV cache + activations`, et que la place laissée au cache
  après les poids est la capacité de concurrence. Toute cette leçon règle ce
  curseur. [Les providers](../framework/providers.md) — l'API
  OpenAI-compatible, qui est ce qui rend vLLM substituable à Ollama.
- **Débloque** : [la charge concurrente](charge-concurrente.md), qui met sous
  pression le cache dimensionné ici ; [les mécanismes vLLM](mecanismes-vllm.md),
  qui expliquent *pourquoi* ces réglages produisent la tenue de charge.

## L'essentiel

vLLM est le serveur d'inférence des offres « LLM infra » : conçu pour servir
**N utilisateurs concurrents** sur GPU (batching continu, PagedAttention —
[mécanismes vLLM](mecanismes-vllm.md)). Le défi assumé ici est de le faire tenir
sur une RTX 2060 de 6 Go, une carte de 2019 — contrainte qui force à
comprendre chaque mégaoctet.

La thèse à retenir n'est pas « voici les flags de vLLM ». C'est que **ces flags
ne sont pas des boutons de confort : chacun déplace l'arbitrage poids/cache** du
[budget VRAM](deploiement.md), et l'un d'eux — `--max-model-len` — multiplie la
concurrence possible sans changer de modèle, en rétrécissant le cache que chaque
requête réclame.

Cette leçon ne couvre pas les mécanismes internes qui rendent le batching
efficace — c'est [mécanismes vLLM](mecanismes-vllm.md) — ni la mesure de ce que
tout cela donne sous charge, qui est [la charge concurrente](charge-concurrente.md).

## Le savoir

### La préallocation change ce que « rentrer dans la carte » veut dire

Contrairement à Ollama qui charge à la demande ([servir un modèle](deploiement.md)),
vLLM **réserve au démarrage** la fraction de VRAM qu'on lui accorde et y
préalloue le KV cache. Conséquence directe et contre-intuitive : un modèle dont
les poids « rentrent » largement dans 6 Go peut faire échouer le démarrage, parce
que le cache réservé s'ajoute aux poids *avant* la première requête. « Ça
rentre » ne se juge pas sur les poids seuls, mais sur poids + cache préalloué.

### Les flags sont des leviers sur le budget, pas des réglages de confort

Le levier qu'il faut vraiment comprendre est `--max-model-len` (longueur de
contexte maximale). Sa portée :

- **Où il agit** : au dimensionnement du KV cache par requête, à la construction
  du moteur.
- **À quelle fréquence** : une fois, au démarrage — il fixe la taille d'une
  place de cache pour toute la vie du serveur.
- **Ce qu'il propage** : tout le reste. Diviser la longueur max par deux
  double (à VRAM égale) le nombre de requêtes simultanées logeables, car chaque
  place de cache est deux fois plus petite. C'est le flag qui achète de la
  concurrence sans toucher au modèle.
- **Ce qui l'annule** : le régler au-delà du besoin réel. Une longueur max de
  32 000 « au cas où » réserve des places de cache géantes dont chaque requête
  n'utilise qu'une fraction — la concurrence s'effondre pour un contexte que
  personne n'atteint.

Les trois autres, plus brièvement, chacun sur le même budget :

- `--gpu-memory-utilization` (≈ 0,90) : la fraction de VRAM que vLLM s'autorise
  et dans laquelle il préalloue le cache. La monter grignote la marge système ;
  la baisser réduit la concurrence.
- `--quantization awq` (ou un modèle pré-quantisé GPTQ/AWQ) : agit sur le poste
  *poids*, donc sur ce qui reste pour le cache.
- `--max-num-seqs` : le plafond de séquences dans un lot — la borne haute de la
  concurrence, à ne pas confondre avec ce que le cache peut réellement tenir.

### Deux causes pour un OOM au démarrage

Le symptôme est identique — le serveur refuse de démarrer, mémoire insuffisante
— et les deux corrections sont opposées :

- **Le cache préalloué ne tient pas.** Les poids rentrent, mais la place réservée
  au cache (fonction de `max-model-len` et `gpu-memory-utilization`) déborde. La
  correction ne touche pas au modèle : baisser l'un de ces deux flags.
- **Les poids eux-mêmes sont trop gros.** Même sans cache, le modèle ne rentre
  pas. La correction est de changer de modèle ou de quantisation.

Ce qui les distingue : regarder l'occupation juste après le chargement des poids,
avant l'allocation du cache — vLLM la journalise au démarrage. Si les poids
passent et que l'échec vient après, c'est le cache ; s'ils ne passent pas, c'est
le modèle. Confondre les deux fait perdre du temps à changer de modèle quand il
suffisait de baisser une longueur de contexte.

### La quantisation n'est pas neutre, et ça se mesure

Comparer vLLM servant un modèle AWQ à Ollama servant le même modèle en GGUF
q4_K_M, c'est comparer deux formats de quantisation *proches mais pas
identiques*. L'écart de qualité qui en résulte ne se règle pas par une note de
bas de page « les formats diffèrent » : il se **mesure**, en rejouant le jeu
d'[evals du domaine retrieval](../retrieval/evals.md) sur les deux moteurs via le
[backend commutable](../framework/providers.md). L'écart devient alors une ligne
de tableau, pas une réserve verbale.

## Quand c'est la bonne réponse

**Régler ces flags finement** quand la VRAM est le facteur limitant — c'est le
cas d'une petite carte. Sur 6 Go, chaque flag compte ; sur 24 Go, la plupart se
laissent au défaut.

**Passer du temps sur `--max-model-len`** dès que la concurrence est l'objectif :
c'est le seul réglage qui l'augmente sans dégrader la qualité. Le dimensionner à
l'usage réel, pas au maximum théorique.

**Ne pas déployer vLLM du tout** pour un usage mono-usager : la préallocation
monopolise la carte pour une concurrence dont personne ne profite, et Ollama
rend alors la carte partageable ([servir un modèle](deploiement.md)).

## Ce qu'on ne saura pas faire

Aucune étape n'existe sous `etapes/inference/` : le conteneur vLLM n'a pas été
lancé dans ce dépôt, et aucune occupation n'a été lue à `nvidia-smi`. Les
tailles de VRAM citées sont des faits matériels et des calculs de poids
quantisés, pas des relevés — l'occupation réelle du cache, elle, reste à mesurer.

Ce que ça laisse ouvert : quel modèle 3B précis laisse une marge de cache
utile sur 6 Go, quelle `max-model-len` maximise la concurrence sans casser les
cas d'usage, et de combien l'écart de qualité AWQ/GGUF pèse réellement. Une
limite matérielle est en revanche certaine : une carte Turing (2019) n'a pas les
optimisations récentes (FP8, entre autres), et certains flags seront refusés au
démarrage — à lire dans les logs.

Ce qui promouvrait cette leçon en « refaire » : un `compose` avec runtime nvidia
sous `etapes/inference/`, un modèle 3B AWQ servi, et les trois relevés qui
comptent — occupation à vide, occupation sous une requête, échec ou non à monter
`max-num-seqs`.

## Se tester

1. Un modèle dont les poids font 2,5 Go refuse de démarrer sur vLLM avec 6 Go de
   VRAM. Deux causes possibles : lesquelles, et où regardez-vous pour trancher ?
   *Réussi si* la réponse oppose le cache préalloué qui déborde aux poids trop
   gros, et propose de lire l'occupation journalisée après chargement des poids —
   ici ce sont les poids qui passent, donc c'est le cache.
2. On veut doubler le nombre d'utilisateurs simultanés sans changer de modèle ni
   de carte. Quel flag, et pourquoi ça marche ?
   *Réussi si* la réponse cite `--max-model-len` et explique qu'une place de
   cache plus petite en loge davantage dans la même VRAM.
3. Un collègue écrit dans le README « vLLM est plus lent qu'Ollama sur notre
   modèle ». Qu'exigez-vous avant de l'accepter ?
   *Réussi si* la réponse demande de vérifier que les quantisations comparées
   sont équivalentes, et propose de mesurer l'écart de qualité par les evals
   plutôt que de le supposer négligeable.

## À retenir

- vLLM préalloue le cache au démarrage : « ça rentre » se juge sur poids + cache
  réservé, jamais sur les poids seuls — d'où des OOM sur des modèles « qui
  devraient tenir ».
- `--max-model-len` est le levier central : il dimensionne le cache par requête,
  donc la concurrence, et se règle à l'usage réel, pas au maximum théorique.
- Un OOM au démarrage a deux causes opposées — cache préalloué ou poids trop
  gros — que l'occupation après chargement des poids sépare.
- AWQ et GGUF ne sont pas équivalents : l'écart de qualité se mesure par les
  evals sur backend commutable, il ne se déclare pas.

## Références

- Doc vLLM : engine args, quantization, serveur OpenAI-compatible — pour la
  liste exacte des flags et ce que chacun préalloue
- [Servir un modèle](deploiement.md) — le budget VRAM que ces flags règlent
- [Providers](../framework/providers.md) — le backend commutable qui rend
  mesurable l'écart de qualité entre formats
