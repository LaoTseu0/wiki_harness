# Conventions du langage ! Important !

**Interdiction suprême de faire ça** : "forme la phrase en anglais, puis je la rhabille en français. Les mots deviennent français, la charpente reste anglaise — structure, images, collocations. Un lecteur natif entend l'anglais en dessous."

**Interdiction suprême de faire ça** : utilisation de faux-amis, l'interdiction du calque.

**le test du francophone natif est ABSOLUMENT IMPERATIF !!** 

# Conventions du repo

Cours + mises en pratique pour comprendre chaque couche d'une application LLM
et en construire un framework maison maîtrisé de bout en bout.
/raw : contiens des informations glané lors de mes recherches pour ajouté de la qualité aux cours. 
Point d'entrée : [wiki/cours/carte.md](wiki/cours/carte.md).

## Organisation

Tout le contenu vit sous `wiki/` — la racine du repo ne garde que la
configuration (`AGENTS.md`, `pyproject.toml`, `.obsidian/`) et `raw/`.

| Dossier                 | Rôle                                                                                |
| ----------------------- | ----------------------------------------------------------------------------------- |
| `wiki-v2/parcours/`     | la connaissance, un dossier par domaine. L'ensemble structurer par couche logiciel. |
| `wiki-v2/cas-pratique/` | Exercice en .py ou .ipynb                                                           |
| `Hosef`                 | le framework maison "Hosef" — s'enrichit à chaque la fin de chaque Parcours         |
| `Harnais`               | le harnais , finalité ultime, complète et entièrement maitrisé                      |
| `wiki-v2/glossaire/`    | définitions courtes des termes qui n'ont pas de leçon                               |
| `wiki/_schemas/canvas/` | schémas `.canvas` générés — jamais édités à la main                                 |
| raw                     | Information brut à fusionner dans les cours uniquement sur demande et validation !  |
| `outils/`               | l'outillage du repo lui-même (génération des schémas, contrôles)                    |
| `wiki/cours/_archive/`  | écrit avant d'être vécu, ou journal historique. Ne pas s'y fier.                    |

## Règles

- **Mesurer** : toute affirmation de performance s'appuie sur un chiffre
  produit ici, jamais sur un souvenir de doc.
- **Un concept, un seul endroit.** Pas de dossier transverse qui rejoue un
  deuxième axe de rangement .
- **Si tu ne sais pas le refaire en ~50 lignes, il te faut une étape.** Un
  concept qu'un framework cache et qu'on ne saurait pas réimplémenter reste
  une boîte noire tant qu'il n'a pas son script exécutable dans `wiki/etapes/`.

## Gabarit d'une leçon

La spécification complète est dans [wiki/cours/_gabarit.md](wiki/cours/_gabarit.md) 

## Contrôles

Ce qui doit rester vrai de `wiki/cours/` se vérifie en une commande — liens
morts, fichiers orphelins, renvois vers `_archive/`, numérotation héritée,
vocabulaire proscrit, chiffres hors rubrique `Mesures`, rubriques vides ou
manquantes :

```bash
python wiki/outils/controles.py
```

`--detail` liste chaque occurrence. Le script constate, il ne trie pas :
un chiffre signalé peut être un fait matériel ou un calcul redéductible,
que le gabarit autorise. C'est à la relecture de trancher.

## Code

- Python 3.12 via `mise` ; un seul venv à la racine, dépendances dans
  `requirements.txt`.
- Commentaires **en français sans accents** dans les `.py` (encodage console
  Windows). Docstring pédagogique en tête de chaque étape.
- Les étapes d'un même domaine s'importent directement — pas de
  `sys.path.insert`, l'arborescence est plate exprès.

