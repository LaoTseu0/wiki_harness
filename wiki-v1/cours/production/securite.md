# Sécurité

> [carte du cours](../carte.md)

## Vue d'ensemble

Connaître les attaques par cœur, les mener soi-même, documenter les
défenses — en vocabulaire métier. Trois leçons : le référentiel (OWASP
Top 10 LLM), la pratique offensive (tests adversariaux sur son propre
système), et la synthèse défensive (le threat model de Jarvis, en
termes qu'un recruteur comprend).

## Contenu

- **[OWASP Top 10 LLM](owasp-top-10-llm.md)**
      — lire et savoir restituer
- **[Tests adversariaux](tests-adversariaux.md)**
      — attaquer son RAG/agent, documenter les défenses
- **[Threat model Jarvis](threat-model-jarvis.md)**
      — la page threat model en vocabulaire métier

## Synthèse

La sécurité du parcours n'est pas un module isolé mais la
**capitalisation** de ce qui est déjà en place : le confinement du
domaine agent, la lecture seule du domaine MCP, l'injection éprouvée en
[prompt injection indirecte](../mcp/prompt-injection-indirecte.md).
OWASP donne le vocabulaire, les tests adversariaux donnent les preuves,
le threat model donne le récit. **Auto-contrôle** : savoir répondre à
« quels risques pour un agent avec accès fichiers ? » (question n°5) en
citant OWASP ET sa propre démo.

## Références

- OWASP GenAI, Simon Willison
