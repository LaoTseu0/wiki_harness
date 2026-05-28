## Connaissances

### L'**environnement virtuel** est un état dérivé

Une installation Python fournit un **interpréteur de base**. `venv` crée à
partir de lui un répertoire qui possède son propre exécutable Python, son
`pyvenv.cfg` et son emplacement `site-packages`.

Par défaut, les distributions installées dans cet environnement sont isolées
de celles de l'interpréteur de base. Le code du projet ne vit pas dans
`.venv` : il reste dans l'arbre de sources et peut être installé dans
l'environnement.

Deux attributs rendent la frontière observable :

```python
import sys

dans_un_venv = sys.prefix != sys.base_prefix
```

`sys.base_prefix` désigne l'installation dont l'environnement dérive.
`sys.prefix` désigne l'environnement actif pour le processus courant.

L'activation ne crée pas cette identité. Elle place principalement les
exécutables de `.venv` en tête du `PATH`. Appeler directement son interpréteur
ou employer `uv run` évite de dépendre de l'état du terminal.

La [documentation Python 3.14 sur `venv`](https://docs.python.org/3.14/library/venv.html)
qualifie les **environnements virtuels** de jetables, non versionnés et non
déplaçables : leur contrat est d'être recréés depuis les déclarations du
projet, pas copiés entre machines. Cette propriété vient des chemins absolus et
de la relation conservée avec l'interpréteur de base.

### Déclaration, résolution et installation

Trois objets répondent à trois questions différentes :

| Objet | Question | Producteur | Versionné |
|---|---|---|---|
| `pyproject.toml` | Quelles contraintes et métadonnées le projet déclare-t-il ? | humain et outils autorisés | oui |
| `uv.lock` | Quelle résolution précise satisfait actuellement ces contraintes ? | resolver [[glossaire/uv|uv]] | oui |
| `.venv` | Qu'est-ce qui est effectivement installé pour ce projet local ? | synchroniseur | non |

Une contrainte comme `httpx>=0.28,<1` autorise plusieurs versions. Le resolver
choisit un ensemble compatible et l'inscrit dans le **lockfile**. Le synchroniseur
matérialise ensuite cet ensemble dans l'environnement.

Un `pip install` manuel dans `.venv` ne modifie pas nécessairement
`pyproject.toml` ou le **lockfile**. L'environnement peut alors fonctionner sur une
machine tout en étant impossible à expliquer ou à reconstruire.

### Les responsabilités de `pyproject.toml`

Le [format `pyproject.toml` maintenu par la
PyPA](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
sépare plusieurs espaces de noms :

| Table | Responsabilité |
|---|---|
| `[build-system]` | [[glossaire/backend-de-build|backend de build]] et dépendances nécessaires pour l'exécuter |
| `[project]` | métadonnées distribuées, version de Python et dépendances runtime |
| `[dependency-groups]` | dépendances internes de développement, de test ou de documentation |
| `[tool.<nom>]` | configuration propre à un outil |

La [spécification des groupes de
dépendances](https://packaging.python.org/en/latest/specifications/dependency-groups/)
exclut leur contenu des métadonnées de la distribution construite. Ils
conviennent donc à pytest ou aux outils de qualité. Une dépendance nécessaire
au fonctionnement de Praxis appartient au contraire à
`[project].dependencies`.

Les `optional-dependencies` de `[project]` ont encore une autre portée : elles
décrivent des fonctionnalités publiques installables comme des extras. Elles ne
remplacent pas les groupes internes de développement.

### Frontend, backend et artefacts

Le **frontend de projet** orchestre les opérations demandées : résoudre,
verrouiller, synchroniser, lancer ou construire. Le **backend de build**
transforme l'arbre de sources selon le contrat de `[build-system]`. Le [flux de
packaging de la PyPA](https://packaging.python.org/en/latest/flow/) conserve
cette frontière entre l'outil qui demande une construction et celui qui
l'exécute.

Même lorsque **uv** fournit les deux implémentations, les responsabilités restent
distinctes :

- `uv` agit comme frontend, resolver et synchroniseur ;
- `uv_build` agit comme **backend de build** ;
- le [[glossaire/wheel|wheel]] est l'artefact installable ;
- le [[glossaire/sdist|sdist]] est l'archive source utilisée pour reconstruire des distributions.

Cette séparation permet de remplacer le backend sans changer la signification
de `[project]`, ou d'utiliser un autre frontend capable de suivre les mêmes
standards.

### La synchronisation avec **uv**

Selon son [contrat de verrouillage et de
synchronisation](https://docs.astral.sh/uv/concepts/projects/sync/), `uv run`
vérifie normalement le **lockfile** et l'environnement avant de lancer la commande.
Ce confort implique un effet de bord possible : une commande locale peut
mettre à jour la résolution si les déclarations ont changé.

Dans un contrôle automatisé, `uv run --locked` ou `uv lock --check` transforme
ce décalage en erreur au lieu de modifier le **lockfile**. Une nouvelle version
publiée sur l'index ne rend pas à elle seule `uv.lock` périmé ; la mise à jour
des versions verrouillées reste une décision explicite.

La [documentation de la structure d'un projet
uv](https://docs.astral.sh/uv/concepts/projects/layout/) précise que `uv.lock`
est propre à **uv**. Le format standard `pylock.toml` peut servir d'artefact
d'échange, mais il ne représente pas encore toutes les fonctions du **lockfile** de
projet **uv**. L'export ne doit donc pas être présenté comme une copie équivalente
dans tous les cas.
