## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : ajout → détokenisation → décision d'arrêt → réponse ou
réinjection.

**Étape ouverte** —
`detokenisation → condition-arret → reponse | reinjection`.  
Input : token choisi, texte stabilisé, compteurs et signaux externes. Output :
décision `continuer` ou raison d'arrêt typée.  
Responsabilité : terminer toujours la boucle selon une priorité documentée et
sans publier un marqueur exclu.

**L'essentiel** — EOS, stop sequence et budget de sortie sont des mécanismes
différents. Une génération bornée possède au moins une limite dure indépendante
de la bonne volonté du modèle.

**Recomposer** — `continuer` réinjecte la séquence. Toute autre décision ferme
le décodeur, publie le suffixe autorisé et produit avec la réponse une raison
d'arrêt exploitable.

![[conditions-arret.canvas]]
