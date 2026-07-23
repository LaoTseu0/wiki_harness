# Charge concurrente

> [carte du cours](../carte.md)

## L'essentiel

À une requête, Ollama et vLLM se ressemblent ; à vingt, ils divergent —
c'est **la** mesure du module. Un script de charge maison (asyncio +
httpx) envoie 1, 5 puis 20 requêtes simultanées aux deux moteurs et
trace ce que chacun fait de la file.

## Le savoir

- **Pourquoi la concurrence discrimine** : Ollama traite peu de
  requêtes en parallèle (`OLLAMA_NUM_PARALLEL`, faible par défaut) et
  fait patienter le reste — le TTFT des requêtes en file **explose
  linéairement**. vLLM insère chaque nouvelle requête dans le batch en
  cours (batching continu,
  [mécanismes vLLM](mecanismes-vllm.md)) :
  le débit **agrégé** grimpe, au prix d'une érosion progressive des
  tokens/s par requête.
- **Le scénario de charge** : n workers async lancés en salve, chacun
  mesurant ses métriques ([métriques : débit et latence](metriques-debit-latence.md)) ;
  prompts réalistes légèrement variés (éviter de mesurer le
  [prompt caching](prompt-caching.md)
  à son insu) ; n ∈ {1, 5, 20}, plusieurs salves par point.
- **Ce qu'on lit dans les courbes attendues** :
  - TTFT p95 vs n : plat puis mur chez Ollama (la file), dégradation
    douce chez vLLM ;
  - débit agrégé vs n : plafonne vite chez Ollama, croît chez vLLM
    jusqu'à saturation du KV cache (6 Go — le mur arrive tôt,
    [vLLM sur RTX 2060](vllm-sur-rtx-2060.md)) ;
  - à surveiller : préemptions/évictions vLLM quand le cache sature
    (visibles dans ses logs/metrics).
- **Asyncio, pas threads** : la charge est de l'I/O pur (attendre des
  streams) — `asyncio.gather` de n coroutines httpx est exact et
  léger ; c'est aussi une leçon Python du parcours.

## En pratique

`charge.py` : paramètres (URL, n, salves, prompt), workers async,
sortie JSON brute par requête, agrégation séparée, courbes générées
(matplotlib suffit) — les trois courbes du README : TTFT p95, tokens/s
par requête, débit agrégé, en fonction de n.

## Pièges connus

- Lancer le bench depuis une machine au réseau instable : le réseau
  entre dans la mesure — bencher depuis le LAN du homelab, le noter.
- Salve unique par point : la variance à n=20 est énorme — plusieurs
  salves, et les distributions plutôt qu'un chiffre.
- Laisser l'autre moteur chargé en VRAM pendant le bench : 6 Go
  partagés faussent tout — un moteur à la fois, vérifié par
  `nvidia-smi`.

## Se tester

> « Comment se comporte votre serveur à 20 utilisateurs
> simultanés ? »
> La réponse est une courbe, pas un chiffre : TTFT p95 et débit agrégé
> en fonction de la concurrence, point de saturation identifié (KV
> cache), et la différence de stratégie file d'attente vs batching
> continu — mesurée sur mon propre matériel.

## Références

- `asyncio` + httpx (streams concurrents)
- Doc vLLM : metrics et scheduling (préemptions)
