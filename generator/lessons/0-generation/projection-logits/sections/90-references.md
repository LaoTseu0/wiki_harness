## Références

- [Vaswani et al., *Attention Is All You Need*, v7](https://arxiv.org/abs/1706.03762) —
  projection linéaire et softmax de sortie.
- [Press et Wolf, *Using the Output Embedding to Improve Language Models*,
  v3](https://arxiv.org/abs/1608.05859) — partage des **embeddings** d'entrée et de
  sortie.
- [Transformers — implémentation `LlamaForCausalLM`, révision `main` vérifiée
  le 2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  normalisation finale, `lm_head` et sélection des **logits**.
