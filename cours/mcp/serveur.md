# 5.1 Le serveur

> **Module 5 — 05-homelab-mcp** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md)
> **Statut** : ⚪ à venir · **Passage** : 3e, avant le module 3
> *(décision du 21 juillet 2026)*
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Écrire un serveur MCP complet qui expose le homelab **en lecture** —
conteneurs, entités HA, recherche dans la doc (le RAG du module 2,
encore chaud). Trois leçons dans l'ordre de construction : le serveur
et ses outils, les transports (stdio puis HTTP), et le branchement sur
un client réel (Claude Code) avec sa doc d'intégration. MCP est nommé
dans ~60 % des offres — le pari du module est déjà gagné, reste à
livrer.

## Contenu

- [ ] **[5.1.1 Serveur MCP Python](5.1.1-serveur-mcp-python/5.1.1-serveur-mcp-python.md)**
      — outils homelab en lecture : conteneurs, entités HA, recherche
      doc (réutilise le [service RAG](../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.1-service-fastapi/2.4.1-service-fastapi.md))
- [ ] **[5.1.2 Transports stdio et HTTP](5.1.2-transports-stdio-http/5.1.2-transports-stdio-http.md)**
      — stdio d'abord, HTTP ensuite
- [ ] **[5.1.3 Intégration Claude Code](5.1.3-integration-claude-code/5.1.3-integration-claude-code.md)**
      — branchement sur un client existant + doc d'intégration

## Synthèse

Le serveur referme une boucle du parcours : le function calling appris
à la main ([1.1.3](../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md))
devient un **service d'outils standardisé** que n'importe quel host
peut découvrir — MCP ne change pas la nature des outils, il change
leur *distribution*. Et le RAG du module 2 gagne son deuxième
consommateur (après le service FastAPI), preuve d'architecture.
**Auto-contrôle** : savoir dessiner host / client / serveur et placer
`tools/list` / `tools/call` sur le schéma.

## Références

- [Roadmap couche 4](../../roadmap.md) — l'architecture MCP complète
- Spec MCP (modelcontextprotocol.io)
