## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la stabilité ou la performance d'un
  kernel d'attention.
- **Praxis ne garantit pas encore** — l'accès aux matrices d'attention d'un
  fournisseur.
- **Échec provoqué** — appliquer le masque après **softmax** laisse le total
  inférieur à un et ne renormalise pas les positions autorisées.
- **Ouverture ultérieure** — [[08-residual-normalisation|Residual stream et
  normalisation]] puis [[17-prefill-decode-kv-cache|cache KV]].
