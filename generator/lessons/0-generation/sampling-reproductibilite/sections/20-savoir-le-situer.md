## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : logits transformés → sampling → ajout du token → boucle.

**Étape ouverte** —
`transformation-logits → sampling → ajout-token`.  
Input : distribution finie, normalisée et non vide. Output : un identifiant de
token.  
Responsabilité : effectuer exactement un tirage catégoriel avec une source
d'aléa explicite, ou appliquer l'argmax demandé.

**L'essentiel** — le sampling tire un indice selon les poids finaux. Une seed
initialise l'état d'un générateur pseudo-aléatoire ; elle ne fige ni les logits
ni les calculs qui les ont produits.

**Recomposer** — le token choisi est ajouté à la séquence. Cette décision
modifie le prochain passage avant, de sorte qu'une divergence unique peut
entraîner une trajectoire entièrement différente.

![[sampling-reproductibilite.canvas]]
