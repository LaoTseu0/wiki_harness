# P.1.1 GitHub public

> **Leçon de la section [P.1 Les repos publics](../p.1-repos-publics.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : 🔵 en continu
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Un GitHub public **en anglais** où chaque README suit le même canon :
problème, architecture (un schéma), métriques, « ce que je referais
autrement ». C'est le format qui transforme un projet en preuve
d'employabilité — et Mirakl en fait un critère de sélection formalisé.

## Le savoir

- **Le canon du README** (quatre sections, non négociables) :
  1. **problème** : quel besoin réel — « interroger la doc du homelab »,
     pas « un RAG » ;
  2. **architecture** : un **schéma** (les
     [schemas/](../../../02-homelab-rag/schemas/) du module 2 en sont
     l'exemple) + les décisions clés ;
  3. **métriques** : le nerf — le [tableau d'evals](../../../02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3.4-tableau-final/2.3.4-tableau-final.md),
     les [latences du bench](../../../04-ollama-vs-vllm-bench/4.3-analyse-et-verdict/4.3.2-verdict-ollama-vs-vllm/4.3.2-verdict-ollama-vs-vllm.md) ;
  4. **« what I'd do differently »** : la section qui prouve le recul —
     les échecs documentés valent les succès.
- **Anglais** : READMEs, commits, posts — le portfolio public est en
  anglais ([roadmap §4](../../../roadmap.md)) ; c'est aussi un attendu
  des offres (anglais professionnel écrit partout).
- **La vitrine expurgée du homelab** : une version publique sans IP,
  sans détails famille — cohérente avec la politique du repo homelab.
  Le [threat model](../../../06-production/6.2-securite/6.2.3-threat-model-jarvis/6.2.3-threat-model-jarvis.md)
  a sa version publique, pas sa version brute.
- **« Un repo qui tourne »** : instructions de lancement testées depuis
  un clone frais (le réflexe de la
  [2.4.3](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.3-tests-typing-packaging/2.4.3-tests-typing-packaging.md)) —
  un README qui ne démarre pas détruit la crédibilité qu'il visait.

## En pratique

Un README au canon pour chaque module livré, schéma inclus, métriques
copiées depuis les scripts (pas recopiées à la main), section « would
do differently » honnête, lancement vérifié sur machine propre — et le
tout lié depuis un profil GitHub soigné.

## Pièges connus

- Le README sans métriques : la section qui distingue des 90 % —
  ne jamais la sauter.
- Le README-tutoriel de 400 lignes : le recruteur scanne — problème,
  schéma, chiffres, recul, en une page.
- Publier des données sensibles du homelab : version expurgée
  systématique, scan avant push (le réflexe secrets de la
  [3.3.3](../../../03-jarvis-agent/3.3-comparaison-regimes-agents/3.3.3-note-de-conception/3.3.3-note-de-conception.md)).

## Question d'entretien

> « Montrez-moi un de vos projets. »
> L'URL d'un repo au canon : problème réel, schéma d'architecture,
> tableau de métriques, et ma section « ce que je referais » — un
> recruteur y trouve en une page ce que 90 % des candidats ne savent
> pas montrer.

## Références

- [Roadmap §6](../../../roadmap.md) — le portfolio ; §10.3 (Mirakl
  exige le lien GitHub)
- Les [schemas/](../../../02-homelab-rag/schemas/) du module 2 — le
  standard visuel
