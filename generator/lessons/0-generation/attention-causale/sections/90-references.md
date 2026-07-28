## Références

- [Vaswani et al., *Attention Is All You Need*, v7](https://arxiv.org/abs/1706.03762) —
  scaled dot-product attention et multi-head attention.
- [Ainslie et al., *GQA: Training Generalized Multi-Query Transformer Models
  from Multi-Head Checkpoints*, v2](https://arxiv.org/abs/2305.13245) —
  partage des clés et valeurs entre groupes de requêtes.
- [Transformers — implémentation Llama, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) —
  projections, masque, scaling, **softmax** et répétition des groupes KV.
