# Sortie précoce et semver

> [carte du cours](../carte.md)

## L'essentiel

Pas de big-bang final : le framework sort en **0.0.1 dès que les
premières briques promues existent** (client LLM, outils, `rag_commun`),
puis évolue par incréments versionnés. La décision du 21 juillet 2026
([roadmap §1.5](../_archive/roadmap.md)) : fini les « v1/v2/v3 » fermées —
tout est jalons successifs, taggés, comparables.

## Le savoir

- **Semver en trois chiffres** : MAJEUR.MINEUR.PATCH —
  incompatibilité / fonctionnalité compatible / correction. En
  pré-1.0.0 (toute la vie de ce parcours), la convention assouplie :
  0.0.x = briques qui arrivent, 0.x.0 = jalon de génération.
  **Attention à la double numérotation héritée** : les dossiers du
  cours étiquettent les générations du RAG « v0.0.1 → v0.0.3 »
  (numérotation du sommaire), mais les **tags git** suivent la
  convention ci-dessus : 0.1.0 (à la main), 0.2.0 (Qdrant), 0.3.0
  (LlamaIndex) — cf. la PROGRESSION du module 2. En cas de doute, le
  tag fait foi.
- **Pourquoi sortir tôt** :
  - une release force la **définition du contrat** (ce qui est public
    est versionné, le reste peut bouger) ;
  - les tags git donnent des **points de comparaison** aux evals
    (« le score a bougé entre 0.0.3 et 0.0.4 — voici le diff ») ;
  - psychologiquement : un livrable imparfait publié bat un chef-d'œuvre
    en cours — c'est le principe n°2 de la
    [roadmap](../_archive/roadmap.md) (« chaque module produit un livrable
    qui tourne »).
- **La mécanique** : version dans `pyproject.toml`, tag git annoté
  (`git tag -a v0.0.1 -m "..."`), CHANGELOG court par release (3 lignes
  suffisent : ajouté / changé / cassé).
- **Le déclencheur de la 0.0.1** : client LLM extrait + registre
  d'outils + `rag_commun` promu — pas un de plus.

## En pratique

Checklist de release (à scripter à terme) : tests verts → bump version
→ CHANGELOG → tag → `pip install -e .` vérifié depuis un module
consommateur. Durée cible : < 10 minutes, sinon on ne le fera pas.

## Pièges connus

- Attendre « encore une brique » : le déclencheur est défini à
  l'avance précisément pour couper court au perfectionnisme.
- Casser un consommateur en 0.0.x « parce que c'est du pré-1.0 » : la
  règle interne reste : cassure = au minimum une note de migration.
- CHANGELOG romancé : trois lignes factuelles battent une page — c'est
  un outil de diff, pas de la communication.

## Se tester

> « Comment gérez-vous les versions d'une lib interne qui bouge
> vite ? »
> Semver dès le premier jour, releases petites et fréquentes, tags =
> points de mesure des evals, et un contrat public explicite — le
> reste est libre de bouger.

## Références

- semver.org ; Keep a Changelog (format minimal)
- [Commit `0704c42`](../_archive/roadmap.md) du repo — la décision semver
  appliquée à l'arborescence elle-même
