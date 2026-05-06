## Décision et dépôt dans Praxis

- **Décision** — `ContextLimit` reçoit le comptage exact du tokenizer et refuse
  une réservation impossible. Aucune troncature automatique dans `generation`.
- **Alternatives** — compter les caractères ; laisser le runtime tronquer ;
  réserver toujours zéro token de sortie.
- **Critère** — préserver les instructions et rendre l'arrêt prévisible.
- **Coût accepté** — une requête trop longue échoue avant l'inférence jusqu'à ce
  qu'une politique de contexte existe.
- **Condition de révision** — le Parcours 3 ajoutera un gestionnaire de budget
  capable de composer et réduire le contexte.
- **Contrat** — `praxis.generation.ContextLimit`.
- **Invariant et tests** — comptage avec le tokenizer exact ; entrée et réserve
  non négatives ; somme inférieure ou égale à la capacité effective.
