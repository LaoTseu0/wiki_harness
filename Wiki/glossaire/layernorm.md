# LayerNorm

Normalisation qui centre et réduit les composantes d’un vecteur avant
d’appliquer des paramètres appris d’échelle et de décalage.

Pour le vecteur (2, 4), le centrage soustrait 3 et donne (−1, 1), avant la division
par l’écart-type régularisé et la transformation affine.
