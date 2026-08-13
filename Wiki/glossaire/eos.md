# EOS

Abréviation de *End of Sequence*. La boucle de génération peut interpréter cet
identifiant produit par le modèle comme une demande d’arrêt.

Si la boucle reçoit l’identifiant EOS après « bonjour », elle peut clore la réponse à
ce pas, même s’il reste vingt tokens dans le budget.

[Distinguer la fin émise par le modèle de la limite de longueur](../parcours/0-generation/16-conditions-arret.md#connaissances)
