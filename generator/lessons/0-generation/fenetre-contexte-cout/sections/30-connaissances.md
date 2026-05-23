## Connaissances

### Trois nombres différents

- **longueur d'entrée** : tokens obtenus après Template et tokenisation ;
- **budget de sortie** : nombre maximal de nouveaux tokens autorisés ;
- **fenêtre effective** : capacité réellement utilisable avec ce [[glossaire/checkpoint|checkpoint]],
  cette configuration et ce runtime.

Une requête simple exige :

$$
\text{**input**\_tokens} + \text{reserved\_output} \leq \text{context\_capacity}
$$

Réserver le maximum de sortie évite d'atteindre la frontière au milieu d'une
réponse. Une autre politique peut accepter une réserve souple, mais elle doit
annoncer le risque d'un arrêt `context_limit`.

### La capacité effective

La configuration du modèle annonce généralement une longueur maximale de
positions. Le runtime peut imposer une valeur inférieure, utiliser une fenêtre
glissante ou permettre une extension RoPE.

La plus grande valeur affichée n'est pas automatiquement la capacité fiable.
Il faut distinguer :

- allocation acceptée ;
- positions encodables sans erreur ;
- qualité effectivement évaluée à cette longueur.

### Coût du [[glossaire/prefill|prefill]]

Dans une attention complète standard, une séquence de longueur $N$ forme une
matrice de scores $N \times N$ par tête avant exploitation du masque. Le
nombre d'interactions d'attention est donc quadratique en $N$.

Les projections et le MLP ont d'autres coûts, généralement linéaires en nombre
de positions pour une largeur de modèle fixée. Le `O(N²)` de l'attention ne
permet pas à lui seul de prédire la latence totale : kernels, bande passante,
batch, précision et matériel interviennent.

### Coût du [[glossaire/decode|decode]] avec cache

Pour un nouveau token et une attention complète, la requête compare ses scores
aux $N$ clés précédentes : cette partie est linéaire en longueur conservée
pour ce pas. Générer $G$ tokens après un prompt de longueur $N$ accumule
environ :

$$
\sum_{g=0}^{G-1}(N+g)
=
GN + \frac{G(G-1)}{2}
$$

interactions requête–clé par tête, sans compter les autres opérations.

Le [[glossaire/cache-kv|cache KV]] consomme lui aussi une mémoire qui croît avec les positions, les
couches, les têtes KV, la dimension de tête et la taille numérique.

### Les architectures peuvent changer ces lois locales

Une fenêtre glissante borne le nombre de clés consultées dans certaines
couches. Une attention par chunks, sparse ou linéaire change la structure du
calcul. Un cache quantifié change le coût mémoire.

Ces variantes ne justifient pas de présenter toutes les fenêtres longues comme
gratuites. Leur portée et leur qualité doivent être mesurées sur
l'implémentation choisie.

### La politique de contexte vient après la frontière

Le Parcours 0 refuse un dépassement et produit une raison explicite. Le Parcours
3 décidera comment construire une conversation sous budget : éviction,
résumé, contexte récupéré et réserve de sortie.

Tronquer ici les premiers tokens pourrait supprimer les instructions ou couper
un message au milieu sans que l'appelant le sache.
