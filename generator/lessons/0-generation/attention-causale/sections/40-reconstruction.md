## Reconstruction

Une tête sans dépendance tensorielle :

```python
from math import exp, sqrt

def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def softmax(valeurs: list[float]) -> list[float]:
    maximum = max(valeurs)
    exp_values = [exp(v - maximum) for v in valeurs]
    total = sum(exp_values)
    return [v / total for v in exp_values]

def attention(
    q: list[float],
    keys: list[list[float]],
    values: list[list[float]],
) -> tuple[list[float], list[float]]:
    scores = [dot(q, key) / sqrt(len(q)) for key in keys]
    poids = softmax(scores)
    sortie = [
        sum(poids[j] * values[j][dimension] for j in range(len(values)))
        for dimension in range(len(values[0]))
    ]
    return sortie, poids
```

Pour simuler la causalité à la position `i`, ne fournir que les clés et valeurs
`0..i`, ou masquer explicitement le reste avant softmax.
