"""Importe les leçons monolithiques dans le format canonique par sections.

Cette commande sert à la migration initiale. Elle refuse d’écraser un dossier
de leçon existant.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lessonlib import (
    DOSSIER_LECONS,
    RACINE,
    ErreurLecon,
    ecrire_json,
    rendre_frontmatter,
)


DOSSIER_WIKI = RACINE / "Wiki" / "parcours"
CHEMIN_CARTOGRAPHIE = (
    RACINE / "generator" / "guardrails" / "parcours" / "cartographie.md"
)
SECTIONS = {
    "Prérequis": ("prerequis", "10-prerequis.md"),
    "Savoir le situer": ("savoir-le-situer", "20-savoir-le-situer.md"),
    "Connaissances": ("connaissances", "30-connaissances.md"),
    "Reconstruction": ("reconstruction", "40-reconstruction.md"),
    "Décision et dépôt dans Praxis": (
        "decision-praxis",
        "50-decision-praxis.md",
    ),
    "Limites et cas d'échec": ("limites", "60-limites.md"),
    "Se tester": ("se-tester", "70-se-tester.md"),
    "Mesures": ("mesures", "80-mesures.md"),
    "Références": ("references", "90-references.md"),
}


@dataclass(frozen=True)
class ImportLecon:
    """Contenu prêt à être écrit après contrôle de réversibilité."""

    source: Path
    dossier: Path
    contrat: dict[str, Any]
    etat: dict[str, Any]
    fragments: dict[Path, str]


def lire_frontmatter(texte: str, chemin: Path) -> tuple[dict[str, Any], str]:
    """Extrait le Frontmatter simple actuellement employé."""

    correspondance = re.match(r"\A---\n(.*?)\n---\n\n", texte, re.DOTALL)
    if not correspondance:
        raise ErreurLecon(f"{chemin} — Frontmatter absent ou mal fermé")

    donnees: dict[str, Any] = {}
    for numero, ligne in enumerate(correspondance.group(1).splitlines(), start=2):
        champ = re.fullmatch(r"([A-Za-z0-9_-]+):\s*(.*)", ligne)
        if not champ:
            raise ErreurLecon(f"{chemin}:{numero} — ligne Frontmatter invalide")
        cle, valeur = champ.groups()
        if valeur.startswith("[") and valeur.endswith("]"):
            interieur = valeur[1:-1].strip()
            donnees[cle] = (
                [item.strip() for item in interieur.split(",")]
                if interieur
                else []
            )
        else:
            donnees[cle] = valeur
    return donnees, texte[correspondance.end() :]


def decouper_corps(
    corps: str,
    chemin: Path,
) -> tuple[str, str, dict[str, str]]:
    """Sépare le titre, l’introduction et les rubriques de niveau deux."""

    titre = re.match(r"\A# ([^\n]+)\n", corps)
    if not titre:
        raise ErreurLecon(f"{chemin} — titre de niveau un absent")
    nom = titre.group(1)
    suite = corps[titre.end() :]
    positions = list(re.finditer(r"^## ([^\n]+)\n", suite, re.MULTILINE))
    if not positions:
        raise ErreurLecon(f"{chemin} — aucune section de niveau deux")

    introduction = suite[: positions[0].start()].strip()
    fragments: dict[str, str] = {}
    for index, position in enumerate(positions):
        fin = positions[index + 1].start() if index + 1 < len(positions) else len(suite)
        titre_section = position.group(1)
        if titre_section not in SECTIONS:
            raise ErreurLecon(
                f"{chemin} — rubrique non déclarée : {titre_section!r}"
            )
        fragments[titre_section] = suite[position.start() : fin].strip()
    return nom, introduction, fragments


def notions_depuis_connaissances(fragment: str) -> list[str]:
    """Utilise les sous-titres existants comme couverture initiale."""

    return re.findall(r"^### ([^\n]+)$", fragment, re.MULTILINE)


def attribution_cartographie(identifiant: str) -> str:
    """Retrouve la couverture attribuée à une leçon dans la cartographie."""

    lignes = CHEMIN_CARTOGRAPHIE.read_text(encoding="utf-8-sig").splitlines()
    correspondances = []
    for ligne in lignes:
        if not ligne.startswith("|"):
            continue
        cellules = [cellule.strip() for cellule in ligne.strip("|").split("|")]
        if len(cellules) < 5 or f"`{identifiant}`" not in cellules[0]:
            continue
        correspondances.append(cellules[4])
    if len(correspondances) != 1:
        raise ErreurLecon(
            f"{identifiant} — attribution cartographique attendue une fois, "
            f"trouvée {len(correspondances)} fois"
        )
    return correspondances[0]


def preparer_import(chemin: Path) -> ImportLecon:
    """Construit un import et prouve qu’il restitue le texte source."""

    texte = chemin.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    frontmatter, corps = lire_frontmatter(texte, chemin)
    titre, introduction, sections_source = decouper_corps(corps, chemin)

    identifiant = frontmatter.get("id")
    parcours = frontmatter.get("parcours")
    if not isinstance(identifiant, str) or not isinstance(parcours, str):
        raise ErreurLecon(f"{chemin} — id ou parcours absent")
    if frontmatter.get("titre") != titre:
        raise ErreurLecon(
            f"{chemin} — le titre du Frontmatter diffère du titre Markdown"
        )

    dossier = DOSSIER_LECONS / parcours / identifiant
    fragments: dict[Path, str] = {
        Path("sections/00-introduction.md"): introduction,
    }
    table_sections: dict[str, str] = {
        identifiant_section: f"sections/{nom_fichier}"
        for identifiant_section, nom_fichier in SECTIONS.values()
    }
    for titre_section, contenu in sections_source.items():
        identifiant_section, nom_fichier = SECTIONS[titre_section]
        chemin_relatif = Path("sections") / nom_fichier
        fragments[chemin_relatif] = contenu

    connaissances = sections_source.get("Connaissances", "")
    contrat = {
        "version": 1,
        "id": identifiant,
        "titre": titre,
        "concept_central": titre,
        "attribution_cartographie": attribution_cartographie(identifiant),
        "notions": notions_depuis_connaissances(connaissances),
        "hors_perimetre": [],
        "termes": [],
        "regles_supplementaires": [],
        "sortie": chemin.relative_to(RACINE).as_posix(),
        "profil_par_defaut": "complet",
        "sauts_de_ligne_fin": len(texte) - len(texte.rstrip("\n")),
        "frontmatter": frontmatter,
        "introduction": "sections/00-introduction.md",
        "sections": table_sections,
    }
    date = frontmatter.get("updated", "")
    etat = {
        "version": 1,
        "lecon": identifiant,
        "contrat": {
            "statut": "a-valider",
            "raison": "Migration structurelle sans validation sémantique.",
        },
        "sections": {
            identifiant_section: (
                {
                    "statut": "generee",
                    "mise_a_jour": date,
                }
                if identifiant_section
                in {
                    SECTIONS[titre_section][0]
                    for titre_section in sections_source
                }
                else {
                    "statut": "a-generer",
                }
            )
            for identifiant_section in table_sections
        },
    }

    morceaux = [rendre_frontmatter(frontmatter), f"# {titre}"]
    if introduction:
        morceaux.append(introduction)
    ordre = [valeur[0] for valeur in SECTIONS.values()]
    par_identifiant = {
        SECTIONS[titre_section][0]: contenu
        for titre_section, contenu in sections_source.items()
    }
    morceaux.extend(
        par_identifiant[identifiant_section]
        for identifiant_section in ordre
        if identifiant_section in par_identifiant
    )
    reconstruit = (
        "\n\n".join(morceaux) + "\n" * contrat["sauts_de_ligne_fin"]
    )
    if reconstruit != texte:
        raise ErreurLecon(
            f"{chemin} — l’import ne restitue pas exactement la leçon"
        )
    return ImportLecon(chemin, dossier, contrat, etat, fragments)


def ecrire_import(importation: ImportLecon) -> None:
    """Écrit un import après avoir refusé toute collision."""

    if importation.dossier.exists():
        raise ErreurLecon(
            f"{importation.dossier} — dossier canonique déjà présent"
        )
    importation.dossier.mkdir(parents=True)
    ecrire_json(importation.dossier / "contract.json", importation.contrat)
    ecrire_json(importation.dossier / "state.json", importation.etat)
    for chemin_relatif, contenu in importation.fragments.items():
        chemin = importation.dossier / chemin_relatif
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(contenu.rstrip() + "\n", encoding="utf-8", newline="")


def analyser_arguments() -> argparse.Namespace:
    """Déclare l’interface de migration."""

    analyseur = argparse.ArgumentParser(
        description="Migre les leçons du Wiki vers des fragments canoniques."
    )
    analyseur.add_argument(
        "--ecrire",
        action="store_true",
        help="écrit les contrats, états et fragments après les contrôles",
    )
    return analyseur.parse_args()


def main() -> int:
    """Prépare tous les imports puis les écrit en une seconde phase."""

    arguments = analyser_arguments()
    chemins = sorted(DOSSIER_WIKI.rglob("*.md"))
    try:
        importations = [preparer_import(chemin) for chemin in chemins]
        collisions = [
            importation.dossier
            for importation in importations
            if importation.dossier.exists()
        ]
        if collisions:
            raise ErreurLecon(
                "dossiers canoniques déjà présents : "
                + ", ".join(str(chemin) for chemin in collisions)
            )
        if arguments.ecrire:
            for importation in importations:
                ecrire_import(importation)
    except (ErreurLecon, OSError, UnicodeError) as erreur:
        print(f"ERREUR · {erreur}", file=sys.stderr)
        return 1

    action = "migrées" if arguments.ecrire else "prêtes à migrer"
    print(f"{len(importations)} leçon(s) {action} sans perte textuelle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
