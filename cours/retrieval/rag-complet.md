# RAG complet

> [carte du cours](../carte.md) · étape : [`06_rag.py`](../../etapes/retrieval/06_rag.py)

## L'essentiel

Brancher le « G » sur le « R » : le top-k remonte, on le met **dans le
prompt** avec la question, et on exige une réponse **fondée sur ce
contexte, citations à l'appui**. Le grounding — répondre depuis les
sources, dire « je ne sais pas » sinon — est ce qui distingue un RAG
d'un chatbot qui brode.

## Le savoir

- **Le prompt RAG canonique**, trois blocs :
  1. **system** : « Tu réponds uniquement à partir des documents
     fournis. Cite le fichier source de chaque affirmation. Si les
     documents ne contiennent pas la réponse, dis-le. » ;
  2. **contexte** : les k chunks, chacun balisé par sa source
     (`[architecture/backup.md § NAS]`) — les balises rendent la
     citation possible ;
  3. **question** de l'utilisateur.
- **Pourquoi les citations** : elles rendent la réponse **vérifiable**
  (cliquer, relire la source), elles disciplinent le modèle (générer
  une citation l'ancre au passage), et elles sont mesurables en eval
  (la source citée est-elle la bonne ?).
- **Le « je ne sais pas » est une feature** : la baseline du module
  affiche **zéro hallucination** précisément parce que le prompt
  autorise et valorise l'abstention. Un RAG qui répond toujours est un
  RAG qui hallucine parfois.
- **L'ordre compte** : instructions stables en system (cacheable,
  [1.2.4](../inference/prompt-caching.md)),
  contexte variable ensuite, question en dernier — et le contexte
  reste borné (k × taille de chunk : le budget se calcule) **et se
  confronte à la fenêtre réellement servie** : Ollama tronque
  silencieusement au-delà de `num_ctx` (défaut modeste, souvent
  4096). Fixer `num_ctx` explicitement dans les options et vérifier
  que `prompt_eval_count` correspond au budget calculé — sinon le
  grounding se joue sur un prompt amputé.
- **Grounding ≠ vérité** : le modèle peut mal lire une bonne source.
  La chaîne complète se juge donc sur deux axes distincts — retrieval
  et fidélité — mesurés séparément en
  [2.1.7](evals.md).

## En pratique

[06_rag.py](../../etapes/retrieval/06_rag.py) : assembler retrieval
([05_rechercher](recherche-top-k.md)) +
prompt + appel génération (Qwen3 4B) ; sortie = réponse + liste des
sources utilisées. Premier test réel : « qu'est-ce qu'on avait décidé
pour le backup du NAS ? ».

## Pièges connus

- Instructions de grounding noyées *après* le contexte : le modèle lit
  40 blocs puis « oublie » la consigne — la consigne vit en system.
- Chunks sans balise de source : le modèle cite « le document » —
  invérifiable, donc invendable.
- Sur-contraindre (« ne réponds QUE par des citations ») : réponses
  inutilisables ; le grounding contraint le *fond*, pas la forme.
- Prompt RAG > `num_ctx` : troncature silencieuse — le modèle
  « ignore » des chunks qu'on croit lui avoir donnés ; symptôme :
  `prompt_eval_count` qui plafonne d'un appel à l'autre.

## Se tester

> « Comment empêchez-vous votre RAG d'halluciner ? »
> Grounding explicite en system, abstention autorisée et valorisée,
> citations obligatoires et vérifiables, contexte borné — et un taux
> d'hallucination **mesuré** dans les evals, pas affirmé.

## Références

- [Schéma 05_rag_grounding](../_schemas/retrieval/05_rag_grounding.png)
- Le vocabulaire des offres : « grounding/citations/hallucinations »
  (Cenova, STEP UP — [roadmap §10.1](../_archive/roadmap.md))
