# 2.3.2 LLM-as-judge

> **Leçon de la section [2.3 v0.0.3 — LlamaIndex + outillage standard](../2.3-v0.0.3-llamaindex-outillage-standard.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Les scores déterministes de la
[2.1.7](../../2.1-v0.0.1-rag-a-la-main/2.1.7-evals/2.1.7-evals.md)
plafonnent : « la réponse contient-elle les mots-clés » rate les bonnes
réponses reformulées. Un **LLM juge** note la qualité avec souplesse —
à condition de le calibrer, et de respecter la règle du module :
**juge ≠ générateur**, jamais Qwen3 4B jugeant Qwen3 4B.

## Le savoir

- **Le principe** : pour chaque question du jeu, le juge reçoit
  (question, réponse attendue, réponse produite, sources) et note
  selon une **rubrique explicite** — par axe, pas en vrac :
  exactitude, fidélité aux sources, complétude, abstention correcte.
  Sortie contrainte
  ([1.1.5](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.5-structured-output/1.1.5-structured-output.md)) :
  `{score: int, justification: str}` par axe.
- **Les biais documentés du juge** — les connaître est la moitié de la
  compétence :
  - **auto-préférence** : un modèle sur-note ses propres sorties →
    d'où juge ≠ générateur (biais d'auto-évaluation, nommé dans le
    [sommaire](../../../sommaire.md)) ;
  - **verbosité** : les réponses longues sur-notées ;
  - **position** : en comparaison A/B, le premier gagne plus souvent —
    randomiser l'ordre ;
  - **complaisance** : échelle 1-10 jamais utilisée en bas — préférer
    des rubriques binaires ou 1-4 ancrées (« 1 = contredit la
    source »).
- **Le choix du juge, documenté dans le README** : un modèle local
  *différent* (autre famille, si possible plus gros) ou une API cloud
  ponctuelle — arbitrage coût/qualité à expliciter. Hiérarchie des
  risques : la **capacité** du juge d'abord, l'identité ensuite — un
  juge faible d'une autre famille respecte la lettre de la règle et
  juge mal ; si un seul modèle fort est disponible, un auto-jugement
  à rubrique serrée et calibration renforcée (en le disant) vaut
  mieux qu'un petit juge « différent ». Dans tous les cas, c'est la
  calibration ci-dessous qui tranche.
- **Calibration** : noter à la main 10 réponses, comparer au juge —
  s'il diverge sur plus de 2, réécrire la rubrique (pas le juge). Le
  juge s'évalue aussi.
- **L'extension du jeu** : passer de 12 à ~30 questions — le juge rend
  le passage à l'échelle possible (noter 30×5 configs à la main ne
  l'est pas).

## En pratique

`juge.py` : rubrique par axe, sortie JSON contrainte, un modèle juge
distinct configuré via le
[backend commutable](../../2.4-service-et-craftsmanship/2.4.2-backend-commutable/2.4.2-backend-commutable.md) ;
étape de calibration sur 10 cas notés à la main, résultats dans le
README.

## Pièges connus

- Le juge qui voit la réponse attendue *mot pour mot* et exige la
  paraphrase exacte : la rubrique doit demander l'équivalence
  sémantique, pas la similarité de surface.
- Moyenner les axes en un score unique trop tôt : on perd le
  diagnostic (fidélité 4/4 mais complétude 1/4 = problème de
  retrieval, pas de grounding).
- Faire confiance au juge sans calibration : un juge non calibré est
  un générateur d'opinions à grande échelle.

## Question d'entretien

> « Quelles limites au LLM-as-judge, et comment les gérez-vous ? »
> Biais d'auto-préférence (juge ≠ générateur), verbosité, position,
> échelle mal ancrée — mitigés par rubrique explicite, ordre
> randomisé, sortie contrainte, et calibration contre un échantillon
> noté humain.

## Références

- Zheng et al., « Judging LLM-as-a-Judge » (MT-Bench) — les biais
  mesurés
- [Roadmap couche T](../../../roadmap.md) — les trois familles d'evals
