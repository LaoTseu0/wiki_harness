"""Les clients LLM.

Un seul provider pour l'instant : Ollama. Pas d'interface commune tant
qu'il n'y a pas de deuxieme implementation — le premier provider s'ecrit
en direct (cours/framework/architecture-modulaire.md, piege de
l'abstraction prematuree).
"""

from framework.llm.ollama import ClientOllama, Reponse

__all__ = ["ClientOllama", "Reponse"]
