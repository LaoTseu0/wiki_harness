# Doctrine visuelle

Le cours suit une approche **holistique → analytique → holistique** :

1. voir l'ensemble complet ;
2. ouvrir une étape ou un élément et comprendre son mécanisme ;
3. replacer cette pièce dans l'ensemble et suivre ses relations.

Le texte et le schéma portent deux fonctions différentes. Le texte explique les
causes, les garanties et les limites. Le schéma conserve les positions, les
frontières et les relations. Aucun des deux ne remplace l'autre.

### Un processus

Un processus est une suite ordonnée de transformations qui possède un Input
global, un Output global et des étapes reliées par un flux de données ou de
contrôle.

Une architecture statique, une taxonomie ou une carte de concepts n'est pas
appelée « processus ». Elle peut recevoir un autre schéma, mais ne donne pas une
fausse étape précédente et une fausse étape suivante à une leçon.

Chaque processus est décrit une seule fois dans `generator/guardrails/schema/processus/`. Son fichier
`.canvas` complet constitue la source de vérité visuelle. Le registre
`generator/guardrails/schema/processus/index.md` fixe son identifiant, son nom, son Input, son Output
et son statut.

### Un sous-processus

Une étape trop dense peut ouvrir un autre Canvas canonique. L'Input et l'Output
du sous-processus raffinent alors l'Input et l'Output locaux de l'étape parente
sans les contredire.

Le nœud parent lie le sous-processus. Une leçon référence le niveau le plus
précis qui contient son mécanisme ; le processus parent reste la vue
holistique de recomposition.

### Un schéma non séquentiel

Une connaissance sans ordre temporel reçoit un schéma non séquentiel plutôt
qu'un faux processus. Sa source canonique vit dans
`generator/guardrails/schema/references/`. Le registre `generator/guardrails/schema/index.md` fixe son
identifiant, son type, sa portée et son statut.

Cinq types sont admis :

- **architecture** — les groupes représentent l'appartenance ou une frontière ;
  chaque arête nomme une dépendance, un appel, une lecture ou une production ;
- **carte de concepts** — chaque arête verbalise la relation entre deux notions ;
  la distance visuelle ne porte aucun sens non documenté ;
- **arbre de décision** — un nœud préfixé `DÉCISION` pose une question, chaque
  arête porte une condition et chaque feuille nomme l'issue ;
- **cycle de vie** — un nœud préfixé `ÉTAT` représente une situation stable et
  une arête nomme l'action ou l'événement qui provoque la transition ;
- **carte de responsabilités** — chaque nœud nomme un propriétaire, une donnée
  ou un contrat ; chaque arête qualifie la responsabilité échangée.

Une forme n'est jamais interprétée par ressemblance. Son sens vient de son type,
de son libellé et de la convention déclarée dans le registre.

### JSON Canvas

Les schémas utilisent JSON Canvas 1.0 et l'extension `.canvas`.

Un processus complet respecte ces conventions :

- les identifiants de nœuds et d'arêtes sont uniques et stables ;
- l'identifiant d'une étape est un slug lisible, réutilisé par le Frontmatter
  des leçons ;
- une vue destinée à une leçon place les nœuds présentés dans un `group` ;
  le `label` du `group` reprend le nom du mécanisme étudié ;
- le flux principal se lit de gauche à droite ;
- une boucle de retour passe sous le flux principal ;
- une arête porte un libellé lorsque sa donnée ou sa condition n'est pas
  évidente ;
- un nœud contient un intitulé court ; le détail appartient à la leçon ;
- un nœud d'annotation commence par `note:` et ne fait pas partie du flux
  structurel ;
- la couleur ne porte jamais seule une information.

La palette des vues de leçon est stable :

- étape ouverte : violet, avec le préfixe `ÉTAPE OUVERTE` ;
- étape précédente : cyan, avec le préfixe `AMONT` ;
- étape suivante : vert, avec le préfixe `AVAL` ;
- autres étapes : style neutre.

Pour un schéma non séquentiel :

- élément ouvert : violet, avec le préfixe `ÉLÉMENT OUVERT` ;
- élément directement relié : cyan, avec le préfixe `RELATION DIRECTE` ;
- autres éléments : style neutre.

La couleur ne crée ni ordre ni causalité dans un schéma non séquentiel.

### Vue contextualisée d'une leçon

Une leçon liée à un processus déclare `processus` et `etape` dans son
Frontmatter. Une leçon liée à un schéma non séquentiel déclare `schema` et
`element`. Dans ce second cas, `processus` porte `aucun — <raison>` et `etape`
est absent.

L'outillage dérive la vue depuis le Canvas canonique et retire ses annotations
secondaires. Pour un processus, il conserve l'étape ouverte, son amont et son
aval. Pour un autre schéma, il conserve l'élément ouvert et ses relations
directes. Les nœuds conservés sont placés dans un `group` nommé d’après le
mécanisme de la leçon.

La vue produite vit dans `generator/guardrails/schema/canvas/<id-de-leçon>.canvas`. Elle est
générée et ne se modifie jamais à la main. Une correction du flux se fait dans
le Canvas complet du processus, puis toutes les vues concernées sont
régénérées.

Chaque leçon possède un repère visuel : processus ou schéma non séquentiel. Elle
ne reçoit jamais un faux diagramme de flux pour satisfaire cette obligation.
