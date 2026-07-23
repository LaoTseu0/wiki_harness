"""La troncature et la compaction, sans serveur.

`compacter` recoit une fonction de resume : on lui en donne une qui
enregistre ce qu'on lui a soumis. C'est ce qui permet de verifier ce que
le modele NE voit pas — le resume deja acquis.
"""

from framework.contexte import PREFIXE_MEMOIRE, compacter, tronquer

SYSTEM = {"role": "system", "content": "Tu es un assistant concis."}


def tours(n: int) -> list[dict[str, str]]:
    """[S, u1, a1, ... un, an] — n echanges apres le system."""
    echanges = []
    for i in range(1, n + 1):
        echanges += [
            {"role": "user", "content": f"u{i}"},
            {"role": "assistant", "content": f"a{i}"},
        ]
    return [SYSTEM] + echanges


class EspionResume:
    """Une fonction de resume qui retient ce qu'on lui a passe."""

    def __init__(self, rendu: str = "RESUME") -> None:
        self.rendu = rendu
        self.recus: list[str] = []

    def __call__(self, consigne: str) -> str:
        self.recus.append(consigne)
        return self.rendu


# --- troncature ------------------------------------------------------


def test_tronquer_garde_le_system_et_les_derniers():
    # Le cas de validation ecrit dans la docstring de l'etape 05.
    assert tronquer(tours(3), garder=4) == [
        SYSTEM,
        {"role": "user", "content": "u2"},
        {"role": "assistant", "content": "a2"},
        {"role": "user", "content": "u3"},
        {"role": "assistant", "content": "a3"},
    ]


def test_tronquer_ne_modifie_pas_l_entree():
    entree = tours(3)
    copie = [dict(m) for m in entree]
    tronquer(entree, garder=2)
    assert entree == copie


def test_tronquer_ne_duplique_pas_le_system_sur_conversation_courte():
    # Le defaut du slicing naif de l'etape : messages[-garder:] reprend
    # le system quand la conversation est plus courte que le seuil, et
    # le contexte le paye deux fois.
    assert tronquer(tours(1), garder=10) == tours(1)


# --- compaction ------------------------------------------------------


def test_compacter_loge_le_resume_dans_le_system():
    messages, resume = compacter(tours(3), EspionResume(), SYSTEM["content"])

    assert resume == "RESUME"
    assert len(messages) == 1
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM["content"] + PREFIXE_MEMOIRE + "RESUME"


def test_compacter_soumet_les_tours_mais_pas_le_system():
    espion = EspionResume()
    compacter(tours(2), espion, SYSTEM["content"])

    (soumis,) = espion.recus
    assert "u1" in soumis and "a2" in soumis
    assert SYSTEM["content"] not in soumis


def test_compacter_ne_re_resume_jamais_le_resume_acquis():
    # Le defaut du script de l'etape : a la deuxieme passe, il redonnait
    # tout au modele, resume precedent compris, qui s'appauvrissait.
    espion = EspionResume(rendu="NEUF")
    _, resume = compacter(
        tours(2), espion, SYSTEM["content"], resume="ACQUIS"
    )

    (soumis,) = espion.recus
    assert "ACQUIS" not in soumis
    assert resume == "ACQUIS NEUF"


def test_compacter_garde_les_tours_recents_verbatim():
    messages, _ = compacter(tours(3), EspionResume(), SYSTEM["content"], garder=2)

    assert [m["content"] for m in messages[1:]] == ["u3", "a3"]


def test_compacter_ne_touche_a_rien_si_rien_n_est_assez_ancien():
    espion = EspionResume()
    entree = tours(1)
    messages, resume = compacter(entree, espion, SYSTEM["content"], garder=2)

    assert messages == entree
    assert resume == ""
    assert espion.recus == []
