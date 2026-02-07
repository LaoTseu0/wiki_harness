# Le client

> [carte du cours](../carte.md)

## Vue d'ensemble

Connaître les **deux côtés** du protocole : après le serveur, un client
MCP minimal écrit à la main — découverte `tools/list`, appel
`tools/call`, au niveau JSON-RPC, sans SDK. C'est l'exercice qui
transforme « j'ai utilisé MCP » en « j'ai écrit un client et un
serveur MCP » — la formulation exacte de certaines offres.

## Contenu

- **[5.2.1 Client MCP minimal](client-mcp-minimal.md)**
      — handshake, découverte, appel — sans SDK *(= l'exercice de
      l'[entrée glossaire handshake MCP](../glossaire/handshake-mcp.md))*

## Synthèse

Écrire le client démystifie le dernier étage : le host n'a aucune
magie — il lance un processus, échange trois messages JSON-RPC, et
injecte les schémas d'outils dans la fenêtre du modèle. Une fois le
client écrit, la phrase « MCP standardise la distribution d'outils,
pas leur nature » devient un vécu, pas un slogan. **Auto-contrôle** :
brancher son client sur son serveur ET sur un serveur tiers — s'il
marche sur les deux, le protocole est compris.

## Références

- [1.2.5 Handshake MCP](../glossaire/handshake-mcp.md)
  — la théorie que ce client exécute
