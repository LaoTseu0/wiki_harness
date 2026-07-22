"""
trace_test.py — la premiere trace, AVANT d'instrumenter quoi que ce soit.

Le reflexe de la lecon 6.1.1 : valider la chaine d'observabilite avec
un script minimal (une trace de test envoyee, retrouvee dans l'UI)
avant de coudre l'instrumentation dans le code des modules 2 et 3
(6.1.2). Si cette trace n'apparait pas, inutile de deboguer
l'instrumentation — c'est le deploiement qui cloche.

Prerequis :
  - Langfuse v3 deploye (compose officiel : web + worker, Postgres,
    ClickHouse, Redis, MinIO — l'empreinte se chiffre AVANT, RAM/disque) ;
  - un projet cree dans l'UI (ex. "homelab-rag") ;
  - les cles API en variables d'environnement (jamais en dur) :
        LANGFUSE_HOST, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY
  - pip install langfuse
"""

import os

try:
    from langfuse import Langfuse
except ImportError:
    raise SystemExit("SDK absent — pip install langfuse")

HOST = os.environ.get("LANGFUSE_HOST", "http://192.168.1.57:3000")

for variable in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"):
    if not os.environ.get(variable):
        raise SystemExit(f"{variable} absente — cles projet dans l'UI "
                         f"Langfuse, exportees en variables d'environnement")

langfuse = Langfuse(host=HOST)

# Une trace complete en miniature : le modele de donnees de la lecon
# (trace -> observations : spans, generations) sur un cas jouet.
with langfuse.start_as_current_span(name="trace-de-test") as trace:
    trace.update(input={"question": "trace de validation du deploiement"})

    with langfuse.start_as_current_span(name="retrieval-factice") as span:
        span.update(output={"chunks": 3, "ms": 42})

    with langfuse.start_as_current_generation(
        name="generation-factice",
        model="qwen3:4b-instruct-2507-q4_K_M",
        input=[{"role": "user", "content": "ping ?"}],
    ) as generation:
        generation.update(
            output="pong (factice)",
            usage_details={"input": 12, "output": 4},
        )

    trace.update(output={"reponse": "pong (factice)"})

# flush() force l'envoi AVANT la fin du process : l'export est
# asynchrone par defaut — sans flush, le script se termine et la
# trace part a la poubelle en silence (le revers de l'async, 6.1.2).
langfuse.flush()

print(f"trace envoyee — a retrouver dans l'UI ({HOST}, projet")
print("homelab-rag). Si elle n'apparait pas en ~30 s : logs du worker")
print("et de ClickHouse d'abord, l'instrumentation ensuite.")
