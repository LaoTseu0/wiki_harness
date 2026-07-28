---
id: py-environnements-dependances
type: leçon
titre: Environnements et dépendances
parcours: preambule-python
statut: brouillon
tags: [python, environnement, dependances, packaging]
created: 2026-07-25
updated: 2026-07-28
verified: 2026-07-25
processus: aucun — préparation du projet
schema: environnement-projet-python
element: environnement-virtuel
brique: contracts
contrat: aucun — prépare le socle de packaging de Praxis
---

# Environnements et dépendances

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> cas pratique :
> [isoler et reconstruire un projet Python](../../cas-pratique/preambule-python/01-isoler-reconstruire-projet.md)

## Prérequis

Aucun prérequis interne. La leçon suppose seulement l'usage courant d'un
terminal et de Git.

## Savoir le situer

**Ensemble** —
[[generator/guardrails/schema/references/environnement-projet-python.canvas|architecture d'un projet Python]].  
Les groupes représentent des frontières versionnées, locales ou distribuées.
Chaque arête nomme une relation ; sa direction ne représente pas le temps.

**Élément ouvert** — `environnement-virtuel`.  
L'interpréteur de base le fonde, le [[glossaire/frontend-de-projet|frontend de projet]] le crée et le
synchronise, `pyproject.toml` en contraint le contenu, le [[glossaire/lockfile|lockfile]] précise la
résolution et `site-packages` reçoit les distributions installées.

**L'essentiel** — Un [[glossaire/environnement-virtuel|environnement virtuel]] est une matérialisation locale et
jetable. La déclaration appartient à `pyproject.toml`, la résolution exacte au
**lockfile** et l'état installé à `.venv`.

**Recomposer** — Supprimer `.venv` ne supprime ni l'intention du projet ni sa
résolution. Une synchronisation peut le reconstruire. Modifier directement son
contenu crée au contraire un état qui n'est expliqué ni par `pyproject.toml` ni
par le **lockfile**.

![[py-environnements-dependances.canvas]]

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

## Reconstruction

Créer un environnement avec la bibliothèque standard, puis observer la
frontière sans installer de dépendance.

Sous PowerShell :

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix); print(sys.base_prefix); print(sys.prefix != sys.base_prefix)"
```

Sous Linux ou macOS :

```bash
python3 -m venv .venv
./.venv/bin/python -c "import sys; print(sys.executable); print(sys.prefix); print(sys.base_prefix); print(sys.prefix != sys.base_prefix)"
```

L'expérience doit montrer deux préfixes distincts et la valeur `True`. Elle
n'établit encore rien sur le resolver, le **lockfile** ou le packaging : elle isole
seulement le mécanisme de l'**environnement virtuel**.

## Décision et dépôt dans Praxis

- **Décision** — Praxis et Mnémos posséderont chacun leur `pyproject.toml`, leur
  `.venv` et leur **lockfile**. Aucun environnement Python ne vivra à la racine.
- **Frontend** — **uv** gérera l'interpréteur, la résolution, le **lockfile**, la
  synchronisation et l'exécution.
- **Backend initial** — `uv_build` construira les packages Python purs.
- **Alternatives** — `venv` + pip + build, Hatchling, PDM et Poetry restent des
  confrontations possibles.
- **Critère** — conserver les métadonnées standard tout en obtenant une
  reconstruction rapide et un échec explicite lorsque le **lockfile** dérive.
- **Coût accepté** — `uv.lock` dépend de **uv** et `uv_build` suit un rythme de
  version rapide.
- **Condition de révision** — besoin d'extensions natives, de scripts de build
  complexes ou d'une interopérabilité que l'export `pylock.toml` ne couvre pas.
- **Contrat** — aucun contrat Python public n'est encore déposé. La leçon
  prépare le contenant des futurs contrats de Praxis.

## Limites et cas d'échec

- Un **environnement virtuel** isole des packages ; il n'isole ni les fichiers, ni
  le réseau, ni les processus. Ce n'est pas une sandbox.
- Un **lockfile** décrit une résolution. Il ne prouve pas que `.venv` lui
  correspond tant qu'un outil ne vérifie ou ne synchronise pas cet état.
- Une résolution multi-plateforme peut sélectionner des distributions
  différentes selon le système d'exploitation, l'architecture ou la version de
  Python.
- Une installation éditable peut masquer un fichier absent du **wheel**. La leçon
  suivante ouvrira le layout `src/` et les imports.
- Construire un **wheel** ne prouve ni la sûreté de ses dépendances ni celle de
  leur chaîne de publication.
- Les comportements propres à **uv** sont vérifiés au 25 juillet 2026 et restent
  distincts des garanties du standard Python.

## Se tester

1. Après la suppression de `.venv`, quelles informations permettent de le
   reconstruire et laquelle ne doit pas être récupérée depuis Git ?
2. Pourquoi un `pip install` manuel peut-il produire un environnement
   fonctionnel mais non reproductible ?
3. Pourquoi le **lockfile** ne peut-il pas remplacer `pyproject.toml` ?
4. Quelles responsabilités restent distinctes lorsque **uv** est à la fois
   frontend et fournisseur du backend `uv_build` ?
5. Pourquoi l'activation d'un environnement n'est-elle pas la preuve utilisée
   par Python pour déterminer `sys.prefix` ?

[Vérifier les réponses et le cas
pratique](../../corrections/preambule-python/01-environnements-dependances.md).

## Références

- [Python 3.14 — `venv`](https://docs.python.org/3.14/library/venv.html) —
  création, isolation, caractère jetable et non-déplaçable.
- [PyPA — écrire `pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) —
  responsabilités de `[build-system]`, `[project]` et `[tool]`.
- [PyPA — groupes de dépendances](https://packaging.python.org/en/latest/specifications/dependency-groups/) —
  dépendances internes absentes des métadonnées construites.
- [PyPA — flux de packaging](https://packaging.python.org/en/latest/flow/) —
  relation entre frontend, backend, **sdist** et **wheel**.
- [uv — structure d'un projet](https://docs.astral.sh/uv/concepts/projects/layout/) —
  `.venv`, `uv.lock` et relation avec `pylock.toml`.
- [uv — verrouillage et synchronisation](https://docs.astral.sh/uv/concepts/projects/sync/) —
  effets de `uv run`, `--locked`, mise à jour et synchronisation.
- [uv — backend de build](https://docs.astral.sh/uv/configuration/build-backend/) —
  portée actuelle et limites de `uv_build`.
