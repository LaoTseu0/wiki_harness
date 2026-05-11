## Reconstruction

Injecter une instance locale de `Random` :

```python
from random import Random

def tirer(probabilites: list[float], rng: Random) -> int:
    if not probabilites or any(poids < 0.0 for poids in probabilites):
        raise ValueError("poids non négatifs requis")
    total = sum(probabilites)
    if total <= 0.0:
        raise ValueError("distribution vide")
    seuil = rng.random() * total
    cumul = 0.0
    for index, poids in enumerate(probabilites):
        cumul += poids
        if seuil < cumul:
            return index
    return len(probabilites) - 1  # protège l'arrondi de la somme

rng_a = Random(1234)
rng_b = Random(1234)
serie_a = [tirer([0.1, 0.3, 0.6], rng_a) for _ in range(10)]
serie_b = [tirer([0.1, 0.3, 0.6], rng_b) for _ in range(10)]
assert serie_a == serie_b
```

Intercaler un tirage supplémentaire dans `rng_b` doit décaler la suite. Cette
variation rend l'état consommable du générateur visible.
