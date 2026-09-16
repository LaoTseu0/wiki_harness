# streaming

Transmission progressive d’une sortie avant que sa production soit terminée.
Le producteur doit distinguer les fragments reçus du texte déjà stabilisé.

Si un fragment se termine par un caractère UTF-8 incomplet, le producteur peut publier
le texte déjà décodé et retenir les derniers octets jusqu’au fragment suivant.

[Choisir quand publier le texte décodé](../parcours/0-generation/15-detokenisation-fragments.md#connaissances)
