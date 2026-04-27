---
id: sampling-reproductibilite
type: leçon
titre: Tirer le prochain token
parcours: 0-generation
statut: brouillon
tags: [generation, sampling, seed, reproductibilite]
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
processus: generation-token
etape: sampling
brique: generation
contrat: praxis.generation.Sampler
---

# Tirer le prochain token

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-13--tirer-et-reproduire)

## Prérequis

- [[12-filtrage-distribution|Transformer la distribution]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : logits transformés → sampling → ajout du token → boucle.

**Étape ouverte** —
`transformation-logits → sampling → ajout-token`.  
Input : distribution finie, normalisée et non vide. Output : un identifiant de
token.  
Responsabilité : effectuer exactement un tirage catégoriel avec une source
d'aléa explicite, ou appliquer l'argmax demandé.

**L'essentiel** — le sampling tire un indice selon les poids finaux. Une seed
initialise l'état d'un générateur pseudo-aléatoire ; elle ne fige ni les logits
ni les calculs qui les ont produits.

**Recomposer** — le token choisi est ajouté à la séquence. Cette décision
modifie le prochain passage avant, de sorte qu'une divergence unique peut
entraîner une trajectoire entièrement différente.

![[sampling-reproductibilite.canvas]]

## Connaissances

### Distribution catégorielle

Pour des probabilités \(p_1,\ldots,p_V\), le sampler choisit l'indice `i` avec
la probabilité \(p_i\). Un tirage possible utilise un nombre uniforme
\(u\in[0,1)\) et la première somme cumulée supérieure à `u`.

Le sampler ne « comprend » pas les tokens. Il reçoit leur ordre et leurs poids.
Une permutation des probabilités sans la même permutation des identifiants
produit un résultat incohérent.

### État du générateur pseudo-aléatoire

Une seed crée un état initial. Chaque tirage consomme cet état et produit le
suivant. Réinitialiser le générateur avec la même seed à chaque token ne rejoue
pas une génération normale : cela réutilise la première valeur uniforme à
chaque étape.

Un générateur dédié par run évite qu'un autre appel concurrent consomme la
séquence aléatoire globale. Son état peut être enregistré pour diagnostiquer ou
reprendre une expérience, à condition que tout le calcul déterministe autour
reste identique.

### La seed ne suffit pas

Pour reproduire une trajectoire, il faut notamment conserver :

- checkpoint et précision des poids ;
- tokenizer, Template et entrée exacte ;
- ordre et paramètres des transformations ;
- runtime, version des bibliothèques et device ;
- algorithmes déterministes ou non ;
- seed et état du générateur ;
- politique de cache et de batch susceptible de modifier les calculs.

PyTorch ne garantit pas une reproductibilité complète entre versions,
plateformes ou exécutions CPU et GPU. Certaines opérations disposent d'une
variante déterministe ; l'activer peut réduire les performances ou provoquer
une erreur lorsqu'aucune variante n'est disponible.

### Greedy et départage

Greedy ne consomme pas de hasard. Avec des logits strictement ordonnés et le
même calcul numérique, il choisit le même indice.

Deux valeurs égales demandent une convention, souvent le premier indice
maximal. Deux runtimes peuvent aussi arrondir différemment des scores presque
égaux. « Sans sampling » est donc une condition nécessaire mais pas toujours
suffisante pour une égalité bit à bit entre environnements.

### Reproductibilité contre qualité

Reproduire un résultat permet de diagnostiquer une transformation ou une
régression. Cela ne montre pas que la sortie est bonne. Inversement, plusieurs
seeds sont nécessaires pour évaluer une stratégie stochastique ; un exemple
favorable ne mesure pas sa distribution de qualité.

## Reconstruction

Injecter une instance locale de `Random` :

```python
from random import Random

def tirer(probabilites: list[float], rng: Random) -> int:
    if not probabilites or any(poids < 0.0 for poids in probabilites):
        raise ValueError("poids non négatifs requis")
    total = sum(probabilites)
    if total <= 0.0:
        raise ValueError("distribution vide")
    seuil = rng.random() * total
    cumul = 0.0
    for index, poids in enumerate(probabilites):
        cumul += poids
        if seuil < cumul:
            return index
    return len(probabilites) - 1  # protège l'arrondi de la somme

rng_a = Random(1234)
rng_b = Random(1234)
serie_a = [tirer([0.1, 0.3, 0.6], rng_a) for _ in range(10)]
serie_b = [tirer([0.1, 0.3, 0.6], rng_b) for _ in range(10)]
assert serie_a == serie_b
```

Intercaler un tirage supplémentaire dans `rng_b` doit décaler la suite. Cette
variation rend l'état consommable du générateur visible.

## Décision et dépôt dans Praxis

- **Décision** — `Sampler` reçoit un générateur pseudo-aléatoire propre au run ;
  greedy utilise un chemin séparé.
- **Alternatives** — RNG global, seed passée à chaque appel, ou choix délégué au
  backend sans métadonnées.
- **Critère** — isoler les exécutions concurrentes et rendre l'expérience
  rejouable dans un environnement fixé.
- **Coût accepté** — la trace conserve seed, versions et configuration, sans
  promettre une portabilité bit à bit.
- **Condition de révision** — une reprise durable du RNG sera cadrée avec les
  checkpoints au Parcours 10.
- **Contrat** — `praxis.generation.Sampler`.
- **Invariant et tests** — un appel choisit un candidat autorisé ; deux
  générateurs ne partagent pas leur état ; mêmes entrées et même état donnent
  le même indice dans l'implémentation testée.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la reproductibilité entre Python,
  PyTorch, llama.cpp et un GPU.
- **Praxis ne garantit pas encore** — la reprise d'un run interrompu.
- **Échec provoqué** — un composant concurrent qui utilise le RNG global doit
  modifier la trajectoire et justifier son exclusion du contrat.
- **Ouverture ultérieure** —
  [[14-boucle-autoregressive|Réinjecter le token choisi]] et le Parcours 10
  pour la reprise durable.

## Se tester

1. Pourquoi réinitialiser la même seed avant chaque token est-il différent
   d'initialiser une fois le run ?
2. Comment un appel concurrent peut-il casser une expérience fondée sur un RNG
   global ?
3. Quelles données faut-il conserver en plus de la seed pour tenter de
   reproduire une génération locale ?
4. Greedy garantit-il une égalité bit à bit entre un CPU et un GPU ?
5. Pourquoi une seule seed ne suffit-elle pas pour comparer la qualité de deux
   configurations stochastiques ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#13--tirer-le-prochain-token).

## Références

- [PyTorch — Reproducibility, mise à jour du
  2025-10-03](https://docs.pytorch.org/docs/stable/notes/randomness.html) —
  portée des seeds et limites entre plateformes et versions.
- [PyTorch — `Generator`](https://docs.pytorch.org/docs/stable/generated/torch.Generator.html) —
  état, seed et clonage d'un générateur.
- [PyTorch — `multinomial`](https://docs.pytorch.org/docs/stable/generated/torch.multinomial.html) —
  tirage d'indices à partir de poids et générateur injecté.
- [Transformers — génération, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/main_classes/text_generation) —
  distinction `do_sample` et greedy.
