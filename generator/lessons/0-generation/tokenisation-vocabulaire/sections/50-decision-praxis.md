## Décision et dépôt dans Praxis

- **Décision** — `Tokenizer` expose `encode`, `decode`, `count` et son identité
  reproductible. Praxis adapte le **tokenizer** fourni avec le modèle.
- **Alternatives** — un **tokenizer** unique pour tous les modèles, ou des appels
  directs à une bibliothèque dans toute la base de code.
- **Critère** — les identifiants doivent rester compatibles avec les poids du
  modèle et les appels doivent être testables sans dépendre d'une classe
  concrète.
- **Coût accepté** — l'adaptateur conserve les options exactes et refuse les
  conversions implicites.
- **Condition de révision** — des modalités non textuelles pourront étendre le
  contrat avec un `Processor` au Parcours 15.
- **Contrat** — `praxis.generation.Tokenizer`.
- **Invariant et tests** — un **tokenizer** est associé à une révision
  d'artefacts ; le comptage utilise `encode` ; les tests couvrent espaces,
  accents composés, emoji, code et **tokens** spéciaux.
