# backend de build

Composant appelé par un frontend pour transformer les sources Python en
artefacts distribuables selon le contrat déclaré dans `pyproject.toml`.

Quand un outil construit une wheel à partir des sources, il consulte la table
`[build-system]` de `pyproject.toml` pour savoir quel backend appeler.
