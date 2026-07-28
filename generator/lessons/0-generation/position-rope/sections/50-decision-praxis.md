## Décision et dépôt dans Praxis

- **Décision** — Praxis ne fixe aucune convention RoPE universelle. Il expose
  seulement les métadonnées nécessaires à l'inspection du runtime.
- **Alternatives** — réécrire la position dans le harnais, ou supposer que tous
  les modèles ajoutent un vecteur positionnel aux embeddings.
- **Critère** — la position fait partie de l'architecture entraînée et ne peut
  pas être remplacée à la périphérie.
- **Coût accepté** — la configuration du modèle reste une dépendance normative
  de l'expérience.
- **Condition de révision** — une stratégie d'extension de contexte ne sera
  adoptée qu'après mesure sur le modèle local.
- **Contrat** — aucun contrat public dans `generation`.
- **Invariant et tests** — une reprise avec cache continue les indices de
  position ; une configuration de scaling est enregistrée avec le checkpoint.
