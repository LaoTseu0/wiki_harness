## Connaissances

### Une transformation par position

Un MLP Transformer classique projette la dimension cachée \(d\) vers une
dimension intermédiaire plus grande, applique une non-linéarité, puis reprojette
vers \(d\).

\[
\operatorname{MLP}(x) = W_{\text{down}}\,
\sigma(W_{\text{up}}x + b_{\text{up}}) + b_{\text{down}}
\]

Les mêmes poids sont appliqués à toutes les positions. Aucun produit entre deux
positions n'apparaît dans ce calcul. Les informations venues d'autres tokens
ont déjà été intégrées dans `x` par l'attention.

### La non-linéarité est indispensable

Deux projections linéaires successives sans non-linéarité se réduisent à une
seule projection linéaire. L'activation permet au sous-bloc de représenter une
transformation plus riche.

Les architectures emploient notamment ReLU, GELU, SiLU ou des variantes
gated. Le nom « MLP » ne fixe donc pas sa formule exacte.

### SwiGLU

Une forme courante dans les modèles de la famille Llama est :

\[
\operatorname{SwiGLU}(x)
=
W_{\text{down}}
\left(
\operatorname{SiLU}(W_{\text{gate}}x)
\odot
W_{\text{up}}x
\right)
\]

Deux projections montantes produisent une porte et un contenu. Leur produit
composante par composante est ensuite projeté vers la dimension cachée. Les
noms `gate`, `up` et `down` décrivent l'implémentation ; leurs tailles viennent
de la configuration.

### Dimension intermédiaire et coût

La dimension intermédiaire détermine la taille des matrices et une part
importante du calcul et de la mémoire des poids. Une architecture gated emploie
trois projections au lieu des deux d'un MLP simple, mais peut ajuster la
dimension intermédiaire pour contrôler le nombre total de paramètres.

Le coût exact dépend du batch, de la longueur, de la précision, du matériel et
des kernels. Il ne se déduit pas d'un adjectif comme « large ».

### Variantes d'architecture

Un Mixture of Experts route certains tokens vers un sous-ensemble d'experts
MLP. D'autres architectures partagent, factorisent ou remplacent le sous-bloc.
Le processus du cours décrit un MLP dense courant ; ces variantes doivent être
comparées à cette frontière, pas présentées comme identiques.
