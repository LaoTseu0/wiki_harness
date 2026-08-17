# Grouped-Query Attention

Variante d’attention qui partage moins de têtes de clés et de valeurs entre un
plus grand nombre de têtes de requêtes. Ce partage réduit notamment la taille
du cache KV.

Avec huit têtes de requêtes réparties en deux groupes égaux, quatre têtes consultent
la même tête de clés et de valeurs dans chaque groupe.

[Voir comment plusieurs requêtes partagent leurs clés et valeurs](../parcours/0-generation/07-attention-causale.md#connaissances)
