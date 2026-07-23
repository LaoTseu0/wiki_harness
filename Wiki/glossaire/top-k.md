# top-k

Filtre qui ne conserve que les `k` candidats aux scores les plus élevés avant
de renormaliser la distribution.

Avec des scores de 7, 4, 2 et 1, top-k réglé à 2 conserve les deux premiers candidats.
Le tirage se fait sur les probabilités renormalisées de ces deux candidats.
