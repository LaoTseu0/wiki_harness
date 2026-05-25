## Décision et dépôt dans Praxis

- **Décision** — la frontière du runtime renverra les **logits** du prochain **token**,
  indexés par le vocabulaire associé.
- **Alternatives** — demander directement des probabilités, ou laisser le
  runtime choisir un **token** sans exposer les scores.
- **Critère** — les **logits** permettent de reconstruire et composer les
  transformations sans perdre d'information par un choix prématuré.
- **Coût accepté** — exposer un vecteur de taille vocabulaire est réservé au
  runtime local et au laboratoire ; une API distante peut ne pas offrir cette
  capacité.
- **Condition de révision** — le contrat par capacités du Parcours 2 rendra
  l'accès aux **logits** optionnel.
- **Contrat** — préparatoire à `praxis.generation.NextTokenModel`.
- **Invariant et tests** — l'ordre des **logits** correspond aux identifiants du
  tokenizer ; la taille vaut `vocab_size`.
