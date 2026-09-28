# vocabulaire

Table finie qui associe chaque identifiant de token à une unité connue du
tokenizer. Sa taille fixe le nombre de candidats produits par la projection de
sortie.

Si la table d’exemple associe l’identifiant 0 à « a » et 1 à « b », la suite [1, 0]
désigne « ba » pour un décodeur qui concatène ces unités.

[Retrouver les unités à partir de leurs identifiants](../parcours/0-generation/02-tokenisation-vocabulaire.md#connaissances)
