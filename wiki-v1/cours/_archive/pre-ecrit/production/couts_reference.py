"""
couts_reference.py — "le local est gratuit" passe a la caisse.

La lecon 6.1.3 : chaque appel local est valorise au tarif qu'il aurait
coute chez un provider cloud (le COUT EQUIVALENT API), et le cout REEL
local (electricite + amortissement) se calcule en face. Ce script est
la calculette de decision — les memes formules que Langfuse appliquera
en continu via sa table de prix par modele.

Deux disciplines de la relecture critique, appliquees :
  - le prix de reference se choisit par CLASSE de taille/qualite, pas
    par prestige — et on declare une FOURCHETTE (mini/standard) pour
    que la conclusion montre sa sensibilite au choix ;
  - la comparaison honnete cite ses limites DES DEUX COTES (egress et
    rate limits cote cloud ; indisponibilite et maintenance cote local).

Usage : renseigner la conso mesuree (les comptes de tokens sont dans
les traces, 6.1.2 — jamais a l'estime) puis lire les trois chiffres.
"""

# --- La consommation mesuree (a relire depuis Langfuse) ---------------

TOKENS_ENTREE_PAR_MOIS = 15_000_000    # A MESURER (dashboard 6.1.2)
TOKENS_SORTIE_PAR_MOIS = 2_000_000     # A MESURER

# --- La fourchette de prix de reference (EUR / million de tokens) -----
# Classe comparable a Qwen3 4B : les offres "mini/small" du marche.
# Deux bornes DOCUMENTEES plutot qu'un chiffre flatteur.

FOURCHETTE_PRIX = {
    #                (entree, sortie) EUR / Mtoken — A VERIFIER a date :
    "borne basse (mini)": (0.10, 0.40),
    "borne haute (standard)": (0.80, 3.20),
}

# --- Le cout reel local -----------------------------------------------

PUISSANCE_GPU_KW = 0.16          # RTX 2060 : ~160 W a pleine charge
HEURES_INFERENCE_PAR_MOIS = 60   # A MESURER (heures GPU actives)
PRIX_KWH_EUR = 0.25
AMORTISSEMENT_MATERIEL_EUR_MOIS = 15   # ex. ~550 EUR de matos / 36 mois


def cout_equivalent_api() -> dict[str, float]:
    couts = {}
    for nom, (prix_entree, prix_sortie) in FOURCHETTE_PRIX.items():
        couts[nom] = (TOKENS_ENTREE_PAR_MOIS / 1e6 * prix_entree
                      + TOKENS_SORTIE_PAR_MOIS / 1e6 * prix_sortie)
    return couts


def cout_reel_local() -> dict[str, float]:
    electricite = PUISSANCE_GPU_KW * HEURES_INFERENCE_PAR_MOIS * PRIX_KWH_EUR
    return {
        "electricite": electricite,
        "amortissement": AMORTISSEMENT_MATERIEL_EUR_MOIS,
        "total": electricite + AMORTISSEMENT_MATERIEL_EUR_MOIS,
    }


if __name__ == "__main__":
    volume = (TOKENS_ENTREE_PAR_MOIS + TOKENS_SORTIE_PAR_MOIS) / 1e6
    print(f"volume mensuel mesure : {volume:.1f} M tokens\n")

    print("cout equivalent API (la fourchette montre la sensibilite au")
    print("choix du prix de reference — jamais un chiffre unique) :")
    for nom, cout in cout_equivalent_api().items():
        print(f"   {nom:<24} {cout:>8.2f} EUR/mois")

    local = cout_reel_local()
    print(f"\ncout reel local :")
    print(f"   {'electricite':<24} {local['electricite']:>8.2f} EUR/mois")
    print(f"   {'amortissement':<24} {local['amortissement']:>8.2f} EUR/mois")
    print(f"   {'total':<24} {local['total']:>8.2f} EUR/mois")

    print("\nLecture (lecon 6.1.3) : le point de bascule est une FONCTION")
    print("du volume, pas une opinion — et la comparaison honnete cite")
    print("ses limites des deux cotes (egress/rate limits vs indispo/")
    print("maintenance). Les trois chiffres + une conclusion : au README.")
    print("\nDans Langfuse : declarer ces prix dans la table par modele —")
    print("chaque trace portera son cout, les dashboards agregeront.")
