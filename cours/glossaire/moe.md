# MoE (mixture of experts)

> [glossaire](index.md)

Une architecture où le modèle n'active, pour chaque token, qu'une fraction de
ses poids — quelques « experts » choisis par un routeur, au lieu de tout le
réseau. Elle permet de très grands modèles à coût d'inférence réduit.

Conséquence qui compte ici : le routage des experts dépend de la composition
du lot (batch), donc deux requêtes identiques ne rencontrent pas forcément les
mêmes voisines ni les mêmes experts — une source de non-déterminisme de plus,
citée dans [sampling](../fondamentaux/sampling.md).
