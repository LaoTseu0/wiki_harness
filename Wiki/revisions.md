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
