# 7.2 Vision locale

> **Module 7 — 07-multimodal** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md)
> **Statut** : ⚪ à venir · **Passage** : après le module 2,
> parallélisable ensuite
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Ajouter la **vision** à l'acquis vocal : un VLM (vision-language model)
local sur la RTX 2060, et la mesure honnête de ce qui rentre en 6 Go.
Une leçon, dans la continuité directe du module 4 (budget VRAM) et du
module 1 (mêmes appels, une image en plus dans le message).

## Contenu

- [ ] **[7.2.1 VLM local](7.2.1-vlm-local/7.2.1-vlm-local.md)**
      — Qwen-VL ou LLaVA sur la RTX 2060 : décrire, lire un scan,
      mesurer les 6 Go

## Synthèse

La vision complète la trilogie multimodale du CV (STT, TTS, vision) sur
un seul matériel grand public. Techniquement, c'est le
[function calling](../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md)
et le budget VRAM ([4.1.1](../../04-ollama-vs-vllm-bench/4.1-deploiement/4.1.1-vllm-sur-rtx-2060/4.1.1-vllm-sur-rtx-2060.md))
déjà connus, appliqués à un modèle qui « voit ». **Auto-contrôle** :
savoir dire quel VLM tient en 6 Go, à quelle résolution d'image, et ce
que ça coûte en latence.

## Références

- [Roadmap couche M](../../roadmap.md) — VLM locaux via Ollama
