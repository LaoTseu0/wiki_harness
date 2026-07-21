# 6.3.1 LoRA sur Colab

> **Leçon de la section [6.3 Culture fine-tuning](../6.3-culture-fine-tuning.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir (option, culture)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Faire *un* fine-tuning LoRA, une fois, sur un petit modèle et un GPU
gratuit (Colab) — pour transformer la connaissance théorique
([1.2.6](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.6-lora/1.2.6-lora.md))
en vécu chiffré. Objectif : savoir en parler en entretien avec des
nombres réels, pas devenir ML Engineer (ce n'est pas le
[métier visé](../../../roadmap.md)).

## Le savoir

- **Le pipeline minimal** : dataset (quelques centaines d'exemples au
  format chat) → `PEFT` + `bitsandbytes` (QLoRA 4-bit) → entraînement
  quelques epochs → adaptateur (~dizaines de Mo) → inférence base +
  adaptateur. La mécanique (rang, α, matrices A·B) est dans
  l'[entrée glossaire](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.6-lora/1.2.6-lora.md).
- **La bonne tâche pour la démo** : du **style/format**, pas des faits
  — apprendre au modèle à répondre dans un format fixe (ton, structure
  JSON récurrente), là où le fine-tuning a un sens réel. Prendre une
  tâche « connaissance » ne ferait que démontrer par l'échec pourquoi
  le RAG existe.
- **Ce qu'on mesure et retient** : temps réel (minutes-heures sur T4
  gratuit), taille du dataset qui commence à marcher, avant/après sur
  un petit jeu de test — et la **fragilité** (oubli catastrophique si
  on pousse, sensibilité au template d'inférence).
- **Le coût total honnête** : dataset propre (le vrai travail, souvent
  des jours), itérations d'entraînement, evals pour valider — à
  comparer à « écrire un bon prompt système » (minutes). C'est ce
  ratio qui justifie l'ordre prompt → few-shot → RAG → fine-tuning
  ([2.3.5](../../../02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3.5-rag-vs-fine-tuning/2.3.5-rag-vs-fine-tuning.md)).
- **Le lien homelab** : l'adaptateur pourrait se servir via vLLM
  ([4.1.1](../../../04-ollama-vs-vllm-bench/4.1-deploiement/4.1.1-vllm-sur-rtx-2060/4.1.1-vllm-sur-rtx-2060.md),
  qui charge des LoRA) — à mentionner, pas forcément à faire.

## En pratique

Un notebook Colab documenté (dataset jouet de style, QLoRA, avant/après
mesuré), résumé en un README + remontée en
[entrée glossaire](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.6-lora/1.2.6-lora.md) :
coût réel, ce que ça a changé, la conclusion « pourquoi RAG d'abord ».

## Pièges connus

- Fine-tuner pour injecter des connaissances et « prouver » que le
  fine-tuning marche : on prouve surtout qu'on aurait dû faire un RAG.
- Négliger le template de chat à l'inférence : l'adaptateur semble
  cassé alors que le format d'entrée ne correspond pas à
  l'entraînement.
- Sur-entraîner : le petit modèle apprend par cœur le dataset et perd
  ses capacités générales — l'oublier, c'est la moitié de la leçon.

## Question d'entretien

> « Avez-vous déjà fine-tuné un modèle, et qu'en retenez-vous ? »
> Un QLoRA de style sur Colab : rapide côté GPU, mais le coût réel est
> le dataset et les evals ; utile pour le format/ton, inutile pour les
> faits (RAG) — et j'ai le notebook et les chiffres pour le montrer.

## Références

- HF PEFT + bitsandbytes (QLoRA) ; Unsloth (pour situer les
  accélérateurs)
- [1.2.6 LoRA](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.6-lora/1.2.6-lora.md)
  — la théorie
