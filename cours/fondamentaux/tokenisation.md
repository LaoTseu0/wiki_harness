# Tokenisation

> [carte du cours](../carte.md) · étape : [`09_tokens.py`](../../etapes/fondamentaux/09_tokens.py)

## L'essentiel

Le modèle ne lit pas des caractères, il lit des **tokens** : des morceaux
de texte tirés d'un vocabulaire figé à l'entraînement. Tout ce que les
leçons précédentes plafonnent, tronquent ou facturent — `num_predict`, la
fenêtre de contexte, le coût d'un appel — se compte dans cette unité-là,
pas en mots ni en caractères. Tant qu'on ne l'a pas mesurée sur ses
propres textes, on raisonne sur une unité qu'on ne connaît pas.

## Le savoir

**Un vocabulaire, pas un dictionnaire.** Le tokenizer découpe le texte en
unités issues d'un vocabulaire construit une fois pour toutes (~150 000
entrées pour Qwen). Ces unités ne sont ni des lettres ni des mots : ce
sont les **séquences les plus fréquentes du corpus d'entraînement**. Un
mot courant tient souvent en un token, espace initial compris ; un mot
rare se fragmente.

**BPE, en une phrase.** L'algorithme (Byte Pair Encoding) part des octets
et fusionne itérativement la paire la plus fréquente du corpus, jusqu'à
atteindre la taille de vocabulaire visée. Conséquence directe : *la
fréquence dans le corpus d'entraînement décide du prix*. Ce qui était
fréquent est compact, ce qui était rare est cher.

**Pourquoi le français coûte plus que l'anglais.** Les corpus sont
majoritairement anglophones : les fusions apprises servent l'anglais. Le
français hérite de fragments plus courts, donc de plus de tokens pour dire
la même chose. Les caractères accentués aggravent le phénomène — hors ASCII,
ils occupent plusieurs octets en UTF-8 et n'apparaissent dans des fusions
que s'ils étaient assez fréquents.

**Ce que ça change concrètement.** Une fenêtre de contexte de 8 192 tokens
n'est pas la même quantité de texte selon qu'on y met de l'anglais, du
français accentué, du YAML ou du code. Le budget se mesure, il ne
s'estime pas.

**Le compteur est indirect.** Ollama n'expose pas d'endpoint de
tokenisation. Mais chaque réponse contient `prompt_eval_count` : le nombre
de tokens lus en entrée — déjà croisé au [chat](chat-historique-contexte.md)
quand le contexte gonflait à chaque tour. C'est l'instrument disponible,
à condition de neutraliser son biais (voir Pièges).

## En pratique

[09_tokens.py](../../etapes/fondamentaux/09_tokens.py) : un banc de paires
opposées — anglais/français, avec/sans accents, YAML/prose équivalente,
mot rare, emoji — mesurées en caractères par token.

**À prédire avant de lancer** (c'est le vrai exercice) : classe les huit
entrées du banc de la plus dense à la moins dense, puis confronte. Les
questions auxquelles ta mesure doit répondre :

- combien de tokens coûte le seul fait d'ouvrir une conversation, sans
  aucun contenu ?
- l'écart français/anglais, en pourcentage ?
- retirer les accents fait-il gagner des tokens, et assez pour justifier
  la convention « commentaires sans accents » du repo ?
- le YAML est-il plus dense ou moins dense que la prose qui dit la même
  chose ? *(l'indentation et les sauts de ligne sont du texte, eux aussi)*

## Pièges connus

- **`prompt_eval_count` ne compte pas que ton texte** : il inclut les
  balises du [template de chat](template-de-chat.md). Sans mesure à blanc
  (message vide) pour isoler ce surcoût fixe, tous les ratios sont faux —
  et d'autant plus faux que le texte mesuré est court.
- **Un ratio n'est pas transportable** : il vaut pour *ce* tokenizer. Un
  autre modèle, une autre famille, d'autres chiffres. C'est une raison de
  plus de mesurer plutôt que de citer.
- **Le cache de contexte d'Ollama** peut fausser des mesures répétées :
  varier les textes plutôt que rejouer le même.

## Se tester

- Pourquoi « anticonstitutionnellement » coûte-t-il plus cher que
  « le », alors que les deux sont des mots français corrects ?
- On te donne un budget de 4 000 tokens de contexte pour de la doc
  technique en français. Comment estimes-tu, *sans deviner*, combien de
  fichiers y tiennent ?
- Un utilisateur se plaint que sa question « coûte » deux fois plus que
  celle de son collègue anglophone, à longueur de texte égale. Que lui
  réponds-tu, et qu'est-ce que tu vérifies d'abord ?

## Références

- Tiktokenizer ou le playground de tokenizer de Hugging Face — voir le
  découpage en direct sur ses propres phrases
- La doc du tokenizer du modèle utilisé (`/api/show` en expose les
  paramètres)
