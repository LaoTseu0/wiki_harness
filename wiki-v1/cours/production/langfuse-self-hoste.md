# Langfuse self-hosté

> [carte du cours](../carte.md)

## L'essentiel

Langfuse est la plateforme d'observabilité LLM **self-hostable** — le
choix cohérent avec l'ADN local-first du homelab : les prompts et
réponses (données sensibles par nature) ne quittent pas la maison. Un
déploiement docker compose de plus, dans le style des autres services.

## Le savoir

- **Ce que c'est** : une UI + une API qui collectent des **traces**
  d'appels LLM — chaque trace contient des spans (générations, appels
  d'outils, retrieval), avec prompt, réponse, latence, tokens, coût,
  métadonnées. Pensé LLM d'emblée (vs un APM généraliste) : les
  prompts sont des objets de première classe.
- **Le déploiement v3** : docker compose officiel — web + worker,
  Postgres (métadonnées), ClickHouse (traces à volume), Redis, MinIO
  (S3 local). C'est le service le plus « gros » du homelab jusqu'ici —
  bonne occasion de pratiquer un compose multi-services avec réseau
  interne.
- **Le modèle de données à connaître** : organisation → projet →
  **traces** → **observations** (spans, generations, events) ; clés
  API par projet (public/secret) ; un projet par module ici (rag,
  agent) pour des tableaux de bord séparés.
- **Les alternatives, à situer** :
  LangSmith (SaaS, écosystème LangChain), Helicone (proxy), Arize
  Phoenix (open source, orienté evals) — le critère décisif ici :
  self-hostable et agnostique du framework.
- **Positionnement homelab** : réseau interne uniquement, pas
  d'exposition extérieure — les traces contiennent les prompts, donc
  potentiellement tout.

## En pratique

Compose Langfuse sur le homelab, projet « homelab-rag », clés en
variables d'environnement, healthcheck — puis première trace de test
envoyée depuis un script minimal avant d'instrumenter quoi que ce soit
([tracer les appels](tracer-les-appels.md)).

## Pièges connus

- Sous-estimer l'empreinte : ClickHouse + Postgres + Redis + MinIO —
  la pile v3 réclame plusieurs Go de RAM à elle seule, sur un hôte
  qui sert déjà Ollama (et bientôt Qdrant). Chiffrer avant/après
  (RAM libre, disque), poser la rétention (purge) dès l'installation
  — pas quand le disque est plein — et documenter les chiffres dans
  le README du module.
- Exposer l'UI sans y penser : elle montre tous les prompts — même en
  LAN, un mot de passe solide et pas de port forwardé.
- Verrouiller ses appels sur le SDK Langfuse partout dans le code :
  instrumenter à la frontière provider
  ([backend commutable](../framework/providers.md)) —
  un seul point de couture, remplaçable.

## Se tester

> « Pourquoi self-hoster son observabilité LLM ? »
> Les traces contiennent prompts et réponses — le plus sensible du
> système ; self-host = confidentialité par construction, coût nul à
> l'échelle homelab, et l'argument souveraineté/RGPD des offres
> françaises.

## Références

- Doc self-hosting Langfuse (docker compose v3)
