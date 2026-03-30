"""Tokenisation : ce que le modele compte vraiment.

Un LLM ne voit pas des caracteres, il voit des TOKENS : des morceaux de
texte issus d'un vocabulaire fige a l'entrainement (~150 000 entrees ici).
"bonjour" peut tenir en 1 token, "anticonstitutionnellement" en 7, un
emoji en 3. Tout ce qui se facture, se plafonne et se tronque dans les
scripts precedents (num_predict, contexte, cout) se compte en tokens.

Ollama n'expose pas d'endpoint de tokenisation. Mais chaque reponse
contient prompt_eval_count : le nombre de tokens qu'il a lus en entree.
C'est notre instrument de mesure — indirect, mais reel.

Piege du protocole : prompt_eval_count compte AUSSI les tokens du
template de chat (les balises que le serveur ajoute autour de ton
message — voir 10_template.py). D'ou la mesure a blanc : on envoie un
message vide, on note le cout du template, et on le soustrait ensuite.

A TOI : ecrire compter_tokens() et remplir le tableau de mesures.
"""

import httpx

OLLAMA_URL = "http://192.168.1.57:11434"
MODEL = "qwen3:4b-instruct-2507-q4_K_M"

# Les textes du banc d'essai. Chaque paire teste UNE hypothese :
#   fr/en          : le francais coute-t-il plus cher que l'anglais ?
#   accents        : les accents coutent-ils des tokens en plus ?
#   yaml/prose     : le texte structure est-il plus dense ou moins ?
#   rare           : un mot long et rare se decoupe-t-il en morceaux ?
BANC = {
    "anglais": "The backup of the NAS runs every night at 3 am.",
    "francais": "La sauvegarde du NAS tourne chaque nuit a 3 heures.",
    "francais accentue": "La sauvegarde du NAS démarre à trois heures précises.",
    "francais sans accents": "La sauvegarde du NAS demarre a trois heures precises.",
    "yaml": "services:\n  qdrant:\n    image: qdrant/qdrant\n    ports:\n      - 6333:6333",
    "prose equivalente": "Le service qdrant utilise l'image qdrant/qdrant et publie le port 6333.",
    "mot rare": "anticonstitutionnellement",
    "emoji": "Sauvegarde terminee ✅ 🎉",
}


def compter_tokens(texte: str) -> int:
    """Nombre de tokens lus par le modele pour ce texte (template inclus).

    Envoyer un /api/chat avec `texte` comme unique message user, en
    demandant le minimum de generation (num_predict=1 : on ne veut pas
    la reponse, seulement le compteur d'entree), puis renvoyer le champ
    prompt_eval_count de la reponse JSON.

    Rappel : httpx.post(url, json={...}, timeout=...).json()
    """
    ...  # A COMPLETER


def mesurer() -> None:
    """Affiche le tableau tokens/caracteres du banc d'essai."""
    # La mesure a blanc : ce que coute le template, sans aucun contenu.
    surcout = compter_tokens("")
    print(f"Surcout du template de chat : {surcout} tokens\n")

    print(f"{'texte':<24} {'car.':>5} {'tokens':>7} {'car/token':>10}")
    print("-" * 50)
    for nom, texte in BANC.items():
        # A COMPLETER : tokens reels = mesure - surcout ; ratio =
        # nombre de caracteres / tokens reels (protege la division par 0)
        ...


if __name__ == "__main__":
    mesurer()
