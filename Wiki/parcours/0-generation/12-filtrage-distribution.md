---
id: filtrage-distribution
type: leçon
titre: Transformer la distribution
parcours: 0-generation
statut: brouillon
tags: [generation, sampling, temperature, top-p]
created: 2026-07-27
updated: 2026-07-29
verified: 2026-07-27
processus: generation-token
etape: transformation-logits
brique: generation
contrat: praxis.generation.LogitsPipeline
---

# Transformer la distribution

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-12--déformer-une-même-distribution)

## Prérequis

- [[11-logits-softmax|Des logits à une distribution]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : [[glossaire/logit|logits]] → transformations → sampling → ajout au contexte.

**Étape ouverte** —
`logits → transformation-logits → sampling`.  
**Input** : **logits** bruts, historique de tokens et configuration. **Output** : un
ensemble de candidats pondérés et non vide.  
Responsabilité : modifier ou exclure des candidats avant le tirage, dans un
ordre explicite.

**L'essentiel** — [[glossaire/temperature|température]], pénalités et filtres ne rendent pas le modèle
plus savant. Ils transforment localement les scores du prochain token et
changent ainsi les trajectoires accessibles.

**Recomposer** — le sampler ne voit que la distribution finale. Une
transformation mal ordonnée ou un ensemble vide se propage immédiatement au
token choisi puis à toutes les inférences suivantes.

![[filtrage-distribution.canvas]]

## Connaissances

### Une chaîne ordonnée

Une pipeline de **logits** peut contenir :

1. des contraintes dures ou des biais ;
2. des pénalités dépendant de l'historique ;
3. une **température** ;
4. un ou plusieurs filtres de candidats ;
5. une renormalisation avant tirage.

Cet ordre n'est pas universel. Il doit être fixé par Praxis et comparé à celui
du runtime utilisé. Les opérations ne sont généralement pas commutatives :
appliquer [[glossaire/top-p|top-p]] avant la **température** peut conserver un autre ensemble
qu'appliquer la **température** avant **top-p**.

### **Température**

Pour une **température** $T>0$, les **logits** deviennent :

$$
z'_i = z_i/T
$$

Une **température** inférieure à un agrandit les écarts et concentre la
distribution. Une **température** supérieure à un les réduit et aplatit la
distribution. $T=1$ ne change rien.

Diviser par zéro n'implémente pas [[glossaire/greedy|greedy]]. Les runtimes utilisent une branche
argmax explicite lorsque le sampling est désactivé ou qu'une interface traite
`temperature=0` comme un raccourci. Mathématiquement, quand $T$ tend vers
zéro, la masse se concentre sur les maxima ; les égalités demandent encore une
règle de départage.

### [[glossaire/top-k|Top-k]]

**Top-k** conserve les `k` **logits** les plus élevés et masque les autres. Son nombre
de candidats est fixe, même lorsque la distribution est très concentrée ou
très plate.

`k=1` suivi d'un tirage équivaut à choisir l'argmax sous une règle de départage
donnée. Une valeur supérieure à la taille du vocabulaire ne doit pas provoquer
un dépassement.

### **Top-p**

**Top-p**, ou nucleus sampling, trie les candidats par probabilité décroissante et
conserve le plus petit préfixe dont la masse cumulée atteint ou dépasse `p`. Le
nombre de candidats s'adapte donc à la forme de la distribution.

Le token qui franchit le seuil est conservé. Retirer tous les tokens une fois
la somme supérieure à `p` peut exclure précisément celui qui permet d'atteindre
le seuil.

### [[glossaire/min-p|Min-p]]

**Min-p** compare chaque probabilité $p_i$ à une fraction $\alpha$ de la
probabilité maximale :

$$
p_i \geq \alpha\,p_{\max}
$$

Le seuil devient plus strict lorsque le meilleur candidat domine et plus
permissif lorsque la distribution est plate. L'implémentation conserve au
moins un nombre minimal de candidats pour éviter un ensemble vide.

### Trois familles de pénalités de répétition

Une *repetition penalty* courante, issue de CTRL et reprise par Transformers,
modifie au plus une fois le **logit** de chaque token déjà présent : un **logit**
positif est divisé par la pénalité, un **logit** négatif est multiplié. La valeur
`1` désactive cette transformation.

Une pénalité de présence additive retire une constante si le token a déjà été
vu. Une pénalité de fréquence retire une valeur proportionnelle au nombre
d'occurrences :

$$
z'_i = z_i - \alpha_p\,\mathbf{1}[c_i>0] - \alpha_f c_i
$$

Ces formules et la fenêtre d'historique varient selon les runtimes. Les noms de
paramètres semblables ne garantissent pas la même opération.

### **Greedy**

**Greedy** choisit un indice de **logit** maximal sans tirage. Il est localement
optimal pour le prochain token, pas pour la probabilité ou la qualité de toute
la séquence.

Il supprime l'aléa du sampler, mais pas nécessairement toutes les divergences
numériques entre runtimes si deux scores sont proches ou égaux.

## Reconstruction

Implémenter trois filtres sur des couples `(token_id, probabilité)` :

```python
def top_k(probs: list[float], k: int) -> set[int]:
    if k <= 0:
        raise ValueError("k doit être positif")
    ordre = sorted(range(len(probs)), key=probs.__getitem__, reverse=True)
    return set(ordre[:min(k, len(probs))])

def top_p(probs: list[float], seuil: float) -> set[int]:
    if not 0.0 < seuil <= 1.0:
        raise ValueError("top_p hors limites")
    ordre = sorted(range(len(probs)), key=probs.__getitem__, reverse=True)
    gardes, cumul = set(), 0.0
    for index in ordre:
        gardes.add(index)
        cumul += probs[index]
        if cumul >= seuil:
            break
    return gardes

def min_p(probs: list[float], alpha: float) -> set[int]:
    limite = alpha * max(probs)
    gardes = {index for index, p in enumerate(probs) if p >= limite}
    return gardes or {probs.index(max(probs))}
```

Appliquer ces fonctions à une distribution plate puis à une distribution
concentrée rend leur différence structurelle visible.

## Décision et dépôt dans Praxis

- **Décision** — `LogitsPipeline` est une séquence ordonnée de transformations
  pures. Chaque étape peut exposer les candidats conservés au laboratoire.
- **Alternatives** — un objet de configuration sans ordre ; déléguer tous les
  réglages au backend.
- **Critère** — rendre les mécanismes comparables entre le sampler reconstruit
  et les runtimes.
- **Coût accepté** — Praxis doit versionner la sémantique et l'ordre de la
  pipeline.
- **Condition de révision** — une nouvelle stratégie n'entre dans le socle que
  si elle change une décision utile ; les samplers exotiques restent au
  glossaire ou dans la veille.
- **Contrat** — `praxis.generation.LogitsPipeline`.
- **Invariant et tests** — au moins un candidat reste fini ; les tokens masqués
  ne peuvent pas être tirés ; l'ordre est stable et tracé.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — qu'un réglage améliore la qualité sur
  toutes les tâches ou tous les modèles.
- **Praxis ne garantit pas encore** — une équivalence avec un backend qui
  n'expose pas l'ordre de ses samplers.
- **Échec provoqué** — une combinaison de contraintes qui masque tous les
  candidats doit produire une erreur explicite.
- **Ouverture ultérieure** —
  [[13-sampling-reproductibilite|Tirer le prochain token]].

## Se tester

1. Pourquoi **température** puis **top-p** peut-il conserver un autre ensemble que
   **top-p** puis **température** ?
2. Quelle différence structurelle sépare **top-k** et **top-p** ?
3. Comment le seuil de **min-p** réagit-il lorsque le meilleur token devient très
   probable ?
4. Pourquoi présence, fréquence et repetition penalty ne sont-elles pas trois
   noms pour la même formule ?
5. **Greedy** maximise-t-il la probabilité de toute la séquence ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#12--transformer-la-distribution).

## Références

- [Holtzman et al., *The Curious Case of Neural Text Degeneration*,
  v2](https://arxiv.org/abs/1904.09751) — nucleus sampling.
- [Nguyen et al., *Turning Up the Heat: Min-p Sampling*, v2](https://arxiv.org/abs/2407.01082) —
  seuil relatif au candidat maximal.
- [Keskar et al., *CTRL*, v2](https://arxiv.org/abs/1909.05858) — repetition
  penalty.
- [Transformers — `GenerationConfig`, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig) —
  paramètres de **température**, **top-k**, **top-p**, **min-p** et répétition.
- [Transformers — `logits_process.py`, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/generation/logits_process.py) —
  formules d'implémentation et garanties minimales.

