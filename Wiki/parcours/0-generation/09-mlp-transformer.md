---
id: mlp-transformer
type: leçon
titre: Le MLP d'une couche
parcours: 0-generation
statut: brouillon
tags: [generation, transformer, mlp, swiglu]
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
processus: inference-transformer
etape: mlp
brique: generation
contrat: aucun — mécanisme interne fourni par le runtime du modèle
---

# Le MLP d'une couche

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-9--ouvrir-le-mlp)

## Prérequis

- [[08-residual-normalisation|Residual stream et normalisation]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer
decoder-only]].  
Input global : identifiants de tokens et cache éventuel. Output global : logits
du prochain token.  
Grandes étapes : attention et résidu → normalisation du MLP → MLP → second
résidu → couche suivante.

**Étape ouverte** —
`normalisation-mlp → mlp → residu-mlp`.  
Input : représentation normalisée de chaque position. Output : une mise à jour
de la dimension cachée pour chaque position.  
Responsabilité : transformer les composantes d'un token sans agréger d'autres
positions.

**L'essentiel** — le MLP applique les mêmes projections et non-linéarités à
chaque position indépendamment. L'attention mélange les positions ; le MLP
mélange les caractéristiques à l'intérieur de chaque position.

**Recomposer** — la mise à jour du MLP rejoint le residual stream, puis le bloc
suivant peut à nouveau faire interagir les positions par attention.

![[mlp-transformer.canvas]]

## Connaissances

### Une transformation par position

Un MLP Transformer classique projette la dimension cachée \(d\) vers une
dimension intermédiaire plus grande, applique une non-linéarité, puis reprojette
vers \(d\).

\[
\operatorname{MLP}(x) = W_{\text{down}}\,
\sigma(W_{\text{up}}x + b_{\text{up}}) + b_{\text{down}}
\]

Les mêmes poids sont appliqués à toutes les positions. Aucun produit entre deux
positions n'apparaît dans ce calcul. Les informations venues d'autres tokens
ont déjà été intégrées dans `x` par l'attention.

### La non-linéarité est indispensable

Deux projections linéaires successives sans non-linéarité se réduisent à une
seule projection linéaire. L'activation permet au sous-bloc de représenter une
transformation plus riche.

Les architectures emploient notamment ReLU, GELU, SiLU ou des variantes
gated. Le nom « MLP » ne fixe donc pas sa formule exacte.

### SwiGLU

Une forme courante dans les modèles de la famille Llama est :

\[
\operatorname{SwiGLU}(x)
=
W_{\text{down}}
\left(
\operatorname{SiLU}(W_{\text{gate}}x)
\odot
W_{\text{up}}x
\right)
\]

Deux projections montantes produisent une porte et un contenu. Leur produit
composante par composante est ensuite projeté vers la dimension cachée. Les
noms `gate`, `up` et `down` décrivent l'implémentation ; leurs tailles viennent
de la configuration.

### Dimension intermédiaire et coût

La dimension intermédiaire détermine la taille des matrices et une part
importante du calcul et de la mémoire des poids. Une architecture gated emploie
trois projections au lieu des deux d'un MLP simple, mais peut ajuster la
dimension intermédiaire pour contrôler le nombre total de paramètres.

Le coût exact dépend du batch, de la longueur, de la précision, du matériel et
des kernels. Il ne se déduit pas d'un adjectif comme « large ».

### Variantes d'architecture

Un Mixture of Experts route certains tokens vers un sous-ensemble d'experts
MLP. D'autres architectures partagent, factorisent ou remplacent le sous-bloc.
Le processus du cours décrit un MLP dense courant ; ces variantes doivent être
comparées à cette frontière, pas présentées comme identiques.

## Reconstruction

Une version scalaire de SiLU et une porte simplifiée :

```python
from math import exp

def silu(x: float) -> float:
    return x / (1.0 + exp(-x))

def swiglu_simplifie(
    gate: list[float], contenu: list[float]
) -> list[float]:
    if len(gate) != len(contenu):
        raise ValueError("dimensions incompatibles")
    return [silu(g) * u for g, u in zip(gate, contenu)]

assert swiglu_simplifie([0.0], [4.0]) == [0.0]
```

La reconstruction ouvre la porte multiplicative. Elle omet volontairement les
trois matrices apprises et la projection de retour.

## Décision et dépôt dans Praxis

- **Décision** — le MLP reste interne au runtime ; le laboratoire inspecte sa
  configuration et ses formes.
- **Alternatives** — résumer le bloc à une « mémoire factuelle », ou recopier
  une implémentation Llama comme contrat générique.
- **Critère** — distinguer le mélange entre positions du mélange entre
  caractéristiques.
- **Coût accepté** — aucune interprétation sémantique n'est attribuée à une
  composante ou à un neurone isolé.
- **Condition de révision** — un modèle MoE exigera une leçon ou une entrée de
  glossaire si le routage change une décision du harnais.
- **Contrat** — aucun contrat public dans `generation`.
- **Invariant et tests** — la sortie retrouve la dimension du residual stream ;
  la fonction et la dimension intermédiaire viennent de la configuration.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — ce qu'un neurone particulier a appris.
- **Praxis ne garantit pas encore** — l'inspection des activations dans tous les
  runtimes.
- **Échec provoqué** — supprimer la non-linéarité réduit deux projections
  successives à une transformation linéaire.
- **Ouverture ultérieure** — [[10-projection-logits|De la représentation aux
  logits]].

## Se tester

1. Quelle opération du bloc permet aux positions de communiquer : attention ou
   MLP ?
2. Pourquoi deux couches linéaires sans activation n'offrent-elles pas le même
   mécanisme qu'un MLP non linéaire ?
3. Quel rôle joue le produit composante par composante dans SwiGLU ?
4. Pourquoi la taille intermédiaire influence-t-elle le coût et la taille des
   poids ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#09--le-mlp-dune-couche).

## Références

- [Vaswani et al., *Attention Is All You Need*, v7](https://arxiv.org/abs/1706.03762) —
  réseau feed-forward par position du Transformer.
- [Shazeer, *GLU Variants Improve Transformer*, v1](https://arxiv.org/abs/2002.05202) —
  variantes gated dont SwiGLU.
- [Transformers — `LlamaMLP`, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  projections `gate`, `up`, `down` et activation configurée.

