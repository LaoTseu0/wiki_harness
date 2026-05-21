## Décision et dépôt dans Praxis

- **Décision** — `GenerationLoop` orchestre des contrats injectés : modèle,
  pipeline de logits, sampler, décodeur et politique d'arrêt.
- **Alternatives** — une fonction monolithique couplée à Transformers, ou une
  boucle récursive.
- **Critère** — chaque mécanisme doit pouvoir être reconstruit, remplacé et
  testé isolément.
- **Coût accepté** — davantage de petits objets et d'événements qu'un simple
  appel `generate()`.
- **Condition de révision** — le Parcours 9 généralisera cette boucle en boucle
  d'agent ; le Parcours 0 reste limité au prochain **token**.
- **Contrat** — `praxis.generation.GenerationLoop`.
- **Invariant et tests** — au plus un **token** est ajouté par tour ; chaque **Input**
  est le préfixe précédent plus ce **token** ; un budget fini borne la boucle.
