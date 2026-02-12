# Gabarit d'une leçon

Spécification de rédaction. Toute leçon de `cours/` s'y conforme, qu'elle
soit écrite à la main ou générée. Ce fichier n'est pas une leçon : il ne
s'indexe pas, il ne se lit pas dans le parcours.

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
respecter par bonne volonté : ils doivent être vérifiés après coup.

1. **Ne jamais inventer une mesure.** Aucun chiffre de performance,
   latence, taille, score ou durée ne s'écrit sans avoir été produit ici.
   Les emplacements prévus restent vides et marqués.
2. **Ne jamais inventer un vécu.** Un incident, une panne, une erreur de
   parcours ne se rédigent que s'ils ont eu lieu. Pas d'anecdote
   plausible, pas de « on observe souvent que ».
3. **Ne jamais livrer la solution d'un exercice non fait.** Le code de
   `etapes/` est un squelette à trous avec un protocole, jamais une
   implémentation complète.

Marqueur unique pour les emplacements à ne pas combler :

```markdown
<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->
```

---

## Gabarit A — leçon « refaire »

```markdown
# Titre

> [carte du cours](../carte.md) · étape : [`NN_sujet.py`](../../etapes/domaine/NN_sujet.py)

## L'essentiel

Une thèse qu'on pourrait contredire, pas un résumé d'ambiance : ce que
cette leçon affirme et qu'on saura vérifier. Se termine par la borne —
ce que la leçon ne traite pas, et où ça se trouve.

## Prérequis et suites

- **Suppose acquis** : les notions nécessaires, chacune avec le lien vers
  la leçon qui l'enseigne. Si une notion n'est enseignée nulle part, elle
  se pose ici, en trois lignes, ou elle devient une leçon à part entière.
- **Débloque** : ce que cette leçon rend possible ensuite.

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

Une fois l'étape lancée : les chiffres obtenus, le matériel et le modèle
sur lesquels ils l'ont été, et ce qui a démenti la prédiction.

## Pièges connus

- **Rencontrés** : ce qui a réellement mordu ici. Raconté en entier —
  symptôme, hypothèse, test discriminant, cause. Un incident est du
  contenu, pas une note de bas de page.
- **Anticipés** : ce qui devrait mordre, non vérifié à ce jour. Jamais
  mélangé avec les précédents.

## Se tester

Trois questions maximum, qu'on peut **rater**. Chacune vient avec son
critère de réussite : à quoi reconnaît-on une réponse juste. Une question
sans critère ne discrimine rien.

## Ce que ça change dans le framework

La brique promue dans `src/framework/`, ou la phrase qui dit que cette
leçon ne produit rien de réutilisable — et pourquoi. Rubrique obligatoire :
c'est elle qui empêche le framework de rester un chapitre final.

## À retenir

Une phrase par bloc du « savoir ». Compact, autoportant, relisible seul
avant de reprendre l'étape.

## Références

Chaque lien avec ce qu'on va y chercher. Une liste sans intention est une
liste morte.
```

---

## Gabarit B — leçon « situer »

Pas d'étape, donc pas de mesure ni de promotion. En contrepartie, la
leçon doit assumer sa limite et fournir un critère de décision — sinon
elle n'est qu'une définition allongée.

```markdown
# Titre

> [carte du cours](../carte.md)

## L'essentiel

La thèse, et la borne : ce que la leçon ne traite pas.

## Prérequis et suites

Identique au gabarit A.

## Le savoir

Identique au gabarit A — mécanisme avant conclusion, une idée par unité.
Le schéma y est plus important encore : sans exécution, c'est le seul
support de vérification.

## Quand c'est la bonne réponse

Le critère de décision : à quelles conditions on emploie ça, à quelles
conditions on ne l'emploie pas, et par quoi on le remplace alors. C'est
la vraie valeur d'une leçon « situer ».

## Ce qu'on ne saura pas faire

La limite assumée, en une ou deux phrases : ce que cette leçon permet de
dire, et ce qu'elle ne permet pas de construire. Dit aussi ce qui la
promouvrait en leçon « refaire ».

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
| 2 | Chaque notion supposée connue est-elle liée à la leçon qui l'enseigne, ou posée sur place ? |
| 3 | Toute propriété affirmée s'accompagne-t-elle de son mécanisme ? |
| 4 | Un lecteur pourrait-il prédire le comportement dans un cas non traité ? |
| 5 | La borne est-elle explicite — ce que la leçon ne couvre pas et où ça se trouve ? |
| 6 | Y a-t-il un seul concept, ou la leçon en empile-t-elle plusieurs ? |
| 7 | Aucun paragraphe n'empile-t-il plus d'une idée dense ? |
| 8 | Tout chiffre présent a-t-il été produit ici, avec son contexte matériel ? |
| 9 | Les emplacements de mesure non exécutés sont-ils vides et marqués ? |
| 10 | Les pièges rencontrés sont-ils séparés des pièges anticipés ? |
| 11 | Les incidents sont-ils racontés en entier, ou seulement cités ? |
| 12 | Les questions de « se tester » peuvent-elles être ratées, et le critère est-il donné ? |
| 13 | La leçon dit-elle ce qu'elle produit dans le framework, ou pourquoi rien ? |
| 14 | Le schéma, s'il existe, porte-t-il une relation ou un ordre — pas une définition ? |
| 15 | Une correction ponctuelle est-elle convertie en réflexe transférable ? |
| 16 | Le ton distingue-t-il le savoir de manuel du vécu du parcours ? |
| 17 | Le vocabulaire est-il exempt d'entretien, recruteur, offres, portfolio, CV ? |
| 18 | La leçon est-elle exempte de statut, de case à cocher et de date de mise à jour ? |

## Note sur la génération

Les contrôles 8 à 11 et 16 ne sont pas satisfiables par un modèle : ils
portent sur ce qui a été vécu et mesuré, qu'il ne peut que fabriquer de
façon plausible. Une leçon générée est donc **complète sur le savoir et
volontairement trouée sur le réel** — les trous se comblent à l'exécution,
par la personne qui l'a faite.
