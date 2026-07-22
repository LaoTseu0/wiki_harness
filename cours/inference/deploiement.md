# Déploiement

> [carte du cours](../carte.md)

## Vue d'ensemble

Faire tourner un serveur d'inférence de **production** sur du matériel
grand public — et découvrir ce que « servir un modèle » veut dire
au-delà d'Ollama : la VRAM se budgète, le modèle se choisit quantisé,
et le serveur se règle. Une seule leçon, dense : le déploiement est le
prérequis des mesures de la
[4.2](benchmark.md).

## Contenu

- **[4.1.1 vLLM sur RTX 2060](vllm-sur-rtx-2060.md)**
      — conteneur, petit modèle adapté aux 6 Go, endpoint
      OpenAI-compatible

## Synthèse

À la fin de cette section, deux moteurs servent le même modèle sur la
même carte : Ollama (celui du quotidien) et vLLM (celui de la
production). Tout le reste du module est une comparaison instrumentée
entre les deux — le déploiement n'est donc pas un but, c'est le montage
de l'expérience. **Auto-contrôle** : savoir décomposer où partent les
6 Go de VRAM (poids + KV cache + activations).

## Références

- [Roadmap couche 1](../_archive/roadmap.md) — le tableau des moteurs
  d'inférence
