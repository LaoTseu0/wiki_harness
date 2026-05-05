## Reconstruction

Le décodeur UTF-8 incrémental de Python :

```python
import codecs

decodeur = codecs.getincrementaldecoder("utf-8")(errors="strict")

assert decodeur.decode(bytes.fromhex("c3"), final=False) == ""
assert decodeur.decode(bytes.fromhex("a9"), final=False) == "é"
assert decodeur.decode(b"", final=True) == ""
```

Une variante doit fournir seulement `C3`, puis appeler `final=True` : le mode
strict signale alors que le flux se termine au milieu d'une séquence.
