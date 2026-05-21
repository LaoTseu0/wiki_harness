## Décision et dépôt dans Praxis

- **Décision** — `StopPolicy` renvoie une union fermée de raisons et contrôle le
  suffixe visible.
- **Alternatives** — un booléen, une exception générique ou une chaîne libre.
- **Critère** — l'appelant doit distinguer une fin normale, une limite et un
  échec.
- **Coût accepté** — un buffer de publication dimensionné par la plus longue
  **stop sequence** pertinente.
- **Condition de révision** — les budgets de temps et d'outils seront composés
  dans la boucle agentique.
- **Contrat** — `praxis.generation.StopPolicy` et `StopReason`.
- **Invariant et tests** — toute boucle est bornée ; une **stop sequence** exclue
  n'est jamais publiée ; **EOS** multiples sont acceptés ; la priorité est testée.
