"""Attention et KV cache : pourquoi le 1er token est lent et les autres rapides.

L'attention est le mecanisme par lequel chaque token regarde TOUS les
tokens precedents pour decider de quoi il depend. Pour cela, chaque
token produit trois vecteurs : une requete Q ("ce que je cherche"), une
cle K ("ce que je propose") et une valeur V ("ce que j'apporte"). Un
token pondere les V des autres selon l'accord entre son Q et leurs K.

Consequence brutale : lire un prompt de n tokens coute ~n^2 comparaisons.
C'est la vraie raison pour laquelle une grande fenetre de contexte n'est
ni gratuite ni pleinement exploitee (cf. "lost in the middle").

Le KV CACHE est l'optimisation qui rend la generation viable. Les K et V
d'un token ne dependent que de lui et de son passe : une fois calcules,
ils ne changent JAMAIS. On les garde en memoire. Generer le token n+1 ne
recalcule donc pas tout le passe — seulement le nouveau token contre le
cache. La generation se coupe en deux regimes :

  - PREFILL  : lire le prompt d'un bloc, remplir le cache — cout ~n^2,
               c'est la latence du premier token ;
  - DECODE   : produire les tokens suivants un par un contre le cache —
               cout ~n par token, bien plus rapide.

Ce cache occupe de la VRAM proportionnellement a la longueur du contexte.
C'est lui qui sature en premier sous charge (lecon charge-concurrente),
et c'est lui que PagedAttention gere par pages (lecon mecanismes-vllm).

Ollama renvoie les deux regimes separement, en nanosecondes :
  prompt_eval_count / prompt_eval_duration -> le prefill
  eval_count        / eval_duration        -> le decode

A TOI : mesurer les deux regimes, et voir lequel depend de la taille du
prompt.
"""

import httpx

OLLAMA_URL = "http://192.168.1.57:11434"
MODEL = "qwen3:4b-instruct-2507-q4_K_M"

# On fait grossir le prompt sans changer la tache demandee : seule la
# longueur varie, donc seul le prefill devrait bouger.
REMPLISSAGE = "Le NAS sauvegarde les donnees de la famille chaque nuit. "
TAILLES = [1, 20, 100, 400]

QUESTION = "En un mot : que fait le NAS ?"


def mesurer(prompt: str) -> dict:
    """Renvoie les compteurs et durees d'un appel.

    POST /api/chat, stream=False, options={"num_predict": 40} pour que
    la phase de decode dure assez longtemps pour etre mesurable.

    Extraire de la reponse : prompt_eval_count, prompt_eval_duration,
    eval_count, eval_duration. Les durees sont en NANOSECONDES
    (diviser par 1e9 pour des secondes).
    """
    ...  # A COMPLETER


def banc() -> None:
    """Compare prefill et decode quand le prompt grossit."""
    print(f"{'tokens entree':>14} {'prefill (s)':>12} {'decode (tok/s)':>15}")
    print("-" * 45)
    for n in TAILLES:
        prompt = REMPLISSAGE * n + QUESTION
        m = mesurer(prompt)
        # A COMPLETER : afficher les tokens d'entree, la duree de prefill
        # en secondes, et le debit de decode (eval_count / eval_duration).
        ...

    # A PREDIRE AVANT DE LANCER, puis a confronter :
    #   - le prefill grandit-il proportionnellement au nombre de tokens,
    #     ou plus vite ?
    #   - le debit de decode (tokens/s) bouge-t-il quand le prompt
    #     grossit ? Pourquoi ?


if __name__ == "__main__":
    banc()
