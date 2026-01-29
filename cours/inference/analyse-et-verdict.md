# 4.3 Analyse et verdict

> **Module 4 — 04-ollama-vs-vllm-bench** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md)
> **Statut** : ⚪ à venir · **Passage** : parallélisable
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Expliquer les chiffres, pas seulement les produire — puis trancher.
Les courbes de la [4.2](../4.2-benchmark-vs-ollama/4.2-benchmark-vs-ollama.md)
s'expliquent par trois mécanismes (batching continu, KV cache,
PagedAttention) qu'il faut savoir raconter ; le verdict traduit ensuite
la mécanique en règle de décision : quand Ollama suffit, quand vLLM se
justifie.

## Contenu

- [ ] **[4.3.1 Mécanismes vLLM](4.3.1-mecanismes-vllm/4.3.1-mecanismes-vllm.md)**
      — batching continu, KV cache, PagedAttention
- [ ] **[4.3.2 Verdict Ollama vs vLLM](4.3.2-verdict-ollama-vs-vllm/4.3.2-verdict-ollama-vs-vllm.md)**
      — quand l'un suffit, quand l'autre se justifie

## Synthèse

Le module se referme en boucle complète : déployer
([4.1](../4.1-deploiement/4.1-deploiement.md)) → mesurer
([4.2](../4.2-benchmark-vs-ollama/4.2-benchmark-vs-ollama.md)) →
expliquer → décider. C'est la démarche d'ingénierie infra en
miniature, et elle produit un discours d'entretien complet : « voici
mes courbes, voici pourquoi elles ont cette forme, voici ma règle de
décision ». **Auto-contrôle** : savoir expliquer chaque cassure de
courbe par son mécanisme.

## Livrable du module

Post de blog / README `04-ollama-vs-vllm-bench` avec les chiffres.
**CV** : « deployed and benchmarked vLLM vs Ollama on consumer GPU ».
