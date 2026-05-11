## Reconstruction

Rendre visible la sérialisation avec un Template jouet :

```python
ROLE = {
    "system": "<|system|>",
    "user": "<|user|>",
    "assistant": "<|assistant|>",
}
FIN_TOUR = "<|end|>"

def rendre(messages: list[dict[str, str]], *, ouvrir_assistant: bool) -> str:
    morceaux = []
    for message in messages:
        morceaux.extend(
            [ROLE[message["role"]], "\n", message["content"], FIN_TOUR, "\n"]
        )
    if ouvrir_assistant:
        morceaux.extend([ROLE["assistant"], "\n"])
    return "".join(morceaux)
```

Afficher `repr(rendre(...))` rend les retours à la ligne et les espaces
observables. Encoder ensuite cette valeur avec un vrai tokenizer montre que
toute variation de sérialisation modifie les identifiants.
