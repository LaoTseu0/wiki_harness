"""Controles du repo : ce qui doit etre vrai de cours/ a tout moment.

Le pendant de canvas.py — celui-ci ne genere rien, il constate. Sept
familles, chacune adossee a une regle ecrite dans AGENTS.md ou dans
cours/_gabarit.md :

  liens         un lien qui ne resout pas
  orphelins     un .md qu'on n'atteint ni depuis la carte ni depuis AGENTS.md
  archive       une lecon vivante qui s'appuie sur cours/_archive/
  numerotation  la numerotation heritee des modules ([2.4.1], « module 3 »)
  vocabulaire   entretien / recruteur / offres / CV — controle 19 du gabarit
  mesures       un chiffre de performance hors d'une rubrique « Mesures »
  vides         une rubrique qui annonce puis ne tient rien
  rubriques     une lecon a qui il manque des rubriques de son gabarit

    python wiki/outils/controles.py           # le tableau, sortie != 0 si dette
    python wiki/outils/controles.py --detail  # chaque occurrence, fichier par ligne

Les familles ne sont pas toutes du meme age : « liens » et « orphelins »
doivent rester a zero en permanence, les autres se vident au fil des
reecritures. Le script ne trie pas — c'est a la relecture de le faire.
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
WIKI = RACINE / "wiki"
COURS = WIKI / "cours"
CARTE = COURS / "carte.md"
CONVENTIONS = RACINE / "AGENTS.md"

# Ni le gabarit ni les processus ne sont des lecons : ils n'ont pas de
# rubriques a tenir, et leurs liens d'exemple ne sont pas des liens.
PAS_UNE_LECON = {"_gabarit.md", "carte.md", "index.md"}

LIEN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
SECTION = re.compile(r"^##\s+(.+?)\s*$", re.M)
NUMEROTATION = re.compile(r"\[\d\.\d(?:\.\d)?[^\]]*\]|\bmodules? \d\b")
VOCABULAIRE = re.compile(
    r"\b(entretiens?|recruteurs?|recrutement|candidats?|portfolio|CV|"
    r"employabilit[ée]|offres?\s+(?:d'emploi|r[ée]elles?)|march[ée]\s+du\s+travail|"
    r"salaires?)\b",
    re.I,
)
# Un chiffre suivi d'une unite de performance. Volontairement etroit :
# mieux vaut manquer une invention que noyer le rapport.
MESURE = re.compile(r"\d[\d ,.]*\s*(%|ms\b|tok/s|Go\b|GB\b|Mo\b|Ko\b|k€|€)")

RUBRIQUES_A = [
    "Où ça s'emboîte",
    "Prérequis et suites",
    "L'essentiel",
    "Le savoir",
    "En pratique",
    "Mesures",
    "Recomposer",
    "Pièges connus",
    "Se tester",
    "Ce que ça change dans le framework",
    "À retenir",
    "Références",
]
RUBRIQUES_B = [
    "Prérequis et suites",
    "L'essentiel",
    "Le savoir",
    "Quand c'est la bonne réponse",
    "Ce qu'on ne saura pas faire",
    "Se tester",
    "À retenir",
    "Références",
]


def hors_code(texte: str) -> str:
    """Blanchit les blocs ``` : le gabarit y montre des liens d'exemple."""
    return re.sub(r"^```.*?^```", "", texte, flags=re.S | re.M)


def lecons() -> list[Path]:
    """Les fiches qui doivent tenir un gabarit.

    Le glossaire et les processus sont du cours mais pas des lecons : une
    definition courte et une chaine technique n'ont ni etape, ni mesure,
    ni promotion.
    """
    return [
        f
        for f in sorted(COURS.rglob("*.md"))
        if "_archive" not in f.parts
        and f.name not in PAS_UNE_LECON
        and not {"glossaire", "_processus"} & set(f.parts)
    ]


def tous_les_md() -> list[Path]:
    return [f for f in sorted(COURS.rglob("*.md")) if "_archive" not in f.parts]


def lignes_hors_code(fichier: Path) -> list[tuple[int, str]]:
    """Numerotees a partir de 1, les lignes des blocs de code blanchies."""
    texte = fichier.read_text(encoding="utf-8")
    return list(enumerate(hors_code(texte).split("\n"), start=1))


# --- les sept familles -----------------------------------------------


def liens_morts() -> list[str]:
    trouves = []
    for f in tous_les_md():
        for numero, ligne in lignes_hors_code(f):
            for m in LIEN.finditer(ligne):
                cible = m.group(2).split("#")[0]
                if not cible or cible.startswith(("http", "mailto")):
                    continue
                if not (f.parent / cible).exists():
                    trouves.append(f"{f.relative_to(COURS)}:{numero} -> {cible}")
    return trouves


def orphelins() -> list[str]:
    vus: set[Path] = set()
    pile = [CARTE, CONVENTIONS]
    while pile:
        f = pile.pop()
        if f in vus or not f.exists():
            continue
        vus.add(f)
        for m in LIEN.finditer(hors_code(f.read_text(encoding="utf-8"))):
            cible = m.group(2).split("#")[0]
            if cible.endswith(".md") and not cible.startswith(("http", "mailto")):
                pile.append((f.parent / cible).resolve())
    return [
        str(f.relative_to(COURS)) for f in tous_les_md() if f.resolve() not in vus
    ]


def motif(expression: re.Pattern) -> list[str]:
    """Occurrences d'un motif dans les lecons, hors blocs de code."""
    trouves = []
    for f in lecons():
        for numero, ligne in lignes_hors_code(f):
            for m in expression.finditer(ligne):
                trouves.append(f"{f.relative_to(COURS)}:{numero} — {m.group(0)}")
    return trouves


def renvois_archive() -> list[str]:
    return motif(re.compile(r"\.\./_archive/[^\s)]+|roadmap\s+§[\d.]+"))


def mesures_non_marquees() -> list[str]:
    """Chiffres de performance hors de la rubrique « Mesures »."""
    trouves = []
    for f in lecons():
        dans_mesures = False
        for numero, ligne in lignes_hors_code(f):
            entete = SECTION.match(ligne)
            if entete:
                dans_mesures = entete.group(1).strip() == "Mesures"
                continue
            if dans_mesures:
                continue
            for m in MESURE.finditer(ligne):
                trouves.append(f"{f.relative_to(COURS)}:{numero} — {m.group(0)}")
    return trouves


def rubriques_vides() -> list[str]:
    """Une rubrique qui annonce puis ne tient rien.

    Pire qu'une rubrique absente : le lecteur y cherche quelque chose.
    Arrive quand on retire le dernier element d'une liste.
    """
    trouves = []
    for f in lecons():
        titre, ligne_titre, vide = None, 0, False
        for numero, ligne in lignes_hors_code(f):
            entete = SECTION.match(ligne)
            if entete:
                if titre and vide:
                    trouves.append(f"{f.relative_to(COURS)}:{ligne_titre} — {titre}")
                titre, ligne_titre, vide = entete.group(1), numero, True
            elif ligne.strip():
                vide = False
        if titre and vide:
            trouves.append(f"{f.relative_to(COURS)}:{ligne_titre} — {titre}")
    return trouves


def rubriques_manquantes() -> list[str]:
    """Une lecon qui declare une etape suit le gabarit A, sinon le B."""
    trouves = []
    for f in lecons():
        texte = f.read_text(encoding="utf-8")
        entete = texte.split("\n## ")[0]
        attendues = RUBRIQUES_A if "· étape :" in entete else RUBRIQUES_B
        presentes = {s.strip() for s in SECTION.findall(texte)}
        absentes = [r for r in attendues if r not in presentes]
        if absentes:
            gabarit = "A" if attendues is RUBRIQUES_A else "B"
            trouves.append(
                f"{f.relative_to(COURS)} [{gabarit}] — manque : {', '.join(absentes)}"
            )
    return trouves


FAMILLES = [
    ("liens morts", liens_morts),
    ("orphelins", orphelins),
    ("renvois vers _archive", renvois_archive),
    ("numerotation heritee", lambda: motif(NUMEROTATION)),
    ("vocabulaire proscrit", lambda: motif(VOCABULAIRE)),
    ("mesures non marquees", mesures_non_marquees),
    ("rubriques vides", rubriques_vides),
    ("rubriques manquantes", rubriques_manquantes),
]


def principal(detail: bool) -> int:
    total = 0
    for nom, controle in FAMILLES:
        trouves = controle()
        total += len(trouves)
        fichiers = len(Counter(t.split(":")[0].split(" —")[0] for t in trouves))
        point = f"{len(trouves)} dans {fichiers} fichiers" if trouves else "0"
        print(f"  {nom:.<26} {point}")
        if detail and trouves:
            for t in trouves:
                print(f"      {t}")
            print()

    print(f"\n{total} constats sur {len(lecons())} lecons")
    if total and not detail:
        print("Le detail : python wiki/outils/controles.py --detail")
    return 1 if total else 0


if __name__ == "__main__":
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--detail", action="store_true")
    sys.exit(principal(parseur.parse_args().detail))
