"""
service_agent.py — l'embryon d'agent persistant : la session attend.

Changement de posture (lecon 3.3.1) : de "l'humain ouvre une session"
a "la session attend des requetes". Un petit service FastAPI (le
pattern 2.4.1) possede une session d'agent et expose POST /task.

Ce que la persistance change, tout est dans ce fichier :
  - le CONTEXTE S'ACCUMULE entre requetes -> checkpoint memoire
    (3.2.2) toutes les N taches ;
  - le HUMAN-IN-THE-LOOP devient asynchrone : file d'approbation avec
    TTL — une approbation qui n'arrive pas a temps devient un refus,
    et une action approuvee tardivement se RE-VALIDE contre l'etat
    courant avant execution ;
  - la SANTE DE SESSION : recyclage sur declencheurs MESURABLES
    (plafond de tokens, n taches, erreurs d'outils), pas au feeling —
    la memoire externe rend la session jetable.

Ici la session est la boucle manuelle du module 1 (07_agent, version
sans input() — un service n'a pas de clavier). Le mode RPC/SDK de Pi
remplacerait AgentSession par une session Pi tenue ouverte : meme
service, autre moteur. Hors scope assume : file de taches,
multi-sessions, declencheurs evenementiels.

Lancer : uvicorn service_agent:app --port 8090
"""

import time
import uuid

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

OLLAMA_URL = "http://192.168.1.57:11434"
MODEL = "qwen3:4b-instruct-2507-q4_K_M"

CHECKPOINT_TOUTES_LES = 5      # taches entre deux checkpoints memoire
RECYCLAGE_TOKENS = 6000        # plafond de contexte avant recyclage
RECYCLAGE_TACHES = 50          # plafond de taches avant recyclage
TTL_APPROBATION_S = 3600       # une approbation attend 1 h, pas plus


class AgentSession:
    """La session persistante : historique + compteurs de sante."""

    def __init__(self):
        self.messages = [{
            "role": "system",
            "content": "Tu es l'agent du homelab. Reponds de facon "
            "concise, en francais.",
        }]
        self.taches = 0
        self.dernier_contexte = 0   # tokens lus au dernier appel

    def traiter(self, tache: str) -> str:
        self.messages.append({"role": "user", "content": tache})
        reponse = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": self.messages,
                  "stream": False, "options": {"num_predict": 500}},
            timeout=180,
        )
        reponse.raise_for_status()
        d = reponse.json()
        contenu = d["message"]["content"]
        self.messages.append({"role": "assistant", "content": contenu})
        self.taches += 1
        self.dernier_contexte = d.get("prompt_eval_count", 0)
        return contenu

    def doit_recycler(self) -> str | None:
        """Les declencheurs MESURABLES du recyclage (pas 'au feeling')."""
        if self.dernier_contexte > RECYCLAGE_TOKENS:
            return f"contexte {self.dernier_contexte} > {RECYCLAGE_TOKENS} tokens"
        if self.taches >= RECYCLAGE_TACHES:
            return f"{self.taches} taches traitees"
        return None


session = AgentSession()
approbations: dict[str, dict] = {}   # la file d'approbation asynchrone
app = FastAPI(title="jarvis-agent-rpc", version="0.1.0")


class TaskRequest(BaseModel):
    tache: str


@app.get("/health")
def health() -> dict:
    """La sante de session est une METRIQUE, pas un sentiment."""
    return {
        "status": "ok",
        "taches": session.taches,
        "contexte_tokens": session.dernier_contexte,
        "recyclage_requis": session.doit_recycler(),
        "approbations_en_attente": len(approbations),
    }


@app.post("/task")
def task(requete: TaskRequest) -> dict:
    # ATTENTION concurrence (piege de la lecon) : une session = un
    # fil. FastAPI + def synchrone serialise naturellement ici ; en
    # async il faudrait une file explicite, pas un espoir.
    motif = session.doit_recycler()
    if motif:
        raise HTTPException(
            status_code=503,
            detail=f"session a recycler ({motif}) : checkpoint memoire "
            f"(3.2.2) puis nouvelle session — mourir ne coute rien, la "
            f"memoire externe existe pour ca",
        )
    reponse = session.traiter(requete.tache)
    if session.taches % CHECKPOINT_TOUTES_LES == 0:
        # Ici : session_shutdown() partiel de memoire_git (3.2.2) —
        # quand la session ne "finit" jamais, on checkpointe.
        print(f"[checkpoint memoire apres {session.taches} taches]")
    return {"reponse": reponse, "tache_n": session.taches}


@app.post("/approbations/{action_id}/approuver")
def approuver(action_id: str) -> dict:
    """Le human-in-the-loop asynchrone : TTL + re-validation."""
    action = approbations.pop(action_id, None)
    if action is None:
        raise HTTPException(status_code=404, detail="action inconnue ou expiree")
    if time.time() - action["creee_a"] > TTL_APPROBATION_S:
        return {"statut": "expiree — refus renvoye au modele comme information"}
    # RE-VALIDATION contre l'etat courant : approuver a H puis executer
    # a H+6 sans re-verifier est LE piege de l'agent persistant.
    return {"statut": f"a re-valider puis executer : {action['description']}"}


def demander_approbation(description: str) -> str:
    """Cote outils : une action sensible s'enregistre ici et ATTEND —
    ni silencieusement refusee, ni pire, accordee."""
    action_id = str(uuid.uuid4())[:8]
    approbations[action_id] = {"description": description,
                               "creee_a": time.time()}
    return action_id
