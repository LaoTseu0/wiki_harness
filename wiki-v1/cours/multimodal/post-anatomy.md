# Post « anatomy of a fully local voice assistant »

> [carte du cours](../carte.md)

## L'essentiel

Transformer l'[étude de cas](etude-de-cas-stt-tts.md)
en **post public** : « anatomy of a fully local voice assistant ». Le
sujet est rare (peu de gens font tourner un assistant vocal 100 %
local et savent le mesurer).

## Le savoir

- **L'angle qui accroche** : « fully local » — pas d'API cloud, pas de
  données qui sortent. C'est l'argument souveraineté/confidentialité
 rendu concret et démontrable.
- **La structure du post** (le canon README du parcours) :
  problème (un assistant vocal sans cloud) → architecture (le schéma de
  la chaîne) → **métriques** (le tableau de latences, le nerf du post)
  → décisions et arbitrages → « ce que je referais autrement ».
- **Le public visé** : les recruteurs AI Engineer *et* la communauté
  r/LocalLLaMA — écrire en anglais,
  montrer les chiffres, publier le schéma.
- **La discipline anti-hype** : des latences mesurées battent des
  adjectifs. Le post vaut par ses nombres et son honnêteté (ce qui
  cloche, ce qui a été dur) — pas par les superlatifs.
- **Le réemploi** : ce post est le **gabarit** des autres posts du
  parcours (un par module) —
  le premier bien fait sert de moule.

## En pratique

Rédiger le post (blog perso ou dev.to), schéma de la chaîne inclus,
tableau de latences de la [étude de cas STT/TTS](etude-de-cas-stt-tts.md),
section « would do differently » — relu par un anglophone, publié, lié
depuis le portfolio.

## Pièges connus

- Le post sans chiffres : « c'est rapide » n'apprend rien — le tableau
  de latences est la raison d'être du post.
- Trop de détails homelab (IP, topologie, famille) : version publique
  expurgée.
- Attendre la perfection pour publier : un post « qui tourne » et
  daté bat un brouillon parfait jamais sorti — le principe de
  [sortie précoce](../framework/sortie-precoce-semver.md)
  vaut aussi pour l'écriture.

## Se tester

> « Parlez-moi d'un contenu technique que vous avez publié. »
> « Anatomy of a fully local voice assistant » : l'architecture STT →
> LLM → TTS, les latences mesurées brique par brique, les arbitrages
> sur 6 Go de VRAM, et ce que je referais — un post à montrer, pas à
> résumer.

## Références

- r/LocalLLaMA, dev.to — les canaux
