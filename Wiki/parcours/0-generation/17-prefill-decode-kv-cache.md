---
id: prefill-decode-kv-cache
type: leçon
titre: Prefill, decode et cache KV
parcours: 0-generation
statut: brouillon
tags: [generation, inference, kv-cache, prefill]
created: 2026-07-27
updated: 2026-07-29
verified: 2026-07-27
processus: generation-token
etape: inference
brique: generation
contrat: praxis.generation.NextTokenModel
---

# Prefill, decode et cache KV

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-17--comparer-avec-et-sans-cache)

## Prérequis

- [[06-position-rope|Représenter la position]]
- [[07-attention-causale|L'attention causale]]
- [[14-boucle-autoregressive|Réinjecter le token choisi]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]],
dont l'étape `inference` ouvre
[[generator/guardrails/schema/processus/inference-transformer.canvas|le passage avant du
Transformer]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : tokenisation → inférence → logits → boucle.

**Étape ouverte** — `tokenisation | reinjection → inference → logits`.  
**Input** : prompt complet au premier passage, puis nouveau token et cache
compatible. **Output** : logits du prochain token et cache étendu.  
Responsabilité : distinguer le calcul initial du préfixe de l'extension
incrémentale.

**L'essentiel** — le [[glossaire/prefill|prefill]] calcule le prompt et construit les clés et valeurs
de chaque couche. Le [[glossaire/decode|decode]] réutilise ce cache et ne calcule les nouveaux
états que pour les positions ajoutées.

**Recomposer** — le cache accélère les retours de la boucle vers l'inférence,
mais ne change ni le [[glossaire/tokenizer|tokenizer]], ni la politique de [[glossaire/sampling|sampling]], ni la condition
d'arrêt.

![[prefill-decode-kv-cache.canvas]]

## Connaissances

### **Prefill**

Le **prefill** traite les $N$ tokens du prompt sous masque causal. Les opérations
sur les positions peuvent être exécutées en parallèle parce que toutes les
valeurs du prompt sont déjà connues.

Chaque couche produit les clés et valeurs correspondant à ces positions. Le
runtime conserve celles qui seront nécessaires aux futurs calculs d'attention.
Le premier logit de génération provient de la dernière position utile du
**prefill**.

Le temps avant le premier token inclut donc Template, tokenisation, transfert
des entrées, **prefill** et choix du premier token. Il ne se réduit pas au seul
**sampling**.

### **Decode**

Après avoir choisi un token, le **decode** calcule sa nouvelle représentation
position par position. À chaque couche :

1. produire `Q`, `K` et `V` pour la nouvelle position ;
2. appliquer sa position à `Q` et `K` ;
3. ajouter le nouveau `K` et `V` au cache ;
4. comparer la nouvelle requête aux clés accessibles ;
5. agréger les valeurs et poursuivre le bloc.

Sans cache, le runtime recalculerait les projections `K` et `V` de tout le
préfixe à chaque tour. Avec cache, il les relit.

### Ce que le cache contient

Un [[glossaire/cache-kv|cache KV]] courant contient, pour chaque couche, les clés et valeurs des
positions conservées, ainsi que les informations permettant de les positionner
et de les masquer correctement.

Il ne contient pas :

- une réponse future ;
- les requêtes de toutes les étapes comme une obligation générale ;
- la sortie du MLP comme substitut au passage de la nouvelle position ;
- une mémoire sémantique réutilisable par n'importe quel modèle.

### Le coût n'est pas supprimé

Avec une attention complète standard, la nouvelle requête doit encore être
comparée aux clés précédentes. Le travail d'attention et la mémoire du cache
croissent avec le nombre de positions conservées.

Le cache évite surtout de recalculer les représentations passées. Il échange de
la mémoire contre du calcul. Une attention à fenêtre glissante ou par chunks
peut borner certaines couches, mais change la portée du contexte accessible.

### Stratégies de cache

- un cache dynamique grandit avec la séquence ;
- un cache statique préalloue une capacité et facilite certaines compilations,
  au prix d'espace et de calcul masqué ;
- un cache déporté échange des transferts contre de la mémoire accélérateur ;
- un cache quantifié réduit la mémoire avec un coût de conversion et une
  possible perte numérique.

Ces propriétés doivent être mesurées sur le runtime et le matériel concernés.

### Compatibilité

Un cache dépend au minimum du checkpoint, des couches, de la convention de
position, du préfixe exact et de la configuration d'attention. Le réutiliser
avec un autre Template ou un autre modèle donne des états sans rapport avec le
nouvel **Input**.

Partager un cache de préfixe stable peut être une optimisation volontaire. Le
préfixe doit être identique au niveau des identifiants et sa frontière de
confidentialité doit être respectée.

## Reconstruction

Compter les positions retraitées dans une boucle conceptuelle :

```python
def positions_sans_cache(prompt: int, nouveaux: int) -> int:
    return sum(prompt + deja_generes for deja_generes in range(nouveaux))

def positions_avec_cache(prompt: int, nouveaux: int) -> int:
    if nouveaux == 0:
        return 0
    return prompt + (nouveaux - 1)

assert positions_sans_cache(100, 10) == 1045
assert positions_avec_cache(100, 10) == 109
```

Ce compteur représente les positions données aux projections du modèle, pas le
nombre d'opérations d'attention ni une latence. Même avec cache, chaque nouvelle
requête parcourt encore les clés autorisées dans une attention complète.

## Décision et dépôt dans Praxis

- **Décision** — `NextTokenModel` sépare `prefill(token_ids)` et
  `decode(token_id, cache)` tout en permettant un adaptateur plus simple pour
  les backends sans cache exposé.
- **Alternatives** — une méthode qui reçoit toujours toute la séquence, ou un
  cache global caché dans le provider.
- **Critère** — rendre visible la durée de vie et la compatibilité du cache.
- **Coût accepté** — le type de cache reste opaque pour ne pas imposer une
  forme tensorielle à tous les runtimes.
- **Condition de révision** — le Parcours 1 comparera les stratégies concrètes ;
  le Parcours 3 décidera la réutilisation de préfixes de session.
- **Contrat** — `praxis.generation.NextTokenModel` et référence de cache opaque.
- **Invariant et tests** — un cache appartient à un modèle et à un préfixe ; la
  position avance exactement avec les tokens ajoutés ; avec ou sans cache, les
  logits restent équivalents à la tolérance du runtime.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — un gain de latence réel.
- **Praxis ne garantit pas encore** — la sérialisation ou la portabilité d'un
  cache.
- **Échec provoqué** — appliquer un cache construit avec un prompt à un autre
  prompt doit être refusé.
- **Ouverture ultérieure** —
  [[18-fenetre-contexte-cout|Fenêtre de contexte et coût]] puis le Parcours 1
  pour les benchmarks de runtime.

## Se tester

1. Quelle différence de disponibilité des tokens sépare **prefill** et **decode** ?
2. Quelles projections le cache évite-t-il de recalculer pour le préfixe ?
3. Pourquoi le coût d'attention du **decode** continue-t-il de croître avec une
   attention complète ?
4. Quelles identités doivent être compatibles avant de réutiliser un cache ?
5. Un **cache KV** est-il une mémoire agentique ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#17--prefill-decode-et-cache-kv).

## Références

- [Transformers — Cache strategies, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/kv_cache) — caches
  dynamique, statique, déporté et quantifié.
- [Transformers — Caching](https://huggingface.co/docs/transformers/cache_explanation) —
  mise à jour par couche, positions et masque.
- [Transformers — implémentation Llama, révision `main`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  production et mise à jour des clés et valeurs.

