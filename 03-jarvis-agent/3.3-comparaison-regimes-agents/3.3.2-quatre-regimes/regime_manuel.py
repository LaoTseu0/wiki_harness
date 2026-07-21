"""
regime_manuel.py — le regime 1/4 : la boucle ecrite par nous.

L'exercice de la lecon 3.3.2 : LE MEME agent a 3 outils (lire un
fichier, chercher dans la doc, agir sur HA mocke) refait dans les
quatre regimes — manuel / harnais Pi / SDK du marche / graphe
LangGraph. Ce fichier est le regime MANUEL, la reference : tout le
reste est constant (memes outils, meme tache), seul le regime change.

Le tableau a remplir AVEC LE VECU (pas la doc), pour chaque regime :
  - combien de lignes a moi ?
  - ou mettre un garde-fou ?
  - que vois-je quand ca rate ?

Les trois autres regimes reutilisent les MEMES fonctions outils
(importables d'ici) : c'est la constante de l'experience.
"""

import json
import sys
from pathlib import Path

import httpx

OLLAMA_URL = "http://192.168.1.57:11434"
MODEL = "qwen3:4b-instruct-2507-q4_K_M"
MAX_TOURS = 8

# Le RAG du module 2 sert d'outil "chercher dans la doc" : le
# dogfooding du parcours (un module consomme le precedent).
M2 = Path(__file__).resolve().parents[3] / "02-homelab-rag"
sys.path.insert(0, str(M2))
sys.path.insert(0, str(M2 / "2.1-v0.0.1-rag-a-la-main" / "2.1.5-recherche-top-k"))


# --- Les 3 outils (constants entre les quatre regimes) ----------------

def lire_fichier(nom: str) -> str:
    """Lecture bornee au dossier de la lecon (sandbox du module 1)."""
    sandbox = Path(__file__).parent.resolve()
    chemin = (sandbox / nom).resolve()
    if not chemin.is_relative_to(sandbox):
        return f"Refus : '{nom}' sort du perimetre"
    try:
        return chemin.read_text(encoding="utf-8")[:2000]
    except FileNotFoundError:
        return f"Fichier introuvable : {nom}"


def chercher_doc(question: str) -> str:
    """Le retrieval du module 2, resume pour la fenetre de l'agent."""
    try:
        from importlib import import_module
        _m05 = import_module("05_rechercher")
        index = _m05.charger_index()
        top = _m05.rechercher(question, index, k=3)
        return "\n".join(f"[{f} > {t}] {x[:200]}" for _, f, t, x in top)
    except Exception as erreur:
        return f"retrieval indisponible : {erreur}"


def ha_agir_mock(entity_id: str, action: str) -> str:
    """HA MOCKE : l'experience compare les regimes, pas la maison —
    aucune action reelle pendant le comparatif."""
    return f"[MOCK] {action} sur {entity_id} : ok"


OUTILS = {
    "lire_fichier": (lire_fichier, {"nom": "string"}),
    "chercher_doc": (chercher_doc, {"question": "string"}),
    "ha_agir_mock": (ha_agir_mock, {"entity_id": "string",
                                    "action": "string"}),
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": nom,
            "description": {
                "lire_fichier": "Lit un fichier du dossier de travail.",
                "chercher_doc": "Cherche dans la documentation du homelab.",
                "ha_agir_mock": "Agit sur un equipement de la maison "
                                "(simulation).",
            }[nom],
            "parameters": {
                "type": "object",
                "properties": {p: {"type": t} for p, t in params.items()},
                "required": list(params),
            },
        },
    }
    for nom, (_, params) in OUTILS.items()
]


# --- La boucle : ~30 lignes, TOUT est visible (c'est le critere) ------

def executer_tache(tache: str) -> str:
    messages = [
        {"role": "system",
         "content": "Tu es un agent outille. Utilise les outils fournis "
         "puis reponds en francais, de facon concise."},
        {"role": "user", "content": tache},
    ]
    for _ in range(MAX_TOURS):
        reponse = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": messages, "tools": TOOLS,
                  "stream": False, "options": {"num_predict": 600}},
            timeout=180,
        ).json()["message"]
        messages.append(reponse)
        appels = reponse.get("tool_calls")
        if not appels:
            return reponse["content"]
        for appel in appels:
            nom = appel["function"]["name"]
            args = appel["function"]["arguments"]
            print(f"   [outil : {nom}({json.dumps(args, ensure_ascii=False)})]")
            fonction = OUTILS.get(nom, (None, None))[0]
            resultat = fonction(**args) if fonction else f"Outil inconnu : {nom}"
            messages.append({"role": "tool", "content": str(resultat)})
    return "[stop : MAX_TOURS atteint]"


if __name__ == "__main__":
    # La TACHE DE REFERENCE, identique dans les quatre regimes :
    tache = ("Cherche dans la doc quel modele LLM tourne sur "
             "jarvis-central, puis allume la lampe du bureau.")
    print(f"Tache : {tache}\n")
    print(f"\nReponse : {executer_tache(tache)}")

    print("\nLigne 'manuel' du tableau 3.3.2 (a completer avec le vecu) :")
    print("  lignes a moi : ~140 | garde-fou : n'importe ou (c'est notre")
    print("  code) | quand ca rate : tout est sous les yeux (print).")
    print("A faire : la meme tache via Pi, un SDK du marche, LangGraph —")
    print("memes outils importes d'ici, tableau rempli regime par regime.")
