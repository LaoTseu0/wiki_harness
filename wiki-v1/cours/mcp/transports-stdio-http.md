# Transports stdio et HTTP

> [carte du cours](../carte.md)

## L'essentiel

MCP sépare **la couche données** (JSON-RPC,
[handshake MCP](handshake-mcp.md))
de **la couche transport** : les mêmes messages voyagent en **stdio**
(local, un sous-processus par client) ou en **HTTP streamable**
(distant, un serveur pour plusieurs clients). Stdio d'abord — simple et
suffisant pour Claude Code — HTTP ensuite, pour le homelab en réseau.

## Le savoir

- **stdio** : le host lance le serveur en sous-processus ; JSON-RPC
  ligne par ligne sur stdin/stdout.
  - Forces : zéro réseau, zéro auth (la sécurité est celle du
    processus), idéal en local ;
  - contraintes : un processus **par client** (pas de partage d'état),
    cycle de vie lié au host, et la règle d'hygiène absolue : stdout
    est réservé au protocole, **les logs vont sur stderr** ;
  - c'est le transport du branchement
    [Claude Code](integration-claude-code.md).
- **HTTP streamable** : le serveur écoute (un endpoint MCP, réponses
  streamées SSE) ; les clients se connectent par le réseau.
  - Forces : serveur **partagé** (un seul processus pour tous les
    hosts du homelab), démarrage indépendant, conteneurisable comme
    les autres services ;
  - coûts : c'est un service réseau — auth (token au minimum), TLS si
    on sort du LAN, gestion de sessions ; la surface d'attaque naît
    ici ([le versant sécurité](securite.md)) ;
  - à situer : SSE pur est l'ancien transport, « streamable HTTP » le
    courant — les deux se rencontrent dans la nature.
- **Le choix par défaut** : stdio tant qu'un seul host local consomme ;
  HTTP quand le serveur devient un service du homelab (plusieurs
  clients, conteneur, monitoring). Le SDK rend la bascule triviale —
  **si** le serveur n'a pas d'état par client caché.

## En pratique

Étape 1 : stdio (le défaut FastMCP), validé avec l'inspector puis
Claude Code. Étape 2 : le même serveur en HTTP streamable dans un
conteneur du homelab, token simple, test depuis le
[client maison](client-mcp-minimal.md)
en réseau.

## Pièges connus

- Un `print()` de debug en mode stdio : le JSON-RPC est corrompu, le
  client décroche — logs sur stderr, toujours.
- De l'état global par client en stdio (un processus chacun) qui casse
  en HTTP (un processus partagé) : concevoir stateless dès le début —
  et le **vérifier** : test à deux clients concurrents sur le serveur
  HTTP (aucune réponse croisée), plus une revue rapide — aucune
  variable de module muable dans `serveur.py`.
- Exposer le HTTP sans auth « parce que c'est le LAN » : le serveur
  lit HA et la doc — un token et un bind d'interface, minimum.

## Se tester

> « stdio ou HTTP pour un serveur MCP ? »
> stdio : local, un processus par client, sécurité du processus,
> parfait pour l'outillage personnel. HTTP streamable : service
> partagé, réseau, auth/TLS — dès que plusieurs hosts ou une machine
> distante consomment. Même protocole au-dessus, la bascule est un
> choix d'exploitation.

## Références

- Spec MCP, section transports
- [Le versant sécurité](securite.md) — ce
  que le passage réseau ouvre
