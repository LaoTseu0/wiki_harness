## Reconstruction

Rendre les rôles explicites avec une configuration minimale :

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class SpecialTokens:
    bos_ids: tuple[int, ...]
    eos_ids: frozenset[int]
    pad_id: int | None
    role_ids: dict[str, int]

TOKENS = SpecialTokens(
    bos_ids=(1,),
    eos_ids=frozenset({2, 7}),
    pad_id=0,
    role_ids={"user": 10, "assistant": 11},
)

def est_fin(token_id: int, tokens: SpecialTokens) -> bool:
    return token_id in tokens.eos_ids

assert est_fin(7, TOKENS)
assert not est_fin(TOKENS.pad_id, TOKENS)
```

Les nombres sont ceux d'un vocabulaire fictif. L'expérience montre pourquoi le
runtime transporte des identifiants issus du tokenizer au lieu de constantes
globales supposées universelles.
