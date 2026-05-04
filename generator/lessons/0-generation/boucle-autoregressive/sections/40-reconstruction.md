## Reconstruction

Une boucle indépendante de tout modèle réel :

```python
from collections.abc import Callable

NextLogits = Callable[[list[int]], list[float]]
Choose = Callable[[list[float]], int]
ShouldStop = Callable[[list[int], int], bool]

def generer(
    prompt: list[int],
    prochains_logits: NextLogits,
    choisir: Choose,
    arreter: ShouldStop,
    maximum: int,
) -> list[int]:
    sequence = prompt[:]
    produits: list[int] = []
    for _ in range(maximum):
        logits = prochains_logits(sequence)
        token_id = choisir(logits)
        sequence.append(token_id)
        produits.append(token_id)
        if arreter(produits, token_id):
            break
    return produits
```

Un `prochains_logits` scripté permet de tester la boucle sans poids ni réseau.
Le maximum reste obligatoire même si une fonction EOS est fournie.
