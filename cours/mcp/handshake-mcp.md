# Handshake MCP

> [carte du cours](../carte.md)

## L'essentiel

MCP n'est pas magique : c'est du **JSON-RPC 2.0** sur un transport
(stdio ou HTTP), avec trois messages à connaître par cœur —
`initialize`, `tools/list`, `tools/call`. Savoir dérouler ce handshake
à la main, c'est pouvoir dire en entretien « j'ai écrit les deux côtés
du protocole ».

## Le savoir

- **JSON-RPC 2.0** : requête = `{jsonrpc: "2.0", id, method, params}`,
  réponse = `{jsonrpc: "2.0", id, result | error}` ; les
  *notifications* (sans `id`) n'attendent pas de réponse.
- **La séquence d'ouverture** :
  1. client → `initialize` (version de protocole, capacités,
     identité) ;
  2. serveur → `result` (ses capacités : tools, resources, prompts) ;
  3. client → notification `notifications/initialized` — la session
     est ouverte.
- **La découverte** : `tools/list` renvoie chaque outil avec `name`,
  `description` et `inputSchema` (JSON Schema) — exactement le format
  du function calling de
  [1.1.3](../fondamentaux/function-calling.md) :
  MCP standardise la *distribution* des outils, pas leur nature.
- **L'appel** : `tools/call` avec `{name, arguments}` → `result.content`
  (liste de blocs typés : text, image…) + `isError`.
- **Les rôles** : host (l'app IA) / client (la connexion, 1 par
  serveur) / serveur (l'exposeur) — et le coût en contexte : chaque
  outil découvert entre dans la fenêtre (le rejet de MCP par Pi vécu
  au homelab).

## En pratique

L'exercice (~50 lignes) : lancer un serveur MCP en sous-processus,
échanger les trois messages sur stdio (une ligne JSON par message),
afficher la liste d'outils, en appeler un — sans SDK d'aucun côté.
C'est le livrable de la
[5.2](client.md).

## Pièges connus

- Oublier la notification `initialized` : certains serveurs refusent
  ensuite les appels — le handshake a trois temps, pas deux.
- Bufferiser stdio : sans flush ligne à ligne, les deux processus
  s'attendent mutuellement (deadlock silencieux).
- Mélanger logs et protocole sur stdout : en stdio, stdout est réservé
  au JSON-RPC — les logs vont sur stderr.

## Se tester

> « Que se passe-t-il concrètement quand un client MCP se connecte à un
> serveur ? »
> initialize / result / initialized, puis tools/list pour la
> découverte, tools/call pour l'exécution — du JSON-RPC 2.0 sur stdio
> ou HTTP, rien de plus.

## Références

- Spec MCP (modelcontextprotocol.io), sections lifecycle et tools
- Spec JSON-RPC 2.0
