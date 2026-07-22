# Retrieval hybride

> [carte du cours](../carte.md)

## L'essentiel

Le retrieval vectoriel comprend « sauvegarde » ≈ « backup » mais rate
« RTX 2060 » ou « qdrant » (termes exacts, hors vocabulaire
sémantique) ; **BM25 fait l'exact inverse**. L'hybride lance les deux
recherches et fusionne les classements — les benchmarks gagnent parce
que les deux moteurs se trompent sur des cas *différents*.

## Le savoir

- **Les deux jambes** :
  - **lexicale** : BM25 sur les textes des chunks — la mécanique
    complète est dans la [leçon dédiée](bm25.md) ;
  - **dense** : le top-k vecteurs de
    [2.2.1](migration-qdrant.md).
- **La fusion : RRF** (Reciprocal Rank Fusion) — la méthode robuste
  par défaut :

  ```
  score(d) = Σ  1 / (k + rang_i(d))      avec k ≈ 60
  ```

  On fusionne des **rangs**, pas des scores : BM25 et cosinus vivent
  sur des échelles incomparables, le rang les rend commensurables.
  Alternative (fusion pondérée α·dense + (1−α)·lexical) : plus fine
  mais exige de normaliser les scores et de régler α — RRF d'abord.
- **Où vit BM25** : soit à la main sur nos chunks (fidèle à l'esprit
  v0.0.1, ~50 lignes), soit via les sparse vectors natifs de Qdrant
  avec fusion RRF côté serveur — faire la version à la main d'abord,
  puis constater ce que Qdrant industrialise.
- **Quand l'hybride gagne** (à vérifier dans le jeu d'evals) :
  identifiants (`docker compose`, noms de conteneurs), acronymes (HA,
  NAS), valeurs (« 6333 ») ; quand le dense gagne : questions
  reformulées, synonymes, paraphrases.

## En pratique

Implémenter `chercher_hybride(question, k)` : top-20 BM25 + top-20
dense → RRF → top-k ; comparer sur les questions ratées par la
baseline (le retrieval 7/12 de la
[2.1.7](evals.md) —
combien l'hybride en repêche-t-il ?).

## Pièges connus

- Additionner des scores bruts BM25 + cosinus : échelles incomparables,
  une jambe écrase l'autre — fusionner des rangs (RRF) ou normaliser.
- Tokenisation incohérente entre l'index BM25 et les requêtes
  (casse, accents) : la jambe lexicale devient sourde.
- Conclure « l'hybride ne sert à rien » sur un jeu d'evals sans
  questions à termes exacts : le jeu doit couvrir les deux régimes de
  faiblesse.

## Se tester

> « Pourquoi votre RAG combine-t-il BM25 et vecteurs ? »
> Erreurs décorrélées : le lexical rate les paraphrases, le dense rate
> les termes exacts ; fusion par rangs (RRF) pour éviter le problème
> d'échelles — et le delta mesuré sur mon jeu d'evals en donne la
> preuve.

## Références

- Cormack et al., « Reciprocal Rank Fusion » (2009)
- Doc Qdrant : sparse vectors et hybrid queries
