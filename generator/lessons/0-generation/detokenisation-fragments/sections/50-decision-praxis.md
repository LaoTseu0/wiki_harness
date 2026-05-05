## Décision et dépôt dans Praxis

- **Décision** — `TokenDecoder` reçoit les identifiants dans l'ordre et renvoie
  des fragments textuels stabilisés plus des événements de contrôle.
- **Alternatives** — décoder chaque token séparément ; redécoder toute la
  séquence à chaque tour sans contrat de stabilité.
- **Critère** — ne jamais produire de texte invalide ni perdre les identifiants
  nécessaires au contrôle.
- **Coût accepté** — un petit état de décodage et éventuellement un suffixe
  retenu.
- **Condition de révision** — le streaming multimodal ajoutera d'autres types de
  fragments au Parcours 15.
- **Contrat** — `praxis.generation.TokenDecoder`.
- **Invariant et tests** — concaténer les fragments émis donne le même texte que
  le décodage complet, avec les mêmes options ; aucun `�` n'est inventé en mode
  strict.
