# Service et craftsmanship

> [carte du cours](../carte.md)

## Vue d'ensemble

Sortir le RAG du script : un micro-service FastAPI consommable par le
reste du parcours, un backend commutable local/cloud, et le
craftsmanship Python qui monte avec les modules. Les trois leçons sont
les trois faces d'une même promotion : le RAG devient un **produit**
(service), **portable** (abstraction provider) et **maintenable**
(tests, typing, packaging).

## Contenu

- **[2.4.1 Service FastAPI](service-fastapi.md)**
      — `POST /ask` → réponse + sources ; réutilisé par le
      [serveur MCP](../mcp/serveur.md),
      tracé en [6.1](../production/observabilite.md)
- **[2.4.2 Backend commutable](backend-commutable.md)**
      — abstraction provider local/cloud par config ; future brique du
      [framework](../framework/index.md)
- **[2.4.3 Tests, typing, packaging](tests-typing-packaging.md)**
      — pytest sur la chaîne
      ([07_evals.py](../../etapes/retrieval/07_evals.py) en germe),
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
