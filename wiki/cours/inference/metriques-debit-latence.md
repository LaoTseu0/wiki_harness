# Métriques : débit et latence

> [carte du cours](../carte.md)

## L'essentiel

Deux familles de métriques, deux expériences utilisateur : la **latence
du premier token** (TTFT — le chat « répond vite ») et le **débit de
génération** (tokens/s — la réponse « s'écrit vite »). Un serveur peut
exceller à l'une et décevoir à l'autre ; les confondre rend tout
benchmark illisible.

## Le savoir

- **Les deux phases d'une requête** (l'explication mécanique est en
  [mécanismes vLLM](mecanismes-vllm.md)) :
  - **prefill** : tout le prompt est traité d'un bloc (parallélisable,
    borné par le calcul) → détermine le **TTFT** ;
  - **decode** : les tokens sortent un à un (borné par la bande
    passante mémoire) → détermine les **tokens/s de génération**.
- **Les métriques à collecter, par requête** :
  - TTFT (ms) — horodater l'envoi et le premier chunk du stream ;
  - tokens/s de génération — tokens générés / (fin − premier token) ;
  - latence totale ;
  - et **côté système** : débit agrégé (tokens/s toutes requêtes
    confondues) — la métrique que la concurrence fera diverger.
- **La discipline statistique** : jamais une moyenne seule — médiane et
  **p95** (la queue de latence est ce que vivent les utilisateurs) ;
  n ≥ 10 mesures par point ; warm-up exclu (premier appel = chargement
  modèle chez Ollama).
- **Conditions à figer et publier** : même modèle (et quantisations
  notées — AWQ vs GGUF,
  [vLLM sur RTX 2060](vllm-sur-rtx-2060.md)),
  même longueur de prompt (le TTFT dépend du prompt), même
  `max_tokens`, température fixée, un moteur à la fois sur le GPU.

## En pratique

Module de mesure du script de charge : timestamps sur stream (httpx),
comptes de tokens depuis les réponses API, sortie JSON par requête
(brut conservé) + agrégats (médiane, p95) calculés à part — les bruts
permettent de recalculer sans re-mesurer.

## Pièges connus

- Mesurer les tokens/s en incluant le TTFT dans le dénominateur : les
  deux métriques se contaminent — séparer les phases dans le calcul.
- Prompts de tailles différentes entre moteurs (templates de chat
  divergents) : le prefill n'est plus comparable — compter les tokens
  du prompt *rendus par chaque API* et le vérifier.
- Le premier appel Ollama inclut le chargement du modèle : warm-up
  systématique avant mesure.

## Se tester

> « Quelles métriques pour évaluer un serveur d'inférence ? »
> TTFT (expérience d'attente), tokens/s par requête (expérience de
> lecture), débit agrégé (capacité), médiane + p95, sous une
> concurrence donnée — et les conditions publiées, sinon le chiffre ne
> se compare à rien.

## Références

- [Mécanismes vLLM](mecanismes-vllm.md)
  — prefill/decode expliqués
- Doc métriques vLLM (`/metrics`, Prometheus) — pour croiser nos
  mesures
