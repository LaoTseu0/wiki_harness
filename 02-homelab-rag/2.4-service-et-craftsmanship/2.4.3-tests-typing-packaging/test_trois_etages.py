"""
test_trois_etages.py — les trois vitesses de test d'un systeme LLM.

Le principe de la lecon 2.4.3 : separer le deterministe (testable en
ms, sans reseau) du probabiliste (mesurable en evals, lent, GPU).
Trois etages, trois marqueurs pytest :

  1. UNITAIRES (defaut)          : le coeur deterministe — chunking,
     similarite, fusion RRF. Aucun reseau, aucun mock.
  2. INTEGRATION (@integration)  : la chaine sur un MINI-CORPUS dedie
     avec provider MOCKE a la frontiere (2.4.2 paye ici) — on teste
     NOTRE code, pas le modele.
  3. EVALS-AS-TESTS (@eval)      : assert score >= baseline — la
     non-regression de la 2.1.7, lancee avant chaque tag (lente, GPU).

Lancer :  pytest test_trois_etages.py -m "not eval"     (rapide)
          pytest test_trois_etages.py -m eval           (avant un tag)
Prerequis marqueurs (pyproject.toml ou pytest.ini) :
  [tool.pytest.ini_options]
  markers = ["integration: chaine avec mock", "eval: lent, GPU"]
"""

import sys
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE))

from rag_commun import similarite_cosinus

BASELINE_RETRIEVAL = 7   # la baseline chiffree de la 2.1.7 (7/12)


# --- Etage 1 : unitaires — ms, zero reseau ----------------------------

def test_cosinus_vecteurs_identiques():
    assert similarite_cosinus([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)


def test_cosinus_vecteurs_orthogonaux():
    assert similarite_cosinus([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_cosinus_insensible_a_la_longueur():
    # L'angle ne change pas si on double la longueur (2.1.2).
    assert similarite_cosinus([2.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)


def test_chunking_sections_preservees():
    from rag_commun import decouper_en_sections
    texte = "intro\n## Backup\nrsync quotidien\n## Reseau\nport 11434\n"
    sections = decouper_en_sections(texte, "test.md")
    titres = [s["titre"] for s in sections]
    assert "Backup" in titres and "Reseau" in titres


# --- Etage 2 : integration — mini-corpus, provider mocke --------------

@pytest.mark.integration
def test_chaine_avec_provider_mocke(monkeypatch):
    """Le mock vit A LA FRONTIERE provider : un faux embedder previsible
    suffit a tester tri et top-k — le comportement du MODELE, lui,
    appartient aux evals (melanger les deux rend la CI non deterministe)."""
    import rag_commun

    # Faux espace 2D : "backup" -> [1, 0], tout le reste -> [0, 1].
    def faux_embedder(texte):
        return [1.0, 0.0] if "backup" in texte.lower() else [0.0, 1.0]

    monkeypatch.setattr(rag_commun, "embedder", faux_embedder)
    index = [
        ("nas.md", "Backup", "le backup se fait par rsync", [1.0, 0.0]),
        ("reseau.md", "Ports", "ollama ecoute sur 11434", [0.0, 1.0]),
    ]
    v_q = rag_commun.embedder("comment marche le backup ?")
    scores = sorted(
        ((rag_commun.similarite_cosinus(v_q, v), f) for f, _, _, v in index),
        reverse=True,
    )
    assert scores[0][1] == "nas.md"   # le tri remonte le bon document


# --- Etage 3 : evals-as-tests — lent, GPU, avant chaque tag -----------

@pytest.mark.eval
def test_non_regression_retrieval():
    """La baseline en assertion : si un changement de chunking/k/modele
    fait tomber le score sous 7/12, ce test le dit AVANT le tag."""
    import json
    from importlib import import_module

    sys.path.insert(0, str(MODULE / "2.1-v0.0.1-rag-a-la-main"
                           / "2.1.5-recherche-top-k"))
    _m05 = import_module("05_rechercher")
    index = _m05.charger_index()
    questions = json.loads(
        (MODULE / "evals" / "questions.json").read_text(encoding="utf-8")
    )
    score = sum(
        all(m.lower() in " ".join(x.lower() for _, _, _, x in
                                  _m05.rechercher(cas["question"], index, 3))
            for m in cas["mots_cles"])
        for cas in questions
    )
    assert score >= BASELINE_RETRIEVAL, (
        f"regression retrieval : {score}/12 < baseline "
        f"{BASELINE_RETRIEVAL}/12"
    )
