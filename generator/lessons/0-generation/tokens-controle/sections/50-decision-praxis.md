## Décision et dépôt dans Praxis

- **Décision** — Praxis charge les identifiants spéciaux depuis l'artefact du
  tokenizer et les fige dans `SpecialTokens`.
- **Alternatives** — coder en dur les chaînes ou les identifiants ; laisser
  chaque boucle relire librement la configuration.
- **Critère** — une même politique doit être testable et liée à la révision du
  tokenizer.
- **Coût accepté** — la configuration représente des ensembles et des valeurs
  optionnelles plutôt qu'un unique `eos_id`.
- **Condition de révision** — les modèles multimodaux pourront ajouter des
  catégories de tokens réservés sans modifier la sémantique de BOS ou EOS.
- **Contrat** — `praxis.generation.SpecialTokens`.
- **Invariant et tests** — aucune valeur n'est inventée ; padding n'arrête pas
  la génération sauf configuration explicite ; les marqueurs ne sont ajoutés
  qu'une fois.
