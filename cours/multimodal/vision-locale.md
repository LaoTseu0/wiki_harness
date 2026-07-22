# Vision locale

> [carte du cours](../carte.md)

## Vue d'ensemble

Ajouter la **vision** à l'acquis vocal : un VLM (vision-language model)
local sur la RTX 2060, et la mesure honnête de ce qui rentre en 6 Go.
Une leçon, dans la continuité directe du module 4 (budget VRAM) et du
module 1 (mêmes appels, une image en plus dans le message).

## Contenu

- **[7.2.1 VLM local](vlm-local.md)**
      — Qwen-VL ou LLaVA sur la RTX 2060 : décrire, lire un scan,
      mesurer les 6 Go

## Synthèse

La vision complète la trilogie multimodale du CV (STT, TTS, vision) sur
un seul matériel grand public. Techniquement, c'est le
[function calling](../fondamentaux/function-calling.md)
et le budget VRAM ([4.1.1](../inference/vllm-sur-rtx-2060.md))
déjà connus, appliqués à un modèle qui « voit ». **Auto-contrôle** :
savoir dire quel VLM tient en 6 Go, à quelle résolution d'image, et ce
que ça coûte en latence.

## Références

- [Roadmap couche M](../_archive/roadmap.md) — VLM locaux via Ollama
