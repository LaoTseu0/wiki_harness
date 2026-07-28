# Point d’entrée du contrat du projet

Ce fichier distribue les règles selon la pièce produite. Il évite de charger
les règles d’une section, d’un schéma ou d’une intégration lorsqu’elles ne sont
pas nécessaires à l’opération demandée.

## Hiérarchie des sources de vérité

1. [AGENTS.md](AGENTS.md) fixe la langue, la rigueur et la méthode de travail ;
2. le présent fichier fixe la hiérarchie et le chargement du cadre ;
3. les fichiers spécialisés ci-dessous fixent leur domaine ;
4. [cartographie.md](cartographie.md) attribue les notions aux leçons ;
5. le contrat d’une leçon fixe son périmètre et son positionnement ;
6. une section canonique applique ces sources.

Une règle locale ne contredit jamais une source placée au-dessus d’elle.

## Règles toujours chargées pour une section de leçon

La préparation d’une section charge :

1. [AGENTS.md](AGENTS.md) ;
2. le présent fichier ;
3. [fondations.md](fondations.md) ;
4. [lecon/REGLES.md](../lecon/REGLES.md) et
   [lecon/base.md](../lecon/base.md) ;
5. le contrat JSON de la leçon ;
6. le fichier de règles propre à la section ;
7. les sections dont elle dépend, après validation.

Le registre [sections.json](../../sections.json) matérialise cet ordre, les
dépendances et les règles spécialisées.

## Règles chargées selon le domaine

| Opération | Règles supplémentaires |
|---|---|
| produire `Savoir le situer` ou un Canvas | [schema/REGLES.md](../schema/REGLES.md) |
| traiter l’état, la mémoire, un workflow ou la reprise | [architecture-agentique.md](architecture-agentique.md) |
| déposer une brique dans Praxis ou faire progresser Mnémos | [integration.md](integration.md) |
| créer ou modifier un cas pratique | [cas-pratique.md](cas-pratique.md) |
| contrôler une leçon ou le dépôt | [lecon/controle.md](../lecon/controle.md) |

Une génération ne charge pas un fichier spécialisé sans rapport avec son
Output. La réduction du contexte ne dispense jamais de charger les règles
communes ni le contrat de la leçon.

## Sources canoniques et sorties dérivées

Les fragments placés dans `generator/lessons/<parcours>/<id>/sections/` sont les
sources canoniques du texte d’une leçon. Son contrat et son état vivent dans le
même dossier.

Le fichier correspondant dans `Wiki/parcours/` est une sortie assemblée. Il ne
se modifie pas directement. Une correction porte sur le contrat ou la section
canonique, puis l’outillage reconstruit la leçon.

Une sortie dérivée peut être supprimée et reconstruite sans perte
d’information. Une source canonique ne le peut pas.

Les Canvas complets de `generator/guardrails/schema/processus/` et
`generator/guardrails/schema/references/` restent les sources canoniques
visuelles. Les vues de `generator/guardrails/schema/canvas/` restent dérivées.

## Documents de cadrage

- [fondations.md](fondations.md) décrit la finalité d’apprentissage et les deux
  objets Praxis et Mnémos ;
- [architecture-agentique.md](architecture-agentique.md) fixe le vocabulaire de
  l’état, de la mémoire, des checkpoints et de la reprise ;
- [integration.md](integration.md) fixe les briques et les exigences
  d’intégration ;
- [cartographie.md](cartographie.md) fixe l’ordre et la couverture ;
- [lecon/REGLES.md](../lecon/REGLES.md) fixe le cycle de vie d’une leçon
  assemblée par sections.
