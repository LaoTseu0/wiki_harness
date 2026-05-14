"""Met à jour explicitement le statut d’un contrat ou d’une section."""

from __future__ import annotations

import argparse
import sys
from datetime import date

from lessonlib import (
    STATUTS_CONTRAT,
    STATUTS_SECTION,
    ErreurLecon,
    charger_etat,
    charger_lecon,
    charger_registre,
    decouvrir_contrats,
    ecrire_json,
    trouver_lecon,
)


def analyser_arguments() -> argparse.Namespace:
    """Déclare l’interface de changement d’état."""

    analyseur = argparse.ArgumentParser(
        description="Change explicitement l’état d’une leçon."
    )
    analyseur.add_argument("lecon", help="identifiant de la leçon")
    cible = analyseur.add_mutually_exclusive_group(required=True)
    cible.add_argument("--contrat", choices=sorted(STATUTS_CONTRAT))
    cible.add_argument("--section", help="identifiant de section")
    analyseur.add_argument(
        "--statut",
        choices=sorted(STATUTS_SECTION),
        help="statut demandé avec --section",
    )
    analyseur.add_argument(
        "--raison",
        help="raison conservée dans l’état",
    )
    return analyseur.parse_args()


def main() -> int:
    """Applique un changement d’état contrôlé."""

    arguments = analyser_arguments()
    try:
        registre = charger_registre()
        lecons = [
            charger_lecon(chemin, registre) for chemin in decouvrir_contrats()
        ]
        lecon = trouver_lecon(arguments.lecon, lecons)
        etat = charger_etat(lecon, registre)

        if arguments.contrat:
            etat["contrat"]["statut"] = arguments.contrat
            etat["contrat"]["mise_a_jour"] = date.today().isoformat()
            if arguments.raison:
                etat["contrat"]["raison"] = arguments.raison
        else:
            if not arguments.statut:
                raise ErreurLecon("--statut est obligatoire avec --section")
            if arguments.section not in etat["sections"]:
                raise ErreurLecon(
                    f"{lecon.identifiant} — section absente : "
                    f"{arguments.section!r}"
                )
            if arguments.statut == "validee":
                non_validees = [
                    dependance
                    for dependance in registre["sections"][
                        arguments.section
                    ]["dependances"]
                    if etat["sections"].get(dependance, {}).get("statut")
                    != "validee"
                ]
                if non_validees:
                    raise ErreurLecon(
                        "dépendances non validées : " + ", ".join(non_validees)
                    )
            etat["sections"][arguments.section]["statut"] = arguments.statut
            etat["sections"][arguments.section][
                "mise_a_jour"
            ] = date.today().isoformat()
            if arguments.raison:
                etat["sections"][arguments.section]["raison"] = arguments.raison
        ecrire_json(lecon.chemin_etat, etat)
    except (ErreurLecon, OSError, UnicodeError) as erreur:
        print(f"ERREUR · {erreur}", file=sys.stderr)
        return 1

    print(f"État mis à jour pour {lecon.identifiant}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
