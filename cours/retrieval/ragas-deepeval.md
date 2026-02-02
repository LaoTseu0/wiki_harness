# 2.3.3 RAGAS / DeepEval

> **Leçon de la section [2.3 v0.0.3 — LlamaIndex + outillage standard](../2.3-v0.0.3-llamaindex-outillage-standard.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Dernier étage des evals : passer notre jeu dans l'**outillage
standard** que citent les offres. Pas pour remplacer le script maison
(assumé par la [roadmap couche T](../../../roadmap.md)) — pour parler
le même vocabulaire que l'industrie et vérifier que nos métriques
maison mesurent bien la même chose.

## Le savoir

- **RAGAS** — le framework spécialisé RAG ; ses quatre métriques
  canoniques, à savoir définir :
  - **faithfulness** : chaque affirmation de la réponse est-elle
    soutenue par le contexte ? (≈ notre score hallucination inversé) ;
  - **answer relevancy** : la réponse répond-elle à la question ?
  - **context precision** : les chunks remontés utiles sont-ils bien
    classés ? (≈ notre score retrieval, en plus fin) ;
  - **context recall** : le contexte couvre-t-il la réponse attendue ?
  Toutes sont des **LLM-as-judge packagés** — les biais de la
  [2.3.2](../2.3.2-llm-as-judge/2.3.2-llm-as-judge.md) s'appliquent,
  et le juge se configure (notre règle juge ≠ générateur reste).
- **DeepEval** — l'approche « pytest pour LLM » : métriques en
  assertions (`assert_test(test_case, [FaithfulnessMetric(...)])`),
  intégration CI naturelle — la passerelle avec le craftsmanship de
  [2.4.3](../../2.4-service-et-craftsmanship/2.4.3-tests-typing-packaging/2.4.3-tests-typing-packaging.md).
- **promptfoo** à situer (config YAML, comparaisons de prompts côte à
  côte) — un paragraphe, pas un chantier.
- **L'exercice de vérité** : corréler les scores RAGAS avec notre
  tableau maison sur les mêmes 30 questions. Convergence = confiance ;
  divergence = comprendre *qui* mesure quoi (souvent : notre score
  génération mélange ce que RAGAS sépare en faithfulness/relevancy).

## En pratique

Adapter le jeu au format RAGAS (question, answer, contexts,
ground_truth), configurer le juge local/API, produire les quatre
métriques pour les trois générations — une annexe du
[tableau final](../2.3.4-tableau-final/2.3.4-tableau-final.md).

## Pièges connus

- Laisser RAGAS juger avec un modèle par défaut (API OpenAI) sans le
  savoir : coût surprise + violation possible de la règle du juge —
  configurer explicitement.
- Empiler dix métriques : quatre bien comprises battent dix récitées ;
  chaque métrique du README doit avoir une phrase d'interprétation.
- Jeter le script maison : c'est lui qu'on sait déboguer, et c'est lui
  qui tourne sans dépendance — l'outillage standard est un
  *complément* de vocabulaire.

## Question d'entretien

> « Quels outils d'évaluation RAG connaissez-vous ? »
> Script maison pour la non-régression (assumé), RAGAS pour les
> métriques standard (faithfulness, context precision/recall…),
> DeepEval pour l'intégration pytest/CI, promptfoo à situer — et la
> corrélation maison/RAGAS vérifiée sur mon jeu.

## Références

- Doc RAGAS (métriques) ; doc DeepEval (métriques + pytest)
- [Roadmap couche T](../../../roadmap.md) — « ou script maison assumé »
