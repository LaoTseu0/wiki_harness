# Modelfile

> [glossaire](index.md)

Le fichier de configuration d'un modèle chez Ollama : il déclare le modèle de
base, le [template de chat](../fondamentaux/template-de-chat.md) et les
paramètres par défaut (temperature, top_p, top_k…). Ces défauts sont le piège
du [sampling](../fondamentaux/sampling.md) : une option absente
de la requête n'est pas neutre, elle retombe sur la valeur du Modelfile.
`/api/show` les expose.
