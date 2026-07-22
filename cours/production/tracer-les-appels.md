# Tracer les appels

> [carte du cours](../carte.md)

## L'essentiel

Instrumenter les modules 2 (RAG) et 3 (agent) : chaque requête devient
une **trace** structurée en spans — un span par maillon de la chaîne.
La règle d'or : la granularité des spans épouse l'architecture ; si les
spans sont illisibles, c'est souvent l'architecture qui l'est.

## Le savoir

- **La trace RAG type** (une requête `POST /ask`,
  [2.4.1](../retrieval/service-fastapi.md)) :

  ```
  trace "ask"
  ├── span retrieval        (question, k, filtres → chunks + scores, ms)
  │   ├── span embed_query  (tokens, ms)
  │   └── span search       (Qdrant, ms)
  ├── span rerank           (si actif — candidats → ordre, ms)
  └── generation "answer"   (prompt complet, réponse, tokens in/out, ms)
  ```

  Chaque maillon de la
  [chaîne](../retrieval/rag-a-la-main.md)
  a son span — le diagnostic par couche devient un clic.
- **La trace agent** (module 3) : un span par tour de
  [boucle](../fondamentaux/boucle-agent.md),
  chaque tool_call avec arguments et résultat, et les **décisions du
  hook** ([3.1.1](../agent/hook-tool-call.md))
  en events — la trace devient aussi un journal de sécurité.
- **Où coudre l'instrumentation** : à la **frontière provider**
  ([2.4.2](../retrieval/backend-commutable.md))
  pour les générations (un seul point pour tous les appels LLM), et
  dans `rag_commun` pour les spans métier — le code applicatif ne voit
  pas Langfuse.
- **Ce qu'on met dans les métadonnées** : version du corpus, config de
  chaîne (hybride ? rerank ?), tag git — c'est ce qui permet de
  corréler traces et [tableau d'evals](../retrieval/tableau-final.md).

## En pratique

Décorateurs/context managers sur `rag_commun` et le provider, envoi
asynchrone (ne jamais bloquer la réponse pour tracer), et le test
d'usage : retrouver depuis l'UI la trace d'une question des evals et
lire chunk par chunk pourquoi elle a raté.

## Pièges connus

- Tracer en synchrone dans le chemin de requête : l'observabilité qui
  dégrade la latence qu'elle mesure — batch/async, toujours. Mais
  l'async a son revers : si l'export échoue (Langfuse indisponible,
  process arrêté avant le flush), on perd en silence précisément les
  traces d'incident — prévoir flush au shutdown, file locale bornée,
  et un compteur d'événements perdus qui rend la perte visible.
- Des spans trop gros (« toute la requête ») ou trop fins (chaque
  fonction) : la bonne maille est le *maillon métier* — celle qu'on
  voudra accuser.
- Oublier l'échec : les erreurs et timeouts sont les traces les plus
  précieuses — les capturer avec leur contexte, pas seulement les
  succès.

## Se tester

> « Que tracez-vous dans votre système LLM ? »
> Une trace par requête, un span par maillon (retrieval avec chunks et
> scores, génération avec prompt/tokens/latence), décisions de
> garde-fous en events, métadonnées de version — cousu à la frontière
> provider pour ne pas polluer le métier.

## Références

- SDK Python Langfuse (décorateurs, spans, generations)
- [2.1.7 Evals](../retrieval/evals.md)
  — ce que les traces expliquent
