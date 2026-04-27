---
id: boucle-autoregressive
type: leçon
titre: Réinjecter le token choisi
parcours: 0-generation
statut: brouillon
tags: [generation, autoregression, loop]
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
processus: generation-token
etape: reinjection
brique: generation
contrat: praxis.generation.GenerationLoop
---

# Réinjecter le token choisi

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-14--exécuter-la-boucle-autoregressive)

## Prérequis

- [[13-sampling-reproductibilite|Tirer le prochain token]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : inférence → choix → ajout → décodage → décision d'arrêt →
réinjection.

**Étape ouverte** —
`condition-arret → reinjection → inference`.  
Input : séquence étendue, état du run et décision de continuer. Output : nouvel
Input du modèle pour le pas suivant.  
Responsabilité : faire du token choisi une partie immuable du préfixe suivant.

**L'essentiel** — un modèle causal produit une distribution pour une position.
Le harnais choisit un token, l'ajoute au préfixe et recommence jusqu'à une
condition d'arrêt.

**Recomposer** — chaque tour repasse par l'inférence, les transformations et le
sampling. Le token réinjecté modifie toutes les distributions suivantes ; une
divergence locale devient une nouvelle trajectoire.

![[boucle-autoregressive.canvas]]

## Connaissances

### Factorisation autorégressive

La probabilité d'une suite \(t_1,\ldots,t_N\) se factorise :

\[
P(t_1,\ldots,t_N)
=
\prod_{i=1}^{N} P(t_i \mid t_1,\ldots,t_{i-1})
\]

Le passage avant fournit la distribution du prochain token conditionnellement
au préfixe courant. Il ne produit pas toute la réponse en une seule décision.

### Le token choisi devient une donnée

Après sampling, le token est ajouté à la séquence. Le pas suivant le traite
comme n'importe quel élément du préfixe. Le modèle ne garde pas à côté une
liste de candidats abandonnés.

Revenir sur un choix exige un algorithme de recherche, un fork de trajectoire
ou une nouvelle génération. La boucle greedy ou sampling simple ne corrige pas
spontanément un token déjà réinjecté.

### État minimal du run

Une boucle pédagogique maintient au moins :

- les identifiants du prompt ;
- les identifiants générés ;
- la configuration des transformations ;
- l'état du générateur pseudo-aléatoire ;
- l'état du décodeur incrémental ;
- la raison d'arrêt éventuelle ;
- le cache du modèle lorsqu'il est utilisé.

Cet état reste éphémère dans le Parcours 0. Le Parcours 10 décidera comment le
sérialiser et le reprendre après interruption.

### Un tour possède des frontières

Un ordre explicite évite les effets cachés :

1. demander les logits ;
2. transformer les logits ;
3. choisir un identifiant ;
4. l'ajouter à la séquence ;
5. alimenter le décodeur ;
6. évaluer les conditions d'arrêt ;
7. réinjecter seulement si la génération continue.

Certaines implémentations vérifient EOS immédiatement après le choix et ne
décodent pas ce token comme contenu. Cette variation doit être fixée par la
politique d'arrêt ; elle ne change pas le principe autorégressif.

### Entraînement et inférence

Pendant l'entraînement causal, plusieurs positions d'une séquence connue
peuvent être évaluées en parallèle sous masque causal. À l'inférence, le
prochain token n'existe pas encore : chaque nouvelle position dépend du choix
précédent.

Cette dépendance séquentielle limite la parallélisation du decode, même si le
calcul interne d'un passage avant reste massivement parallèle.

## Reconstruction

Une boucle indépendante de tout modèle réel :

```python
from collections.abc import Callable

NextLogits = Callable[[list[int]], list[float]]
Choose = Callable[[list[float]], int]
ShouldStop = Callable[[list[int], int], bool]

def generer(
    prompt: list[int],
    prochains_logits: NextLogits,
    choisir: Choose,
    arreter: ShouldStop,
    maximum: int,
) -> list[int]:
    sequence = prompt[:]
    produits: list[int] = []
    for _ in range(maximum):
        logits = prochains_logits(sequence)
        token_id = choisir(logits)
        sequence.append(token_id)
        produits.append(token_id)
        if arreter(produits, token_id):
            break
    return produits
```

Un `prochains_logits` scripté permet de tester la boucle sans poids ni réseau.
Le maximum reste obligatoire même si une fonction EOS est fournie.

## Décision et dépôt dans Praxis

- **Décision** — `GenerationLoop` orchestre des contrats injectés : modèle,
  pipeline de logits, sampler, décodeur et politique d'arrêt.
- **Alternatives** — une fonction monolithique couplée à Transformers, ou une
  boucle récursive.
- **Critère** — chaque mécanisme doit pouvoir être reconstruit, remplacé et
  testé isolément.
- **Coût accepté** — davantage de petits objets et d'événements qu'un simple
  appel `generate()`.
- **Condition de révision** — le Parcours 9 généralisera cette boucle en boucle
  d'agent ; le Parcours 0 reste limité au prochain token.
- **Contrat** — `praxis.generation.GenerationLoop`.
- **Invariant et tests** — au plus un token est ajouté par tour ; chaque Input
  est le préfixe précédent plus ce token ; un budget fini borne la boucle.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la performance d'une boucle avec cache.
- **Praxis ne garantit pas encore** — la reprise après arrêt du processus.
- **Échec provoqué** — une politique EOS défectueuse ne doit pas créer une
  boucle infinie grâce au budget maximal.
- **Ouverture ultérieure** —
  [[15-detokenisation-fragments|Reconstruire le texte généré]],
  [[16-conditions-arret|Borner la génération]] et
  [[17-prefill-decode-kv-cache|cache KV]].

## Se tester

1. Pourquoi une seule différence de token peut-elle faire diverger tout le
   suffixe ?
2. Quelle partie de l'état doit progresser à chaque tirage aléatoire ?
3. Pourquoi l'entraînement peut-il évaluer plusieurs positions en parallèle
   alors que le decode simple reste séquentiel ?
4. Quelle garantie apporte un budget maximal même lorsque EOS existe ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#14--réinjecter-le-token-choisi).

## Références

- [Bengio et al., *A Neural Probabilistic Language Model*](https://www.jmlr.org/papers/v3/bengio03a.html) —
  factorisation conditionnelle d'un modèle de langage neuronal.
- [Transformers — GenerationMixin, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/main_classes/text_generation) —
  boucle de génération, stratégies et sorties.
- [Transformers — `generation/utils.py`, révision `main`](https://github.com/huggingface/transformers/blob/main/src/transformers/generation/utils.py) —
  implémentation industrielle à confronter à la reconstruction.

