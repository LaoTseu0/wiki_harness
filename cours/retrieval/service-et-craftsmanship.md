# 2.4 Service et craftsmanship ⚪

> **Module 2 — 02-homelab-rag** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md) · [progression du module](../PROGRESSION.md)
> **Statut** : ⚪ à venir *(section ajoutée le 21 juillet 2026)*
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Sortir le RAG du script : un micro-service FastAPI consommable par le
reste du parcours, un backend commutable local/cloud, et le
craftsmanship Python qui monte avec les modules. Les trois leçons sont
les trois faces d'une même promotion : le RAG devient un **produit**
(service), **portable** (abstraction provider) et **maintenable**
(tests, typing, packaging).

## Contenu

- [ ] **[2.4.1 Service FastAPI](2.4.1-service-fastapi/2.4.1-service-fastapi.md)**
      — `POST /ask` → réponse + sources ; réutilisé par le
      [serveur MCP](../../05-homelab-mcp/5.1-serveur/5.1-serveur.md),
      tracé en [6.1](../../06-production/6.1-observabilite/6.1-observabilite.md)
- [ ] **[2.4.2 Backend commutable](2.4.2-backend-commutable/2.4.2-backend-commutable.md)**
      — abstraction provider local/cloud par config ; future brique du
      [framework](../../01-llm-from-scratch/1.3-framework-maison/1.3-framework-maison.md)
- [ ] **[2.4.3 Tests, typing, packaging](2.4.3-tests-typing-packaging/2.4.3-tests-typing-packaging.md)**
      — pytest sur la chaîne
      ([07_evals.py](../2.1-v0.0.1-rag-a-la-main/2.1.7-evals/07_evals.py) en germe),
      typing, packaging à la promotion

## Synthèse

Cette section transforme l'exercice en **actif** : le service expose le
RAG au module 5 (MCP) et au module 6 (traces), l'abstraction provider
répond à l'angle mort cloud, et le craftsmanship rend le tout
promouvable en brique du framework. C'est le pattern complet des offres
— « RAG en production », pas « PoC de RAG ». **Auto-contrôle** : le
service tient-il les trois promesses — un `curl` suffit à l'interroger,
un changement de config suffit à changer de backend, un `pytest` suffit
à le valider ?

## Livrable du module

`02-homelab-rag/` avec le tableau de métriques dans le README.
**CV** : « built and evaluated a RAG pipeline end-to-end (custom, then
Qdrant + LlamaIndex), with regression evals ».
