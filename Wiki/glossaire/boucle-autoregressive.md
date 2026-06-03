# boucle autorégressive

Boucle qui choisit un token, l’ajoute au préfixe puis recalcule la distribution
du token suivant. Chaque décision devient ainsi une donnée du tour suivant.

Avec le préfixe « le chat », si le tirage choisit « dort », le passage suivant prend
en compte « le chat dort ». Un autre tirage au premier tour aurait donné un autre
préfixe.
