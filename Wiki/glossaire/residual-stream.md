# residual stream

Flux de représentations auquel les sous-blocs d’un Transformer ajoutent leurs
mises à jour. Les connexions résiduelles conservent ainsi un chemin direct à
travers les couches.

Si une représentation vaut (2, 1) et qu’un sous-bloc propose la mise à jour (−1, 3),
l’addition transmet (1, 4) au calcul suivant.

[Suivre une mise à jour le long du chemin résiduel](../parcours/0-generation/08-residual-normalisation.md#connaissances)
