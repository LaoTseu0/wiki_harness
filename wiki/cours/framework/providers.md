# Backend commutable

> [carte du cours](../carte.md)

## L'essentiel

Embeddings et génération basculables **local ↔ cloud par config**, sans
toucher au code : l'abstraction provider. C'est trois choses à la
fois : la future brique client LLM du
[framework](../framework/architecture-modulaire.md),
la réponse minimale à l'angle mort cloud
, et l'argument de réversibilité
qui plaît aux entreprises (souveraineté ↔ état de l'art).

## Le savoir

- **L'interface, étroite et typée** (`typing.Protocol`) :

  ```python
  class LLMProvider(Protocol):
      async def chat(self, messages: list[Message], **opts) -> Reponse: ...
      async def embed(self, textes: list[str]) -> list[Vecteur]: ...
  ```

  Implémentations : `OllamaProvider` (l'existant),
  `OpenAICompatProvider` (couvre vLLM du domaine inférence, OpenRouter, et la
  plupart des clouds), éventuellement `ClaudeProvider` (API native).
  Le choix vient de la config (`RAG_PROVIDER=ollama|openai|...` + URL,
  clé, modèles) — Pydantic Settings, jamais de clé en dur.
- **Normaliser aux frontières** : mêmes `Message`/`Reponse` pour tous ;
  les particularités (préfixes de tâche des
  [embeddings](../retrieval/embeddings.md), formats de tool calls) se
  gèrent *dans* le provider.
- **Le piège de fond — les embeddings ne commutent pas** : changer de
  provider d'embeddings = changer d'espace vectoriel = **ré-indexer
  tout le corpus**
  ([embeddings](../retrieval/embeddings.md)).
  L'index mémorise donc le modèle qui l'a produit, et le service
  refuse un mismatch au démarrage. La génération, elle, commute
  librement.
- **Situer les offres managées** : AWS Bedrock, Azure OpenAI, GCP
  Vertex AI — mêmes concepts, API parfois OpenAI-compatibles,
  argumentaire RGPD/région à connaître.

## En pratique

Extraire le provider de `rag_commun`, config par variables
d'environnement, et une démo : les mêmes evals rejouées avec la
génération sur une API cloud ponctuelle — une ligne de tableau de plus
(qualité vs coût vs confidentialité).

## Pièges connus

- L'interface qui épouse Ollama (champ `options` exposé tel quel) :
  chaque provider suivant devra le simuler — normaliser d'abord.
- Commuter les embeddings « pour tester » sans ré-indexer : scores
  effondrés, debug long — d'où le verrou index ↔ modèle.
- Multiplier les providers spéculatifs : deux réels (Ollama +
  OpenAI-compat) couvrent le besoin ; le troisième attendra un usage
  ([dogfooding](../framework/dogfooding.md)).

## Se tester

> « Votre client veut du local pour la confidentialité mais du cloud
> pour la qualité : votre architecture ? »
> Abstraction provider par capacité, bascule par config, verrou
> index/embeddings, routage par sensibilité des données
> ([routage multi-agentique](../framework/routage-multi-agentique.md)) —
> et les offres managées situées (Bedrock/Azure/Vertex).

## Références

- Pydantic Settings — la config validée
