"""Client Ollama : l'appel au modele, en bloc ou en flux.

Promu depuis etapes/fondamentaux/01_hello.py, 02_chat.py et 03_stream.py.
Ce que la promotion ajoute aux scripts : les comptes de tokens ne sont
plus affiches puis perdus, ils remontent dans `Reponse` — le cout d'un
tour devient une donnee du programme, pas une trace a l'ecran.

Le parsing est separe du transport (`Reponse.depuis_ollama`,
`morceaux_ndjson`) : c'est ce qui rend la brique testable sans serveur.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass

import httpx

Message = dict[str, str]

URL_DEFAUT = "http://192.168.1.57:11434"
MODELE_DEFAUT = "qwen3:4b-instruct-2507-q4_K_M"


@dataclass(frozen=True)
class Reponse:
    """Ce que rend un tour : le texte, et ce qu'il a coute en tokens.

    `tokens_lus` compte tout le prefixe relu (system + historique), pas
    seulement le dernier message : c'est lui qui grossit a chaque tour.
    """

    contenu: str
    tokens_lus: int
    tokens_generes: int

    @classmethod
    def depuis_ollama(cls, donnees: dict) -> Reponse:
        """Lit la charge utile d'/api/chat. Absents, les compteurs valent 0."""
        return cls(
            contenu=donnees["message"]["content"],
            tokens_lus=donnees.get("prompt_eval_count", 0),
            tokens_generes=donnees.get("eval_count", 0),
        )


def morceaux_ndjson(lignes: Iterable[str]) -> Iterator[str]:
    """Decoupe un flux Ollama en morceaux de texte.

    Ollama repond au streaming par une ligne de JSON par morceau, la
    derniere portant `done: true` et les compteurs. On ignore les lignes
    vides — un flux HTTP en produit — et on s'arrete sur `done`.
    """
    for ligne in lignes:
        if not ligne:
            continue
        bloc = json.loads(ligne)
        morceau = bloc.get("message", {}).get("content", "")
        if morceau:
            yield morceau
        if bloc.get("done"):
            return


class ClientOllama:
    """Parle a un serveur Ollama. Une instance = un modele, une adresse."""

    def __init__(
        self,
        url: str = URL_DEFAUT,
        modele: str = MODELE_DEFAUT,
        timeout: float = 120,
    ) -> None:
        self.url = url.rstrip("/")
        self.modele = modele
        self.timeout = timeout

    def _charge(self, messages: list[Message], flux: bool, options: dict) -> dict:
        charge = {"model": self.modele, "messages": messages, "stream": flux}
        if options:
            charge["options"] = options
        return charge

    def chat(self, messages: list[Message], **options) -> Reponse:
        """Un tour complet : envoie tout l'historique, attend la fin.

        Le modele est stateless — c'est `messages` en entier qui fait la
        conversation, pas le serveur.
        """
        reponse = httpx.post(
            f"{self.url}/api/chat",
            json=self._charge(messages, flux=False, options=options),
            timeout=self.timeout,
        )
        reponse.raise_for_status()
        return Reponse.depuis_ollama(reponse.json())

    def stream(self, messages: list[Message], **options) -> Iterator[str]:
        """Meme tour, rendu morceau par morceau au fil de la generation.

        Rend le texte seul : les compteurs de la derniere ligne ne sont
        pas exposes ici. Un appelant qui les veut utilise `chat`.
        """
        with httpx.stream(
            "POST",
            f"{self.url}/api/chat",
            json=self._charge(messages, flux=True, options=options),
            timeout=self.timeout,
        ) as reponse:
            reponse.raise_for_status()
            yield from morceaux_ndjson(reponse.iter_lines())
