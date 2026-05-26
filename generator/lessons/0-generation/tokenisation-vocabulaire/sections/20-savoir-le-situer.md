## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : Template de chat → tokenisation → inférence → transformation
des logits → sampling → boucle et arrêt.

**Étape ouverte** — `chat-template → tokenisation → inference`.  
**Input** : texte sérialisé. **Output** : identifiants du [[glossaire/vocabulaire|vocabulaire]].  
Responsabilité : appliquer les règles exactes du [[glossaire/tokenizer|tokenizer]] associé au modèle.

**L'essentiel** — le **tokenizer** transforme une séquence textuelle en
identifiants discrets. Son **vocabulaire**, sa normalisation, son pré-découpage et
son algorithme font partie du contrat du modèle.

**Recomposer** — changer de **tokenizer** change les identifiants envoyés à la
table d'embeddings. Même si le texte affiché reste identique, le modèle reçoit
alors une autre entrée.

![[tokenisation-vocabulaire.canvas]]
