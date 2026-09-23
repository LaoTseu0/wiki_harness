# top-p

Filtre qui conserve le plus petit préfixe de candidats triés dont la probabilité
cumulée atteint un seuil `p`, puis renormalise cet ensemble.

Pour des probabilités triées de 0,55, 0,30 et 0,15, un seuil de 0,80 retient les deux
premiers candidats. Leur somme atteint 0,85.

[Trouver le candidat qui fait franchir le seuil](../parcours/0-generation/12-filtrage-distribution.md#connaissances)
