## Décision et dépôt dans Praxis

- **Décision** — `ChatTemplate` transforme des messages typés en identifiants en
  passant par le **Template** livré avec le **tokenizer**.
- **Alternatives** — maintenir un **Template** global Praxis ; laisser chaque
  appelant concaténer les messages.
- **Critère** — la séquence doit rester compatible avec le [[glossaire/checkpoint|checkpoint]] et
  reproductible à partir de ses artefacts.
- **Coût accepté** — Praxis conserve l'identité et la révision du **Template** dans
  les traces de génération.
- **Condition de révision** — un modèle sans **Template** fourni exige un adaptateur
  explicitement configuré et testé sur son format d'entraînement.
- **Contrat** — `praxis.generation.ChatTemplate`.
- **Invariant et tests** — ordre des messages préservé ; rôle inconnu refusé ;
  rendu déterministe ; aucune duplication de BOS/EOS ; égalité entre la voie
  directe et la voie texte puis tokenisation.
