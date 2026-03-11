# LLM-as-judge

> [carte du cours](../carte.md)

## L'essentiel

Les scores déterministes de la
[evals du RAG](../retrieval/evals.md)
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
  ([structured output](../fondamentaux/structured-output.md)) :
  `{score: int, justification: str}` par axe.
- **Les biais documentés du juge** — les connaître est la moitié de la
  compétence :
  - **auto-préférence** : un modèle sur-note ses propres sorties →
    d'où juge ≠ générateur (biais d'auto-évaluation, nommé dans le
    [sommaire](../carte.md)) ;
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
[backend commutable](providers.md) ;
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

## Se tester

> « Quelles limites au LLM-as-judge, et comment les gérez-vous ? »
> Biais d'auto-préférence (juge ≠ générateur), verbosité, position,
> échelle mal ancrée — mitigés par rubrique explicite, ordre
> randomisé, sortie contrainte, et calibration contre un échantillon
> noté humain.

## Références

- Zheng et al., « Judging LLM-as-a-Judge » (MT-Bench) — les biais
  mesurés
