"""Socle commun de la génération incrémentale des leçons.

Les fragments de ``generator/lessons`` sont canoniques. Les fichiers Markdown
de ``Wiki/parcours`` sont assemblés à partir de ces fragments.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


RACINE = Path(__file__).resolve().parents[2]
DOSSIER_GENERATEUR = RACINE / "generator"
DOSSIER_LECONS = DOSSIER_GENERATEUR / "lessons"
DOSSIER_PROFILS = DOSSIER_GENERATEUR / "profiles"
DOSSIER_GLOSSAIRE = RACINE / "Wiki" / "glossaire"
CHEMIN_SECTIONS = DOSSIER_GENERATEUR / "sections.json"
CHEMIN_CARTOGRAPHIE = (
    DOSSIER_GENERATEUR / "guardrails" / "parcours" / "cartographie.md"
)

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
STATUTS_CONTRAT = {"a-valider", "valide"}
STATUTS_SECTION = {
    "a-generer",
    "generee",
    "a-corriger",
    "validee",
    "desactivee",
    "bloquee",
}
CHAMPS_FRONTMATTER = {
    "id",
    "type",
    "titre",
    "parcours",
    "statut",
    "tags",
    "created",
    "updated",
    "verified",
    "processus",
    "brique",
    "contrat",
}


class ErreurLecon(Exception):
    """Erreur de contrat présentée sans trace d’exécution."""


def slugifier_terme(terme: str) -> str:
    """Transforme un terme consacré en nom stable d’entrée de glossaire."""

    sans_accents = "".join(
        caractere
        for caractere in unicodedata.normalize("NFKD", terme)
        if not unicodedata.combining(caractere)
    )
    slug = re.sub(r"[^a-z0-9]+", "-", sans_accents.casefold()).strip("-")
    if not slug or not SLUG.fullmatch(slug):
        raise ErreurLecon(f"terme de glossaire invalide : {terme!r}")
    return slug


@dataclass(frozen=True)
class Lecon:
    """Contrat chargé avec ses chemins résolus."""

    chemin_contrat: Path
    dossier: Path
    donnees: dict[str, Any]

    @property
    def identifiant(self) -> str:
        return self.donnees["id"]

    @property
    def titre(self) -> str:
        return self.donnees["titre"]

    @property
    def chemin_sortie(self) -> Path:
        return resoudre_dans_racine(self.donnees["sortie"], "sortie")

    @property
    def chemin_etat(self) -> Path:
        return self.dossier / "state.json"


def chemin_relatif(chemin: Path) -> str:
    """Retourne un chemin lisible depuis la racine."""

    try:
        return chemin.resolve().relative_to(RACINE.resolve()).as_posix()
    except ValueError:
        return str(chemin)


def lire_json(chemin: Path) -> dict[str, Any]:
    """Charge un objet JSON avec un diagnostic localisé."""

    try:
        contenu = json.loads(chemin.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as erreur:
        raise ErreurLecon(f"{chemin_relatif(chemin)} — fichier absent") from erreur
    except json.JSONDecodeError as erreur:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)}:{erreur.lineno}:{erreur.colno} — "
            f"JSON invalide : {erreur.msg}"
        ) from erreur
    except (OSError, UnicodeError) as erreur:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — fichier illisible : {erreur}"
        ) from erreur

    if not isinstance(contenu, dict):
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — la racine JSON doit être un objet"
        )
    return contenu


def ecrire_json(chemin: Path, contenu: dict[str, Any]) -> None:
    """Écrit un objet JSON de manière déterministe."""

    texte = json.dumps(contenu, ensure_ascii=False, indent=2) + "\n"
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(texte, encoding="utf-8", newline="")


def resoudre_dans_racine(valeur: str, champ: str) -> Path:
    """Résout un chemin relatif et interdit une sortie du dépôt."""

    if not isinstance(valeur, str) or not valeur:
        raise ErreurLecon(f"{champ} doit être un chemin relatif non vide")
    chemin = Path(valeur)
    if chemin.is_absolute():
        raise ErreurLecon(f"{champ} doit rester relatif à la racine")
    resolu = (RACINE / chemin).resolve()
    try:
        resolu.relative_to(RACINE.resolve())
    except ValueError as erreur:
        raise ErreurLecon(f"{champ} sort de la racine : {valeur!r}") from erreur
    return resolu


def resoudre_dans_dossier(dossier: Path, valeur: str, champ: str) -> Path:
    """Résout un fragment et interdit une sortie du dossier de la leçon."""

    if not isinstance(valeur, str) or not valeur:
        raise ErreurLecon(f"{champ} doit être un chemin relatif non vide")
    chemin = Path(valeur)
    if chemin.is_absolute():
        raise ErreurLecon(f"{champ} doit être relatif au dossier de la leçon")
    resolu = (dossier / chemin).resolve()
    try:
        resolu.relative_to(dossier.resolve())
    except ValueError as erreur:
        raise ErreurLecon(f"{champ} sort du dossier de la leçon") from erreur
    return resolu


def charger_registre() -> dict[str, Any]:
    """Charge et vérifie le registre des sections."""

    registre = lire_json(CHEMIN_SECTIONS)
    if registre.get("version") != 1:
        raise ErreurLecon(
            f"{chemin_relatif(CHEMIN_SECTIONS)} — version attendue : 1"
        )
    sections = registre.get("sections")
    ordre = registre.get("ordre_lecture")
    regles = registre.get("regles_communes")
    if not isinstance(sections, dict) or not sections:
        raise ErreurLecon("sections.json — sections doit être un objet non vide")
    if not isinstance(ordre, list) or set(ordre) != set(sections):
        raise ErreurLecon(
            "sections.json — ordre_lecture doit contenir chaque section une fois"
        )
    if not isinstance(regles, list) or not all(
        isinstance(item, str) for item in regles
    ):
        raise ErreurLecon("sections.json — regles_communes doit être une liste")

    for identifiant, definition in sections.items():
        if not SLUG.fullmatch(identifiant) or not isinstance(definition, dict):
            raise ErreurLecon(
                f"sections.json — définition invalide pour {identifiant!r}"
            )
        titre = definition.get("titre")
        dependances = definition.get("dependances")
        fichiers = definition.get("regles")
        if not isinstance(titre, str) or not titre:
            raise ErreurLecon(
                f"sections.json — titre absent pour {identifiant!r}"
            )
        if not isinstance(dependances, list) or not all(
            item in sections for item in dependances
        ):
            raise ErreurLecon(
                f"sections.json — dépendance inconnue pour {identifiant!r}"
            )
        if not isinstance(fichiers, list) or not all(
            isinstance(item, str) for item in fichiers
        ):
            raise ErreurLecon(
                f"sections.json — règles invalides pour {identifiant!r}"
            )

    verifier_cycles(sections)
    return registre


def verifier_cycles(sections: dict[str, Any]) -> None:
    """Refuse un cycle dans les dépendances de génération."""

    visites: set[str] = set()
    pile: list[str] = []

    def visiter(identifiant: str) -> None:
        if identifiant in pile:
            cycle = " → ".join(pile[pile.index(identifiant) :] + [identifiant])
            raise ErreurLecon(f"sections.json — cycle de dépendances : {cycle}")
        if identifiant in visites:
            return
        pile.append(identifiant)
        for dependance in sections[identifiant]["dependances"]:
            visiter(dependance)
        pile.pop()
        visites.add(identifiant)

    for identifiant in sections:
        visiter(identifiant)


def charger_profil(identifiant: str, registre: dict[str, Any]) -> dict[str, Any]:
    """Charge un profil et vérifie sa sélection."""

    if not SLUG.fullmatch(identifiant):
        raise ErreurLecon(f"profil invalide : {identifiant!r}")
    chemin = DOSSIER_PROFILS / f"{identifiant}.json"
    profil = lire_json(chemin)
    if profil.get("version") != 1 or profil.get("id") != identifiant:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — version ou identifiant incohérent"
        )
    obligatoires = profil.get("obligatoires")
    optionnelles = profil.get("optionnelles")
    if not isinstance(obligatoires, list) or not isinstance(optionnelles, list):
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — listes de sections absentes"
        )
    selection = obligatoires + optionnelles
    if len(selection) != len(set(selection)):
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — une section est sélectionnée deux fois"
        )
    inconnues = set(selection) - set(registre["sections"])
    if inconnues:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — sections inconnues : "
            f"{', '.join(sorted(inconnues))}"
        )
    return profil


def decouvrir_contrats() -> list[Path]:
    """Découvre tous les contrats canoniques."""

    if not DOSSIER_LECONS.exists():
        return []
    return sorted(DOSSIER_LECONS.rglob("contract.json"))


def charger_attributions_cartographie() -> dict[str, str]:
    """Lit les attributions des tableaux de découpage prévu."""

    try:
        lignes = CHEMIN_CARTOGRAPHIE.read_text(
            encoding="utf-8-sig"
        ).splitlines()
    except (OSError, UnicodeError) as erreur:
        raise ErreurLecon(
            f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)} — illisible : {erreur}"
        ) from erreur

    attributions: dict[str, str] = {}
    motif_id = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`")
    for numero, ligne in enumerate(lignes, start=1):
        if not ligne.startswith("|"):
            continue
        cellules = [cellule.strip() for cellule in ligne.strip("|").split("|")]
        if len(cellules) < 5:
            continue
        identifiant = motif_id.search(cellules[0])
        if identifiant is None or cellules[4] in {"Connaissances attribuées", "---"}:
            continue
        valeur = identifiant.group(1)
        if valeur in attributions:
            raise ErreurLecon(
                f"{chemin_relatif(CHEMIN_CARTOGRAPHIE)}:{numero} — "
                f"attribution dupliquée pour {valeur!r}"
            )
        attributions[valeur] = cellules[4]
    return attributions


def charger_lecon(chemin: Path, registre: dict[str, Any]) -> Lecon:
    """Charge un contrat et vérifie sa structure."""

    donnees = lire_json(chemin)
    dossier = chemin.parent
    if donnees.get("version") != 1:
        raise ErreurLecon(f"{chemin_relatif(chemin)} — version attendue : 1")
    if "statut" in donnees:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — le statut appartient à state.json"
        )

    identifiant = donnees.get("id")
    titre = donnees.get("titre")
    if not isinstance(identifiant, str) or not SLUG.fullmatch(identifiant):
        raise ErreurLecon(f"{chemin_relatif(chemin)} — id invalide")
    if dossier.name != identifiant:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — le dossier doit porter l’id de la leçon"
        )
    if not isinstance(titre, str) or not titre:
        raise ErreurLecon(f"{chemin_relatif(chemin)} — titre absent")

    for champ in (
        "concept_central",
        "attribution_cartographie",
        "sortie",
        "profil_par_defaut",
        "introduction",
    ):
        if not isinstance(donnees.get(champ), str) or not donnees[champ]:
            raise ErreurLecon(
                f"{chemin_relatif(chemin)} — champ {champ!r} absent"
            )
    sauts_fin = donnees.get("sauts_de_ligne_fin")
    if not isinstance(sauts_fin, int) or sauts_fin < 1:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — sauts_de_ligne_fin doit être "
            "un entier positif"
        )
    for champ in ("notions", "hors_perimetre", "termes"):
        valeur = donnees.get(champ)
        if not isinstance(valeur, list) or not all(
            isinstance(item, str) for item in valeur
        ):
            raise ErreurLecon(
                f"{chemin_relatif(chemin)} — {champ} doit être une liste"
            )
    termes = donnees["termes"]
    if any(not terme.strip() or terme != terme.strip() for terme in termes):
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — termes contient une entrée vide "
            "ou entourée d’espaces"
        )
    slugs_termes = [slugifier_terme(terme) for terme in termes]
    if len(slugs_termes) != len(set(slugs_termes)):
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — termes contient un doublon de glossaire"
        )
    regles_supplementaires = donnees.get("regles_supplementaires")
    if not isinstance(regles_supplementaires, list) or not all(
        isinstance(item, str) for item in regles_supplementaires
    ):
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — regles_supplementaires doit être "
            "une liste"
        )
    for valeur in regles_supplementaires:
        resoudre_dans_racine(valeur, "regles_supplementaires")

    frontmatter = donnees.get("frontmatter")
    if not isinstance(frontmatter, dict):
        raise ErreurLecon(f"{chemin_relatif(chemin)} — Frontmatter absent")
    absents = CHAMPS_FRONTMATTER - set(frontmatter)
    if absents:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — champs Frontmatter absents : "
            f"{', '.join(sorted(absents))}"
        )
    if frontmatter.get("id") != identifiant or frontmatter.get("titre") != titre:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — identité incohérente avec le Frontmatter"
        )
    if frontmatter.get("type") != "leçon":
        raise ErreurLecon(f"{chemin_relatif(chemin)} — type doit valoir leçon")
    tags = frontmatter.get("tags")
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        raise ErreurLecon(f"{chemin_relatif(chemin)} — tags doit être une liste")

    processus = frontmatter.get("processus")
    if not isinstance(processus, str) or not processus:
        raise ErreurLecon(f"{chemin_relatif(chemin)} — processus absent")
    if processus.startswith("aucun"):
        if "etape" in frontmatter:
            raise ErreurLecon(
                f"{chemin_relatif(chemin)} — etape interdite sans processus"
            )
        if not frontmatter.get("schema") or not frontmatter.get("element"):
            raise ErreurLecon(
                f"{chemin_relatif(chemin)} — schema et element obligatoires"
            )
    elif "schema" in frontmatter or "element" in frontmatter:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — schema et element interdits avec processus"
        )
    elif not frontmatter.get("etape"):
        raise ErreurLecon(f"{chemin_relatif(chemin)} — etape absente")

    sortie = resoudre_dans_racine(donnees["sortie"], "sortie")
    dossier_wiki = (RACINE / "Wiki" / "parcours").resolve()
    try:
        sortie.relative_to(dossier_wiki)
    except ValueError as erreur:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — sortie hors de Wiki/parcours"
        ) from erreur
    if sortie.suffix != ".md":
        raise ErreurLecon(f"{chemin_relatif(chemin)} — sortie non Markdown")

    introduction = resoudre_dans_dossier(
        dossier, donnees["introduction"], "introduction"
    )
    if not introduction.is_file():
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — introduction absente "
            f"{chemin_relatif(introduction)}"
        )

    sections = donnees.get("sections")
    if not isinstance(sections, dict):
        raise ErreurLecon(f"{chemin_relatif(chemin)} — sections absent")
    inconnues = set(sections) - set(registre["sections"])
    if inconnues:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — sections inconnues : "
            f"{', '.join(sorted(inconnues))}"
        )
    for identifiant_section, valeur in sections.items():
        resoudre_dans_dossier(
            dossier, valeur, f"sections.{identifiant_section}"
        )

    profil = donnees["profil_par_defaut"]
    charger_profil(profil, registre)
    return Lecon(chemin, dossier, donnees)


def charger_etat(lecon: Lecon, registre: dict[str, Any]) -> dict[str, Any]:
    """Charge et vérifie l’état de génération."""

    etat = lire_json(lecon.chemin_etat)
    if etat.get("version") != 1 or etat.get("lecon") != lecon.identifiant:
        raise ErreurLecon(
            f"{chemin_relatif(lecon.chemin_etat)} — identité incohérente"
        )
    contrat = etat.get("contrat")
    if not isinstance(contrat, dict) or contrat.get("statut") not in STATUTS_CONTRAT:
        raise ErreurLecon(
            f"{chemin_relatif(lecon.chemin_etat)} — statut du contrat invalide"
        )
    sections = etat.get("sections")
    if not isinstance(sections, dict):
        raise ErreurLecon(
            f"{chemin_relatif(lecon.chemin_etat)} — état des sections absent"
        )
    if set(sections) != set(lecon.donnees["sections"]):
        raise ErreurLecon(
            f"{chemin_relatif(lecon.chemin_etat)} — sections incohérentes "
            "avec le contrat"
        )
    for identifiant, valeur in sections.items():
        if identifiant not in registre["sections"] or not isinstance(valeur, dict):
            raise ErreurLecon(
                f"{chemin_relatif(lecon.chemin_etat)} — section invalide "
                f"{identifiant!r}"
            )
        if valeur.get("statut") not in STATUTS_SECTION:
            raise ErreurLecon(
                f"{chemin_relatif(lecon.chemin_etat)} — statut invalide pour "
                f"{identifiant!r}"
            )
    return etat


def chemin_fragment(lecon: Lecon, identifiant: str) -> Path:
    """Résout le chemin canonique d’une section."""

    valeur = lecon.donnees["sections"].get(identifiant)
    if valeur is None:
        raise ErreurLecon(
            f"{lecon.identifiant} — section absente du contrat : {identifiant}"
        )
    return resoudre_dans_dossier(
        lecon.dossier, valeur, f"sections.{identifiant}"
    )


def lire_fragment(chemin: Path) -> str:
    """Lit un fragment en normalisant seulement ses bordures."""

    try:
        return chemin.read_text(encoding="utf-8-sig").strip()
    except (OSError, UnicodeError) as erreur:
        raise ErreurLecon(
            f"{chemin_relatif(chemin)} — fragment illisible : {erreur}"
        ) from erreur


def encoder_valeur_frontmatter(valeur: Any) -> str:
    """Rend le sous-ensemble YAML employé par le Frontmatter."""

    if isinstance(valeur, list) and all(isinstance(item, str) for item in valeur):
        return "[" + ", ".join(valeur) + "]"
    if isinstance(valeur, str):
        return valeur
    raise ErreurLecon(
        f"Frontmatter — type non pris en charge : {type(valeur).__name__}"
    )


def rendre_frontmatter(frontmatter: dict[str, Any]) -> str:
    """Rend un Frontmatter stable en conservant l’ordre du contrat JSON."""

    lignes = ["---"]
    for cle, valeur in frontmatter.items():
        lignes.append(f"{cle}: {encoder_valeur_frontmatter(valeur)}")
    lignes.append("---")
    return "\n".join(lignes)


def selectionner_sections(
    lecon: Lecon,
    profil: dict[str, Any],
    registre: dict[str, Any],
) -> list[str]:
    """Sélectionne les fragments présents dans l’ordre de lecture."""

    disponibles = {
        identifiant
        for identifiant in lecon.donnees["sections"]
        if chemin_fragment(lecon, identifiant).is_file()
    }
    absentes = set(profil["obligatoires"]) - disponibles
    if absentes:
        raise ErreurLecon(
            f"{lecon.identifiant} — sections obligatoires absentes du profil "
            f"{profil['id']!r} : {', '.join(sorted(absentes))}"
        )
    selection = set(profil["obligatoires"])
    selection.update(set(profil["optionnelles"]) & disponibles)
    return [
        identifiant
        for identifiant in registre["ordre_lecture"]
        if identifiant in selection
    ]


def assembler(
    lecon: Lecon,
    registre: dict[str, Any],
    profil: dict[str, Any],
) -> str:
    """Assemble une leçon depuis ses sources canoniques."""

    morceaux = [
        rendre_frontmatter(lecon.donnees["frontmatter"]),
        f"# {lecon.titre}",
    ]
    introduction = lire_fragment(
        resoudre_dans_dossier(
            lecon.dossier, lecon.donnees["introduction"], "introduction"
        )
    )
    if introduction:
        morceaux.append(introduction)

    for identifiant in selectionner_sections(lecon, profil, registre):
        chemin = chemin_fragment(lecon, identifiant)
        fragment = lire_fragment(chemin)
        titre_attendu = registre["sections"][identifiant]["titre"]
        if not fragment.startswith(f"## {titre_attendu}\n") and fragment != (
            f"## {titre_attendu}"
        ):
            raise ErreurLecon(
                f"{chemin_relatif(chemin)} — le fragment doit commencer par "
                f"'## {titre_attendu}'"
            )
        morceaux.append(fragment)
    return "\n\n".join(morceaux) + "\n" * lecon.donnees["sauts_de_ligne_fin"]


def trouver_lecon(
    identifiant: str,
    lecons: Iterable[Lecon],
) -> Lecon:
    """Trouve une leçon par identifiant."""

    correspondances = [
        lecon for lecon in lecons if lecon.identifiant == identifiant
    ]
    if not correspondances:
        raise ErreurLecon(f"leçon inconnue : {identifiant!r}")
    if len(correspondances) > 1:
        raise ErreurLecon(f"identifiant de leçon dupliqué : {identifiant!r}")
    return correspondances[0]
