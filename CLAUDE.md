# Conventions du repo

Cours + mises en pratique pour comprendre chaque couche d'une application LLM
et en construire un framework maison maîtrisé de bout en bout.
Point d'entrée : [cours/carte.md](cours/carte.md).

## Organisation

| Dossier | Rôle |
|---|---|
| `cours/` | la prose, un dossier par domaine. Aucun numéro dans les chemins. |
| `etapes/` | les scripts exécutables, numérotés par domaine (`NN_sujet.py`) |
| `src/framework/` | le framework maison — s'enrichit à chaque leçon acquise |
| `tests/` | pytest sur `src/framework/` |
| `cours/_archive/` | écrit avant d'être vécu, ou journal historique. Ne pas s'y fier. |

## Règles

- **Pas de suivi d'avancement.** Ni statuts, ni cases à cocher, ni dates de
  mise à jour, ni fichier de progression. L'état se lit dans le réel : ce qui
  est dans `src/framework/` a été compris et promu, ce qui est dans `etapes/`
  a tourné. Git porte l'historique.
- **Ne jamais écrire d'avance la solution d'une leçon non faite.** Un énoncé,
  un squelette à trous, oui. Du code complet livré clé en main, non — c'est
  ce qui a rendu l'ancien repo inutilisable pour apprendre.
- **Le cours n'est pas un CV.** Pas de « question d'entretien », pas de
  vocabulaire d'offres d'emploi, pas de framing portfolio. Le critère de
  validation est : *sais-tu le réimplémenter et prédire son comportement ?*
- **Mesurer** : toute affirmation de performance s'appuie sur un chiffre
  produit ici, jamais sur un souvenir de doc.
- **Un concept, un seul endroit.** Pas de dossier transverse qui rejoue un
  deuxième axe de rangement : une notion se range dans le domaine qui
  l'utilise. Quand un concept mérite d'être séparé de son application (la
  théorie du re-ranking vs son branchement), ce sont deux fichiers voisins,
  pas deux dossiers.
- **Si tu ne sais pas le refaire en ~50 lignes, il te faut une étape.** Un
  concept qu'un framework cache et qu'on ne saurait pas réimplémenter reste
  une boîte noire tant qu'il n'a pas son script exécutable dans `etapes/`.

## Gabarit d'une leçon

```markdown
# Titre

> [carte du cours](../carte.md) · étape : [`NN_sujet.py`](../../etapes/domaine/NN_sujet.py)

## L'essentiel
## Le savoir
## En pratique
## Pièges connus
## Se tester
## Références
```

Rubrique optionnelle quand la leçon promeut du code :
`## Ce que ça change dans le framework`.

## Code

- Python 3.12 via `mise` ; un seul venv à la racine, dépendances dans
  `requirements.txt`.
- Commentaires **en français sans accents** dans les `.py` (encodage console
  Windows). Docstring pédagogique en tête de chaque étape.
- Les étapes d'un même domaine s'importent directement — pas de
  `sys.path.insert`, l'arborescence est plate exprès.
- Le corpus RAG vient du repo `homelab`, supposé installé en frère
  (`../homelab`).
