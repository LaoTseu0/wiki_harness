# Transformers

> [glossaire](index.md)

L'architecture de réseau de neurones sur laquelle reposent tous les LLM
actuels (article *Attention Is All You Need*, 2017). Son idée centrale est
le mécanisme d'**attention** : chaque position d'une séquence peut regarder
toutes les autres pour construire sa représentation, plutôt que de traiter
le texte strictement de gauche à droite comme les architectures
précédentes (RNN, LSTM).

Ce qu'on en retient ici, sans refaire les maths : c'est l'attention qui
donne son coût quadratique et son KV cache — voir la leçon
[attention et KV cache](../fondamentaux/attention-et-kv-cache.md).
