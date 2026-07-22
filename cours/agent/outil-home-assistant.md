# 3.2.1 Outil home_assistant

> **Leçon de la section [3.2 Outils et mémoire](../3.2-outils-et-memoire.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Premier outil custom **réel** de l'agent : `home_assistant`, enregistré
via `pi.registerTool`, qui appelle l'API REST de HA avec un token à
périmètre limité. Le pattern est exactement celui du
[function calling](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md) —
mais cette fois l'outil touche la maison, donc chaque choix de
périmètre compte.

## Le savoir

- **L'API REST de HA, le minimum vital** : `GET /api/states` (entités
  et états), `GET /api/states/<entity_id>`,
  `POST /api/services/<domain>/<service>` (actions — allumer, couper) ;
  auth par header `Authorization: Bearer <token>` (long-lived access
  token).
- **Le périmètre du token** : HA ne scope pas finement ses tokens →
  le scope se construit : un **utilisateur HA dédié** à l'agent, non
  admin ; côté outil, une **liste blanche d'entités et de services**
  (les lampes du salon oui, la serrure non) — le moindre privilège de
  la [3.1.2](../../3.1-garde-fous-et-securite/3.1.2-conteneur-moindre-privilege/3.1.2-conteneur-moindre-privilege.md)
  appliqué aux credentials.
- **Le design de l'outil** (le schéma est du prompt engineering,
  [1.1.3](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md)) :
  - plutôt **deux outils** (`ha_lire` / `ha_agir`) qu'un couteau
    suisse : la lecture peut être allow, l'action passe en ask
    ([3.1.1](../../3.1-garde-fous-et-securite/3.1.1-hook-tool-call/3.1.1-hook-tool-call.md)) ;
  - arguments **énumérés** quand c'est possible (entity_id dans un
    enum généré depuis la liste blanche) — le modèle ne peut pas
    inventer une entité hors périmètre ;
  - réponses **compactes** : `GET /api/states` complet sature la
    fenêtre — filtrer et résumer côté outil.
- **Lien MCP** : le même homelab sera exposé en lecture par le
  [serveur MCP](../../../05-homelab-mcp/5.1-serveur/5.1.1-serveur-mcp-python/5.1.1-serveur-mcp-python.md) —
  deux canaux de distribution (outil de harnais vs protocole), même
  savoir-faire de périmètre.

## En pratique

`pi.registerTool` : `ha_lire` (états, liste blanche) et `ha_agir`
(services, liste blanche + ask), token d'un utilisateur HA dédié
stocké hors du code ; test réel : « quelle température au salon ? »
puis « allume la lampe du bureau » (avec validation humaine visible).

## Pièges connus

- Le token admin « pour que ça marche » : le jour où l'agent est
  injecté, l'injection est admin de la maison.
- Renvoyer le JSON brut de HA au modèle : des milliers de tokens
  d'attributs inutiles — résumer côté outil, toujours.
- Décrire l'outil vaguement (« contrôle la maison ») : le modèle
  tentera des services non prévus ; la description énonce le périmètre
  exact.

## Question d'entretien

> « Comment donnez-vous à un agent l'accès à une API sensible ? »
> Identité dédiée non admin, liste blanche d'opérations côté outil,
> arguments énumérés, lecture/action séparées avec human-in-the-loop
> sur l'action, réponses filtrées — et le hook + conteneur en dessous.

## Références

- Doc API REST Home Assistant (states, services, tokens)
- [architecture/jarvis.md](../../../../homelab/architecture/jarvis.md)
