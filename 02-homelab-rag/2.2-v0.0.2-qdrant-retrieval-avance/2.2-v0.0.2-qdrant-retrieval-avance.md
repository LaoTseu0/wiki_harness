# 2.2 v0.0.2 — Qdrant + retrieval avancé ⚪

> **Module 2 — 02-homelab-rag** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md) · [progression du module](../PROGRESSION.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Outiller le stockage et pousser le retrieval au niveau exigé par les
offres seniors — Qdrant, recherche hybride, re-ranking, filtres — et
**mesurer le gain** contre la baseline 7/12 de la
[v0.0.1](../2.1-v0.0.1-rag-a-la-main/2.1-v0.0.1-rag-a-la-main.md). Les
cinq leçons forment un entonnoir de précision : une vraie base (2.2.1),
un rappel élargi (2.2.2 hybride), un tri affiné (2.2.3 re-ranking), un
périmètre maîtrisé (2.2.4 filtres) — et la preuve chiffrée (2.2.5).

## Contenu

- [ ] **[2.2.1 Migration Qdrant](2.2.1-migration-qdrant/2.2.1-migration-qdrant.md)**
      — conteneur docker homelab, collections, payloads
- [ ] **[2.2.2 Retrieval hybride](2.2.2-retrieval-hybride/2.2.2-retrieval-hybride.md)**
      — BM25 + vecteurs, fusion des classements *(→
      [entrée glossaire BM25](../../01-llm-from-scratch/1.2-glossaire-executable/1.2.1-bm25/1.2.1-bm25.md))*
- [ ] **[2.2.3 Re-ranking du top-k](2.2.3-re-ranking-top-k/2.2.3-re-ranking-top-k.md)**
      — cross-encoder sur les candidats *(→
      [entrée glossaire](../../01-llm-from-scratch/1.2-glossaire-executable/1.2.2-re-ranking/1.2.2-re-ranking.md))*
- [ ] **[2.2.4 Filtres métadonnées](2.2.4-filtres-metadonnees/2.2.4-filtres-metadonnees.md)**
      — par dossier, par type de doc
- [ ] **[2.2.5 Evals comparatives](2.2.5-evals-comparatives/2.2.5-evals-comparatives.md)**
      — même jeu, tableau v0.0.1 → v0.0.2

## Synthèse

La v0.0.2 ne change **pas la nature** de la chaîne — elle muscle le
« R » : mêmes embeddings, même génération, mais un rappel plus large
(hybride), un tri plus fin (re-ranking) et un périmètre plus net
(filtres), servis par une vraie base (Qdrant, dont l'index HNSW est
compris via le [glossaire](../../01-llm-from-scratch/1.2-glossaire-executable/1.2.3-hnsw/1.2.3-hnsw.md)).
Chaque ajout se justifie par son delta dans le tableau — un ajout sans
delta se retire. **Auto-contrôle** : savoir expliquer pourquoi hybride
et re-ranking attaquent des faiblesses *différentes* du retrieval
vectoriel.

## Livrable

Le tableau comparatif v0.0.1 → v0.0.2 dans le README du module —
chaque technique avec son delta mesuré.
