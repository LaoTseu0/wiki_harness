# Evals comparatives

> [carte du cours](../carte.md)

## L'essentiel

La v0.0.2 n'existe que si elle **bat la v0.0.1 sur le même jeu** : les
12 questions de la [2.1.7](evals.md),
rejouées à l'identique sur chaque configuration, produisent LE
livrable de la section — le tableau comparatif. C'est la
non-régression appliquée au retrieval : traiter les changements de
chaîne comme du code.

## Le savoir

- **Le protocole** : jeu figé (aucune question modifiée entre
  versions — sinon la comparaison ment), une ligne de tableau par
  configuration, mêmes trois scores (retrieval / génération /
  hallucination) + latence :

  | Config | Retrieval | Génération | Halluc. | Latence |
  |---|---|---|---|---|
  | v0.0.1 SQLite brute force | 7/12 | 7/12 | 0 | réf. |
  | Qdrant seul | ? | ? | ? | ? |
  | + hybride | ? | ? | ? | ? |
  | + re-ranking | ? | ? | ? | ? |
  | + filtres | ? | ? | ? | ? |

- **L'ablation** : ajouter les techniques **une par une** (chaque ligne
  ne change qu'une variable) — c'est ce qui permet d'attribuer chaque
  point gagné à sa cause, et de retirer ce qui ne rapporte rien.
- **Lire les deltas** : Qdrant seul ne devrait *rien* changer aux
  scores (même embeddings, index quasi exact sur petit corpus) — si ça
  bouge, c'est un bug (recall HNSW, préfixes). Les gains attendus
  viennent de l'hybride (questions à termes exacts) et du re-ranking
  (bon document mal classé).
- **Enrichir le jeu, prudemment** : les nouvelles capacités (filtres)
  appellent 2-3 questions nouvelles — elles s'ajoutent *pour toutes
  les configs* et sont marquées comme extension du jeu (le cœur de 12
  reste comparable).

## En pratique

Étendre [07_evals.py](../../etapes/retrieval/07_evals.py)
pour paramétrer la
configuration de chaîne, boucler sur les cinq configs, générer le
tableau en markdown — copié tel quel dans le README du module (et
c'est la ligne du CV : « with regression evals »).

## Pièges connus

- Changer deux choses entre deux lignes (hybride ET k) : le tableau ne
  prouve plus rien — une variable par ligne, discipline d'ablation.
- Ignorer la variance : la génération n'est pas déterministe — fixer
  temperature basse pour les evals, et rejouer deux fois avant de
  crier au progrès d'un point. Et sur 12 questions, 1 point = 8 % :
  un delta de ±1-2 points ne se conclut pas — regarder *quelles*
  questions ont basculé plutôt que les totaux, et réserver les
  verdicts fins au jeu étendu (~30,
  [2.3.2](llm-as-judge.md)).
- Oublier la latence : +3 points de retrieval pour ×4 en latence est
  un *choix* à documenter, pas une victoire gratuite.

## Se tester

> « Comment prouvez-vous qu'une amélioration RAG en est une ? »
> Jeu figé, ablation technique par technique, scores ventilés +
> latence, tableau versionné — et la volonté de retirer ce qui n'a pas
> de delta ; c'est exactement la démarche du tableau de mon module 2.

## Références

- [2.1.7 Evals](evals.md)
  — le socle et le jeu de questions
- [Roadmap couche T](../_archive/roadmap.md) — « tests de non-régression »
