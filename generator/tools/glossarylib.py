"""Analyse et mise en forme des termes de glossaire dans les leçons."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


CODE_INLINE = re.compile(r"`+[^`\n]+`+")
LIEN_MARKDOWN = re.compile(r"!?\[[^\]]*\]\([^\)]+\)", re.DOTALL)
LIEN_WIKI = re.compile(
    r"!?\[\["
    r"(?P<cible>[^\]|]+)"
    r"(?:\|(?P<libelle>[^\]]+))?"
    r"\]\]",
    re.DOTALL,
)
GRAS = re.compile(
    r"(?<!\*)\*\*(?!\*)(?P<contenu>.+?)(?<!\*)\*\*(?!\*)",
    re.DOTALL,
)


@dataclass(frozen=True)
class Occurrence:
    """Occurrence localisée d’un terme dans la prose."""

    position: int
    statut: str
    surface: str


def motif_terme(terme: str) -> re.Pattern[str]:
    """Construit un motif insensible à la casse avec pluriel simple."""

    morceaux = re.split(r"\s+", terme)
    variantes = [re.escape(morceau) for morceau in morceaux]
    dernier = terme[-1]
    if (
        len(variantes) > 1
        and morceaux[0][-1].isalpha()
        and morceaux[0][-1].casefold() not in {"s", "x", "z"}
    ):
        variantes[0] += "s?"
    pluriel = (
        "s?"
        if dernier.isalpha() and dernier.casefold() not in {"s", "x", "z"}
        else ""
    )
    corps = r"\s+".join(variantes)
    return re.compile(rf"(?<!\w){corps}{pluriel}(?!\w)", re.IGNORECASE)


def cible_glossaire(cible: str) -> str:
    """Normalise une cible Obsidian de glossaire sans ancre ni extension."""

    normalisee = cible.split("#", 1)[0].replace("\\", "/").strip("/")
    if normalisee.casefold().endswith(".md"):
        normalisee = normalisee[:-3]
    return normalisee.casefold()


def intervalles_blocs_code(texte: str) -> list[tuple[int, int]]:
    """Localise les blocs de code délimités, y compris sur plusieurs lignes."""

    intervalles: list[tuple[int, int]] = []
    debut: int | None = None
    marqueur: str | None = None
    position = 0
    for ligne in texte.splitlines(keepends=True):
        correspondance = re.match(r"^\s*(```|~~~)", ligne)
        if correspondance:
            courant = correspondance.group(1)
            if debut is None:
                debut = position
                marqueur = courant
            elif courant == marqueur:
                intervalles.append((debut, position + len(ligne)))
                debut = None
                marqueur = None
        position += len(ligne)
    if debut is not None:
        intervalles.append((debut, len(texte)))
    return intervalles


def chevauche(
    debut: int,
    fin: int,
    intervalles: list[tuple[int, int]],
) -> bool:
    """Indique si une plage rencontre un intervalle protégé."""

    return any(
        debut < borne_fin and fin > borne_debut
        for borne_debut, borne_fin in intervalles
    )


def occurrences_texte(
    texte: str,
    terme: str,
    slug: str,
) -> list[Occurrence]:
    """Repère les occurrences de prose et leur mise en forme."""

    motif = motif_terme(terme)
    protegees = intervalles_blocs_code(texte)
    occurrences: list[Occurrence] = []

    for correspondance in CODE_INLINE.finditer(texte):
        protegees.append(correspondance.span())
    for correspondance in LIEN_MARKDOWN.finditer(texte):
        protegees.append(correspondance.span())
    for correspondance in LIEN_WIKI.finditer(texte):
        debut, fin = correspondance.span()
        if chevauche(debut, fin, protegees):
            continue
        protegees.append((debut, fin))
        libelle = correspondance.group("libelle")
        if (
            libelle is not None
            and cible_glossaire(correspondance.group("cible"))
            == f"glossaire/{slug}".casefold()
        ):
            for terme_lie in motif.finditer(libelle):
                occurrences.append(
                    Occurrence(
                        correspondance.start("libelle") + terme_lie.start(),
                        "glossaire",
                        terme_lie.group(0),
                    )
                )
    for correspondance in GRAS.finditer(texte):
        debut, fin = correspondance.span()
        if chevauche(debut, fin, protegees):
            continue
        protegees.append((debut, fin))
        contenu = correspondance.group("contenu")
        for terme_gras in motif.finditer(contenu):
            occurrences.append(
                Occurrence(
                    correspondance.start("contenu") + terme_gras.start(),
                    "gras",
                    terme_gras.group(0),
                )
            )

    masque = [False] * len(texte)
    for debut, fin in protegees:
        for position in range(max(0, debut), min(len(texte), fin)):
            masque[position] = True
    for correspondance in motif.finditer(texte):
        debut, fin = correspondance.span()
        if not any(masque[debut:fin]):
            occurrences.append(
                Occurrence(debut, "brut", correspondance.group(0))
            )
    return sorted(occurrences, key=lambda occurrence: occurrence.position)


def formater_terme(
    texte: str,
    terme: str,
    slug: str,
    deja_vues: int,
) -> tuple[str, int]:
    """Lie la première occurrence et met les suivantes en gras."""

    vues = deja_vues
    morceaux: list[str] = []
    curseur = 0
    for occurrence in occurrences_texte(texte, terme, slug):
        if occurrence.statut != "brut":
            vues += 1
            continue
        debut = occurrence.position
        fin = debut + len(occurrence.surface)
        morceaux.append(texte[curseur:debut])
        if vues == 0:
            morceaux.append(f"[[glossaire/{slug}|{occurrence.surface}]]")
        else:
            morceaux.append(f"**{occurrence.surface}**")
        curseur = fin
        vues += 1
    if not morceaux:
        return texte, vues
    morceaux.append(texte[curseur:])
    return "".join(morceaux), vues


def fichiers_lecon(lecon, registre, profil) -> list[Path]:
    """Retourne les fragments dans leur ordre de lecture."""

    from lessonlib import (
        chemin_fragment,
        resoudre_dans_dossier,
        selectionner_sections,
    )

    fichiers = [
        resoudre_dans_dossier(
            lecon.dossier,
            lecon.donnees["introduction"],
            "introduction",
        )
    ]
    fichiers.extend(
        chemin_fragment(lecon, identifiant)
        for identifiant in selectionner_sections(lecon, profil, registre)
    )
    return fichiers
