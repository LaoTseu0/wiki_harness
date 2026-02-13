# Gabarit d'une leçon

Spécification de rédaction. Toute leçon de `cours/` s'y conforme, qu'elle
soit écrite à la main ou générée. Ce fichier n'est pas une leçon : il ne
se lit pas dans le parcours.

## La forme d'ensemble

Une leçon va du **tout** aux **parties**, puis revient au **tout**. Ce n'est
pas un principe importé : c'est la forme du repo lui-même — le framework
maison est le tout, les leçons sont les parties, la promotion dans
`src/framework/` est le retour au tout.

| Phase | Rubrique | Opération mentale |
|---|---|---|
| Tout | `Où ça s'emboîte` | localiser la pièce parmi ses voisines |
| — | `L'essentiel` | ce que la leçon affirme, et qu'on saura vérifier |
| Parties | `Le savoir` | décomposer, expliquer le mécanisme |
| Parties | `En pratique` · `Mesures` | l'épreuve du réel |
| Tout | `Recomposer` | remettre la pièce, prédire ce qui change ailleurs |

**`Recomposer` n'est pas `À retenir`.** Compresser, c'est redire les parties
en plus court ; recomposer, c'est remettre la pièce dans l'ensemble et en
tirer une prédiction sur autre chose. C'est le mouvement le plus difficile,
donc celui qu'on saute — il est obligatoire.

## Choisir le gabarit

Deux niveaux de maîtrise, deux squelettes. Le choix se déclare et ne se
devine pas.

| Niveau | Critère | Gabarit |
|---|---|---|
| **Refaire** | on doit savoir le réimplémenter et prédire son comportement | A |
| **Situer** | on doit savoir l'expliquer, le reconnaître et décider quand l'employer | B |

Une leçon **Situer** peut être promue en **Refaire** plus tard ; l'inverse
n'arrive pas. Dans le doute, prendre A : le coût d'une étape en trop est
plus faible que celui d'une boîte noire.

---

## Les trois interdits

Ils priment sur tout le reste. Un LLM qui rédige une leçon ne peut pas les
respecter par bonne volonté : ils se vérifient après coup.

1. **Ne jamais inventer une mesure.** Aucun chiffre de performance,
   latence, taille, score ou durée ne s'écrit sans avoir été produit ici.
2. **Ne jamais inventer un vécu.** Un incident, une panne, une erreur de
   parcours ne se rédigent que s'ils ont eu lieu. Pas d'anecdote
   plausible, pas de « on observe souvent que ».
3. **Ne jamais livrer la solution d'un exercice non fait.** Le code de
   `etapes/` est un squelette à trous avec un protocole.

Marqueur des emplacements à ne pas combler :

```markdown
<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->
```

---

## `Où ça s'emboîte` — la rubrique qui se dessine

Quatre lignes, jamais plus, toujours dans cet ordre. C'est la **source** du
schéma `.canvas` voisin, régénéré par `outils/canvas.py` — donc sa forme est
contrainte.

```markdown
## Où ça s'emboîte

- **En amont** : [tokenisation](tokenisation.md) — le texte est déjà découpé en tokens
- **La pièce** : transforme la liste de messages en le texte unique que le modèle lit
- **En aval** : [function calling](function-calling.md) — le rôle `tool` n'est qu'une balise de plus
- **À ne pas confondre avec** : le prompt système, qui est un *contenu*, pas un *format*
```

- **En amont / En aval** : un lien par voisin, suivi d'un tiret cadratin et
  de la relation en une clause — cette clause devient l'étiquette de la
  flèche. Plusieurs voisins possibles, séparés par ` · `.
- **La pièce** : ce que fait cet élément, sans lien, une ligne.
- **À ne pas confondre avec** : l'axe de discrimination. Un concept se
  définit autant par ce dont on le distingue que par ce qu'il est.

Trois règles non négociables :

1. **Rayon 1.** Voisins immédiats seulement. Sans cette borne, chaque schéma
   rampe vers une carte globale et diverge de `carte.md`.
2. **La prose est la source, le canvas est le rendu.** Le `.md` se lit seul ;
   le `.canvas` se régénère. Jamais l'inverse.
3. **Aucune analogie.** La réponse nomme des voisins réels du cours. Si on ne
   peut pas la dessiner, c'est que l'ouverture est vague — le schéma échoue
   avant le lecteur, et c'est le but.

---

## Gabarit A — leçon « refaire »

```markdown
# Titre

> [carte du cours](../carte.md) · étape : [`NN_sujet.py`](../../etapes/domaine/NN_sujet.py)

## Où ça s'emboîte

Les quatre lignes décrites plus haut.

## L'essentiel

Une thèse qu'on pourrait contredire, pas un résumé d'ambiance : ce que
cette leçon affirme et qu'on saura vérifier. Se termine par la borne —
ce que la leçon ne traite pas, et où ça se trouve.

## Le savoir

Le corps. Une idée par unité de texte. Règle non négociable : **toute
propriété affirmée est accompagnée de la cause qui permet de la
redéduire**. Interdiction de l'adjectif-verdict seul (« adaptatif »,
« instable », « coûteux ») — il faut le mécanisme derrière.

Un schéma quand l'obstacle est un ordre ou une relation entre étapes ;
pas quand c'est une définition.

## En pratique

Le protocole de l'étape, puis — avant de lancer — **ce qu'il faut
prédire**. Des questions dont la réponse sera confirmée ou démentie par
l'exécution : c'est l'écart entre la prédiction et le réel qui apprend.

## Mesures

<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->

Les chiffres obtenus, le matériel et le modèle sur lesquels ils l'ont été,
et ce qui a démenti la prédiction.

## Recomposer

La pièce remise dans l'ensemble. Deux questions, pas une de plus :

- qu'est-ce que ça **change à ce qu'on croyait déjà savoir** ? (les notions
  déjà vues qui prennent un autre sens)
- qu'est-ce qu'on peut désormais **prédire ailleurs**, dans une leçon qu'on
  n'a pas encore faite ?

Ni résumé, ni transition. Si le paragraphe pourrait être remplacé par
« en résumé », il est à réécrire.

## Pièges connus

- **Rencontrés** : ce qui a réellement mordu ici. Raconté en entier —
  symptôme, hypothèse, test discriminant, cause.
- **Anticipés** : ce qui devrait mordre, non vérifié à ce jour. Jamais
  mélangé avec les précédents.

## Se tester

Trois questions maximum, qu'on peut **rater**. Chacune vient avec son
critère de réussite : à quoi reconnaît-on une réponse juste.

## Ce que ça change dans le framework

La brique promue dans `src/framework/`, ou la phrase qui dit que cette
leçon ne produit rien de réutilisable — et pourquoi. Rubrique obligatoire :
c'est le cas le plus concret de `Recomposer`, la pièce remise dans le tout
littéral.

## À retenir

Une phrase par bloc du « savoir ». Compact, autoportant, relisible seul
avant de reprendre l'étape.

## Références

Chaque lien avec ce qu'on va y chercher.
```

---

## Gabarit B — leçon « situer »

Pas d'étape, donc pas de mesure ni de promotion. Les deux phases
holistiques changent de nature : le tout n'est pas une chaîne qui tourne
mais un **paysage**, et la recomposition est un **critère de décision**.

```markdown
# Titre

> [carte du cours](../carte.md)

## Où ça s'emboîte

Mêmes quatre lignes. Ici « en amont / en aval » se lisent comme
« ce qui amène à en parler / ce que ça permet de comprendre ».

## L'essentiel

La thèse, et la borne.

## Le savoir

Identique au gabarit A — mécanisme avant conclusion, une idée par unité.
Le schéma y compte davantage : sans exécution, c'est le seul support de
vérification.

## Quand c'est la bonne réponse

La recomposition de cette famille de leçons : à quelles conditions on
emploie ça, à quelles conditions on ne l'emploie pas, et par quoi on le
remplace alors. C'est la vraie valeur d'une leçon « situer ».

## Ce qu'on ne saura pas faire

La limite assumée : ce que la leçon permet de dire, et ce qu'elle ne permet
pas de construire. Dit aussi ce qui la promouvrait en leçon « refaire ».

## Se tester

Identique au gabarit A : des questions qu'on peut rater, avec critère.

## À retenir

Identique au gabarit A.

## Références

Identique au gabarit A.
```

---

## Vérification avant de valider une leçon

Chaque ligne se répond par oui ou non. Un seul non = la leçon repasse.

| # | Contrôle |
|---|---|
| 1 | Le niveau visé (refaire / situer) est-il déclaré et le bon gabarit employé ? |
| 2 | `Où ça s'emboîte` tient-il en quatre lignes, à rayon 1, sans aucune analogie ? |
| 3 | Le schéma `.canvas` se génère-t-il sans erreur depuis ces quatre lignes ? |
| 4 | Chaque notion supposée connue est-elle liée à la leçon qui l'enseigne, ou posée sur place ? |
| 5 | Toute propriété affirmée s'accompagne-t-elle de son mécanisme ? |
| 6 | Un lecteur pourrait-il prédire le comportement dans un cas non traité ? |
| 7 | La borne est-elle explicite — ce que la leçon ne couvre pas et où ça se trouve ? |
| 8 | Y a-t-il un seul concept, ou la leçon en empile-t-elle plusieurs ? |
| 9 | Aucun paragraphe n'empile-t-il plus d'une idée dense ? |
| 10 | `Recomposer` produit-il une prédiction sur autre chose, plutôt qu'un résumé ? |
| 11 | Tout chiffre présent a-t-il été produit ici, avec son contexte matériel ? |
| 12 | Les emplacements de mesure non exécutés sont-ils vides et marqués ? |
| 13 | Les pièges rencontrés sont-ils séparés des pièges anticipés ? |
| 14 | Les incidents sont-ils racontés en entier, ou seulement cités ? |
| 15 | Les questions de « se tester » peuvent-elles être ratées, et le critère est-il donné ? |
| 16 | La leçon dit-elle ce qu'elle produit dans le framework, ou pourquoi rien ? |
| 17 | Une correction ponctuelle est-elle convertie en réflexe transférable ? |
| 18 | Le ton distingue-t-il le savoir de manuel du vécu du parcours ? |
| 19 | Le vocabulaire est-il exempt d'entretien, recruteur, offres, portfolio, CV ? |
| 20 | La leçon est-elle exempte de statut, de case à cocher et de date de mise à jour ? |

## Note sur la génération

Les contrôles 11 à 14 et 18 ne sont pas satisfiables par un modèle : ils
portent sur ce qui a été vécu et mesuré, qu'il ne peut que fabriquer de
façon plausible. Une leçon générée est donc **complète sur le savoir et
volontairement trouée sur le réel** — les trous se comblent à l'exécution,
par la personne qui l'a faite.
