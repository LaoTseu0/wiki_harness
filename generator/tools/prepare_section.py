"""Prépare le contexte minimal nécessaire à la génération d’une section."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lessonlib import (
    RACINE,
    ErreurLecon,
    charger_etat,
    charger_lecon,
    charger_registre,
    chemin_fragment,
    chemin_relatif,
    decouvrir_contrats,
    resoudre_dans_racine,
    trouver_lecon,
)


def analyser_arguments() -> argparse.Namespace:
    """Déclare l’interface de préparation."""

    analyseur = argparse.ArgumentParser(
        description="Produit le contexte minimal d’une section de leçon."
    )
    analyseur.add_argument("lecon", help="identifiant de la leçon")
    analyseur.add_argument("section", help="identifiant de la section")
    analyseur.add_argument(
        "--lister",
        action="store_true",
        help="liste seulement les fichiers qui composent le contexte",
    )
    analyseur.add_argument(
        "--sortie",
        type=Path,
        help="écrit le contexte dans ce fichier au lieu de la sortie standard",
    )
    return analyseur.parse_args()


def composer_contexte(lecon, section: str, registre, etat) -> tuple[list[Path], str]:
    """Valide les dépendances et concatène uniquement les entrées utiles."""

    definition = registre["sections"].get(section)
    if definition is None:
        raise ErreurLecon(f"section inconnue : {section!r}")

    manquantes: list[str] = []
    for dependance in definition["dependances"]:
        statut = etat["sections"].get(dependance, {}).get("statut")
        if statut != "validee":
            manquantes.append(f"{dependance} ({statut or 'absente'})")
    if manquantes:
        raise ErreurLecon(
            f"{lecon.identifiant}/{section} — dépendances non validées : "
            + ", ".join(manquantes)
        )

    chemins: list[Path] = []
    regles = (
        registre["regles_communes"]
        + lecon.donnees["regles_supplementaires"]
        + definition["regles"]
    )
    for valeur in regles:
        chemin = resoudre_dans_racine(valeur, "règle")
        if not chemin.is_file():
            raise ErreurLecon(f"{chemin_relatif(chemin)} — règle absente")
        if chemin not in chemins:
            chemins.append(chemin)
    chemins.append(lecon.chemin_contrat)
    chemins.extend(
        chemin_fragment(lecon, dependance)
        for dependance in definition["dependances"]
    )
    cible = chemin_fragment(lecon, section)
    if cible.is_file():
        chemins.append(cible)

    blocs = []
    for chemin in chemins:
        contenu = chemin.read_text(encoding="utf-8-sig").strip()
        blocs.append(
            f"<!-- SOURCE: {chemin_relatif(chemin)} -->\n\n{contenu}"
        )
    instruction = {
        "lecon": lecon.identifiant,
        "section": section,
        "output": lecon.donnees["sections"].get(section),
        "regle": (
            "Produire uniquement le fragment demandé. Ne modifier aucune "
            "autre section ni la leçon assemblée."
        ),
    }
    blocs.append(
        "<!-- CONTRAT DE SORTIE -->\n\n```json\n"
        + json.dumps(instruction, ensure_ascii=False, indent=2)
        + "\n```"
    )
    return chemins, "\n\n---\n\n".join(blocs) + "\n"


def main() -> int:
    """Prépare le contexte ou sa liste de sources."""

    arguments = analyser_arguments()
    try:
        registre = charger_registre()
        lecons = [
            charger_lecon(chemin, registre) for chemin in decouvrir_contrats()
        ]
        lecon = trouver_lecon(arguments.lecon, lecons)
        etat = charger_etat(lecon, registre)
        chemins, contexte = composer_contexte(
            lecon, arguments.section, registre, etat
        )

        if arguments.lister:
            resultat = "\n".join(chemin_relatif(chemin) for chemin in chemins)
        else:
            resultat = contexte.rstrip()

        if arguments.sortie:
            chemin_sortie = (
                arguments.sortie
                if arguments.sortie.is_absolute()
                else RACINE / arguments.sortie
            )
            chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
            chemin_sortie.write_text(resultat + "\n", encoding="utf-8", newline="")
            print(chemin_relatif(chemin_sortie))
        else:
            print(resultat)
    except (ErreurLecon, OSError, UnicodeError) as erreur:
        print(f"ERREUR · {erreur}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
