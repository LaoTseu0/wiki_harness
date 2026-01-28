# 3.3 Comparaison des régimes d'agents

> **Module 3 — 03-jarvis-agent** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md)
> **Statut** : ⚪ à venir · **Passage** : 4e, après le module 5
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Zoom arrière final du module : la même boucle d'agent existe sous
quatre régimes — manuelle, harnais, SDK, graphe — et savoir les situer
vaut une réponse d'entretien à elle seule. La section ajoute le mode
persistant (RPC/SDK), la comparaison quatre régimes, et la note de
conception qui capitalise le tout.

## Contenu

- [ ] **[3.3.1 Mode RPC/SDK](3.3.1-mode-rpc-sdk/3.3.1-mode-rpc-sdk.md)**
      — (bonus) un service qui tient une session Pi ouverte — embryon
      d'agent persistant
- [ ] **[3.3.2 Quatre régimes, même boucle](3.3.2-quatre-regimes/3.3.2-quatre-regimes.md)**
      — (bonus culture) manuelle / harnais Pi / SDK du marché /
      graphe LangGraph
- [ ] **[3.3.3 Note de conception](3.3.3-note-de-conception/3.3.3-note-de-conception.md)**
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
