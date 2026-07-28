## Reconstruction

**RMSNorm** et une mise à jour résiduelle :

```python
from math import sqrt

def rms_norm(
    x: list[float], gain: list[float], epsilon: float = 1e-6
) -> list[float]:
    moyenne_carres = sum(v * v for v in x) / len(x)
    inverse_rms = 1.0 / sqrt(moyenne_carres + epsilon)
    return [g * v * inverse_rms for v, g in zip(x, gain)]

def ajouter_residu(
    residu: list[float], mise_a_jour: list[float]
) -> list[float]:
    if len(residu) != len(mise_a_jour):
        raise ValueError("dimensions incompatibles")
    return [x + delta for x, delta in zip(residu, mise_a_jour)]
```

Faire varier l'amplitude de `x` montre que **RMSNorm** remet l'échelle sous
contrôle, tandis que l'addition conserve exactement une mise à jour nulle.
