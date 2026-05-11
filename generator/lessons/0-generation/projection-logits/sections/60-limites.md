## Limites et cas d'échec

- **La reconstruction ne prouve pas** — que le plus grand logit donne le
  meilleur texte à long terme.
- **Praxis ne garantit pas encore** — l'accès aux logits d'un modèle servi par
  une API.
- **Échec provoqué** — utiliser un vocabulaire permuté conserve la forme du
  vecteur mais associe les scores aux mauvais tokens.
- **Ouverture ultérieure** — [[11-logits-softmax|Des logits à une distribution]]
  puis [[12-filtrage-distribution|Transformer la distribution]].
