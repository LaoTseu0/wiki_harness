# 1.2 Glossaire exécutable

> **Module 1 — 01-llm-from-scratch** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md) · [progression du module](../PROGRESSION.md)
> **Statut** : 🔵 continu — alimenté par les modules 2-7 ; le module 1
> n'est jamais fermé
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Transformer le module 1 en **glossaire dont chaque terme est un script
qui tourne**. Chaque leçon ci-dessous porte le savoir du concept (le
comprendre maintenant) ; l'exercice en Python pur arrive quand le
module source l'introduit. Règle d'entrée :

> Un concept qu'un framework cache et qu'on ne saurait pas refaire en
> ~50 lignes → un exercice numéroté en Python pur ici, avec renvoi
> croisé depuis le module qui l'a introduit.

## Contenu

- [ ] **[1.2.1 BM25](1.2.1-bm25/1.2.1-bm25.md)** — retrieval lexical
      (← [2.2](../../02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2-v0.0.2-qdrant-retrieval-avance.md)),
      implémentable à la main
- [ ] **[1.2.2 Re-ranking](1.2.2-re-ranking/1.2.2-re-ranking.md)** —
      ré-ordonner le top-k (← 2.2)
- [ ] **[1.2.3 HNSW](1.2.3-hnsw/1.2.3-hnsw.md)** — l'index de Qdrant
      (← 2.2), « comprendre et schématiser », pas implémenter
- [ ] **[1.2.4 Prompt caching](1.2.4-prompt-caching/1.2.4-prompt-caching.md)**
      — ne pas re-payer le préfixe stable (← couche 0 / module 3)
- [ ] **[1.2.5 Handshake MCP](1.2.5-handshake-mcp/1.2.5-handshake-mcp.md)**
      — `tools/list` / `tools/call`
      (← [5.2](../../05-homelab-mcp/5.2-client/5.2-client.md))
- [ ] **[1.2.6 LoRA](1.2.6-lora/1.2.6-lora.md)** — culture fine-tuning
      (← [6.3](../../06-production/6.3-culture-fine-tuning/6.3-culture-fine-tuning.md))

## Synthèse

Le glossaire est le **muscle anti-boîte-noire** du parcours : chaque
fois qu'un module 2-7 rencontre un terme que son framework enrobe, le
terme redescend ici en Python pur, puis remonte en renvoi croisé. À
terme, le README anglais devient un glossaire dont chaque entrée est un
script exécutable — la preuve portable qu'aucune couche n'est magique.
**Auto-contrôle** : pour chaque entrée, savoir répondre à « comment le
referiez-vous en 50 lignes ? ».
**Entrées candidates suivantes** (relecture critique du 21 juillet
2026, [CHALLENGE.md](../../CHALLENGE.md)) : la **tokenisation** (ce
que coûte vraiment le français accentué ou un bloc YAML), le
**template de chat** (le texte que le modèle voit réellement — vu en
[1.1.3](../1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md))
et l'**attention/KV cache** en schéma commenté — la couche 0 ne doit
pas rester la seule couche magique du parcours.

## Livrable

[README](../README.md) anglais : « every entry is a runnable script » —
pièce maîtresse du portfolio.
