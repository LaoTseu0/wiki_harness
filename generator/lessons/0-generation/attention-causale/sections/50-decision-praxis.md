## Décision et dépôt dans Praxis

- **Décision** — le laboratoire reconstruit une tête pour expliquer les
  invariants ; Praxis délègue l'attention réelle au runtime.
- **Alternatives** — traiter l'attention comme une recherche vectorielle, ou
  réimplémenter toutes les variantes de kernels.
- **Critère** — ouvrir le calcul qui explique le contexte et le cache sans
  confondre harnais et moteur d'inférence.
- **Coût accepté** — la reconstruction ignore le batch, les têtes et les kernels
  optimisés.
- **Condition de révision** — aucune ; les optimisations seront comparées au
  Parcours 1.
- **Contrat** — aucun contrat public dans `generation`.
- **Invariant et tests** — un token futur a un poids nul ; les poids autorisés
  somment à un à la tolérance numérique choisie.
