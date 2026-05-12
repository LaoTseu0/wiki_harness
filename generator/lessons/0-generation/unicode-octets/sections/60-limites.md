## Limites et cas d'échec

- **La reconstruction ne prouve pas** — le nombre de grapheme clusters ; Python
  n'expose pas directement l'algorithme complet de segmentation Unicode.
- **Praxis ne garantit pas encore** — la tokenisation ni le rendu incrémental.
- **Échec provoqué** — décoder `b"\xc3"` en UTF-8 strict doit échouer tant que
  l'octet suivant n'est pas disponible.
- **Ouverture ultérieure** — [[02-tokenisation-vocabulaire|Tokenisation et
  vocabulaire]] puis [[15-detokenisation-fragments|Détokenisation
  incrémentale]].
