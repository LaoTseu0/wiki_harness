## Reconstruction

Observer les représentations sans bibliothèque externe :

```python
import unicodedata

textes = {
    "précomposé": "é",
    "décomposé": "e\u0301",
    "famille": "👨‍👩‍👧‍👦",
}

for nom, texte in textes.items():
    points = [f"U+{ord(caractere):04X}" for caractere in texte]
    octets = texte.encode("utf-8")
    print(nom, len(texte), points, octets.hex(" "))

assert unicodedata.normalize("NFC", textes["précomposé"]) == unicodedata.normalize(
    "NFC", textes["décomposé"]
)
assert textes["précomposé"].encode("utf-8") != textes["décomposé"].encode("utf-8")
```

L'expérience isole trois faits : le rendu ne fixe pas la séquence de points de
code, `len(str)` ne compte pas les octets et une normalisation peut rendre deux
séquences égales sans qu'elles l'aient été au départ.
