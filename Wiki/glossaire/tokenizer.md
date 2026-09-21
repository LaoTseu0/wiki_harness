# tokenizer

Composant qui transforme un texte en identifiants de tokens et effectue
l’opération inverse. Son vocabulaire et ses règles doivent correspondre au
checkpoint du modèle.

Pour comparer deux tokenizers sur « bonjour ! », conserver la même chaîne et relever
les identifiants de chacun. Un identifiant numérique prend son sens dans le
vocabulaire qui l’a produit.

[Suivre les étapes de l’encodage et du décodage](../parcours/0-generation/02-tokenisation-vocabulaire.md#connaissances)
