# Mémoire versionnée

> [carte du cours](../carte.md)

## L'essentiel

La fenêtre de contexte est périssable — la mémoire d'un agent doit
vivre **ailleurs** : des fichiers markdown dans un dépôt git,
synchronisés par hooks de session (pull à l'ouverture, commit à la
fermeture). C'est le pattern « external memory » du context
engineering ([roadmap couche 0](../_archive/roadmap.md)), avec un bonus
décisif : la mémoire devient **diffable, auditable, réversible**.

## Le savoir

- **La mécanique OKF** (la convention du homelab) : un dépôt mémoire
  dédié ; hooks du harnais —
  - `session_start` → `git pull` + chargement des fichiers pertinents
    dans le contexte initial ;
  - `session_shutdown` → l'agent consolide ce qu'il a appris dans les
    fichiers → `git commit` (+ push).
- **Ce qui va en mémoire — et ce qui n'y va pas** : décisions et
  préférences durables, état des projets, leçons d'incidents — **pas**
  le transcript brut (c'est du bruit), pas ce que la doc du homelab
  sait déjà (une mémoire qui duplique sa source dérive, cf. le RAG du
  module 2 pour la connaissance documentaire).
- **Le protocole de consolidation** (l'étape difficile, à écrire
  comme un prompt) : (1) relire la session et lister des faits
  candidats ; (2) filtrer par trois questions — durable ? absent de
  la doc *et* de la mémoire existante ? utile à la prochaine
  session ? ; (3) en conflit avec l'existant, la version datée la
  plus récente l'emporte (l'ancienne reste dans l'historique git) ;
  (4) budget : quelques lignes par session, pas un compte rendu.
- **Pourquoi git, précisément** :
  - **audit** : `git log` répond à « pourquoi l'agent croit-il ça ? »
    — et `git blame` date la croyance ;
  - **rollback** : une mémoire polluée (erreur, ou injection
    [5.3.1](../mcp/prompt-injection-indirecte.md))
    se révoque par revert — une mémoire en base opaque, non ;
  - **le commit est un checkpoint** : la granularité session borne le
    rayon d'une pollution.
- **Structure de fichiers** : un index court chargé à chaque session +
  des fichiers thématiques chargés à la demande — la mémoire se
  *recherche*, elle ne se charge pas en bloc (sinon elle devient le
  problème de contexte qu'elle devait résoudre).

## En pratique

Hooks `session_start`/`session_shutdown` dans `.pi/`, dépôt mémoire
séparé du dépôt de code, template des fichiers (index + thèmes) — et
un test de bout en bout : apprendre un fait en session A, le retrouver
en session B, le corriger en session C et lire l'historique.

## Pièges connus

- Tout mémoriser : la mémoire enfle, le chargement sature le contexte,
  le signal se noie — la consolidation est une *sélection*.
- Le commit automatique sans relecture possible : garder les messages
  de commit descriptifs (« appris : X ; corrigé : Y ») — c'est eux
  qu'on auditera.
- Conflits git entre deux sessions parallèles : une seule session
  écrivaine à la fois, ou des fichiers par domaine — le problème est
  connu, le trancher explicitement.

## Se tester

> « Comment donnez-vous une mémoire long terme à un agent ? »
> Mémoire externe en fichiers versionnés, hooks de session
> (pull/consolidation/commit), index + chargement sélectif, audit et
> rollback par git — et la distinction mémoire (décisions apprises) vs
> RAG (connaissance documentaire).

## Références

- [Roadmap couche 0](../_archive/roadmap.md) — « mémoire externe » dans
  le context engineering
- La convention OKF du homelab
  ([architecture/jarvis.md](../../../homelab/architecture/jarvis.md))
