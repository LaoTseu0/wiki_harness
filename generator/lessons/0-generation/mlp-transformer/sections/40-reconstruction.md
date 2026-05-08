## Reconstruction

Une version scalaire de SiLU et une porte simplifiée :

```python
from math import exp

def silu(x: float) -> float:
    return x / (1.0 + exp(-x))

def swiglu_simplifie(
    gate: list[float], contenu: list[float]
) -> list[float]:
    if len(gate) != len(contenu):
        raise ValueError("dimensions incompatibles")
    return [silu(g) * u for g, u in zip(gate, contenu)]

assert swiglu_simplifie([0.0], [4.0]) == [0.0]
```

La reconstruction ouvre la porte multiplicative. Elle omet volontairement les
trois matrices apprises et la projection de retour.
