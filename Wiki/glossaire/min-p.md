# min-p

Filtre qui écarte les candidats dont la probabilité reste sous une fraction de
la probabilité du meilleur candidat.

Si la meilleure probabilité vaut 0,50 et que min-p vaut 0,20, le seuil vaut 0,10. Un
candidat à 0,12 passe le filtre et un candidat à 0,08 en est exclu.

[Calculer le seuil relatif au meilleur candidat](../parcours/0-generation/12-filtrage-distribution.md#connaissances)
