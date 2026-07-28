## Reconstruction

Une seule fréquence suffit pour observer l'identité relative :

```python
from math import cos, sin

def rotation(vecteur: tuple[float, float], angle: float) -> tuple[float, float]:
    x, y = vecteur
    return (x * cos(angle) - y * sin(angle),
            x * sin(angle) + y * cos(angle))

def produit(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]

q = (1.0, 0.4)
k = (0.3, 0.8)
frequence = 0.2

score_2_5 = produit(rotation(q, 2 * frequence), rotation(k, 5 * frequence))
score_7_10 = produit(rotation(q, 7 * frequence), rotation(k, 10 * frequence))
assert abs(score_2_5 - score_7_10) < 1e-12
```

Les deux paires ont le même déplacement. Cette expérience ne reproduit ni les
nombreuses fréquences, ni les formes tensorielles, ni les variantes de scaling.
