## Limites et cas d'échec

- **La reconstruction ne prouve pas** — qu'un BPE miniature produit une
  segmentation utile pour un modèle entraîné.
- **Praxis ne garantit pas encore** — la compatibilité du Template de chat ou
  le traitement des tokens spéciaux.
- **Échec provoqué** — encoder avec le tokenizer d'un autre checkpoint doit
  être considéré comme une incompatibilité, même si la taille du vocabulaire
  coïncide.
- **Ouverture ultérieure** — [[03-tokens-controle|Tokens de contrôle]] et
  [[04-templates-chat|Template de chat]].
