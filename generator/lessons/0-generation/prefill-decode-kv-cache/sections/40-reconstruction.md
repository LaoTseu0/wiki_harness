## Reconstruction

Compter les positions retraitées dans une boucle conceptuelle :

```python
def positions_sans_cache(prompt: int, nouveaux: int) -> int:
    return sum(prompt + deja_generes for deja_generes in range(nouveaux))

def positions_avec_cache(prompt: int, nouveaux: int) -> int:
    if nouveaux == 0:
        return 0
    return prompt + (nouveaux - 1)

assert positions_sans_cache(100, 10) == 1045
assert positions_avec_cache(100, 10) == 109
```

Ce compteur représente les positions données aux projections du modèle, pas le
nombre d'opérations d'attention ni une latence. Même avec cache, chaque nouvelle
requête parcourt encore les clés autorisées dans une attention complète.
