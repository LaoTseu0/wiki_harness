# 2.3.5 RAG vs fine-tuning

> **Leçon de la section [2.3 v0.0.3 — LlamaIndex + outillage standard](../2.3-v0.0.3-llamaindex-outillage-standard.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir — la réponse se rédige dans le README en fin
> de module
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Question d'entretien n°4 du [relevé de terrain](../../../roadmap.md),
récurrente parce qu'elle teste la lucidité d'architecture : **RAG pour
la connaissance changeante et sourçable, fine-tuning pour le style et
les formats, presque jamais pour injecter des faits**. La leçon rédige
cette réponse, appuyée sur *ce* projet.

## Le savoir

- **La grille de décision** :

  | Critère | RAG | Fine-tuning |
  |---|---|---|
  | Les faits changent | ✅ ré-indexer suffit | ❌ ré-entraîner |
  | Sources exigées | ✅ citations natives | ❌ opaque |
  | Contrôle d'accès | ✅ filtres par requête | ❌ tout est dans les poids |
  | Style/format récurrent | ~ prompt/few-shot | ✅ son vrai cas d'usage |
  | Coût d'entrée | index + retrieval | dataset propre + GPU + evals |
  | Risque | retrieval raté (mesurable) | oubli catastrophique, dérive |

- **Pourquoi RAG était le bon choix ici** (l'argumentaire du README) :
  la doc homelab **change** (chaque décision l'amende), les réponses
  doivent être **sourcées** (« qu'avait-on décidé pour le backup ? »
  exige la référence), le corpus est petit (l'index se reconstruit en
  minutes), et un fine-tuning sur 60 documents apprendrait par cœur
  sans généraliser.
- **Ce que le fine-tuning ferait ici** : rien pour les faits — au
  mieux, styliser le ton des réponses ; le détail mécanique (LoRA,
  coûts réels) vit dans l'[entrée glossaire](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.6-lora/1.2.6-lora.md)
  et la [6.3](../../../06-production/6.3-culture-fine-tuning/6.3-culture-fine-tuning.md).
- **La réponse n'est pas exclusive** : les deux se combinent (un modèle
  fine-tuné sur le *format* de réponse, alimenté par un RAG pour les
  *faits*) — le dire en entretien évite le faux dilemme.
- **L'ordre des solutions** (à réciter) : prompt → few-shot → RAG →
  fine-tuning — chaque marche coûte un ordre de grandeur de plus en
  complexité opérationnelle.

## En pratique

Rédiger la section « RAG vs fine-tuning: why RAG here » du README
anglais (10 lignes max, la grille + trois arguments locaux) — relue à
voix haute : c'est un texte à *dire* en entretien, pas à lire.

## Pièges connus

- Réciter la grille sans l'ancrer : la force de la réponse vient des
  exemples de *ce* projet (la doc qui change, les citations exigées).
- Opposer les deux absolument : le combiné style-par-tuning +
  faits-par-RAG est la réponse senior.
- Oublier la première marche : beaucoup de « besoins de fine-tuning »
  meurent avec un bon prompt système — le dire fait gagner des points.

## Question d'entretien

> « RAG ou fine-tuning pour ce besoin ? »
> Poser trois questions en retour : les faits changent-ils ? faut-il
> des sources ? est-ce un problème de fond ou de forme ? — puis
> dérouler la grille, et citer un cas concret des deux côtés.

## Références

- [1.2.6 LoRA](../../../01-llm-from-scratch/1.2-glossaire-executable/1.2.6-lora/1.2.6-lora.md)
  — la mécanique de l'autre branche de l'alternative
- [Roadmap couche 2](../../../roadmap.md) — « question d'entretien
  récurrente »
