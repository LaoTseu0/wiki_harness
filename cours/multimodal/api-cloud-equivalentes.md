# API cloud équivalentes

> [carte du cours](../carte.md)

## L'essentiel

Savoir faire en local ne dispense pas de savoir **situer** ce que le
cloud fait : les offres attendent qu'on connaisse les API multimodales
managées (vision, images, audio). La leçon est une carte — de nom, avec
l'arbitrage local/cloud, pas un chantier d'intégration.

## Le savoir

- **Vision (comprendre l'image)** : GPT (OpenAI), Claude (Anthropic),
  Gemini (Google) — tous acceptent des images en entrée, plus capables
  qu'un VLM 6 Go local ([7.2.1](vlm-local.md)),
  mais **les données sortent**.
- **Génération d'images** : DALL-E (OpenAI), Nano Banana (Google),
  Stable Diffusion (ouvert, self-hostable) — l'inverse de la vision
  (texte → image) ; à connaître de nom, hors périmètre local du
  homelab (VRAM).
- **Audio** : Whisper API (STT managé — le pendant cloud de notre
  [Whisper local](etude-de-cas-stt-tts.md)),
  TTS cloud (OpenAI, ElevenLabs) — plus de voix, meilleure qualité,
  mais latence réseau et données qui sortent.
- **Le support des frameworks** : LangChain/LlamaIndex abstraient le
  multimodal (mêmes interfaces, providers cloud ou locaux) — le
  [backend commutable](../retrieval/backend-commutable.md)
  du module 2 est exactement ce raisonnement, étendu aux modalités.
- **L'arbitrage, toujours le même** ([roadmap couche M](../_archive/roadmap.md)) :
  local pour la confidentialité/coût/souveraineté (l'ADN homelab),
  cloud pour la capacité de pointe et le zéro-ops — et le
  [routage](../framework/routage-multi-agentique.md)
  peut mêler les deux par modalité et sensibilité.

## En pratique

Une page de synthèse (README module 7 ou veille Obsidian) : tableau
modalité × provider local × provider cloud × quand choisir quoi —
révisée à la veille ([roadmap §7](../_archive/roadmap.md)), pas un
développement.

## Pièges connus

- Confondre les modalités : « vision » = comprendre une image ≠
  « génération d'images » = en produire — deux marchés, deux familles
  d'API.
- RécITER des noms sans l'arbitrage : l'entretien veut « quand
  local/quand cloud », pas un catalogue.
- Envoyer des données sensibles à une API pour la démo : même en
  culture cloud, le réflexe confidentialité reste (données jouet
  uniquement).

## Se tester

> « Quelles solutions cloud pour le multimodal, et quand les
> préférer ? »
> Vision GPT/Claude/Gemini, génération DALL-E/Nano Banana/SD, audio
> Whisper API/TTS cloud — plus capables et zéro-ops, mais données
> sortantes ; local pour confidentialité/coût, cloud pour la pointe,
> et un routage par sensibilité entre les deux.

## Références

- [Roadmap couche M](../_archive/roadmap.md) — implémentation API à
  connaître de nom
- [2.4.2 Backend commutable](../retrieval/backend-commutable.md)
  — le même arbitrage local/cloud, côté texte
