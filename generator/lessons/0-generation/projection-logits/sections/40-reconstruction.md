## Reconstruction

Projeter un vecteur caché vers quatre candidats :

```python
def produit(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def projeter(
    hidden: list[float],
    poids_vocabulaire: list[list[float]],
    biais: list[float] | None = None,
) -> list[float]:
    biais = biais or [0.0] * len(poids_vocabulaire)
    return [
        produit(ligne, hidden) + offset
        for ligne, offset in zip(poids_vocabulaire, biais)
    ]

hidden = [0.5, -1.0, 0.2]
poids = [
    [0.1, 0.4, -0.2],
    [-0.3, 0.2, 0.8],
    [0.7, -0.1, 0.0],
    [0.0, 0.2, 0.5],
]
logits = projeter(hidden, poids)
assert len(logits) == len(poids)
```

Le classement des scores est observable, mais aucune valeur n'est encore une
probabilité.
