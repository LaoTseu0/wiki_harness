## Connaissances

### Du caractère abstrait au point de code

Unicode attribue des points de code dans l'espace `U+0000` à `U+10FFFF`. Un
point de code est une position numérique. Un caractère abstrait est l'entité
textuelle à laquelle Unicode associe des propriétés et, généralement, un point
de code.

Les points de code des surrogates, de `U+D800` à `U+DFFF`, servent à UTF-16.
Ils ne sont pas des valeurs scalaires Unicode. Une valeur scalaire est donc un
point de code hors de cette plage.

Python expose une chaîne `str` comme une séquence de points de code. Cette
représentation n'est pas une séquence UTF-8 en mémoire au sens de l'API : le
passage vers des octets est une opération explicite avec `encode()`.

### Un symbole visible peut contenir plusieurs points de code

Le texte `é` peut être représenté par le point de code précomposé `U+00E9` ou
par la séquence `U+0065 U+0301`, lettre `e` suivie d'un accent combinant. Les
deux séquences peuvent avoir le même rendu tout en donnant des longueurs, des
octets et des tokenisations différents.

Un grapheme cluster étendu correspond approximativement à l'unité que
l'utilisateur perçoit comme un caractère. Un emoji composé avec des modificateurs
ou des caractères de jointure peut réunir plusieurs points de code dans un seul
grapheme cluster. `len(text)` ne compte donc ni les octets, ni nécessairement
les symboles perçus.

La normalisation Unicode transforme certaines séquences équivalentes vers une
forme choisie, comme NFC ou NFD. Elle n'est pas une opération neutre à appliquer
partout : elle change la séquence de points de code et peut modifier un
identifiant, une signature ou la tokenisation.

### UTF-8 produit des octets

UTF-8 associe chaque valeur scalaire à une séquence de un à quatre octets. Les
points de code ASCII utilisent un octet. `U+00E9` utilise les deux octets
hexadécimaux `C3 A9`. Un octet de continuation isolé n'a pas de signification
textuelle valide.

Le décodage doit définir son comportement devant une séquence mal formée :
refus strict, remplacement, ignorance ou stratégie spécialisée. Remplacer
silencieusement un octet invalide par `U+FFFD` perd l'information d'origine ;
ce choix ne convient pas à une frontière qui doit être reproductible.

### Le token est encore une autre unité

Un tokenizer peut opérer sur des caractères, des sous-mots ou une
représentation byte-level. Même lorsqu'il part d'octets, un token peut contenir
un octet, plusieurs octets ou un fragment qui ne forme pas seul une chaîne
UTF-8 complète.

Il n'existe donc aucune conversion générale :

```text
1 caractère visible = 1 point de code = 1 octet = 1 token
```

Chacune de ces égalités peut être fausse. Le comptage de tokens exige le
tokenizer exact du modèle.
