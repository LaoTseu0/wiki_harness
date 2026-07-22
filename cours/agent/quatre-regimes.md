# 3.3.2 Quatre régimes, même boucle

> **Leçon de la section [3.3 Comparaison des régimes d'agents](../3.3-comparaison-regimes-agents.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir (bonus culture)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Refaire **le même mini-agent quatre fois** : à la main (module 1), sur
le harnais Pi, avec un SDK du marché (Claude Agent SDK ou OpenAI
Agents SDK), et en graphe LangGraph. La boucle
réfléchir → agir → observer est identique partout — ce qui change,
c'est ce que chaque régime prend en charge et ce qu'il confisque.

## Le savoir

- **Le comparatif, critère par critère** :

  | Régime | Qui écrit la boucle | Contrôle | Observabilité | Coût d'entrée | Quand |
  |---|---|---|---|---|---|
  | **Manuel** ([1.1.4](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.4-mini-boucle-agent/1.1.4-mini-boucle-agent.md)) | nous | total | totale (c'est notre code) | élevé | comprendre ; besoins très spécifiques |
  | **Harnais** (Pi, Claude Code) | le harnais | via hooks/extensions | bonne (sessions visibles) | faible | interactif outillé, dev quotidien |
  | **SDK** (Claude Agent SDK, OpenAI Agents SDK) | le SDK | via callbacks/config | moyenne (selon SDK) | moyen | embarquer un agent dans un produit |
  | **Graphe** (LangGraph) | déclaré en graphe | fort sur le *flux* | bonne (état explicite) | moyen-élevé | workflows multi-étapes contraints, reprise sur état |

- **Ce que le graphe change vraiment** : LangGraph déclare les états
  et transitions **explicitement** (nœuds, arêtes, checkpoints) — la
  boucle libre devient un workflow contraint. Force : reprise sur
  panne, human-in-the-loop *dans* le graphe, flux auditables.
  Coût : rigidité, courbe d'apprentissage — monte vite dans les offres
  ([roadmap §10.4](../../../roadmap.md)).
- **Le scepticisme de Pi, assumé** ([roadmap couche 3](../../../roadmap.md)) :
  des sessions séparées observables battent souvent l'orchestration en
  boîte noire — le multi-agents se juge aux mêmes critères
  ([1.3.4](../../../01-llm-from-scratch/1.3-framework-maison/1.3.4-routage-multi-agentique/1.3.4-routage-multi-agentique.md)).
- **La méthode de comparaison honnête** : même tâche, mêmes outils,
  mêmes questions — combien de lignes à moi ? où mettre un
  garde-fou ? que vois-je quand ça rate ? — consignées dans la
  [note de conception](../3.3.3-note-de-conception/3.3.3-note-de-conception.md).

## En pratique

Le même agent à 3 outils (lire un fichier, chercher dans la doc, agir
sur HA mocké) dans les quatre régimes ; tableau rempli avec le vécu,
pas la doc — c'est le vécu qui se raconte en entretien.

## Pièges connus

- Comparer des tâches différentes entre régimes : le tableau ne vaut
  que si tout le reste est constant.
- Conclure « le manuel est mieux » parce qu'on l'a écrit : le critère
  coût d'entrée/maintenance compte pour une équipe — la lucidité vaut
  mieux que la fierté.
- Apprendre les quatre à fond : un à fond (Pi), les autres situés — la
  [roadmap](../../../roadmap.md) dit « à situer, l'un à pratiquer ».

## Question d'entretien

> « Framework d'agents ou boucle maison : que choisissez-vous ? »
> Les quatre régimes existent, même boucle en dessous ; le choix suit
> le besoin — contrôle et garde-fous fins (manuel/harnais + hooks),
> intégration produit (SDK), workflow contraint avec reprise
> (LangGraph) — et je les ai comparés sur la même tâche.

## Références

- [Roadmap couche 3](../../../roadmap.md) — SDKs et harnais à situer
- Doc LangGraph (graphes, checkpoints, human-in-the-loop)
