## Décision et dépôt dans Praxis

- **Décision** — `NextTokenModel` sépare `prefill(token_ids)` et
  `decode(token_id, cache)` tout en permettant un adaptateur plus simple pour
  les backends sans cache exposé.
- **Alternatives** — une méthode qui reçoit toujours toute la séquence, ou un
  cache global caché dans le provider.
- **Critère** — rendre visible la durée de vie et la compatibilité du cache.
- **Coût accepté** — le type de cache reste opaque pour ne pas imposer une
  forme tensorielle à tous les runtimes.
- **Condition de révision** — le Parcours 1 comparera les stratégies concrètes ;
  le Parcours 3 décidera la réutilisation de préfixes de session.
- **Contrat** — `praxis.generation.NextTokenModel` et référence de cache opaque.
- **Invariant et tests** — un cache appartient à un modèle et à un préfixe ; la
  position avance exactement avec les tokens ajoutés ; avec ou sans cache, les
  logits restent équivalents à la tolérance du runtime.
