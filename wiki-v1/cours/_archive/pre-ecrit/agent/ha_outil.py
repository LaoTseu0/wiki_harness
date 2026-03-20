"""
ha_outil.py — le premier outil custom REEL : Home Assistant, borne.

La logique Python des deux outils que `pi.registerTool` enveloppera :
le pattern est exactement le function calling de 1.1.3, mais l'outil
touche la maison — donc chaque choix de perimetre compte (lecon 3.2.1) :

  - DEUX outils, pas un couteau suisse : ha_lire (etats, candidate au
    allow) / ha_agir (services, toujours en ask) ;
  - LISTE BLANCHE cote outil : HA ne scope pas finement ses tokens ->
    le scope se CONSTRUIT ici. Entites et services hors liste =
    refuses avant meme d'appeler HA. Les arguments s'ENUMERENT depuis
    la liste blanche : le modele ne peut pas inventer une entite hors
    perimetre ;
  - TOKEN d'un utilisateur HA DEDIE, NON admin, en variable
    d'environnement (HA_TOKEN) — jamais dans le code ni dans .pi/ ;
  - REPONSES COMPACTES : le JSON brut de HA (des milliers de tokens
    d'attributs) sature la fenetre — on resume cote outil, toujours.

Test reel de la lecon : "quelle temperature au salon ?" puis "allume
la lampe du bureau" (avec validation humaine visible cote harnais).
"""

import os

import httpx

HA_URL = os.environ.get("HA_URL", "http://192.168.1.57:8123")
HA_TOKEN = os.environ.get("HA_TOKEN", "")

# La liste blanche EST le perimetre. Les lampes du salon oui, la
# serrure non — et la description de l'outil enonce ce perimetre
# exact (une description vague -> le modele tente des services non
# prevus, piege de la lecon).
ENTITES_AUTORISEES = {
    "sensor.salon_temperature",
    "sensor.bureau_temperature",
    "light.salon_plafond",
    "light.bureau_lampe",
}
SERVICES_AUTORISES = {
    ("light", "turn_on"),
    ("light", "turn_off"),
}


def _entetes() -> dict:
    if not HA_TOKEN:
        raise SystemExit("HA_TOKEN absent — creer un utilisateur HA dedie "
                         "non admin et exporter son token longue duree")
    return {"Authorization": f"Bearer {HA_TOKEN}"}


def ha_lire(entity_id: str) -> str:
    """LECTURE seule, liste blanche, reponse compacte."""
    if entity_id not in ENTITES_AUTORISEES:
        # Le refus est une information pour le modele (lecon 1.1.4) :
        # on liste ce qui est permis au lieu d'un "non" sec.
        return (f"Entite hors perimetre : {entity_id}. Autorisees : "
                f"{', '.join(sorted(ENTITES_AUTORISEES))}")
    reponse = httpx.get(f"{HA_URL}/api/states/{entity_id}",
                        headers=_entetes(), timeout=10)
    if reponse.status_code == 404:
        return f"Entite inconnue de HA : {entity_id}"
    reponse.raise_for_status()
    d = reponse.json()
    # Resume : etat + unite, PAS le dict d'attributs complet.
    unite = d.get("attributes", {}).get("unit_of_measurement", "")
    return f"{entity_id} = {d['state']} {unite}".strip()


def ha_agir(domaine: str, service: str, entity_id: str) -> str:
    """ACTION, liste blanche double (service ET entite). Cote harnais,
    cet outil passe en ask : la validation humaine reste au-dessus —
    la liste blanche borne ce qui est demandable, l'humain valide ce
    qui est demande."""
    if (domaine, service) not in SERVICES_AUTORISES:
        return (f"Service hors perimetre : {domaine}.{service}. Autorises : "
                f"{', '.join(f'{d}.{s}' for d, s in sorted(SERVICES_AUTORISES))}")
    if entity_id not in ENTITES_AUTORISEES:
        return f"Entite hors perimetre : {entity_id}"
    reponse = httpx.post(
        f"{HA_URL}/api/services/{domaine}/{service}",
        headers=_entetes(), json={"entity_id": entity_id}, timeout=10,
    )
    reponse.raise_for_status()
    # Confirmation TEXTE explicite : le modele ne voit que ce qu'on
    # lui renvoie ("aucune sortie" est ambigu — incident du module 1).
    return f"Service {domaine}.{service} execute sur {entity_id}."


# Les schemas a donner a pi.registerTool : arguments ENUMERES depuis
# les listes blanches — le perimetre est DANS le contrat de l'outil.
SCHEMA_HA_LIRE = {
    "name": "ha_lire",
    "description": "Lit l'etat d'UNE entite Home Assistant autorisee "
    "(capteurs et lampes du salon/bureau uniquement).",
    "parameters": {
        "type": "object",
        "properties": {
            "entity_id": {"type": "string",
                          "enum": sorted(ENTITES_AUTORISEES)},
        },
        "required": ["entity_id"],
    },
}
SCHEMA_HA_AGIR = {
    "name": "ha_agir",
    "description": "Allume ou eteint UNE lampe autorisee (salon/bureau). "
    "Toute action est soumise a validation humaine.",
    "parameters": {
        "type": "object",
        "properties": {
            "domaine": {"type": "string", "enum": ["light"]},
            "service": {"type": "string", "enum": ["turn_on", "turn_off"]},
            "entity_id": {"type": "string",
                          "enum": sorted(e for e in ENTITES_AUTORISEES
                                         if e.startswith("light."))},
        },
        "required": ["domaine", "service", "entity_id"],
    },
}


if __name__ == "__main__":
    print(ha_lire("sensor.salon_temperature"))
    print(ha_lire("lock.porte_entree"))          # hors perimetre : refus
    print(ha_agir("light", "turn_on", "light.bureau_lampe"))
    print(ha_agir("lock", "unlock", "lock.porte_entree"))  # refus double
