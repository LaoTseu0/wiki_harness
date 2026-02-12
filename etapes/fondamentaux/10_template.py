"""Le template de chat : le texte que le modele voit reellement.

Depuis le script 02, on envoie une LISTE de messages avec des roles
(system/user/assistant/tool). Le modele, lui, ne connait pas les listes
ni les roles : il ne sait que continuer UNE chaine de caracteres.

Entre les deux, le serveur applique le TEMPLATE DE CHAT du modele : un
gabarit, livre avec le modele, qui aplatit la liste en un seul texte
balise. Pour Qwen, c'est le format ChatML :

    <|im_start|>system
    Tu es un assistant concis.<|im_end|>
    <|im_start|>user
    Bonjour<|im_end|>
    <|im_start|>assistant

La derniere ligne, ouverte et sans contenu, est ce qui "donne la parole"
au modele : il complete, et s'arrete en produisant <|im_end|>.

Pourquoi ca compte : le template explique le cout fixe mesure au 09, le
fait qu'un role system ait plus d'autorite (il est physiquement en tete
du texte), et pourquoi un modele fine-tune avec un autre format devient
incoherent (piege classique, voir la lecon LoRA).

A TOI : recuperer le template, puis prouver que tu sais le reproduire.
"""

import httpx

OLLAMA_URL = "http://192.168.1.57:11434"
MODEL = "qwen3:4b-instruct-2507-q4_K_M"

MESSAGES = [
    {"role": "system", "content": "Tu es un assistant concis."},
    {"role": "user", "content": "Bonjour"},
]


def montrer_template() -> str:
    """Affiche et renvoie le gabarit brut livre avec le modele.

    POST /api/show avec {"model": MODEL} : la reponse contient une cle
    "template" (le gabarit, en syntaxe Go) et une cle "parameters"
    (les defauts du Modelfile — ceux qui t'avaient piege au 04).
    """
    ...  # A COMPLETER


def rendre_a_la_main(messages: list[dict]) -> str:
    """Reconstruit le texte ChatML a partir de la liste de messages.

    Pour chaque message : "<|im_start|>{role}\\n{content}<|im_end|>\\n"
    Puis on ouvre le tour de l'assistant : "<|im_start|>assistant\\n"
    """
    ...  # A COMPLETER


def verifier(messages: list[dict]) -> None:
    """Prouve que la reconstruction est exacte, en comptant les tokens.

    Deux chemins doivent aboutir au MEME texte, donc au meme nombre de
    tokens en entree :

      A. /api/chat avec la liste de messages (le serveur applique le
         template lui-meme) ;
      B. /api/generate avec {"raw": True, "prompt": rendre_a_la_main(...)}
         — "raw" dit a Ollama de n'appliquer AUCUN template et d'envoyer
         la chaine telle quelle.

    Dans les deux cas, num_predict=1 et on lit prompt_eval_count.
    Si les deux comptes sont egaux, ta reconstruction est la bonne.
    """
    ...  # A COMPLETER


if __name__ == "__main__":
    montrer_template()
    print(rendre_a_la_main(MESSAGES))
    verifier(MESSAGES)
