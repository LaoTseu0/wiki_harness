"""
06_rag.py — la chaine complete : Retrieval-Augmented Generation.

On assemble tout. A chaque question :
  1. rechercher() (05) -> les 3 chunks les plus pertinents
  2. construire_prompt() -> un prompt qui COLLE ces chunks comme
     contexte + une consigne d'ancrage (repondre seulement a partir
     d'eux, citer les sources)
  3. generer() -> Qwen3 repond (l'/api/chat du module 1, retrouve)

Tu reconnais la fin : un prompt system enrichi, comme la compaction du
05 (module 1). La difference RAG : le contexte est RECUPERE
automatiquement au bon moment (les 3 chunks utiles), au lieu d'etre
toute la conversation. Le modele reste stateless — on ne lui "apprend"
rien, on lui souffle les bonnes notes.

Le mot d'entretien pour ce qu'on fait ici : GROUNDING (ancrage). Deux
leviers, tous les deux dans le prompt system :
  - "reponds UNIQUEMENT a partir des extraits" -> limite les
    hallucinations (le modele n'invente pas hors contexte) ;
  - "cite tes sources (source : fichier > section)" -> reponse
    verifiable, l'utilisateur peut remonter au .md d'origine.

Ces deux consignes sont l'essentiel du prompt : je te les fournis
redigees (c'est du savoir-faire), mais l'exercice est de les ASSEMBLER
avec les chunks recuperes.

=== EXERCICE ===================================================
Completer construire_prompt(question, chunks). generer() et
repondre() sont fournis.

Spec de construire_prompt(question, chunks) -> list[dict] :
  - chunks : liste de (score, fichier, titre, texte) (sortie du 05)
  - etape 1 : pour chaque chunk, fabriquer un bloc de texte :
        f"[source : {fichier} > {titre}]\\n{texte}"
      (le score ne sert pas au modele, on l'ignore ici)
  - etape 2 : les joindre par "\\n\\n" -> la variable `contexte`
  - etape 3 : renvoyer la liste de messages :
        [{"role": "system", "content": CONSIGNE + contexte},
         {"role": "user",   "content": question}]
      ou CONSIGNE est la constante fournie ci-dessous.

Attendu pour "backup du NAS" : une reponse qui parle de rsync/cron
et cite (source : backlog.md > NAS).
================================================================
"""

import httpx

from importlib import import_module

from rag_commun import MODELE_CHAT, OLLAMA

# "05_rechercher" commence par un chiffre : import classique impossible,
# on passe par import_module (juste pour reutiliser ton code du 05).
_m05 = import_module("05_rechercher")
charger_index = _m05.charger_index
rechercher = _m05.rechercher

CONSIGNE = (
    "Tu es l'assistant de documentation d'un homelab. Reponds a la "
    "question UNIQUEMENT avec les extraits ci-dessous. Cite tes sources "
    "au format (source : fichier > section). Si les extraits ne "
    "suffisent pas pour repondre, dis-le clairement.\n\n"
    "=== EXTRAITS ===\n\n"
)


def construire_prompt(question: str, chunks: list[tuple]) -> list[dict]:
    """Assemble les messages [system + contexte, user] pour le modele."""
    ...  # A COMPLETER (blocs -> contexte -> messages)


def generer(messages: list[dict]) -> str:
    """Appelle Qwen3 (/api/chat). temperature=0 + seed : reponse stable."""
    reponse = httpx.post(
        f"{OLLAMA}/api/chat",
        json={
            "model": MODELE_CHAT,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0, "seed": 42, "num_predict": 500},
        },
        timeout=180,
    )
    reponse.raise_for_status()
    return reponse.json()["message"]["content"]


def repondre(question: str, index: list[tuple], k: int = 3) -> tuple[list, str]:
    """Chaine complete : renvoie (chunks_utilises, reponse_texte)."""
    chunks = rechercher(question, index, k)
    messages = construire_prompt(question, chunks)
    return chunks, generer(messages)


if __name__ == "__main__":
    index = charger_index()
    question = "Qu'est-ce qu'on avait decide pour le backup du NAS ?"
    print(f"Q: {question}\n")

    chunks, reponse = repondre(question, index)

    print("Chunks injectes dans le contexte :")
    for score, fichier, titre, _ in chunks:
        print(f"   {score:.4f}  {fichier} > {titre}")
    print(f"\nReponse du modele :\n{reponse}")
