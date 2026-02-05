# Dogfooding

> [carte du cours](../carte.md)

## L'essentiel

Le framework n'a pas d'utilisateurs imaginaires : **ses utilisateurs
sont les modules 2-7 de ce repo**. Chaque module consomme les briques
existantes et fait remonter ce qui manque — le framework évolue sous
la pression d'usages réels, jamais sur spéculation. C'est la meilleure
protection contre l'API désagréable et la feature inutile.

## Le savoir

- **Le contrat de dogfooding** : un module a interdiction de recoder ce
  qu'une brique fait déjà, et obligation de remonter (issue, note dans
  PROGRESSION) ce qu'une brique fait mal. La friction ressentie est le
  signal de conception n°1.
- **Le calendrier de consommation** :

  | Module | Consomme | Fait évoluer |
  |---|---|---|
  | 2 (RAG) | client LLM | retrieval (`rag_commun` promu), evals |
  | 5 (MCP) | outils, retrieval | exposition d'outils via protocole |
  | 3 (agent) | boucle, outils | mémoire, garde-fous |
  | 4 (vLLM) | client (nouveau provider) | routage coût/latence |
  | 6 (prod) | evals | observabilité (traces) |

- **La boucle de promotion** : script qui marche → besoin ressenti
  ailleurs → extraction en brique + tests
  ([1.3.2](clean-code.md))
  → les deux usages migrent dessus. Jamais d'extraction avant le
  **deuxième** usage (règle des deux occurrences).
- **Pourquoi ça vaut de l'or en entretien** : « mon framework a cinq
  consommateurs réels et voici ce qu'ils m'ont fait changer » est un
  récit d'ingénierie ; « j'ai conçu une architecture » n'en est pas un.

## En pratique

À la fin de chaque module : une note « friction framework » dans son
PROGRESSION.md (ce qui a manqué, ce qui a gêné) → triage → incrément
semver. Le premier cas réel : le module 2 consommera le client LLM
extrait des scripts 01-03.

## Pièges connus

- Le framework qui devance ses usages : une brique sans consommateur
  est un passif (à maintenir) déguisé en actif.
- Casser les consommateurs en silence : dès deux modules dépendants,
  les changements passent par semver + tests contractuels.
- Dogfooding de complaisance : si le module contourne la brique « pour
  aller vite », le signal de friction est perdu — le contournement se
  documente ou se corrige.

## Se tester

> « Comment évitez-vous de construire un framework que personne
> n'utilise ? »
> En n'extrayant qu'au deuxième usage réel, en faisant des modules du
> parcours les premiers clients, et en traitant leur friction comme le
> backlog — le framework suit l'usage, jamais l'inverse.

## Références

- [PROGRESSION.md du module 2](../_archive/journal/progression-fondamentaux.md)
  — premier terrain de dogfooding
