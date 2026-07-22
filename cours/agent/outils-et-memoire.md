# Outils et mémoire

> [carte du cours](../carte.md)

## Vue d'ensemble

Les garde-fous posés ([3.1](garde-fous.md)),
l'agent gagne ses deux capacités : **agir** sur le homelab via un outil
Home Assistant à périmètre limité, et **se souvenir** via une mémoire
externe versionnée dans git. Deux leçons, deux patterns du métier :
l'outil custom enregistré dans un harnais, et l'« external memory » du
context engineering.

## Contenu

- **[3.2.1 Outil home_assistant](outil-home-assistant.md)**
      — `pi.registerTool` : API REST de HA, token à périmètre limité
- **[3.2.2 Mémoire versionnée](memoire-versionnee.md)**
      — hooks session → git pull/commit (convention OKF)

## Synthèse

Capacité et mémoire se renforcent : un agent qui agit sans mémoire
répète ses erreurs, une mémoire sans capacité n'a rien à retenir.
L'outil HA montre le pattern « registre »
([1.3.3](../framework/evolutivite.md))
en conditions réelles ; la mémoire git montre que le long terme d'un
agent se déporte **hors de la fenêtre de contexte**, dans des fichiers
diffables et réversibles. **Auto-contrôle** : savoir expliquer pourquoi
la mémoire d'un agent doit être *versionnée* (audit, rollback, blame —
la mémoire est du code).

## Références

- [architecture/jarvis.md](../../../homelab/architecture/jarvis.md) —
  la roadmap Jarvis dont ce module est la Phase 3
