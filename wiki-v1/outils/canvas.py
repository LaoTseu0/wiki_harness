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

    python wiki/outils/canvas.py
    python wiki/outils/canvas.py --verifier   # sortie != 0 si un canvas est perime

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

# RACINE est aussi la racine du vault Obsidian (.obsidian/ y est range) :
# c'est elle qui donne les chemins ecrits dans les canvas, wiki/ compris.
RACINE = Path(__file__).resolve().parents[2]
WIKI = RACINE / "wiki"
COURS = WIKI / "cours"
PROCESSUS = COURS / "_processus"
SORTIE = COURS / "_schemas" / "canvas"

# Une taille par role : l'etape de la lecon domine, ses voisines s'effacent.
ALLUMEE = (310, 180)   # l'etape que la lecon ouvre
VOISINE = (290, 140)   # les etapes d'avant / d'apres, cliquables
ECART_X, ECART_Y = 340, 140  # blanc entre deux boites, en rangee / en colonne
ALLUME, VOISIN = "4", "6"  # vert, violet

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


def cible_lecon(lecon: Path) -> str:
    """Chemin vault de la lecon, sans extension — pour un [[lien|alias]]."""
    return lecon.relative_to(RACINE).with_suffix("").as_posix()


def rendu(canvas: dict) -> str:
    return json.dumps(canvas, ensure_ascii=False, indent="\t") + "\n"


def boite(ident, x, y, taille, texte=None, fichier=None, couleur=None) -> dict:
    largeur, hauteur = taille
    n = {"id": ident, "x": x, "y": y, "width": largeur, "height": hauteur}
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
    pas = ALLUMEE[0] + ECART_X
    noeuds = [boite(i, n * pas, 0, ALLUMEE,
                    texte=f"**{proc['libelle'][i]}**\n\n{proc['role'][i]}")
              for n, (i, _, _) in enumerate(etapes)]
    aretes = []
    for k, ((de, vers), lab) in enumerate(proc["label"].items()):
        retour = pos[vers] < pos[de]
        cote = ("bottom", "bottom") if retour else ("right", "left")
        aretes.append(fleche(f"fil{k}", de, vers, lab, cote))
    return {"nodes": noeuds, "edges": aretes}


def milieu(hauteur: int) -> int:
    """Ordonnee d'une boite centree sur la hauteur d'une etape allumee."""
    return (ALLUMEE[1] - hauteur) // 2


def placer(allumees: list[str], avant, apres, taille: dict) -> dict:
    """Position (x, y) de chaque boite.

    Au-dela de deux etapes allumees la rangee devient une colonne : la
    lecon se lit de haut en bas et reste lisible sans defiler. Les deux
    voisines restent sur les cotes, accrochees a la premiere et a la
    derniere etape.
    """
    pos = {}
    if len(allumees) > 2:
        colonne = VOISINE[0] + ECART_X if avant else 0
        for n, ident in enumerate(allumees):
            pos[ident] = (colonne, n * (ALLUMEE[1] + ECART_Y))
        if avant:
            pos[avant] = (0, milieu(taille[avant][1]))
        if apres:
            pos[apres] = (colonne + ALLUMEE[0] + ECART_X,
                          pos[allumees[-1]][1] + milieu(taille[apres][1]))
        return pos

    # rangee : abscisses cumulees, les boites n'ont pas la meme largeur
    curseur = 0
    for ident in ([avant] if avant else []) + allumees + ([apres] if apres else []):
        pos[ident] = (curseur, milieu(taille[ident][1]))
        curseur += taille[ident][0] + ECART_X
    return pos


def dessiner_lecon(proc: dict, allumees: list[str], detail: str,
                   lien_lecon: str, voisin_canvas) -> dict:
    """Trois boites : precedente, celle(s) de la lecon, suivante.

    La boite allumee se suffit a elle-meme : son titre est un lien vers la
    lecon, son corps une liste a puces (role de l'etape, puis ce que la
    lecon ouvre). Rien autour, pour ne pas encombrer la vue.

    voisin_canvas : fonction step_id -> chemin canvas du voisin, ou None.
    """
    premiere, derniere = allumees[0], allumees[-1]
    avant = proc["avant"].get(premiere)
    apres = proc["apres"].get(derniere)

    # sens de lecture : [avant] + allumees + [apres]
    sequence = ([avant] if avant else []) + allumees + ([apres] if apres else [])
    taille = {i: ALLUMEE if i in allumees else VOISINE for i in sequence}
    pos = placer(allumees, avant, apres, taille)
    colonne = len(allumees) > 2

    noeuds, aretes = [], []
    for ident in sequence:
        est_allumee = ident in allumees
        x, y = pos[ident]
        cible = None if est_allumee else voisin_canvas(ident)
        if cible:
            noeuds.append(boite(ident, x, y, taille[ident],
                                fichier=cible, couleur=VOISIN))
            continue
        if est_allumee:
            titre = f"[[{lien_lecon}|{proc['libelle'][ident]}]]"
            # le detail ne concerne que l'entree du groupe allume
            lignes = [proc["role"][ident]]
            if detail and ident == premiere:
                lignes.append(detail)
        else:
            titre, lignes = proc["libelle"][ident], [proc["role"][ident]]
        txt = f"**{titre}**\n\n" + "\n".join(f"- {p}" for p in lignes)
        noeuds.append(boite(ident, x, y, taille[ident], texte=txt,
                            couleur=ALLUME if est_allumee else None))

    for a, b in zip(sequence, sequence[1:]):
        # en colonne, seules les fleches entre allumees descendent
        empile = colonne and a in allumees and b in allumees
        cote = ("bottom", "top") if empile else ("right", "left")
        aretes.append(fleche(f"e-{a}-{b}", a, b, proc["label"].get((a, b)), cote))

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
                                cible_lecon(lecon), voisin)
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
