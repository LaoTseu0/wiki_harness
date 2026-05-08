## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer
decoder-only]].  
Input global : identifiants de tokens et cache éventuel. Output global : logits
du prochain token.  
Grandes étapes : attention et résidu → normalisation du MLP → MLP → second
résidu → couche suivante.

**Étape ouverte** —
`normalisation-mlp → mlp → residu-mlp`.  
Input : représentation normalisée de chaque position. Output : une mise à jour
de la dimension cachée pour chaque position.  
Responsabilité : transformer les composantes d'un token sans agréger d'autres
positions.

**L'essentiel** — le MLP applique les mêmes projections et non-linéarités à
chaque position indépendamment. L'attention mélange les positions ; le MLP
mélange les caractéristiques à l'intérieur de chaque position.

**Recomposer** — la mise à jour du MLP rejoint le residual stream, puis le bloc
suivant peut à nouveau faire interagir les positions par attention.

![[mlp-transformer.canvas]]
