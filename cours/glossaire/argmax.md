# argmax

> [glossaire](index.md)

L'opération qui renvoie l'élément de plus grande valeur — ici, le token dont
le [logit](logits.md) est le plus élevé. Choisir toujours l'argmax, c'est la
génération *gloutonne* (greedy) : déterministe au niveau de la stratégie,
répétitive en pratique. La [temperature](../fondamentaux/sampling-et-prompting.md)
tend vers l'argmax quand elle tend vers 0.
