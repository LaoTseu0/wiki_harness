## Références

- [Holtzman et al., *The Curious Case of Neural Text Degeneration*,
  v2](https://arxiv.org/abs/1904.09751) — nucleus sampling.
- [Nguyen et al., *Turning Up the Heat: Min-p Sampling*, v2](https://arxiv.org/abs/2407.01082) —
  seuil relatif au candidat maximal.
- [Keskar et al., *CTRL*, v2](https://arxiv.org/abs/1909.05858) — repetition
  penalty.
- [Transformers — `GenerationConfig`, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig) —
  paramètres de **température**, **top-k**, **top-p**, **min-p** et répétition.
- [Transformers — `logits_process.py`, révision `main` vérifiée le
  2026-07-27](https://github.com/huggingface/transformers/blob/main/src/transformers/generation/logits_process.py) —
  formules d'implémentation et garanties minimales.
