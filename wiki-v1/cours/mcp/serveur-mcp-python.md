# Serveur MCP Python

> [carte du cours](../carte.md)

## L'essentiel

Un serveur MCP est un **exposeur d'outils** : il déclare des fonctions
typées, le protocole les rend découvrables (`tools/list`) et
appelables (`tools/call`) par n'importe quel host. Le nôtre expose le
homelab **en lecture seule** : état des conteneurs, entités HA,
recherche dans la doc — trois outils, trois sources, zéro écriture.

## Le savoir

- **Le SDK officiel (FastMCP)** : un outil = une fonction Python
  décorée ; la signature typée + la docstring **deviennent** le schéma
  JSON publié — le design d'outil de la
  [function calling à la main](../fondamentaux/function-calling.md)
  s'applique tel quel (description = prompt engineering, sorties
  compactes).
- **Les trois outils du serveur** :
  - `conteneurs_status()` — état docker (via socket en RO ou API) :
    nom, état, santé — résumé, pas le JSON brut ;
  - `ha_entites(filtre)` — états HA en lecture, liste blanche
    d'entités (même périmètre que la
    [outil home_assistant](../agent/outil-home-assistant.md) —
    le savoir-faire est partagé) ;
  - `chercher_doc(question, k)` — appelle le **service RAG** du
    domaine retrieval (`POST /ask`,
    [service FastAPI](../framework/service.md)) :
    réutilisation, pas duplication — le serveur MCP est un *adaptateur*
    de protocole, la logique reste dans le service.
- **Lecture seule par conception** : aucune écriture exposée — le
  moindre privilège du
  [garde-fous et sécurité d'abord](../agent/garde-fous.md)
  appliqué au protocole ; et la surface d'injection
  ([prompt injection indirecte](prompt-injection-indirecte.md))
  reste bornée à l'exfiltration, pas à l'action.
- **Le coût en contexte, à concevoir — et à mesurer** : chaque outil
  découvert entre dans la fenêtre du host : trois
  outils bien décrits, pas quinze. Le chiffre s'obtient en comptant
  les tokens des `inputSchema` renvoyés par `tools/list` tels
  qu'injectés dans la fenêtre — le mesurer pour *son* serveur, c'est
  fonder la règle au lieu de la réciter.
- **Quand MCP, quand outil natif** (la règle que le vécu Pi impose) :
  MCP se justifie à partir de **deux hosts consommateurs** ou d'un
  besoin d'interopérabilité hors harnais ; pour un seul harnais
  maison, `registerTool`
  ([outil home_assistant](../agent/outil-home-assistant.md))
  reste moins cher (pas de handshake, pas de schémas re-découverts à
  chaque session). L'arbitrage est celui du périmètre : MCP se paye en
  handshake et en contexte, et se rembourse dès qu'un deuxième host
  consomme les mêmes outils.

## En pratique

`serveur.py` (FastMCP) : les trois outils, périmètres en config,
timeouts sur les backends (docker/HA/RAG), erreurs renvoyées comme
`isError` propre — testable dès maintenant avec l'inspector MCP, avant
même le [transport HTTP](transports-stdio-http.md).

## Pièges connus

- L'outil bavard : renvoyer 80 entités HA sature la fenêtre du host —
  filtres obligatoires et résumés côté serveur.
- Ré-implémenter le retrieval dans le serveur « pour éviter une
  dépendance » : deux chaînes RAG à maintenir divergeront — appeler le
  service.
- Une exception backend qui crashe le serveur : chaque outil attrape et
  renvoie une erreur MCP — un serveur d'outils ne meurt pas d'un
  conteneur arrêté.

## Se tester

> « Qu'expose un serveur MCP, et comment le concevez-vous ? »
> Des outils typés découvrables (nom, description, inputSchema), ici
> en lecture seule sur trois sources, sorties compactes pour la
> fenêtre du host, logique déléguée aux services existants — le
> serveur est un adaptateur de protocole, pas une application.

## Références

- SDK MCP Python (FastMCP) + MCP Inspector
- [Handshake MCP](handshake-mcp.md)
  — ce que le SDK enrobe
