# Note de conception

> [carte du cours](../carte.md)

## L'essentiel

Le module se termine par de l'écriture : une **note de conception**
dans `architecture/` (le dépôt homelab) et le **`.pi/` complet
versionné** — le « profil » de l'agent. Le code montre *ce qui*
tourne ; la note montre *pourquoi* — et c'est elle qui se lit en
entretien.

## Le savoir

- **La note de conception, structure canonique** (une page, style ADR) :
  1. **contexte** : l'agent Jarvis, Phase 3 de
     [jarvis.md](../../../../homelab/architecture/jarvis.md) ;
  2. **décisions** (avec alternatives écartées et pourquoi) : hooks +
     conteneur plutôt que prompt seul
     ([garde-fous et sécurité d'abord](garde-fous.md)),
     deux outils HA au lieu d'un
     ([outil home_assistant](outil-home-assistant.md)),
     mémoire git vs base
     ([mémoire versionnée](memoire-versionnee.md)),
     harnais Pi vs SDK
     ([quatre régimes, même boucle](quatre-regimes.md)) ;
  3. **conséquences** : ce qu'on gagne, ce qu'on s'interdit, ce qui
     reste ouvert (le multi-sessions du
     [mode RPC/SDK](mode-rpc-sdk.md)).
- **Le `.pi/` versionné comme livrable** : extensions (hook
  tool_call), outils enregistrés, hooks de session mémoire, config —
  le dossier *est* le profil reproductible de l'agent : cloner, lancer,
  obtenir le même agent confiné. Peu de candidats peuvent montrer ça —
  d'où « le projet portfolio le plus original du lot »
.
- **La règle d'écriture** : une décision = alternatives + choix +
  raison en une phrase chacun. Pas de prose d'ambiance — le format ADR
  existe pour être relu dans six mois.

## En pratique

Rédiger la note dans `architecture/` du homelab (le corpus RAG la
connaîtra — l'agent pourra citer sa propre conception), vérifier que
`.pi/` ne contient **aucun secret** (le token HA vit en variable
d'environnement), tag de fin de module.

## Pièges connus

- Documenter après avoir oublié : la note s'écrit au fil des décisions
  (deux lignes par décision le jour même), se met en forme à la fin.
- Versionner un secret dans `.pi/` : config oui, credentials jamais —
  un scan avant commit.
- La note qui paraphrase le code : elle documente les *pourquoi* et
  les alternatives écartées — le code dit déjà le comment.

## Se tester

> « Racontez une décision d'architecture que vous avez prise sur ce
> projet. »
> Format réponse = format ADR : contexte, alternatives, choix,
> conséquences — ex. mémoire git plutôt que base : audit et rollback
> gagnés, concurrence de sessions sacrifiée, et le lien vers la note
> en preuve.

## Références

- Le format ADR (Architecture Decision Records) — Michael Nygard
- [jarvis.md](../../../../homelab/architecture/jarvis.md) — la Phase 3
  que ce module réalise
