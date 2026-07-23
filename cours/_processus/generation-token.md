# D'un texte à un token

> Processus canonique. C'est **la** description de la chaîne : les leçons
> qui l'utilisent n'en redonnent pas leur version, elles déclarent quelle
> étape elles ouvrent. Corriger ici corrige tous les schémas.
> Les `.canvas` se régénèrent — ne jamais les éditer à la main.

![[generation-token.canvas]]

Un appel au modèle traverse toujours cette chaîne, et la parcourt **une
fois par token généré**. Le retour de `tirage` vers `messages` n'est pas
une commodité de dessin : c'est l'autorégression, le token produit devient
l'entrée du suivant, sans retour en arrière possible.

L'ordre retenu ici pour les trois dernières étapes — les **filtres avant la
temperature** — n'est pas celui des manuels, qui placent souvent l'inverse. Ce
que l'étape [sampling](../fondamentaux/sampling.md) mesure, c'est que le filtre
a le dernier mot sur la temperature ; l'ordre d'application dans le code du
moteur, lui, n'a pas été vérifié ici — une sortie déterministe ne suffit pas à
le discriminer, et il est parfois configurable. À lire dans sa propre
configuration avant d'en dépendre.

## Les étapes

| id | Étape | Ce qu'elle fait |
|---|---|---|
| `messages` | La liste de messages | l'état côté client, renvoyé en entier à chaque tour |
| `template` | Le template de chat | aplatit la liste en un texte unique et balisé |
| `tokenizer` | La tokenisation | découpe ce texte en unités du vocabulaire |
| `modele` | Le modèle | attention sur tout le passé, KV cache pour ne pas tout recalculer |
| `filtres` | top-k / top-p | taille la distribution des candidats |
| `temperature` | La temperature | règle le tranchant de ce qui reste |
| `tirage` | Le tirage | extrait un token, seul endroit où le hasard agit |

## Le fil

- `messages` → `template` : la liste à aplatir
- `template` → `tokenizer` : un texte unique et balisé
- `tokenizer` → `modele` : des entiers du vocabulaire
- `modele` → `filtres` : un logit par token du vocabulaire
- `filtres` → `temperature` : les candidats retenus
- `temperature` → `tirage` : la distribution tranchée
- `tirage` → `messages` : le token choisi, réinjecté — autorégression
