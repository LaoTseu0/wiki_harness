# stop sequence

Chaîne configurée dont la reconnaissance dans le texte reconstruit provoque
l’arrêt de la génération. Elle peut traverser plusieurs tokens ou fragments.

Si la chaîne d’arrêt est « FIN », un fragment terminé par « F » et le suivant ouvert
par « IN » forment ensemble le motif. Le contrôle doit couvrir la jonction.

[Détecter un motif réparti sur plusieurs fragments](../parcours/0-generation/16-conditions-arret.md#connaissances)
