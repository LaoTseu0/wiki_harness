---
id: cas-py-environnements-dependances
type: cas-pratique
titre: Isoler et reconstruire un projet Python
parcours: preambule-python
statut: brouillon
created: 2026-07-25
updated: 2026-07-25
lecon: py-environnements-dependances
---

# Isoler et reconstruire un projet Python

> Leçon :
> [[Wiki/parcours/preambule-python/01-environnements-dependances|Environnements et dépendances]]

## Objectif observable

Créer un package Python pur, matérialiser son environnement, construire ses
artefacts, écarter l'environnement local puis le reconstruire depuis les
fichiers versionnables.

## Prérequis matériels et logiciels

- uv installé et accessible avec `uv --version` ;
- un accès initial à l'index de packages ;
- PowerShell, Bash ou un terminal équivalent ;
- un dossier de travail qui ne contient pas déjà de `pyproject.toml`.

Conserver la version affichée par `uv --version` avec les résultats.

## État initial

Créer un dossier de laboratoire distinct de Praxis et de Mnémos. Il ne doit
contenir ni `.venv`, ni lockfile, ni package Python préexistant.

## Étapes

1. Initialiser une bibliothèque Python pure :

   ```text
   uv init --lib --build-backend uv env-lab
   ```

2. Entrer dans `env-lab`, puis relever les fichiers créés avant toute
   synchronisation.
3. Ajouter pytest au groupe de test :

   ```text
   uv add --group test pytest
   ```

4. Relever les différences entre `pyproject.toml`, `uv.lock` et `.venv`.
5. Exécuter sans activation :

   ```text
   uv run python -c "import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)"
   ```

6. Construire le wheel et le sdist :

   ```text
   uv build
   ```

7. Vérifier que les deux artefacts existent dans `dist/`.
8. Fermer les processus qui utilisent `.venv`, puis le renommer en
   `.venv.avant-reconstruction`.
9. Reconstruire l'environnement sans autoriser une nouvelle résolution :

   ```text
   uv sync --locked
   ```

10. Réexécuter la commande de l'étape 5 et comparer les chemins observés.

## Résultats à conserver

- version de uv ;
- arbre des fichiers après initialisation, puis après synchronisation ;
- sections `[project]`, `[build-system]` et `[dependency-groups]` du
  `pyproject.toml` ;
- présence de `uv.lock`, `.venv`, du wheel et du sdist ;
- sorties des deux observations de `sys.executable` et de la frontière
  `sys.prefix != sys.base_prefix`.

Ne pas conserver le contenu complet de `.venv`.

## Critères de réussite

- `.venv` est absent de Git et peut être reconstruit ;
- `uv.lock` est présent et `uv lock --check` réussit ;
- pytest appartient au groupe de test, pas aux dépendances runtime ;
- `uv sync --locked` ne modifie pas le lockfile ;
- le wheel et le sdist sont produits ;
- l'interpréteur exécuté appartient au nouvel environnement.

## Pannes et variations à provoquer

1. Modifier une contrainte dans `pyproject.toml`, puis lancer
   `uv sync --locked`. Conserver l'erreur sans régénérer immédiatement le
   lockfile.
2. Restaurer la déclaration, puis vérifier de nouveau avec
   `uv lock --check`.
3. Ajouter temporairement une distribution avec l'interface pip de uv sans
   l'inscrire au projet. Comparer l'état installé aux déclarations, puis
   reconstruire exactement l'environnement.
4. Tenter d'utiliser `.venv.avant-reconstruction` après son déplacement et
   expliquer pourquoi sa réutilisation n'est pas un contrat portable.

## Nettoyage

Supprimer uniquement le dossier de laboratoire après avoir vérifié son chemin
absolu et conservé les résultats demandés. Ne modifier ni Praxis, ni Mnémos
pendant ce cas pratique.
