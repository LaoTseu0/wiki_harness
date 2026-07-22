# Attention et KV cache

> [carte du cours](../carte.md) · étape : [`11_kv_cache.py`](../../etapes/fondamentaux/11_kv_cache.py)

## L'essentiel

L'**attention** est le mécanisme par lequel chaque token regarde tous les
tokens précédents pour décider de quoi il dépend. Son coût croît avec le
carré de la longueur — c'est pour ça qu'un long contexte n'est ni gratuit
ni pleinement exploité. Le **KV cache** est l'optimisation qui rend la
génération viable malgré ça, et qui explique une observation banale de
toutes les leçons précédentes : *le premier token est lent, les suivants
sont rapides.*

## Le savoir

**Q, K, V.** Chaque token produit trois vecteurs : une **requête** Q (ce
que je cherche), une **clé** K (ce que je propose) et une **valeur** V (ce
que j'apporte). Un token pondère les V de tous les autres selon l'accord
entre son Q et leurs K. C'est la même opération que la
[similarité cosinus](../retrieval/similarite-cosinus.md) du RAG — un
produit scalaire qui mesure un alignement — appliquée ici à l'intérieur du
modèle, à chaque couche, plutôt qu'entre documents.

**Le coût quadratique.** Lire un prompt de *n* tokens demande ~*n*²
comparaisons. Doubler le contexte quadruple le travail. C'est la raison
mécanique derrière le *lost in the middle* déjà rencontré : une grande
fenêtre n'est pas une grande attention.

**Le KV cache.** Les K et V d'un token ne dépendent que de lui et de son
passé : une fois calculés, ils **ne changent jamais**. On les garde en
mémoire. Générer le token suivant ne recalcule donc pas tout le passé,
seulement le nouveau token contre le cache. La génération se scinde en
deux régimes :

| Régime | Ce qui se passe | Coût |
|---|---|---|
| **Prefill** | lire le prompt d'un bloc, remplir le cache | ~*n*², c'est la latence du 1er token |
| **Decode** | produire les tokens un par un contre le cache | ~*n* par token, bien plus rapide |

**Ce que le cache coûte.** Il occupe de la VRAM proportionnellement à la
longueur du contexte × le nombre de couches. Sur 6 Go, le mur arrive vite.
C'est ce cache qui sature en premier sous
[charge concurrente](../inference/charge-concurrente.md), et c'est lui que
PagedAttention gère par pages plutôt que d'un bloc — le sujet des
[mécanismes vLLM](../inference/mecanismes-vllm.md).

**Ce que ça éclaire ailleurs.** Le [prompt caching](../inference/prompt-caching.md)
n'est rien d'autre que *garder le prefill d'un préfixe stable* d'une
requête à l'autre : sans KV cache, l'idée n'a pas de sens. Et l'ordre du
prompt cesse d'être esthétique — ce qui est stable se met devant, ce qui
varie derrière, sinon le préfixe réutilisable n'existe pas.

## En pratique

[11_kv_cache.py](../../etapes/fondamentaux/11_kv_cache.py) : la même tâche,
avec un prompt qu'on fait grossir. Ollama sépare les deux régimes dans sa
réponse — `prompt_eval_duration` (prefill) et `eval_duration` (decode).

**À prédire avant de lancer** :

- le prefill grandit-il proportionnellement au nombre de tokens, ou plus
  vite ? Ta mesure suffit-elle à trancher entre les deux ?
- le débit de decode (tokens/s) bouge-t-il quand le prompt grossit ?
  Pourquoi devrait-il, ou ne pas devoir ?

## Pièges connus

- **Confondre la théorie et la mesure** : le coût est quadratique *en
  calcul*, mais sur un GPU peu chargé la parallélisation masque la courbe
  aux petites tailles. Un banc trop court montrera du linéaire — ce n'est
  pas une réfutation, c'est un banc trop court.
- **Attribuer au modèle une lenteur qui vient du prefill** : « il est
  lent » sur un long prompt est un diagnostic vide. Séparer prefill et
  decode *avant* de conclure.
- **Oublier que le cache est par séquence** : deux conversations
  concurrentes ne le partagent pas — d'où la saturation VRAM bien plus tôt
  qu'un calcul « un utilisateur » ne le laisse croire.
- **Premier appel non représentatif** : chargement du modèle en VRAM.
  Toujours un tour de chauffe avant de mesurer.

## Se tester

- Pourquoi le premier token met-il plus longtemps à venir que les
  cinquante suivants réunis ?
- On te demande de réduire la latence perçue d'un chat sans changer de
  modèle ni de machine. Quels leviers, et sur quel régime agit chacun ?
- Ton service tient 5 utilisateurs et s'écroule à 8, sans que le CPU ni le
  GPU ne saturent. Quelle est ta première hypothèse ?

## Références

- 3Blue1Brown, série sur les transformers — l'intuition visuelle de Q/K/V
- *Attention Is All You Need* (Vaswani et al., 2017) — l'article d'origine
- La doc PagedAttention de vLLM, pour la suite côté serving
