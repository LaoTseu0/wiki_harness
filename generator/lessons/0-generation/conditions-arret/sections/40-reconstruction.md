## Reconstruction

Une politique minimale :

```python
from dataclasses import dataclass
from enum import StrEnum

class StopReason(StrEnum):
    EOS = "eos"
    STOP_SEQUENCE = "stop_sequence"
    MAX_NEW_TOKENS = "max_new_tokens"

@dataclass(frozen=True)
class StopDecision:
    reason: StopReason | None
    visible_text: str

def evaluer_arret(
    token_id: int,
    texte: str,
    generated_count: int,
    eos_ids: frozenset[int],
    stop_strings: tuple[str, ...],
    max_new_tokens: int,
) -> StopDecision:
    if token_id in eos_ids:
        return StopDecision(StopReason.EOS, texte)
    positions = [
        (texte.find(stop), stop)
        for stop in stop_strings
        if texte.find(stop) >= 0
    ]
    if positions:
        position, _ = min(positions)
        return StopDecision(StopReason.STOP_SEQUENCE, texte[:position])
    if generated_count >= max_new_tokens:
        return StopDecision(StopReason.MAX_NEW_TOKENS, texte)
    return StopDecision(None, texte)
```

Cette version travaille sur le texte cumulé. Un streamer réel doit aussi
retenir les suffixes qui sont des préfixes possibles d'une **stop sequence**.
