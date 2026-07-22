# 3.1.1 Hook tool_call

> **Leçon de la section [3.1 Garde-fous et sécurité d'abord](../3.1-garde-fous-et-securite.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Le hook `tool_call` est un **point d'interception** : chaque appel
d'outil de l'agent passe par notre code *avant* d'être exécuté. C'est
là que vivent la liste noire des commandes destructives et la
validation humaine — la version industrialisée de ce que la
[mini-boucle](../../../01-llm-from-scratch/1.1-socle-sans-framework/1.1.4-mini-boucle-agent/1.1.4-mini-boucle-agent.md)
faisait à la main.

## Le savoir

- **La mécanique** : le harnais (Pi) expose un point d'extension appelé
  à chaque tool_call avec `(outil, arguments)` ; le hook rend une
  décision — **allow / deny / ask**. Notre politique :
  - **deny** (liste noire) : `rm -rf`, écritures hors périmètre,
    commandes réseau sortantes non prévues, tout accès aux partages
    famille — le refus est motivé et loggé ;
  - **ask** (human-in-the-loop) : toute commande shell non listée,
    toute écriture — l'humain voit la commande *exacte* et tranche ;
  - **allow** : lectures dans le périmètre — le flux nominal reste
    fluide.
- **Les principes qui rendent la politique robuste** :
  - décider sur les **arguments résolus** (chemin absolu canonique,
    pas la chaîne brute — le path-traversal se joue là) ;
  - liste noire pour l'évidence, mais **default-ask** pour l'inconnu :
    une blacklist seule est toujours incomplète ;
  - le hook **logge tout** (décision comprise) — c'est aussi un outil
    d'observabilité ([6.1](../../../06-production/6.1-observabilite/6.1-observabilite.md)) ;
  - le hook ne fait *que* décider : pas de logique métier dedans.
- **Pourquoi un hook et pas « un bon prompt »** : le prompt est une
  *demande*, le hook est une *contrainte*. Un agent prompt-injecté
  ([5.3.1](../../../05-homelab-mcp/5.3-securite/5.3.1-prompt-injection-indirecte/5.3.1-prompt-injection-indirecte.md))
  ignore les demandes — il ne peut pas ignorer l'interception.

## En pratique

Extension Pi : hook `tool_call` avec politique en trois niveaux,
patterns de la liste noire dans un fichier de config versionné
(`.pi/`), log JSON par décision — et un test : demander à l'agent de
supprimer un fichier protégé, vérifier le deny + le log.

## Pièges connus

- Filtrer la chaîne de commande par regex naïve : `rm$IFS-rf`, alias,
  chemins relatifs — décider sur les arguments résolus, et garder
  default-ask.
- La fatigue de validation : si l'humain valide 40 fois par session,
  il validera sans lire — la politique doit rendre le « ask » rare
  (allow large sur les lectures sûres).
- Le hook silencieux : un deny sans explication → l'agent réessaie en
  boucle des variantes ; renvoyer la *raison* du refus dans le
  résultat d'outil.

## Question d'entretien

> « Comment empêchez-vous un agent d'exécuter une commande
> destructive ? »
> Interception de chaque tool_call, décision sur arguments résolus,
> liste noire + default-ask avec human-in-the-loop, journalisation
> complète — et un conteneur en dessous pour ce que le hook raterait
> ([3.1.2](../3.1.2-conteneur-moindre-privilege/3.1.2-conteneur-moindre-privilege.md)).

## Références

- [securite.md §5](../../../../homelab/architecture/securite.md) — le
  non-négociable d'origine
- Doc extensions/hooks de Pi
