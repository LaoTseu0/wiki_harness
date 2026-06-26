# MoE

Abréviation de *Mixture of Experts*. Cette architecture route chaque position
vers une partie seulement de plusieurs sous-réseaux spécialisés.

Avec huit experts et un routeur qui en retient deux par token, deux tokens voisins
peuvent être envoyés à des paires d’experts différentes.
