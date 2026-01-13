# 2.1.7 Evals

> **Leçon de la section [2.1 v0.0.1 — le RAG à la main](../2.1-v0.0.1-rag-a-la-main.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir — [07_evals.py](07_evals.py) (germe des
> tests pytest du module)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

« Un projet LLM sans évaluation chiffrée est une démo, pas de
l'ingénierie » ([roadmap, principe 3](../../../roadmap.md)). Un jeu de
questions figé, un score automatique, une baseline — c'est ce qui
permet de dire « la v0.0.2 est meilleure » au lieu de « ça a l'air
mieux ». La partie la plus valorisable du module, et la question
d'entretien n°1.

## Le savoir

- **Le jeu de questions**
  ([evals/questions.json](../../evals/questions.json)) : 12 entrées
  pour commencer — question, fichier source attendu, éléments de
  réponse attendus. Figé et versionné : c'est un **jeu de
  non-régression**, on le traite comme du code.
- **Trois scores séparés, un par maillon** :
  - **retrieval** : le fichier attendu est-il dans le top-k ? (7/12 en
    baseline — c'est LE maillon faible identifié) ;
  - **génération** : la réponse contient-elle les éléments attendus,
    sachant le bon contexte ? (7/12) ;
  - **hallucination** : la réponse affirme-t-elle quelque chose
    d'absent des sources ? (0/12 — grâce au « je ne sais pas » de
    [2.1.6](../2.1.6-rag-complet/2.1.6-rag-complet.md)). Ce score-là
    n'est **pas** vérifiable par mot-clé : en v0.0.1 il vient d'une
    relecture humaine assumée des 12 réponses (rapide à cette
    échelle), doublée d'un garde-fou automatique — toute réponse
    non-abstention dont le retrieval a raté est suspecte par
    construction ; l'automatisation complète attend le juge
    ([2.3.2](../../2.3-v0.0.3-llamaindex-outillage-standard/2.3.2-llm-as-judge/2.3.2-llm-as-judge.md)).
    Et conclure « zéro hallucination » exige la correspondance
    **question par question** entre échecs retrieval et génération —
    l'égalité des totaux (7/12 = 7/12) ne prouve rien à elle seule.
  Séparer les scores, c'est ce qui rend le **diagnostic par couche**
  possible.
- **Déterministe d'abord** : exact match sur la source, présence de
  mots-clés attendus — rapide, reproductible, gratuit. Les juges LLM
  ([2.3.2](../../2.3-v0.0.3-llamaindex-outillage-standard/2.3.2-llm-as-judge/2.3.2-llm-as-judge.md))
  n'arrivent qu'en v0.0.3, sur ce socle.
- **La baseline est un point de départ, pas un bulletin** : 7/12
  retrieval est *honnête et médiocre* — exactement ce qu'il faut pour
  prouver le gain de Qdrant/hybride/re-ranking en
  [2.2.5](../../2.2-v0.0.2-qdrant-retrieval-avance/2.2.5-evals-comparatives/2.2.5-evals-comparatives.md).
- **Evals = tests** : chaque score est une assertion pytest en puissance
  (`assert score_retrieval >= baseline`) — le germe du craftsmanship de
  [2.4.3](../../2.4-service-et-craftsmanship/2.4.3-tests-typing-packaging/2.4.3-tests-typing-packaging.md).

## En pratique

[07_evals.py](07_evals.py) : boucler sur le jeu, exécuter la
chaîne, calculer les trois scores, afficher le tableau — et commiter le
résultat daté dans le README (l'historique des scores raconte le
module).

## Pièges connus

- Améliorer le prompt en regardant les questions du jeu : c'est de
  l'overfitting sur son propre thermomètre — le jeu s'enrichit, il ne
  se « vise » pas.
- Un score global unique : 14/24 ne dit pas *quel maillon* répare —
  toujours ventiler.
- Jeu trop facile (questions-titres) : 12/12 partout et plus rien à
  apprendre — inclure des questions à reformulation, à cheval sur deux
  documents, et hors corpus.

## Question d'entretien

> « Comment évaluez-vous votre système ? » — la question n°1, que 90 %
> des candidats ratent ([roadmap §3](../../../roadmap.md)).
> Jeu figé versionné, scores déterministes par maillon (retrieval /
> génération / hallucination), baseline chiffrée, non-régression à
> chaque changement — puis LLM-as-judge et RAGAS pour l'échelle.

## Références

- [Schéma 06_evals_baseline](../../schemas/06_evals_baseline.png)
- [Roadmap couche T](../../../roadmap.md) — les trois familles d'evals
