# Le versant sécurité

> [carte du cours](../carte.md)

## Vue d'ensemble

Attaquer son propre serveur avant les autres : brancher un système
d'outils sur un corpus documentaire ouvre **la** faille classe des
LLM — la prompt injection indirecte, via un document indexé qui
contient une instruction. Une leçon unique, dense, et un sujet
d'entretien certain.

## Contenu

- **[5.3.1 Prompt injection indirecte](prompt-injection-indirecte.md)**
      — le document piégé, la démonstration sur notre chaîne, les
      défenses

## Synthèse

La leçon installe le réflexe qui restera pour tout le parcours : **tout
contenu qui entre dans la fenêtre est une entrée non fiable** — les
documents du RAG comme les résultats d'outils. Les défenses (séparation
données/instructions, lecture seule, moindre privilège,
human-in-the-loop) sont déjà dans l'architecture des modules 3 et 5 ;
cette section les *éprouve*. Le test adversarial systématique arrive en
[6.2](../production/securite.md).
**Auto-contrôle** : savoir dérouler le scénario d'attaque complet sur
notre propre chaîne, et pour chaque étape, nommer la défense qui la
casse.

## Livrable du module

`05-homelab-mcp/`.
**CV** : « authored an MCP server and client » — déjà demandé tel quel
dans des offres.
