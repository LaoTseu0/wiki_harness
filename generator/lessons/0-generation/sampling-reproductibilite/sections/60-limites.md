## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la reproductibilité entre Python,
  PyTorch, llama.cpp et un GPU.
- **Praxis ne garantit pas encore** — la reprise d'un run interrompu.
- **Échec provoqué** — un composant concurrent qui utilise le RNG global doit
  modifier la trajectoire et justifier son exclusion du contrat.
- **Ouverture ultérieure** —
  [[14-boucle-autoregressive|Réinjecter le token choisi]] et le Parcours 10
  pour la reprise durable.
