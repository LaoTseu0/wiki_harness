# Benchmark documenté vs Ollama

> [carte du cours](../carte.md)

## Vue d'ensemble

Chiffrer, pas ressentir : les mêmes prompts, les deux moteurs, des
métriques comparables. La section définit d'abord **quoi** mesurer
(débit, latence premier token — deux choses différentes que les
vendeurs confondent volontiers), puis **comment** charger (1/5/20
requêtes concurrentes, script maison) — c'est la montée en concurrence
qui sépare vraiment les deux moteurs.

## Contenu

- **[Métriques : débit et latence](metriques-debit-latence.md)**
      — tokens/s, latence premier token (TTFT)
- **[Charge concurrente](charge-concurrente.md)**
      — 1 / 5 / 20 requêtes, script de charge maison

## Synthèse

Un benchmark honnête tient en trois disciplines : des métriques
définies avant de mesurer (4.2.1), une charge réaliste et reproductible
(4.2.2), et les conditions publiées avec les chiffres (modèle,
quantisation, contexte, matériel). Le résultat attendu n'est pas un
vainqueur mais une **courbe** : à 1 requête les moteurs se valent, à 20
ils racontent deux philosophies — l'explication arrive en
[analyse et verdict](analyse-et-verdict.md).
**Auto-contrôle** : savoir dire pourquoi « X tokens/s » ne veut rien
dire sans le nombre de requêtes concurrentes.

## Références

- Le script de charge : livrable de la section, versionné dans ce
  module
