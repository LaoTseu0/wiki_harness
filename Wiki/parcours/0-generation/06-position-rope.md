---
id: position-rope
type: leçon
titre: Représenter la position
parcours: 0-generation
statut: brouillon
tags: [generation, transformer, rope, position]
created: 2026-07-27
updated: 2026-07-28
verified: 2026-07-27
processus: inference-transformer
etape: attention-causale
brique: generation
contrat: aucun — mécanisme interne fourni par le runtime du modèle
---

# Représenter la position

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-6--faire-tourner-rope)

## Prérequis

- [[05-embeddings-tokens|Embeddings de tokens]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer]].  
[[glossaire/input|Input]] global : identifiants de tokens et cache éventuel. [[glossaire/output|Output]] global : logits
du prochain token.  
Grandes étapes : embeddings → normalisation → attention causale → résidu → MLP
→ projection.

**Étape ouverte** —
`normalisation-attention → attention-causale → residu-attention`.  
**Input** : requêtes et clés dérivées du residual stream, avec leurs positions.
**Output** : requêtes et clés portant une relation de position.  
Responsabilité : rendre la position exploitable par le score d'attention sans
la confondre avec le [[glossaire/masque-causal|masque causal]].

**L'essentiel** — [[glossaire/rope|RoPE]] fait tourner par paires les composantes de `Q` et `K`
selon leur position. Leur produit scalaire dépend alors du déplacement relatif
entre deux positions.

**Recomposer** — **RoPE** modifie les scores calculés par l'attention. Le **masque
causal** décide séparément quelles positions sont accessibles ; le cache doit
conserver des clés positionnées de manière compatible.

![[position-rope.canvas]]

## Connaissances

### Pourquoi ajouter une information de position

L'attention compare des vecteurs. Sans mécanisme positionnel supplémentaire,
les mêmes contenus utilisent les mêmes projections, et le calcul ne dispose pas
d'une représentation riche de leur distance ou de leur position.

Le **masque causal** apporte déjà une asymétrie : une position ne voit que son
préfixe. Il interdit le futur, mais ne remplace pas un encodage positionnel
capable de moduler les relations entre positions autorisées.

### La rotation

Sur une paire de composantes, une rotation d'angle $\theta$ s'écrit :

$$
R_\theta
\begin{bmatrix}x_1\\x_2\end{bmatrix}
=
\begin{bmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}
$$

La multiplication donne deux nouvelles composantes :

$$
x'_1 = x_1\cos\theta - x_2\sin\theta
\qquad
x'_2 = x_1\sin\theta + x_2\cos\theta
$$

La paire change ainsi de direction sans changer de longueur.

**RoPE** utilise plusieurs fréquences sur les paires de dimensions. À la position
`m`, il applique une rotation dépendant de `m` à la requête et à la clé. Le
produit scalaire entre la requête positionnée en `m` et la clé positionnée en
`n` peut se réécrire avec une rotation dépendant de `n - m`. La relation
relative apparaît donc directement dans le score.

Les implémentations de la famille Llama appliquent **RoPE** à `Q` et `K`, pas à
`V`. D'autres architectures peuvent choisir un autre encodage positionnel.

### **RoPE** et **masque causal** répondent à deux questions

- **RoPE** : comment la position modifie-t-elle la compatibilité entre une requête
  et une clé ?
- **Masque causal** : cette clé a-t-elle le droit de contribuer à cette requête ?

Une rotation correcte ne bloque pas le futur. Un masque correct sans encodage
de position n'implémente pas **RoPE**.

### Étendre la fenêtre n'est pas changer un nombre

La fréquence de base, la dimension des têtes, le nombre de positions vues à
l'entraînement et l'éventuelle stratégie de scaling déterminent le comportement
hors de la plage habituelle.

Modifier seulement `max_position_embeddings` permet parfois d'allouer une
séquence plus longue, mais ne prouve pas que le modèle conserve sa qualité.
Les variantes de scaling de **RoPE** doivent être lues dans la configuration et
évaluées avec le [[glossaire/checkpoint|checkpoint]] concerné.

### Position absolue du cache

Pendant le decode, le nouveau token reçoit la position qui suit celles déjà
présentes dans le [[glossaire/cache-kv|cache KV]]. Recommencer arbitrairement à zéro tout en
réutilisant des clés anciennes rend les rotations incompatibles.

Le cache doit donc transporter ou permettre de reconstruire la longueur déjà
vue et la convention de position.

## Reconstruction

Une seule fréquence suffit pour observer l'identité relative :

```python
from math import cos, sin

def rotation(vecteur: tuple[float, float], angle: float) -> tuple[float, float]:
    x, y = vecteur
    return (x * cos(angle) - y * sin(angle),
            x * sin(angle) + y * cos(angle))

def produit(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]

q = (1.0, 0.4)
k = (0.3, 0.8)
frequence = 0.2

score_2_5 = produit(rotation(q, 2 * frequence), rotation(k, 5 * frequence))
score_7_10 = produit(rotation(q, 7 * frequence), rotation(k, 10 * frequence))
assert abs(score_2_5 - score_7_10) < 1e-12
```

Les deux paires ont le même déplacement. Cette expérience ne reproduit ni les
nombreuses fréquences, ni les formes tensorielles, ni les variantes de scaling.

## Décision et dépôt dans Praxis

- **Décision** — Praxis ne fixe aucune convention **RoPE** universelle. Il expose
  seulement les métadonnées nécessaires à l'inspection du runtime.
- **Alternatives** — réécrire la position dans le harnais, ou supposer que tous
  les modèles ajoutent un vecteur positionnel aux embeddings.
- **Critère** — la position fait partie de l'architecture entraînée et ne peut
  pas être remplacée à la périphérie.
- **Coût accepté** — la configuration du modèle reste une dépendance normative
  de l'expérience.
- **Condition de révision** — une stratégie d'extension de contexte ne sera
  adoptée qu'après mesure sur le modèle local.
- **Contrat** — aucun contrat public dans `generation`.
- **Invariant et tests** — une reprise avec cache continue les indices de
  position ; une configuration de scaling est enregistrée avec le **checkpoint**.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la qualité d'une extrapolation **RoPE**.
- **Praxis ne garantit pas encore** — la compatibilité d'un cache entre deux
  runtimes ou deux configurations.
- **Échec provoqué** — réutiliser le même cache en repartant à la position zéro
  doit être considéré comme une séquence incohérente.
- **Ouverture ultérieure** — [[07-attention-causale|L'attention causale]] et
  [[17-prefill-decode-kv-cache|Prefill, decode et cache KV]].

## Se tester

1. Pourquoi le **masque causal** ne remplace-t-il pas **RoPE** ?
2. Quelles composantes sont tournées dans une implémentation Llama courante ?
3. Pourquoi deux paires de positions séparées par le même déplacement peuvent-
   elles produire le même score dans la reconstruction ?
4. Pourquoi augmenter seulement la limite numérique de contexte ne garantit-il
   pas la qualité du modèle ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#06--représenter-la-position).

## Références

- [Su et al., *RoFormer: Enhanced Transformer with Rotary Position Embedding*,
  v5](https://arxiv.org/abs/2104.09864) — formulation et propriétés de **RoPE**.
- [Transformers — implémentation Llama, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  calcul des fréquences, rotation de `Q` et `K`, position du cache.
- [Transformers — RoPE utilities](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py) —
  variantes configurables et validation.
