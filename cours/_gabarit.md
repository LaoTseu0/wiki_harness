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
| Tout | `Où ça s'emboîte` | voir la machine entière, et où cette pièce agit |
| — | `Prérequis et suites` | de quoi ça dépend, ce que ça débloque |
| — | `L'essentiel` | ce que la leçon affirme, et qu'on saura vérifier |
| Parties | `Le savoir` | décomposer, expliquer le mécanisme |
| Parties | `En pratique` · `Mesures` | l'épreuve du réel |
| Tout | `Recomposer` | remettre la pièce, prédire ce qui change ailleurs |

Ne pas confondre les deux premières : `Où ça s'emboîte` situe la pièce dans
un **processus technique** (ce qui se passe à l'exécution) ; `Prérequis et
suites` situe la leçon dans le **parcours** (ce qui se lit avant et après).
Deux axes distincts, deux rubriques distinctes.

**`Recomposer` n'est pas `À retenir`.** Compresser, c'est redire les parties
en plus court ; recomposer, c'est remettre la pièce dans l'ensemble et en
tirer une prédiction sur autre chose. C'est le mouvement le plus difficile,
donc celui qu'on saute — il est obligatoire.

## Les termes techniques sont des liens

À sa **première occurrence utile** dans une leçon, un terme technique devient
un lien. Priorité de la cible :

1. la **leçon** qui traite ce terme, si elle existe (`KV cache` → sa leçon) ;
2. sinon, sa **définition dans `cours/glossaire/`** (`transformers` → le
   glossaire) — créée si elle manque.

Le glossaire ne contient que ce qui n'a pas de leçon : ni étape, ni mesure,
ni promotion, juste de quoi ne pas rester bloqué sur un mot. Le jour où un
terme mérite d'être refait à la main, il quitte le glossaire pour devenir une
leçon, et les liens se retournent vers elle.

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

La leçon ne décrit **pas** son schéma : elle déclare quel processus elle
traverse et quelle étape elle ouvre. Deux lignes, jamais plus.

```markdown
## Où ça s'emboîte

- **Processus** : [d'un texte à un token](../_processus/generation-token.md)
- **L'étape ouverte** : `tokenizer` — entre un texte balisé, sortent des entiers du vocabulaire

![[tokenisation.canvas]]
```

- **Processus** : un lien vers une définition de `cours/_processus/`. Si le
  processus n'existe pas encore, on l'écrit d'abord — jamais en double.
- **L'étape ouverte** : un ou plusieurs identifiants d'étape contigus, entre
  accents graves, séparés par ` · `, puis un tiret cadratin et ce qui entre /
  ce qui sort. Cette clause devient une puce de la boîte allumée.
- **L'incrustation** `![[<stem>.canvas]]` affiche le schéma sous la rubrique.
  Le nom de base suffit — Obsidian le résout où qu'il soit rangé.

Le générateur produit **deux vues**, toutes deux rangées dans
`cours/_schemas/canvas/` :

- le **processus complet**, une fois par définition — la carte de référence,
  incrustée dans le fichier de `cours/_processus/` et nulle part ailleurs ;
- la **vue locale** de chaque leçon — l'étape précédente, celle(s) de la
  leçon (allumées, en vert), l'étape suivante. Les boîtes voisines sont des
  liens : un clic ouvre le canvas de la leçon voisine, et de proche en proche
  on parcourt toute la chaîne.

La boîte verte se suffit à elle-même : son **titre est un lien vers la leçon**
(`[[chemin|libellé de l'étape]]`), son corps une liste à puces — le rôle de
l'étape, puis la clause « ce qui entre / ce qui sort ». Rien d'autre autour :
ni encadré annexe, ni renvoi vers le processus complet, qu'on rejoint par la
prose. Le générateur produit tout cela ; on ne dessine rien à la main.

```bash
python outils/canvas.py            # régénère tout
python outils/canvas.py --verifier # échoue si un canvas est périmé
```

Trois règles non négociables :

1. **Une définition, N rendus.** Le processus est décrit une seule fois dans
   `cours/_processus/` ; les leçons n'en redonnent jamais leur version. Une
   mécanique fausse se corrige à un seul endroit.
2. **La même machine, une boîte qui bouge.** Une leçon qui ouvre une seule
   étape la place toujours aux mêmes coordonnées, entre les mêmes voisines :
   d'une leçon à l'autre, seul le contenu de la boîte allumée change. C'est
   ce qui donne la vision de l'imbrication. Au-delà de deux étapes ouvertes,
   la rangée devient une colonne — la leçon se lit alors de haut en bas, ses
   voisines restant accrochées à gauche de la première et à droite de la
   dernière.
3. **La prose est la source, le canvas est le rendu.** Ne jamais éditer un
   `.canvas` à la main : il sera écrasé.

Une leçon sans processus technique — `LoRA`, `quatre régimes`, tout le
gabarit B en général — n'a simplement pas de schéma, et c'est normal.

---

## Gabarit A — leçon « refaire »

```markdown
# Titre

> [carte du cours](../carte.md) · étape : [`NN_sujet.py`](../../etapes/domaine/NN_sujet.py)

## Où ça s'emboîte

Les deux lignes décrites plus haut : le processus, l'étape ouverte.

## Prérequis et suites

- **Suppose acquis** : les notions nécessaires, chacune avec le lien vers
  la leçon qui l'enseigne. Si une notion n'est enseignée nulle part, elle
  se pose ici en trois lignes, ou elle devient une leçon à part entière.
- **Débloque** : ce que cette leçon rend possible ensuite.

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

Rubrique **omise** la plupart du temps : une leçon « situer » ne porte
généralement pas sur une étape d'un processus technique. Si elle en couvre
une malgré tout, mêmes deux lignes que le gabarit A.

## Prérequis et suites

Identique au gabarit A.

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
| 2 | `Où ça s'emboîte` désigne-t-il un processus existant et une étape réelle, sans redécrire la chaîne ? |
| 3 | Le schéma `.canvas` se génère-t-il sans erreur, et `--verifier` passe-t-il ? |
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
