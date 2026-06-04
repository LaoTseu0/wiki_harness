# BPE

Famille de tokenisation qui construit des unités en fusionnant progressivement
des paires fréquentes. Les règles apprises déterminent le découpage obtenu.

Avec les unités `a`, `b`, `c` et une règle qui fusionne `a` et `b`, la séquence
devient `ab`, `c`. Une fusion supplémentaire exigerait une règle applicable à cette
nouvelle paire.
