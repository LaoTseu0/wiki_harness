# decode

Phase incrémentale qui traite chaque nouvelle position après le prefill. Elle
réutilise le cache disponible pour éviter de recalculer tout le préfixe.

Après le prefill, le modèle propose un premier token. Le réinjecter avec le cache
permet de calculer les scores du token suivant sur une seule nouvelle position.
