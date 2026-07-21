"""
instrumentation.py — le point de couture unique de l'observabilite.

La regle de la lecon 6.1.2 : l'instrumentation se coud A LA FRONTIERE
provider (2.4.2) pour les generations — UN seul point pour tous les
appels LLM — et dans rag_commun pour les spans metier. Le code
applicatif ne voit pas Langfuse : ce module fournit le decorateur et
le context manager, remplacables (si Langfuse change, un seul fichier
bouge).

La granularite des spans epouse l'architecture (la trace RAG type) :
    trace "ask"
    |- span retrieval (question, k -> chunks + scores, ms)
    |  |- span embed_query
    |  |- span search
    |- span rerank (si actif)
    |- generation "answer" (prompt, reponse, tokens, ms)

Fiabilite du canal (ajout de la relecture critique) : l'export est
asynchrone (ne jamais bloquer la reponse pour tracer), MAIS un export
qui echoue perd en silence les traces d'incident — d'ou : flush au
shutdown, et un compteur local d'evenements perdus qui rend la perte
VISIBLE.

Degradation propre : sans cles Langfuse, tout fonctionne en no-op —
l'application ne meurt jamais de son observabilite.
"""

import functools
import os
import time
from contextlib import contextmanager

_evenements_perdus = 0   # le compteur qui rend la perte visible

try:
    from langfuse import Langfuse
    _langfuse = (Langfuse(host=os.environ.get("LANGFUSE_HOST",
                                              "http://192.168.1.57:3000"))
                 if os.environ.get("LANGFUSE_PUBLIC_KEY") else None)
except ImportError:
    _langfuse = None

if _langfuse is None:
    print("(instrumentation en mode no-op : SDK ou cles absents)")


@contextmanager
def span(nom: str, **attributs):
    """Le span metier : `with span("retrieval", k=5): ...`
    A poser au MAILLON metier (celui qu'on voudra accuser) — ni un
    span "toute la requete", ni un par fonction (pieges de la lecon)."""
    global _evenements_perdus
    debut = time.perf_counter()
    contexte = None
    if _langfuse is not None:
        try:
            contexte = _langfuse.start_as_current_span(name=nom,
                                                       input=attributs)
            contexte.__enter__()
        except Exception:
            _evenements_perdus += 1
            contexte = None
    try:
        yield
    except Exception as erreur:
        # Les erreurs sont les traces les plus precieuses : capturees
        # AVEC leur contexte, pas seulement les succes.
        if contexte is not None:
            contexte.__exit__(None, None, None)
            contexte = None
            _fermer_span_erreur(nom, erreur)
        raise
    finally:
        if contexte is not None:
            try:
                duree_ms = int((time.perf_counter() - debut) * 1000)
                contexte.__exit__(None, None, None)
            except Exception:
                _evenements_perdus += 1


def _fermer_span_erreur(nom: str, erreur: Exception) -> None:
    global _evenements_perdus
    try:
        with _langfuse.start_as_current_span(name=f"{nom}:erreur") as s:
            s.update(output={"erreur": str(erreur)[:500]}, level="ERROR")
    except Exception:
        _evenements_perdus += 1


def generation_tracee(fonction):
    """Le decorateur pour la frontiere provider : enveloppe chat().
    Metadonnees a fournir par l'appelant via l'attribut _meta du
    provider : version du corpus, config de chaine, tag git — ce qui
    correle traces et tableau d'evals (2.3.4)."""
    @functools.wraps(fonction)
    def enveloppe(self, messages, **options):
        global _evenements_perdus
        if _langfuse is None:
            return fonction(self, messages, **options)
        debut = time.perf_counter()
        try:
            contexte = _langfuse.start_as_current_generation(
                name="chat",
                model=getattr(self, "modele_chat", "?"),
                input=messages,
                metadata=getattr(self, "_meta", {}),
            )
        except Exception:
            _evenements_perdus += 1
            return fonction(self, messages, **options)
        with contexte as generation:
            reponse = fonction(self, messages, **options)
            try:
                generation.update(
                    output=reponse.get("content", "")[:2000],
                    usage_details={
                        "input": reponse.get("tokens_entree", 0),
                        "output": reponse.get("tokens_sortie", 0),
                    },
                )
            except Exception:
                _evenements_perdus += 1
        return reponse
    return enveloppe


def shutdown() -> None:
    """A appeler a l'arret du service : flush + bilan des pertes."""
    if _langfuse is not None:
        _langfuse.flush()
    if _evenements_perdus:
        print(f"ATTENTION : {_evenements_perdus} evenement(s) de trace "
              f"perdu(s) — le canal d'observabilite a des trous")


if __name__ == "__main__":
    # Demonstration no-op / reelle selon les cles presentes.
    with span("retrieval", question="test", k=3):
        time.sleep(0.05)
    shutdown()
    print("instrumentation ok — a coudre : decorateur sur le chat() des")
    print("providers (2.4.2), spans dans rag_commun, events du hook du")
    print("module 3 (la trace devient aussi un journal de securite).")
