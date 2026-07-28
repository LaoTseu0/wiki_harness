## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : [[glossaire/logit|logits]] → transformations → sampling → ajout au contexte.

**Étape ouverte** —
`logits → transformation-logits → sampling`.  
**Input** : **logits** bruts, historique de tokens et configuration. **Output** : un
ensemble de candidats pondérés et non vide.  
Responsabilité : modifier ou exclure des candidats avant le tirage, dans un
ordre explicite.

**L'essentiel** — [[glossaire/temperature|température]], pénalités et filtres ne rendent pas le modèle
plus savant. Ils transforment localement les scores du prochain token et
changent ainsi les trajectoires accessibles.

**Recomposer** — le sampler ne voit que la distribution finale. Une
transformation mal ordonnée ou un ensemble vide se propage immédiatement au
token choisi puis à toutes les inférences suivantes.

![[filtrage-distribution.canvas]]
