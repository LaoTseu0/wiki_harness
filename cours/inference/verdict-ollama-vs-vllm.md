# 4.3.2 Verdict Ollama vs vLLM

> **Leçon de la section [4.3 Analyse et verdict](../4.3-analyse-et-verdict.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Le livrable final : une **règle de décision** défendable, écrite —
quand Ollama suffit, quand vLLM se justifie. Pas de vainqueur
absolu : deux outils pour deux problèmes, et la maturité consiste à
refuser le faux duel.

## Le savoir

- **Quand Ollama suffit** :
  - un ou deux utilisateurs, usage interactif (le homelab au
    quotidien) ;
  - besoin de *commodité* : pull de modèles, GGUF, déchargement
    automatique, CPU possible ;
  - matériel modeste où la simplicité prime sur le rendement ;
  - c'est le choix du parcours pour apprendre — et il reste le bon
    pour cet usage.
- **Quand vLLM se justifie** :
  - **concurrence réelle** (une équipe, un service public interne) :
    le débit agrégé et le TTFT sous charge sont sans appel
    ([4.2.2](../../4.2-benchmark-vs-ollama/4.2.2-charge-concurrente/4.2.2-charge-concurrente.md)) ;
  - besoin de rendement par euro de GPU (batching continu,
    PagedAttention — [4.3.1](../4.3.1-mecanismes-vllm/4.3.1-mecanismes-vllm.md)) ;
  - production outillée : métriques Prometheus, déploiement k8s — le
    monde des offres « LLM infra ».
  - Coûts associés à assumer : préallocation VRAM (la carte est
    occupée), pas de va-et-vient de modèles, exigence GPU.
- **La zone grise, à trancher par les chiffres** : notre RTX 2060 en
  est une — vLLM y apporte la tenue de charge mais le KV cache de
  6 Go borne vite la fête ; à ~5 utilisateurs c'est déjà pertinent, à
  1 c'est du sur-engineering.
- **La structure du post/README** (« un README qui tourne »,
  [P.2.1](../../../transverse-portfolio/p.2-ecrire/p.2.1-un-post-par-module/p.2.1-un-post-par-module.md)) :
  question → montage ([4.1.1](../../4.1-deploiement/4.1.1-vllm-sur-rtx-2060/4.1.1-vllm-sur-rtx-2060.md))
  → métriques ([4.2.1](../../4.2-benchmark-vs-ollama/4.2.1-metriques-debit-latence/4.2.1-metriques-debit-latence.md))
  → courbes → mécanismes → règle de décision. Les chiffres d'abord,
  l'opinion en conclusion.

## En pratique

Rédiger le verdict en ~15 lignes dans le README anglais du module,
avec la règle en gras et les trois courbes en preuve ; relire en se
demandant : « un lead infra qui lit ça peut-il décider ? ».

## Pièges connus

- Le verdict militant (« vLLM écrase Ollama ») : les chiffres montrent
  un *régime* de supériorité, pas une supériorité — la nuance est la
  crédibilité.
- Généraliser depuis 6 Go : sur une carte de 24 Go le point de bascule
  se déplace — donner la règle *paramétrée* (concurrence, VRAM), pas
  le chiffre brut. Le homelab possède d'ailleurs le second point de
  mesure (jarvis-core, RTX 4090 24 Go) : deux points font une règle,
  un seul fait une conjecture — à bencher quand jarvis-core entre en
  service.
- Oublier les coûts d'exploitation dans la règle : la préallocation
  VRAM de vLLM interdit le multi-modèles à la Ollama — ça compte dans
  un homelab.

## Question d'entretien

> « Ollama ou vLLM pour notre équipe de 10 devs ? »
> Question de charge : 10 utilisateurs actifs → vLLM (batching
> continu, débit agrégé, métriques) sur un GPU dédié dimensionné KV
> cache compris ; Ollama reste l'outil des postes individuels — et
> voici mes courbes de bench pour situer le point de bascule.

## Références

- Les courbes du bench (ce module) — la preuve
- [Roadmap §3](../../../roadmap.md) — le profil « LLM Infra / MLOps
  GPU » que ce discours adresse
