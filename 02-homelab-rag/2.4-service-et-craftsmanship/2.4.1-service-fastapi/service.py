"""
service.py — le RAG cesse d'etre un script : POST /ask -> reponse + sources.

Le pattern micro-service IA des offres (lecon 2.4.1), avec ses trois
disciplines visibles dans ce fichier :

  - CONTRAT PYDANTIC DES DEUX COTES (1.1.5 applique au web) : FastAPI
    valide l'entree, serialise la sortie, genere /docs — gratuitement ;
  - ROUTE MINCE : la route valide, appelle la bibliotheque, serialise.
    Toute la logique reste dans rag_commun & les scripts promus —
    c'est ELLE qu'on teste (2.4.3) et qu'on promeut en brique ;
  - OPERATIONNEL MINIMAL : GET /health (les conteneurs du homelab en
    vivent), erreurs HTTP propres (422 validation par FastAPI, 503
    backend indisponible), metriques par reponse (pour Langfuse, 6.1).

Lancer : uvicorn service:app --host 0.0.0.0 --port 8080
Tester : curl -X POST localhost:8080/ask -H "Content-Type: application/json"
              -d '{"question": "backup du NAS ?"}'
Prerequis : pip install fastapi uvicorn ; index.db construit ; trous
des scripts 05/06 remplis.
"""

import sys
import time
from pathlib import Path
from importlib import import_module

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODULE = Path(__file__).resolve().parents[2]
V1 = MODULE / "2.1-v0.0.1-rag-a-la-main"
sys.path.insert(0, str(MODULE))
sys.path.insert(0, str(V1 / "2.1.5-recherche-top-k"))
sys.path.insert(0, str(V1 / "2.1.6-rag-complet"))

_m05 = import_module("05_rechercher")
_m06 = import_module("06_rag")


# --- Le contrat d'API : Pydantic des deux cotes -----------------------

class AskRequest(BaseModel):
    question: str = Field(min_length=3)
    k: int = Field(default=5, ge=1, le=20)
    # Filtres de la 2.2.4, exposes tels quels (ex. {"dossier": "..."}).
    filtres: dict[str, str] | None = None


class Source(BaseModel):
    fichier: str
    section: str
    score: float


class Metriques(BaseModel):
    latence_ms: int
    k_utilise: int


class AskResponse(BaseModel):
    reponse: str
    sources: list[Source]
    metriques: Metriques


# --- Le service -------------------------------------------------------

app = FastAPI(title="homelab-rag", version="0.1.0")

# L'index charge UNE fois au demarrage, pas a chaque requete.
_index = None


def index():
    global _index
    if _index is None:
        _index = _m05.charger_index()
    return _index


@app.get("/health")
def health() -> dict:
    """Vivant ET capable : l'index est-il la, Ollama repond-il ?"""
    try:
        import rag_commun
        httpx.get(f"{rag_commun.OLLAMA}/api/version", timeout=5)
    except Exception:
        raise HTTPException(status_code=503, detail="backend Ollama injoignable")
    return {"status": "ok", "chunks": len(index())}


@app.post("/ask", response_model=AskResponse)
def ask(requete: AskRequest) -> AskResponse:
    """La route est MINCE : orchestre, ne travaille pas."""
    debut = time.perf_counter()
    try:
        chunks = _m05.rechercher(requete.question, index(), requete.k)
        reponse = _m06.generer(_m06.construire_prompt(requete.question, chunks))
    except httpx.HTTPError as erreur:
        raise HTTPException(status_code=503, detail=f"backend : {erreur}")

    return AskResponse(
        reponse=reponse,
        sources=[Source(fichier=f, section=t, score=round(s, 4))
                 for s, f, t, _ in chunks],
        metriques=Metriques(
            latence_ms=int((time.perf_counter() - debut) * 1000),
            k_utilise=requete.k,
        ),
    )

# Notes de la lecon, a dire en entretien meme si hors perimetre ici :
# au-dela du reseau homelab il faudrait auth, rate limiting, quotas —
# et les appels Ollama/Qdrant etant de l'I/O, la version async
# (async def + httpx.AsyncClient) sert plusieurs requetes pendant les
# attentes reseau (ce que le module 4 mesurera cote moteur).
