## Décision et dépôt dans Praxis

- **Décision** — `LogitsPipeline` est une séquence ordonnée de transformations
  pures. Chaque étape peut exposer les candidats conservés au laboratoire.
- **Alternatives** — un objet de configuration sans ordre ; déléguer tous les
  réglages au backend.
- **Critère** — rendre les mécanismes comparables entre le sampler reconstruit
  et les runtimes.
- **Coût accepté** — Praxis doit versionner la sémantique et l'ordre de la
  pipeline.
- **Condition de révision** — une nouvelle stratégie n'entre dans le socle que
  si elle change une décision utile ; les samplers exotiques restent au
  glossaire ou dans la veille.
- **Contrat** — `praxis.generation.LogitsPipeline`.
- **Invariant et tests** — au moins un candidat reste fini ; les tokens masqués
  ne peuvent pas être tirés ; l'ordre est stable et tracé.
