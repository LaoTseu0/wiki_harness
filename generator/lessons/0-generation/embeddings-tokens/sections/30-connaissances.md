## Connaissances

### Une matrice indexée par le vocabulaire

Pour un vocabulaire de taille \(V\) et une dimension cachée \(d\), la table
d'embeddings possède la forme \(V \times d\). Un identifiant `i` sélectionne la
ligne \(E_i\).

Pour un batch de forme `[batch, sequence]`, la lecture produit typiquement un
tenseur `[batch, sequence, hidden_size]`. Ce n'est pas une multiplication
one-hot réellement matérialisée, même si elle lui est mathématiquement
équivalente : le runtime effectue une sélection optimisée de lignes.

Un identifiant négatif ou supérieur à `V - 1` n'a aucune représentation. Le
runtime doit le refuser plutôt que le rabattre silencieusement.

### Une représentation apprise, pas un dictionnaire de sens

Les lignes sont ajustées pendant l'entraînement afin de réduire la fonction de
perte. Leur proximité peut refléter des régularités apprises, mais une ligne
n'est ni une définition, ni un document récupérable, ni une mémoire agentique.

Le même identifiant sélectionne le même vecteur initial à chaque occurrence.
Deux occurrences acquièrent des représentations différentes après les
interactions avec leur contexte et leur position.

### Position et échelle dépendent de l'architecture

Le Transformer original ajoute un encodage positionnel au vecteur d'entrée.
Des modèles decoder-only actuels, comme les variantes Llama, appliquent plutôt
RoPE aux requêtes et clés dans l'attention. Il ne faut donc pas ajouter
arbitrairement un vecteur de position à une architecture qui n'a pas été
entraînée ainsi.

Certaines architectures multiplient aussi les embeddings par une constante.
Cette échelle est une propriété de la configuration et du code du modèle, pas
une étape universelle de Praxis.

### Partage avec la projection de sortie

La matrice de projection vers le vocabulaire peut partager ses poids avec la
table d'embeddings. Ce *weight tying* réduit le nombre de paramètres et relie
les représentations d'entrée et de sortie.

Le partage reste optionnel. Deux matrices de mêmes dimensions ne sont pas
nécessairement le même paramètre. Le runtime et la configuration du checkpoint
font foi.
