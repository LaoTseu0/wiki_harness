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
