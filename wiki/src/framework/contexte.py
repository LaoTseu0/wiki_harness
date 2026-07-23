"""Contenir l'historique : le jeter, ou le resumer.

Promu depuis etapes/fondamentaux/05_contexte.py. Le modele etant
stateless, c'est l'appelant qui renvoie tout l'historique a chaque tour :
le prefixe relu grossit sans fin, et il faut le borner.

Ce que la promotion ajoute au script : la compaction ne re-resume jamais
son propre resume. Le script repartait de l'historique entier a chaque
compaction — a la deuxieme passe, le resume precedent redevenait matiere
a resumer, et s'appauvrissait. Ici le resume acquis est transporte a
part et seuls les tours nouveaux passent au modele.
"""

from __future__ import annotations

from collections.abc import Callable

Message = dict[str, str]

# Le resume vit dans le message system, pas dans un message user : teste
# a l'etape 05, un resume en role user etait ignore par le modele.
PREFIXE_MEMOIRE = (
    " Memoire de la conversation en cours (utilise ces faits pour repondre) : "
)

CONSIGNE_RESUME = (
    "Resume la conversation suivante en 5 phrases maximum, en conservant "
    "imperativement les faits concrets (prenoms, lieux, chiffres, "
    "decisions). Reponds par le resume seul.\n\n"
)


def tronquer(messages: list[Message], garder: int = 4) -> list[Message]:
    """Garde le system et les `garder` derniers tours.

    Ne modifie pas la liste recue. Le message system n'est jamais jete :
    le perdre change le comportement du modele en silence.

    La tranche porte sur `messages[1:]`, pas sur `messages` : sur une
    conversation plus courte que `garder`, un slicing naif reprendrait le
    system et le mettrait en double dans le contexte.
    """
    return [messages[0]] + messages[1:][-garder:]


def compacter(
    messages: list[Message],
    resumer: Callable[[str], str],
    system: str,
    resume: str = "",
    garder: int = 0,
) -> tuple[list[Message], str]:
    """Remplace les tours anciens par une memoire logee dans le system.

    `resumer` prend un transcript et rend son resume — un appel LLM, une
    fonction de test, peu importe : la brique ne connait pas le client.
    `system` est le prompt system de base, sans memoire ; `resume` est la
    memoire deja acquise, qui ne repasse jamais par le modele.

    Rend la nouvelle liste et la memoire mise a jour. Si rien n'est assez
    ancien pour etre resume, rend l'entree inchangee.
    """
    coupe = len(messages) - garder
    if coupe <= 1:
        return list(messages), resume

    anciens, recents = messages[1:coupe], messages[coupe:]
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in anciens)
    neuf = resumer(CONSIGNE_RESUME + transcript)

    total = f"{resume} {neuf}".strip()
    memoire = {"role": "system", "content": system + PREFIXE_MEMOIRE + total}
    return [memoire, *recents], total
