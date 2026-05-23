## Connaissances

### Définition

Pour des **logits** $z_1,\ldots,z_V$ :

$$
p_i = \frac{\exp(z_i)}{\sum_{j=1}^{V}\exp(z_j)}
$$

Chaque $p_i$ est positif et la somme vaut un, à l'erreur numérique près. Un
écart de **logits** devient un rapport de probabilités :

$$
\frac{p_i}{p_j} = \exp(z_i-z_j)
$$

La valeur absolue d'un **logit** importe donc moins que ses écarts avec les autres
candidats.

### Stabilité numérique

Exponentier de grands **logits** peut déborder. On soustrait le maximum $m$ :

$$
p_i =
\frac{\exp(z_i-m)}{\sum_j \exp(z_j-m)}
$$

Cette transformation ne change pas la distribution, car le facteur
$\exp(-m)$ apparaît au numérateur et au dénominateur. Elle garantit qu'au
moins un exposant vaut zéro et que les autres sont négatifs ou nuls.

Des **logits** contenant `NaN`, `+inf`, uniquement `-inf`, ou une somme
exponentielle nulle ne forment pas une distribution exploitable. Un `-inf`
isolé reste utile pour représenter un candidat masqué : son poids exponentiel
vaut zéro.

### Probabilité conditionnelle

La distribution représente :

$$
P(t_{n+1}\mid t_1,\ldots,t_n;\theta)
$$

Elle dépend des poids $\theta$, du préfixe tokenisé et du passage avant. Elle
ne mesure pas directement la probabilité qu'une affirmation soit vraie. Un
token peut être très probable parce qu'il complète une formulation fréquente,
même si la proposition complète est fausse.

### [[glossaire/log-probabilite|Log-probabilités]]

Le logarithme de **softmax** évite de multiplier de très petites probabilités. La
**log-probabilité** d'une séquence autorégressive est la somme des
**log-probabilités** conditionnelles de ses tokens.

Comparer des sommes brutes entre séquences de longueurs différentes favorise
généralement les séquences courtes, puisque chaque terme ajouté est inférieur
ou égal à zéro. Toute normalisation par longueur doit donc être annoncée.

### **Softmax** n'est pas encore une stratégie de génération

**Softmax** rend une distribution possible. Il ne décide pas si tous les candidats
restent autorisés, si la température les aplatit, si un filtre tronque la queue
ou si l'argmax remplace le tirage.

Selon l'implémentation, certaines transformations agissent sur les **logits** avant
un unique **softmax** final ; d'autres calculent temporairement les probabilités
pour choisir un masque. L'ordre exact fait partie du contrat du sampler.
