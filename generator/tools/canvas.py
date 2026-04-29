"""Valide les Canvas canoniques et génère les vues des leçons.

Les processus et schémas de référence sont les sources de vérité. Une vue
contextualisée n'est jamais éditée à la main : elle est dérivée du couple
``processus``–``etape`` ou ``schema``–``element`` d'une leçon.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RACINE = Path(__file__).resolve().parents[2]
DOSSIER_GARDE_FOUS = RACINE / "generator" / "guardrails"
DOSSIER_PROCESSUS = DOSSIER_GARDE_FOUS / "schema" / "processus"
DOSSIER_SCHEMAS = DOSSIER_GARDE_FOUS / "schema" / "references"
DOSSIER_LECONS = RACINE / "Wiki" / "parcours"
DOSSIER_VUES = DOSSIER_GARDE_FOUS / "schema" / "canvas"
CHEMIN_CARTOGRAPHIE = DOSSIER_GARDE_FOUS / "parcours" / "cartographie.md"

CHAMPS_NOEUD = {"id", "type", "x", "y", "width", "height"}
TYPES_NOEUD = {"text", "file", "link", "group"}
CHAMPS_ARETE = {"id", "fromNode", "toNode"}
COTES = {"top", "right", "bottom", "left"}
EXTREMITES = {"none", "arrow"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ErreurCanvas(Exception):
    """Erreur de contrat destinée à être affichée sans trace Python."""


@dataclass(frozen=True)
class Lecon:
    """Référence d'une leçon vers une pièce d'un Canvas canonique."""

    identifiant: str
    chemin: Path
    processus: str | None = None
    etape: str | None = None
    schema: str | None = None
    element: str | None = None


def chemin_relatif(chemin: Path) -> str:
    """Retourne un chemin lisible depuis la racine du dépôt."""

    return chemin.relative_to(RACINE).as_posix()


def charger_json(chemin: Path) -> dict[str, Any]:
    """Charge un objet JSON et transforme les erreurs en diagnostics lisibles."""

    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        raise ErreurCanvas(
            f"{chemin_relatif(chemin)}:{erreur.lineno}:{erreur.colno} "
            f"JSON invalide — {erreur.msg}"
        ) from erreur
    except OSError as erreur:
        raise ErreurCanvas(
            f"{chemin_relatif(chemin)} illisible — {erreur}"
        ) from erreur

    if not isinstance(contenu, dict):
        raise ErreurCanvas(
            f"{chemin_relatif(chemin)} — la racine JSON doit être un objet"
        )
    return contenu


def verifier_nombre(
    valeur: Any,
    champ: str,
    identifiant: str,
    chemin: Path,
    *,
    strictement_positif: bool = False,
) -> None:
    """Vérifie un nombre JSON, en excluant les booléens."""

    valide = isinstance(valeur, (int, float)) and not isinstance(valeur, bool)
    if strictement_positif:
        valide = valide and valeur > 0
    if not valide:
        contrainte = "un nombre strictement positif" if strictement_positif else "un nombre"
        raise ErreurCanvas(
            f"{chemin_relatif(chemin)} — nœud {identifiant!r} : "
            f"{champ} doit être {contrainte}"
        )


def verifier_canvas(contenu: dict[str, Any], chemin: Path) -> None:
    """Vérifie le sous-ensemble structurel de JSON Canvas 1.0 utilisé ici."""

    noeuds = contenu.get("nodes")
    aretes = contenu.get("edges")
    if not isinstance(noeuds, list) or not isinstance(aretes, list):
        raise ErreurCanvas(
            f"{chemin_relatif(chemin)} — nodes et edges doivent être des listes"
        )

    ids_noeuds: set[str] = set()
    for position, noeud in enumerate(noeuds):
        if not isinstance(noeud, dict):
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — nœud #{position} invalide"
            )

        absents = CHAMPS_NOEUD - noeud.keys()
        if absents:
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — nœud #{position} : "
                f"champs absents {', '.join(sorted(absents))}"
            )

        identifiant = noeud["id"]
        if not isinstance(identifiant, str) or not identifiant:
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — nœud #{position} : id invalide"
            )
        if identifiant in ids_noeuds:
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — id de nœud dupliqué {identifiant!r}"
            )
        ids_noeuds.add(identifiant)
        if identifiant.startswith("note:"):
            if not SLUG.fullmatch(identifiant.removeprefix("note:")):
                raise ErreurCanvas(
                    f"{chemin_relatif(chemin)} — annotation "
                    f"{identifiant!r} : suffixe non canonique"
                )
        elif not SLUG.fullmatch(identifiant):
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — nœud {identifiant!r} : "
                "identifiant d'étape non canonique"
            )

        type_noeud = noeud["type"]
        if type_noeud not in TYPES_NOEUD:
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — nœud {identifiant!r} : "
                f"type inconnu {type_noeud!r}"
            )

        verifier_nombre(noeud["x"], "x", identifiant, chemin)
        verifier_nombre(noeud["y"], "y", identifiant, chemin)
        verifier_nombre(
            noeud["width"],
            "width",
            identifiant,
            chemin,
            strictement_positif=True,
        )
        verifier_nombre(
            noeud["height"],
            "height",
            identifiant,
            chemin,
            strictement_positif=True,
        )

        champ_par_type = {"text": "text", "file": "file", "link": "url"}
        champ_requis = champ_par_type.get(type_noeud)
        if champ_requis and (
            not isinstance(noeud.get(champ_requis), str)
            or not noeud[champ_requis]
        ):
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — nœud {identifiant!r} : "
                f"{champ_requis} doit être une chaîne non vide"
            )

        couleur = noeud.get("color")
        if couleur is not None and not isinstance(couleur, str):
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — nœud {identifiant!r} : "
                "color doit être une chaîne"
            )

    ids_aretes: set[str] = set()
    for position, arete in enumerate(aretes):
        if not isinstance(arete, dict):
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — arête #{position} invalide"
            )

        absents = CHAMPS_ARETE - arete.keys()
        if absents:
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — arête #{position} : "
                f"champs absents {', '.join(sorted(absents))}"
            )

        identifiant = arete["id"]
        if not isinstance(identifiant, str) or not identifiant:
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — arête #{position} : id invalide"
            )
        if identifiant in ids_aretes:
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — id d'arête dupliqué "
                f"{identifiant!r}"
            )
        ids_aretes.add(identifiant)
        if not SLUG.fullmatch(identifiant):
            raise ErreurCanvas(
                f"{chemin_relatif(chemin)} — arête {identifiant!r} : "
                "identifiant non canonique"
            )

        for champ in ("fromNode", "toNode"):
            if arete[champ] not in ids_noeuds:
                raise ErreurCanvas(
                    f"{chemin_relatif(chemin)} — arête {identifiant!r} : "
                    f"{champ} référence un nœud absent {arete[champ]!r}"
                )

        for champ in ("fromSide", "toSide"):
            if champ in arete and arete[champ] not in COTES:
                raise ErreurCanvas(
                    f"{chemin_relatif(chemin)} — arête {identifiant!r} : "
                    f"{champ} invalide {arete[champ]!r}"
                )

        for champ in ("fromEnd", "toEnd"):
            if champ in arete and arete[champ] not in EXTREMITES:
                raise ErreurCanvas(
                    f"{chemin_relatif(chemin)} — arête {identifiant!r} : "
                    f"{champ} invalide {arete[champ]!r}"
                )


def lire_frontmatter(chemin: Path) -> dict[str, str] | None:
    """Lit les scalaires utiles d'un Frontmatter YAML sans dépendance externe."""

    lignes = chemin.read_text(encoding="utf-8-sig").splitlines()
    if not lignes or lignes[0].strip() != "---":
        return None

    fin = next(
        (index for index, ligne in enumerate(lignes[1:], start=1) if ligne.strip() == "---"),
        None,
    )
    if fin is None:
        raise ErreurCanvas(
            f"{chemin_relatif(chemin)} — Frontmatter ouvert mais non fermé"
        )

    donnees: dict[str, str] = {}
    for ligne in lignes[1:fin]:
        correspondance = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", ligne)
        if not correspondance:
            continue
        cle, valeur = correspondance.groups()
        if len(valeur) >= 2 and valeur[0] == valeur[-1] and valeur[0] in "\"'":
            valeur = valeur[1:-1]
        donnees[cle] = valeur
    return donnees


def decouvrir_lecons() -> tuple[list[Lecon], list[str]]:
    """Découvre les leçons et vérifie leur référence visuelle."""

    if not DOSSIER_LECONS.exists():
        return [], []

    lecons: list[Lecon] = []
    erreurs: list[str] = []
    ids: dict[str, Path] = {}

    for chemin in sorted(DOSSIER_LECONS.rglob("*.md")):
        try:
            frontmatter = lire_frontmatter(chemin)
        except (ErreurCanvas, OSError, UnicodeError) as erreur:
            erreurs.append(str(erreur))
            continue

        if frontmatter is None or frontmatter.get("type") != "leçon":
            continue

        identifiant = frontmatter.get("id", "")
        processus = frontmatter.get("processus", "")
        etape = frontmatter.get("etape", "")
        schema = frontmatter.get("schema", "")
        element = frontmatter.get("element", "")

        if not identifiant:
            erreurs.append(f"{chemin_relatif(chemin)} — id de leçon absent")
            continue
        if not SLUG.fullmatch(identifiant):
            erreurs.append(
                f"{chemin_relatif(chemin)} — id de leçon non canonique "
                f"{identifiant!r}"
            )
        if identifiant in ids:
            erreurs.append(
                f"{chemin_relatif(chemin)} — id {identifiant!r} déjà utilisé "
                f"par {chemin_relatif(ids[identifiant])}"
            )
        else:
            ids[identifiant] = chemin

        if not processus:
            erreurs.append(
                f"{chemin_relatif(chemin)} — processus absent ; utiliser un "
                "identifiant ou « aucun — <raison> »"
            )
            continue

        if processus.startswith("aucun"):
            if etape:
                erreurs.append(
                    f"{chemin_relatif(chemin)} — etape doit être absente "
                    "lorsque processus vaut « aucun — <raison> »"
                )
            if not re.fullmatch(r"aucun — .+", processus):
                erreurs.append(
                    f"{chemin_relatif(chemin)} — l'absence de processus "
                    "doit porter une raison"
                )
            if not schema or not element:
                erreurs.append(
                    f"{chemin_relatif(chemin)} — schema et element sont "
                    "obligatoires sans processus"
                )
                continue
            if not SLUG.fullmatch(schema):
                erreurs.append(
                    f"{chemin_relatif(chemin)} — identifiant de schéma non "
                    f"canonique {schema!r}"
                )
                continue
            if not SLUG.fullmatch(element):
                erreurs.append(
                    f"{chemin_relatif(chemin)} — identifiant d'élément non "
                    f"canonique {element!r}"
                )
                continue
            lecons.append(
                Lecon(
                    identifiant=identifiant,
                    chemin=chemin,
                    schema=schema,
                    element=element,
                )
            )
            continue

        if schema or element:
            erreurs.append(
                f"{chemin_relatif(chemin)} — schema et element doivent être "
                "absents lorsqu'un processus est déclaré"
            )
            continue

        if not SLUG.fullmatch(processus):
            erreurs.append(
                f"{chemin_relatif(chemin)} — identifiant de processus non "
                f"canonique {processus!r}"
            )
            continue
        if not etape:
            erreurs.append(
                f"{chemin_relatif(chemin)} — etape absente pour le processus "
                f"{processus!r}"
            )
            continue
        if not SLUG.fullmatch(etape):
            erreurs.append(
                f"{chemin_relatif(chemin)} — identifiant d'étape non "
                f"canonique {etape!r}"
            )
            continue

        lecons.append(
            Lecon(
                identifiant=identifiant,
                chemin=chemin,
                processus=processus,
                etape=etape,
            )
        )

    return lecons, erreurs


def charger_processus() -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Charge et valide tous les Canvas canoniques."""

    processus: dict[str, dict[str, Any]] = {}
    erreurs: list[str] = []

    if not DOSSIER_PROCESSUS.exists():
        return {}, [f"{chemin_relatif(DOSSIER_PROCESSUS)} — dossier absent"]

    for chemin in sorted(DOSSIER_PROCESSUS.glob("*.canvas")):
        identifiant = chemin.stem
        if not SLUG.fullmatch(identifiant):
            erreurs.append(
                f"{chemin_relatif(chemin)} — nom de processus non canonique"
            )
        try:
            contenu = charger_json(chemin)
            verifier_canvas(contenu, chemin)
        except ErreurCanvas as erreur:
            erreurs.append(str(erreur))
            continue
        processus[identifiant] = contenu

    if not processus and not erreurs:
        erreurs.append(
            f"{chemin_relatif(DOSSIER_PROCESSUS)} — aucun processus canonique"
        )
    return processus, erreurs


def charger_schemas() -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Charge et valide les Canvas canoniques non séquentiels."""

    schemas: dict[str, dict[str, Any]] = {}
    erreurs: list[str] = []

    if not DOSSIER_SCHEMAS.exists():
        return {}, [f"{chemin_relatif(DOSSIER_SCHEMAS)} — dossier absent"]

    for chemin in sorted(DOSSIER_SCHEMAS.glob("*.canvas")):
        identifiant = chemin.stem
        if not SLUG.fullmatch(identifiant):
            erreurs.append(
                f"{chemin_relatif(chemin)} — nom de schéma non canonique"
            )
        try:
            contenu = charger_json(chemin)
            verifier_canvas(contenu, chemin)
        except ErreurCanvas as erreur:
            erreurs.append(str(erreur))
            continue
        schemas[identifiant] = contenu

    if not schemas and not erreurs:
        erreurs.append(
            f"{chemin_relatif(DOSSIER_SCHEMAS)} — aucun schéma canonique"
        )
    return schemas, erreurs


def verifier_references_cartographie(
    processus: dict[str, dict[str, Any]],
    schemas: dict[str, dict[str, Any]],
) -> tuple[int, list[str]]:
    """Vérifie les références visuelles des tableaux de leçons prévus."""

    try:
        lignes = CHEMIN_CARTOGRAPHIE.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as erreur:
        return 0, [
            f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)} illisible — {erreur}"
        ]

    dans_table = False
    nombre_references = 0
    erreurs: list[str] = []

    for numero, ligne in enumerate(lignes, start=1):
        if ligne.startswith("|") and "Processus · étape" in ligne:
            dans_table = True
            continue
        if dans_table and not ligne.startswith("|"):
            dans_table = False
            continue
        if not dans_table or re.fullmatch(r"\|[\s|:-]+\|", ligne):
            continue

        cellules = [cellule.strip() for cellule in ligne.strip("|").split("|")]
        if len(cellules) < 4:
            erreurs.append(
                f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                "ligne de découpage incomplète"
            )
            continue

        reference_processus = cellules[2]
        reference_schema = cellules[3]
        nombre_references += 1
        sans_processus = reference_processus.startswith("`aucun")

        if sans_processus:
            if not re.fullmatch(r"`aucun — [^`]+`", reference_processus):
                erreurs.append(
                    f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                    "l'absence de processus doit porter une raison"
                )
        else:
            correspondance = re.fullmatch(
                r"`([a-z0-9]+(?:-[a-z0-9]+)*)`\s*·\s*"
                r"`([a-z0-9]+(?:-[a-z0-9]+)*)`",
                reference_processus,
            )
            if not correspondance:
                erreurs.append(
                    f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                    "référence processus–étape invalide "
                    f"{reference_processus!r}"
                )
            else:
                identifiant_processus, identifiant_etape = (
                    correspondance.groups()
                )
                canvas = processus.get(identifiant_processus)
                if canvas is None:
                    erreurs.append(
                        f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                        f"processus absent {identifiant_processus!r}"
                    )
                else:
                    ids_structurels = {
                        noeud["id"]
                        for noeud in canvas["nodes"]
                        if not noeud["id"].startswith("note:")
                    }
                    if identifiant_etape not in ids_structurels:
                        erreurs.append(
                            f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                            f"étape absente {identifiant_etape!r} dans "
                            f"{identifiant_processus!r}"
                        )

        if not sans_processus:
            if reference_schema != "—":
                erreurs.append(
                    f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                    "un repère de processus ne reçoit pas un second schéma"
                )
            continue

        if reference_schema == "à cadrer":
            continue

        correspondance_schema = re.fullmatch(
            r"`([a-z0-9]+(?:-[a-z0-9]+)*)`\s*·\s*"
            r"`([a-z0-9]+(?:-[a-z0-9]+)*)`",
            reference_schema,
        )
        if not correspondance_schema:
            erreurs.append(
                f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                f"référence schéma–élément invalide {reference_schema!r}"
            )
            continue

        identifiant_schema, identifiant_element = (
            correspondance_schema.groups()
        )
        canvas = schemas.get(identifiant_schema)
        if canvas is None:
            erreurs.append(
                f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                f"schéma absent {identifiant_schema!r}"
            )
            continue

        ids_structurels = {
            noeud["id"]
            for noeud in canvas["nodes"]
            if not noeud["id"].startswith("note:")
        }
        if identifiant_element not in ids_structurels:
            erreurs.append(
                f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                f"élément absent {identifiant_element!r} dans "
                f"{identifiant_schema!r}"
            )

    return nombre_references, erreurs


def prefixer(noeud: dict[str, Any], etiquette: str, couleur: str) -> None:
    """Ajoute le rôle visuel sans dépendre uniquement de la couleur."""

    if noeud.get("type") == "text":
        noeud["text"] = f"**{etiquette}**\n\n{noeud['text']}"
    elif noeud.get("type") == "group":
        libelle = noeud.get("label", noeud["id"])
        noeud["label"] = f"{etiquette} · {libelle}"
    else:
        raise ErreurCanvas(
            f"le nœud {noeud.get('id')!r} doit être de type text ou group "
            "pour porter un rôle dans une vue de leçon"
        )
    noeud["color"] = couleur


def produire_vue(
    lecon: Lecon,
    processus: dict[str, dict[str, Any]],
    schemas: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Construit la vue contextualisée d'une leçon."""

    est_processus = lecon.processus is not None
    if est_processus:
        if lecon.processus not in processus:
            raise ErreurCanvas(
                f"{chemin_relatif(lecon.chemin)} — processus absent "
                f"{lecon.processus!r}"
            )
        source = processus[lecon.processus]
        cible = lecon.etape
    else:
        if lecon.schema not in schemas:
            raise ErreurCanvas(
                f"{chemin_relatif(lecon.chemin)} — schéma absent "
                f"{lecon.schema!r}"
            )
        source = schemas[lecon.schema]
        cible = lecon.element

    ids_structurels = {
        noeud["id"]
        for noeud in source["nodes"]
        if not noeud["id"].startswith("note:")
    }
    if cible not in ids_structurels:
        nature = "étape" if est_processus else "élément"
        source_id = lecon.processus if est_processus else lecon.schema
        raise ErreurCanvas(
            f"{chemin_relatif(lecon.chemin)} — {nature} absent "
            f"{cible!r} dans {source_id!r}"
        )

    aretes = [
        copy.deepcopy(arete)
        for arete in source["edges"]
        if arete["fromNode"] in ids_structurels
        and arete["toNode"] in ids_structurels
    ]
    predecesseurs: set[str] = set()
    successeurs: set[str] = set()
    relations: set[str] = set()
    if est_processus:
        predecesseurs = {
            arete["fromNode"]
            for arete in aretes
            if arete["toNode"] == cible
        }
        successeurs = {
            arete["toNode"]
            for arete in aretes
            if arete["fromNode"] == cible
        }
    else:
        relations = {
            extremite
            for arete in aretes
            if cible in (arete["fromNode"], arete["toNode"])
            for extremite in (arete["fromNode"], arete["toNode"])
            if extremite != cible
        }

    noeuds: list[dict[str, Any]] = []
    for source_noeud in source["nodes"]:
        identifiant = source_noeud["id"]
        if identifiant not in ids_structurels:
            continue

        noeud = copy.deepcopy(source_noeud)
        noeud.pop("color", None)
        if identifiant == cible:
            etiquette = "ÉTAPE OUVERTE" if est_processus else "ÉLÉMENT OUVERT"
            prefixer(noeud, etiquette, "6")
        elif est_processus:
            if identifiant in predecesseurs and identifiant in successeurs:
                prefixer(noeud, "AMONT ET AVAL", "3")
            elif identifiant in predecesseurs:
                prefixer(noeud, "AMONT", "5")
            elif identifiant in successeurs:
                prefixer(noeud, "AVAL", "4")
        elif identifiant in relations:
            prefixer(noeud, "RELATION DIRECTE", "5")
        noeuds.append(noeud)

    return {"nodes": noeuds, "edges": aretes}


def encoder_json(contenu: dict[str, Any]) -> str:
    """Sérialise un Canvas de façon déterministe et lisible."""

    return json.dumps(contenu, ensure_ascii=False, indent=2) + "\n"


def construire_vues(
    lecons: list[Lecon],
    processus: dict[str, dict[str, Any]],
    schemas: dict[str, dict[str, Any]],
) -> tuple[dict[Path, dict[str, Any]], list[str]]:
    """Construit toutes les vues attendues sans encore écrire de fichier."""

    vues: dict[Path, dict[str, Any]] = {}
    erreurs: list[str] = []
    for lecon in lecons:
        try:
            vues[DOSSIER_VUES / f"{lecon.identifiant}.canvas"] = produire_vue(
                lecon,
                processus,
                schemas,
            )
        except ErreurCanvas as erreur:
            erreurs.append(str(erreur))
    return vues, erreurs


def verifier_vues(vues: dict[Path, dict[str, Any]]) -> list[str]:
    """Compare les vues présentes aux vues dérivées attendues."""

    erreurs: list[str] = []
    attendus = set(vues)

    for chemin, attendu in vues.items():
        if not chemin.exists():
            erreurs.append(f"{chemin_relatif(chemin)} — vue générée absente")
            continue
        try:
            observe = charger_json(chemin)
            verifier_canvas(observe, chemin)
        except ErreurCanvas as erreur:
            erreurs.append(str(erreur))
            continue
        if observe != attendu:
            erreurs.append(
                f"{chemin_relatif(chemin)} — vue périmée ; relancer "
                "python generator/tools/canvas.py"
            )

    if DOSSIER_VUES.exists():
        for chemin in sorted(DOSSIER_VUES.glob("*.canvas")):
            if chemin not in attendus:
                erreurs.append(
                    f"{chemin_relatif(chemin)} — vue orpheline sans leçon"
                )
    return erreurs


def ecrire_vues(vues: dict[Path, dict[str, Any]]) -> None:
    """Écrit les vues attendues sans supprimer les éventuels orphelins."""

    DOSSIER_VUES.mkdir(parents=True, exist_ok=True)
    for chemin, contenu in vues.items():
        chemin.write_text(encoder_json(contenu), encoding="utf-8")


def analyser_arguments() -> argparse.Namespace:
    """Déclare l'interface en ligne de commande."""

    analyseur = argparse.ArgumentParser(
        description=(
            "Valide les Canvas canoniques et génère les vues "
            "contextualisées des leçons."
        )
    )
    analyseur.add_argument(
        "--verifier",
        action="store_true",
        help="vérifie que les vues présentes sont à jour sans écrire",
    )
    return analyseur.parse_args()


def main() -> int:
    """Exécute la validation puis la génération ou la vérification."""

    arguments = analyser_arguments()
    processus, erreurs_processus = charger_processus()
    schemas, erreurs_schemas = charger_schemas()
    references, erreurs_cartographie = verifier_references_cartographie(
        processus,
        schemas,
    )
    lecons, erreurs_lecons = decouvrir_lecons()
    vues, erreurs_vues = construire_vues(lecons, processus, schemas)
    erreurs = (
        erreurs_processus
        + erreurs_schemas
        + erreurs_cartographie
        + erreurs_lecons
        + erreurs_vues
    )

    if not erreurs and arguments.verifier:
        erreurs.extend(verifier_vues(vues))

    if erreurs:
        for erreur in erreurs:
            print(f"ERREUR · {erreur}", file=sys.stderr)
        print(f"{len(erreurs)} erreur(s) détectée(s).", file=sys.stderr)
        return 1

    if arguments.verifier:
        print(
            f"Canvas valides · {len(processus)} processus · "
            f"{len(schemas)} schéma(s) · "
            f"{references} référence(s) cartographiques · "
            f"{len(vues)} vue(s) de leçon à jour."
        )
    else:
        ecrire_vues(vues)
        print(
            f"Canvas générés · {len(processus)} processus validé(s) · "
            f"{len(schemas)} schéma(s) validé(s) · "
            f"{references} référence(s) cartographiques · "
            f"{len(vues)} vue(s) écrite(s)."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
