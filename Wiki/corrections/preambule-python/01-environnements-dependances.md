---
id: correction-py-environnements-dependances
type: correction
titre: Correction — environnements et dépendances
parcours: preambule-python
created: 2026-07-25
updated: 2026-07-25
lecon: py-environnements-dependances
---

# Correction — environnements et dépendances

> [Revenir à la leçon](../../parcours/preambule-python/01-environnements-dependances.md) ·
> [revenir au cas pratique](../../cas-pratique/preambule-python/01-isoler-reconstruire-projet.md)

## Se tester

### 1 · Reconstruire après la suppression de `.venv`

`pyproject.toml` conserve les contraintes et `uv.lock` la résolution choisie.
L'interpréteur compatible et uv permettent de matérialiser un nouvel
environnement. `.venv` ne doit pas être récupéré depuis Git : il contient un
état installé dérivé, des chemins locaux et une relation avec un interpréteur
de base.

### 2 · L'installation manuelle

Une installation manuelle modifie `site-packages` sans modifier nécessairement
la déclaration ou le lockfile. Le programme peut alors importer la
distribution sur cette machine, mais une synchronisation sur une autre machine
ne sait pas qu'elle est nécessaire.

La panne se situe entre l'état installé et ses deux sources explicatives. Elle
ne prouve pas que le resolver a choisi une mauvaise version.

### 3 · Le lockfile ne remplace pas `pyproject.toml`

Le lockfile est le résultat d'une résolution. Il ne porte pas à lui seul
l'intention publique du projet : plage de versions Python, dépendances runtime,
extras, métadonnées et backend de build.

Modifier seulement le lockfile reviendrait à modifier un résultat calculé sans
changer les contraintes qui doivent le produire.

### 4 · uv frontend et `uv_build` backend

Le frontend reçoit l'intention de l'utilisateur : synchroniser, lancer ou
construire. Il résout les dépendances et prépare les environnements nécessaires.

Le backend reçoit une demande de build normalisée et transforme l'arbre de
sources en sdist ou en wheel. Le fait que les deux implémentations appartiennent
au même projet ne fusionne pas leurs contrats.

### 5 · Activation et identité

L'activation modifie l'environnement du terminal afin que `python` désigne
prioritairement l'exécutable de `.venv`. Python reconnaît l'environnement à
partir de l'interpréteur lancé et de sa configuration, notamment
`pyvenv.cfg`.

Lancer directement `.venv\Scripts\python.exe` sous Windows ou
`.venv/bin/python` sous Unix établit donc la même frontière sans script
d'activation.

## Cas pratique

Une réalisation correcte doit faire apparaître trois états différents :

1. après `uv init`, le projet possède ses sources et `pyproject.toml`, mais le
   lockfile et l'environnement peuvent ne pas encore exister ;
2. après `uv add`, la déclaration, le lockfile et `.venv` sont matérialisés ;
3. après le déplacement de `.venv` et `uv sync --locked`, un nouvel
   environnement est construit sans changer la résolution.

Le wheel et le sdist appartiennent à `dist/`. Ils ne doivent pas être confondus
avec le package installé dans `site-packages`.

### Variation du `pyproject.toml`

Après une modification qui rend le lockfile obsolète, `uv sync --locked` doit
refuser de poursuivre. La réussite de cette variation est l'observation de ce
refus et l'absence de modification silencieuse du lockfile.

### Distribution ajoutée hors déclaration

La distribution ajoutée avec l'interface pip de uv existe seulement dans
l'environnement. Une synchronisation exacte depuis le lockfile doit retirer
cet élément étranger. Si elle reste présente, vérifier que la commande employée
n'utilise pas un mode de synchronisation inexact.

### Environnement déplacé

Le dossier renommé peut contenir des scripts dont les chemins pointent encore
vers son ancien emplacement. Même lorsqu'une commande semble fonctionner, cet
état ne constitue pas une preuve de portabilité. Le résultat attendu est la
reconstruction, pas la réparation du dossier déplacé.
