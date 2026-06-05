# cache KV

Mémoire des clés et valeurs déjà calculées par les couches d’attention. Elle
accélère le decode tout en consommant de la mémoire à mesure que le contexte
s’allonge.

Après le traitement de trois positions, un cache complet contient déjà leurs clés et
leurs valeurs. La quatrième requête peut les consulter sans les recalculer.
