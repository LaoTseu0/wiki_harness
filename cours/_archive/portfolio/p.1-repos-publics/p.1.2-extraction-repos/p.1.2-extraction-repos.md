# P.1.2 Extraction en repos dédiés

> **Leçon de la section [P.1 Les repos publics](../p.1-repos-publics.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : 🔵 décision au fil de l'eau
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Ce repo `framework` est le **monorepo de travail** ; certains modules
gagneront à devenir des **repos publics autonomes** (un projet = une
vitrine focalisée). La décision se prend au cas par cas — extraire a un
coût, et tout n'a pas vocation à sortir.

## Le savoir

- **Pourquoi extraire** : un repo dédié raconte **une** histoire (un
  recruteur qui cherche « RAG » trouve un repo RAG, pas un monorepo de
  formation), a son propre README au canon
  ([P.1.1](../p.1.1-github-public/p.1.1-github-public.md)), ses issues,
  ses stars. `llm-from-scratch` (le glossaire exécutable) et
  `homelab-rag` (le tableau d'evals) sont les candidats naturels.
- **Le coût, à ne pas sous-estimer** : préserver l'**historique git**
  (`git subtree split` ou `filter-repo` plutôt qu'un copier-coller qui
  jette le passé), gérer la dépendance au
  [framework maison](../../../01-llm-from-scratch/1.3-framework-maison/1.3-framework-maison.md)
  (un module extrait doit pouvoir installer le framework — d'où le
  [packaging](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.3-tests-typing-packaging/2.4.3-tests-typing-packaging.md)),
  et maintenir deux endroits.
- **La règle de décision** (au fil de l'eau, pas d'avance) : extraire
  quand le module est **stable, autoportant et raconte une histoire
  vendable** — pas avant. Un module encore en 0.0.x qui bouge chaque
  semaine reste dans le monorepo.
- **La cohérence avec le semver du framework**
  ([1.3.6](../../../01-llm-from-scratch/1.3-framework-maison/1.3.6-sortie-precoce-semver/1.3.6-sortie-precoce-semver.md)) :
  un repo extrait qui dépend du framework consomme une **version
  taguée** — l'extraction force à figer le contrat, ce qui est sain.
- **Décision consignée** : la
  [PROGRESSION du module 1](../../../01-llm-from-scratch/PROGRESSION.md)
  note déjà « extraction en repo dédié : reportée, à décider si
  nécessaire » — la trace de l'arbitrage vaut la décision.

## En pratique

Au moment jugé opportun : `git subtree split` du module → nouveau repo
→ README au canon → dépendance framework via version taguée → CI
minimale (lint + tests rapides) ; garder un pointeur depuis le
monorepo. Ne rien extraire tant que le critère (stable + vendable)
n'est pas rempli.

## Pièges connus

- Extraire trop tôt : un module instable en repo séparé = double
  maintenance pour une vitrine qui change tout le temps.
- Copier-coller en jetant l'historique : le `git log` *est* une partie
  du récit (le
  [dogfooding](../../../01-llm-from-scratch/1.3-framework-maison/1.3.5-dogfooding/1.3.5-dogfooding.md),
  les décisions datées) — préserver via subtree/filter-repo.
- Extraire un module qui dépend du framework sans packaging propre :
  le repo ne s'installe pas, l'effet vitrine est perdu.

## Question d'entretien

> « Comment organisez-vous vos projets sur GitHub ? »
> Un monorepo de travail, et des extractions ciblées quand un module
> est stable et raconte une histoire — historique préservé par
> subtree, dépendances par versions taguées ; on n'extrait pas pour
> extraire.

## Références

- `git subtree split` / `git filter-repo` — préserver l'historique
- [PROGRESSION module 1](../../../01-llm-from-scratch/PROGRESSION.md) —
  l'arbitrage déjà noté
