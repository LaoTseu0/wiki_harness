---
id: embeddings-tokens
type: leçon
titre: Embeddings de tokens
parcours: 0-generation
statut: brouillon
tags: [generation, transformer, embeddings]
created: 2026-07-27
updated: 2026-07-29
verified: 2026-07-27
processus: inference-transformer
etape: embeddings-tokens
brique: generation
contrat: aucun — mécanisme interne fourni par le runtime du modèle
---

# Embeddings de tokens

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-5--inspecter-les-embeddings)

## Prérequis

- [[02-tokenisation-vocabulaire|Tokenisation et vocabulaire]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer]].  
[[glossaire/input|Input]] global : identifiants de [[glossaire/token|tokens]] et cache éventuel. [[glossaire/output|Output]] global : logits
du prochain **token**.  
Grandes étapes : [[glossaire/embedding|embeddings]] → blocs Transformer répétés → normalisation finale
→ projection [[glossaire/vocabulaire|vocabulaire]].

**Étape ouverte** —
`identifiants-tokens → embeddings-tokens → normalisation-attention`.  
**Input** : entiers compris dans le **vocabulaire**. **Output** : un vecteur initial par
position.  
Responsabilité : sélectionner dans une matrice apprise la représentation
associée à chaque identifiant.

**L'essentiel** — l'**embedding** de **token** est une lecture de ligne dans une
matrice de poids. Le contexte ne modifie pas encore ce vecteur ; les couches
Transformer le contextualisent ensuite.

**Recomposer** — la table d'**embeddings** suppose exactement le **vocabulaire** utilisé
pendant l'entraînement. Une erreur d'identifiant devient un mauvais vecteur
avant même la première couche d'attention.

![[embeddings-tokens.canvas]]

## Connaissances

### Une matrice indexée par le **vocabulaire**

Pour un **vocabulaire** de taille $V$ et une dimension cachée $d$, la table
d'**embeddings** possède la forme $V \times d$. Un identifiant `i` sélectionne la
ligne $E_i$.

Pour un batch de forme `[batch, sequence]`, la lecture produit typiquement un
tenseur `[batch, sequence, hidden_size]`. Ce n'est pas une multiplication
one-hot réellement matérialisée, même si elle lui est mathématiquement
équivalente : le runtime effectue une sélection optimisée de lignes.

Un identifiant négatif ou supérieur à `V - 1` n'a aucune représentation. Le
runtime doit le refuser plutôt que le rabattre silencieusement.

### Une représentation apprise, pas un dictionnaire de sens

Les lignes sont ajustées pendant l'entraînement afin de réduire la fonction de
perte. Leur proximité peut refléter des régularités apprises, mais une ligne
n'est ni une définition, ni un document récupérable, ni une mémoire agentique.

Le même identifiant sélectionne le même vecteur initial à chaque occurrence.
Deux occurrences acquièrent des représentations différentes après les
interactions avec leur contexte et leur position.

### Position et échelle dépendent de l'architecture

Le Transformer original ajoute un encodage positionnel au vecteur d'entrée.
Des modèles decoder-only actuels, comme les variantes Llama, appliquent plutôt
RoPE aux requêtes et clés dans l'attention. Il ne faut donc pas ajouter
arbitrairement un vecteur de position à une architecture qui n'a pas été
entraînée ainsi.

Certaines architectures multiplient aussi les **embeddings** par une constante.
Cette échelle est une propriété de la configuration et du code du modèle, pas
une étape universelle de Praxis.

### Partage avec la projection de sortie

La matrice de projection vers le **vocabulaire** peut partager ses poids avec la
table d'**embeddings**. Ce *weight tying* réduit le nombre de paramètres et relie
les représentations d'entrée et de sortie.

Le partage reste optionnel. Deux matrices de mêmes dimensions ne sont pas
nécessairement le même paramètre. Le runtime et la configuration du [[glossaire/checkpoint|checkpoint]]
font foi.

## Reconstruction

Une table jouet rend la sélection observable :

```python
EMBEDDINGS = [
    [0.0, 0.0, 0.0],   # padding
    [0.2, -0.1, 0.5],  # token 1
    [-0.4, 0.8, 0.1],  # token 2
]

def embed(token_ids: list[int]) -> list[list[float]]:
    if any(token_id < 0 or token_id >= len(EMBEDDINGS) for token_id in token_ids):
        raise ValueError("identifiant hors vocabulaire")
    return [EMBEDDINGS[token_id][:] for token_id in token_ids]

assert embed([1, 2, 1])[0] == embed([1, 2, 1])[2]
```

L'égalité finale porte seulement sur les vecteurs initiaux. Une couche
d'attention causale pourra ensuite produire deux représentations différentes
pour les deux occurrences.

## Décision et dépôt dans Praxis

- **Décision** — Praxis n'implémente pas les poids d'**embedding** d'un modèle
  réel. Le laboratoire peut les inspecter à travers le runtime.
- **Alternatives** — recopier l'architecture d'un modèle dans `generation`, ou
  traiter l'**embedding** comme un service de recherche sémantique.
- **Critère** — le Parcours 0 doit ouvrir le mécanisme qui explique la frontière
  identifiants–tenseurs sans réécrire un moteur tensoriel.
- **Coût accepté** — l'inspection dépend d'un runtime et d'un **checkpoint**
  explicitement versionnés.
- **Condition de révision** — le Parcours 1 définira la frontière d'inférence et
  les formats de poids réellement servis.
- **Contrat** — aucun contrat public : ce mécanisme reste interne au modèle.
- **Invariant et tests** — le tokenizer et le **checkpoint** ont un **vocabulaire**
  compatible ; les identifiants restent dans les bornes.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — que les distances entre les trois
  vecteurs jouets portent une sémantique.
- **Praxis ne garantit pas encore** — la forme tensorielle d'un fournisseur
  distant.
- **Échec provoqué** — un identifiant hors **vocabulaire** doit échouer avant
  l'inférence.
- **Ouverture ultérieure** — [[06-position-rope|Représenter la position]] et
  [[07-attention-causale|L'attention causale]].

## Se tester

1. Pourquoi deux occurrences du même **token** ont-elles le même **embedding** initial
   mais pas nécessairement la même représentation après une couche ?
2. Que faudrait-il permuter en plus du **vocabulaire** pour préserver exactement le
   comportement du modèle ?
3. Pourquoi une base vectorielle de documents et la table d'**embeddings** du
   modèle ne remplissent-elles pas la même fonction ?
4. Le partage des poids avec la projection de sortie peut-il être déduit de la
   seule forme des matrices ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#05--embeddings-de-tokens).

## Références

- [Vaswani et al., *Attention Is All You Need*, v7](https://arxiv.org/abs/1706.03762) —
  **embeddings** et architecture Transformer d'origine.
- [PyTorch — `Embedding`](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html) —
  table de recherche et formes d'entrée et de sortie.
- [Transformers — implémentation Llama, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  `embed_tokens`, blocs, normalisation et tête de sortie.

