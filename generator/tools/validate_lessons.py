"""Valide les contrats, états, fragments et sorties assemblées."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lessonlib import (
    DOSSIER_GLOSSAIRE,
    DOSSIER_PROFILS,
    RACINE,
    ErreurLecon,
    assembler,
    charger_attributions_cartographie,
    charger_etat,
    charger_lecon,
    charger_profil,
    charger_registre,
    chemin_fragment,
    chemin_relatif,
    decouvrir_contrats,
    slugifier_terme,
)
from glossarylib import fichiers_lecon, occurrences_texte


DOSSIER_WIKI = RACINE / "Wiki" / "parcours"
DELIMITEURS_MATHJAX_INTERDITS = re.compile(r"\\(?:\(|\)|\[|\])")


def verifier_glossaire(lecon, registre, profil) -> list[str]:
    """Vérifie les entrées, les premiers liens et le gras des répétitions."""

    erreurs: list[str] = []
    for terme in lecon.donnees["termes"]:
        slug = slugifier_terme(terme)
        chemin_entree = DOSSIER_GLOSSAIRE / f"{slug}.md"
        try:
            contenu_entree = chemin_entree.read_text(encoding="utf-8-sig")
        except FileNotFoundError:
            erreurs.append(
                f"{chemin_relatif(lecon.chemin_contrat)} — entrée de "
                f"glossaire absente pour {terme!r} : "
                f"{chemin_relatif(chemin_entree)}"
            )
            continue
        except (OSError, UnicodeError) as erreur:
            erreurs.append(
                f"{chemin_relatif(chemin_entree)} — illisible : {erreur}"
            )
            continue
        lignes_entree = contenu_entree.strip().splitlines()
        if not lignes_entree or lignes_entree[0] != f"# {terme}":
            erreurs.append(
                f"{chemin_relatif(chemin_entree)}:1 — titre attendu : # {terme}"
            )
        definition = [
            ligne
            for ligne in lignes_entree[1:]
            if ligne.strip() and not ligne.startswith("#")
        ]
        if not definition:
            erreurs.append(
                f"{chemin_relatif(chemin_entree)} — définition française absente"
            )

        occurrences = []
        for chemin in fichiers_lecon(lecon, registre, profil):
            texte = chemin.read_text(encoding="utf-8-sig")
            occurrences.extend(
                (
                    chemin,
                    texte[: occurrence.position].count("\n") + 1,
                    occurrence,
                )
                for occurrence in occurrences_texte(texte, terme, slug)
            )
        if not occurrences:
            erreurs.append(
                f"{chemin_relatif(lecon.chemin_contrat)} — terme déclaré "
                f"mais absent de la prose : {terme!r}"
            )
            continue
        chemin, numero, premiere = occurrences[0]
        if premiere.statut != "glossaire":
            erreurs.append(
                f"{chemin_relatif(chemin)}:{numero} — première occurrence "
                f"de {terme!r} sans lien vers le glossaire"
            )
        for chemin, numero, occurrence in occurrences[1:]:
            if occurrence.statut == "brut":
                erreurs.append(
                    f"{chemin_relatif(chemin)}:{numero} — occurrence suivante "
                    f"de {terme!r} non mise en gras"
                )
            elif occurrence.statut == "glossaire":
                erreurs.append(
                    f"{chemin_relatif(chemin)}:{numero} — lien de glossaire "
                    f"répété pour {terme!r}"
                )
    return erreurs


def verifier_lecon(lecon, registre) -> tuple[list[str], list[str]]:
    """Vérifie une leçon et sa sortie principale."""

    erreurs: list[str] = []
    avertissements: list[str] = []
    try:
        etat = charger_etat(lecon, registre)
    except ErreurLecon as erreur:
        return [str(erreur)], []

    for identifiant in lecon.donnees["sections"]:
        chemin = chemin_fragment(lecon, identifiant)
        statut = etat["sections"][identifiant]["statut"]
        if not chemin.is_file():
            if statut not in {"a-generer", "desactivee", "bloquee"}:
                erreurs.append(
                    f"{chemin_relatif(chemin)} — fragment absent avec le "
                    f"statut {statut!r}"
                )
            continue
        try:
            texte = chemin.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as erreur:
            erreurs.append(f"{chemin_relatif(chemin)} — illisible : {erreur}")
            continue
        attendu = registre["sections"][identifiant]["titre"]
        if not texte.startswith(f"## {attendu}\n"):
            erreurs.append(
                f"{chemin_relatif(chemin)} — titre attendu : ## {attendu}"
            )
        correspondance = DELIMITEURS_MATHJAX_INTERDITS.search(texte)
        if correspondance:
            ligne = texte[: correspondance.start()].count("\n") + 1
            diagnostic = (
                f"{chemin_relatif(chemin)}:{ligne} — délimiteur MathJax "
                "interdit ; utiliser $ ou $$"
            )
            if statut == "validee":
                erreurs.append(diagnostic)
            else:
                avertissements.append(diagnostic)

    for identifiant, valeur in etat["sections"].items():
        if valeur["statut"] != "validee":
            continue
        non_validees = [
            dependance
            for dependance in registre["sections"][identifiant]["dependances"]
            if etat["sections"].get(dependance, {}).get("statut") != "validee"
        ]
        if non_validees:
            erreurs.append(
                f"{chemin_relatif(lecon.chemin_etat)} — {identifiant!r} est "
                "validée avec des dépendances non validées : "
                + ", ".join(non_validees)
            )

    try:
        profil = charger_profil(lecon.donnees["profil_par_defaut"], registre)
        erreurs.extend(verifier_glossaire(lecon, registre, profil))
        attendu = assembler(lecon, registre, profil)
        chemin_sortie = lecon.chemin_sortie
        if not chemin_sortie.is_file():
            erreurs.append(
                f"{chemin_relatif(chemin_sortie)} — sortie assemblée absente"
            )
        else:
            observe = chemin_sortie.read_text(
                encoding="utf-8-sig"
            ).replace("\r\n", "\n")
            if observe != attendu:
                erreurs.append(
                    f"{chemin_relatif(chemin_sortie)} — sortie différente "
                    "des sources canoniques"
                )
    except (ErreurLecon, OSError, UnicodeError) as erreur:
        erreurs.append(str(erreur))
    return erreurs, avertissements


def main() -> int:
    """Exécute tous les contrôles de la génération par sections."""

    erreurs: list[str] = []
    avertissements: list[str] = []
    try:
        registre = charger_registre()
        attributions = charger_attributions_cartographie()
        for chemin_profil in sorted(DOSSIER_PROFILS.glob("*.json")):
            charger_profil(chemin_profil.stem, registre)

        lecons = []
        for chemin in decouvrir_contrats():
            try:
                lecons.append(charger_lecon(chemin, registre))
            except ErreurLecon as erreur:
                erreurs.append(str(erreur))

        ids: dict[str, Path] = {}
        sorties: dict[Path, Path] = {}
        for lecon in lecons:
            attribution = attributions.get(lecon.identifiant)
            if attribution is None:
                erreurs.append(
                    f"{chemin_relatif(lecon.chemin_contrat)} — leçon absente "
                    "des tableaux de découpage prévu"
                )
            elif attribution != lecon.donnees["attribution_cartographie"]:
                erreurs.append(
                    f"{chemin_relatif(lecon.chemin_contrat)} — attribution "
                    "différente de la cartographie"
                )
            if lecon.identifiant in ids:
                erreurs.append(
                    f"{chemin_relatif(lecon.chemin_contrat)} — id déjà employé "
                    f"par {chemin_relatif(ids[lecon.identifiant])}"
                )
            else:
                ids[lecon.identifiant] = lecon.chemin_contrat
            sortie = lecon.chemin_sortie.resolve()
            if sortie in sorties:
                erreurs.append(
                    f"{chemin_relatif(lecon.chemin_contrat)} — sortie déjà "
                    f"produite par {chemin_relatif(sorties[sortie])}"
                )
            else:
                sorties[sortie] = lecon.chemin_contrat
            erreurs_lecon, avertissements_lecon = verifier_lecon(lecon, registre)
            erreurs.extend(erreurs_lecon)
            avertissements.extend(avertissements_lecon)

        sorties_attendues = set(sorties)
        for chemin in sorted(DOSSIER_WIKI.rglob("*.md")):
            if chemin.resolve() not in sorties_attendues:
                erreurs.append(
                    f"{chemin_relatif(chemin)} — leçon assemblée sans contrat"
                )
    except (ErreurLecon, OSError, UnicodeError) as erreur:
        erreurs.append(str(erreur))

    if erreurs:
        for erreur in erreurs:
            print(f"ERREUR · {erreur}", file=sys.stderr)
        print(f"{len(erreurs)} erreur(s) détectée(s).", file=sys.stderr)
        return 1

    for avertissement in avertissements:
        print(f"AVERTISSEMENT · {avertissement}", file=sys.stderr)
    print(
        f"Génération valide · {len(lecons)} leçon(s) · "
        f"{len(registre['sections'])} section(s) déclarée(s) · "
        f"{len(avertissements)} avertissement(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
