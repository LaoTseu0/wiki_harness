"""
evals_comparatives.py — le meme jeu, une ligne de tableau par config.

La v0.0.2 n'existe que si elle bat la v0.0.1 SUR LE MEME JEU. Ce
harnais rejoue les 12 questions sur chaque configuration de chaine et
produit le tableau markdown du README — l'ABLATION : chaque ligne ne
change qu'UNE variable, pour attribuer chaque point gagne a sa cause.

Discipline statistique (lecon 2.2.5) : sur 12 questions, 1 point =
8 % — le harnais affiche donc aussi les BASCULES (quelles questions
changent d'etat entre deux configs), pas seulement les totaux.

Le score generation (appels LLM lents) est optionnel : GENERATION =
False mesure le retrieval seul en quelques secondes.

Prerequis : index.db (v0.0.1) ; Qdrant migre pour les configs qdrant+ ;
les trous de 05/06/07 remplis (exercices de la 2.1).
"""

import json
import sys
import time
from pathlib import Path
from importlib import import_module

MODULE = Path(__file__).resolve().parents[2]
V1 = MODULE / "2.1-v0.0.1-rag-a-la-main"
V2 = MODULE / "2.2-v0.0.2-qdrant-retrieval-avance"
sys.path.insert(0, str(MODULE))
sys.path.insert(0, str(V1 / "2.1.5-recherche-top-k"))
sys.path.insert(0, str(V2 / "2.2.2-retrieval-hybride"))

_m05 = import_module("05_rechercher")

JEU = MODULE / "evals" / "questions.json"
GENERATION = False   # True = rejouer aussi la generation (lent)
K = 5


# --- Les configurations : une fonction par ligne du tableau -----------
# Chaque config : (question) -> liste de (score, fichier, titre, texte).

def config_v1_brute_force(question):
    index = config_v1_brute_force.index
    return _m05.rechercher(question, index, K)


def config_hybride(question):
    from retrieval_hybride import chercher_hybride
    etat = config_hybride.etat
    resultats = chercher_hybride(question, *etat, k=K)
    return [(s, c["fichier"], c["titre"], c["texte"]) for s, c in resultats]


def preparer_configs() -> dict:
    """Ne charge que ce qui est disponible — chaque config manquante
    est annoncee, pas fatale (l'ablation se complete au fil de la 2.2)."""
    configs = {}

    config_v1_brute_force.index = _m05.charger_index()
    configs["v0.0.1 SQLite brute force"] = config_v1_brute_force

    try:
        from bm25 import calculer_idf, charger_chunks
        chunks = charger_chunks()
        idf = calculer_idf(chunks)
        avgdl = sum(c["longueur"] for c in chunks) / len(chunks)
        config_hybride.etat = (chunks, idf, avgdl)
        configs["+ hybride (RRF)"] = config_hybride
    except Exception as erreur:
        print(f"(config hybride indisponible : {erreur})")

    # A completer au fil de la section (une variable par ligne !) :
    #   "Qdrant seul"   -> rechercher_qdrant de la 2.2.1 (delta attendu
    #                      nul : meme embeddings — si ca bouge, bug) ;
    #   "+ re-ranking"  -> hybride puis rerank de la 2.2.3 ;
    #   "+ filtres"     -> chercher(question, k, filtres) de la 2.2.4.
    return configs


# --- Les metriques de la 2.1.7, reutilisees ---------------------------

def retrieval_ok(chunks, mots_cles) -> bool:
    textes = " ".join(x.lower() for _, _, _, x in chunks)
    return all(m.lower() in textes for m in mots_cles)


def generation_ok(question, chunks, mots_cles) -> bool:
    sys.path.insert(0, str(V1 / "2.1.6-rag-complet"))
    _m06 = import_module("06_rag")
    reponse = _m06.generer(_m06.construire_prompt(question, chunks))
    return all(m.lower() in reponse.lower() for m in mots_cles)


if __name__ == "__main__":
    questions = json.loads(JEU.read_text(encoding="utf-8"))
    configs = preparer_configs()
    n = len(questions)
    resultats = {}   # nom_config -> liste de bool (retrieval par question)

    lignes_markdown = ["| Config | Retrieval | Generation | Latence |",
                       "|---|---|---|---|"]
    for nom, chercher in configs.items():
        etats, gen_total = [], 0
        debut = time.perf_counter()
        for cas in questions:
            chunks = chercher(cas["question"])
            ok = retrieval_ok(chunks, cas["mots_cles"])
            etats.append(ok)
            if GENERATION:
                gen_total += generation_ok(cas["question"], chunks,
                                           cas["mots_cles"])
        latence = (time.perf_counter() - debut) / n
        resultats[nom] = etats
        gen = f"{gen_total}/{n}" if GENERATION else "—"
        lignes_markdown.append(
            f"| {nom} | {sum(etats)}/{n} | {gen} | {latence * 1000:.0f} ms |"
        )
        print(f"{nom:<30} retrieval {sum(etats)}/{n}")

    # Les bascules : ce que les totaux cachent (12 questions !).
    noms = list(resultats)
    if len(noms) >= 2:
        print(f"\nBascules {noms[0]} -> {noms[-1]} :")
        for cas, av, ap in zip(questions, resultats[noms[0]],
                               resultats[noms[-1]]):
            if av != ap:
                sens = "repechee" if ap else "PERDUE"
                print(f"   [{sens}] {cas['question'][:56]}")

    print("\nTableau pour le README (a coller tel quel, jamais recopie")
    print("a la main — piege de la 2.3.4) :\n")
    print("\n".join(lignes_markdown))
