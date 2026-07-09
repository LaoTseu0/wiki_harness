# RoPE

Abréviation de *Rotary Position Embedding*. Cette méthode encode la position en
appliquant aux requêtes et aux clés des rotations dont l’angle dépend de leur
indice.

À la position zéro, l’angle de rotation standard est nul. À la position suivante, la
même paire de composantes est tournée d’un angle fixé par sa fréquence.
