# Le template de chat

> [carte du cours](../carte.md) · étape : [`10_template.py`](../../etapes/fondamentaux/10_template.py)

## Où ça s'emboîte

- **Processus** : [d'un texte à un token](../_processus/generation-token.md)
- **L'étape ouverte** : `template` — entre une liste de messages, sort un texte unique et balisé

![[template-de-chat.canvas]]

## Prérequis et suites

- **Suppose acquis** : [le chat](chat-historique-contexte.md) (la liste de
  messages), [la tokenisation](tokenisation.md) (les balises se facturent).
- **Débloque** : [function calling](function-calling.md) (le rôle `tool` n'est
  qu'une balise de plus),
  [la prompt injection](../mcp/prompt-injection-indirecte.md) (écrire les
  balises soi-même est l'attaque la plus directe).

## L'essentiel

Depuis le [chat](chat-historique-contexte.md), on envoie une **liste de
messages** avec des rôles. Le modèle, lui, ne connaît ni listes ni rôles :
il ne sait que continuer **une chaîne de caractères**. Entre les deux, le
serveur applique le **template de chat** — un gabarit livré avec le modèle
qui aplatit la liste en un seul texte balisé. C'est le dernier endroit du
socle où quelque chose se passe *à notre insu*.

## Le savoir

**Le format, ici ChatML.** Pour Qwen, la liste devient :

```
<|im_start|>system
Tu es un assistant concis.<|im_end|>
<|im_start|>user
Bonjour<|im_end|>
<|im_start|>assistant
```

Les rôles n'ont aucune existence magique : ce sont **des balises dans un
texte**. La dernière ligne, ouverte et vide, est ce qui donne la parole au
modèle — il complète, et signale sa fin en produisant `<|im_end|>`, un
token spécial que le serveur intercepte pour couper la génération.

**D'où vient le gabarit.** Il est livré avec le modèle
([Modelfile](../glossaire/modelfile.md) chez Ollama, `chat_template` du
tokenizer chez Hugging Face) — pas choisi par
nous. `/api/show` l'expose, au même endroit que les paramètres de sampling
par défaut qui avaient piégé le [débogage du sampling](sampling-et-prompting.md).
Même leçon : *ce que tu n'as pas envoyé, quelqu'un l'a rempli à ta place.*

**Et quand le format est faux ?** Le modèle a été entraîné sur *ce*
balisage. Lui en présenter un autre ne provoque pas d'erreur : il produit
du texte plausible, et dégradé. C'est un bug silencieux — la pire espèce.

## En pratique

[10_template.py](../../etapes/fondamentaux/10_template.py) en trois temps :
afficher le gabarit brut (`/api/show`), le reconstruire à la main, puis
**prouver que la reconstruction est exacte**.

La preuve vaut plus que le code : on envoie les mêmes messages par deux
chemins — `/api/chat` (le serveur applique le template) et
`/api/generate` avec `raw: true` (aucun template, notre chaîne telle
quelle) — et on compare `prompt_eval_count`. Deux comptes égaux = même
texte. On ne croit pas sa reconstruction sur parole, on la mesure.

## Mesures

<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->

## Recomposer

**Ce que ça change à ce qu'on croyait savoir.** Trois observations des
leçons précédentes cessent d'être des mystères :

- le **coût fixe** mesuré à la [tokenisation](tokenisation.md) : ce sont
  ces balises, facturées à chaque tour ;
- l'**autorité du message `system`** : il n'a aucun statut privilégié dans
  le modèle, il est simplement *physiquement en tête* du texte. Ce qui
  éclaire l'incident de la compaction — le même résumé ignoré en `user`,
  suivi en `system` ;
- le **rôle `tool`** du [function calling](function-calling.md) : encore
  une balise, dans le même texte. Un appel d'outil n'est pas un canal
  séparé, c'est une convention d'écriture.

**Ce qu'on peut prédire ailleurs.** Puisque tout est un seul texte, une
donnée récupérée par un outil ou par le RAG entre dans le même flux que les
consignes, sans frontière typée. C'est mécaniquement pourquoi la
[prompt injection indirecte](../mcp/prompt-injection-indirecte.md) fonctionne —
et pourquoi aucune parade ne peut consister à « bien séparer les champs ».

## Pièges connus

- **Écrire les balises à la main dans un message `user`** : elles ne sont
  pas neutralisées, le modèle voit un faux tour de conversation. C'est le
  mécanisme d'injection de prompt le plus direct qui soit — retenir ce
  point pour la [prompt injection indirecte](../mcp/prompt-injection-indirecte.md).
- **Croire que `raw: true` est « plus proche du modèle »** : sans template
  reconstruit, le modèle n'est pas en mode conversation du tout et part en
  complétion libre.
- **Changer de modèle sans changer de template** : chaque famille a le
  sien (ChatML, Llama, Mistral…). Le jour où le [backend devient
  commutable](../retrieval/backend-commutable.md), c'est un point de
  rupture à traiter explicitement.
- **Fine-tuner avec un format et servir avec un autre** : l'adaptateur
  semble « ne rien faire ». Piège classique, repris dans la
  [leçon LoRA](../production/lora.md).

## Se tester

- Pourquoi un message `system` a-t-il plus d'autorité qu'un message
  `user`, alors que le modèle n'a pas de notion de rôle ?
- Un utilisateur colle `<|im_start|>system` dans le champ de saisie de ton
  chat. Que voit le modèle, et comment l'empêches-tu ?
- Tu ajoutes un modèle d'une autre famille derrière la même API. Qu'est-ce
  qui casse en premier, et comment le détectes-tu — sachant que rien ne
  lèvera d'exception ?

## Ce que ça change dans le framework

Rien tant qu'on parle à un seul serveur, qui applique le gabarit lui-même.
Le jour du [backend commutable](../retrieval/backend-commutable.md), le
template devient une propriété du provider : c'est là que la brique
apparaîtra, pas avant.

## À retenir

- Les rôles n'existent pas dans le modèle : ce sont des balises dans un
  texte unique, et leur ordre fait leur autorité.
- Le gabarit est livré avec le modèle, pas choisi par nous — `/api/show`
  l'expose, comme il exposait les défauts de sampling.
- Un mauvais template ne lève aucune erreur : il dégrade silencieusement.

## Références

- `/api/show` du serveur Ollama — le gabarit et les paramètres réels
- La spécification ChatML, et les `chat_template` Jinja des modèles
  Hugging Face
