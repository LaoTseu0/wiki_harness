## Décision et dépôt dans Praxis

- **Décision** — les frontières textuelles de Praxis acceptent `str`. Une
  conversion en octets nomme explicitement UTF-8 et utilise le mode strict.
- **Alternatives** — accepter arbitrairement `str | bytes`, ou normaliser toutes
  les chaînes à l'entrée.
- **Critère** — conserver une représentation sans ambiguïté tout en laissant au
  contrat métier ou au tokenizer la décision de normaliser.
- **Coût accepté** — les frontières binaires doivent décoder explicitement
  avant d'entrer dans la génération.
- **Condition de révision** — une API de tokenizer qui exige réellement des
  octets recevra un adaptateur dédié.
- **Contrat** — aucun contrat public n'est déposé avant la leçon sur la
  tokenisation.
- **Invariant et tests** — aucune fonction ne déduit un nombre de tokens de
  `len(text)` ou de `len(text.encode("utf-8"))`.
