## Décision et dépôt dans Praxis

- **Décision** — `Sampler` reçoit un générateur pseudo-aléatoire propre au run ;
  greedy utilise un chemin séparé.
- **Alternatives** — RNG global, seed passée à chaque appel, ou choix délégué au
  backend sans métadonnées.
- **Critère** — isoler les exécutions concurrentes et rendre l'expérience
  rejouable dans un environnement fixé.
- **Coût accepté** — la trace conserve seed, versions et configuration, sans
  promettre une portabilité bit à bit.
- **Condition de révision** — une reprise durable du RNG sera cadrée avec les
  checkpoints au Parcours 10.
- **Contrat** — `praxis.generation.Sampler`.
- **Invariant et tests** — un appel choisit un candidat autorisé ; deux
  générateurs ne partagent pas leur état ; mêmes entrées et même état donnent
  le même indice dans l'implémentation testée.
