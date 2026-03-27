# VLM local

> [carte du cours](../carte.md)

## L'essentiel

Faire « voir » un modèle en local : un VLM (Qwen-VL ou LLaVA) via
Ollama sur la RTX 2060, pour décrire une photo ou lire un document
scanné. Techniquement, c'est un appel LLM avec une **image dans le
message** — la nouveauté est le budget VRAM (encodeur de vision en
plus) et les usages.

## Le savoir

- **Comment un VLM « voit »** : un **encodeur d'image** (type ViT)
  transforme l'image en tokens visuels, projetés dans l'espace du LLM ;
  le modèle traite ensuite texte et image dans la même séquence.
  Conséquence pratique : l'image **consomme des tokens** (souvent
  beaucoup, selon la résolution) — le budget contexte s'applique à la
  vision.
- **L'appel, familier** : même API que le chat, un champ `images` dans
  le message (base64 chez Ollama) — le
  [client LLM](../framework/architecture-modulaire.md)
  du framework s'étend d'un champ, pas d'un paradigme.
- **Le budget 6 Go** ([vLLM sur RTX 2060](../inference/vllm-sur-rtx-2060.md)) :
  poids du LLM + **encodeur de vision** + KV cache gonflé par les
  tokens visuels — un VLM 7B quantisé est serré ; mesurer ce qui tient
  et à quelle résolution d'image (réduire l'image réduit les tokens et
  la VRAM).
- **Les usages à démontrer** : description d'image (« qu'y a-t-il sur
  cette photo ? »), **OCR/lecture de document scanné** (le plus utile
  au homelab — documents famille vers le NAS,
  [caméra et OCR](camera-et-ocr.md)),
  extraction structurée depuis une image (VLM +
  [structured output](../fondamentaux/structured-output.md)).
- **Situer les API cloud** (culture,
  [API cloud équivalentes](api-cloud-equivalentes.md)) :
  vision GPT/Claude/Gemini — plus capables, mais les données sortent ;
  l'arbitrage local/cloud est le même que partout.

## En pratique

Puller un VLM (Qwen-VL ou LLaVA) via Ollama, script de description +
script d'OCR d'un document scanné, mesure VRAM (`nvidia-smi`) et
latence à deux résolutions d'image — tableau « ce qui tient en 6 Go ».

## Pièges connus

- Envoyer l'image en pleine résolution : explosion des tokens visuels
  et de la VRAM — redimensionner selon la tâche (l'OCR a besoin de
  netteté, la description non).
- Attendre d'un petit VLM local la qualité d'OCR d'un service dédié :
  mesurer, et pour du document critique, situer les alternatives (OCR
  spécialisé, API cloud).
- Oublier que le VLM et le pipeline vocal
  ([étude de cas STT/TTS](etude-de-cas-stt-tts.md))
  partagent les 6 Go : ils ne tournent pas forcément en même temps.

## Se tester

> « Avez-vous fait tourner un modèle de vision en local ? »
> Un VLM (Qwen-VL/LLaVA) sur RTX 2060 via Ollama : description et OCR
> de documents, image encodée en tokens visuels donc budget VRAM et
> contexte à gérer, résolution arbitrée par tâche — mesuré, avec les
> limites des 6 Go assumées.

## Références

- Qwen-VL / LLaVA (cartes modèles Ollama)
