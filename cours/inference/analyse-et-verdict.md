# Analyse et verdict

> [carte du cours](../carte.md)

## Vue d'ensemble

Expliquer les chiffres, pas seulement les produire — puis trancher.
Les courbes de la [4.2](benchmark.md)
s'expliquent par trois mécanismes (batching continu, KV cache,
PagedAttention) qu'il faut savoir raconter ; le verdict traduit ensuite
la mécanique en règle de décision : quand Ollama suffit, quand vLLM se
justifie.

## Contenu

- **[4.3.1 Mécanismes vLLM](mecanismes-vllm.md)**
      — batching continu, KV cache, PagedAttention
- **[4.3.2 Verdict Ollama vs vLLM](verdict-ollama-vs-vllm.md)**
      — quand l'un suffit, quand l'autre se justifie

## Synthèse

Le module se referme en boucle complète : déployer
([4.1](deploiement.md)) → mesurer
([4.2](benchmark.md)) →
expliquer → décider. C'est la démarche d'ingénierie infra en
miniature, et elle produit un discours d'entretien complet : « voici
mes courbes, voici pourquoi elles ont cette forme, voici ma règle de
décision ». **Auto-contrôle** : savoir expliquer chaque cassure de
courbe par son mécanisme.

## Livrable du module

Post de blog / README `04-ollama-vs-vllm-bench` avec les chiffres.
**CV** : « deployed and benchmarked vLLM vs Ollama on consumer GPU ».
