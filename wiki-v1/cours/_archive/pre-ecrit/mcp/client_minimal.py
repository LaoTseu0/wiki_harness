"""
client_minimal.py — les deux cotes du protocole : le client, sans SDK.

~90 lignes de Python pur : lancer un serveur MCP en sous-processus,
derouler le handshake, lister les outils, en appeler un. C'est
l'exercice de l'entree glossaire 1.2.5 (le savoir y est) — apres ca,
plus rien dans MCP n'est une boite noire.

La sequence, a connaitre par coeur (JSON-RPC 2.0, une ligne par
message sur stdio) :
  1. -> initialize            (version, capacites, identite)
  2. <- result                (les capacites du serveur)
  3. -> notifications/initialized   (SANS id : une notification —
     l'oublier est le piege classique : certains serveurs refusent
     ensuite les appels, le handshake a TROIS temps, pas deux)
  4. -> tools/list  <- result (name, description, inputSchema)
  5. -> tools/call  <- result.content

Ce que ce client revele du host (Claude Code) : il ne fait QUE ca en
plus — boucler sur plusieurs serveurs, traduire les inputSchemas au
format d'outils du modele (1.1.3), router les tool_calls. Le pont
modele <-> MCP est du code ordinaire.

Test d'interoperabilite : marcher sur NOTRE serveur (5.1.1) ET sur un
serveur tiers — c'est le protocole qu'on valide, pas notre paire.
"""

import json
import subprocess
import sys
import threading
from pathlib import Path

# Le serveur a lancer : le notre par defaut, n'importe lequel en argv.
SERVEUR = sys.argv[1:] or [
    sys.executable,
    str(Path(__file__).resolve().parents[2] / "5.1-serveur"
        / "5.1.1-serveur-mcp-python" / "serveur.py"),
]

compteur_id = 0


def requete(methode: str, params: dict | None = None) -> dict:
    """Une requete JSON-RPC : id incremental (notre client est
    sequentiel — un compteur suffit, mais la correspondance des ids
    est ce qui rend JSON-RPC asynchrone par nature : a dire)."""
    global compteur_id
    compteur_id += 1
    message = {"jsonrpc": "2.0", "id": compteur_id, "method": methode}
    if params is not None:
        message["params"] = params
    return message


def notification(methode: str) -> dict:
    """Une notification = PAS de champ id : aucune reponse attendue."""
    return {"jsonrpc": "2.0", "method": methode}


def envoyer(processus, message: dict) -> None:
    # Un JSON par ligne + FLUSH : sans flush ligne a ligne, les deux
    # processus s'attendent mutuellement (deadlock silencieux, 1.2.5).
    processus.stdin.write(json.dumps(message) + "\n")
    processus.stdin.flush()


def lire_reponse(processus, id_attendu: int) -> dict:
    """readline() et un JSON par ligne : lire par blocs couperait un
    message en deux. On saute les notifications du serveur."""
    while True:
        ligne = processus.stdout.readline()
        if not ligne:
            raise SystemExit("le serveur a ferme stdout (voir ses logs stderr)")
        message = json.loads(ligne)
        if message.get("id") == id_attendu:
            if "error" in message:
                raise SystemExit(f"erreur serveur : {message['error']}")
            return message["result"]


def drainer_stderr(processus) -> None:
    """Le serveur logge sur stderr : jamais lu -> pipe plein -> blocage.
    Un thread le vide en continu (et l'affiche, prefixe)."""
    for ligne in processus.stderr:
        print(f"   [serveur] {ligne.rstrip()}", file=sys.stderr)


if __name__ == "__main__":
    processus = subprocess.Popen(
        SERVEUR, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8",
    )
    threading.Thread(target=drainer_stderr, args=(processus,),
                     daemon=True).start()

    # 1-2-3 : le handshake, trois temps.
    envoyer(processus, requete("initialize", {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "client-minimal", "version": "0.0.1"},
    }))
    capacites = lire_reponse(processus, compteur_id)
    print(f"serveur : {capacites['serverInfo']['name']} "
          f"(protocole {capacites['protocolVersion']})")
    envoyer(processus, notification("notifications/initialized"))

    # 4 : la decouverte — exactement le format du function calling.
    envoyer(processus, requete("tools/list"))
    outils = lire_reponse(processus, compteur_id)["tools"]
    print(f"\n{len(outils)} outil(s) decouvert(s) :")
    for outil in outils:
        parametres = list(outil.get("inputSchema", {}).get("properties", {}))
        print(f"  - {outil['name']}({', '.join(parametres)}) : "
              f"{outil['description'][:60]}")

    # 5 : un appel reel — chercher_doc avec une vraie question.
    envoyer(processus, requete("tools/call", {
        "name": "chercher_doc",
        "arguments": {"question": "Qu'est-ce qu'on avait decide pour "
                                  "le backup du NAS ?"},
    }))
    resultat = lire_reponse(processus, compteur_id)
    print("\ntools/call chercher_doc :")
    for bloc in resultat["content"]:
        if bloc["type"] == "text":
            print(bloc["text"][:400])
    if resultat.get("isError"):
        print("(isError : l'outil a echoue proprement — le protocole, lui, marche)")

    processus.terminate()
    print("\nMCP demystifie : trois messages JSON-RPC sur un pipe, des")
    print("schemas traduits pour le modele, un dispatch — la valeur est")
    print("dans la standardisation de la DECOUVERTE (1.2.5).")
