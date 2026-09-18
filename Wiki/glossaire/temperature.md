# température

Paramètre positif qui divise les logits avant softmax. Une valeur faible
concentre la distribution ; une valeur élevée l’aplatit.

Pour des logits (2, 4), une température de 2 donne (1, 2). L’écart passe de 2 à 1, ce
qui rapproche les probabilités après softmax.

[Comparer les écarts avant et après division](../parcours/0-generation/12-filtrage-distribution.md#connaissances)
