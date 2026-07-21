# 5.2.1 Client MCP minimal

> **Leçon de la section [5.2 Le client](../5.2-client.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir — c'est l'exercice de l'entrée glossaire
> [handshake MCP](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.5-handshake-mcp/1.2.5-handshake-mcp.md)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

~50 lignes de Python pur : lancer un serveur MCP en sous-processus,
dérouler le handshake, lister les outils, en appeler un. Aucun SDK des
deux côtés de la table — après ça, plus rien dans MCP n'est une boîte
noire.

## Le savoir

- **L'anatomie du client** (la séquence détaillée vit dans
  l'[entrée glossaire](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.5-handshake-mcp/1.2.5-handshake-mcp.md)) :
  1. `subprocess.Popen` du serveur, pipes stdin/stdout, **flush ligne
     à ligne** ;
  2. `initialize` → lire le `result` (capacités) → notification
     `notifications/initialized` ;
  3. `tools/list` → afficher nom / description / inputSchema de chaque
     outil ;
  4. `tools/call` avec `{name, arguments}` → lire `result.content`.
- **Ce que le client révèle du host** : ce que fait Claude Code en
  plus, et *seulement* ça — boucler sur plusieurs serveurs, traduire
  les inputSchemas au format d'outils du modèle
  ([1.1.3](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md)),
  router le tool_call du modèle vers le bon serveur. Le pont
  modèle ↔ MCP est du code ordinaire.
- **La correspondance des ids** : JSON-RPC est asynchrone par nature —
  la réponse porte l'`id` de la requête ; notre client séquentiel peut
  se contenter d'un compteur, mais le *dire* (c'est la différence avec
  un client production).
- **Test d'interopérabilité** : le client doit marcher sur **notre**
  serveur ([5.1.1](../../5.1-serveur/5.1.1-serveur-mcp-python/5.1.1-serveur-mcp-python.md))
  et sur un serveur tiers (ex. un serveur d'exemple du SDK) — c'est le
  protocole qu'on valide, pas notre paire.

## En pratique

`client_minimal.py` : les 4 étapes, affichage lisible de la découverte,
un appel à `chercher_doc` avec une vraie question — et la démo croisée
sur un serveur tiers. Renvoi croisé depuis le glossaire
([1.2.5](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.5-handshake-mcp/1.2.5-handshake-mcp.md)).

## Pièges connus

- Lire stdout par blocs au lieu de lignes : un message JSON-RPC coupé
  en deux ne se parse pas — `readline()` et un JSON par ligne.
- Oublier stderr : si le serveur logge sur stderr et qu'on ne le lit
  jamais, le pipe peut se remplir et bloquer — le drainer (thread ou
  redirection).
- Sauter la notification `initialized` parce que « ça marche sans sur
  mon serveur » : le client doit suivre la spec, pas la tolérance d'une
  implémentation.

## Question d'entretien

> « Vous avez écrit un client MCP : qu'est-ce que ça vous a appris ? »
> Que le host n'a aucune magie : trois messages JSON-RPC sur un pipe,
> des schémas d'outils traduits pour le modèle, un dispatch — et que
> toute la valeur de MCP est dans la standardisation de la découverte,
> le reste étant du function calling classique.

## Références

- Spec MCP (lifecycle, tools) + spec JSON-RPC 2.0
- [1.1.3 Function calling](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md)
  — ce que le host fait des schémas découverts
