## Connaissances

### Pourquoi ajouter une information de position

L'attention compare des vecteurs. Sans mécanisme positionnel supplémentaire,
les mêmes contenus utilisent les mêmes projections, et le calcul ne dispose pas
d'une représentation riche de leur distance ou de leur position.

Le **masque causal** apporte déjà une asymétrie : une position ne voit que son
préfixe. Il interdit le futur, mais ne remplace pas un encodage positionnel
capable de moduler les relations entre positions autorisées.

### La rotation

Sur une paire de composantes, une rotation d'angle $\theta$ s'écrit :

$$
R_\theta
\begin{bmatrix}x_1\\x_2\end{bmatrix}
=
\begin{bmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}
$$

La multiplication donne deux nouvelles composantes :

$$
x'_1 = x_1\cos\theta - x_2\sin\theta
\qquad
x'_2 = x_1\sin\theta + x_2\cos\theta
$$

La paire change ainsi de direction sans changer de longueur.

**RoPE** utilise plusieurs fréquences sur les paires de dimensions. À la position
`m`, il applique une rotation dépendant de `m` à la requête et à la clé. Le
produit scalaire entre la requête positionnée en `m` et la clé positionnée en
`n` peut se réécrire avec une rotation dépendant de `n - m`. La relation
relative apparaît donc directement dans le score.

Les implémentations de la famille Llama appliquent **RoPE** à `Q` et `K`, pas à
`V`. D'autres architectures peuvent choisir un autre encodage positionnel.

### **RoPE** et **masque causal** répondent à deux questions

- **RoPE** : comment la position modifie-t-elle la compatibilité entre une requête
  et une clé ?
- **Masque causal** : cette clé a-t-elle le droit de contribuer à cette requête ?

Une rotation correcte ne bloque pas le futur. Un masque correct sans encodage
de position n'implémente pas **RoPE**.

### Étendre la fenêtre n'est pas changer un nombre

La fréquence de base, la dimension des têtes, le nombre de positions vues à
l'entraînement et l'éventuelle stratégie de scaling déterminent le comportement
hors de la plage habituelle.

Modifier seulement `max_position_embeddings` permet parfois d'allouer une
séquence plus longue, mais ne prouve pas que le modèle conserve sa qualité.
Les variantes de scaling de **RoPE** doivent être lues dans la configuration et
évaluées avec le [[glossaire/checkpoint|checkpoint]] concerné.

### Position absolue du cache

Pendant le decode, le nouveau token reçoit la position qui suit celles déjà
présentes dans le [[glossaire/cache-kv|cache KV]]. Recommencer arbitrairement à zéro tout en
réutilisant des clés anciennes rend les rotations incompatibles.

Le cache doit donc transporter ou permettre de reconstruire la longueur déjà
vue et la convention de position.
