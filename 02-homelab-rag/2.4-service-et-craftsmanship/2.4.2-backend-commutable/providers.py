"""
providers.py — l'abstraction provider : local <-> cloud par config.

La future brique client LLM du framework (1.3.1), la reponse minimale
a l'angle mort cloud (P.4.1), et l'argument de reversibilite des
entreprises (souverainete <-> etat de l'art). Trois regles de la
lecon 2.4.2, toutes visibles ici :

  - INTERFACE ETROITE ET TYPEE (typing.Protocol) : chat() + embed(),
    memes Message/Reponse pour tous — les particularites (prefixes de
    tache des embeddings, formats d'options) se gerent DANS le
    provider, jamais dans le code appelant ;
  - CONFIG PAR VARIABLES D'ENVIRONNEMENT, jamais de cle en dur :
        RAG_PROVIDER=ollama|openai  RAG_URL=...  RAG_API_KEY=...
        RAG_MODELE_CHAT=...         RAG_MODELE_EMBED=...
  - LE VERROU INDEX <-> EMBEDDINGS : la generation commute librement,
    les embeddings NON — changer de modele d'embeddings = changer
    d'espace vectoriel = tout re-indexer. Le provider expose donc
    l'identite de son modele d'embeddings, et l'appelant DOIT refuser
    un mismatch avec l'index au demarrage.
"""

import os
from typing import Protocol

import httpx


class Message(dict):
    """{role, content} — le format unique aux frontieres."""


class Reponse(dict):
    """{content, tokens_entree, tokens_sortie} — normalise pour tous."""


class LLMProvider(Protocol):
    """L'interface par capacite : un provider sait chatter et embedder."""

    modele_embed: str   # identite de l'espace vectoriel (le verrou)

    def chat(self, messages: list[Message], **options) -> Reponse: ...
    def embed(self, textes: list[str]) -> list[list[float]]: ...


class OllamaProvider:
    """L'existant du parcours : Ollama local, API native."""

    def __init__(self, url: str, modele_chat: str, modele_embed: str):
        self.url = url
        self.modele_chat = modele_chat
        self.modele_embed = modele_embed

    def chat(self, messages: list[Message], **options) -> Reponse:
        r = httpx.post(
            f"{self.url}/api/chat",
            json={"model": self.modele_chat, "messages": messages,
                  "stream": False, "options": options or {"num_predict": 500}},
            timeout=180,
        )
        r.raise_for_status()
        d = r.json()
        # Normalisation aux frontieres : les cles Ollama restent ICI.
        return Reponse(content=d["message"]["content"],
                       tokens_entree=d.get("prompt_eval_count", 0),
                       tokens_sortie=d.get("eval_count", 0))

    def embed(self, textes: list[str]) -> list[list[float]]:
        r = httpx.post(f"{self.url}/api/embed",
                       json={"model": self.modele_embed, "input": textes},
                       timeout=60)
        r.raise_for_status()
        return r.json()["embeddings"]


class OpenAICompatProvider:
    """Couvre vLLM (module 4), OpenRouter et la plupart des clouds —
    l'API OpenAI-compatible est le standard de fait (roadmap couche 4)."""

    def __init__(self, url: str, cle: str, modele_chat: str,
                 modele_embed: str):
        self.url = url.rstrip("/")
        self.entetes = {"Authorization": f"Bearer {cle}"} if cle else {}
        self.modele_chat = modele_chat
        self.modele_embed = modele_embed

    def chat(self, messages: list[Message], **options) -> Reponse:
        r = httpx.post(
            f"{self.url}/v1/chat/completions", headers=self.entetes,
            json={"model": self.modele_chat, "messages": messages,
                  "max_tokens": options.get("num_predict", 500),
                  "temperature": options.get("temperature", 0.7)},
            timeout=180,
        )
        r.raise_for_status()
        d = r.json()
        return Reponse(content=d["choices"][0]["message"]["content"],
                       tokens_entree=d["usage"]["prompt_tokens"],
                       tokens_sortie=d["usage"]["completion_tokens"])

    def embed(self, textes: list[str]) -> list[list[float]]:
        r = httpx.post(f"{self.url}/v1/embeddings", headers=self.entetes,
                       json={"model": self.modele_embed, "input": textes},
                       timeout=60)
        r.raise_for_status()
        return [e["embedding"] for e in r.json()["data"]]


def provider_depuis_config() -> LLMProvider:
    """La bascule : un changement de variable d'environnement, zero
    changement de code. C'est le critere de la lecon."""
    nom = os.environ.get("RAG_PROVIDER", "ollama")
    if nom == "ollama":
        return OllamaProvider(
            url=os.environ.get("RAG_URL", "http://192.168.1.57:11434"),
            modele_chat=os.environ.get("RAG_MODELE_CHAT",
                                       "qwen3:4b-instruct-2507-q4_K_M"),
            modele_embed=os.environ.get("RAG_MODELE_EMBED",
                                        "nomic-embed-text"),
        )
    if nom == "openai":
        return OpenAICompatProvider(
            url=os.environ["RAG_URL"],
            cle=os.environ.get("RAG_API_KEY", ""),
            modele_chat=os.environ["RAG_MODELE_CHAT"],
            modele_embed=os.environ.get("RAG_MODELE_EMBED", ""),
        )
    raise SystemExit(f"RAG_PROVIDER inconnu : {nom} (ollama|openai)")


def verifier_verrou_index(provider: LLMProvider, modele_index: str) -> None:
    """Le verrou de la lecon : l'index memorise le modele qui l'a
    produit ; un mismatch = scores effondres et debug long — on refuse
    AU DEMARRAGE, pas apres trois heures de confusion."""
    if provider.modele_embed != modele_index:
        raise SystemExit(
            f"Verrou index <-> embeddings : l'index a ete construit avec "
            f"'{modele_index}', le provider embedde avec "
            f"'{provider.modele_embed}'. Re-indexer ou changer de config."
        )


if __name__ == "__main__":
    provider = provider_depuis_config()
    print(f"provider : {type(provider).__name__} "
          f"(embeddings : {provider.modele_embed})")
    verifier_verrou_index(provider, "nomic-embed-text")
    reponse = provider.chat([{"role": "user",
                              "content": "Reponds en un mot : ping ?"}])
    print(f"chat : {reponse['content'][:60]} "
          f"({reponse['tokens_entree']}+{reponse['tokens_sortie']} tokens)")
    vecteurs = provider.embed(["test d'embedding"])
    print(f"embed : {len(vecteurs[0])} dimensions")
