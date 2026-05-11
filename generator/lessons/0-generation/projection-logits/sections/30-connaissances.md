## Connaissances

### La normalisation finale

Une architecture pré-norm courante applique une dernière normalisation après le
dernier bloc. Elle prépare la représentation avant la tête de langage. Son type
et son epsilon viennent de l'architecture ; ce n'est pas le softmax du
vocabulaire.

### Une ligne par candidat

Pour une dimension cachée \(d\) et un vocabulaire de taille \(V\), la matrice de
sortie possède typiquement la forme \(V \times d\).

\[
z = W_{\text{vocab}}h + b
\]

`h` est la représentation d'une position et `z` contient \(V\) logits. Chaque
indice de `z` correspond au même identifiant de vocabulaire que le tokenizer.
Le biais est optionnel selon l'architecture.

Pour une séquence complète, le modèle peut produire `[batch, sequence, V]`.
La génération du prochain token utilise les logits de la dernière position
utile. Les logits des autres positions servent notamment à l'entraînement ou à
des analyses.

### Les scores sont relatifs

Un logit peut être négatif, positif ou nul. Il n'est ni borné entre zéro et un,
ni interprétable isolément comme une confiance.

Ajouter la même constante à tous les logits ne change pas le softmax, car le
facteur multiplicatif correspondant s'annule lors de la normalisation. En
revanche, multiplier tous les logits modifie leurs écarts relatifs et donc la
distribution ; la température exploitera précisément cette propriété.

### Tous les tokens du vocabulaire sont candidats

La projection comprend les sous-mots, octets et tokens spéciaux présents dans
le vocabulaire. Un EOS reçoit donc un logit comme les autres. La boucle
n'arrête pas le calcul parce que le modèle « sait qu'il a fini » : elle tire ou
choisit EOS, puis la politique d'arrêt interprète son identifiant.

Une grammaire ou un `logit_bias` pourra modifier les candidats plus tard, après
la projection. La tête de langage brute ne connaît pas ces contraintes du
harnais.

### Partage de poids optionnel

La tête peut réutiliser la matrice d'embeddings transposée ou posséder ses
propres poids. Cette décision, appelée *weight tying*, est configurée pendant
l'entraînement. Le harnais ne doit pas la déduire du nom `lm_head`.
