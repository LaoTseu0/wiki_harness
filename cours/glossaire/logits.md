# Logits

> [glossaire](index.md)

Les scores bruts produits par la dernière couche du modèle, un par token du
vocabulaire, à chaque étape de génération. Ils ne sont pas normalisés :
positifs ou négatifs, grands ou petits, illisibles comme probabilités en
l'état. C'est le [softmax](softmax.md) qui les convertit en une distribution.

Tout le [sampling](../fondamentaux/sampling-et-prompting.md) se joue sur ces
valeurs : la temperature les divise, les filtres en écartent, avant le tirage.
