# Génération et assemblage d’une leçon

## Unité canonique

Une leçon possède un dossier :

```text
generator/lessons/<parcours>/<id>/
├── contract.json
├── state.json
└── sections/
    ├── 00-introduction.md
    ├── 10-prerequis.md
    ├── 20-savoir-le-situer.md
    └── ...
```

`contract.json` fixe l’identité, le périmètre, le Frontmatter, la destination
et le profil d’assemblage. `state.json` décrit l’avancement sans porter de
connaissance pédagogique. Les fichiers Markdown de `sections/` portent le
contenu canonique.

Le fichier déclaré par `sortie` dans le contrat est dérivé. Toute modification
directe de ce fichier crée un écart que le contrôle doit signaler.

## Contrat de leçon

Un contrat possède au minimum :

- une version de format ;
- un identifiant stable ;
- un titre ;
- un concept central ;
- l’attribution textuelle issue de la cartographie ;
- les notions attribuées ;
- les notions explicitement hors périmètre ;
- les termes techniques à relier au glossaire ;
- les règles de domaine supplémentaires nécessaires à cette leçon ;
- un Frontmatter complet ;
- une destination dans `Wiki/parcours/` ;
- un profil par défaut ;
- le nombre de sauts de ligne terminaux à conserver ;
- la table des fragments disponibles.

`visualisation` peut fixer un identifiant de `group` et son `libelle`. À défaut,
l’outillage utilise `groupe-<id-de-lecon>` et le titre de la leçon. Le champ
`hauteurs` peut conserver les dimensions qu’Obsidian exige après l’ajout des
préfixes de contexte.

Une migration peut laisser `hors_perimetre` et `termes` vides. Cet état ne vaut
pas validation sémantique : le statut du contrat reste alors `a-valider`.

## État de génération

Le statut d’une section vaut :

- `a-generer` — aucun contenu exploitable n’existe ;
- `generee` — un contenu existe mais n’a pas encore été validé ;
- `a-corriger` — la relecture a trouvé un défaut ;
- `validee` — le contenu peut servir de dépendance ;
- `desactivee` — le profil ou une décision explicite l’exclut ;
- `bloquee` — une dépendance ou une information nécessaire manque.

Une section `generee` ne devient jamais implicitement `validee`. La validation
est une décision humaine ou un contrôle explicitement autorisé par le contrat.

## Ordre de lecture et ordre de génération

L’ordre des rubriques dans la leçon reste défini par
`generator/sections.json`. L’ordre de génération suit les dépendances.

`Références` peut ainsi être préparée avant `Savoir le situer`, même si elle
apparaît à la fin de la leçon. `Se tester` est produit après les connaissances
et les limites qu’il doit manipuler.

Une section ne reçoit comme contexte que :

- les règles communes ;
- ses règles spécialisées ;
- le contrat de la leçon ;
- ses dépendances validées.

## Profils

Un profil choisit les rubriques présentes dans une sortie. Il ne change ni le
sens des rubriques ni leurs règles.

Le profil `complet` produit la leçon principale du Wiki. Un autre profil doit
écrire dans une destination distincte afin de ne pas remplacer silencieusement
la sortie principale.

Une rubrique obligatoire absente bloque l’assemblage. Une rubrique optionnelle
absente est omise.

## Assemblage

L’assembleur :

1. valide le contrat et le profil ;
2. rend le Frontmatter depuis le contrat ;
3. écrit le titre ;
4. ajoute l’introduction ;
5. ajoute les sections sélectionnées dans l’ordre de lecture ;
6. compare ou écrit la sortie.

L’assemblage est déterministe. Deux assemblages du même contrat et des mêmes
fragments produisent le même texte.

Les règles éditoriales communes historiques restent dans
[base.md](base.md). Les contrôles transverses vivent dans
[controle.md](controle.md).
