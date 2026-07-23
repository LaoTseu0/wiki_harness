"""
serveur.py — le serveur MCP du homelab : trois outils, lecture seule.

Un serveur MCP est un EXPOSEUR d'outils (lecon 5.1.1) : la signature
typee + la docstring de chaque fonction decoree DEVIENNENT le schema
JSON publie par tools/list — le design d'outil de 1.1.3 s'applique tel
quel (description = prompt engineering, sorties compactes).

Les trois outils, trois sources, ZERO ecriture :
  - conteneurs_status() : etat docker, resume (pas le JSON brut) ;
  - ha_entites(filtre)  : etats HA, meme liste blanche que 3.2.1 ;
  - chercher_doc(...)   : appelle le SERVICE RAG du module 2 (2.4.1)
    — reutilisation, pas duplication : le serveur MCP est un
    ADAPTATEUR de protocole, la logique reste dans le service.

Transports (lecon 5.1.2) — le meme serveur, deux modes :
    python serveur.py            # stdio (defaut : Claude Code, 5.1.3)
    python serveur.py http       # HTTP streamable (service du homelab)
Regle d'hygiene stdio : stdout est reserve au JSON-RPC, les logs vont
sur STDERR (un print() de debug corrompt le protocole).

Prerequis : pip install "mcp[cli]" httpx ; service RAG lance (2.4.1).
"""

import os
import subprocess
import sys

import httpx

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise SystemExit('SDK MCP absent — pip install "mcp[cli]"')

RAG_URL = os.environ.get("RAG_URL", "http://192.168.1.57:8080")
HA_URL = os.environ.get("HA_URL", "http://192.168.1.57:8123")
HA_TOKEN = os.environ.get("HA_TOKEN", "")

# Meme perimetre que l'outil du module 3 (3.2.1) : le savoir-faire de
# liste blanche est PARTAGE entre les deux canaux de distribution.
ENTITES_AUTORISEES = {
    "sensor.salon_temperature",
    "sensor.bureau_temperature",
    "light.salon_plafond",
    "light.bureau_lampe",
}

mcp = FastMCP("homelab")


@mcp.tool()
def conteneurs_status() -> str:
    """Etat des conteneurs docker du homelab : nom, etat, sante.
    Lecture seule, sortie resumee (une ligne par conteneur)."""
    resultat = subprocess.run(
        ["docker", "ps", "-a", "--format",
         "{{.Names}}\t{{.State}}\t{{.Status}}"],
        capture_output=True, text=True, timeout=15,
    )
    if resultat.returncode != 0:
        # Une exception backend ne CRASHE pas le serveur : chaque outil
        # attrape et renvoie une erreur propre (piege de la lecon).
        return f"docker indisponible : {resultat.stderr.strip()[:200]}"
    return resultat.stdout.strip() or "aucun conteneur"


@mcp.tool()
def ha_entites(filtre: str = "") -> str:
    """Etats des entites Home Assistant autorisees (capteurs et lampes
    du salon/bureau). `filtre` restreint par sous-chaine du nom.
    Sortie compacte : 80 entites brutes satureraient la fenetre du host."""
    if not HA_TOKEN:
        return "HA_TOKEN absent cote serveur — outil indisponible"
    lignes = []
    for entity_id in sorted(ENTITES_AUTORISEES):
        if filtre and filtre.lower() not in entity_id.lower():
            continue
        try:
            r = httpx.get(f"{HA_URL}/api/states/{entity_id}",
                          headers={"Authorization": f"Bearer {HA_TOKEN}"},
                          timeout=10)
            if r.status_code == 200:
                lignes.append(f"{entity_id} = {r.json()['state']}")
        except httpx.HTTPError as erreur:
            lignes.append(f"{entity_id} : erreur ({erreur})")
    return "\n".join(lignes) or "aucune entite ne matche le filtre"


@mcp.tool()
def chercher_doc(question: str, k: int = 3) -> str:
    """Cherche dans la documentation du homelab (architecture, serveurs,
    decisions) et repond avec les sources. A utiliser pour toute
    question sur la configuration ou les choix passes du homelab."""
    try:
        r = httpx.post(f"{RAG_URL}/ask",
                       json={"question": question, "k": k}, timeout=120)
        r.raise_for_status()
    except httpx.HTTPError as erreur:
        return f"service RAG indisponible : {erreur}"
    d = r.json()
    sources = ", ".join(f"{s['fichier']} > {s['section']}"
                        for s in d["sources"])
    return f"{d['reponse']}\n\n(sources : {sources})"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "http":
        # Le service partage du homelab : plusieurs clients, conteneur.
        # C'est un service RESEAU : auth token + bind d'interface au
        # minimum, meme en LAN (le serveur lit HA et la doc — 5.1.2).
        mcp.run(transport="streamable-http")
    else:
        # stdio : un sous-processus par client, logs sur stderr.
        print("serveur MCP homelab : demarrage stdio", file=sys.stderr)
        mcp.run()
