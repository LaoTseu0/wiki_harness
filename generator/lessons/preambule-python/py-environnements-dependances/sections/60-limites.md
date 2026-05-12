## Limites et cas d'échec

- Un environnement virtuel isole des packages ; il n'isole ni les fichiers, ni
  le réseau, ni les processus. Ce n'est pas une sandbox.
- Un lockfile décrit une résolution. Il ne prouve pas que `.venv` lui
  correspond tant qu'un outil ne vérifie ou ne synchronise pas cet état.
- Une résolution multi-plateforme peut sélectionner des distributions
  différentes selon le système d'exploitation, l'architecture ou la version de
  Python.
- Une installation éditable peut masquer un fichier absent du wheel. La leçon
  suivante ouvrira le layout `src/` et les imports.
- Construire un wheel ne prouve ni la sûreté de ses dépendances ni celle de
  leur chaîne de publication.
- Les comportements propres à uv sont vérifiés au 25 juillet 2026 et restent
  distincts des garanties du standard Python.
