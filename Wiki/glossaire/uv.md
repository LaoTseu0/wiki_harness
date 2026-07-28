# uv

Outil de projet Python capable notamment de résoudre des dépendances, maintenir
un lockfile, synchroniser un environnement et lancer des commandes.

Dans un projet muni d’un `uv.lock` à jour, `uv sync --locked` synchronise
l’environnement en exigeant que la résolution enregistrée reste applicable.
