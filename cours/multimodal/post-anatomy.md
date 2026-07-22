# 7.1.2 Post « anatomy of a fully local voice assistant »

> **Leçon de la section [7.1 Documenter l'existant](../7.1-documenter-existant.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Transformer l'[étude de cas](../7.1.1-etude-de-cas-stt-tts/7.1.1-etude-de-cas-stt-tts.md)
en **post public** : « anatomy of a fully local voice assistant ». Le
sujet est rare (peu de gens font tourner un assistant vocal 100 %
local et savent le mesurer) — donc parfait pour le portfolio
([P.2](../../../transverse-portfolio/p.2-ecrire/p.2-ecrire.md)).

## Le savoir

- **L'angle qui accroche** : « fully local » — pas d'API cloud, pas de
  données qui sortent. C'est l'argument souveraineté/confidentialité
  ([roadmap §10.3](../../../roadmap.md)) rendu concret et démontrable.
- **La structure du post** (le canon README du parcours,
  [P.1.1](../../../transverse-portfolio/p.1-repos-publics/p.1.1-github-public/p.1.1-github-public.md)) :
  problème (un assistant vocal sans cloud) → architecture (le schéma de
  la chaîne) → **métriques** (le tableau de latences, le nerf du post)
  → décisions et arbitrages → « ce que je referais autrement ».
- **Le public visé** : les recruteurs AI Engineer *et* la communauté
  r/LocalLLaMA ([roadmap §7](../../../roadmap.md)) — écrire en anglais,
  montrer les chiffres, publier le schéma.
- **La discipline anti-hype** : des latences mesurées battent des
  adjectifs. Le post vaut par ses nombres et son honnêteté (ce qui
  cloche, ce qui a été dur) — pas par les superlatifs.
- **Le réemploi** : ce post est le **gabarit** des autres posts du
  parcours (un par module, [P.2.1](../../../transverse-portfolio/p.2-ecrire/p.2.1-un-post-par-module/p.2.1-un-post-par-module.md)) —
  le premier bien fait sert de moule.

## En pratique

Rédiger le post (blog perso ou dev.to), schéma de la chaîne inclus,
tableau de latences de la [7.1.1](../7.1.1-etude-de-cas-stt-tts/7.1.1-etude-de-cas-stt-tts.md),
section « would do differently » — relu par un anglophone, publié, lié
depuis le portfolio.

## Pièges connus

- Le post sans chiffres : « c'est rapide » n'apprend rien — le tableau
  de latences est la raison d'être du post.
- Trop de détails homelab (IP, topologie, famille) : version publique
  expurgée, comme le reste du portfolio
  ([P.1.1](../../../transverse-portfolio/p.1-repos-publics/p.1.1-github-public/p.1.1-github-public.md)).
- Attendre la perfection pour publier : un post « qui tourne » et
  daté bat un brouillon parfait jamais sorti — le principe de
  [sortie précoce](../../../01-llm-from-scratch/1.3-framework-maison/1.3.6-sortie-precoce-semver/1.3.6-sortie-precoce-semver.md)
  vaut aussi pour l'écriture.

## Question d'entretien

> « Parlez-moi d'un contenu technique que vous avez publié. »
> « Anatomy of a fully local voice assistant » : l'architecture STT →
> LLM → TTS, les latences mesurées brique par brique, les arbitrages
> sur 6 Go de VRAM, et ce que je referais — un post à montrer, pas à
> résumer.

## Références

- [P.2.1 Un post par module](../../../transverse-portfolio/p.2-ecrire/p.2.1-un-post-par-module/p.2.1-un-post-par-module.md)
  — la stratégie d'écriture
- r/LocalLLaMA, dev.to — les canaux
