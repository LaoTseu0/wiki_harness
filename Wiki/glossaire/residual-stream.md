# residual stream

Flux de représentations auquel les sous-blocs d’un Transformer ajoutent leurs
mises à jour. Les connexions résiduelles conservent ainsi un chemin direct à
travers les couches.

Si une représentation vaut (2, 1) et qu’un sous-bloc propose la mise à jour (−1, 3),
l’addition transmet (1, 4) au calcul suivant.
