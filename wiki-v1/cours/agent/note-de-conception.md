# Note de conception

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : tous les choix du domaine, puisque la note les documente —
  [garde-fous](garde-fous.md), [outil Home Assistant](outil-home-assistant.md),
  [mémoire versionnée](memoire-versionnee.md), [quatre régimes](quatre-regimes.md) ;
  le format ADR, posé sur place ci-dessous.
- **Débloque** : rien de neuf en capacité — c'est la capitalisation du domaine.
  La note nourrit le corpus RAG du homelab : l'agent pourra citer sa propre
  conception.

## L'essentiel

Le domaine se termine par de l'écriture : une **note de conception** dans
`architecture/` (le dépôt homelab) et le **`.pi/` complet versionné** — le profil
reproductible de l'agent.

La thèse : le code montre *ce qui* tourne, la note montre *pourquoi* — et un
pourquoi qu'on n'écrit pas au moment de la décision est un pourquoi perdu, parce
qu'on ne se souvient plus des alternatives qu'on avait écartées. La valeur d'une
note au format ADR est d'être **relisible dans six mois** par quelqu'un qui n'a
pas assisté à la décision.

Un ADR — *Architecture Decision Record* — est un format court qui fige une
décision, les alternatives écartées, la raison du choix et ses conséquences.
Cette leçon ne réimplémente rien : elle documente des décisions prises ailleurs
dans le domaine.

## Le savoir

### La note de conception, structure ADR

Une page, trois blocs.

1. **Contexte** : l'agent Jarvis, Phase 3 de
   [jarvis.md](../../../../homelab/architecture/jarvis.md).
2. **Décisions**, chacune avec son alternative écartée et la raison :
   - hooks + conteneur plutôt que prompt seul
     ([garde-fous](garde-fous.md)) ;
   - deux outils HA au lieu d'un couteau suisse
     ([outil `home_assistant`](outil-home-assistant.md)) ;
   - mémoire git plutôt qu'une base
     ([mémoire versionnée](memoire-versionnee.md)) ;
   - harnais Pi plutôt qu'un SDK
     ([quatre régimes](quatre-regimes.md)).
3. **Conséquences** : ce qu'on gagne, ce qu'on s'interdit, ce qui reste ouvert —
   dont le multi-sessions du [mode RPC/SDK](mode-rpc-sdk.md).

### Le `.pi/` versionné comme livrable

Extensions (le hook `tool_call`), outils enregistrés, hooks de session pour la
mémoire, configuration : le dossier `.pi/` **est** le profil reproductible de
l'agent. Cloner, lancer, obtenir le même agent confiné — c'est ce que le
versionnement du dossier garantit, là où une capture d'écran de configuration ne
garantit rien.

Ce qui n'y entre **jamais** : un secret. Le token HA vit en variable
d'environnement, pas dans le dépôt. Config oui, credentials jamais.

### La règle d'écriture ADR

Une décision = alternatives + choix + raison, une phrase chacun. Pas de prose
d'ambiance. La note qui **paraphrase le code** ne sert à rien — le code dit déjà
le *comment* ; la note documente les *pourquoi* et les alternatives écartées, qui
sont précisément ce que le code ne peut pas montrer.

## Quand c'est la bonne réponse

**Un ADR** dès qu'une décision a des alternatives réelles qu'on a écartées :
c'est ce qu'on oublie et qu'on regrette de ne pas avoir écrit. Une décision sans
alternative n'a rien à documenter — l'ADR ne sert pas à narrer, il sert à retenir
un arbitrage.

**Au fil des décisions**, pas après coup : deux lignes le jour même, mise en
forme à la fin. Documenter après coup, c'est documenter ce dont on se souvient —
donc un souvenir biaisé, d'où les alternatives écartées ont déjà disparu.

## Ce qu'on ne saura pas faire

Il n'y a rien à mesurer — c'est de l'écriture. La seule vérification possible est
que le `.pi/` versionné soit **effectivement reproductible** : cloner le dépôt et
obtenir le même agent confiné, ce qui se constate en le faisant, pas en le
déclarant.

Un piège reste à écarter à chaque commit : **versionner un secret** dans `.pi/`.
La parade est un scan avant commit — la config passe, les credentials sont
rejetés.

Ce qui promouvrait cette leçon en « refaire » : la note écrite et le `.pi/`
versionné dont on a vérifié qu'un clone redonne le même agent.

## Se tester

1. Qu'est-ce qu'une note de conception doit contenir que le code ne dit pas ?
   *Réussi si* la réponse répond « les pourquoi et les alternatives écartées », et
   note que le code dit déjà le comment.
2. Vous versionnez le `.pi/` complet. Qu'est-ce qui ne doit jamais y entrer, et
   comment s'en assurer ?
   *Réussi si* la réponse exclut tout secret — le token en variable
   d'environnement — et prévoit un scan avant commit.
3. Quand écrit-on la note : au fil des décisions ou à la fin ?
   *Réussi si* la réponse écrit au fil (deux lignes par décision le jour même) et
   met en forme à la fin, parce que documenter après coup fixe un souvenir biaisé
   d'où les alternatives ont disparu.

## À retenir

- Le code montre ce qui tourne, la note montre pourquoi : un pourquoi non écrit au
  moment de la décision est perdu.
- Format ADR : une décision = alternatives écartées + choix + raison, une phrase
  chacun, relisible dans six mois.
- Le `.pi/` versionné est le profil reproductible de l'agent — cloner et lancer
  redonne le même agent confiné.
- Un secret ne se versionne jamais : config oui, credentials en variable
  d'environnement, scan avant commit.
- La note s'écrit au fil des décisions, se met en forme à la fin.

## Références

- Le format ADR (*Architecture Decision Records*), Michael Nygard — la structure
  contexte / décision / alternatives / conséquences
- [jarvis.md du homelab](../../../../homelab/architecture/jarvis.md) — la Phase 3
  que ce domaine réalise
