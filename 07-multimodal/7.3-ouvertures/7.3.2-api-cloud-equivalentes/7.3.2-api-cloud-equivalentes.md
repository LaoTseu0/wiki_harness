# 7.3.2 API cloud équivalentes

> **Leçon de la section [7.3 Ouvertures](../7.3-ouvertures.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir (culture)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Savoir faire en local ne dispense pas de savoir **situer** ce que le
cloud fait : les offres attendent qu'on connaisse les API multimodales
managées (vision, images, audio). La leçon est une carte — de nom, avec
l'arbitrage local/cloud, pas un chantier d'intégration.

## Le savoir

- **Vision (comprendre l'image)** : GPT (OpenAI), Claude (Anthropic),
  Gemini (Google) — tous acceptent des images en entrée, plus capables
  qu'un VLM 6 Go local ([7.2.1](../../7.2-vision-locale/7.2.1-vlm-local/7.2.1-vlm-local.md)),
  mais **les données sortent**.
- **Génération d'images** : DALL-E (OpenAI), Nano Banana (Google),
  Stable Diffusion (ouvert, self-hostable) — l'inverse de la vision
  (texte → image) ; à connaître de nom, hors périmètre local du
  homelab (VRAM).
- **Audio** : Whisper API (STT managé — le pendant cloud de notre
  [Whisper local](../../7.1-documenter-existant/7.1.1-etude-de-cas-stt-tts/7.1.1-etude-de-cas-stt-tts.md)),
  TTS cloud (OpenAI, ElevenLabs) — plus de voix, meilleure qualité,
  mais latence réseau et données qui sortent.
- **Le support des frameworks** : LangChain/LlamaIndex abstraient le
  multimodal (mêmes interfaces, providers cloud ou locaux) — le
  [backend commutable](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.2-backend-commutable/2.4.2-backend-commutable.md)
  du module 2 est exactement ce raisonnement, étendu aux modalités.
- **L'arbitrage, toujours le même** ([roadmap couche M](../../../roadmap.md)) :
  local pour la confidentialité/coût/souveraineté (l'ADN homelab),
  cloud pour la capacité de pointe et le zéro-ops — et le
  [routage](../../../01-llm-from-scratch/1.3-framework-maison/1.3.4-routage-multi-agentique/1.3.4-routage-multi-agentique.md)
  peut mêler les deux par modalité et sensibilité.

## En pratique

Une page de synthèse (README module 7 ou veille Obsidian) : tableau
modalité × provider local × provider cloud × quand choisir quoi —
révisée à la veille ([roadmap §7](../../../roadmap.md)), pas un
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

## Question d'entretien

> « Quelles solutions cloud pour le multimodal, et quand les
> préférer ? »
> Vision GPT/Claude/Gemini, génération DALL-E/Nano Banana/SD, audio
> Whisper API/TTS cloud — plus capables et zéro-ops, mais données
> sortantes ; local pour confidentialité/coût, cloud pour la pointe,
> et un routage par sensibilité entre les deux.

## Références

- [Roadmap couche M](../../../roadmap.md) — implémentation API à
  connaître de nom
- [2.4.2 Backend commutable](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.2-backend-commutable/2.4.2-backend-commutable.md)
  — le même arbitrage local/cloud, côté texte
