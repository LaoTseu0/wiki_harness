# Softmax

> [glossaire](index.md)

La fonction qui transforme des scores bruts (les [logits](logits.md)) en une
distribution de probabilités : chaque valeur entre 0 et 1, somme égale à 1.

$$\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

Deux propriétés qui resservent partout : l'**ordre est conservé** (le plus
gros logit reste la plus grosse probabilité), et les **écarts sont
amplifiés** par l'exponentielle (un léger avantage en logit devient un net
avantage en probabilité). La [temperature](../fondamentaux/sampling-et-prompting.md)
agit juste avant cette fonction.
