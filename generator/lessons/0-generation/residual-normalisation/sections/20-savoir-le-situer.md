## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer
decoder-only]].  
[[glossaire/input|Input]] global : identifiants de tokens et cache éventuel. [[glossaire/output|Output]] global : logits
du prochain token.  
Grandes étapes : normaliser → attention → ajouter au résidu → normaliser → [[glossaire/mlp|MLP]]
→ ajouter au résidu.

**Étape ouverte** —
`attention-causale → residu-attention → normalisation-mlp`.  
**Input** : [[glossaire/residual-stream|residual stream]] d'entrée et mise à jour d'attention. **Output** : leur somme
transmise au second sous-bloc.  
Responsabilité : préserver le chemin principal tout en y accumulant une mise à
jour contextualisée.

**L'essentiel** — dans un bloc [[glossaire/pre-norm|pré-norm]] courant, la normalisation prépare
l'entrée d'un sous-bloc, puis sa sortie est ajoutée au **residual stream**. La
normalisation et la connexion résiduelle ont des fonctions distinctes.

**Recomposer** — l'attention et le **MLP** écrivent successivement dans le même flux
de représentations. Ce flux traverse les couches et atteint finalement la
projection vocabulaire.

![[residual-normalisation.canvas]]
