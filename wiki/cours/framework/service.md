# Service FastAPI

> [carte du cours](../carte.md)

## L'essentiel

Le RAG cesse d'être un script qu'on lance : il devient un
**micro-service HTTP** — `POST /ask` → réponse + sources. C'est le
pattern d'intégration usuel — un LLM ne vit jamais seul — et le
prérequis de ce qui suit : le serveur MCP l'appellera, Langfuse le
tracera.

## Le savoir

- **Le contrat d'API, en Pydantic des deux côtés**
  ([structured output](../fondamentaux/structured-output.md)
  appliqué au web) :

  ```python
  class AskRequest(BaseModel):
      question: str
      k: int = 5
      filtres: Filtres | None = None    # 2.2.4 exposé

  class AskResponse(BaseModel):
      reponse: str
      sources: list[Source]             # fichier, section, score
      metriques: Metriques              # latence, tokens — pour 6.1
  ```

  FastAPI valide l'entrée, sérialise la sortie, génère la doc OpenAPI
  (`/docs`) — gratuitement.
- **Async où ça compte** : les appels Ollama/Qdrant sont de l'I/O —
  `async def` + client httpx async permettent de servir plusieurs
  requêtes pendant les attentes réseau (et c'est le domaine inférence qui
  mesurera ce que le *moteur* fait de la concurrence).
- **La frontière service/bibliothèque** : la route est **mince** — elle
  valide, appelle `rag_commun.ask()`, sérialise. Toute la logique
  reste dans la bibliothèque : c'est elle qu'on teste
  ([tests, typing, packaging](tests-typing-packaging.md))
  et qu'on promeut en brique.
- **Opérationnel minimal** : `GET /health` (les conteneurs du homelab
  en vivent), erreurs HTTP propres (422 validation, 503 backend
  indisponible), uvicorn en conteneur — un service de plus dans le
  style homelab.

## En pratique

`service.py` : deux routes (`/ask`, `/health`), modèles Pydantic,
appel à la bibliothèque commune ; test de bout en bout au `curl` — et
brancher le [client MCP du domaine MCP](../mcp/serveur-mcp-python.md)
dessus le moment venu.

## Pièges connus

- La logique dans la route : intestable sans serveur, non promouvable —
  la route orchestre, la bibliothèque travaille.
- Bloquer l'event loop avec un client HTTP synchrone dans une route
  async : une requête lente gèle toutes les autres.
- Exposer le service au-delà du réseau homelab sans auth : hors
  périmètre pour l'instant, mais à dire en entretien (auth, rate
  limiting, quotas — la partie « production » du discours).

## Se tester

> « Comment exposez-vous un système LLM au reste du SI ? »
> Micro-service HTTP au contrat Pydantic strict, routes minces sur une
> bibliothèque testée, health check, doc OpenAPI générée, async sur
> l'I/O — et des métriques par réponse pour l'observabilité.

## Références

- Doc FastAPI (Pydantic models, async, `/docs`)
