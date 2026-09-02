# prefill

Premier passage d’inférence qui traite le prompt complet et construit les états
réutilisables, notamment les clés et valeurs du cache KV.

Pour un prompt de douze tokens, le premier passage traite les douze positions et
fournit, à la dernière, les scores du premier token à générer.

[Retrouver l’origine des scores du premier token](../parcours/0-generation/17-prefill-decode-kv-cache.md#connaissances)
