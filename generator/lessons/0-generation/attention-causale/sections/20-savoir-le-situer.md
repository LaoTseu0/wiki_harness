## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer
decoder-only]].  
[[glossaire/input|Input]] global : identifiants de tokens et cache éventuel. [[glossaire/output|Output]] global : logits
du prochain token.  
Grandes étapes : embeddings → normalisation d'attention → [[glossaire/attention-causale|attention causale]] →
résidu → MLP → projection.

**Étape ouverte** —
`normalisation-attention → attention-causale → residu-attention`.  
**Input** : residual stream normalisé et masque. **Output** : une mise à jour qui
agrège les valeurs des positions autorisées.  
Responsabilité : calculer, pour chaque requête, une combinaison pondérée du
passé accessible.

**L'essentiel** — `Q` cherche, `K` décrit ce qui peut correspondre et `V`
transporte la contribution. Le produit `QKᵀ`, mis à l'échelle, masqué puis
normalisé, fournit les poids appliqués à `V`.

**Recomposer** — la sortie d'attention ne remplace pas le residual stream. Elle
est projetée puis ajoutée par la connexion résiduelle avant le sous-bloc MLP.

![[attention-causale.canvas]]
