# Comparaison des régimes d'agents

> [carte du cours](../carte.md)

## Vue d'ensemble

Zoom arrière final du module : la même boucle d'agent existe sous
quatre régimes — manuelle, harnais, SDK, graphe — et savoir les situer
vaut une réponse d'entretien à elle seule. La section ajoute le mode
persistant (RPC/SDK), la comparaison quatre régimes, et la note de
conception qui capitalise le tout.

## Contenu

- **[Mode RPC/SDK](mode-rpc-sdk.md)**
      — (bonus) un service qui tient une session Pi ouverte — embryon
      d'agent persistant
- **[Quatre régimes, même boucle](quatre-regimes.md)**
      — (bonus culture) manuelle / harnais Pi / SDK du marché /
      graphe LangGraph
- **[Note de conception](note-de-conception.md)**
      — dans `architecture/` + `.pi/` complet versionné

## Synthèse

Le message de la section : **la boucle est un invariant, le régime est
un choix d'exploitation**. Manuel pour comprendre, harnais pour
l'interactif outillé, SDK pour l'embarqué produit, graphe pour les
workflows contraints — et le choix se défend par les critères
(contrôle, observabilité, coût d'entrée), pas par la mode.
**Auto-contrôle** : savoir dire pour un cas donné (« un bot de triage
de mails ») quel régime on prendrait et pourquoi.

## Livrable du module

`03-jarvis-agent/` (le `.pi/` complet versionné = le « profil » de
l'agent) + note de conception dans `architecture/`.
**CV** : « designed a sandboxed autonomous agent with tool-call
interception, human-in-the-loop guardrails and git-versioned memory ».
*Le projet portfolio le plus original du lot.*
