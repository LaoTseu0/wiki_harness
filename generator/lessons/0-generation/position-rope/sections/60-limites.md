## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la qualité d'une extrapolation RoPE.
- **Praxis ne garantit pas encore** — la compatibilité d'un cache entre deux
  runtimes ou deux configurations.
- **Échec provoqué** — réutiliser le même cache en repartant à la position zéro
  doit être considéré comme une séquence incohérente.
- **Ouverture ultérieure** — [[07-attention-causale|L'attention causale]] et
  [[17-prefill-decode-kv-cache|Prefill, decode et cache KV]].
