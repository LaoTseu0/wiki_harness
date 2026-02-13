"""Regenere les schemas .canvas depuis la rubrique "Ou ca s'emboite".

La prose est la source, le canvas est le rendu. Ce script lit le bloc de
quatre lignes de chaque lecon et ecrit un JSONCanvas a cote d'elle, meme
nom de base. Aucun canvas ne s'edite a la main : il serait ecrase.

    python outils/canvas.py            # regenere tout
    python outils/canvas.py --verifier # echoue si un canvas est absent
                                       # ou perime (pour un hook git)

Format attendu dans la lecon :

    ## Ou ca s'emboite

    - **En amont** : [x](x.md) — la relation · [y](y.md) — la relation
    - **La piece** : ce que fait cet element
    - **En aval** : [z](z.md) — la relation
    - **A ne pas confondre avec** : la distinction

Les lignes "En amont"/"En aval" acceptent plusieurs voisins separes par
" · ". La clause qui suit le tiret cadratin devient l'etiquette de la
fleche. Toutes les lignes sont facultatives sauf "La piece".
"""

import argparse
import json
import re
import sys
import unicodedata

from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
COURS = RACINE / "cours"

# Geometrie : la piece au centre, les voisins de part et d'autre.
LARGEUR, HAUTEUR, INTERLIGNE = 260, 90, 130
COLONNE = 420

ROUGE, VERT, VIOLET = "1", "4", "6"

TITRE = re.compile(r"^##\s+O[ùu] [çc]a s'embo[îi]te\s*$", re.M)
SECTION = re.compile(r"^##\s", re.M)
PUCE = re.compile(r"^-\s+\*\*(.+?)\*\*\s*:\s*(.+)$")
LIEN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def sans_accents(texte: str) -> str:
    """Pour comparer des intitules de puce sans se soucier des accents."""
    plat = unicodedata.normalize("NFD", texte)
    return "".join(c for c in plat if unicodedata.category(c) != "Mn").lower()


def extraire_bloc(texte: str) -> dict[str, str] | None:
    """Renvoie {intitule_normalise: contenu} pour la rubrique, ou None."""
    debut = TITRE.search(texte)
    if not debut:
        return None
    suite = texte[debut.end():]
    fin = SECTION.search(suite)
    corps = suite[: fin.start()] if fin else suite

    puces = {}
    for ligne in corps.split("\n"):
        m = PUCE.match(ligne.strip())
        if m:
            puces[sans_accents(m.group(1))] = m.group(2).strip()
    return puces


# Une lecon peut n'avoir aucun voisin d'un cote : on l'ecrit en toutes
# lettres dans la prose, mais on ne dessine pas une boite "rien".
ABSENCE = {"rien", "aucun", "aucune", "-", "—"}


def voisins(clause: str, lecon: Path) -> list[tuple[str, str | None, str]]:
    """Decoupe une ligne amont/aval en (libelle, chemin_vault, relation)."""
    resultat = []
    for morceau in clause.split(" · "):
        morceau = morceau.strip()
        if not morceau:
            continue
        tete = morceau.split("—", 1)[0].strip()
        if sans_accents(tete) in ABSENCE:
            continue
        # la relation est ce qui suit le tiret cadratin, hors du lien
        relation = ""
        if "—" in morceau:
            avant, relation = morceau.split("—", 1)
            relation = relation.strip()
        else:
            avant = morceau
        lien = LIEN.search(avant)
        if lien:
            cible = (lecon.parent / lien.group(2)).resolve()
            chemin = cible.relative_to(RACINE).as_posix() if cible.exists() else None
            resultat.append((lien.group(1), chemin, relation))
        else:
            resultat.append((avant.strip(), None, relation))
    return resultat


def noeud(ident, x, y, texte=None, fichier=None, couleur=None) -> dict:
    n = {"id": ident, "x": x, "y": y, "width": LARGEUR, "height": HAUTEUR}
    if fichier:
        n["type"], n["file"] = "file", fichier
    else:
        n["type"], n["text"] = "text", texte
    if couleur:
        n["color"] = couleur
    return n


def colonne(items, x, prefixe, couleur) -> list[dict]:
    """Empile verticalement une liste de voisins, centree sur y=0."""
    depart = -((len(items) - 1) * INTERLIGNE) // 2
    noeuds = []
    for i, (libelle, chemin, _) in enumerate(items):
        noeuds.append(
            noeud(f"{prefixe}{i}", x, depart + i * INTERLIGNE,
                  texte=f"**{libelle}**", fichier=chemin, couleur=couleur)
        )
    return noeuds


def construire(lecon: Path, puces: dict[str, str]) -> dict | None:
    piece = puces.get("la piece")
    if not piece:
        return None

    amont = voisins(puces.get("en amont", ""), lecon)
    aval = voisins(puces.get("en aval", ""), lecon)

    centre = noeud("piece", 0, 0, texte=f"**{lecon.stem}**\n\n{piece}",
                   couleur=VERT)
    centre["height"] = 120
    noeuds = [centre]
    noeuds += colonne(amont, -COLONNE, "amont", VIOLET)
    noeuds += colonne(aval, COLONNE, "aval", VIOLET)

    aretes = []
    for i, (_, _, relation) in enumerate(amont):
        a = {"id": f"e-amont{i}", "fromNode": f"amont{i}", "fromSide": "right",
             "toNode": "piece", "toSide": "left"}
        if relation:
            a["label"] = relation
        aretes.append(a)
    for i, (_, _, relation) in enumerate(aval):
        a = {"id": f"e-aval{i}", "fromNode": "piece", "fromSide": "right",
             "toNode": f"aval{i}", "toSide": "left"}
        if relation:
            a["label"] = relation
        aretes.append(a)

    confusion = puces.get("a ne pas confondre avec")
    if confusion:
        noeuds.append(noeud("confusion", 0, 300, texte=confusion, couleur=ROUGE))
        aretes.append({
            "id": "e-confusion", "fromNode": "piece", "fromSide": "bottom",
            "toNode": "confusion", "toSide": "top", "toEnd": "none", "label": "≠",
        })

    return {"nodes": noeuds, "edges": aretes}


def lecons():
    for f in sorted(COURS.rglob("*.md")):
        if "_archive" in f.parts or f.name.startswith("_"):
            continue
        yield f


def principal(verifier: bool) -> int:
    ecrits, absents, sans_rubrique = [], [], []
    for lecon in lecons():
        texte = lecon.read_text(encoding="utf-8")
        puces = extraire_bloc(texte)
        if puces is None:
            sans_rubrique.append(lecon)
            continue
        canvas = construire(lecon, puces)
        if canvas is None:
            print(f"  ! {lecon.relative_to(RACINE)} : rubrique sans 'La piece'")
            continue

        cible = lecon.with_suffix(".canvas")
        rendu = json.dumps(canvas, ensure_ascii=False, indent="\t") + "\n"
        if verifier:
            if not cible.exists() or cible.read_text(encoding="utf-8") != rendu:
                absents.append(cible)
        else:
            cible.write_text(rendu, encoding="utf-8")
            ecrits.append(cible)

    if verifier:
        for c in absents:
            print(f"  ! perime ou absent : {c.relative_to(RACINE)}")
        print(f"{len(absents)} canvas a regenerer")
        return 1 if absents else 0

    print(f"{len(ecrits)} canvas ecrits, "
          f"{len(sans_rubrique)} lecons sans rubrique \"Ou ca s'emboite\"")
    return 0


if __name__ == "__main__":
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--verifier", action="store_true",
                         help="ne rien ecrire, sortir en erreur si perime")
    sys.exit(principal(parseur.parse_args().verifier))
