# 6.2.1 OWASP Top 10 for LLM Applications

> **Leçon de la section [6.2 Sécurité](../6.2-securite.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Le référentiel que « connaître par cœur » ([roadmap](../../../roadmap.md))
n'est pas une figure de style : l'OWASP Top 10 for LLM Applications est
le vocabulaire commun des offres sécurité IA. La compétence n'est pas
de le réciter mais de **mapper chaque risque sur son propre système** —
ce qu'on a déjà mitigé, ce qui reste ouvert.

## Le savoir

- **Les dix, avec l'ancrage sur ce parcours** (édition 2025) :

  | # | Risque | Où dans ce repo |
  |---|---|---|
  | LLM01 | Prompt injection | [5.3.1](../../../05-homelab-mcp/5.3-securite/5.3.1-prompt-injection-indirecte/5.3.1-prompt-injection-indirecte.md) (démo) |
  | LLM02 | Sensitive info disclosure | traces self-hostées [6.1.1](../../6.1-observabilite/6.1.1-langfuse-self-hoste/6.1.1-langfuse-self-hoste.md), local-first |
  | LLM03 | Supply chain | modèles/paquets vérifiés, quantisations tracées |
  | LLM04 | Data & model poisoning | scan du corpus à l'indexation |
  | LLM05 | Improper output handling | `calculer` filtré [1.1.3](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md), sorties validées |
  | LLM06 | Excessive agency | moindre privilège [3.1.2](../../../03-jarvis-agent/3.1-garde-fous-et-securite/3.1.2-conteneur-moindre-privilege/3.1.2-conteneur-moindre-privilege.md), lecture seule MCP |
  | LLM07 | System prompt leakage | pas de secret en prompt |
  | LLM08 | Vector/embedding weaknesses | filtres [2.2.4](../../../02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.4-filtres-metadonnees/2.2.4-filtres-metadonnees.md), périmètres |
  | LLM09 | Misinformation | grounding + citations [2.1.6](../../../02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.6-rag-complet/2.1.6-rag-complet.md), evals hallucination |
  | LLM10 | Unbounded consumption | MAX_TOURS, plafonds, suivi coûts [6.1.3](../../6.1-observabilite/6.1.3-suivi-des-couts/6.1.3-suivi-des-couts.md) |

- **La lecture transversale** : la moitié du Top 10 se mitige par
  **moindre privilège + validation des E/S** — exactement les deux
  périmètres du module 3. Le dire ainsi montre qu'on a compris la
  structure, pas mémorisé une liste.
- **Ce qui reste ouvert (à assumer)** : le homelab n'a pas de gateway
  LLM ni de guardrails outillés (Llama Guard, etc.) — les *situer*
  ([roadmap §10.1](../../../roadmap.md)) et dire pourquoi c'est hors
  scope à cette échelle.

## En pratique

Une page dans le README du module 6 : le tableau ci-dessus rempli avec
les liens réels du repo, plus deux lignes par risque non mitigé
(pourquoi acceptable ici, comment on le traiterait en entreprise).

## Pièges connus

- Réciter les dix sans ancrage : l'entretien teste l'application, pas
  la mémoire — chaque risque doit pointer un fichier du repo ou un
  choix conscient.
- Confondre injection (LLM01) et excessive agency (LLM06) :
  l'injection fait *dire/demander*, l'agency laisse *faire* — les
  défenses diffèrent (balisage/périmètre vs privilèges/interception).
- Ignorer les versions : OWASP LLM évolue (2023 → 2025) — citer
  l'édition, c'est montrer qu'on suit.

## Question d'entretien

> « Que connaissez-vous de l'OWASP Top 10 for LLM ? »
> Le citer, puis le mapper sur un système réel : injection démontrée,
> excessive agency bornée par moindre privilège, output handling
> validé, misinformation contrée par grounding+evals — la liste
> devient une revue d'architecture.

## Références

- OWASP Top 10 for LLM Applications (édition courante)
- [Roadmap couche T](../../../roadmap.md) — « à connaître par cœur »
