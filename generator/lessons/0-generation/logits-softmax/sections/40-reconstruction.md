## Reconstruction

Une implémentation stable :

```python
from math import exp, inf, isnan

def softmax(logits: list[float]) -> list[float]:
    if not logits or any(isnan(logit) or logit == inf for logit in logits):
        raise ValueError("logits invalides")
    maximum = max(logits)
    if maximum == -inf:
        raise ValueError("tous les candidats sont masqués")
    poids = [exp(logit - maximum) for logit in logits]
    total = sum(poids)
    if total == 0.0:
        raise ValueError("distribution vide")
    return [poids_i / total for poids_i in poids]

logits = [1000.0, 1001.0, 999.0]
probabilites = softmax(logits)
assert abs(sum(probabilites) - 1.0) < 1e-12
assert probabilites.index(max(probabilites)) == 1
```

Ajouter la même constante à tous les éléments doit laisser la distribution
inchangée à la tolérance choisie.
