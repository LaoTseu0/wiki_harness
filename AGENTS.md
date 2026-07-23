# Conventions du repo

Cours + mises en pratique pour comprendre chaque couche d'une application LLM
et en construire un framework maison maîtrisé de bout en bout.
/raw : contiens des informations glané lors de mes recherches pour ajouté de la qualité aux cours. 
Point d'entrée : [wiki/cours/carte.md](wiki/cours/carte.md).

## Organisation

Tout le contenu vit sous `wiki/` — la racine du repo ne garde que la
configuration (`AGENTS.md`, `pyproject.toml`, `.obsidian/`) et `raw/`.

| Dossier | Rôle |
|---|---|
| `wiki/cours/` | la prose, un dossier par domaine. Aucun numéro dans les chemins. |
| `wiki/etapes/` | les scripts exécutables, numérotés par domaine (`NN_sujet.py`) |
| `wiki/src/framework/` | le framework maison — s'enrichit à chaque leçon acquise |
| `wiki/cours/framework/` | la colonne vertébrale : les briques transverses et ce qui les fait tenir |
| `wiki/cours/agent/` | le harnais — ce qui sépare une boucle `while` d'un agent tenable |
| `wiki/cours/glossaire/` | définitions courtes des termes qui n'ont pas de leçon |
| `wiki/cours/_schemas/canvas/` | schémas `.canvas` générés — jamais édités à la main |
| `wiki/tests/` | pytest sur `wiki/src/framework/` |
| `wiki/outils/` | l'outillage du repo lui-même (génération des schémas, contrôles) |
| `wiki/cours/_archive/` | écrit avant d'être vécu, ou journal historique. Ne pas s'y fier. |

## Règles

- **Mesurer** : toute affirmation de performance s'appuie sur un chiffre
  produit ici, jamais sur un souvenir de doc.
- **Un concept, un seul endroit.** Pas de dossier transverse qui rejoue un
  deuxième axe de rangement : une notion se range dans le domaine qui
  l'utilise. Quand un concept mérite d'être séparé de son application (la
  théorie du re-ranking vs son branchement), ce sont deux fichiers voisins,
  pas deux dossiers. Une notion qu'aucun domaine ne possède seul — evals,
  providers, service — appartient à `wiki/cours/framework/`, pas au domaine qui
  l'a croisée en premier.
- **Un domaine, une tête.** L'entrée d'un domaine est une leçon-chapeau,
  jamais un `index.md` qui rejoue la carte. La table des matières du cours
  est [wiki/cours/carte.md](wiki/cours/carte.md), et elle est unique.
- **Si tu ne sais pas le refaire en ~50 lignes, il te faut une étape.** Un
  concept qu'un framework cache et qu'on ne saurait pas réimplémenter reste
  une boîte noire tant qu'il n'a pas son script exécutable dans `wiki/etapes/`.

## Gabarit d'une leçon

La spécification complète est dans [wiki/cours/_gabarit.md](wiki/cours/_gabarit.md) :
deux squelettes selon le niveau visé (*refaire* ou *situer*), et la liste
de contrôle à passer avant de valider une leçon. À lire avant d'en écrire
ou d'en réécrire une.

Ses trois interdits, qui priment sur le reste :

1. **Ne jamais inventer une mesure** — les emplacements prévus restent
   vides et marqués `<!-- À MESURER -->` tant que l'étape n'a pas tourné.
2. **Ne jamais inventer un vécu** — pas d'incident plausible, pas de « on
   observe souvent que ».
3. **Ne jamais livrer la solution d'un exercice non fait.**

Une leçon va du tout aux parties puis revient au tout : `Où ça s'emboîte`
(la machine, et l'étape que la leçon ouvre) → `Le savoir` → `Recomposer`
(ce que ça change ailleurs, jamais un résumé).

Un terme technique devient un lien à sa première occurrence : vers la leçon
qui le traite, ou à défaut vers `wiki/cours/glossaire/` (définition créée si
absente). Le glossaire ne contient que ce qui n'a pas de leçon.

Les processus techniques sont décrits **une seule fois** dans
`wiki/cours/_processus/` ; une leçon déclare lequel elle traverse et quelle étape
elle ouvre, et incruste son schéma par `![[<stem>.canvas]]`. Le générateur
produit une vue locale navigable (précédent / leçon / suivant) plus le
processus complet, tous dans `wiki/cours/_schemas/canvas/`. Ne jamais éditer un
`.canvas` à la main :

```bash
python wiki/outils/canvas.py
```

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
- Le corpus RAG vient du repo `homelab`, supposé installé en frère
  (`../homelab`).
