## Reconstruction

Apprendre un **BPE** miniature sur un corpus volontairement réduit :

```python
from collections import Counter

corpus = {
    tuple("bas") + ("</w>",): 5,
    tuple("basse") + ("</w>",): 3,
    tuple("base") + ("</w>",): 4,
}

def paires(mots: dict[tuple[str, ...], int]) -> Counter[tuple[str, str]]:
    resultat: Counter[tuple[str, str]] = Counter()
    for symboles, frequence in mots.items():
        resultat.update(
            {paire: frequence for paire in zip(symboles, symboles[1:])}
        )
    return resultat

def fusionner(
    mots: dict[tuple[str, ...], int], paire: tuple[str, str]
) -> dict[tuple[str, ...], int]:
    fusion = "".join(paire)
    resultat = {}
    for symboles, frequence in mots.items():
        nouveaux = []
        index = 0
        while index < len(symboles):
            if tuple(symboles[index:index + 2]) == paire:
                nouveaux.append(fusion)
                index += 2
            else:
                nouveaux.append(symboles[index])
                index += 1
        resultat[tuple(nouveaux)] = frequence
    return resultat

for _ in range(4):
    paire, _ = paires(corpus).most_common(1)[0]
    print("fusion", paire)
    corpus = fusionner(corpus, paire)
```

Cette reconstruction montre l'apprentissage des fusions. Elle ne reproduit ni
le pré-**tokenizer**, ni les optimisations, ni toutes les règles d'égalité d'un
**tokenizer** de production.
