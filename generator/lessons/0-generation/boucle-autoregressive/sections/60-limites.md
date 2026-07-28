## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la performance d'une boucle avec cache.
- **Praxis ne garantit pas encore** — la reprise après arrêt du processus.
- **Échec provoqué** — une politique EOS défectueuse ne doit pas créer une
  boucle infinie grâce au budget maximal.
- **Ouverture ultérieure** —
  [[15-detokenisation-fragments|Reconstruire le texte généré]],
  [[16-conditions-arret|Borner la génération]] et
  [[17-prefill-decode-kv-cache|cache KV]].
