# seed

Valeur utilisée pour initialiser un générateur pseudo-aléatoire. Elle ne
garantit une répétition identique que si l’algorithme, l’ordre des appels et
l’environnement restent compatibles.

Deux générateurs initialisés avec la même seed peuvent diverger dans leur usage si
l’un consomme un tirage supplémentaire avant de choisir le premier token.

[Identifier les autres conditions d’une répétition](../parcours/0-generation/13-sampling-reproductibilite.md#connaissances)
