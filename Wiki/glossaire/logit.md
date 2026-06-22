# logit

Score réel non normalisé attribué à un candidat. Seuls ses écarts avec les
autres logits déterminent la distribution obtenue après softmax.

Les couples de logits (1, 3) et (6, 8) donnent les mêmes probabilités après softmax.
Dans les deux cas, l’écart entre les candidats vaut 2.
