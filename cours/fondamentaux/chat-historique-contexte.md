# Chat CLI, historique et contexte

> [carte du cours](../carte.md) · étape : [`01_hello.py`](../../etapes/fondamentaux/01_hello.py)

## Où ça s'emboîte

- **Processus** : [d'un texte à un token](../_processus/generation-token.md)
- **L'étape ouverte** : `messages` — la liste côté client, renvoyée en entier à chaque tour et où le token généré est réinjecté

![[chat-historique-contexte.canvas]]

## L'essentiel

Un LLM est **stateless** : il ne se souvient de rien entre deux appels.
« Avoir une conversation » est une illusion reconstruite par le client —
c'est *nous* qui renvoyons l'historique entier à chaque tour. Toute la
gestion de contexte (troncature, compaction, streaming) découle de ce
fait unique.

## Le savoir

- **Le format messages** : une liste `[{role, content}]` avec trois
  rôles — `system` (comportement), `user`, `assistant`. L'API reçoit
  la liste complète et prédit le message suivant. Rien d'autre.
- **Conséquence économique** : chaque tour re-paye tout le préfixe. Une
  conversation de n tours coûte O(n²) tokens cumulés — d'où le prompt
  caching ([1.2.4](../inference/prompt-caching.md))
  et la compaction.
- **Streaming** : la réponse arrive token par token (lignes NDJSON chez
  Ollama, SSE chez les API cloud). L'UX de tout chat : afficher au fil
  de l'eau au lieu d'attendre la fin. Métrique associée : la latence du
  premier token (TTFT).
- **La fenêtre déborde** : system + historique + outils + documents
  finissent par dépasser le contexte. Deux réponses écrites à la main :
  - **troncature** (sliding window) : garder le system + les k derniers
    messages — simple, mais oublie le début ;
  - **compaction** : résumer les anciens tours par un appel LLM et
    placer le résumé **en system** — garde le sens, perd le verbatim.
    Pour recompacter sans dérive : ne jamais redonner le résumé
    précédent à résumer — résumer uniquement les tours *nouveaux*
    depuis la dernière compaction et concaténer/fusionner les
    résumés (l'historique brut, archivé hors contexte, permet de
    régénérer en cas de doute). Et « garde le sens » se **mesure** :
    quelques questions de rappel posées avant/après compaction (le
    fait du tour 2 survit-il ?) — sinon c'est une opinion.
- **Compter les tokens** : le modèle ne voit pas des mots
  (tokenisation, couche 0 de la [roadmap](../_archive/roadmap.md)) ;
  l'API renvoie les comptes exacts (`prompt_eval_count`/`eval_count`
  chez Ollama) — les afficher à chaque tour rend le coût visible.

## En pratique

[01_hello.py](../../etapes/fondamentaux/01_hello.py) (l'appel brut),
[02_chat.py](../../etapes/fondamentaux/02_chat.py) (boucle de chat + compteur de tokens),
[03_stream.py](../../etapes/fondamentaux/03_stream.py) (streaming NDJSON),
[05_contexte.py](../../etapes/fondamentaux/05_contexte.py) (`tronquer()` par slicing, puis
compaction déboguée en live : trace du résumé, placement en system).

## Pièges connus

- Tronquer en jetant le message `system` — le comportement du bot
  change silencieusement.
- Résumer avec le résumé précédent dans l'entrée → dérive cumulative
  (le résumé du résumé s'appauvrit).
- Estimer les tokens avec `len(texte.split())` — faux dès qu'il y a du
  code, des accents ou une autre langue ; utiliser les comptes de l'API.

## Se tester

> « Pourquoi l'API d'un LLM est-elle stateless, et qu'est-ce que ça
> implique pour votre application ? »
> Réponse attendue : le serveur d'inférence ne conserve pas l'état
> conversationnel ; le client renvoie tout l'historique, donc le coût
> croît avec la conversation, et la gestion du contexte (troncature,
> compaction, mémoire externe) est **votre** responsabilité, pas celle
> du modèle.

## Références

- Karpathy, « Intro to LLMs » (couche 0 de la [roadmap](../_archive/roadmap.md))
- Doc API Ollama (`/api/chat`, streaming NDJSON)
