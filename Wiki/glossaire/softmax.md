# softmax

Fonction qui exponentie des scores puis les divise par leur somme. Elle produit
des valeurs non négatives dont la somme vaut un et conserve l’ordre des scores.

Pour trois logits égaux, les trois exponentielles sont égales. Après division par leur
somme, chaque candidat reçoit une probabilité de 1/3.
