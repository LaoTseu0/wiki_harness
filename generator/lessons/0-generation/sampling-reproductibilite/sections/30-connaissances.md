## Connaissances

### Distribution catégorielle

Pour des probabilités $p_1,\ldots,p_V$, le sampler choisit l'indice `i` avec
la probabilité $p_i$. Un tirage possible utilise un nombre uniforme
$u\in[0,1)$ et la première somme cumulée supérieure à `u`.

Le sampler ne « comprend » pas les **tokens**. Il reçoit leur ordre et leurs poids.
Une permutation des probabilités sans la même permutation des identifiants
produit un résultat incohérent.

### État du générateur pseudo-aléatoire

Une **seed** crée un état initial. Chaque tirage consomme cet état et produit le
suivant. Réinitialiser le générateur avec la même **seed** à chaque **token** ne rejoue
pas une génération normale : cela réutilise la première valeur uniforme à
chaque étape.

Un générateur dédié par run évite qu'un autre appel concurrent consomme la
séquence aléatoire globale. Son état peut être enregistré pour diagnostiquer ou
reprendre une expérience, à condition que tout le calcul déterministe autour
reste identique.

### La **seed** ne suffit pas

Pour reproduire une trajectoire, il faut notamment conserver :

- checkpoint et précision des poids ;
- tokenizer, Template et entrée exacte ;
- ordre et paramètres des transformations ;
- runtime, version des bibliothèques et device ;
- algorithmes déterministes ou non ;
- **seed** et état du générateur ;
- politique de cache et de batch susceptible de modifier les calculs.

PyTorch ne garantit pas une reproductibilité complète entre versions,
plateformes ou exécutions CPU et GPU. Certaines opérations disposent d'une
variante déterministe ; l'activer peut réduire les performances ou provoquer
une erreur lorsqu'aucune variante n'est disponible.

### [[glossaire/greedy|Greedy]] et départage

**Greedy** ne consomme pas de hasard. Avec des logits strictement ordonnés et le
même calcul numérique, il choisit le même indice.

Deux valeurs égales demandent une convention, souvent le premier indice
maximal. Deux runtimes peuvent aussi arrondir différemment des scores presque
égaux. « Sans **sampling** » est donc une condition nécessaire mais pas toujours
suffisante pour une égalité bit à bit entre environnements.

### Reproductibilité contre qualité

Reproduire un résultat permet de diagnostiquer une transformation ou une
régression. Cela ne montre pas que la sortie est bonne. Inversement, plusieurs
**seeds** sont nécessaires pour évaluer une stratégie stochastique ; un exemple
favorable ne mesure pas sa distribution de qualité.
