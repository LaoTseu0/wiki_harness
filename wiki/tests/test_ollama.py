"""Le parsing du client Ollama, sans serveur.

Le transport HTTP n'est pas teste ici — il n'y a rien a verifier dans
httpx. Ce qui merite un test, c'est ce que le repo a ecrit : la lecture
des compteurs et le decoupage du flux NDJSON.
"""

import json

import pytest

from framework.llm.ollama import ClientOllama, Reponse, morceaux_ndjson


# --- lecture d'une reponse -------------------------------------------


def test_reponse_lit_le_contenu_et_les_compteurs():
    reponse = Reponse.depuis_ollama(
        {
            "message": {"role": "assistant", "content": "bonjour"},
            "prompt_eval_count": 412,
            "eval_count": 17,
        }
    )

    assert reponse.contenu == "bonjour"
    assert reponse.tokens_lus == 412
    assert reponse.tokens_generes == 17


def test_reponse_sans_compteurs_vaut_zero():
    # Ollama ne renvoie pas toujours les deux compteurs ; un tour non
    # compte doit valoir 0, pas faire tomber l'appelant.
    reponse = Reponse.depuis_ollama({"message": {"content": "ok"}})

    assert (reponse.tokens_lus, reponse.tokens_generes) == (0, 0)


def test_reponse_sans_message_est_une_erreur():
    # Une charge utile sans message n'est pas un tour vide : c'est une
    # reponse qu'on n'a pas comprise, et il faut le savoir tout de suite.
    with pytest.raises(KeyError):
        Reponse.depuis_ollama({"error": "model not found"})


# --- decoupage du flux -----------------------------------------------


def flux(*blocs: dict) -> list[str]:
    return [json.dumps(b) for b in blocs]


def test_morceaux_recolle_la_reponse():
    lignes = flux(
        {"message": {"content": "Bon"}, "done": False},
        {"message": {"content": "jour"}, "done": False},
        {"message": {"content": ""}, "done": True, "eval_count": 2},
    )

    assert "".join(morceaux_ndjson(lignes)) == "Bonjour"


def test_morceaux_ignore_les_lignes_vides():
    lignes = flux({"message": {"content": "a"}, "done": False})
    lignes = ["", *lignes, ""]

    assert list(morceaux_ndjson(lignes)) == ["a"]


def test_morceaux_s_arrete_a_done():
    # Ce qui suit `done` n'est pas de la generation : le flux s'arrete la,
    # meme si la connexion continue de rendre des lignes.
    lignes = flux(
        {"message": {"content": "a"}, "done": True},
        {"message": {"content": "JAMAIS"}, "done": False},
    )

    assert list(morceaux_ndjson(lignes)) == ["a"]


# --- construction de la charge utile ---------------------------------


def test_charge_sans_options_n_envoie_pas_le_champ():
    # Un champ "options" vide n'est pas neutre : autant ne pas l'envoyer.
    charge = ClientOllama()._charge([{"role": "user", "content": "hi"}], False, {})

    assert "options" not in charge
    assert charge["stream"] is False


def test_charge_transporte_les_options():
    charge = ClientOllama(modele="m")._charge([], True, {"num_predict": 300})

    assert charge["model"] == "m"
    assert charge["options"] == {"num_predict": 300}


def test_url_sans_slash_final():
    assert ClientOllama(url="http://hote:11434/").url == "http://hote:11434"
