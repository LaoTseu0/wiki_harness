## Connaissances

### Une chaîne ordonnée

Une pipeline de logits peut contenir :

1. des contraintes dures ou des biais ;
2. des pénalités dépendant de l'historique ;
3. une température ;
4. un ou plusieurs filtres de candidats ;
5. une renormalisation avant tirage.

Cet ordre n'est pas universel. Il doit être fixé par Praxis et comparé à celui
du runtime utilisé. Les opérations ne sont généralement pas commutatives :
appliquer top-p avant la température peut conserver un autre ensemble
qu'appliquer la température avant top-p.

### Température

Pour une température \(T>0\), les logits deviennent :

\[
z'_i = z_i/T
\]

Une température inférieure à un agrandit les écarts et concentre la
distribution. Une température supérieure à un les réduit et aplatit la
distribution. \(T=1\) ne change rien.

Diviser par zéro n'implémente pas greedy. Les runtimes utilisent une branche
argmax explicite lorsque le sampling est désactivé ou qu'une interface traite
`temperature=0` comme un raccourci. Mathématiquement, quand \(T\) tend vers
zéro, la masse se concentre sur les maxima ; les égalités demandent encore une
règle de départage.

### Top-k

Top-k conserve les `k` logits les plus élevés et masque les autres. Son nombre
de candidats est fixe, même lorsque la distribution est très concentrée ou
très plate.

`k=1` suivi d'un tirage équivaut à choisir l'argmax sous une règle de départage
donnée. Une valeur supérieure à la taille du vocabulaire ne doit pas provoquer
un dépassement.

### Top-p

Top-p, ou nucleus sampling, trie les candidats par probabilité décroissante et
conserve le plus petit préfixe dont la masse cumulée atteint ou dépasse `p`. Le
nombre de candidats s'adapte donc à la forme de la distribution.

Le token qui franchit le seuil est conservé. Retirer tous les tokens une fois
la somme supérieure à `p` peut exclure précisément celui qui permet d'atteindre
le seuil.

### Min-p

Min-p compare chaque probabilité \(p_i\) à une fraction \(\alpha\) de la
probabilité maximale :

\[
p_i \geq \alpha\,p_{\max}
\]

Le seuil devient plus strict lorsque le meilleur candidat domine et plus
permissif lorsque la distribution est plate. L'implémentation conserve au
moins un nombre minimal de candidats pour éviter un ensemble vide.

### Trois familles de pénalités de répétition

Une *repetition penalty* courante, issue de CTRL et reprise par Transformers,
modifie au plus une fois le logit de chaque token déjà présent : un logit
positif est divisé par la pénalité, un logit négatif est multiplié. La valeur
`1` désactive cette transformation.

Une pénalité de présence additive retire une constante si le token a déjà été
vu. Une pénalité de fréquence retire une valeur proportionnelle au nombre
d'occurrences :

\[
z'_i = z_i - \alpha_p\,\mathbf{1}[c_i>0] - \alpha_f c_i
\]

Ces formules et la fenêtre d'historique varient selon les runtimes. Les noms de
paramètres semblables ne garantissent pas la même opération.

### Greedy

Greedy choisit un indice de logit maximal sans tirage. Il est localement
optimal pour le prochain token, pas pour la probabilité ou la qualité de toute
la séquence.

Il supprime l'aléa du sampler, mais pas nécessairement toutes les divergences
numériques entre runtimes si deux scores sont proches ou égaux.
