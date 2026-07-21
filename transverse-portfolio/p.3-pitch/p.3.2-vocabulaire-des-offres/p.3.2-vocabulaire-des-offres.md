# P.3.2 Vocabulaire des offres

> **Leçon de la section [P.3 Le pitch](../p.3-pitch.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : 🔵 en continu
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Employer **les mots des offres** — production-grade, human-in-the-loop,
grounding, pipelines d'évaluation continue, gateway multi-modèles. Ce
n'est pas du jargon décoratif : chaque terme est un signal de
reconnaissance, et derrière chacun il y a un module de ce parcours qui
le prouve.

## Le savoir

- **Le lexique, adossé aux preuves** ([roadmap §10.4](../../../roadmap.md)) :

  | Terme de l'offre | Ce que je montre |
  |---|---|
  | **production-grade** | tests, typing, packaging ([2.4.3](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.3-tests-typing-packaging/2.4.3-tests-typing-packaging.md), [1.3.2](../../../01-llm-from-scratch/1.3-framework-maison/1.3.2-clean-code-production-grade/1.3.2-clean-code-production-grade.md)) |
  | **human-in-the-loop** | hook tool_call ([3.1.1](../../../03-jarvis-agent/3.1-garde-fous-et-securite/3.1.1-hook-tool-call/3.1.1-hook-tool-call.md)) |
  | **grounding** | citations + « je ne sais pas » ([2.1.6](../../../02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.6-rag-complet/2.1.6-rag-complet.md)) |
  | **pipelines d'évaluation continue** | evals de non-régression ([2.1.7](../../../02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.7-evals/2.1.7-evals.md), [2.2.5](../../../02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.5-evals-comparatives/2.2.5-evals-comparatives.md)) |
  | **gateway multi-modèles** | routage coût/latence/qualité ([1.3.4](../../../01-llm-from-scratch/1.3-framework-maison/1.3.4-routage-multi-agentique/1.3.4-routage-multi-agentique.md)) |
  | **hybrid search / re-ranking** | [2.2.2](../../../02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.2-retrieval-hybride/2.2.2-retrieval-hybride.md) / [2.2.3](../../../02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.3-re-ranking-top-k/2.2.3-re-ranking-top-k.md) |
  | **observabilité / suivi des coûts** | Langfuse ([6.1](../../../06-production/6.1-observabilite/6.1-observabilite.md)) |

- **La règle anti-buzzword** : n'employer un terme que si on peut
  enchaîner sur sa preuve dans la phrase suivante. « J'ai fait du
  human-in-the-loop » suivi de « le hook intercepte chaque tool_call et
  l'humain valide les commandes shell » — le terme *plus* la mécanique.
- **Pourquoi ça trie** : les recruteurs scannent ces mots ; les
  candidats qui les emploient *avec* la mécanique derrière se
  distinguent de ceux qui les récitent. Le parcours entier est conçu
  pour que chaque terme ait sa démonstration.
- **La mise à jour** : le vocabulaire des offres bouge (LangGraph a
  monté en 2026, [roadmap §10.4](../../../roadmap.md)) — la
  [veille](../../p.2-ecrire/p.2.2-veille-obsidian/p.2.2-veille-obsidian.md)
  tient le lexique à jour.

## En pratique

Ficher le lexique (terme → définition en une phrase → module preuve),
le réviser avant chaque entretien, et s'entraîner à l'enchaînement
terme → mécanique à voix haute.

## Pièges connus

- Le buzzword nu : employer « grounding » sans pouvoir l'expliquer se
  retourne immédiatement — terme + preuve, toujours groupés.
- Le vocabulaire figé : les offres de 2026 ne sont pas celles de 2024 —
  la veille maintient le lexique.
- Traduire mécaniquement : certains termes restent en anglais dans les
  offres françaises (grounding, embeddings) — les garder tels quels.

## Question d'entretien

> Chaque terme *est* une question potentielle. « Qu'entendez-vous par
> production-grade / grounding / human-in-the-loop ? » — la réponse est
> la définition **plus** le module de ce repo qui l'implémente ; le
> vocabulaire n'est crédible qu'adossé au code.

## Références

- [Roadmap §10.4](../../../roadmap.md) — les termes à employer
- [P.3.1 La phrase](../p.3.1-la-phrase/p.3.1-la-phrase.md) — le pitch
  qui les met en scène
