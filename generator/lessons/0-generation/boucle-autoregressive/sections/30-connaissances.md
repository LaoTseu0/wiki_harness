## Connaissances

### Factorisation autorégressive

La probabilité d'une suite \(t_1,\ldots,t_N\) se factorise :

\[
P(t_1,\ldots,t_N)
=
\prod_{i=1}^{N} P(t_i \mid t_1,\ldots,t_{i-1})
\]

Le passage avant fournit la distribution du prochain token conditionnellement
au préfixe courant. Il ne produit pas toute la réponse en une seule décision.

### Le token choisi devient une donnée

Après sampling, le token est ajouté à la séquence. Le pas suivant le traite
comme n'importe quel élément du préfixe. Le modèle ne garde pas à côté une
liste de candidats abandonnés.

Revenir sur un choix exige un algorithme de recherche, un fork de trajectoire
ou une nouvelle génération. La boucle greedy ou sampling simple ne corrige pas
spontanément un token déjà réinjecté.

### État minimal du run

Une boucle pédagogique maintient au moins :

- les identifiants du prompt ;
- les identifiants générés ;
- la configuration des transformations ;
- l'état du générateur pseudo-aléatoire ;
- l'état du décodeur incrémental ;
- la raison d'arrêt éventuelle ;
- le cache du modèle lorsqu'il est utilisé.

Cet état reste éphémère dans le Parcours 0. Le Parcours 10 décidera comment le
sérialiser et le reprendre après interruption.

### Un tour possède des frontières

Un ordre explicite évite les effets cachés :

1. demander les logits ;
2. transformer les logits ;
3. choisir un identifiant ;
4. l'ajouter à la séquence ;
5. alimenter le décodeur ;
6. évaluer les conditions d'arrêt ;
7. réinjecter seulement si la génération continue.

Certaines implémentations vérifient EOS immédiatement après le choix et ne
décodent pas ce token comme contenu. Cette variation doit être fixée par la
politique d'arrêt ; elle ne change pas le principe autorégressif.

### Entraînement et inférence

Pendant l'entraînement causal, plusieurs positions d'une séquence connue
peuvent être évaluées en parallèle sous masque causal. À l'inférence, le
prochain token n'existe pas encore : chaque nouvelle position dépend du choix
précédent.

Cette dépendance séquentielle limite la parallélisation du decode, même si le
calcul interne d'un passage avant reste massivement parallèle.
