# Étude de cas STT/TTS

> [carte du cours](../carte.md)

## L'essentiel

Le pipeline vocal de Jarvis est du multimodal **de production** :
Whisper (speech-to-text) et Piper (text-to-speech) déjà acquis. La
leçon le décortique en étude de cas — latences par brique, modèles
choisis, streaming — pour savoir le raconter dans le vocabulaire des
offres.

## Le savoir

- **La chaîne de bout en bout** :
  `voix → VAD → Whisper (STT) → LLM → Piper (TTS) → audio`, et chaque
  brique a une **latence propre** qui se mesure :
  - **wake word** (reconnaître « Jarvis » — l'entrée du pipeline) et
    **VAD** (détecter le début et surtout la **fin** de parole) :
    deux mécanismes distincts, deux latences — c'est la fin de parole
    détectée par le VAD qui démarre le chrono de la latence perçue
    (et l'écoute déclenchée économise le GPU) ;
  - **Whisper (STT)** : audio → texte ; le compromis taille/latence/
    précision (tiny→large) est le même arbitrage que partout dans le
    parcours ;
  - **LLM** : le cœur déjà maîtrisé (domaine fondamentaux) ;
  - **Piper (TTS)** : texte → audio, **streamé** — la première syllabe
    sort avant la fin de la phrase, comme le
    [streaming de tokens](../fondamentaux/chat-historique-contexte.md)
    côté texte.
- **La métrique qui compte : la latence perçue** — le temps entre « fin
  de ma phrase » et « début de la réponse audio ». Le streaming Piper
  la réduit drastiquement (on n'attend pas la synthèse complète) —
  exactement l'analogue du TTFT
  ([métriques : débit et latence](../inference/metriques-debit-latence.md)).
- **Les termes du marché** :
  STT, TTS, VAD, streaming, latence de bout en bout — les mêmes qu'on
  emploie pour n'importe quel pipeline multimodal ; savoir les mapper
  sur Whisper/Piper est la compétence.
- **La contrainte partagée** : tout tourne en **local sur la RTX
  2060** — le pipeline vocal et la [vision](vlm-local.md)
  se disputent les mêmes 6 Go, ce qui se budgète.

## En pratique

Instrumenter le pipeline existant pour horodater chaque brique
(réutiliser l'esprit des [traces](../production/tracer-les-appels.md)),
produire un tableau de latences (médiane + p95), un schéma de la
chaîne, et la latence perçue avec/sans streaming Piper.

## Pièges connus

- Mesurer les briques isolément et sommer : les recouvrements
  (streaming, pipelining) font que le tout ≠ la somme — mesurer aussi
  le bout-en-bout réel.
- Oublier le VAD/wake word dans le budget : la latence perçue commence
  à la détection, pas à Whisper.
- Choisir Whisper large « pour la qualité » sans mesurer : sur 6 Go
  partagés, le modèle STT concurrence le LLM — l'arbitrage se chiffre.

## Se tester

> « Décrivez un pipeline multimodal que vous avez fait tourner. »
> Assistant vocal 100 % local : VAD → Whisper STT → LLM → Piper TTS
> streamé, latence perçue mesurée brique par brique, tout sur une RTX
> 2060 — et je peux détailler les arbitrages taille/latence de chaque
> maillon.

## Références

- Whisper (OpenAI) ; Piper (TTS local streamé)
- [architecture/jarvis.md](../../../../homelab/architecture/jarvis.md) —
  le pipeline vocal d'origine
