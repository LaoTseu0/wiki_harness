"""
tableau_final.py — generer LA piece maitresse du module.

Le tableau v0.0.1 -> v0.0.2 -> v0.0.3 du README ne se recopie JAMAIS a
la main (recopier des chiffres, c'est en trahir un — piege de la
lecon). Ce script agrege les resultats produits par les harnais
d'evals en un tableau markdown date, pret a coller.

Convention d'echange : chaque harnais (07_evals etendu, 2.2.5, la
v0.0.3) depose un JSON dans evals/resultats/ au format :

    {"generation": "v0.0.2", "stack": "Qdrant + hybride",
     "date": "2026-07-21", "tag": "0.2.0",
     "retrieval": 9, "generation_score": 8, "hallucinations": 0,
     "total": 12, "latence_ms": 210,
     "commentaire": "l'hybride a repeche les questions a termes exacts"}

Le COMMENTAIRE est obligatoire : chaque chiffre a une histoire, et les
echecs documentes valent autant que les gains ("ce que je referais
autrement" est une section attendue du README, P.1.1).
"""

import json
from datetime import date
from pathlib import Path

MODULE = Path(__file__).resolve().parents[2]
DOSSIER_RESULTATS = MODULE / "evals" / "resultats"


def charger_resultats() -> list[dict]:
    if not DOSSIER_RESULTATS.exists():
        raise SystemExit(
            f"{DOSSIER_RESULTATS} absent — les harnais d'evals doivent y "
            f"deposer leurs JSON (voir convention en docstring)."
        )
    resultats = [
        json.loads(f.read_text(encoding="utf-8"))
        for f in sorted(DOSSIER_RESULTATS.glob("*.json"))
    ]
    if not resultats:
        raise SystemExit("aucun resultat trouve — lancer d'abord les evals")
    return resultats


def generer_tableau(resultats: list[dict]) -> str:
    lignes = [
        f"### Metrics — updated {date.today().isoformat()}",
        "",
        "| Generation | Stack | Retrieval | Generation | Halluc. | Latency |",
        "|---|---|---|---|---|---|",
    ]
    for r in resultats:
        lignes.append(
            f"| {r['generation']} (tag {r.get('tag', '?')}) | {r['stack']} "
            f"| {r['retrieval']}/{r['total']} "
            f"| {r['generation_score']}/{r['total']} "
            f"| {r['hallucinations']} | {r.get('latence_ms', '?')} ms |"
        )
    lignes.append("")
    # Les commentaires de transition : deux phrases par ligne, la
    # difference entre un tableau muet et un tableau qui raconte.
    for r in resultats:
        lignes.append(f"- **{r['generation']}** : {r['commentaire']}")
    return "\n".join(lignes)


if __name__ == "__main__":
    tableau = generer_tableau(charger_resultats())
    print(tableau)
    print("\n(A coller dans le README anglais du module — hygiene de la")
    print("lecon 2.3.4 : le coeur de 12 questions reste identique entre")
    print("generations, les extensions sont marquees, et chaque config")
    print("est rejouable depuis son tag git.)")
