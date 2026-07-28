## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : inférence → [[glossaire/logit|logits]] → transformations → [[glossaire/sampling|sampling]] → ajout du
token.

**Étape ouverte** — `inference → logits → transformation-logits`.  
**Input** : un score réel par token du vocabulaire. **Output** : les mêmes candidats,
interprétables relativement et convertibles en probabilités.  
Responsabilité : préserver l'association identifiant–score et normaliser
numériquement lorsque la transformation l'exige.

**L'essentiel** — [[glossaire/softmax|softmax]] exponentie les écarts de **logits** et normalise leur
somme. La distribution obtenue décrit le prochain token conditionnellement au
préfixe exact, pas la vérité d'une réponse entière.

**Recomposer** — les transformations de **sampling** peuvent agir directement sur
les **logits** ou consulter leur **softmax**. Après filtrage, les candidats conservés
doivent former une distribution valide avant le tirage.

![[logits-softmax.canvas]]
