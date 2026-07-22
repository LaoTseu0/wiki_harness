# Re-ranking

> [carte du cours](../carte.md)

## L'essentiel

Le retrieval rapide (BM25, vecteurs) est **volontairement grossier** :
il ramène 20-50 candidats en millisecondes. Le re-ranking applique
ensuite un modèle plus coûteux et plus précis sur ce petit lot pour
choisir le vrai top-5. C'est le pattern entonnoir : *rappel d'abord,
précision ensuite* — exigé tel quel par les offres seniors.

## Le savoir

- **Pourquoi le retrieval de base se trompe** : un bi-encoder encode la
  question et le document **séparément** — leur interaction fine
  (négations, « pourquoi » vs « comment », conditions) est perdue dans
  la compression en un seul vecteur.
- **Cross-encoder** : le re-ranker lit la paire *(question, document)*
  **ensemble** dans un même transformer et produit un score de
  pertinence. Beaucoup plus précis — mais il faut un passage par
  candidat, donc inapplicable à tout le corpus (d'où l'entonnoir).
- **L'architecture canonique** :
  `requête → top-50 (rapide) → cross-encoder sur 50 → top-5 (précis)`.
- **Les options** : modèles dédiés (bge-reranker, jina-reranker,
  MiniLM cross-encoders — self-hostables), API (Cohere Rerank), ou
  **LLM-as-reranker** (demander au LLM de noter chaque paire — lent
  mais sans dépendance nouvelle, bon premier exercice).
- **Mesurer** : le gain se lit dans les evals retrieval (le bon
  document monte dans le top-k) — tableau v0.0.1 → v0.0.2 du module 2.

## En pratique

L'exercice (~50 lignes) : prendre le top-20 vecteurs du RAG, re-scorer
chaque paire (question, chunk) avec Qwen3 via un prompt de notation
0-10, re-trier, comparer le rang du bon document avant/après sur le
[jeu d'evals](../../etapes/retrieval/evals/questions.json).

## Pièges connus

- Re-ranker un top-k trop petit (5) : si le bon document est 12ᵉ, le
  re-ranker ne peut pas le sauver — élargir le rappel d'abord.
- Latence oubliée : 50 passages de cross-encoder peuvent coûter plus
  que tout le reste de la chaîne ; mesurer, budgéter.
- LLM-as-reranker sans schéma de sortie : les notes arrivent en prose —
  contraindre ([1.1.5](../fondamentaux/structured-output.md)).

## Se tester

> « Votre RAG ramène le bon document en 8ᵉ position : que faites-vous ? »
> Élargir le top-k au retrieval, ajouter un re-ranker cross-encoder sur
> les candidats, et mesurer le déplacement de rang dans les evals —
> pas « changer de modèle d'embeddings » en premier réflexe.

## Références

- sentence-transformers, doc cross-encoders
- Cohere Rerank (pour situer l'offre API)
