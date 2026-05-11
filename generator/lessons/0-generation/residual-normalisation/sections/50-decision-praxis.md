## Décision et dépôt dans Praxis

- **Décision** — Praxis décrit l'ordre des sous-blocs à partir de la
  configuration du modèle ; il ne généralise pas le Canvas pré-norm à tous les
  checkpoints.
- **Alternatives** — enseigner seulement « chaque couche transforme le
  tenseur », ou reproduire le kernel de normalisation.
- **Critère** — l'ordre résidu–normalisation explique les points d'inspection et
  les divergences entre architectures.
- **Coût accepté** — la reconstruction ne simule pas la précision mixte.
- **Condition de révision** — un modèle local d'une autre famille exigera son
  propre relevé architectural.
- **Contrat** — aucun contrat public dans `generation`.
- **Invariant et tests** — les additions résiduelles conservent la forme ; la
  normalisation applique l'epsilon configuré.
