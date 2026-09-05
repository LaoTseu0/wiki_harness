# RMSNorm

Normalisation qui met un vecteur à l’échelle d’après sa moyenne quadratique,
sans soustraire sa moyenne. Un facteur appris ajuste ensuite chaque composante.

Pour le vecteur (3, 4), la moyenne des carrés vaut 12,5. Avant l’échelle apprise,
chaque composante est divisée par √(12,5 + ε).

[Retrouver le dénominateur de RMSNorm](../parcours/0-generation/08-residual-normalisation.md#connaissances)
