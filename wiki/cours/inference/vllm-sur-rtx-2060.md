# vLLM sur RTX 2060

> [carte du cours](../carte.md)

## L'essentiel

vLLM est le serveur d'inférence des offres « LLM infra » : pensé pour
servir **N utilisateurs concurrents** sur GPU (batching continu,
PagedAttention — mécanismes détaillés en
[mécanismes vLLM](mecanismes-vllm.md)).
Le défi ici est assumé : le faire tenir sur une RTX 2060 à **6 Go** —
contrainte qui force à comprendre chaque mégaoctet.

## Le savoir

- **Le budget VRAM, à savoir décomposer** :
  `VRAM = poids du modèle + KV cache + activations/overhead`.
  Sur 6 Go : un modèle ~3B quantisé (AWQ/GPTQ 4-bit ≈ 2-2,5 Go) laisse
  ~3 Go de KV cache ; un 7-8B même quantisé (~4,5 Go) n'en laisse
  presque plus — or **le KV cache, c'est la concurrence** (chaque
  requête active y vit). Servir, c'est arbitrer poids contre cache.
- **Les flags qui comptent** :
  - `--gpu-memory-utilization` (≈ 0,90) : la fraction de VRAM que vLLM
    s'autorise — il **préalloue** le KV cache dedans ;
  - `--max-model-len` : longueur max de contexte — dimensionne le
    cache par requête ; la réduire (ex. 4096) multiplie les requêtes
    simultanées possibles ;
  - `--quantization awq` (ou modèle pré-quantisé GPTQ/AWQ) ;
  - `--max-num-seqs` : plafond de séquences en batch.
- **Différence de philosophie avec Ollama** : Ollama charge/décharge à
  la demande (confort mono-usager, GGUF/CPU-friendly) ; vLLM
  **préalloue et occupe** la carte (rendement multi-usagers). Les deux
  exposent une API **OpenAI-compatible** — notre
  [backend commutable](../framework/providers.md)
  bascule sans changer de code (le dogfooding du framework en action).
- **Déploiement homelab** : image officielle `vllm/vllm-openai`,
  runtime nvidia, port 8000 — un conteneur de plus, mais qui
  monopolise le GPU : Ollama et vLLM ne tournent pas en même temps sur
  6 Go (à orchestrer pour le bench).

## En pratique

Compose avec runtime nvidia, un modèle 3B instruct quantisé AWQ,
`--max-model-len 4096` ; validation : `curl /v1/models`, une
complétion, `nvidia-smi` pour lire l'occupation — noter chaque chiffre,
ils alimentent le [README du bench](verdict-ollama-vs-vllm.md).

## Pièges connus

- OOM au démarrage avec un modèle « qui devrait rentrer » : la
  préallocation du KV cache est comprise dedans — baisser
  `--max-model-len` ou `gpu-memory-utilization` avant de changer de
  modèle.
- Comparer vLLM (modèle AWQ) à Ollama (GGUF q4_K_M) en croyant les
  quantisations équivalentes : formats différents, qualité proche mais
  pas identique — et plutôt que « le dire dans le README », le
  **mesurer** : rejouer le jeu d'evals du domaine retrieval sur les deux
  moteurs via le
  [backend commutable](../framework/providers.md) —
  l'écart de qualité devient une ligne de tableau, pas une note de
  bas de page.
- Oublier qu'une carte de 2019 (Turing) n'a pas toutes les
  optimisations récentes : certaines options (FP8, etc.) sont
  indisponibles — vérifier les logs de démarrage.

## Se tester

> « Que faut-il pour servir un LLM 7B à une équipe ? »
> Budget VRAM décomposé (poids quantisés + KV cache × concurrence
> cible), un serveur à batching continu (vLLM), max-model-len
> dimensionné à l'usage, API OpenAI-compatible pour l'intégration — et
> des mesures de charge avant la promesse
> ([charge concurrente](charge-concurrente.md)).

## Références

- Doc vLLM : engine args, quantization, OpenAI server
