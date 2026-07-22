# 1.3.4 Routage multi-agentique

> **Leçon de la section [1.3 Le framework maison](../1.3-framework-maison.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Le [routeur multi-modèles](../../../../homelab/architecture/router-multi-model.md)
du homelab devenu code : envoyer chaque requête au **bon modèle** selon
coût / latence / qualité / confidentialité, et orchestrer plusieurs
agents quand une tâche se décompose. C'est la « gateway
multi-modèles » des offres (GRDF en construit littéralement une —
[roadmap §10.3](../../../roadmap.md)).

## Le savoir

- **Routage mono-agent (le plus rentable)** : une table de décision
  requête → modèle.
  - Critères d'entrée : complexité estimée, taille de contexte requise,
    sensibilité des données (local obligatoire ?), budget latence.
  - Politiques : par règles (regex/taille/type de tâche — début
    honnête), par classifieur LLM léger (un petit modèle route vers
    les gros), par **escalade** (essayer petit, escalader si échec
    mesurable — le pattern au meilleur ratio coût/qualité).
- **Multi-agents, version sceptique** (le scepticisme de Pi, assumé
  dans la [roadmap couche 3](../../../roadmap.md)) : des sessions
  séparées **observables** battent souvent la boîte noire. Le pattern
  retenu : **superviseur/ouvriers** — un superviseur décompose,
  distribue à des ouvriers *sans mémoire partagée*, agrège. Pas de
  « swarm » : deux niveaux, des frontières nettes, des E/S tracées.
- **L'isolation de contexte** comme argument : chaque ouvrier reçoit
  un contexte minimal ciblé (context engineering, couche 0) — c'est
  souvent *la* vraie raison de découper, avant le parallélisme.
- **Interface de la brique** : `router.route(requête) → provider` +
  `superviseur.run(tâche) → résultat` ; le routeur est un provider
  comme un autre (composable, testable).

## En pratique

Premier incrément : politique par règles à trois niveaux (Qwen3 4B
local / modèle local plus gros / API cloud) + escalade sur échec
d'eval ; tracer chaque décision de routage (module 6) pour pouvoir la
défendre chiffres en main.

## Pièges connus

- Router au feeling sans mesure : sans coût/latence/qualité tracés par
  route, impossible de prouver que le routage rapporte.
- Multi-agents pour le plaisir : si une seule session avec un bon
  contexte suffit, l'orchestration n'ajoute que de la surface d'erreur.
- Mémoire partagée entre ouvriers : les agents se polluent — préférer
  le superviseur comme seul point d'agrégation.

## Question d'entretien

> « Quand introduire du multi-agents, et comment le garder
> débogable ? »
> Quand la tâche se décompose en sous-tâches à contextes disjoints ;
> deux niveaux max, E/S de chaque agent tracées, agrégation en un seul
> point — et du routage mono-agent d'abord, qui capte l'essentiel du
> gain.

## Références

- [router-multi-model.md](../../../../homelab/architecture/router-multi-model.md)
  (homelab) — le raisonnement d'origine
- Blog d'ingénierie Anthropic sur les agents (veille,
  [roadmap §7](../../../roadmap.md))
