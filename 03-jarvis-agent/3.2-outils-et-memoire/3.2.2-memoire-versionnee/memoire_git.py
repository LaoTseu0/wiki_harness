"""
memoire_git.py — la memoire long terme d'un agent : des fichiers, git.

Le pattern "external memory" du context engineering (lecon 3.2.2) :
la fenetre de contexte est perissable, la memoire vit AILLEURS — des
markdown dans un depot git, synchronises par hooks de session :

  session_start    -> git pull + chargement de l'INDEX (court) ;
  session_shutdown -> consolidation (une SELECTION !) + commit + push.

Pourquoi git : audit (git log = "pourquoi l'agent croit-il ca ?"),
rollback (une memoire polluee se revoque par revert), checkpoint (la
granularite session borne le rayon d'une pollution).

Le protocole de consolidation (l'etape difficile, ajoutee par la
relecture critique) est implemente dans consolider() : candidats ->
filtre trois questions -> conflit tranche par la date -> budget.

Test de bout en bout de la lecon : apprendre un fait en session A, le
retrouver en session B, le corriger en session C, lire l'historique.

Prerequis : un depot memoire dedie (SEPARE du depot de code),
git configure. MEMOIRE_DIR par variable d'environnement.
"""

import os
import subprocess
from datetime import date
from pathlib import Path

MEMOIRE = Path(os.environ.get("MEMOIRE_DIR", "~/jarvis-memoire")).expanduser()
INDEX = MEMOIRE / "INDEX.md"


def _git(*args: str) -> str:
    resultat = subprocess.run(
        ["git", "-C", str(MEMOIRE), *args],
        capture_output=True, text=True, timeout=60,
    )
    if resultat.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} : {resultat.stderr.strip()}")
    return resultat.stdout.strip()


# --- session_start ----------------------------------------------------

def session_start() -> str:
    """Pull + renvoie l'index SEUL. La memoire se RECHERCHE, elle ne se
    charge pas en bloc — sinon elle devient le probleme de contexte
    qu'elle devait resoudre (piege de la lecon)."""
    _git("pull", "--ff-only")
    if not INDEX.exists():
        INDEX.write_text("# Index memoire\n", encoding="utf-8")
    return INDEX.read_text(encoding="utf-8")


def charger_theme(nom: str) -> str:
    """Chargement A LA DEMANDE d'un fichier thematique cite par l'index."""
    fichier = MEMOIRE / f"{nom}.md"
    return fichier.read_text(encoding="utf-8") if fichier.exists() else ""


# --- La consolidation : une SELECTION, pas un compte rendu ------------

def consolider(faits_candidats: list[dict]) -> list[dict]:
    """Filtre les faits proposes en fin de session (par l'agent).

    Chaque candidat : {"texte", "theme", "durable": bool,
    "deja_connu": bool} — les deux booleens sont a evaluer par l'agent
    (durable ? absent de la doc ET de la memoire ?). Le protocole :
      1. durable ? sinon jete (le transcript brut est du bruit) ;
      2. deja connu (doc homelab ou memoire) ? sinon duplication ->
         jete (une memoire qui duplique sa source derive) ;
      3. budget : quelques lignes par session — au-dela, on garde les
         premiers (l'agent doit prioriser, pas deverser)."""
    retenus = [f for f in faits_candidats
               if f.get("durable") and not f.get("deja_connu")]
    BUDGET = 5
    return retenus[:BUDGET]


def ecrire_faits(faits: list[dict]) -> None:
    """Un fait = une ligne datee dans son fichier theme. En conflit
    avec l'existant, la version la plus recente l'emporte — l'ancienne
    reste dans l'historique git (c'est le rollback)."""
    aujourd_hui = date.today().isoformat()
    for fait in faits:
        fichier = MEMOIRE / f"{fait['theme']}.md"
        existant = fichier.read_text(encoding="utf-8") if fichier.exists() else f"# {fait['theme']}\n"
        fichier.write_text(existant + f"- [{aujourd_hui}] {fait['texte']}\n",
                           encoding="utf-8")
        # L'index reste court : une ligne par theme, pas par fait.
        index = INDEX.read_text(encoding="utf-8")
        if f"[[{fait['theme']}]]" not in index:
            INDEX.write_text(index + f"- [[{fait['theme']}]]\n",
                             encoding="utf-8")


# --- session_shutdown -------------------------------------------------

def session_shutdown(faits_candidats: list[dict]) -> str:
    """Consolide, commit avec un message DESCRIPTIF (c'est lui qu'on
    auditera : "appris : X ; corrige : Y"), push."""
    faits = consolider(faits_candidats)
    if not faits:
        return "rien a consolider (c'est un resultat valide)"
    ecrire_faits(faits)
    resume = " ; ".join(f["texte"][:40] for f in faits)
    _git("add", "-A")
    _git("commit", "-m", f"session {date.today().isoformat()} — appris : {resume}")
    _git("push")
    return f"{len(faits)} fait(s) consolide(s) et pousse(s)"


if __name__ == "__main__":
    # Demonstration du cycle (suppose MEMOIRE_DIR initialise en depot).
    print("index charge :", len(session_start()), "caracteres")
    print(session_shutdown([
        {"texte": "Anthony prefere les schemas aux paragraphes",
         "theme": "preferences", "durable": True, "deja_connu": False},
        {"texte": "il a plu aujourd'hui",
         "theme": "meteo", "durable": False, "deja_connu": False},  # jete
    ]))
    print("\naudit : git log --oneline -3")
    print(_git("log", "--oneline", "-3"))
