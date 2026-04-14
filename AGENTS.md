# Conventions du langage ! Important !

**Interdiction suprême de faire ça** : "forme la phrase en anglais, puis je la rhabille en français. Les mots deviennent français, la charpente reste anglaise — structure, images, collocations. Un lecteur natif entend l'anglais en dessous."
**Interdiction suprême de faire ça** : utilisation de faux-amis, l'interdiction du calque.
Tous les termes techniques anglicisés peuvent rester en anglais pour la bonne compréhension du jargon !

**Le test du francophone natif est ABSOLUMENT IMPÉRATIF !!** 

- **Le test du francophone natif prime** — règle suprême d'AGENTS.md : aucun calque de l'anglais, aucun faux-ami. Le jargon technique anglais, lui, reste en anglais. 
	- liste acceptée en plus des termes communs : 
	  - Template
	  - Frontmatter — le bloc de métadonnées en tête de note, jamais « en-tête » ni « en-tête YAML »
	  - Input / Output — dans les signatures de pièces ou d'étapes, jamais « entrée / sortie » ni « entrent X, sort Y »


- **Registre écrit, précis.** Pas de béquilles de l'oral (« du coup », « en gros », « un peu »), pas d'emphase commerciale (« puissant », « incontournable »).
- **Une phrase, une idée.** Phrases courtes par défaut. Un paragraphe défend une seule affirmation.
- **Toute propriété affirmée porte sa cause.** Interdit : l'adjectif-verdict seul (« instable », « coûteux »). On donne le mécanisme qui le produit, ou on se tait.
- **Nommer la pièce, pas « le système ».** Si la phrase reste vraie en remplaçant le nom par « le système », elle n'explique rien.
- **Le concret avant l'abstrait.** L'exemple porte la règle ; la règle ne flotte pas seule.
- **Pas d'auto-référence.** Ni « dans cette leçon nous allons voir », ni statut, ni date, ni note sur sa propre rédaction dans le corps.

# Conventions du repo

Cours + mises en pratique pour comprendre chaque couche d'une application LLM
et en construire un framework maison maîtrisé de bout en bout.
/raw : contient des informations glanées lors de mes recherches pour ajouter de la qualité aux cours. 
Point d'entrée : [Wiki/cartographie.md](Wiki/cartographie.md).

# Hiérarchie des sources de vérité

AGENTS.md (+ REGLES.md, importé ci-dessous) -> cartographie.md

`REGLES.md` fusionne l'ancien cadrage (ce qu'on construit) et l'ancien gabarit
de leçon (sous quelle forme elle rentre). Il est chargé avec ce fichier :

@Wiki/REGLES.md

## Organisation

Tout le contenu vit sous `Wiki/` — la racine du repo ne garde que la
configuration (`AGENTS.md`, `.obsidian/`) et `raw/`.

| Dossier                   | Rôle                                                                                |
| ------------------------- | ----------------------------------------------------------------------------------- |
| `Wiki/parcours/`          | la connaissance, un dossier par domaine. L'ensemble structuré par couche logicielle. |
| `Wiki/cas-pratique/`      | Exercice en .py ou .ipynb                                                           |
| `Praxis/`                 | le framework maison Praxis — s'enrichit à la fin de chaque Parcours            |
| `Mnemos/`                 | Mnémos, l'assistant personnel, finalité ultime du projet                        |
| `Wiki/glossaire/`         | définitions courtes des termes qui n'ont pas de leçon                               |
| `wiki/_schemas/canvas/`   | schémas `.canvas` générés — jamais édités à la main                                 |
| raw                       | Information brute à fusionner dans les cours uniquement sur demande et validation !  |
| `outils/`                 | l'outillage du repo lui-même (génération des schémas, contrôles)                    |

## Règles

- **Un concept, un seul endroit.** Pas de dossier transverse qui rejoue un
  deuxième axe de rangement.
- **Aucun concept boîte noir**. On veut une maitrise total de l'outil. Si un concept est très pertinent mais complexe il doit avoir ça place dans le référentiel "Cartographie"

## Gabarit d'une leçon

La spécification vit dans la partie II de [REGLES.md](Wiki/REGLES.md), chargé avec ce fichier.

## Contrôles

Ce qui doit rester vrai de `Wiki/parcours/` se vérifie en une commande — liens
morts, fichiers orphelins, numérotation héritée,
vocabulaire proscrit, chiffres hors rubrique `Mesures`, rubriques vides ou
manquantes :

```bash
python outils/conformite.py
```

`--detail` liste chaque occurrence. Le script constate, il ne trie pas :
un chiffre signalé peut être un fait matériel ou un calcul redéductible,
que le gabarit autorise. C'est à la relecture de trancher.


## Git

Interdiction de mettre des références de co-autheur anthropic ou autre.
exemple: Co-authored-by: Claude <noreply@anthropic.com>
Interdit.
## Code

- Praxis et Mnémos disposent chacun de leur propre runtime Python, de leur
  environnement virtuel et de leurs dépendances. Aucun environnement Python ne
  vit à la racine du dépôt.
- Commentaires **en français sans accents** dans les `.py` (encodage console
  Windows). Docstring pédagogique en tête de chaque étape.
- Les étapes d'un même domaine s'importent directement — pas de
  `sys.path.insert`, l'arborescence est plate exprès.
