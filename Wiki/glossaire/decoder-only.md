# decoder-only

Architecture de Transformer qui prédit chaque nouveau token à partir du préfixe
déjà disponible, sans encodeur séparé. Un masque causal interdit l’accès aux
positions futures.
