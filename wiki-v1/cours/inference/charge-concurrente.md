# Charge concurrente

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [un benchmark honnête](benchmark.md) — la courbe comme
  livrable ; [débit et latence](metriques-debit-latence.md) — les métriques que
  chaque requête relève, dont le débit agrégé que la concurrence fait diverger.
  [Les mécanismes vLLM](mecanismes-vllm.md) posent le batching continu que cette
  leçon met à l'épreuve.
- **Débloque** : [l'analyse](analyse-et-verdict.md), qui explique cassure par
  cassure les courbes produites ici, puis le [verdict](verdict-ollama-vs-vllm.md).

## L'essentiel

À une requête, Ollama et vLLM se ressemblent ; à vingt, ils divergent — c'est
**la** mesure du module. Un script de charge maison (asyncio + httpx) envoie 1,
5 puis 20 requêtes simultanées aux deux moteurs et trace ce que chacun fait de
la file.

La thèse : la concurrence n'est pas *un* axe de mesure parmi d'autres, c'est
**l'axe qui discrimine**. Et la forme de la divergence est prévisible avant même
de lancer — un mur chez Ollama, une érosion douce chez vLLM — parce qu'elle
découle directement de leur stratégie de file. Ce qui reste à mesurer n'est pas
*si* ça diverge, mais *où* : le point de charge où le cache de 6 Go casse la
courbe de vLLM.

Cette leçon ne redonne pas le mécanisme du batching continu — il est aux
[mécanismes vLLM](mecanismes-vllm.md) — ni la définition des métriques, qui est
[débit et latence](metriques-debit-latence.md). Elle décrit le montage de la
charge et la lecture de ses courbes.

## Le savoir

### Pourquoi la concurrence discrimine, et rien d'autre

Deux stratégies de file opposées produisent deux courbes opposées :

- **Ollama** traite peu de requêtes en parallèle (`OLLAMA_NUM_PARALLEL`, faible
  par défaut) et fait patienter le reste. Le TTFT des requêtes en file **croît
  linéairement** avec leur rang d'attente : la cinquième attend que les quatre
  d'avant finissent.
- **vLLM** insère chaque nouvelle requête dans le lot en cours (batching continu,
  [mécanismes vLLM](mecanismes-vllm.md)) : le débit **agrégé** grimpe, au prix
  d'une érosion progressive des tokens/s par requête, car la bande passante se
  partage.

C'est pourquoi une mesure à une requête ne prouve rien : sans file, aucune des
deux stratégies ne joue. La divergence est un phénomène de file, donc elle
n'apparaît qu'en montant en charge — la raison même pour laquelle la courbe, et
non le point, est le livrable.

### Le scénario de charge, et le piège qu'il évite

Le montage : *n* workers asynchrones lancés en salve, chacun mesurant ses propres
métriques ([débit et latence](metriques-debit-latence.md)) ; `n ∈ {1, 5, 20}` ;
plusieurs salves par point, parce que la variance à `n = 20` est grande et qu'un
seul tir donnerait un chiffre trompeur.

Un détail décide de la validité : les prompts doivent être **réalistes et
légèrement variés**. Des prompts identiques enchaînés mesureraient, à notre insu,
le [prompt caching](prompt-caching.md) — le second réutiliserait le préfixe du
premier — et gonfleraient le débit d'un effet qui n'a rien à voir avec la tenue
de charge. Varier le début de chaque prompt neutralise ce cache.

### Asyncio, pas des threads, et la raison est la nature de la charge

La charge est de l'**I/O pur** : chaque worker passe son temps à *attendre* un
flux réseau, pas à calculer. C'est exactement le cas où une boucle d'événements
à un fil est le bon outil — `asyncio.gather` de *n* coroutines httpx lance *n*
requêtes réellement simultanées sans le poids de *n* threads système. Des threads
ici paieraient un coût de commutation pour paralléliser des attentes qui ne
demandent aucun cœur.

### Lire les courbes avant de les avoir

Trois lectures se prédisent, et l'exercice consiste à vérifier chacune :

- **TTFT p95 vs n** : plat puis **mur** chez Ollama (la file), dégradation
  *douce* chez vLLM (l'insertion continue) ;
- **débit agrégé vs n** : plafonne vite chez Ollama, **croît** chez vLLM jusqu'à
  saturation du KV cache — sur 6 Go, le mur arrive tôt ([vLLM sur RTX 2060](vllm-sur-rtx-2060.md)) ;
- **signe de saturation** : les préemptions/évictions de vLLM quand le cache
  déborde, visibles dans ses logs et ses métriques — c'est la cassure de la
  courbe de débit, pas un plateau.

### Deux causes pour « le débit plafonne sous charge »

Symptôme identique — la courbe de débit agrégé cesse de monter — et deux origines
qui ne se corrigent pas au même endroit :

- **La file d'attente (Ollama).** Pas de batching continu : au-delà du
  parallélisme configuré, les requêtes attendent, et le débit ne monte plus
  quel que soit *n*.
- **Le cache saturé (vLLM).** Le batching insère jusqu'à ce que le KV cache soit
  plein, puis préempte des séquences pour en admettre d'autres — le débit casse
  au lieu de plafonner.

Ce qui les distingue : le moteur, et ses logs. Un plateau sans préemption est une
file (Ollama) ; une cassure accompagnée d'évictions est un cache plein (vLLM).
Confondre les deux ferait chercher de la VRAM là où il fallait augmenter le
parallélisme.

## Quand c'est la bonne réponse

**Mesurer la charge** dès que plus d'un utilisateur peut appeler le serveur en
même temps. C'est la seule mesure qui répond à « combien la carte en tient ».

**Se contenter d'une requête** quand l'usage cible est strictement mono-usager :
la courbe de charge décrit alors un régime que personne n'atteindra.

**Isoler la mesure du réseau et du voisinage** toujours : bencher depuis le LAN,
un seul moteur en VRAM à la fois (vérifié à `nvidia-smi`), sinon on mesure le
réseau et le partage de carte en plus du moteur.

## Ce qu'on ne saura pas faire

Le script `charge.py` n'est pas écrit et aucune salve n'a été tirée : les courbes
décrites sont des **prédictions** tirées des stratégies de file, pas des relevés.
On sait quelle forme *devrait* apparaître ; on ne sait pas encore où tombe la
cassure de vLLM sur cette carte, ni à quel `n` Ollama fait mur.

Ce que ça laisse ouvert : combien de salves par point domptent la variance à
`n = 20`, et si `n = 20` est même atteignable avant saturation sur 6 Go — il est
possible que le cache casse avant.

Ce qui promouvrait cette leçon en « refaire » : `charge.py` sous
`etapes/inference/` — workers async, sortie JSON brute par requête, agrégation
séparée, trois courbes générées — et le premier relevé qui confirme ou dément le
mur d'Ollama et la cassure de vLLM.

## Se tester

1. Un collègue mesure les deux moteurs à une seule requête, les trouve
   équivalents, et conclut qu'Ollama suffit pour une équipe. Où est la faute ?
   *Réussi si* la réponse note qu'à une requête aucune stratégie de file ne joue,
   et exige la mesure sous concurrence avant toute conclusion sur une équipe.
2. Vous enchaînez le même prompt à toutes les requêtes de la salve pour
   « simplifier ». Qu'est-ce que vous mesurez sans le vouloir ?
   *Réussi si* la réponse identifie le prompt caching (réutilisation du préfixe)
   et propose de varier le début de chaque prompt.
3. La courbe de débit agrégé cesse de monter. Deux causes possibles selon le
   moteur : lesquelles, et que regardez-vous ?
   *Réussi si* la réponse oppose la file d'Ollama (plateau, pas de batching) au
   cache plein de vLLM (cassure, préemptions), et va lire les logs pour trancher.

## À retenir

- La concurrence est l'axe qui discrimine : à une requête les moteurs se valent,
  la divergence est un phénomène de file.
- Ollama fait la queue (TTFT en mur linéaire) ; vLLM insère dans le lot (débit
  agrégé qui monte, tokens/s par requête qui s'érodent).
- Prompts variés obligatoires, sinon on mesure le prompt caching au lieu de la
  tenue de charge.
- Asyncio et non des threads : la charge est de l'attente réseau, pas du calcul.
- « Le débit plafonne » a deux causes selon le moteur — file d'Ollama ou cache
  saturé de vLLM — que les préemptions dans les logs séparent.

## Références

- `asyncio` + httpx — les streams concurrents, l'outil exact pour une charge
  d'I/O pur
- [Mécanismes vLLM](mecanismes-vllm.md) — le batching continu qui explique la
  forme des courbes
- Doc vLLM : metrics et scheduling — les préemptions qui signent la saturation
  du cache
