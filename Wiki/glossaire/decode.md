# decode

Phase incrémentale qui traite chaque nouvelle position après le prefill. Elle
réutilise le cache disponible pour éviter de recalculer tout le préfixe.
