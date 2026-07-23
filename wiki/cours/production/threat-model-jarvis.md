# Threat model Jarvis

> [carte du cours](../carte.md)

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
    conteneur [conteneur et moindre privilège](../agent/conteneur-moindre-privilege.md),
    hook [hook tool_call](../agent/hook-tool-call.md),
    lecture seule MCP [serveur MCP Python](../mcp/serveur-mcp-python.md),
    token HA limité [outil home_assistant](../agent/outil-home-assistant.md) ;
  - **risque résiduel assumé** : ce qui reste, et pourquoi c'est
    acceptable à cette échelle.
- **La question qui structure tout** : « si l'agent est compromis,
  quel est le rayon des dégâts ? » — et la réponse, par construction :
  son workspace, deux endpoints, un token limité. Un threat model qui
  ne sait pas répondre à ça n'en est pas un
  ([conteneur et moindre privilège](../agent/conteneur-moindre-privilege.md)).
- **Le registre métier** : « moindre privilège », « défense en
  profondeur », « human-in-the-loop », « rayon de souffle », « risque
  résiduel » — les termes des offres
,
  pas le jargon homelab.
- **Le lien souveraineté** : local-first = données qui ne sortent pas
  = argument RGPD — le threat
  model le formalise.

## En pratique

Écrire la page (actifs / surfaces / menaces / défenses / résiduel) dans
`architecture/` du homelab, la relire du point de vue d'un recruteur
non-homelab, et en extraire une version portfolio expurgée (pas d'IP,
pas de détails famille).

## Pièges connus

- Le threat model catalogue de menaces sans défenses ni résiduel :
  incomplet — chaque menace se termine par sa mitigation et ce qui
  reste.
- Le théâtre de la menace (APT étatiques sur un homelab) : crédibilité
  perdue — des acteurs réalistes pour l'échelle.
- La page jamais reliée aux tests : un threat model se **vérifie** par
  les [tests adversariaux](tests-adversariaux.md) —
  sinon c'est de la fiction rassurante.

## Se tester

> « Décrivez le modèle de menace de votre agent. »
> Actifs (partages, credentials, domotique), surfaces (question,
> corpus, outils), menaces réalistes, défenses en profondeur (conteneur
> + hook + lecture seule + token limité), rayon de dégâts borné par
> construction, risque résiduel assumé — et vérifié par mes tests
> adversariaux.

## Références

- [securite.md](../../../../homelab/architecture/securite.md) — la base
  à traduire
- [Tests adversariaux](tests-adversariaux.md)
  — la vérification empirique du modèle
