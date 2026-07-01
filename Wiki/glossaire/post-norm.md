# post-norm

Organisation d’un bloc Transformer où la normalisation suit l’addition
résiduelle. Elle ne place donc pas la normalisation au même endroit qu’un bloc
pré-norm.

Dans une écriture simplifiée, `Norm(x + F(x))` normalise la somme. La représentation
issue du chemin résiduel participe donc elle aussi au calcul de la moyenne ou de
l’échelle.
