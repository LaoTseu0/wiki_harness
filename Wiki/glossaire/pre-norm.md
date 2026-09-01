# pré-norm

Organisation d’un bloc Transformer où la normalisation précède le sous-bloc
d’attention ou le MLP. La sortie du sous-bloc est ensuite ajoutée au chemin
résiduel.

Dans `x + F(Norm(x))`, le sous-bloc F reçoit une entrée normalisée. Le terme x qui
rejoint directement la somme conserve sa valeur.

[Suivre les deux chemins jusqu’à l’addition](../parcours/0-generation/08-residual-normalisation.md#connaissances)
