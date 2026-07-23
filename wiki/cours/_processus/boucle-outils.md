# D'une tâche à un résultat

> Processus canonique. C'est **la** description de la chaîne : les leçons
> qui l'utilisent n'en redonnent pas leur version, elles déclarent quelle
> étape elles ouvrent. Corriger ici corrige tous les schémas.
> Les `.canvas` se régénèrent — ne jamais les éditer à la main.

![[boucle-outils.canvas]]

Le second processus du cours, et il en **contient** un autre : l'étape
`emission` est un parcours entier de [d'un texte à un
token](generation-token.md), répété autant de fois qu'il y a de tokens dans
l'appel produit. Les deux chaînes ne sont pas concurrentes, elles sont
emboîtées — c'est pourquoi un plafond de tours et un `num_predict` ne bornent
pas la même chose.

La boucle se referme sur `schema` et non sur `emission` : au tour suivant, ce
n'est pas la génération qui reprend là où elle en était, c'est **la requête
entière qui repart**, catalogue d'outils et historique compris. Rien n'est
conservé côté serveur entre deux tours — le fait stateless de [chat, historique
et contexte](../fondamentaux/chat-historique-contexte.md), vu ici à l'échelle
de l'agent.

## Les étapes

| id | Étape | Ce qu'elle fait |
|---|---|---|
| `schema` | Le schéma annoncé | des noms, des descriptions et des types joints à la requête — champ `tools` ou champ `format` |
| `contrainte` | La contrainte de forme | ce que le schéma fait réellement pendant la génération, et qui diffère selon le champ employé |
| `emission` | L'émission | le modèle rend un message : du texte libre, ou un appel structuré |
| `dispatch` | Le dispatch | le nom généré est résolu en fonction Python, ou refusé faute d'entrée |
| `execution` | L'exécution | la fonction tourne derrière ses gardes — périmètre, validation, délai |
| `renvoi` | Le renvoi | la valeur de retour entre dans l'historique, en message de rôle `tool` |
| `plafond` | Le plafond de tours | ce qui reprend la main quand le modèle ne conclut pas |

## Le fil

- `schema` → `contrainte` : les types que la sortie devra respecter
- `contrainte` → `emission` : selon le champ, du texte dans le prompt ou un masque sur les tokens
- `emission` → `dispatch` : un nom d'outil et des arguments JSON
- `dispatch` → `execution` : la fonction Python résolue, et ses arguments déballés
- `execution` → `renvoi` : une valeur de retour, à rendre lisible par le modèle
- `renvoi` → `plafond` : l'historique augmenté d'un message de plus
- `plafond` → `schema` : un tour de plus — la requête entière repart
