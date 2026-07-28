# Fondations du projet

## La finalité d'apprentissage

Le cours s'adresse à un développeur full stack expérimenté en JavaScript, avec
des bases en Java et une pratique récente de Python.

L'apprenant retient particulièrement bien une information lorsqu'il peut la
replacer dans un schéma. La représentation visuelle n'est donc pas une
illustration facultative ajoutée après le texte : elle participe à la méthode
d'apprentissage et à la cohérence du référentiel.

Il poursuit trois résultats :

- comprendre les mécanismes qui relient un modèle de langage à un harnais
  agentique ;
- apprendre le Python nécessaire en construisant ces mécanismes ;
- faire émerger un assistant local réellement utilisé sur une infrastructure
  personnelle.

Le cours ne prépare pas une démonstration jetable. Chaque Parcours doit produire
une connaissance vérifiable et une pièce qui rapproche Mnémos d'un usage
quotidien.

## Deux objets

**Praxis** est la bibliothèque générique. Elle expose les contrats, clients,
outils, mémoires et mécanismes d'exécution appris pendant le parcours. Elle ne
connaît ni la personnalité, ni la topologie concrète, ni les appareils de
Mnémos.

**Mnémos** est l'assistant personnel construit sur Praxis. Il est local-first,
mono-utilisateur et auto-hébergé. Il peut employer un service cloud lorsqu'une
capacité locale manque, mais ce choix reste explicite et remplaçable.

Praxis fournit les mécanismes. Mnémos prend les décisions propres au produit :
agents disponibles, permissions, sources de mémoire, voix, appareils et
politiques d'exploitation.

## Ce que « maîtriser » veut dire

Le cours ouvre toute boîte noire dont le mécanisme change une décision de
conception, une limite, un risque ou une mesure.

Deux passages sont attendus :

1. reconstruire une version minimale du mécanisme ;
2. la confronter à une implémentation industrielle.

Reconstruire un sampler, un client streaming, une boucle d'outils ou un
checkpointer minimal appartient au parcours. Réécrire un pilote GPU, une pile
TLS ou un moteur de base de données n'y appartient pas. Dans ce second cas, la
leçon ouvre le contrat et les garanties de la dépendance, puis marque
explicitement la frontière.

Un outil ne tient jamais lieu de concept. Ollama, llama.cpp, vLLM, LangGraph,
Temporal ou Qdrant servent d'études de cas après l'explication du mécanisme
qu'ils matérialisent.

## L'ordre du parcours

La cartographie suit un **ordre de construction du harnais**. Cet ordre est
cognitif et pratique ; il ne prétend pas représenter une pile logicielle
strictement ascendante.

Un Parcours peut rouvrir une pièce rencontrée plus tôt lorsqu'il change de
niveau d'analyse. Le KV cache peut ainsi être expliqué pendant la génération,
puis mesuré pendant l'inférence locale.

Les notions de la cartographie sont exhaustives pour la version courante du
référentiel. Elles ne sont pas figées pour toujours. Une évolution étayée peut
modifier la cartographie et doit alors préserver les identifiants des leçons
déjà publiées ou documenter leur migration.

## La forme d'un Parcours

Chaque Parcours contient quatre résultats :

1. **Mécanismes** — les concepts à comprendre et leurs relations ;
2. **Reconstruction** — une version minimale écrite ou manipulée à la main ;
3. **Cas pratique** — une situation vérifiable sur le matériel ou les services
   du projet ;
4. **Intégration** — une brique testée déposée dans Praxis, ou l'assemblage
   explicite d'une brique déjà acquise.

À partir du premier client utilisable, chaque Parcours fait également progresser
un fil rouge de Mnémos. Le produit ne doit pas attendre le dernier Parcours pour
commencer à fonctionner.

## Connaissance stable et veille

La cartographie contient les mécanismes durables. Les fonctions mouvantes d'un
produit ou d'un protocole vivent dans `Wiki/veille/`.

Une entrée de veille porte :

- son statut : `stable`, `adopté`, `à comparer`, `émergent` ou `déprécié` ;
- une source primaire ;
- la version ou la date vérifiée ;
- le mécanisme concerné ;
- la décision : intégrer, attendre ou écarter.

Une nouveauté ne rejoint pas le cours parce qu'elle est populaire. Elle le
rejoint si elle modifie un mécanisme, un contrat, une garantie, une menace ou
une décision mesurable.
