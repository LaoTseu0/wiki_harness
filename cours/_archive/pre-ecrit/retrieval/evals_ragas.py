"""
evals_ragas.py — passer notre jeu dans l'outillage standard.

Pas pour remplacer le script maison (assume — c'est lui qu'on sait
deboguer et qui tourne sans dependance) : pour parler le vocabulaire
des offres et VERIFIER que nos metriques mesurent la meme chose.

Les quatre metriques RAGAS, mappees sur les notres :
  - faithfulness      ~= notre score hallucination, inverse ;
  - answer_relevancy  : la reponse repond-elle a la question ?
  - context_precision ~= notre score retrieval, en plus fin ;
  - context_recall    : le contexte couvre-t-il la reponse attendue ?
Toutes sont des LLM-as-judge PACKAGES : les biais de la 2.3.2
s'appliquent, et la regle juge != generateur reste — d'ou le piege
n.1 de la lecon : sans configuration explicite, RAGAS juge avec une
API OpenAI par defaut (cout surprise + violation de la regle).

L'exercice de verite : correler ces scores avec notre tableau maison
sur les memes questions. Convergence = confiance ; divergence =
comprendre QUI mesure quoi.

Prerequis : pip install ragas datasets langchain-ollama ; la chaine
v0.0.1 complete (trous remplis) pour produire les reponses.
"""

import json
import sys
from pathlib import Path
from importlib import import_module

MODULE = Path(__file__).resolve().parents[2]
V1 = MODULE / "2.1-v0.0.1-rag-a-la-main"
sys.path.insert(0, str(MODULE))
sys.path.insert(0, str(V1 / "2.1.5-recherche-top-k"))
sys.path.insert(0, str(V1 / "2.1.6-rag-complet"))

JEU = MODULE / "evals" / "questions.json"
MODELE_JUGE = "gemma3:4b"   # juge != generateur, comme en 2.3.2

try:
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import (answer_relevancy, context_precision,
                               context_recall, faithfulness)
    from langchain_ollama import ChatOllama, OllamaEmbeddings
except ImportError:
    raise SystemExit("outillage absent — pip install ragas datasets "
                     "langchain-ollama (voir docstring)")

from rag_commun import MODELE_EMBED, OLLAMA


def produire_jeu_ragas() -> Dataset:
    """Adapte notre jeu au format RAGAS : question, answer, contexts,
    ground_truth — en faisant tourner NOTRE chaine v0.0.1."""
    _m05 = import_module("05_rechercher")
    _m06 = import_module("06_rag")
    index = _m05.charger_index()

    lignes = {"question": [], "answer": [], "contexts": [],
              "ground_truth": []}
    for cas in json.loads(JEU.read_text(encoding="utf-8")):
        chunks = _m05.rechercher(cas["question"], index, k=3)
        reponse = _m06.generer(_m06.construire_prompt(cas["question"], chunks))
        lignes["question"].append(cas["question"])
        lignes["answer"].append(reponse)
        lignes["contexts"].append([texte for _, _, _, texte in chunks])
        # Notre jeu n'a que des mots-cles : le ground_truth minimal est
        # le mot-cle en phrase — a enrichir avec le jeu etendu (~30).
        lignes["ground_truth"].append(
            f"La reponse mentionne : {', '.join(cas['mots_cles'])} "
            f"(source : {cas['fichier_attendu']})."
        )
    return Dataset.from_dict(lignes)


if __name__ == "__main__":
    jeu = produire_jeu_ragas()

    # Configuration EXPLICITE du juge et des embeddings : jamais le
    # defaut (API OpenAI silencieuse). Notre regle, notre modele.
    resultat = evaluate(
        jeu,
        metrics=[faithfulness, answer_relevancy,
                 context_precision, context_recall],
        llm=ChatOllama(model=MODELE_JUGE, base_url=OLLAMA, temperature=0),
        embeddings=OllamaEmbeddings(model=MODELE_EMBED, base_url=OLLAMA),
    )
    print(resultat)

    print("\nExercice de verite (lecon 2.3.3) : correler ces scores avec")
    print("le tableau maison — si notre score generation diverge, c'est")
    print("souvent qu'il MELANGE ce que RAGAS separe (faithfulness vs")
    print("answer_relevancy). Quatre metriques comprises battent dix")
    print("recitees : une phrase d'interpretation par metrique au README.")
