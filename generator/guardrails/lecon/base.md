# Contrat commun d'une leçon

## Un seul concept

Une leçon ouvre une seule pièce. Elle peut montrer ses relations, mais ne
réenseigne pas les pièces voisines. Une notion majeure possède sa propre leçon.
Une notion secondaire tient en quelques lignes ou rejoint le glossaire.

La cartographie fixe ce que chaque Parcours doit couvrir. Une notion ne peut pas
disparaître pendant la rédaction : elle devient une leçon, une partie
explicitement rattachée à une leçon, ou une entrée de glossaire.

## Termes techniques et glossaire

Un terme ou un mot-clé technique spécifique qui exige une définition pour
comprendre le cours possède une entrée dans `Wiki/glossaire/`. Cette entrée
conserve le terme consacré et donne sa définition en français simple.

Dans le corps de chaque leçon :

1. la première occurrence du terme ou de l'expression porte un lien vers son
   entrée de glossaire ;
2. les occurrences suivantes dans cette même leçon sont en gras, sans lien.

La règle recommence dans chaque leçon. Elle rend la définition accessible au
premier emploi sans multiplier les liens dans le reste du texte.

## Cadrage d'un Parcours avant rédaction

Avant la première leçon d'un Parcours, sa rubrique de cartographie reçoit un
tableau `Découpage prévu`. Chaque ligne fixe :

- l'ordre et l'identifiant stable de la leçon ;
- son titre de travail ;
- son processus et son étape, ou `aucun — <raison>` ;
- son schéma et son élément lorsqu'elle n'ouvre pas un processus ;
- les connaissances qui lui sont exclusivement attribuées.

Le tableau est le contrat de génération des leçons. Le rédacteur ne déplace pas
une connaissance vers une autre leçon et n'élargit pas la couverture sans
modifier d'abord la cartographie.

Toutes les notions de la liste du Parcours possèdent exactement une destination
dans le tableau. Plusieurs leçons peuvent ouvrir la même étape lorsqu'elles
étudient des mécanismes distincts de cette étape. Un processus référencé doit
être au moins `cadré` dans `generator/guardrails/schema/processus/index.md`. Un schéma référencé doit
être au moins `cadré` dans `generator/guardrails/schema/index.md`.

## Frontmatter

Le contrat canonique porte les champs du Frontmatter. La leçon assemblée
commence par leur représentation Markdown :

```yaml
---
id: sampling
type: leçon
titre: Le sampling
parcours: 0-generation
statut: brouillon
tags: [generation, sampling]
created: 2026-07-24
updated: 2026-07-24
verified: 2026-07-24
processus: generation-token
etape: sampling
brique: generation
contrat: praxis.generation.Sampler
---
```

Une leçon sans processus remplace `etape` par le couple `schema`–`element` :

```yaml
processus: aucun — architecture statique du projet
schema: environnement-projet-python
element: environnement-virtuel
```

- `id` est stable et unique ;
- `parcours` correspond à une section de la cartographie ;
- `statut` vaut `brouillon`, `en-revue` ou `validé` ;
- `verified` date la dernière vérification des sources mouvantes ;
- `processus` correspond à un Canvas de `generator/guardrails/schema/processus/` ;
- `etape` correspond à un nœud stable de ce Canvas ;
- `schema` correspond à un Canvas de `generator/guardrails/schema/references/` ;
- `element` correspond à un nœud stable de ce schéma ;
- `brique` nomme la brique Praxis concernée ;
- `contrat` nomme l'API publique déposée ou vaut `aucun — <raison>`.

Une mise à jour éditoriale change `updated`. Une nouvelle vérification des
sources change `verified`.

Une leçon déclare exactement un couple de positionnement : `processus`–`etape`
ou `schema`–`element`.

## MathJax

Dans une leçon destinée à Obsidian :

- une formule intégrée à une phrase utilise `$...$` ;
- une formule en bloc utilise `$$...$$` ;
- les délimiteurs `\(...\)` et `\[...\]` ne sont pas utilisés.

## Squelette

Les fichiers de `generator/templates/sections/` matérialisent les rubriques à
initialiser. Ils servent à créer un fragment canonique ; ils ne sont pas
eux-mêmes des leçons.

```markdown
---
<Frontmatter complet>
---

# Titre

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> cas pratique : [`sujet.py`](../../cas-pratique/...)

## Prérequis

## Savoir le situer

## Connaissances

## Reconstruction

## Décision et dépôt dans Praxis

## Limites et cas d'échec

## Se tester

## Mesures

## Références
```

`Mesures` est présent lorsque la leçon avance ou produit un résultat
quantitatif. Il est omis dans le cas contraire.

Chaque rubrique est conservée dans un fragment distinct. L’ordre ci-dessus est
un ordre de lecture ; `generator/sections.json` fixe séparément les dépendances
de génération.
