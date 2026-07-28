## Reconstruction

Implémenter trois filtres sur des couples `(token_id, probabilité)` :

```python
def top_k(probs: list[float], k: int) -> set[int]:
    if k <= 0:
        raise ValueError("k doit être positif")
    ordre = sorted(range(len(probs)), key=probs.__getitem__, reverse=True)
    return set(ordre[:min(k, len(probs))])

def top_p(probs: list[float], seuil: float) -> set[int]:
    if not 0.0 < seuil <= 1.0:
        raise ValueError("top_p hors limites")
    ordre = sorted(range(len(probs)), key=probs.__getitem__, reverse=True)
    gardes, cumul = set(), 0.0
    for index in ordre:
        gardes.add(index)
        cumul += probs[index]
        if cumul >= seuil:
            break
    return gardes

def min_p(probs: list[float], alpha: float) -> set[int]:
    limite = alpha * max(probs)
    gardes = {index for index, p in enumerate(probs) if p >= limite}
    return gardes or {probs.index(max(probs))}
```

Appliquer ces fonctions à une distribution plate puis à une distribution
concentrée rend leur différence structurelle visible.
