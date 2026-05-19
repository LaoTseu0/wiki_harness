---
id: fenetre-contexte-cout
type: leçon
titre: Fenêtre de contexte et coût
parcours: 0-generation
statut: brouillon
tags: [generation, context-window, complexity, budgets]
created: 2026-07-27
updated: 2026-07-29
verified: 2026-07-27
processus: generation-token
etape: ajout-token
brique: generation
contrat: praxis.generation.ContextLimit
---

# Fenêtre de contexte et coût

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-18--atteindre-la-frontière-de-contexte)

## Prérequis

- [[14-boucle-autoregressive|Réinjecter le token choisi]]
- [[17-prefill-decode-kv-cache|Prefill, decode et cache KV]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : sampling → ajout au contexte → décodage → arrêt ou
réinjection.

**Étape ouverte** — `sampling → ajout-token → detokenisation`.  
**Input** : token choisi, longueur courante et capacité du modèle. **Output** : séquence
étendue si la capacité le permet.  
Responsabilité : empêcher que l'entrée plus la sortie dépasse la fenêtre
effective et rendre le budget explicite.

**L'essentiel** — la [[glossaire/fenetre-de-contexte|fenêtre de contexte]] se mesure en positions ou tokens après
application du Template. Elle borne ensemble le préfixe et les tokens conservés
pour la suite ; elle n'est ni un nombre de caractères ni un budget de sortie.

**Recomposer** — chaque ajout consomme une position et agrandit le cache. Quand
la capacité manque, la boucle doit s'arrêter ou appliquer une politique de
contexte décidée ailleurs, jamais tronquer silencieusement.

![[fenetre-contexte-cout.canvas]]

## Connaissances

### Trois nombres différents

- **longueur d'entrée** : tokens obtenus après Template et tokenisation ;
- **budget de sortie** : nombre maximal de nouveaux tokens autorisés ;
- **fenêtre effective** : capacité réellement utilisable avec ce [[glossaire/checkpoint|checkpoint]],
  cette configuration et ce runtime.

Une requête simple exige :

$$
\text{**input**\_tokens} + \text{reserved\_output} \leq \text{context\_capacity}
$$

Réserver le maximum de sortie évite d'atteindre la frontière au milieu d'une
réponse. Une autre politique peut accepter une réserve souple, mais elle doit
annoncer le risque d'un arrêt `context_limit`.

### La capacité effective

La configuration du modèle annonce généralement une longueur maximale de
positions. Le runtime peut imposer une valeur inférieure, utiliser une fenêtre
glissante ou permettre une extension RoPE.

La plus grande valeur affichée n'est pas automatiquement la capacité fiable.
Il faut distinguer :

- allocation acceptée ;
- positions encodables sans erreur ;
- qualité effectivement évaluée à cette longueur.

### Coût du [[glossaire/prefill|prefill]]

Dans une attention complète standard, une séquence de longueur $N$ forme une
matrice de scores $N \times N$ par tête avant exploitation du masque. Le
nombre d'interactions d'attention est donc quadratique en $N$.

Les projections et le MLP ont d'autres coûts, généralement linéaires en nombre
de positions pour une largeur de modèle fixée. Le `O(N²)` de l'attention ne
permet pas à lui seul de prédire la latence totale : kernels, bande passante,
batch, précision et matériel interviennent.

### Coût du [[glossaire/decode|decode]] avec cache

Pour un nouveau token et une attention complète, la requête compare ses scores
aux $N$ clés précédentes : cette partie est linéaire en longueur conservée
pour ce pas. Générer $G$ tokens après un prompt de longueur $N$ accumule
environ :

$$
\sum_{g=0}^{G-1}(N+g)
=
GN + \frac{G(G-1)}{2}
$$

interactions requête–clé par tête, sans compter les autres opérations.

Le [[glossaire/cache-kv|cache KV]] consomme lui aussi une mémoire qui croît avec les positions, les
couches, les têtes KV, la dimension de tête et la taille numérique.

### Les architectures peuvent changer ces lois locales

Une fenêtre glissante borne le nombre de clés consultées dans certaines
couches. Une attention par chunks, sparse ou linéaire change la structure du
calcul. Un cache quantifié change le coût mémoire.

Ces variantes ne justifient pas de présenter toutes les fenêtres longues comme
gratuites. Leur portée et leur qualité doivent être mesurées sur
l'implémentation choisie.

### La politique de contexte vient après la frontière

Le Parcours 0 refuse un dépassement et produit une raison explicite. Le Parcours
3 décidera comment construire une conversation sous budget : éviction,
résumé, contexte récupéré et réserve de sortie.

Tronquer ici les premiers tokens pourrait supprimer les instructions ou couper
un message au milieu sans que l'appelant le sache.

## Reconstruction

Un budget sans troncature implicite :

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ContextBudget:
    capacity: int
    input_tokens: int
    reserved_output: int

    @property
    def remaining(self) -> int:
        return self.capacity - self.input_tokens

    def validate(self) -> None:
        if min(self.capacity, self.input_tokens, self.reserved_output) < 0:
            raise ValueError("budget négatif")
        if self.input_tokens + self.reserved_output > self.capacity:
            raise ValueError("fenêtre de contexte insuffisante")

ContextBudget(capacity=2048, input_tokens=1800, reserved_output=248).validate()
```

Le laboratoire fera ensuite varier la longueur réelle d'un prompt et mesurera
séparément temps de **prefill**, temps par token et mémoire lorsque le runtime les
expose.

## Décision et dépôt dans Praxis

- **Décision** — `ContextLimit` reçoit le comptage exact du tokenizer et refuse
  une réservation impossible. Aucune troncature automatique dans `generation`.
- **Alternatives** — compter les caractères ; laisser le runtime tronquer ;
  réserver toujours zéro token de sortie.
- **Critère** — préserver les instructions et rendre l'arrêt prévisible.
- **Coût accepté** — une requête trop longue échoue avant l'inférence jusqu'à ce
  qu'une politique de contexte existe.
- **Condition de révision** — le Parcours 3 ajoutera un gestionnaire de budget
  capable de composer et réduire le contexte.
- **Contrat** — `praxis.generation.ContextLimit`.
- **Invariant et tests** — comptage avec le tokenizer exact ; entrée et réserve
  non négatives ; somme inférieure ou égale à la capacité effective.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — une latence ou une mémoire pour le
  matériel de Mnémos.
- **Praxis ne garantit pas encore** — la qualité d'une extension de contexte ou
  d'une attention à fenêtre glissante.
- **Échec provoqué** — un prompt qui tient sans Template mais dépasse après
  sérialisation doit être refusé.
- **Ouverture ultérieure** — Parcours 1 pour mesurer le runtime et Parcours 3
  pour construire le contexte sous budget.

## Se tester

1. Pourquoi le budget doit-il être calculé après le Template de chat ?
2. Quelle différence sépare une capacité allouable d'une longueur à laquelle la
   qualité a été évaluée ?
3. Quel coût le **cache KV** évite-t-il, et quel coût linéaire demeure pendant un
   **decode** à attention complète ?
4. Pourquoi `O(N²)` ne suffit-il pas à prédire la latence réelle du **prefill** ?
5. Pourquoi `generation` refuse-t-il de tronquer silencieusement le prompt ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#18--fenêtre-de-contexte-et-coût).

## Références

- [Vaswani et al., *Attention Is All You Need*, v7](https://arxiv.org/abs/1706.03762) —
  complexité de l'attention complète.
- [Transformers — Cache strategies, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/kv_cache) — croissance
  du cache dynamique et fenêtres locales.
- [Transformers — `GenerationConfig`](https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig) —
  `max_new_tokens`, longueur et capacité de cache.
- [RoFormer, v5](https://arxiv.org/abs/2104.09864) — position rotative et
  frontière des extrapolations.

