# Template

Règle de sérialisation qui transforme une structure en texte ou en tokens selon
un format déterminé. Un Template de chat encode notamment les rôles, les
séparateurs et les marqueurs attendus par le modèle.

Une même liste de messages peut être sérialisée avec ou sans ouverture du tour
assistant. Comparer les identifiants obtenus révèle l’effet de ce choix sur l’entrée
du modèle.
