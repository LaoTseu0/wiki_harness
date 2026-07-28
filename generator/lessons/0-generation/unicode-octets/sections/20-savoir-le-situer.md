## Savoir le situer

**Ensemble** — [[generator/guardrails/schema/references/representation-texte.canvas|carte de
concepts de la représentation du texte]]. Une arête indique une relation de
représentation. Elle n'indique pas une étape d'exécution.

**Élément ouvert** — `point-code`. Il relie le caractère abstrait, la valeur
scalaire encodable, la chaîne Python, le grapheme cluster et les octets produits
par UTF-8.

**L'essentiel** — un texte ne possède pas une frontière universelle appelée
« caractère ». Le point de code, l'octet, l'élément de `str`, le grapheme
cluster visible et le token sont des unités différentes.

**Recomposer** — le tokenizer reçoit une chaîne ou des octets selon son
contrat. Toute confusion en amont sur l'encodage ou les frontières modifie la
séquence de tokens et se propage jusqu'aux logits.

![[unicode-octets.canvas]]
