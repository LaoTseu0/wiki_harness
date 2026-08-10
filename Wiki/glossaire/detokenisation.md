# détokenisation

Reconstruction d’un flux de texte à partir d’identifiants ou de fragments de
tokens. Elle doit respecter l’état du décodeur et les frontières d’encodage.

Dans un décodeur à octets, deux identifiants peuvent fournir chacun une partie du même
caractère. Il faut réunir les octets avant de publier le caractère complet.

[Passer des identifiants au texte affichable](../parcours/0-generation/15-detokenisation-fragments.md#connaissances)
