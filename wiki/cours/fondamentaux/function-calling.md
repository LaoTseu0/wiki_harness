# Function calling à la main

> [carte du cours](../carte.md) · étape : [`06_outils.py`](../../etapes/fondamentaux/06_outils.py)

## L'essentiel

Le modèle ne peut rien *faire* — il ne fait que générer du texte. Le
function calling est un **contrat de format** : on décrit des outils en
schéma JSON, le modèle génère un appel structuré, notre code le parse,
l'exécute, et renvoie le résultat comme un message de plus. Tout tient
au niveau HTTP/JSON — aucune magie.

## Le savoir

Le cycle complet, celui qu'il faut savoir raconter en entretien :

1. **Déclarer** : chaque outil = nom + description + schéma JSON des
   paramètres, injectés dans la requête (champ `tools`).
2. **Le modèle choisit** : au lieu d'une réponse texte, il émet un
   `tool_call` — un nom d'outil + des arguments JSON. C'est toujours de
   la **génération probabiliste** : le format est appris, pas garanti.
3. **Parser et exécuter** : notre code fait le dispatch
   (`{"heure_actuelle": fn, ...}`), exécute la vraie fonction Python.
4. **Renvoyer** : le résultat repart dans l'historique (rôle `tool`),
   et le modèle reprend la génération avec cette information.

C'est la boucle **ReAct** (Reasoning + Acting) industrialisée — à une
nuance près, à savoir dire en entretien : le papier ReAct (Yao et al.)
fait générer une trace de raisonnement explicite (« Thought: ») avant
chaque action ; le function calling natif n'émet que l'action, le
« raisonnement » restant implicite (ou dans le texte qui précède le
tool_call). Même alternance, sans le R visible — et la boucle
([mini-boucle d'agent](boucle-agent.md)) n'est
que la répétition de ce cycle.

**Sous le capot du champ `tools`** : le serveur fusionne schémas et
messages en un seul texte via le **template de chat** du modèle —
c'est ce texte, et rien d'autre, que le modèle voit ; un modèle dont
le template n'a pas de section outils « ne sait pas » appeler.
`ollama show <modèle> --template` le révèle — à regarder une fois pour
que le tool calling cesse d'être abstrait.

**Sécurité dès la conception** : les arguments générés sont des
**entrées non fiables** — un `calculer` naïf devient un `eval()`
arbitraire ; filtrer les caractères, valider les schémas, limiter les
périmètres.

## En pratique

[06_outils.py](../../etapes/fondamentaux/06_outils.py) : trois outils — `heure_actuelle`,
`calculer` (eval filtré), et `modeles_charges` **écrit par Anthony de
bout en bout** (appel httpx + schéma JSON + dispatch).

## Pièges connus

- Faire confiance aux arguments : le modèle a déjà fait une typo dans
  un nom de fichier qu'on lui demandait de créer — valider, toujours.
- Description d'outil vague → le modèle appelle le mauvais outil ou
  invente des paramètres ; la description est du prompt engineering.
- Oublier de renvoyer le résultat dans l'historique : le modèle
  « répond » sans avoir vu la donnée, en hallucinant l'exécution.

## Se tester

> Que se passe-t-il, au niveau HTTP et JSON, entre « le modèle décide
> d'appeler un outil » et « le modèle reçoit le résultat » ?
> *Réussi si* la réponse décrit les quatre étapes ci-dessus sans jamais
> dire « le framework s'en occupe », et situe où le code appelant agit.

## Références

- Doc tool use d'Ollama et de la Claude Messages API (mêmes concepts,
  champs différents)
- Papier ReAct (Yao et al., 2022) — pour situer l'origine du pattern
