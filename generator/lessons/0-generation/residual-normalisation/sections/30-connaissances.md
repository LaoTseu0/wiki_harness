## Connaissances

### Le chemin résiduel

Une architecture decoder-only **pré-norm** courante peut s'écrire :

$$
y = x + \operatorname{Attention}(\operatorname{Norm}(x))
$$

$$
z = y + \operatorname{**MLP**}(\operatorname{Norm}(y))
$$

`x`, `y` et `z` possèdent la même dimension cachée. Chaque sous-bloc produit une
mise à jour compatible avec cette dimension ; l'addition conserve un chemin
direct pour l'information et les gradients.

Le **residual stream** n'est pas un objet stocké séparément par le modèle. C'est
le nom donné au tenseur principal qui traverse les blocs et accumule leurs
contributions.

### **Pré-norm** et [[glossaire/post-norm|post-norm]]

Dans une architecture **pré-norm**, la normalisation précède le sous-bloc. Dans
l'architecture Transformer d'origine, une normalisation suit l'addition
résiduelle. Ces organisations ne sont pas interchangeables après
l'entraînement : déplacer une normalisation change la fonction calculée.

Le Canvas du cours représente une architecture **pré-norm** fréquente, pas tous les
Transformers.

### [[glossaire/layernorm|LayerNorm]] et [[glossaire/rmsnorm|RMSNorm]]

**LayerNorm** recentre les composantes autour de leur moyenne et les remet à
l'échelle avec leur variance, puis peut appliquer des paramètres appris.

**RMSNorm** ne soustrait pas la moyenne. Une forme courante calcule :

$$
\operatorname{**RMSNorm**}(x)
=
g \odot \frac{x}{\sqrt{\operatorname{mean}(x^2)+\varepsilon}}
$$

`g` est une échelle apprise et $\varepsilon$ évite une division instable près
de zéro. La normalisation agit par position sur la dimension cachée ; elle ne
normalise ni les tokens entre eux, ni les probabilités de sortie.

### Précision numérique

Les carrés, moyennes et racines peuvent être calculés dans une précision plus
élevée que celle des poids, puis reconvertis. Ce détail limite les erreurs
numériques. Il relève de l'implémentation du runtime et doit être observé avant
de comparer deux passages avant.
