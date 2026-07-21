# 3.1 Garde-fous et sécurité d'abord

> **Module 3 — 03-jarvis-agent** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md)
> **Statut** : ⚪ à venir · **Passage** : 4e, après le module 5
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

La sécurité n'est pas une couche finale : **l'agent naît confiné**. La
section installe les deux périmètres avant la première capacité — le
périmètre logiciel (interception des appels d'outils) et le périmètre
système (conteneur à moindre privilège). Les non-négociables du homelab
([securite.md §5](../../../homelab/architecture/securite.md)) sont
exactement les bonnes pratiques métier, et l'ordre des sections du
module est lui-même le message : garde-fous d'abord, capacités ensuite.

## Contenu

- [ ] **[3.1.1 Hook tool_call](3.1.1-hook-tool-call/3.1.1-hook-tool-call.md)**
      — extension Pi : liste noire de commandes destructives +
      validation humaine (human-in-the-loop)
- [ ] **[3.1.2 Conteneur et moindre privilège](3.1.2-conteneur-moindre-privilege/3.1.2-conteneur-moindre-privilege.md)**
      — conteneur dédié, aucun accès aux partages famille

## Synthèse

Deux périmètres complémentaires, à savoir distinguer : le hook filtre
**ce que l'agent demande** (contrôle fin, mais contournable si l'agent
trouve un chemin non hooké), le conteneur borne **ce que le processus
peut** (grossier, mais infranchissable). La défense en profondeur,
c'est leur produit — et le vécu de la
[mini-boucle](../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.4-mini-boucle-agent/1.1.4-mini-boucle-agent.md)
(sandbox, validation humaine) passe ici à l'échelle d'un vrai harnais.
**Auto-contrôle** : pour chaque outil accordé à l'agent, savoir dire ce
qui se passe si le modèle l'appelle avec les *pires* arguments
possibles.

## Références

- [securite.md §5 du homelab](../../../homelab/architecture/securite.md)
  — les non-négociables d'origine
