# Tableau final

> [carte du cours](../carte.md)

## L'essentiel

Le tableau v0.0.1 → v0.0.2 → v0.0.3 dans le README est **la pièce
maîtresse du module** : trois générations, un même jeu de questions,
des scores comparables. C'est l'artefact qui transforme « j'ai fait un
RAG » en « j'ai construit, mesuré et amélioré un RAG » — la différence
entre une démo et de l'ingénierie, visible en une image.

## Le savoir

- **La forme cible** (README, section Metrics) :

  | Génération | Stack | Retrieval | Génération | Halluc. | Latence |
  |---|---|---|---|---|---|
  | v0.0.1 | SQLite + brute force | 7/12 | 7/12 | 0 | réf. |
  | v0.0.2 | Qdrant + hybride + rerank + filtres | ? | ? | ? | ? |
  | v0.0.3 | LlamaIndex (même socle) | ? | ? | ? | ? |

  complété par : le jeu étendu (~30 questions,
  [LLM-as-judge](../framework/llm-as-judge.md)) et l'annexe
  RAGAS ([RAGAS / DeepEval](ragas-deepeval.md)).
- **Chaque chiffre a une histoire** : le tableau seul ne suffit pas —
  deux ou trois phrases par transition (« l'hybride a repêché les
  questions à termes exacts ; le re-ranking n'a rien apporté sur ce
  corpus, retiré »). Les échecs documentés valent autant que les
  gains : « ce que je referais autrement » est une section attendue
  du README.
- **L'hygiène de comparaison** : le cœur du jeu (12 questions) reste
  identique sur les trois générations ; les extensions sont marquées ;
  les configs sont rejouables depuis les tags git
  ([sortie précoce et semver](../framework/sortie-precoce-semver.md)).
- **Pourquoi c'est LE différenciateur** : la question d'entretien n°1
  (« comment évaluez-vous ? ») trouve ici une réponse *pointable* — un
  lien vaut mieux qu'un discours.

## En pratique

Générer le tableau depuis
[07_evals.py](../../etapes/retrieval/07_evals.py) (sortie
markdown), le coller daté dans le README anglais, avec le commentaire
de transition par génération — et le garder à jour à chaque tag.

## Pièges connus

- Le tableau sans commentaire : des chiffres muets n'apprennent rien à
  un recruteur pressé — deux phrases par ligne.
- Cacher une régression : un score qui baisse et s'explique (latence
  contre précision, par exemple) renforce la crédibilité ; un tableau
  trop parfait l'affaiblit.
- Le tableau généré à la main : recopier des chiffres, c'est en
  trahir un — la sortie markdown vient du script.

## Se tester

> « Montrez-moi comment votre système a progressé. »
> Le tableau : trois générations, même jeu, scores ventilés, deltas
> attribués technique par technique, échecs inclus — et l'URL du
> README en guise de réponse.

## Références

- [Evals comparatives](evals-comparatives.md)
  — la discipline d'ablation qui alimente ce tableau
