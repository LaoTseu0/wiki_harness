# SwiGLU

Variante de MLP à porte qui combine une branche activée par SiLU avec une
seconde projection. Le produit des deux branches est ensuite reprojeté.

Si une composante de la branche activée vaut zéro, le produit annule la composante
correspondante de l’autre branche avant la projection de sortie.

[Retrouver le produit entre les deux branches du MLP](../parcours/0-generation/09-mlp-transformer.md#connaissances)
