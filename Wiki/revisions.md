# Réviser le parcours

Chaque question propose un calcul ou une situation à examiner. Déplie la réponse
pour vérifier ton raisonnement, puis retrouve la leçon en suivant son lien.

## Octets et caractères

Combien d’octets UTF-8 faut-il pour « A€B » ?

<details>
<summary>Réponse</summary>

Cinq. A et B occupent chacun un octet. Le signe € en occupe trois.

</details>

[Texte, Unicode et octets](parcours/0-generation/01-unicode-octets.md#connaissances)

## Ordre des fusions

Avec les unités a, b, c, on applique d’abord la fusion de b et c. Peut-on encore
fusionner a et b au pas suivant ?

<details>
<summary>Réponse</summary>

Les unités restantes sont a et bc. La paire a, b a disparu et il faudrait une règle
portant sur a et bc.

</details>

[Tokenisation et vocabulaire](parcours/0-generation/02-tokenisation-vocabulaire.md#connaissances)

## Marqueurs de contrôle

Un encodeur ajoute BOS devant une séquence qui commence déjà par BOS. Que faut-il
comparer pour repérer l’erreur ?

<details>
<summary>Réponse</summary>

Comparer la liste d’identifiants produite à la séquence attendue par le modèle. Les
deux premiers identifiants peuvent être identiques même si aucun marqueur n’apparaît à
l’écran.

</details>

[Tokens de contrôle](parcours/0-generation/03-tokens-controle.md#connaissances)

## Tours de conversation

Deux prompts affichent les mêmes mots. L’un contient un retour à la ligne de plus
devant le tour assistant. Comment vérifier si l’entrée du modèle change ?

<details>
<summary>Réponse</summary>

Appliquer le tokenizer prévu et comparer les séquences d’identifiants, en conservant
les marqueurs spéciaux.

</details>

[Le texte réellement lu par le modèle](parcours/0-generation/04-templates-chat.md#connaissances)

## Dimensions des embeddings

Une table contient 80 lignes de 6 valeurs. Quelle forme obtient-on en sélectionnant
les lignes 3, 7 et 3 ?

<details>
<summary>Réponse</summary>

Trois lignes de six valeurs. Avant l’ajout d’informations de contexte ou de position,
la première et la dernière sélectionnent le même vecteur.

</details>

[Embeddings de tokens](parcours/0-generation/05-embeddings-tokens.md#connaissances)

## Rotation de position

Sur une paire de composantes, que devient (1, 0) après une rotation positive d’un
quart de tour ?

<details>
<summary>Réponse</summary>

Elle devient (0, 1). La direction change et la norme reste égale à 1.

</details>

[Représenter la position](parcours/0-generation/06-position-rope.md#connaissances)

## Accès aux positions

Dans une séquence de quatre positions numérotées à partir de 1, quelles positions la
troisième peut-elle consulter en attention causale complète ?

<details>
<summary>Réponse</summary>

Les positions 1, 2 et 3. La quatrième doit être masquée avant la normalisation des
scores.

</details>

[L'attention causale](parcours/0-generation/07-attention-causale.md#connaissances)

## Chemin résiduel

Dans un bloc pré-norm simplifié, que devient x si le sous-bloc renvoie le vecteur nul
?

<details>
<summary>Réponse</summary>

La sortie vaut x, puisque l’addition résiduelle donne x + 0.

</details>

[Residual stream et normalisation](parcours/0-generation/08-residual-normalisation.md#connaissances)
