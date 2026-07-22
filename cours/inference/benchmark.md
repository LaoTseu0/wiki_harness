# 4.2 Benchmark documenté vs Ollama

> **Module 4 — 04-ollama-vs-vllm-bench** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md)
> **Statut** : ⚪ à venir · **Passage** : parallélisable
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Chiffrer, pas ressentir : les mêmes prompts, les deux moteurs, des
métriques comparables. La section définit d'abord **quoi** mesurer
(débit, latence premier token — deux choses différentes que les
vendeurs confondent volontiers), puis **comment** charger (1/5/20
requêtes concurrentes, script maison) — c'est la montée en concurrence
qui sépare vraiment les deux moteurs.

## Contenu

- [ ] **[4.2.1 Métriques : débit et latence](4.2.1-metriques-debit-latence/4.2.1-metriques-debit-latence.md)**
      — tokens/s, latence premier token (TTFT)
- [ ] **[4.2.2 Charge concurrente](4.2.2-charge-concurrente/4.2.2-charge-concurrente.md)**
      — 1 / 5 / 20 requêtes, script de charge maison

## Synthèse

Un benchmark honnête tient en trois disciplines : des métriques
définies avant de mesurer (4.2.1), une charge réaliste et reproductible
(4.2.2), et les conditions publiées avec les chiffres (modèle,
quantisation, contexte, matériel). Le résultat attendu n'est pas un
vainqueur mais une **courbe** : à 1 requête les moteurs se valent, à 20
ils racontent deux philosophies — l'explication arrive en
[4.3](../4.3-analyse-et-verdict/4.3-analyse-et-verdict.md).
**Auto-contrôle** : savoir dire pourquoi « X tokens/s » ne veut rien
dire sans le nombre de requêtes concurrentes.

## Références

- Le script de charge : livrable de la section, versionné dans ce
  module
