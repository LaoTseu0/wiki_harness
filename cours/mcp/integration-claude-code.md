# Intégration Claude Code

> [carte du cours](../carte.md)

## L'essentiel

Un serveur ne vaut que branché : connecter le serveur homelab à un
**client réel** (Claude Code), vérifier la découverte et l'usage
spontané des outils, et écrire la **doc d'intégration** — le livrable
qui prouve que quelqu'un d'autre peut le faire en cinq minutes.

## Le savoir

- **La configuration côté host** : Claude Code lit une config MCP
  (fichier `.mcp.json` au niveau projet, ou config utilisateur) —
  pour stdio : commande + arguments + variables d'environnement du
  serveur. Au lancement, le host démarre le sous-processus, fait le
  [handshake](handshake-mcp.md),
  et les outils apparaissent.
- **Le test qui compte — l'usage *spontané*** : ne pas dire « utilise
  l'outil chercher_doc » mais poser la question métier (« qu'est-ce
  qu'on avait décidé pour le backup du NAS ? ») et observer si le
  modèle **choisit** l'outil. S'il ne le fait pas, la description de
  l'outil est en cause
  ([5.1.1](serveur-mcp-python.md)) —
  itérer dessus est du prompt engineering mesurable.
- **La doc d'intégration, structure minimale** (en anglais — portfolio) :
  prérequis, la config à copier, les trois outils avec un exemple de
  question chacun, limites connues (lecture seule, périmètres), et un
  dépannage court (serveur ne démarre pas → tester avec l'inspector ;
  outils invisibles → vérifier le handshake dans les logs).
- **La boucle du parcours se referme** : Claude Code (host) découvre
  via MCP des outils qui interrogent le RAG maison — chaque couche de
  la pile est à nous, et démontrable en une démo de deux minutes.
  C'est l'artefact d'entretien du module.

## En pratique

`.mcp.json` versionné dans le repo (sans secrets — les tokens en
variables d'environnement), scénario de démo écrit (trois questions,
une par outil), doc d'intégration dans le README du module — testée en
conditions réelles : config depuis zéro, chrono en main.

## Pièges connus

- Le serveur qui marche à l'inspector mais pas dans Claude Code :
  presque toujours l'environnement (PATH, venv, variables absentes de
  la config) — la config MCP doit être autoporteuse.
- Des outils que le modèle n'utilise jamais : descriptions vagues ou
  redondantes avec ce qu'il croit savoir — les réécrire du point de
  vue du *modèle qui choisit*.
- Une doc d'intégration jamais testée depuis zéro : elle rate toujours
  une étape « évidente » — la faire dérouler par quelqu'un d'autre (ou
  soi-même sur une machine propre).

## Se tester

> « Comment intègre-t-on un serveur MCP à un assistant existant ? »
> Config déclarative côté host (commande stdio ou URL HTTP), handshake
> automatique, outils découverts dans la fenêtre — puis itération sur
> les descriptions jusqu'à l'usage spontané, et une doc d'intégration
> testée depuis zéro.

## Références

- Doc MCP de Claude Code (`.mcp.json`)
- Le README du module — la doc d'intégration en est une section
