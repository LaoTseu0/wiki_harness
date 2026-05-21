# Générateur du parcours

Ce dossier rassemble les sources canoniques, les règles et les outils employés
pour produire les leçons du Wiki.

## Principe

Une leçon n’est plus générée en une seule fois. Son contenu canonique est
découpé en sections dans :

```text
generator/lessons/<parcours>/<id>/
```

Le fichier correspondant dans `Wiki/parcours/` est assemblé depuis ces
fragments. Il ne se modifie pas directement.

## Organisation

- `guardrails/parcours/AGENTS.md` fixe la langue, la rigueur et la méthode ;
- `guardrails/parcours/CADRAGE.md` distribue les règles selon l’opération ;
- `guardrails/lecon/` fixe le contrat commun et les contrôles ;
- `guardrails/sections/` contient une règle ciblée par rubrique ;
- `guardrails/schema/` contient les règles, registres et Canvas ;
- `sections.json` fixe l’ordre de lecture et les dépendances de génération ;
- `profiles/` sélectionne les rubriques selon l’usage ;
- `templates/sections/` contient les gabarits de nouveaux fragments ;
- `lessons/` contient les contrats, états et fragments canoniques ;
- `tools/` contient la préparation, l’assemblage et les contrôles.

Les contrats et profils utilisent JSON afin de rester lisibles sans ajouter de
dépendance Python au générateur.

## Cycle d’une section

1. choisir la leçon et la section ;
2. préparer son contexte minimal ;
3. produire uniquement le fragment demandé ;
4. relire le fragment ;
5. marquer la section `validee` ;
6. assembler et contrôler la leçon.

Les dépendances sont distinctes de l’ordre de lecture. `Références` peut être
validée avant `Savoir le situer`, même si elle apparaît à la fin du cours.

## Préparer le contexte

Lister les fichiers nécessaires :

```bash
python generator/tools/prepare_section.py position-rope savoir-le-situer --lister
```

Afficher le contexte complet :

```bash
python generator/tools/prepare_section.py position-rope savoir-le-situer
```

La commande refuse de préparer une section tant que ses dépendances ne sont pas
marquées `validee`.

## Mettre à jour un état

```bash
python generator/tools/set_lesson_status.py position-rope --section references --statut validee
```

La validation d’une section échoue si ses propres dépendances ne sont pas
validées.

## Assembler

Vérifier les sorties principales sans écrire :

```bash
python generator/tools/assemble_lesson.py --verifier
```

Reconstruire les sorties principales :

```bash
python generator/tools/assemble_lesson.py --ecrire
```

Assembler un profil différent exige une destination distincte :

```bash
python generator/tools/assemble_lesson.py position-rope --profil apprentissage --sortie build/apprentissage --ecrire
```

## Contrôler

```bash
python generator/tools/test_glossarylib.py
python generator/tools/format_glossary_terms.py --verifier
python generator/tools/validate_lessons.py
python generator/tools/canvas.py --verifier
```

Le test protège le traitement des pluriels et des zones Markdown qui ne sont
pas de la prose. Le formateur vérifie que les fragments portent déjà la mise en
forme déclarée par les contrats. Le validateur principal vérifie les contrats,
les états, les fragments, les profils et la conformité des sorties assemblées.
Le contrôle du glossaire exige une entrée française, un lien sur la première
occurrence de prose et du gras sur les occurrences suivantes. Le code, les URL
et les libellés de navigation ne sont pas des occurrences de prose. Une dette
éditoriale trouvée dans une section non validée reste un avertissement. La même
dette devient une erreur dès que la section est marquée `validee`.

## Migration initiale

`migrate_lessons.py` a servi à importer les leçons monolithiques existantes. Il
refuse d’écraser un dossier canonique. Une nouvelle leçon doit être créée depuis
les gabarits de `templates/sections/`, pas réimportée depuis le Wiki.

Le fichier `guardrails/parcours/REGLES.md` conserve le contrat monolithique de
la génération 1 comme archive. Il n’est plus chargé par la génération.

Le fichier `AGENTS.md` conservé à la racine sert uniquement de point d’entrée
pour les agents qui découvrent leurs instructions depuis la racine du dépôt.
