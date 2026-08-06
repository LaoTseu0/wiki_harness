# checkpoint

État versionné des paramètres d’un modèle, accompagné des fichiers nécessaires
à son chargement. Le tokenizer, le Template et la configuration doivent rester
compatibles avec cet état.

Deux vocabulaires de même taille peuvent attribuer l’identifiant 42 à des unités
différentes. Charger les poids de l’un avec le tokenizer de l’autre change alors
l’entrée du modèle.

[Vérifier la correspondance entre tokenizer et modèle](../parcours/0-generation/02-tokenisation-vocabulaire.md#connaissances)
