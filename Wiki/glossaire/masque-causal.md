# masque causal

Contrainte qui empêche une position de consulter les positions futures pendant
l’attention. Elle préserve la factorisation autorégressive du calcul.

Sur trois positions, la deuxième ligne du masque autorise les colonnes 1 et 2. La
colonne 3 est exclue avant de normaliser les scores de cette ligne.

[Localiser le masque dans le calcul de l’attention](../parcours/0-generation/07-attention-causale.md#connaissances)
