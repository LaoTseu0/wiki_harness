---
id: residual-normalisation
type: leçon
titre: Residual stream et normalisation
parcours: 0-generation
statut: brouillon
tags: [generation, transformer, residual, rmsnorm]
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
processus: inference-transformer
etape: residu-attention
brique: generation
contrat: aucun — mécanisme interne fourni par le runtime du modèle
---

# Residual stream et normalisation

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-8--suivre-le-residual-stream)

## Prérequis

- [[07-attention-causale|L'attention causale]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer
decoder-only]].  
Input global : identifiants de tokens et cache éventuel. Output global : logits
du prochain token.  
Grandes étapes : normaliser → attention → ajouter au résidu → normaliser → MLP
→ ajouter au résidu.

**Étape ouverte** —
`attention-causale → residu-attention → normalisation-mlp`.  
Input : residual stream d'entrée et mise à jour d'attention. Output : leur somme
transmise au second sous-bloc.  
Responsabilité : préserver le chemin principal tout en y accumulant une mise à
jour contextualisée.

**L'essentiel** — dans un bloc pré-norm courant, la normalisation prépare
l'entrée d'un sous-bloc, puis sa sortie est ajoutée au residual stream. La
normalisation et la connexion résiduelle ont des fonctions distinctes.

**Recomposer** — l'attention et le MLP écrivent successivement dans le même flux
de représentations. Ce flux traverse les couches et atteint finalement la
projection vocabulaire.

![[residual-normalisation.canvas]]

## Connaissances

### Le chemin résiduel

Une architecture decoder-only pré-norm courante peut s'écrire :

\[
y = x + \operatorname{Attention}(\operatorname{Norm}(x))
\]

\[
z = y + \operatorname{MLP}(\operatorname{Norm}(y))
\]

`x`, `y` et `z` possèdent la même dimension cachée. Chaque sous-bloc produit une
mise à jour compatible avec cette dimension ; l'addition conserve un chemin
direct pour l'information et les gradients.

Le residual stream n'est pas un objet stocké séparément par le modèle. C'est
le nom donné au tenseur principal qui traverse les blocs et accumule leurs
contributions.

### Pré-norm et post-norm

Dans une architecture pré-norm, la normalisation précède le sous-bloc. Dans
l'architecture Transformer d'origine, une normalisation suit l'addition
résiduelle. Ces organisations ne sont pas interchangeables après
l'entraînement : déplacer une normalisation change la fonction calculée.

Le Canvas du cours représente une architecture pré-norm fréquente, pas tous les
Transformers.

### LayerNorm et RMSNorm

LayerNorm recentre les composantes autour de leur moyenne et les remet à
l'échelle avec leur variance, puis peut appliquer des paramètres appris.

RMSNorm ne soustrait pas la moyenne. Une forme courante calcule :

\[
\operatorname{RMSNorm}(x)
=
g \odot \frac{x}{\sqrt{\operatorname{mean}(x^2)+\varepsilon}}
\]

`g` est une échelle apprise et \(\varepsilon\) évite une division instable près
de zéro. La normalisation agit par position sur la dimension cachée ; elle ne
normalise ni les tokens entre eux, ni les probabilités de sortie.

### Précision numérique

Les carrés, moyennes et racines peuvent être calculés dans une précision plus
élevée que celle des poids, puis reconvertis. Ce détail limite les erreurs
numériques. Il relève de l'implémentation du runtime et doit être observé avant
de comparer deux passages avant.

## Reconstruction

RMSNorm et une mise à jour résiduelle :

```python
from math import sqrt

def rms_norm(
    x: list[float], gain: list[float], epsilon: float = 1e-6
) -> list[float]:
    moyenne_carres = sum(v * v for v in x) / len(x)
    inverse_rms = 1.0 / sqrt(moyenne_carres + epsilon)
    return [g * v * inverse_rms for v, g in zip(x, gain)]

def ajouter_residu(
    residu: list[float], mise_a_jour: list[float]
) -> list[float]:
    if len(residu) != len(mise_a_jour):
        raise ValueError("dimensions incompatibles")
    return [x + delta for x, delta in zip(residu, mise_a_jour)]
```

Faire varier l'amplitude de `x` montre que RMSNorm remet l'échelle sous
contrôle, tandis que l'addition conserve exactement une mise à jour nulle.

## Décision et dépôt dans Praxis

- **Décision** — Praxis décrit l'ordre des sous-blocs à partir de la
  configuration du modèle ; il ne généralise pas le Canvas pré-norm à tous les
  checkpoints.
- **Alternatives** — enseigner seulement « chaque couche transforme le
  tenseur », ou reproduire le kernel de normalisation.
- **Critère** — l'ordre résidu–normalisation explique les points d'inspection et
  les divergences entre architectures.
- **Coût accepté** — la reconstruction ne simule pas la précision mixte.
- **Condition de révision** — un modèle local d'une autre famille exigera son
  propre relevé architectural.
- **Contrat** — aucun contrat public dans `generation`.
- **Invariant et tests** — les additions résiduelles conservent la forme ; la
  normalisation applique l'epsilon configuré.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — les bénéfices d'optimisation ou de
  convergence attribués à une variante de normalisation.
- **Praxis ne garantit pas encore** — une égalité numérique bit à bit entre
  runtimes.
- **Échec provoqué** — intervertir pré-norm et post-norm avec les mêmes poids
  doit produire une autre fonction.
- **Ouverture ultérieure** — [[09-mlp-transformer|Le MLP d'une couche]].

## Se tester

1. Pourquoi la sortie d'attention doit-elle retrouver la dimension du residual
   stream ?
2. Quelle opération de LayerNorm est absente de RMSNorm ?
3. Déplacer une normalisation après le sous-bloc conserve-t-il le modèle
   entraîné ?
4. Pourquoi RMSNorm ne transforme-t-elle pas les logits en probabilités ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#08--residual-stream-et-normalisation).

## Références

- [Vaswani et al., *Attention Is All You Need*, v7](https://arxiv.org/abs/1706.03762) —
  connexions résiduelles et LayerNorm dans le Transformer d'origine.
- [Zhang et Sennrich, *Root Mean Square Layer Normalization*,
  v1](https://arxiv.org/abs/1910.07467) — définition et motivation de RMSNorm.
- [Transformers — `LlamaDecoderLayer`, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  exemple concret de pré-norm et d'additions résiduelles.

