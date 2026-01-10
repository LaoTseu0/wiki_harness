# 6.2.3 Threat model Jarvis

> **Leçon de la section [6.2 Sécurité](../6.2-securite.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Rassembler tout le versant sécurité en une **page threat model** de
l'agent Jarvis, écrite en vocabulaire métier — le document qui répond,
à froid et par écrit, à « quels risques, quelles défenses, quel rayon
de dégâts ». À moitié déjà fait dans
[securite.md](../../../../homelab/architecture/securite.md) ; ici, on le
traduit pour un recruteur.

## Le savoir

- **La structure d'un threat model lisible** :
  - **actifs** : ce qu'on protège — partages famille, credentials HA,
    intégrité de la domotique, données personnelles ;
  - **surfaces d'entrée** : question utilisateur, corpus RAG (injection
    indirecte), résultats d'outils, mémoire versionnée ;
  - **acteurs de menace** : injection via document, utilisateur
    malveillant, dépendance compromise — réalistes pour un homelab,
    pas du théâtre APT ;
  - **défenses par actif** (ce qui existe déjà, lié) : confinement
    conteneur [3.1.2](../../../03-jarvis-agent/3.1-garde-fous-et-securite/3.1.2-conteneur-moindre-privilege/3.1.2-conteneur-moindre-privilege.md),
    hook [3.1.1](../../../03-jarvis-agent/3.1-garde-fous-et-securite/3.1.1-hook-tool-call/3.1.1-hook-tool-call.md),
    lecture seule MCP [5.1.1](../../../05-homelab-mcp/5.1-serveur/5.1.1-serveur-mcp-python/5.1.1-serveur-mcp-python.md),
    token HA limité [3.2.1](../../../03-jarvis-agent/3.2-outils-et-memoire/3.2.1-outil-home-assistant/3.2.1-outil-home-assistant.md) ;
  - **risque résiduel assumé** : ce qui reste, et pourquoi c'est
    acceptable à cette échelle.
- **La question qui structure tout** : « si l'agent est compromis,
  quel est le rayon des dégâts ? » — et la réponse, par construction :
  son workspace, deux endpoints, un token limité. Un threat model qui
  ne sait pas répondre à ça n'en est pas un
  ([3.1.2](../../../03-jarvis-agent/3.1-garde-fous-et-securite/3.1.2-conteneur-moindre-privilege/3.1.2-conteneur-moindre-privilege.md)).
- **Le registre métier** : « moindre privilège », « défense en
  profondeur », « human-in-the-loop », « rayon de souffle », « risque
  résiduel » — les termes des offres
  ([roadmap §10.1](../../../roadmap.md), guardrails/RGPD chez GRDF),
  pas le jargon homelab.
- **Le lien souveraineté** : local-first = données qui ne sortent pas
  = argument RGPD ([roadmap §10.3](../../../roadmap.md)) — le threat
  model le formalise.

## En pratique

Écrire la page (actifs / surfaces / menaces / défenses / résiduel) dans
`architecture/` du homelab, la relire du point de vue d'un recruteur
non-homelab, et en extraire une version portfolio expurgée (pas d'IP,
pas de détails famille — [P.1.1](../../../transverse-portfolio/p.1-repos-publics/p.1.1-github-public/p.1.1-github-public.md)).

## Pièges connus

- Le threat model catalogue de menaces sans défenses ni résiduel :
  incomplet — chaque menace se termine par sa mitigation et ce qui
  reste.
- Le théâtre de la menace (APT étatiques sur un homelab) : crédibilité
  perdue — des acteurs réalistes pour l'échelle.
- La page jamais reliée aux tests : un threat model se **vérifie** par
  les [tests adversariaux](../6.2.2-tests-adversariaux/6.2.2-tests-adversariaux.md) —
  sinon c'est de la fiction rassurante.

## Question d'entretien

> « Décrivez le modèle de menace de votre agent. »
> Actifs (partages, credentials, domotique), surfaces (question,
> corpus, outils), menaces réalistes, défenses en profondeur (conteneur
> + hook + lecture seule + token limité), rayon de dégâts borné par
> construction, risque résiduel assumé — et vérifié par mes tests
> adversariaux.

## Références

- [securite.md](../../../../homelab/architecture/securite.md) — la base
  à traduire
- [6.2.2 Tests adversariaux](../6.2.2-tests-adversariaux/6.2.2-tests-adversariaux.md)
  — la vérification empirique du modèle
