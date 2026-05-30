# attention causale

Mécanisme d’attention où chaque position agrège seulement les positions déjà
disponibles. Le masque causal retire les positions futures avant la
normalisation des scores.

Dans la séquence « le chat dort », la position de « chat » peut consulter « le » et «
chat ». Le score qui la relie à « dort » est masqué.
