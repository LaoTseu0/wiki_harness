## Décision et dépôt dans Praxis

- **Décision** — `softmax` est une fonction pure et stable utilisée par le
  laboratoire et le sampler.
- **Alternatives** — déléguer toute normalisation au runtime, ou stocker
  uniquement des probabilités.
- **Critère** — conserver les **logits** permet de composer les transformations et
  d'observer chaque étape.
- **Coût accepté** — l'implémentation pédagogique en Python n'est pas utilisée
  sur le chemin de production tensoriel.
- **Condition de révision** — le backend pourra fournir une primitive optimisée
  derrière le même invariant.
- **Contrat** — `praxis.generation.softmax`.
- **Invariant et tests** — sortie finie, non négative, somme proche de un,
  ordre conservé, poids nul pour `-inf`, invariance à une translation commune.
