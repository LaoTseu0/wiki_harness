## Connaissances

### Projeter Q, K et V

À partir d'une matrice de représentations $X$, une tête calcule :

$$
Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V
$$

Les poids sont appris. `Q`, `K` et `V` ne sont pas trois copies sémantiques
étiquetées à la main ; ce sont trois projections servant des rôles différents
dans le calcul.

Pour une requête $q_i$ et une clé $k_j$, le score brut est leur produit
scalaire. La division par $\sqrt{d_k}$ limite la croissance de la magnitude
des produits lorsque la dimension de tête augmente.

### Masquer le futur

Dans un modèle autorégressif, la position `i` ne doit pas exploiter les tokens
`j > i` pendant l'entraînement ou l'inférence. Le masque ajoute une valeur
équivalente à moins l'infini aux scores interdits avant [[glossaire/softmax|softmax]]. Leur
probabilité devient alors nulle.

$$
\operatorname{Attention}(Q,K,V)
=
\operatorname{**softmax**}
\left(\frac{QK^\top}{\sqrt{d_k}} + M\right)V
$$

Le masque de padding et le [[glossaire/masque-causal|masque causal]] peuvent contribuer à `M`. Leur forme
et leur convention dépendent du runtime.

### Pondérer les valeurs

**Softmax** transforme chaque ligne de scores autorisés en poids non négatifs dont
la somme vaut un. La sortie d'une tête est la somme pondérée des vecteurs
`V`.

Une forte valeur d'attention indique une contribution importante dans cette
tête et cette couche pour ce passage avant. Elle ne prouve pas à elle seule une
explication causale du comportement final du modèle.

### Plusieurs têtes

L'attention multi-head répète le mécanisme dans plusieurs sous-espaces, concatène
les sorties puis les projette vers la dimension cachée. Les têtes peuvent
apprendre des relations différentes sans qu'un rôle stable leur soit assigné à
l'avance.

La [[glossaire/grouped-query-attention|Grouped-Query Attention]] utilise davantage de têtes de requêtes que de têtes
de clés et valeurs. Plusieurs requêtes partagent alors un même groupe de
`K`/`V`, ce qui réduit le cache. Ce choix d'architecture ne change pas le
contrat conceptuel `QKᵀ → poids → V`.

### La causalité ne garantit pas la vérité

Le masque empêche une fuite d'information depuis les tokens futurs de la
séquence. Il ne garantit ni la pertinence de l'attention, ni la factualité, ni
le respect des instructions. « Causal » décrit ici la direction temporelle du
calcul.
