"""
rag_llamaindex.py — la meme chaine, refaite dans le framework.

L'exercice n'est pas d'apprendre un outil : c'est de MAPPER chaque
abstraction LlamaIndex sur le script maison deja ecrit (la table de
correspondance de la lecon 2.3.1), et de tenir le double registre
apports / caches. Chaque defaut du framework est ici soit REPRIS EN
MAIN (commente "repris"), soit ACCEPTE ET NOTE (commente "accepte").

Correspondance appliquee dans ce fichier :
    SimpleDirectoryReader        <- lecture des .md (03)
    MarkdownNodeParser           <- decoupe par sections (03)
    OllamaEmbedding              <- embedder() httpx (01)
    QdrantVectorStore            <- migration 2.2.1
    retriever(similarity_top_k)  <- rechercher() (05)
    query_engine                 <- la chaine complete (06)

Meme Qdrant, meme modele que la v0.0.2 : l'ecart d'evals mesure
exactement l'effet des defauts du framework — chaque ecart s'explique
ou se corrige (piege : comparer LlamaIndex-avec-ses-defauts a notre
chaine reglee et accuser le framework).

Prerequis : pip install llama-index llama-index-embeddings-ollama
llama-index-llms-ollama llama-index-vector-stores-qdrant
"""

import sys
from pathlib import Path

MODULE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE))

from rag_commun import MODELE_CHAT, MODELE_EMBED, OLLAMA, RACINE

try:
    from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
    from llama_index.core.node_parser import MarkdownNodeParser
    from llama_index.core.prompts import PromptTemplate
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.llms.ollama import Ollama
except ImportError:
    raise SystemExit("llama-index absent — voir prerequis en docstring")

# REPRIS EN MAIN : le prompt de synthese par defaut est en anglais,
# SANS notre grounding ni notre "je ne sais pas" — le laisser tel quel
# fait bouger le score hallucination et on accuserait le framework
# (piege n.1 de la lecon). On remet NOTRE consigne de la 2.1.6.
PROMPT_MAISON = PromptTemplate(
    "Tu es l'assistant de documentation d'un homelab. Reponds a la "
    "question UNIQUEMENT avec les extraits ci-dessous. Cite tes sources "
    "au format (source : fichier > section). Si les extraits ne "
    "suffisent pas pour repondre, dis-le clairement.\n\n"
    "=== EXTRAITS ===\n\n{context_str}\n\n"
    "Question : {query_str}\nReponse :"
)


def construire_moteur():
    # ACCEPTE ET NOTE : SimpleDirectoryReader lit les .md avec son
    # propre parsing (metadonnees differentes de notre 03) — on note,
    # on comparera les comptes de chunks avec les 132 de la v0.0.1.
    documents = SimpleDirectoryReader(
        input_dir=str(RACINE), required_exts=[".md"], recursive=True,
    ).load_data()

    # REPRIS EN MAIN : MarkdownNodeParser au lieu du chunking par
    # defaut (1024/20 si on ne dit rien — un defaut CACHE qui aurait
    # change tous les scores retrieval sans un mot).
    noeuds = MarkdownNodeParser().get_nodes_from_documents(documents)
    print(f"{len(documents)} documents -> {len(noeuds)} noeuds "
          f"(a comparer aux 132 sections de la v0.0.1)")

    index = VectorStoreIndex(
        noeuds,
        embed_model=OllamaEmbedding(model_name=MODELE_EMBED,
                                    base_url=OLLAMA),
    )

    # REPRIS EN MAIN : response_mode="compact" explicite. Les modes
    # refine/tree_summarize font PLUSIEURS appels LLM sans qu'on le
    # voie — chaque option non defaut doit avoir sa ligne d'ablation.
    return index.as_query_engine(
        llm=Ollama(model=MODELE_CHAT, base_url=OLLAMA,
                   temperature=0, request_timeout=180),
        similarity_top_k=3,
        response_mode="compact",
        text_qa_template=PROMPT_MAISON,
    )


if __name__ == "__main__":
    moteur = construire_moteur()
    question = "Qu'est-ce qu'on avait decide pour le backup du NAS ?"
    print(f"\nQ: {question}\n")
    reponse = moteur.query(question)
    print(reponse)
    print("\nSources remontees par le framework :")
    for noeud in reponse.source_nodes:
        nom = noeud.metadata.get("file_name", "?")
        print(f"   {noeud.score:.4f}  {nom}")
    print("\nA faire (lecon 2.3.1) : rejouer le jeu d'evals complet sur")
    print("ce moteur (meme Qdrant, meme modele) et documenter chaque")
    print("ecart avec la v0.0.2 dans le registre apports/caches du README.")
