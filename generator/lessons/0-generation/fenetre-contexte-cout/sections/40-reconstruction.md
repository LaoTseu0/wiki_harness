## Reconstruction

Un budget sans troncature implicite :

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ContextBudget:
    capacity: int
    input_tokens: int
    reserved_output: int

    @property
    def remaining(self) -> int:
        return self.capacity - self.input_tokens

    def validate(self) -> None:
        if min(self.capacity, self.input_tokens, self.reserved_output) < 0:
            raise ValueError("budget négatif")
        if self.input_tokens + self.reserved_output > self.capacity:
            raise ValueError("fenêtre de contexte insuffisante")

ContextBudget(capacity=2048, input_tokens=1800, reserved_output=248).validate()
```

Le laboratoire fera ensuite varier la longueur réelle d'un prompt et mesurera
séparément temps de **prefill**, temps par token et mémoire lorsque le runtime les
expose.
