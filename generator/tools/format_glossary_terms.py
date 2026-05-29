"""Applique les liens et le gras déclarés par les contrats de leçon."""

from __future__ import annotations

import argparse
import sys

from glossarylib import fichiers_lecon, formater_terme
from lessonlib import (
    ErreurLecon,
    charger_lecon,
    charger_profil,
    charger_registre,
    chemin_relatif,
    decouvrir_contrats,
    slugifier_terme,
)


def analyser_arguments() -> argparse.Namespace:
    """Déclare l’interface de mise en forme."""

    analyseur = argparse.ArgumentParser(
        description="Formate les termes de glossaire déclarés par les leçons."
    )
    mode = analyseur.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--ecrire",
        action="store_true",
        help="écrit les fragments canoniques modifiés",
    )
    mode.add_argument(
        "--verifier",
        action="store_true",
        help="signale les fragments qui devraient être reformattés",
    )
    return analyseur.parse_args()


def main() -> int:
    """Formate toutes les leçons dans l’ordre de lecture."""

    arguments = analyser_arguments()
    try:
        registre = charger_registre()
        differences: list[str] = []
        ecrits = 0
        for chemin_contrat in decouvrir_contrats():
            lecon = charger_lecon(chemin_contrat, registre)
            profil = charger_profil(
                lecon.donnees["profil_par_defaut"],
                registre,
            )
            fichiers = fichiers_lecon(lecon, registre, profil)
            contenus = {
                chemin: chemin.read_text(encoding="utf-8-sig")
                for chemin in fichiers
            }
            for terme in lecon.donnees["termes"]:
                vues = 0
                slug = slugifier_terme(terme)
                for chemin in fichiers:
                    formate, vues = formater_terme(
                        contenus[chemin],
                        terme,
                        slug,
                        vues,
                    )
                    contenus[chemin] = formate
            for chemin, contenu in contenus.items():
                observe = chemin.read_text(encoding="utf-8-sig")
                if contenu == observe:
                    continue
                differences.append(chemin_relatif(chemin))
                if arguments.ecrire:
                    chemin.write_text(contenu, encoding="utf-8", newline="")
                    ecrits += 1
    except (ErreurLecon, OSError, UnicodeError) as erreur:
        print(f"ERREUR · {erreur}", file=sys.stderr)
        return 1

    if arguments.verifier and differences:
        for difference in differences:
            print(
                f"ERREUR · {difference} — termes de glossaire non formatés",
                file=sys.stderr,
            )
        return 1
    if arguments.verifier:
        print("Termes de glossaire correctement formatés.")
    else:
        print(f"{ecrits} fragment(s) mis en forme.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
