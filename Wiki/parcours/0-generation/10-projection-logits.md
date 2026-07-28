---
id: projection-logits
type: leçon
titre: De la représentation aux logits
parcours: 0-generation
statut: brouillon
tags: [generation, transformer, logits, lm-head]
created: 2026-07-27
updated: 2026-07-29
verified: 2026-07-27
processus: inference-transformer
etape: projection-vocabulaire
brique: generation
contrat: aucun — la frontière NextTokenModel est déposée après le cache
---

# De la représentation aux logits

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-10--projeter-vers-le-vocabulaire)

## Prérequis

- [[08-residual-normalisation|Residual stream et normalisation]]
- [[09-mlp-transformer|Le MLP d'une couche]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer
decoder-only]].  
[[glossaire/input|Input]] global : identifiants de [[glossaire/token|tokens]] et cache éventuel. [[glossaire/output|Output]] global : [[glossaire/logit|logits]]
du prochain **token**.  
Grandes étapes : blocs répétés → normalisation finale → projection vocabulaire
→ **logits**.

**Étape ouverte** —
`normalisation-finale → projection-vocabulaire → logits-sortie`.  
**Input** : représentation finale de dimension cachée. **Output** : un score par entrée
du vocabulaire.  
Responsabilité : ramener l'état du modèle dans l'espace discret des candidats.

**L'essentiel** — la tête de langage applique une projection linéaire vers la
taille du vocabulaire. Ses sorties sont des scores relatifs, pas encore des
probabilités.

**Recomposer** — les **logits** quittent le sous-processus d'inférence et rejoignent
le processus de génération, où les contraintes, pénalités, filtres et softmax
décideront du prochain **token**.

![[projection-logits.canvas]]

## Connaissances

### La normalisation finale

Une architecture pré-norm courante applique une dernière normalisation après le
dernier bloc. Elle prépare la représentation avant la tête de langage. Son type
et son epsilon viennent de l'architecture ; ce n'est pas le softmax du
vocabulaire.

### Une ligne par candidat

Pour une dimension cachée $d$ et un vocabulaire de taille $V$, la matrice de
sortie possède typiquement la forme $V \times d$.

$$
z = W_{\text{vocab}}h + b
$$

`h` est la représentation d'une position et `z` contient $V$ **logits**. Chaque
indice de `z` correspond au même identifiant de vocabulaire que le tokenizer.
Le biais est optionnel selon l'architecture.

Pour une séquence complète, le modèle peut produire `[batch, sequence, V]`.
La génération du prochain **token** utilise les **logits** de la dernière position
utile. Les **logits** des autres positions servent notamment à l'entraînement ou à
des analyses.

### Les scores sont relatifs

Un **logit** peut être négatif, positif ou nul. Il n'est ni borné entre zéro et un,
ni interprétable isolément comme une confiance.

Ajouter la même constante à tous les **logits** ne change pas le softmax, car le
facteur multiplicatif correspondant s'annule lors de la normalisation. En
revanche, multiplier tous les **logits** modifie leurs écarts relatifs et donc la
distribution ; la température exploitera précisément cette propriété.

### Tous les **tokens** du vocabulaire sont candidats

La projection comprend les sous-mots, octets et **tokens** spéciaux présents dans
le vocabulaire. Un EOS reçoit donc un **logit** comme les autres. La boucle
n'arrête pas le calcul parce que le modèle « sait qu'il a fini » : elle tire ou
choisit EOS, puis la politique d'arrêt interprète son identifiant.

Une grammaire ou un `logit_bias` pourra modifier les candidats plus tard, après
la projection. La tête de langage brute ne connaît pas ces contraintes du
harnais.

### Partage de poids optionnel

La tête peut réutiliser la matrice d'[[glossaire/embedding|embeddings]] transposée ou posséder ses
propres poids. Cette décision, appelée *weight tying*, est configurée pendant
l'entraînement. Le harnais ne doit pas la déduire du nom `lm_head`.

## Reconstruction

Projeter un vecteur caché vers quatre candidats :

```python
def produit(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def projeter(
    hidden: list[float],
    poids_vocabulaire: list[list[float]],
    biais: list[float] | None = None,
) -> list[float]:
    biais = biais or [0.0] * len(poids_vocabulaire)
    return [
        produit(ligne, hidden) + offset
        for ligne, offset in zip(poids_vocabulaire, biais)
    ]

hidden = [0.5, -1.0, 0.2]
poids = [
    [0.1, 0.4, -0.2],
    [-0.3, 0.2, 0.8],
    [0.7, -0.1, 0.0],
    [0.0, 0.2, 0.5],
]
logits = projeter(hidden, poids)
assert len(logits) == len(poids)
```

Le classement des scores est observable, mais aucune valeur n'est encore une
probabilité.

## Décision et dépôt dans Praxis

- **Décision** — la frontière du runtime renverra les **logits** du prochain **token**,
  indexés par le vocabulaire associé.
- **Alternatives** — demander directement des probabilités, ou laisser le
  runtime choisir un **token** sans exposer les scores.
- **Critère** — les **logits** permettent de reconstruire et composer les
  transformations sans perdre d'information par un choix prématuré.
- **Coût accepté** — exposer un vecteur de taille vocabulaire est réservé au
  runtime local et au laboratoire ; une API distante peut ne pas offrir cette
  capacité.
- **Condition de révision** — le contrat par capacités du Parcours 2 rendra
  l'accès aux **logits** optionnel.
- **Contrat** — préparatoire à `praxis.generation.NextTokenModel`.
- **Invariant et tests** — l'ordre des **logits** correspond aux identifiants du
  tokenizer ; la taille vaut `vocab_size`.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — que le plus grand **logit** donne le
  meilleur texte à long terme.
- **Praxis ne garantit pas encore** — l'accès aux **logits** d'un modèle servi par
  une API.
- **Échec provoqué** — utiliser un vocabulaire permuté conserve la forme du
  vecteur mais associe les scores aux mauvais **tokens**.
- **Ouverture ultérieure** — [[11-logits-softmax|Des logits à une distribution]]
  puis [[12-filtrage-distribution|Transformer la distribution]].

## Se tester

1. Pourquoi un **logit** de `5` n'est-il pas une probabilité de 500 % ?
2. Quelle position de la sortie complète sert à choisir le prochain **token** ?
3. Pourquoi ajouter la même constante à tous les **logits** ne change-t-il pas le
   softmax ?
4. À quel moment EOS devient-il une condition d'arrêt plutôt qu'un simple
   candidat ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#10--de-la-représentation-aux-logits).

## Références

- [Vaswani et al., *Attention Is All You Need*, v7](https://arxiv.org/abs/1706.03762) —
  projection linéaire et softmax de sortie.
- [Press et Wolf, *Using the Output Embedding to Improve Language Models*,
  v3](https://arxiv.org/abs/1608.05859) — partage des **embeddings** d'entrée et de
  sortie.
- [Transformers — implémentation `LlamaForCausalLM`, révision `main` vérifiée
  le 2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  normalisation finale, `lm_head` et sélection des **logits**.

