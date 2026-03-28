# v0.0.2 — Qdrant + retrieval avancé

> [carte du cours](../carte.md)

## Vue d'ensemble

Outiller le stockage et pousser le retrieval au niveau exigé par les
offres seniors — Qdrant, recherche hybride, re-ranking, filtres — et
**mesurer le gain** contre la baseline 7/12 de la
[v0.0.1](rag-a-la-main.md). Les
cinq leçons forment un entonnoir de précision : une vraie base (2.2.1),
un rappel élargi (2.2.2 hybride), un tri affiné (2.2.3 re-ranking), un
périmètre maîtrisé (2.2.4 filtres) — et la preuve chiffrée (2.2.5).

## Contenu

- **[Migration Qdrant](migration-qdrant.md)**
      — conteneur docker homelab, collections, payloads
- **[Retrieval hybride](retrieval-hybride.md)**
      — BM25 + vecteurs, fusion des classements *(→
      [leçon BM25](bm25.md))*
- **[Re-ranking du top-k](re-ranking-top-k.md)**
      — cross-encoder sur les candidats *(→
      [leçon dédiée](re-ranking.md))*
- **[Filtres métadonnées](filtres-metadonnees.md)**
      — par dossier, par type de doc
- **[Evals comparatives](evals-comparatives.md)**
      — même jeu, tableau v0.0.1 → v0.0.2

## Synthèse

La v0.0.2 ne change **pas la nature** de la chaîne — elle muscle le
« R » : mêmes embeddings, même génération, mais un rappel plus large
(hybride), un tri plus fin (re-ranking) et un périmètre plus net
(filtres), servis par une vraie base (Qdrant, dont l'index HNSW est
compris via la [leçon HNSW](hnsw.md)).
Chaque ajout se justifie par son delta dans le tableau — un ajout sans
delta se retire. **Auto-contrôle** : savoir expliquer pourquoi hybride
et re-ranking attaquent des faiblesses *différentes* du retrieval
vectoriel.

## Livrable

Le tableau comparatif v0.0.1 → v0.0.2 dans le README du module —
chaque technique avec son delta mesuré.
