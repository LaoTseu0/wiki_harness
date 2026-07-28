---
id: attention-causale
type: leçon
titre: L'attention causale
parcours: 0-generation
statut: brouillon
tags: [generation, transformer, attention]
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
processus: inference-transformer
etape: attention-causale
brique: generation
contrat: aucun — mécanisme interne fourni par le runtime du modèle
---

# L'attention causale

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-7--reconstruire-une-tête-dattention)

## Prérequis

- [[05-embeddings-tokens|Embeddings de tokens]]
- [[06-position-rope|Représenter la position]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer
decoder-only]].  
Input global : identifiants de tokens et cache éventuel. Output global : logits
du prochain token.  
Grandes étapes : embeddings → normalisation d'attention → attention causale →
résidu → MLP → projection.

**Étape ouverte** —
`normalisation-attention → attention-causale → residu-attention`.  
Input : residual stream normalisé et masque. Output : une mise à jour qui
agrège les valeurs des positions autorisées.  
Responsabilité : calculer, pour chaque requête, une combinaison pondérée du
passé accessible.

**L'essentiel** — `Q` cherche, `K` décrit ce qui peut correspondre et `V`
transporte la contribution. Le produit `QKᵀ`, mis à l'échelle, masqué puis
normalisé, fournit les poids appliqués à `V`.

**Recomposer** — la sortie d'attention ne remplace pas le residual stream. Elle
est projetée puis ajoutée par la connexion résiduelle avant le sous-bloc MLP.

![[attention-causale.canvas]]

## Connaissances

### Projeter Q, K et V

À partir d'une matrice de représentations \(X\), une tête calcule :

\[
Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V
\]

Les poids sont appris. `Q`, `K` et `V` ne sont pas trois copies sémantiques
étiquetées à la main ; ce sont trois projections servant des rôles différents
dans le calcul.

Pour une requête \(q_i\) et une clé \(k_j\), le score brut est leur produit
scalaire. La division par \(\sqrt{d_k}\) limite la croissance de la magnitude
des produits lorsque la dimension de tête augmente.

### Masquer le futur

Dans un modèle autorégressif, la position `i` ne doit pas exploiter les tokens
`j > i` pendant l'entraînement ou l'inférence. Le masque ajoute une valeur
équivalente à moins l'infini aux scores interdits avant softmax. Leur
probabilité devient alors nulle.

\[
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}
\left(\frac{QK^\top}{\sqrt{d_k}} + M\right)V
\]

Le masque de padding et le masque causal peuvent contribuer à `M`. Leur forme
et leur convention dépendent du runtime.

### Pondérer les valeurs

Softmax transforme chaque ligne de scores autorisés en poids non négatifs dont
la somme vaut un. La sortie d'une tête est la somme pondérée des vecteurs
`V`.

Une forte valeur d'attention indique une contribution importante dans cette
tête et cette couche pour ce passage avant. Elle ne prouve pas à elle seule une
explication causale du comportement final du modèle.

### Plusieurs têtes

L'attention multi-head répète le mécanisme dans plusieurs sous-espaces, concatène
les sorties puis les projette vers la dimension cachée. Les têtes peuvent
apprendre des relations différentes sans qu'un rôle stable leur soit assigné à
l'avance.

La Grouped-Query Attention utilise davantage de têtes de requêtes que de têtes
de clés et valeurs. Plusieurs requêtes partagent alors un même groupe de
`K`/`V`, ce qui réduit le cache. Ce choix d'architecture ne change pas le
contrat conceptuel `QKᵀ → poids → V`.

### La causalité ne garantit pas la vérité

Le masque empêche une fuite d'information depuis les tokens futurs de la
séquence. Il ne garantit ni la pertinence de l'attention, ni la factualité, ni
le respect des instructions. « Causal » décrit ici la direction temporelle du
calcul.

## Reconstruction

Une tête sans dépendance tensorielle :

```python
from math import exp, sqrt

def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def softmax(valeurs: list[float]) -> list[float]:
    maximum = max(valeurs)
    exp_values = [exp(v - maximum) for v in valeurs]
    total = sum(exp_values)
    return [v / total for v in exp_values]

def attention(
    q: list[float],
    keys: list[list[float]],
    values: list[list[float]],
) -> tuple[list[float], list[float]]:
    scores = [dot(q, key) / sqrt(len(q)) for key in keys]
    poids = softmax(scores)
    sortie = [
        sum(poids[j] * values[j][dimension] for j in range(len(values)))
        for dimension in range(len(values[0]))
    ]
    return sortie, poids
```

Pour simuler la causalité à la position `i`, ne fournir que les clés et valeurs
`0..i`, ou masquer explicitement le reste avant softmax.

## Décision et dépôt dans Praxis

- **Décision** — le laboratoire reconstruit une tête pour expliquer les
  invariants ; Praxis délègue l'attention réelle au runtime.
- **Alternatives** — traiter l'attention comme une recherche vectorielle, ou
  réimplémenter toutes les variantes de kernels.
- **Critère** — ouvrir le calcul qui explique le contexte et le cache sans
  confondre harnais et moteur d'inférence.
- **Coût accepté** — la reconstruction ignore le batch, les têtes et les kernels
  optimisés.
- **Condition de révision** — aucune ; les optimisations seront comparées au
  Parcours 1.
- **Contrat** — aucun contrat public dans `generation`.
- **Invariant et tests** — un token futur a un poids nul ; les poids autorisés
  somment à un à la tolérance numérique choisie.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la stabilité ou la performance d'un
  kernel d'attention.
- **Praxis ne garantit pas encore** — l'accès aux matrices d'attention d'un
  fournisseur.
- **Échec provoqué** — appliquer le masque après softmax laisse le total
  inférieur à un et ne renormalise pas les positions autorisées.
- **Ouverture ultérieure** — [[08-residual-normalisation|Residual stream et
  normalisation]] puis [[17-prefill-decode-kv-cache|cache KV]].

## Se tester

1. Pourquoi diviser les scores par \(\sqrt{d_k}\) ?
2. Quelle différence sépare le rôle d'une clé de celui d'une valeur ?
3. Pourquoi le masque doit-il agir avant softmax ?
4. Une matrice d'attention élevée constitue-t-elle une explication suffisante
   de la réponse finale ?
5. Quel coût mémoire la Grouped-Query Attention cherche-t-elle notamment à
   réduire ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#07--lattention-causale).

## Références

- [Vaswani et al., *Attention Is All You Need*, v7](https://arxiv.org/abs/1706.03762) —
  scaled dot-product attention et multi-head attention.
- [Ainslie et al., *GQA: Training Generalized Multi-Query Transformer Models
  from Multi-Head Checkpoints*, v2](https://arxiv.org/abs/2305.13245) —
  partage des clés et valeurs entre groupes de requêtes.
- [Transformers — implémentation Llama, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  projections, masque, scaling, softmax et répétition des groupes KV.

