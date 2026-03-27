# Caméra et OCR

> [carte du cours](../carte.md)

## L'essentiel

Rendre la [vision locale](vlm-local.md)
*utile* en la branchant sur la vraie maison : une caméra Home Assistant
qui alimente « Jarvis, décris ce que tu vois », et l'OCR des documents
famille vers le NAS. Le multimodal cesse d'être une démo et devient un
service.

## Le savoir

- **Caméra → VLM** : HA expose les flux/snapshots caméra ; le pattern —
  snapshot déclenché (mouvement, ou demande vocale via le
  [pipeline STT](etude-de-cas-stt-tts.md))
  → VLM local → description → réponse (vocale via Piper, ou
  notification HA). Toute la chaîne du domaine multimodal s'assemble ici.
- **OCR documents → NAS** : un dossier surveillé → VLM en mode OCR
  ([VLM local](vlm-local.md))
  → texte + métadonnées → indexable. Le lien fort : ces documents
  deviennent un **corpus RAG** (domaine retrieval) — l'OCR est un *ingesteur*
  pour le retrieval. La boucle multimodal → RAG se ferme.
- **Les garde-fous s'appliquent** : ces usages touchent des données
  **très** personnelles (caméra, documents famille) — moindre
  privilège ([conteneur et moindre privilège](../agent/conteneur-moindre-privilege.md)),
  local-first strict (aucune image ne sort), périmètres HA en liste
  blanche ([outil home_assistant](../agent/outil-home-assistant.md)).
  C'est précisément là que « fully local » n'est pas un slogan mais une
  exigence.
- **Le statut « bonus »** : ces ouvertures démontrent la vision
  produit ; elles ne sont pas sur le chemin critique de
  l'employabilité — à faire si le temps et l'envie suivent.

## En pratique

Un flux de bout en bout minimal : déclencheur (vocal ou mouvement) →
snapshot HA → VLM local → réponse ; et, séparément, un dossier surveillé
→ OCR → fichier texte prêt à indexer. Démo filmée courte pour le
portfolio.

## Pièges connus

- Traiter le flux vidéo en continu : coûteux et inutile — snapshots sur
  déclencheur, pas de streaming permanent.
- Laisser fuiter une image vers une API cloud « pour une meilleure
  description » : sur des données famille, c'est la ligne rouge —
  local strict.
- OCR sans validation : un VLM hallucine du texte **sans signal
  d'erreur** — il n'a pas de score de confiance calibré (contrairement
  à un OCR classique type Tesseract). Garde-fous réalistes : double
  passe (deux résolutions ou deux prompts, comparer les sorties),
  témoin OCR dédié sur les champs critiques, toute divergence →
  relecture humaine — et garder l'original, toujours.

## Se tester

> « Un exemple d'usage multimodal de bout en bout ? »
> Caméra HA → snapshot → VLM local → description vocale (Piper), et OCR
> de documents vers un corpus RAG interrogeable — 100 % local sur la
> RTX 2060, garde-fous stricts parce que les données sont familiales.

## Références

- Doc caméras Home Assistant (snapshots)
- [VLM local](vlm-local.md)
  · [Module 2 RAG](../retrieval/rag-a-la-main.md)
  (l'OCR alimente le retrieval)
