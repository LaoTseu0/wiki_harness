## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : messages → [[glossaire/template|Template]] de chat → tokenisation → inférence →
boucle.

**Étape ouverte** — `messages → chat-template → tokenisation`.  
**Input** : une liste ordonnée de messages et les options du tour. **Output** : une
séquence sérialisée ou directement tokenisée.  
Responsabilité : reproduire exactement le format appris par le modèle.

**L'essentiel** — un modèle [[glossaire/decoder-only|decoder-only]] ne reçoit pas une liste de messages.
Le **Template** transforme les rôles et contenus en une séquence unique où les
délimiteurs, espaces et [[glossaire/token-de-controle|tokens de contrôle]] font partie de l'entrée.

**Recomposer** — le texte produit devient l'**Input** du [[glossaire/tokenizer|tokenizer]]. Une différence
de **Template** change tous les identifiants à partir de son premier écart et donc
la trajectoire de génération.

![[templates-chat.canvas]]
