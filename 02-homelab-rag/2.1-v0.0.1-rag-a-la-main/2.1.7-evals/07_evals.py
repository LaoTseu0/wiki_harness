"""
07_evals.py — mesurer le RAG. LA competence qui trie en entretien.

"Comment evaluez-vous votre systeme ?" : 90 % des candidats n'ont pas de
reponse (ta propre enquete de terrain, roadmap section 10.3). Un RAG sans
eval chiffree est une demo, pas de l'ingenierie. On construit donc un
banc de test : un jeu de questions dont on connait la reponse, et un
score automatique — reproductible avant/apres chaque changement (le
"test de non-regression" applique aux LLM).

Le jeu : evals/questions.json — 12 questions, chacune avec le mot-cle
factuel attendu dans la reponse (ex. "rsync" pour le backup). A etendre
vers ~30 pour un vrai jeu (c'est du travail de curation, note au backlog).

Deux metriques DETERMINISTES (pas de LLM juge ici — rapides, fiables,
100 % reproductibles) :
  - RETRIEVAL : le mot-cle apparait-il dans un des chunks du top-k ?
    = "a-t-on mis la reponse dans le contexte ?" Mesure le "R" seul.
  - GENERATION : le mot-cle apparait-il dans la reponse finale ?
    = bout-en-bout, "le modele a-t-il produit le bon fait ?"

Lire l'ecart entre les deux est un diagnostic : generation < retrieval
=> le contexte etait bon mais le modele l'a rate (probleme de prompt ou
de modele). retrieval bas => probleme de chunking/recherche (le vrai
sujet de la v2). C'est la demarche "debug par couche" attendue en
entretien.

Plus tard (couche T de la roadmap) : le LLM-as-judge (un modele note la
qualite/fidelite — souple mais a calibrer), puis RAGAS/DeepEval en fin
de module pour parler l'outillage standard.

=== EXERCICE ===================================================
Completer les DEUX fonctions de mesure (petites, deterministes).
Le harnais (boucle, chargement du jeu, tableau) est fourni.

1. chunk_contient_reponse(chunks, mots_cles) -> bool
   chunks : liste de (score, fichier, titre, texte).
   Renvoyer True si CHAQUE mot-cle (compare en minuscules) apparait
   dans le texte concatene des chunks.
   Indice : textes = " ".join(x.lower() for _, _, _, x in chunks)
            puis all(m.lower() in textes for m in mots_cles)

2. reponse_contient(reponse, mots_cles) -> bool
   Renvoyer True si chaque mot-cle (en minuscules) est dans `reponse`
   (en minuscules). Meme motif "all(... in ...)".

Attendu (retrieval reproductible a l'identique ; generation stable
grace a temperature=0/seed, peut bouger de +/-1) :
   retrieval  : 7/12
   generation : 7/12
Lecture : les 5 echecs sont des echecs de RETRIEVAL (le bon chunk
n'est pas remonte) — et le modele, lui, ne se rattrape jamais en
inventant : il dit "je ne sais pas". Retrieval == generation =>
zero hallucination. La v1 est HONNETE mais sa recherche est
mediocre. C'est le point de depart chiffre que la v2 doit battre.
================================================================
"""

import json
import sys

from pathlib import Path
from importlib import import_module

# Le script vit dans son dossier de lecon ; les scripts 05 et 06 sont
# dans les leurs, et rag_commun.py a la racine du module. On ajoute
# les trois emplacements au chemin de recherche des imports.
MODULE = Path(__file__).resolve().parents[2]
V1 = MODULE / "2.1-v0.0.1-rag-a-la-main"
sys.path.insert(0, str(MODULE))
sys.path.insert(0, str(V1 / "2.1.5-recherche-top-k"))
sys.path.insert(0, str(V1 / "2.1.6-rag-complet"))

_m06 = import_module("06_rag")
charger_index = import_module("05_rechercher").charger_index
rechercher = import_module("05_rechercher").rechercher
construire_prompt = _m06.construire_prompt
generer = _m06.generer

# Le jeu de questions vit a la racine du module (evals/), partage par
# toutes les generations — plus de dependance a l'emplacement du repo
# homelab pour les evals elles-memes.
JEU = MODULE / "evals" / "questions.json"


def chunk_contient_reponse(chunks: list[tuple], mots_cles: list[str]) -> bool:
    """True si tous les mots-cles sont presents dans le texte des chunks."""
    ...  # A COMPLETER


def reponse_contient(reponse: str, mots_cles: list[str]) -> bool:
    """True si tous les mots-cles sont presents dans la reponse."""
    ...  # A COMPLETER


def evaluer():
    questions = json.loads(JEU.read_text(encoding="utf-8"))
    index = charger_index()
    retrieval_ok = generation_ok = 0

    print(f"{'RETR':>4} {'GEN':>4}  question")
    print("-" * 64)
    for cas in questions:
        chunks = rechercher(cas["question"], index, k=3)
        r_ok = chunk_contient_reponse(chunks, cas["mots_cles"])
        reponse = generer(construire_prompt(cas["question"], chunks))
        g_ok = reponse_contient(reponse, cas["mots_cles"])
        retrieval_ok += r_ok
        generation_ok += g_ok
        print(f"{'OK' if r_ok else 'MISS':>4} {'OK' if g_ok else 'MISS':>4}  "
              f"{cas['question'][:52]}")

    n = len(questions)
    print("-" * 64)
    print(f"retrieval  (mot-cle dans un chunk du top-3) : {retrieval_ok}/{n}  (attendu 7/12)")
    print(f"generation (mot-cle dans la reponse)         : {generation_ok}/{n}  (attendu 7/12)")


if __name__ == "__main__":
    evaluer()
