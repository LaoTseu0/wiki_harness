"""Assemble ou vérifie les leçons dérivées du Wiki."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lessonlib import (
    RACINE,
    ErreurLecon,
    assembler,
    charger_lecon,
    charger_profil,
    charger_registre,
    chemin_relatif,
    decouvrir_contrats,
    trouver_lecon,
)


def analyser_arguments() -> argparse.Namespace:
    """Déclare l’interface d’assemblage."""

    analyseur = argparse.ArgumentParser(
        description="Assemble les leçons depuis leurs fragments canoniques."
    )
    analyseur.add_argument(
        "lecon",
        nargs="?",
        help="identifiant d’une leçon ; toutes les leçons si absent",
    )
    analyseur.add_argument(
        "--profil",
        help="profil à employer ; le profil du contrat est utilisé par défaut",
    )
    analyseur.add_argument(
        "--sortie",
        type=Path,
        help="racine alternative obligatoire pour un profil non principal",
    )
    mode = analyseur.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--ecrire",
        action="store_true",
        help="écrit les sorties assemblées",
    )
    mode.add_argument(
        "--verifier",
        action="store_true",
        help="compare les sorties existantes sans écrire",
    )
    return analyseur.parse_args()


def destination(
    lecon,
    profil: str,
    racine_alternative: Path | None,
) -> Path:
    """Choisit une destination sans écraser le Wiki avec un autre profil."""

    profil_principal = lecon.donnees["profil_par_defaut"]
    if profil != profil_principal and racine_alternative is None:
        raise ErreurLecon(
            f"{lecon.identifiant} — --sortie est obligatoire avec le profil "
            f"{profil!r}"
        )
    if racine_alternative is None:
        return lecon.chemin_sortie

    racine = (
        racine_alternative
        if racine_alternative.is_absolute()
        else RACINE / racine_alternative
    ).resolve()
    relatif = lecon.chemin_sortie.relative_to((RACINE / "Wiki" / "parcours").resolve())
    return racine / relatif


def main() -> int:
    """Assemble ou compare la sélection demandée."""

    arguments = analyser_arguments()
    try:
        registre = charger_registre()
        lecons = [
            charger_lecon(chemin, registre) for chemin in decouvrir_contrats()
        ]
        if arguments.lecon:
            lecons = [trouver_lecon(arguments.lecon, lecons)]
        if not lecons:
            raise ErreurLecon("aucun contrat de leçon découvert")

        erreurs: list[str] = []
        ecrites = 0
        identiques = 0
        for lecon in lecons:
            identifiant_profil = (
                arguments.profil or lecon.donnees["profil_par_defaut"]
            )
            profil = charger_profil(identifiant_profil, registre)
            texte = assembler(lecon, registre, profil)
            chemin = destination(lecon, identifiant_profil, arguments.sortie)

            observe = (
                chemin.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
                if chemin.exists()
                else None
            )
            if arguments.verifier:
                if observe is None:
                    erreurs.append(
                        f"{chemin_relatif(chemin)} — sortie assemblée absente"
                    )
                elif observe != texte:
                    erreurs.append(
                        f"{chemin_relatif(chemin)} — sortie différente des "
                        "sources canoniques"
                    )
                else:
                    identiques += 1
                continue

            if observe == texte:
                identiques += 1
                continue
            chemin.parent.mkdir(parents=True, exist_ok=True)
            chemin.write_text(texte, encoding="utf-8", newline="")
            ecrites += 1

        if erreurs:
            for erreur in erreurs:
                print(f"ERREUR · {erreur}", file=sys.stderr)
            return 1
    except (ErreurLecon, OSError, UnicodeError) as erreur:
        print(f"ERREUR · {erreur}", file=sys.stderr)
        return 1

    if arguments.verifier:
        print(f"{identiques} sortie(s) conforme(s) aux sources canoniques.")
    else:
        print(
            f"{ecrites} sortie(s) écrite(s) · "
            f"{identiques} déjà identique(s)."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
