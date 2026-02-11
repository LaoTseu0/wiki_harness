# Glossaire exécutable

> [carte du cours](../carte.md)

## Vue d'ensemble

Transformer le module 1 en **glossaire dont chaque terme est un script
qui tourne**. Chaque leçon ci-dessous porte le savoir du concept (le
comprendre maintenant) ; l'exercice en Python pur arrive quand le
module source l'introduit. Règle d'entrée :

> Un concept qu'un framework cache et qu'on ne saurait pas refaire en
> ~50 lignes → un exercice numéroté en Python pur ici, avec renvoi
> croisé depuis le module qui l'a introduit.

## Contenu

- **[1.2.1 BM25](bm25.md)** — retrieval lexical
      (← [2.2](../retrieval/qdrant.md)),
      implémentable à la main
- **[1.2.2 Re-ranking](re-ranking.md)** —
      ré-ordonner le top-k (← 2.2)
- **[1.2.3 HNSW](hnsw.md)** — l'index de Qdrant
      (← 2.2), « comprendre et schématiser », pas implémenter
- **[1.2.4 Prompt caching](prompt-caching.md)**
      — ne pas re-payer le préfixe stable (← couche 0 / module 3)
- **[1.2.5 Handshake MCP](handshake-mcp.md)**
      — `tools/list` / `tools/call`
      (← [5.2](../mcp/client.md))
- **[1.2.6 LoRA](lora.md)** — culture fine-tuning
      (← [6.3](../production/culture-fine-tuning.md))

## Synthèse

Le glossaire est le **muscle anti-boîte-noire** du parcours : chaque
fois qu'un module 2-7 rencontre un terme que son framework enrobe, le
terme redescend ici en Python pur, puis remonte en renvoi croisé. À
terme, le README anglais devient un glossaire dont chaque entrée est un
script exécutable — la preuve portable qu'aucune couche n'est magique.
**Auto-contrôle** : pour chaque entrée, savoir répondre à « comment le
referiez-vous en 50 lignes ? ».
**Entrées candidates suivantes** (relecture critique du 21 juillet
2026, [CHALLENGE.md](../_archive/CHALLENGE.md)) : la **tokenisation** (ce
que coûte vraiment le français accentué ou un bloc YAML), le
**template de chat** (le texte que le modèle voit réellement — vu en
[1.1.3](../fondamentaux/function-calling.md))
et l'**attention/KV cache** en schéma commenté — la couche 0 ne doit
pas rester la seule couche magique du parcours.

## La règle

Une entrée = un script qu'on peut lancer. Tant qu'un concept n'a pas
sa version exécutable ici, il n'est pas acquis : il est récité.
