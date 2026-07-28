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
