# 3.3.1 Mode RPC/SDK

> **Leçon de la section [3.3 Comparaison des régimes d'agents](../3.3-comparaison-regimes-agents.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir (bonus)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Jusqu'ici l'agent vit le temps d'une session interactive. Le mode
RPC/SDK inverse le rapport : un **service qui tient une session Pi
ouverte**, pilotable par programme — l'embryon d'agent *persistant*,
celui qui pourra être déclenché par un événement HA plutôt que par un
humain au clavier.

## Le savoir

- **Le changement de posture** : de « l'humain ouvre une session » à
  « la session attend des requêtes ». Concrètement : un petit service
  (FastAPI, le pattern de la
  [2.4.1](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.1-service-fastapi/2.4.1-service-fastapi.md))
  qui possède une session Pi via son mode RPC/SDK et expose
  `POST /task` → réponse de l'agent.
- **Ce que la persistance change** :
  - le **contexte s'accumule** entre requêtes → la gestion de contexte
    ([1.1.1](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.1-chat-cli-historique-contexte/1.1.1-chat-cli-historique-contexte.md))
    et la [mémoire versionnée](../../3.2-outils-et-memoire/3.2.2-memoire-versionnee/3.2.2-memoire-versionnee.md)
    passent de confort à nécessité (quand committer, si la session ne
    « finit » jamais ? → checkpoints périodiques) ;
  - les **garde-fous restent** : le hook
    ([3.1.1](../../3.1-garde-fous-et-securite/3.1.1-hook-tool-call/3.1.1-hook-tool-call.md))
    vaut pour les requêtes programmatiques aussi — mais le
    human-in-the-loop doit trouver sa forme asynchrone : file
    d'approbation avec **TTL** (une approbation qui n'arrive pas à
    temps devient un refus, renvoyé au modèle comme information), et
    une action approuvée tardivement se **re-valide contre l'état
    courant** avant exécution — approuver à H puis exécuter à H+6
    sans re-vérifier est le piège de l'agent persistant ;
  - la **santé de session** : une session qui vit des jours dérive
    (contexte, état) — prévoir recyclage et resurrection propre sur
    des **déclencheurs mesurables** (plafond de tokens de contexte,
    n tâches traitées, taux d'erreurs d'outils qui monte), pas « au
    feeling » ; la mémoire externe rend la session jetable.
- **Pourquoi c'est un embryon** : file de tâches, multi-sessions,
  déclencheurs événementiels sont *hors scope* — le but est de
  démontrer le régime, pas de construire la plateforme.

## En pratique

Service minimal : une session Pi tenue ouverte, `POST /task`,
checkpoint mémoire toutes les n tâches, endpoint `/health` qui vérifie
la session — démonstration : trois tâches successives qui partagent le
contexte.

## Pièges connus

- La session immortelle : sans recyclage, le contexte finit par
  déborder ou dériver — la mémoire externe existe pour que mourir ne
  coûte rien.
- Sérialiser les requêtes sans le dire : une session = un fil ; deux
  requêtes concurrentes s'entremêlent — file d'attente explicite.
- Perdre le human-in-the-loop en devenant service : les actions
  sensibles doivent *attendre* une approbation, pas être silencieusement
  refusées ou pire, accordées.

## Question d'entretien

> « Quelle différence entre un agent interactif et un agent
> persistant ? »
> Le cycle de vie : session éphémère pilotée par l'humain vs service
> long-vivant piloté par événements — ce qui déplace la gestion de
> contexte, la forme du human-in-the-loop et la santé de session au
> premier plan ; la mémoire externe est ce qui rend les deux régimes
> compatibles.

## Références

- Mode RPC/SDK de Pi (doc du harnais)
- [3.2.2 Mémoire versionnée](../../3.2-outils-et-memoire/3.2.2-memoire-versionnee/3.2.2-memoire-versionnee.md)
  — la brique qui rend la session jetable
