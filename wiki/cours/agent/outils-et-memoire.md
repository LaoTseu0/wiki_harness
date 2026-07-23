# Outils et mémoire : agir et se souvenir

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [les garde-fous](garde-fous.md) — les deux périmètres,
  sans lesquels accorder une capacité qui *agit* est prématuré ; [le function
  calling](../fondamentaux/function-calling.md) — un outil est un schéma joint à
  la requête plus une fonction, et le schéma **est du prompt**. Cette propriété
  ressert : c'est en restreignant le schéma qu'on restreint ce que le modèle peut
  demander.
- **Débloque** : [les régimes d'agents](regimes-agents.md), où l'agent devient
  persistant — et où la mémoire externe passe de confort à nécessité, parce
  qu'une session qui ne finit jamais ne peut pas garder son état dans la fenêtre.

## L'essentiel

Les garde-fous posés, l'agent gagne ses deux capacités : **agir** sur le homelab
via un [outil Home Assistant](outil-home-assistant.md) à périmètre limité, et
**se souvenir** via une [mémoire externe versionnée dans git](memoire-versionnee.md).

La thèse : ce ne sont pas deux fonctionnalités indépendantes, elles se
**renforcent**. Un agent qui agit sans mémoire répète ses erreurs ; une mémoire
sans capacité n'a rien à retenir. Et les deux obéissent à la même discipline que
les garde-fous viennent de poser : moindre privilège sur le périmètre de
l'outil, externalisation et versionnement pour la mémoire. Le mécanisme commun,
sous les deux : **l'état durable d'un agent vit hors de la fenêtre de contexte**.

Cette leçon situe les deux capacités l'une par rapport à l'autre ; leur
construction est dans les deux leçons du groupe.

## Le savoir

### Deux capacités qui se referment l'une sur l'autre

Prises séparément, chacune est incomplète. Un agent qui agit sans rien retenir
recommence à zéro chaque session : il redemande ce qu'il savait déjà, refait
l'erreur qu'il venait de corriger. Une mémoire sans capacité d'agir n'a aucune
expérience à consigner — elle ne peut mémoriser que ce qu'on lui dicte.

La boucle ne se referme que si les deux existent : **agir** produit de
l'expérience, **se souvenir** la retient, et l'expérience retenue améliore
l'action suivante. C'est pourquoi le domaine les traite ensemble et non l'une
après l'autre comme deux briques sans rapport.

### Le même réflexe de périmètre qu'aux garde-fous

L'outil Home Assistant applique le pattern « registre » de
[l'évolutivité sans friction](../framework/evolutivite.md) — un outil s'ajoute
en un fichier — mais avec un token à **périmètre limité** : le moindre privilège
du [conteneur](conteneur-moindre-privilege.md) appliqué aux credentials. La
capacité d'agir n'échappe pas à la discipline posée juste avant ; elle en est la
première application concrète.

### L'état durable vit hors de la fenêtre de contexte

La fenêtre est périssable : elle se tronque, la session se ferme, et tout ce
qu'elle contenait disparaît. Le long terme d'un agent doit donc se déporter
**ailleurs** — dans des fichiers, et non dans le contexte. Le choix décisif est
de les mettre dans **git** : la mémoire devient diffable, auditable, réversible.
La mémoire d'un agent est du code, avec les mêmes garanties — on peut demander
*pourquoi* elle croit une chose, et *révoquer* une croyance polluée.

## Quand c'est la bonne réponse

**Un outil custom** dès qu'une capacité est récurrente et son périmètre
définissable — pas pour une action ponctuelle qu'un script suffirait à faire.
L'outil vaut son schéma et son enregistrement quand le modèle aura à le
rappeler plusieurs fois, avec des arguments variables mais bornés.

**Une mémoire externe** dès que l'agent doit persister entre sessions, ou agir
sur un système dont l'état importe d'une fois à l'autre. Tant qu'une seule
session suffit à la tâche, la mémoire externe n'ajoute que son coût — la
consolidation à écrire, les conflits à trancher — sans contrepartie.

## Ce qu'on ne saura pas faire

Cette leçon situe ; elle ne construit ni l'outil ni la mémoire. Le détail de
chacun est dans [l'outil Home Assistant](outil-home-assistant.md) et [la mémoire
versionnée](memoire-versionnee.md).

Ce qui promouvrait ce groupe en « refaire » : deux étapes réelles sous
`wiki/etapes/agent/` — l'enregistrement d'un outil qui agit, et les hooks de
session qui synchronisent la mémoire — chacune avec son test de bout en bout.

## Se tester

1. Pourquoi versionner la mémoire d'un agent plutôt que la garder dans une base
   dédiée ?
   *Réussi si* la réponse cite l'audit (`git log` répond « pourquoi croit-il
   ça ? »), le rollback (une pollution se révoque par revert) et le blame (la
   croyance est datée), et résume par « la mémoire est du code ».
2. Un agent agit correctement mais ne retient rien d'une session à l'autre.
   Quel symptôme, et qu'est-ce que ça dit du couple capacité / mémoire ?
   *Réussi si* la réponse observe qu'il répète ses erreurs et redemande ce qu'il
   sait déjà, et conclut que la capacité sans mémoire ne referme pas la boucle.
3. Pour simplifier, on donne à l'outil un token « accès complet à la maison ».
   Pourquoi est-ce le même piège que le montage large du conteneur ?
   *Réussi si* la réponse relie au moindre privilège : un token admin fait que
   le jour où l'agent est injecté, l'injection est admin de la maison — le rayon
   de dégât est tout ce qu'on a accordé.

## À retenir

- Agir et se souvenir se renforcent : sans mémoire l'agent répète ses erreurs,
  sans capacité la mémoire n'a rien à retenir.
- L'état durable vit hors de la fenêtre de contexte, dans des fichiers — et dans
  git pour être auditable et réversible.
- La capacité d'agir hérite du moindre privilège des garde-fous : le token est
  une credential à périmètre limité, comme un montage.

## Références

- [architecture/jarvis.md du homelab](../../../../homelab/architecture/jarvis.md)
  — la Phase 3 dont ce groupe est la réalisation
