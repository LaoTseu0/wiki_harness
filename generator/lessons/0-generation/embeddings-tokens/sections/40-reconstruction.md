## Reconstruction

Une table jouet rend la sélection observable :

```python
EMBEDDINGS = [
    [0.0, 0.0, 0.0],   # padding
    [0.2, -0.1, 0.5],  # token 1
    [-0.4, 0.8, 0.1],  # token 2
]

def embed(token_ids: list[int]) -> list[list[float]]:
    if any(token_id < 0 or token_id >= len(EMBEDDINGS) for token_id in token_ids):
        raise ValueError("identifiant hors vocabulaire")
    return [EMBEDDINGS[token_id][:] for token_id in token_ids]

assert embed([1, 2, 1])[0] == embed([1, 2, 1])[2]
```

L'égalité finale porte seulement sur les vecteurs initiaux. Une couche
d'attention causale pourra ensuite produire deux représentations différentes
pour les deux occurrences.
