# Socle sans framework

> [carte du cours](../carte.md)

## Vue d'ensemble

Écrire chaque mécanisme fondamental en **Python pur**, sans framework,
contre l'Ollama du homelab — comprendre sous le capot avant d'adopter le
moindre outil. Les cinq leçons forment ensemble l'**anatomie de toute
application LLM** : parler au modèle (chat), régler sa génération
(sampling), le faire agir (function calling), le faire boucler (agent),
fiabiliser ses sorties (structured output). Tout ce que LangChain ou un
SDK feront plus tard est déjà là, en ~200 lignes à chaque fois.

## Contenu

- **[1.1.1 Chat CLI, historique et contexte](chat-historique-contexte.md)**
      — modèle stateless, streaming, troncature et compaction à la main
- **[1.1.2 Sampling](sampling.md)**
      — temperature, top-k, top-p, le tirage et la portée de la seed
- **[Prompting](prompting.md)**
      — zero/few-shot, chain-of-thought, ReAct, prompt système
- **[1.1.3 Function calling à la main](function-calling.md)**
      — schémas JSON, parsing, exécution, renvoi (= ReAct implémenté)
- **[1.1.4 Mini-boucle d'agent](boucle-agent.md)**
      — pattern Pi : read/write/edit/bash dans une boucle while
- **[1.1.5 Structured output](structured-output.md)**
      — extraction JSON validée Pydantic, retry sur JSON invalide

## Synthèse

Les cinq briques se recomposent en une seule phrase : *un chat (1.1.1)
dont on maîtrise la génération (1.1.2) peut appeler des outils (1.1.3)
en boucle (1.1.4) et rendre des sorties fiables (1.1.5) — c'est un
agent.* Chaque module suivant ne fait que spécialiser une de ces
briques : le RAG enrichit le contexte, le MCP standardise les outils,
le framework maison les industrialise.
**Se tester** : savoir expliquer, au niveau HTTP/JSON, ce qui se passe
entre « le modèle décide d'appeler un outil » et « le modèle reçoit le
résultat ».

## Les étapes

Les 8 scripts, de [01_hello.py](../../etapes/fondamentaux/01_hello.py)
à [08_structured.py](../../etapes/fondamentaux/08_structured.py) —
à lire et à exécuter dans l'ordre.
