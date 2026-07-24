"""
mesure_latences.py — le harnais qui chiffre le pipeline vocal.

Le pipeline de Jarvis (voix -> wake word -> VAD -> Whisper -> LLM ->
Piper -> audio) tourne en production mais n'est PAS mesure — et au
standard du cours, non mesure = pas acquis (lecon 7.1.1). Ce harnais
transforme des horodatages en tableau de latences (mediane + p95).

Deux subtilites de la lecon, integrees :
  - wake word != VAD : le chrono de la LATENCE PERCUE demarre a la
    FIN DE PAROLE detectee par le VAD (pas au wake word) et s'arrete
    au PREMIER audio de Piper (streaming : la premiere syllabe sort
    avant la fin de la synthese — l'analogue du TTFT) ;
  - le tout != la somme : les recouvrements (streaming, pipelining)
    font que le bout-en-bout REEL se mesure aussi, pas seulement les
    briques isolees.

Integration : le pipeline reel (repo homelab) appelle marquer() aux
frontieres de chaque brique et ecrit les sessions en JSONL ; ce script
agrege. En attendant le branchement : mode demo avec des horodatages
factices pour valider le tableau.
"""

import json
import statistics
import time
from pathlib import Path

FICHIER_MESURES = Path(__file__).parent / "latences.jsonl"

# Les frontieres de briques, dans l'ordre du pipeline. Chaque session
# est une serie d'horodatages nommes (time.perf_counter()).
ETAPES = [
    ("fin_de_parole", "reponse du VAD : fin de l'enonce (le chrono percu demarre ICI)"),
    ("transcription_prete", "Whisper a rendu le texte"),
    ("premier_token_llm", "le LLM commence a repondre (TTFT)"),
    ("dernier_token_llm", "le LLM a fini"),
    ("premier_audio_piper", "la premiere syllabe sort (le chrono percu s'arrete ICI)"),
    ("fin_audio_piper", "la synthese est terminee"),
]


class SessionVocale:
    """A instancier dans le pipeline reel : une session = un enonce."""

    def __init__(self):
        self.marques: dict[str, float] = {}

    def marquer(self, etape: str) -> None:
        self.marques[etape] = time.perf_counter()

    def enregistrer(self) -> None:
        with FICHIER_MESURES.open("a", encoding="utf-8") as f:
            f.write(json.dumps(self.marques) + "\n")


def calculer_intervalles(marques: dict) -> dict:
    """Les latences par brique + les deux bout-en-bout qui comptent."""
    def delta(a, b):
        return (marques[b] - marques[a]) * 1000 if a in marques and b in marques else None
    return {
        "stt_ms": delta("fin_de_parole", "transcription_prete"),
        "ttft_llm_ms": delta("transcription_prete", "premier_token_llm"),
        "generation_ms": delta("premier_token_llm", "dernier_token_llm"),
        "tts_premier_audio_ms": delta("dernier_token_llm", "premier_audio_piper"),
        # LA metrique : fin de ma phrase -> debut de la reponse audio.
        "latence_percue_ms": delta("fin_de_parole", "premier_audio_piper"),
        # Le bout-en-bout complet, pour voir les recouvrements.
        "total_ms": delta("fin_de_parole", "fin_audio_piper"),
    }


def agreger(sessions: list[dict]) -> None:
    intervalles = [calculer_intervalles(s) for s in sessions]
    print(f"{len(sessions)} sessions mesurees\n")
    print(f"{'brique':<24} {'mediane':>9} {'p95':>9}")
    print("-" * 44)
    for cle in intervalles[0]:
        valeurs = sorted(i[cle] for i in intervalles if i[cle] is not None)
        if not valeurs:
            continue
        p95 = valeurs[min(len(valeurs) - 1, int(0.95 * (len(valeurs) - 1)))]
        print(f"{cle:<24} {statistics.median(valeurs):>7.0f}ms {p95:>7.0f}ms")
    print("\nA verifier dans le tableau : latence_percue < somme des")
    print("briques STT+LLM+TTS (le streaming Piper recouvre la generation")
    print("— c'est SA raison d'etre, lecon 7.1.1). Ces chiffres sont le")
    print("nerf du post 'anatomy' (7.1.2).")


if __name__ == "__main__":
    if FICHIER_MESURES.exists():
        sessions = [json.loads(l) for l in
                    FICHIER_MESURES.read_text(encoding="utf-8").splitlines()]
    else:
        # Mode demo : 12 sessions factices, pour valider le tableau
        # avant de brancher le vrai pipeline (les VRAIES valeurs :
        # A MESURER sur jarvis-central).
        import random
        print("(latences.jsonl absent : demo avec horodatages factices)\n")
        sessions = []
        for _ in range(12):
            t = 0.0
            marques = {}
            for etape, _desc in ETAPES:
                t += random.uniform(0.1, 0.8)
                marques[etape] = t
            # le premier audio sort AVANT la fin du LLM (streaming) :
            marques["premier_audio_piper"] = marques["dernier_token_llm"] - 0.2
            sessions.append(marques)
    agreger(sessions)
