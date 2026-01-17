"""
ocr_dossier.py — le multimodal devient un service : dossier -> texte.

Le flux de la lecon 7.3.1, versant OCR : un dossier surveille -> VLM
local en mode OCR (7.2.1) -> fichier texte + metadonnees, pret a
indexer. Le lien fort : ces textes deviennent un CORPUS RAG (module 2)
— l'OCR est un INGESTEUR pour le retrieval, la boucle multimodal ->
RAG se ferme.

Les garde-fous de la lecon, tous appliques (donnees TRES personnelles) :
  - LOCAL STRICT : aucune image ne sort (pas d'API cloud, ligne rouge) ;
  - VALIDATION : un VLM hallucine du texte SANS signal d'erreur — ici
    DOUBLE PASSE (deux resolutions) et comparaison : toute divergence
    marque le fichier "A RELIRE" ; l'original est TOUJOURS garde ;
  - pas de flux continu : traitement sur depot de fichier, pas de
    streaming permanent.

Usage : python ocr_dossier.py <dossier_entree> <dossier_sortie>
(le versant camera HA — snapshot sur declencheur -> description vocale
— reutilise interroger() de 7.2.1 avec l'API camera de HA.)
"""

import sys
from datetime import date
from pathlib import Path

# Reutilisation de la brique 7.2.1 : meme modele, meme appel.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                       / "7.2-vision-locale" / "7.2.1-vlm-local"))
from vlm_local import PROMPTS, encoder_image, interroger

EXTENSIONS_IMAGES = {".jpg", ".jpeg", ".png"}


def similarite_grossiere(a: str, b: str) -> float:
    """Accord entre les deux passes : ratio de mots communs (grossier
    mais suffisant pour DETECTER une divergence a relire)."""
    mots_a, mots_b = set(a.lower().split()), set(b.lower().split())
    if not mots_a or not mots_b:
        return 0.0
    return len(mots_a & mots_b) / max(len(mots_a), len(mots_b))


SEUIL_ACCORD = 0.85   # en-dessous : les deux passes divergent -> relire


def ocr_double_passe(chemin: Path) -> tuple[str, bool]:
    """Deux resolutions, comparaison : le garde-fou realiste contre
    l'hallucination silencieuse (un VLM n'a pas de score de confiance
    calibre — la confiance se CONSTRUIT par recoupement)."""
    passe_nette = interroger(encoder_image(chemin, None), PROMPTS["ocr"])
    passe_reduite = interroger(encoder_image(chemin, 1024), PROMPTS["ocr"])
    accord = similarite_grossiere(passe_nette["texte"], passe_reduite["texte"])
    return passe_nette["texte"], accord >= SEUIL_ACCORD


def traiter_dossier(entree: Path, sortie: Path) -> None:
    sortie.mkdir(parents=True, exist_ok=True)
    images = [f for f in sorted(entree.iterdir())
              if f.suffix.lower() in EXTENSIONS_IMAGES]
    if not images:
        raise SystemExit(f"aucune image dans {entree}")

    for image in images:
        cible = sortie / f"{image.stem}.md"
        if cible.exists():
            continue   # idempotent : deja traite (reflexe de la 2.1.4)
        print(f"OCR : {image.name} ...")
        texte, fiable = ocr_double_passe(image)
        statut = "ocr-double-passe-ok" if fiable else "A RELIRE (divergence)"
        # Frontmatter : metadonnees pour le chunking du module 2 —
        # elles se decident a l'ingestion, pas apres coup (2.2.4).
        cible.write_text(
            f"---\n"
            f"source_originale: {image.name}\n"
            f"date_ocr: {date.today().isoformat()}\n"
            f"statut: {statut}\n"
            f"---\n\n{texte}\n",
            encoding="utf-8",
        )
        print(f"   -> {cible.name} [{statut}]")

    print("\nL'original reste en place (toujours), les .md sont prets a")
    print("indexer — c'est un nouveau dossier de corpus pour le RAG du")
    print("module 2, et la boucle multimodal -> retrieval est fermee.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage : python ocr_dossier.py <entree> <sortie>")
    traiter_dossier(Path(sys.argv[1]), Path(sys.argv[2]))
