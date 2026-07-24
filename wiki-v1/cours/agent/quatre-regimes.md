# Quatre régimes, même boucle

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la mini-boucle d'agent](../fondamentaux/boucle-agent.md)
  — le régime manuel, référence à laquelle on rapporte les trois autres ; [le
  routage multi-agentique](../framework/routage-multi-agentique.md) — la
  distinction sous-agents / orchestration, à ne pas confondre avec le choix de
  régime.
- **Débloque** : [la note de conception](note-de-conception.md), qui consigne la
  comparaison au lieu de la laisser à la mémoire.

## L'essentiel

Refaire **le même mini-agent quatre fois** : à la main (domaine fondamentaux),
sur le harnais Pi, avec un SDK du marché (Claude Agent SDK ou OpenAI Agents SDK),
et en graphe LangGraph. La boucle réfléchir → agir → observer est identique
partout ; ce qui change, c'est ce que chaque régime prend en charge et ce qu'il
confisque.

La thèse : un comparatif de régimes n'a de valeur que fait sur la **même tâche,
mêmes outils, mêmes questions**. Recopié depuis la documentation des SDK, il ne
dit rien de ce qui décide vraiment — combien de lignes restent à ma charge, où
j'insère un garde-fou, ce que je vois quand ça rate.

Cette leçon ne couvre pas le mode persistant, qui est l'autre axe de variation
([mode RPC/SDK](mode-rpc-sdk.md)) : ici, les quatre régimes sont comparés à cycle
de vie égal.

## Le savoir

### Le comparatif, critère par critère

| Régime | Qui écrit la boucle | Contrôle | Observabilité | Coût d'entrée | Quand |
|---|---|---|---|---|---|
| **Manuel** ([mini-boucle](../fondamentaux/boucle-agent.md)) | nous | total | totale (c'est notre code) | élevé | comprendre ; besoins très spécifiques |
| **Harnais** (Pi, Claude Code) | le harnais | via hooks/extensions | bonne (sessions visibles) | faible | interactif outillé, développement quotidien |
| **SDK** (Claude Agent SDK, OpenAI Agents SDK) | le SDK | via callbacks/config | moyenne (selon le SDK) | moyen | embarquer un agent dans un produit |
| **Graphe** (LangGraph) | déclaré en graphe | fort sur le *flux* | bonne (état explicite) | moyen-élevé | workflows multi-étapes contraints, reprise sur état |

Chaque colonne est un des trois critères de choix, plus « qui écrit la boucle »
qui les explique : c'est parce que le harnais écrit la boucle qu'on n'y touche
que par hooks, et c'est parce que c'est notre code au régime manuel que
l'observabilité y est totale.

### Ce que le graphe change vraiment

LangGraph déclare les états et transitions **explicitement** — nœuds, arêtes,
checkpoints. La boucle libre devient un workflow contraint. La force est là :
reprise sur panne depuis un checkpoint, human-in-the-loop inséré *dans* le
graphe, flux auditables parce que l'état est nommé. Le coût aussi : rigidité — un
flux qui doit rester déclaré — et une courbe d'apprentissage que la liberté d'une
boucle `while` n'impose pas.

### Le scepticisme assumé sur le multi-agents

Des sessions séparées et observables battent souvent l'orchestration en boîte
noire. Le multi-agents ne se juge pas à son élégance mais aux mêmes critères que
le reste — contrôle, observabilité, coût — et sa vraie justification est
l'isolation de contexte, pas le parallélisme
([routage multi-agentique](../framework/routage-multi-agentique.md)). Un graphe
qui masque ce qui se passe entre ses nœuds a perdu l'observabilité qu'on lui
prêtait.

### La méthode de comparaison honnête

Trois questions, posées à l'identique dans les quatre régimes, font toute la
valeur du tableau : **combien de lignes restent à moi ? où est-ce que je place un
garde-fou ? qu'est-ce que je vois quand ça rate ?** Elles se consignent dans
[la note de conception](note-de-conception.md) au fil de l'expérience — pas
reconstituées après coup, où elles se réduiraient à la documentation qu'on
prétendait dépasser.

## Quand c'est la bonne réponse

- **Manuel** pour comprendre, ou quand un besoin très spécifique justifie le coût
  du contrôle total.
- **Harnais** pour l'interactif outillé et le développement quotidien.
- **SDK** pour embarquer un agent dans un produit.
- **Graphe** pour un workflow multi-étapes contraint avec reprise sur état.

Et une décision de méthode : **ne pas** apprendre les quatre à fond. Le temps y
passe et la comparaison n'y gagne rien — un seul régime se pratique, les trois
autres se situent. C'est la profondeur de la pratique sur un, pas la surface sur
quatre, qui rend la comparaison crédible.

## Ce qu'on ne saura pas faire

Tant que le même agent n'a pas tourné dans les quatre régimes, le tableau est
rempli de documentation, pas de vécu : les colonnes contrôle, observabilité et
coût ne valent qu'éprouvées. Deux pièges rôdent à ce moment-là — comparer des
tâches **différentes** entre régimes (le tableau ne vaut que si tout le reste est
constant), et conclure « le manuel est mieux » **parce qu'on l'a écrit** (le coût
d'entrée et de maintenance compte pour une équipe, la lucidité vaut mieux que la
fierté du code).

Ce qui promouvrait cette leçon en « refaire » : le même agent à trois outils —
lire un fichier, chercher dans la doc, agir sur un Home Assistant mocké — dans
les quatre régimes, et le tableau rempli avec le vécu.

## Se tester

1. « Framework d'agents ou boucle maison ? » Que répondez-vous, et sur quoi ?
   *Réussi si* la réponse rappelle que les quatre régimes partagent la même
   boucle, que le choix suit le besoin — contrôle et garde-fous fins pour
   manuel/harnais, intégration produit pour un SDK, workflow contraint avec
   reprise pour un graphe —, et que la comparaison ne vaut que faite sur une même
   tâche.
2. On vous montre un tableau comparatif des régimes tiré de la documentation des
   SDK. Qu'est-ce qui lui manque ?
   *Réussi si* la réponse note qu'un tableau de documentation ne répond pas aux
   trois questions du vécu — lignes à ma charge, place du garde-fou, ce que je
   vois quand ça rate — qui seules départagent.
3. Pourquoi ne pas apprendre les quatre régimes à fond ?
   *Réussi si* la réponse voit que le temps y passe sans que la comparaison y
   gagne, et qu'un régime pratiqué en profondeur situe mieux les autres que
   quatre survolés.

## À retenir

- Même boucle dans les quatre régimes ; ce qui change est qui écrit la boucle et
  ce que le régime confisque.
- Le graphe déclare états et transitions : reprise sur panne et flux auditables,
  contre rigidité et courbe d'apprentissage.
- Le multi-agents se justifie par l'isolation de contexte, pas le parallélisme,
  et se juge aux mêmes critères que le reste.
- Un comparatif ne vaut que sur une même tâche, avec trois questions de vécu :
  lignes à moi, place du garde-fou, ce que je vois quand ça rate.
- Un régime se pratique, les trois autres se situent.

## Références

- Documentation LangGraph — graphes, checkpoints, human-in-the-loop dans le flux
