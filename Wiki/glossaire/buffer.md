# buffer

Zone mémoire temporaire qui retient des données incomplètes avant leur
traitement ou leur publication. Sa durée de vie dépend de la frontière qu’il
protège.

Un fragment se termine par l’octet `C3`, le suivant commence par `A9`. Un décodeur
UTF-8 incrémental conserve le premier octet jusqu’à pouvoir émettre « é ».

[Suivre les octets retenus entre deux fragments](../parcours/0-generation/15-detokenisation-fragments.md#connaissances)
