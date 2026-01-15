"""
juge.py — noter les reponses du RAG avec un LLM... calibre.

Les scores deterministes (2.1.7) plafonnent : "la reponse contient le
mot-cle" rate les bonnes reponses reformulees. Le juge LLM note avec
souplesse — a condition de respecter les regles de la lecon 2.3.2 :

  - JUGE != GENERATEUR : jamais Qwen3 4B jugeant Qwen3 4B (biais
    d'auto-preference). Hierarchie des risques : la CAPACITE du juge
    d'abord, l'identite ensuite — le juge se configure ci-dessous et
    le choix se documente dans le README ;
  - RUBRIQUE PAR AXE, pas de note globale : exactitude / fidelite /
    completude / abstention — moyenner trop tot perd le diagnostic ;
  - ECHELLE ANCREE 1-4 (une echelle 1-10 n'est jamais utilisee en
    bas — biais de complaisance) ;
  - SORTIE CONTRAINTE (1.1.5) : {score, justification} par axe ;
  - CALIBRATION : noter 10 reponses a la main, comparer au juge ;
    s'il diverge sur plus de 2, reecrire la RUBRIQUE (pas le juge).

Prerequis : un modele juge DIFFERENT tire sur Ollama (ex. un gemma ou
un llama pulle pour l'occasion) ou une API cloud ponctuelle via le
backend commutable (2.4.2).
"""

import json
import sys
from pathlib import Path

import httpx

MODULE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE))

from rag_commun import OLLAMA

# Le juge : DIFFERENT du generateur (Qwen3 4B). A ajuster selon ce qui
# est disponible — et a documenter dans le README (regle du module).
MODELE_JUGE = "gemma3:4b"

AXES = {
    "exactitude": "La reponse est-elle factuellement correcte par "
                  "rapport a la reponse attendue ?",
    "fidelite": "Chaque affirmation de la reponse est-elle soutenue "
                "par les sources fournies ?",
    "completude": "La reponse couvre-t-elle tous les elements "
                  "attendus ?",
    "abstention": "Si les sources ne permettaient pas de repondre, la "
                  "reponse le dit-elle (au lieu d'inventer) ?",
}

# Echelle 1-4 ANCREE : chaque barreau est defini, pas laisse au gout
# du juge. La rubrique demande l'EQUIVALENCE SEMANTIQUE, pas la
# paraphrase exacte (piege : un juge qui voit la reponse attendue mot
# pour mot exige le mot pour mot).
ECHELLE = ("1 = contredit la reference ou les sources ; "
           "2 = partiellement juste, manques importants ; "
           "3 = juste sur l'essentiel, detail manquant ; "
           "4 = equivalent a la reference (reformulation acceptee)")

SCHEMA_VERDICT = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "minimum": 1, "maximum": 4},
        "justification": {"type": "string"},
    },
    "required": ["score", "justification"],
}


def juger_axe(axe: str, question: str, attendue: str, produite: str,
              sources: str) -> dict:
    """Un appel par axe : {score 1-4, justification} en sortie contrainte."""
    reponse = httpx.post(
        f"{OLLAMA}/api/chat",
        json={
            "model": MODELE_JUGE,
            "messages": [
                {"role": "system",
                 "content": f"Tu evalues la reponse d'un systeme RAG sur "
                 f"UN critere : {AXES[axe]} Echelle : {ECHELLE}. Juge "
                 f"l'equivalence de sens, pas la formulation."},
                {"role": "user",
                 "content": f"Question : {question}\n\n"
                 f"Reponse attendue (reference) : {attendue}\n\n"
                 f"Sources fournies au systeme :\n{sources[:2000]}\n\n"
                 f"Reponse produite : {produite}"},
            ],
            "stream": False,
            "format": SCHEMA_VERDICT,
            "options": {"temperature": 0, "seed": 42, "num_predict": 200},
        },
        timeout=180,
    )
    reponse.raise_for_status()
    return json.loads(reponse.json()["message"]["content"])


def juger(question: str, attendue: str, produite: str, sources: str) -> dict:
    """Tous les axes — SEPARES : fidelite 4/4 mais completude 1/4 =
    probleme de retrieval, pas de grounding (le diagnostic survit)."""
    return {axe: juger_axe(axe, question, attendue, produite, sources)
            for axe in AXES}


if __name__ == "__main__":
    # Demonstration de calibration sur un cas jouet : la vraie
    # calibration se fait sur 10 reponses REELLES notees a la main.
    verdicts = juger(
        question="Qu'est-ce qu'on avait decide pour le backup du NAS ?",
        attendue="Un rsync quotidien planifie par cron vers le second "
                 "disque, decision notee dans backlog.md.",
        produite="La sauvegarde du NAS se fait par une synchronisation "
                 "rsync programmee chaque nuit.",
        sources="[backlog.md > NAS] Backup : rsync quotidien via cron...",
    )
    for axe, verdict in verdicts.items():
        print(f"{axe:<12} {verdict['score']}/4  {verdict['justification']}")

    print("\nEtape suivante (lecon 2.3.2) : la CALIBRATION — noter 10")
    print("reponses reelles a la main, comparer au juge ; divergence sur")
    print("plus de 2 -> reecrire la rubrique. Un juge non calibre est un")
    print("generateur d'opinions a grande echelle.")
