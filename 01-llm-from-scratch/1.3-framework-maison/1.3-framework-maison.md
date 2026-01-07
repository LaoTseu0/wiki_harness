# 1.3 Le framework maison

> **Module 1 — 01-llm-from-scratch** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md) · [progression du module](../PROGRESSION.md)
> **Statut** : ⚪ à venir — release 0.0.1 dès les premières briques
> promues, puis semver en continu
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

L'aboutissement du parcours : la trajectoire scripts → glossaire →
bibliothèque → **framework maison**, que les modules suivants
consomment (dogfooding) et font évoluer. Les six leçons couvrent les
deux faces du chantier : *ce qu'on construit* (briques, routage) et
*comment on le construit* (craftsmanship, plugins, releases précoces).
Pas de big-bang final — 0.0.1 tôt, incréments semver ensuite.

## Contenu

- [ ] **[1.3.1 Architecture modulaire](1.3.1-architecture-modulaire/1.3.1-architecture-modulaire.md)**
      — briques enfichables : client LLM, outils, boucle, mémoire,
      retrieval, evals
- [ ] **[1.3.2 Clean code production-grade](1.3.2-clean-code-production-grade/1.3.2-clean-code-production-grade.md)**
      — typing, Pydantic, pytest, packaging, docstrings
- [ ] **[1.3.3 Évolutivité sans friction](1.3.3-evolutivite-sans-friction/1.3.3-evolutivite-sans-friction.md)**
      — ajouter un outil/provider/agent = un fichier, zéro modification
      du cœur
- [ ] **[1.3.4 Routage multi-agentique](1.3.4-routage-multi-agentique/1.3.4-routage-multi-agentique.md)**
      — superviseur/ouvriers, routage coût/latence/qualité
- [ ] **[1.3.5 Dogfooding](1.3.5-dogfooding/1.3.5-dogfooding.md)**
      — les modules 2-7 consomment le framework et le font évoluer
- [ ] **[1.3.6 Sortie précoce et semver](1.3.6-sortie-precoce-semver/1.3.6-sortie-precoce-semver.md)**
      — 0.0.1 dès les premières briques promues (client LLM, outils,
      `rag_commun`)

## Synthèse

Le framework est le point où tout le parcours **se recompose** : chaque
script du socle devient une brique, chaque brique un module enfichable,
chaque module suivant un consommateur qui teste l'architecture en
conditions réelles. Si ajouter un provider coûte plus qu'un fichier,
l'architecture a échoué — c'est le critère. **Auto-contrôle** : savoir
défendre chaque choix d'architecture face à « pourquoi pas LangChain ? »
(réponse : parce qu'on sait exactement ce qu'il ferait, et ce qu'il
cacherait).

## Livrable

Le framework, packagé et versionné semver — première release 0.0.1 dès
les premières briques promues, puis évolution incrémentale.
