## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/inference-transformer.canvas|passage avant d'un Transformer
decoder-only]].  
[[glossaire/input|Input]] global : identifiants de [[glossaire/token|tokens]] et cache éventuel. [[glossaire/output|Output]] global : [[glossaire/logit|logits]]
du prochain **token**.  
Grandes étapes : blocs répétés → normalisation finale → projection vocabulaire
→ **logits**.

**Étape ouverte** —
`normalisation-finale → projection-vocabulaire → logits-sortie`.  
**Input** : représentation finale de dimension cachée. **Output** : un score par entrée
du vocabulaire.  
Responsabilité : ramener l'état du modèle dans l'espace discret des candidats.

**L'essentiel** — la tête de langage applique une projection linéaire vers la
taille du vocabulaire. Ses sorties sont des scores relatifs, pas encore des
probabilités.

**Recomposer** — les **logits** quittent le sous-processus d'inférence et rejoignent
le processus de génération, où les contraintes, pénalités, filtres et softmax
décideront du prochain **token**.

![[projection-logits.canvas]]
