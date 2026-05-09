## Références

- [Su et al., *RoFormer: Enhanced Transformer with Rotary Position Embedding*,
  v5](https://arxiv.org/abs/2104.09864) — formulation et propriétés de RoPE.
- [Transformers — implémentation Llama, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  calcul des fréquences, rotation de `Q` et `K`, position du cache.
- [Transformers — RoPE utilities](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py) —
  variantes configurables et validation.
