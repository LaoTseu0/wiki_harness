# Tests adversariaux

> [carte du cours](../carte.md)

## L'essentiel

« Attaquer soi-même son système avant les autres » — passer de la
défense théorique
([6.2.1](owasp-top-10-llm.md)) à la
preuve : une petite campagne d'attaques sur son propre RAG et son
propre agent, chaque défense mesurée contre chaque attaque. Le
prolongement systématique de la démo d'injection de la
[5.3.1](../mcp/prompt-injection-indirecte.md).

## Le savoir

- **La démarche, comme les evals mais offensive** : un jeu d'attaques
  figé (comme le [jeu de questions](../retrieval/evals.md)),
  rejoué à chaque changement — la sécurité traitée en non-régression.
- **Les familles à couvrir** (chacune avec charge **bénigne**, un
  marqueur observable type « BANANE », jamais destructive) :
  - **injection indirecte** (document piégé) : la démo 5.3.1,
    systématisée sur plusieurs formulations ;
  - **injection directe** (dans la question) : « ignore le contexte
    et… » — teste le grounding
    ([2.1.6](../retrieval/rag-complet.md)) ;
  - **exfiltration par outil** (agent) : amener l'agent à passer une
    donnée sensible à un outil — teste le hook
    ([3.1.1](../agent/hook-tool-call.md))
    et le confinement réseau
    ([3.1.2](../agent/conteneur-moindre-privilege.md)) ;
  - **déni par consommation** : question qui fait boucler/exploser le
    contexte — teste MAX_TOURS et les plafonds.
- **Le livrable : la matrice attaque × défense** — pour chaque attaque,
  le comportement sans défense, puis avec chaque couche activée : qui
  casse quoi. C'est ce tableau qui prouve que les défenses *marchent*,
  pas juste qu'elles existent.
- **L'éthique du test** : uniquement sur **son** système, avec des
  charges inoffensives — l'objectif est la démonstration mécanique,
  pas la nuisance ([contexte : sécurité défensive](../_archive/roadmap.md)).

## En pratique

`adversarial/` : jeu d'attaques en JSON (famille, charge bénigne,
marqueur attendu), runner qui rejoue contre RAG et agent dans plusieurs
configs de défense, matrice générée — et traces Langfuse
([6.1.2](tracer-les-appels.md))
des tentatives pour l'analyse.

## Pièges connus

- Charges réellement dangereuses « pour le réalisme » : le marqueur
  bénin prouve exactement la même chose, sans risque — discipline non
  négociable.
- Tester une seule formulation d'injection : les modèles résistent à
  certaines, cèdent à d'autres — plusieurs variantes par famille.
- Déclarer « c'est sécurisé » : on déclare « ces attaques-ci sont
  mitigées, mesuré ainsi » — la sécurité absolue ne se prouve pas.

## Se tester

> « Comment testez-vous la sécurité de votre système LLM ? »
> Jeu d'attaques figé rejoué en non-régression, familles OWASP
> (injection directe/indirecte, exfiltration, consommation), charges
> bénignes à marqueur, matrice attaque × défense — et les traces des
> tentatives ; la même rigueur que les evals, côté offensif.

## Références

- [5.3.1 Prompt injection indirecte](../mcp/prompt-injection-indirecte.md)
  — la première démo, à systématiser
- OWASP LLM ([6.2.1](owasp-top-10-llm.md)) ;
  Simon Willison (veille injection)
