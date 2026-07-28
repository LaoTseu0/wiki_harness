---
id: logits-softmax
type: leçon
titre: Des logits à une distribution
parcours: 0-generation
statut: brouillon
tags: [generation, logits, softmax, probabilites]
created: 2026-07-27
updated: 2026-07-29
verified: 2026-07-27
processus: generation-token
etape: logits
brique: generation
contrat: praxis.generation.softmax
---

# Des logits à une distribution

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-11--normaliser-les-logits)

## Prérequis

- [[10-projection-logits|De la représentation aux logits]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : inférence → [[glossaire/logit|logits]] → transformations → [[glossaire/sampling|sampling]] → ajout du
token.

**Étape ouverte** — `inference → logits → transformation-logits`.  
**Input** : un score réel par token du vocabulaire. **Output** : les mêmes candidats,
interprétables relativement et convertibles en probabilités.  
Responsabilité : préserver l'association identifiant–score et normaliser
numériquement lorsque la transformation l'exige.

**L'essentiel** — [[glossaire/softmax|softmax]] exponentie les écarts de **logits** et normalise leur
somme. La distribution obtenue décrit le prochain token conditionnellement au
préfixe exact, pas la vérité d'une réponse entière.

**Recomposer** — les transformations de **sampling** peuvent agir directement sur
les **logits** ou consulter leur **softmax**. Après filtrage, les candidats conservés
doivent former une distribution valide avant le tirage.

![[logits-softmax.canvas]]

## Connaissances

### Définition

Pour des **logits** $z_1,\ldots,z_V$ :

$$
p_i = \frac{\exp(z_i)}{\sum_{j=1}^{V}\exp(z_j)}
$$

Chaque $p_i$ est positif et la somme vaut un, à l'erreur numérique près. Un
écart de **logits** devient un rapport de probabilités :

$$
\frac{p_i}{p_j} = \exp(z_i-z_j)
$$

La valeur absolue d'un **logit** importe donc moins que ses écarts avec les autres
candidats.

### Stabilité numérique

Exponentier de grands **logits** peut déborder. On soustrait le maximum $m$ :

$$
p_i =
\frac{\exp(z_i-m)}{\sum_j \exp(z_j-m)}
$$

Cette transformation ne change pas la distribution, car le facteur
$\exp(-m)$ apparaît au numérateur et au dénominateur. Elle garantit qu'au
moins un exposant vaut zéro et que les autres sont négatifs ou nuls.

Des **logits** contenant `NaN`, `+inf`, uniquement `-inf`, ou une somme
exponentielle nulle ne forment pas une distribution exploitable. Un `-inf`
isolé reste utile pour représenter un candidat masqué : son poids exponentiel
vaut zéro.

### Probabilité conditionnelle

La distribution représente :

$$
P(t_{n+1}\mid t_1,\ldots,t_n;\theta)
$$

Elle dépend des poids $\theta$, du préfixe tokenisé et du passage avant. Elle
ne mesure pas directement la probabilité qu'une affirmation soit vraie. Un
token peut être très probable parce qu'il complète une formulation fréquente,
même si la proposition complète est fausse.

### [[glossaire/log-probabilite|Log-probabilités]]

Le logarithme de **softmax** évite de multiplier de très petites probabilités. La
**log-probabilité** d'une séquence autorégressive est la somme des
**log-probabilités** conditionnelles de ses tokens.

Comparer des sommes brutes entre séquences de longueurs différentes favorise
généralement les séquences courtes, puisque chaque terme ajouté est inférieur
ou égal à zéro. Toute normalisation par longueur doit donc être annoncée.

### **Softmax** n'est pas encore une stratégie de génération

**Softmax** rend une distribution possible. Il ne décide pas si tous les candidats
restent autorisés, si la température les aplatit, si un filtre tronque la queue
ou si l'argmax remplace le tirage.

Selon l'implémentation, certaines transformations agissent sur les **logits** avant
un unique **softmax** final ; d'autres calculent temporairement les probabilités
pour choisir un masque. L'ordre exact fait partie du contrat du sampler.

## Reconstruction

Une implémentation stable :

```python
from math import exp, inf, isnan

def softmax(logits: list[float]) -> list[float]:
    if not logits or any(isnan(logit) or logit == inf for logit in logits):
        raise ValueError("logits invalides")
    maximum = max(logits)
    if maximum == -inf:
        raise ValueError("tous les candidats sont masqués")
    poids = [exp(logit - maximum) for logit in logits]
    total = sum(poids)
    if total == 0.0:
        raise ValueError("distribution vide")
    return [poids_i / total for poids_i in poids]

logits = [1000.0, 1001.0, 999.0]
probabilites = softmax(logits)
assert abs(sum(probabilites) - 1.0) < 1e-12
assert probabilites.index(max(probabilites)) == 1
```

Ajouter la même constante à tous les éléments doit laisser la distribution
inchangée à la tolérance choisie.

## Décision et dépôt dans Praxis

- **Décision** — `softmax` est une fonction pure et stable utilisée par le
  laboratoire et le sampler.
- **Alternatives** — déléguer toute normalisation au runtime, ou stocker
  uniquement des probabilités.
- **Critère** — conserver les **logits** permet de composer les transformations et
  d'observer chaque étape.
- **Coût accepté** — l'implémentation pédagogique en Python n'est pas utilisée
  sur le chemin de production tensoriel.
- **Condition de révision** — le backend pourra fournir une primitive optimisée
  derrière le même invariant.
- **Contrat** — `praxis.generation.softmax`.
- **Invariant et tests** — sortie finie, non négative, somme proche de un,
  ordre conservé, poids nul pour `-inf`, invariance à une translation commune.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la calibration factuelle du modèle.
- **Praxis ne garantit pas encore** — l'accès aux **log-probabilités** d'un
  fournisseur.
- **Échec provoqué** — un vecteur contenant `NaN` doit être rejeté plutôt que
  tiré.
- **Ouverture ultérieure** —
  [[12-filtrage-distribution|Transformer la distribution]].

## Se tester

1. Pourquoi soustraire le maximum ne change-t-il pas la distribution ?
2. Que vaut le rapport $p_i/p_j$ en fonction des deux **logits** ?
3. Pourquoi la probabilité du prochain token n'est-elle pas une mesure de
   vérité ?
4. Pourquoi comparer la somme des **log-probabilités** de deux séquences de
   longueurs différentes demande-t-il une règle supplémentaire ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#11--des-logits-à-une-distribution).

## Références

- [PyTorch — `softmax`](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.softmax.html) —
  définition et dimension de normalisation.
- [PyTorch — `log_softmax`](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.log_softmax.html) —
  formulation numériquement stable des **log-probabilités**.
- [Transformers — génération, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/main_classes/text_generation) —
  scores, sorties et transformations de génération.
