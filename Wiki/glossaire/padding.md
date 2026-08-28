# padding

Ajout de tokens de remplissage pour donner une longueur commune à plusieurs
séquences traitées ensemble. Un masque empêche normalement ces positions
d’influencer le calcul utile.

Dans un lot de séquences de longueurs 2 et 4, deux tokens de remplissage peuvent
compléter la première ligne. Le masque doit en signaler les positions au modèle.

[Distinguer le remplissage des tokens de contenu](../parcours/0-generation/03-tokens-controle.md#connaissances)
