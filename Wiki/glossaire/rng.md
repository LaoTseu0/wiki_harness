# RNG

Abréviation de *Random Number Generator*. Ce composant conserve un état et
produit la suite pseudo-aléatoire utilisée par le sampling.

Deux tirages consécutifs consomment deux états successifs du générateur. Insérer un
tirage intermédiaire suffit à décaler la suite utilisée par le sampler.

[Suivre l’état du générateur entre deux tirages](../parcours/0-generation/13-sampling-reproductibilite.md#connaissances)
