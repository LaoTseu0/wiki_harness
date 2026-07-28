## Connaissances

### **Prefill**

Le **prefill** traite les $N$ tokens du prompt sous masque causal. Les opérations
sur les positions peuvent être exécutées en parallèle parce que toutes les
valeurs du prompt sont déjà connues.

Chaque couche produit les clés et valeurs correspondant à ces positions. Le
runtime conserve celles qui seront nécessaires aux futurs calculs d'attention.
Le premier logit de génération provient de la dernière position utile du
**prefill**.

Le temps avant le premier token inclut donc Template, tokenisation, transfert
des entrées, **prefill** et choix du premier token. Il ne se réduit pas au seul
**sampling**.

### **Decode**

Après avoir choisi un token, le **decode** calcule sa nouvelle représentation
position par position. À chaque couche :

1. produire `Q`, `K` et `V` pour la nouvelle position ;
2. appliquer sa position à `Q` et `K` ;
3. ajouter le nouveau `K` et `V` au cache ;
4. comparer la nouvelle requête aux clés accessibles ;
5. agréger les valeurs et poursuivre le bloc.

Sans cache, le runtime recalculerait les projections `K` et `V` de tout le
préfixe à chaque tour. Avec cache, il les relit.

### Ce que le cache contient

Un [[glossaire/cache-kv|cache KV]] courant contient, pour chaque couche, les clés et valeurs des
positions conservées, ainsi que les informations permettant de les positionner
et de les masquer correctement.

Il ne contient pas :

- une réponse future ;
- les requêtes de toutes les étapes comme une obligation générale ;
- la sortie du MLP comme substitut au passage de la nouvelle position ;
- une mémoire sémantique réutilisable par n'importe quel modèle.

### Le coût n'est pas supprimé

Avec une attention complète standard, la nouvelle requête doit encore être
comparée aux clés précédentes. Le travail d'attention et la mémoire du cache
croissent avec le nombre de positions conservées.

Le cache évite surtout de recalculer les représentations passées. Il échange de
la mémoire contre du calcul. Une attention à fenêtre glissante ou par chunks
peut borner certaines couches, mais change la portée du contexte accessible.

### Stratégies de cache

- un cache dynamique grandit avec la séquence ;
- un cache statique préalloue une capacité et facilite certaines compilations,
  au prix d'espace et de calcul masqué ;
- un cache déporté échange des transferts contre de la mémoire accélérateur ;
- un cache quantifié réduit la mémoire avec un coût de conversion et une
  possible perte numérique.

Ces propriétés doivent être mesurées sur le runtime et le matériel concernés.

### Compatibilité

Un cache dépend au minimum du checkpoint, des couches, de la convention de
position, du préfixe exact et de la configuration d'attention. Le réutiliser
avec un autre Template ou un autre modèle donne des états sans rapport avec le
nouvel **Input**.

Partager un cache de préfixe stable peut être une optimisation volontaire. Le
préfixe doit être identique au niveau des identifiants et sa frontière de
confidentialité doit être respectée.
