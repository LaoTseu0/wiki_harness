# decoder-only

Architecture de Transformer qui prédit chaque nouveau token à partir du préfixe
déjà disponible, sans encodeur séparé. Un masque causal interdit l’accès aux
positions futures.

Pour la séquence A, B, C, les scores à la position B servent à prédire C à partir de A
et B. Le calcul à cette position exclut C, même si toute la séquence est disponible à
l’entraînement.
