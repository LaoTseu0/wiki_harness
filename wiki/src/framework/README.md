# framework

Ce dossier se remplit **par promotion**, jamais par anticipation.

Quand une leçon est comprise — pas lue, comprise : le code écrit à la main
tourne et on sait dire pourquoi chaque ligne est là — la brique réutilisable
qui en sort est reprise depuis `etapes/`, nettoyée (typée, testée), et la
leçon gagne une section « Ce que ça change dans le framework ». Le mécanisme
complet est dans [cours/framework/promotion.md](../../cours/framework/promotion.md).

## Ce qui est monté

| Brique | Vient de | Ce qu'elle rend |
|---|---|---|
| `llm/ollama.py` | [chat, historique et contexte](../../cours/fondamentaux/chat-historique-contexte.md) | `chat()` → `Reponse(contenu, tokens_lus, tokens_generes)` ; `stream()` → les morceaux |
| `contexte.py` | la même | `tronquer()` et `compacter()` sur une liste de messages |

Pas d'interface de client : `llm/` n'a qu'une implémentation, et un `Protocol`
écrit à une seule décrirait Ollama plutôt qu'un contrat. Elle arrivera avec le
deuxième provider.

Sous-paquets attendus au fil du parcours : `outils/`, `agent/` (la boucle),
`memoire/`, `retrieval/`, `evals/`. Aucun n'est créé d'avance — un dossier
vide n'est pas une architecture, c'est une intention.

## Tests

```bash
python -m pytest -q
```

Le chemin d'import passe par `pythonpath = ["src"]` dans `pyproject.toml` :
pas d'installation, pas de `sys.path` bricolé dans les tests.
