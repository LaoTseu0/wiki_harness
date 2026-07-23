"""Regenere les schemas .canvas : vue locale par lecon + processus complet.

Principe : UNE definition du processus (cours/_processus/*.md), N rendus.
Chaque lecon declare quel processus elle traverse et quelle(s) etape(s)
elle ouvre. Le generateur produit deux familles de canvas, tous ranges
dans cours/_schemas/canvas/ :

  - un canvas PAR PROCESSUS  : la chaine entiere, carte de reference ;
  - un canvas PAR LECON      : trois boites — l'etape precedente, celle
                               de la lecon (allumee), l'etape suivante.
                               Les boites voisines sont des liens : un
                               clic ouvre le canvas de la lecon voisine.

    python outils/canvas.py
    python outils/canvas.py --verifier   # sortie != 0 si un canvas est perime

Dans une lecon :

    ## Ou ca s'emboite

    - **Processus** : [d'un texte a un token](../_processus/generation-token.md)
    - **L'etape ouverte** : `tokenizer` — entre un texte, sortent des entiers

Plusieurs etapes contigues possibles, separees par " · ".
"""

import argparse
import json
import re
import sys
import unicodedata

from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
COURS = RACINE / "cours"
PROCESSUS = COURS / "_processus"
SORTIE = COURS / "_schemas" / "canvas"

LARGEUR, HAUTEUR, PAS = 260, 110, 340
DETAIL_Y, PROC_Y = 200, -190
ALLUME, VOISIN, DETAIL, PROC = "4", "6", "3", "2"  # vert, violet, jaune, cyan

TITRE = re.compile(r"^##\s+O[ùu] [çc]a s'embo[îi]te\s*$", re.M)
SECTION = re.compile(r"^##\s", re.M)
PUCE = re.compile(r"^-\s+\*\*(.+?)\*\*\s*:\s*(.+)$")
LIEN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
ETAPE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", re.M)
FIL = re.compile(r"^-\s+`([^`]+)`\s*(?:→|->)\s*`([^`]+)`\s*:\s*(.+)$", re.M)
CODE = re.compile(r"`([^`]+)`")


def sans_accents(texte: str) -> str:
    plat = unicodedata.normalize("NFD", texte)
    return "".join(c for c in plat if unicodedata.category(c) != "Mn").lower()


def bloc(texte: str, titre: re.Pattern) -> str | None:
    debut = titre.search(texte)
    if not debut:
        return None
    suite = texte[debut.end():]
    fin = SECTION.search(suite)
    return suite[: fin.start()] if fin else suite


def puces(corps: str) -> dict[str, str]:
    trouvees = {}
    for ligne in corps.split("\n"):
        m = PUCE.match(ligne.strip())
        if m:
            trouvees[sans_accents(m.group(1))] = m.group(2).strip()
    return trouvees


def charger_processus(fichier: Path) -> dict:
    texte = fichier.read_text(encoding="utf-8")
    etapes = [(i, lib.strip(), role.strip()) for i, lib, role in ETAPE.findall(texte)]
    if not etapes:
        raise ValueError(f"{fichier.name} : aucune etape dans le tableau")
    connus = {i for i, _, _ in etapes}
    fil = FIL.findall(texte)
    for de, vers, _ in fil:
        for bout in (de, vers):
            if bout not in connus:
                raise ValueError(f"{fichier.name} : etape inconnue dans le fil : {bout}")
    return {
        "etapes": etapes,
        "libelle": {i: lib for i, lib, _ in etapes},
        "role": {i: role for i, _, role in etapes},
        "avant": {vers: de for de, vers, _ in fil},   # predecesseur (suit le fil, boucle comprise)
        "apres": {de: vers for de, vers, _ in fil},   # successeur
        "label": {(de, vers): lab for de, vers, lab in fil},
    }


def cible_canvas(lecon: Path) -> str:
    """Chemin vault du canvas d'une lecon (range dans _schemas/canvas)."""
    return (SORTIE / f"{lecon.stem}.canvas").relative_to(RACINE).as_posix()


def rendu(canvas: dict) -> str:
    return json.dumps(canvas, ensure_ascii=False, indent="\t") + "\n"


def boite(ident, x, y, texte=None, fichier=None, couleur=None, h=HAUTEUR) -> dict:
    n = {"id": ident, "x": x, "y": y, "width": LARGEUR, "height": h}
    if fichier:
        n["type"], n["file"] = "file", fichier
    else:
        n["type"], n["text"] = "text", texte
    if couleur:
        n["color"] = couleur
    return n


def fleche(ident, de, vers, label=None, cote=("right", "left")) -> dict:
    a = {"id": ident, "fromNode": de, "fromSide": cote[0],
         "toNode": vers, "toSide": cote[1]}
    if label:
        a["label"] = label
    return a


def dessiner_processus(proc: dict) -> dict:
    """La chaine entiere, carte de reference — rien d'allume."""
    etapes = proc["etapes"]
    pos = {i: n for n, (i, _, _) in enumerate(etapes)}
    noeuds = [boite(i, n * PAS, 0, texte=f"**{proc['libelle'][i]}**\n\n{proc['role'][i]}")
              for n, (i, _, _) in enumerate(etapes)]
    aretes = []
    for k, ((de, vers), lab) in enumerate(proc["label"].items()):
        retour = pos[vers] < pos[de]
        cote = ("bottom", "bottom") if retour else ("right", "left")
        aretes.append(fleche(f"fil{k}", de, vers, lab, cote))
    return {"nodes": noeuds, "edges": aretes}


def dessiner_lecon(proc: dict, allumees: list[str], detail: str,
                   proc_canvas: str, voisin_canvas) -> dict:
    """Trois boites : precedente, celle(s) de la lecon, suivante.

    voisin_canvas : fonction step_id -> chemin canvas du voisin, ou None.
    """
    premiere, derniere = allumees[0], allumees[-1]
    avant = proc["avant"].get(premiere)
    apres = proc["apres"].get(derniere)

    # sequence de gauche a droite : [avant] + allumees + [apres]
    sequence = ([avant] if avant else []) + allumees + ([apres] if apres else [])
    x = {ident: i * PAS for i, ident in enumerate(sequence)}

    noeuds, aretes = [], []
    for ident in sequence:
        est_allumee = ident in allumees
        cible = None if est_allumee else voisin_canvas(ident)
        if cible:
            noeuds.append(boite(ident, x[ident], 0, fichier=cible, couleur=VOISIN))
        else:
            txt = f"**{proc['libelle'][ident]}**\n\n{proc['role'][ident]}"
            noeuds.append(boite(ident, x[ident], 0, texte=txt,
                                couleur=ALLUME if est_allumee else None))

    for a, b in zip(sequence, sequence[1:]):
        aretes.append(fleche(f"e-{a}-{b}", a, b, proc["label"].get((a, b))))

    if detail:
        noeuds.append(boite("detail", x[premiere], DETAIL_Y, texte=detail,
                            couleur=DETAIL))
        aretes.append(fleche("e-detail", "detail", premiere, "la leçon ouvre ici",
                             cote=("top", "bottom")))

    noeuds.append(boite("proc", x[premiere], PROC_Y, fichier=proc_canvas,
                        couleur=PROC, h=60))
    aretes.append(fleche("e-proc", "proc", premiere, "processus complet",
                         cote=("bottom", "top")))
    return {"nodes": noeuds, "edges": aretes}


def lecons():
    for f in sorted(COURS.rglob("*.md")):
        if any(p.startswith("_") for p in f.relative_to(COURS).parts):
            continue
        yield f


def collecter(caches: dict) -> tuple[list, dict]:
    """Renvoie (declarations, proprietaire[(proc_path, step)] -> canvas)."""
    declarations, proprietaire = [], {}
    for lecon in lecons():
        corps = bloc(lecon.read_text(encoding="utf-8"), TITRE)
        if corps is None:
            continue
        champs = puces(corps)
        lien = LIEN.search(champs.get("processus", ""))
        if not lien:
            print(f"  ! {lecon.relative_to(RACINE)} : pas de lien de processus")
            continue
        proc_path = (lecon.parent / lien.group(2)).resolve()
        if proc_path not in caches:
            print(f"  ! {lecon.relative_to(RACINE)} : processus inconnu ({lien.group(2)})")
            continue
        avant_tiret = champs.get("l'etape ouverte", "").split("—", 1)
        allumees = CODE.findall(avant_tiret[0])
        connus = {i for i, _, _ in caches[proc_path]["etapes"]}
        hors = [e for e in allumees if e not in connus]
        if hors:
            print(f"  ! {lecon.relative_to(RACINE)} : etape(s) hors processus {hors}")
            continue
        detail = avant_tiret[1].strip() if len(avant_tiret) > 1 else ""
        declarations.append((lecon, proc_path, allumees, detail))
        for step in allumees:
            proprietaire[(proc_path, step)] = cible_canvas(lecon)
    return declarations, proprietaire


def principal(verifier: bool) -> int:
    SORTIE.mkdir(parents=True, exist_ok=True)
    perimes, ecrits, sans = [], 0, 0

    caches = {p: charger_processus(p) for p in sorted(PROCESSUS.glob("*.md"))}
    canvas_proc = {p: (SORTIE / f"{p.stem}.canvas").relative_to(RACINE).as_posix()
                   for p in caches}

    def ecrire(cible: Path, canvas: dict) -> None:
        nonlocal ecrits
        contenu = rendu(canvas)
        if verifier:
            if not cible.exists() or cible.read_text(encoding="utf-8") != contenu:
                perimes.append(cible)
        else:
            cible.write_text(contenu, encoding="utf-8")
            ecrits += 1

    for p, cache in caches.items():
        ecrire(SORTIE / f"{p.stem}.canvas", dessiner_processus(cache))

    declarations, proprietaire = collecter(caches)
    sans = sum(1 for _ in lecons()) - len(declarations)

    for lecon, proc_path, allumees, detail in declarations:
        def voisin(step, _pp=proc_path):
            return proprietaire.get((_pp, step))
        canvas = dessiner_lecon(caches[proc_path], allumees, detail,
                                canvas_proc[proc_path], voisin)
        ecrire(SORTIE / f"{lecon.stem}.canvas", canvas)

    if verifier:
        for c in perimes:
            print(f"  ! perime ou absent : {c.relative_to(RACINE)}")
        print(f"{len(perimes)} canvas a regenerer")
        return 1 if perimes else 0

    print(f"{ecrits} canvas ecrits, {sans} lecons sans schema")
    return 0


if __name__ == "__main__":
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--verifier", action="store_true")
    sys.exit(principal(parseur.parse_args().verifier))
