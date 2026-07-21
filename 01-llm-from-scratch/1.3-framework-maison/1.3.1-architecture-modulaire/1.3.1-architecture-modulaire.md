# 1.3.1 Architecture modulaire

> **Leçon de la section [1.3 Le framework maison](../1.3-framework-maison.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Découper le framework en **briques enfichables** dont chacune a une
interface étroite et un remplaçant possible : client LLM, outils,
boucle d'agent, mémoire, retrieval, evals. La règle : les briques
dépendent d'**abstractions** (interfaces), jamais les unes des autres —
c'est ce qui permet au module 2 d'utiliser le retrieval sans embarquer
la boucle d'agent.

## Le savoir

- **Les six briques et leur origine** — chaque brique est un script du
  parcours, promu :

  | Brique | Origine | Interface minimale |
  |---|---|---|
  | client LLM | 01-03 (chat, stream) | `chat(messages, **options) → réponse/stream` |
  | outils | 06 (function calling) | `nom, description, schéma, run(args)` |
  | boucle d'agent | 07 (mini-agent) | `run(tâche, outils, garde-fous) → résultat` |
  | mémoire | module 3 (OKF) | `charger(clé) / sauver(clé, valeur)` |
  | retrieval | module 2 (`rag_commun`) | `chercher(question, k, filtres) → chunks` |
  | evals | 07_evals du module 2 | `évaluer(jeu, système) → scores` |

- **Providers interchangeables** : le client LLM est une interface
  (`Protocol` Python) avec des implémentations Ollama / OpenAI-compat /
  Claude — la
  [2.4.2](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.2-backend-commutable/2.4.2-backend-commutable.md)
  en est le prototype.
- **Le sens des dépendances** : boucle → (outils, client) ; RAG →
  (retrieval, client) ; **jamais l'inverse**, et jamais brique →
  brique concrète. Un `import` qui traverse deux briques est un bug
  d'architecture.
- **Anti-modèle assumé** : pas de « God object » à la LangChain
  (chaînes qui savent tout faire) — des petites interfaces qu'on
  compose à la main, lisibles en entretien.

## En pratique

Premier jalon : extraire le client LLM des scripts 01-03 en
`framework/client.py` + tests ; y brancher `rag_commun` promu — la
0.0.1 de la
[1.3.6](../1.3.6-sortie-precoce-semver/1.3.6-sortie-precoce-semver.md).

## Pièges connus

- L'abstraction prématurée : ne créer l'interface qu'au **deuxième**
  usage concret (le premier provider s'écrit en direct).
- Interface qui fuit : si `chat()` expose un champ spécifique Ollama,
  tous les providers devront le simuler — normaliser aux frontières.
- Découper trop fin : six briques, pas seize ; une brique = un concept
  qu'on peut nommer en entretien.

## Question d'entretien

> « Comment structureriez-vous une lib LLM interne pour qu'elle
> survive au changement de provider ? »
> Interfaces par capacité (chat, embed), providers en plugins,
> normalisation aux frontières, tests contractuels communs à tous les
> providers — et un exemple concret : ce framework.

## Références

- Le [routeur multi-modèles](../../../../homelab/architecture/router-multi-model.md)
  du homelab — la brique routage en germe
- « Dependency Inversion Principle » (le D de SOLID) appliqué en Python
  (`typing.Protocol`)
