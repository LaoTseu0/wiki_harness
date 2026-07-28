---
id: unicode-octets
type: leçon
titre: Texte, Unicode et octets
parcours: 0-generation
statut: brouillon
tags: [generation, unicode, utf8]
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
processus: aucun — représentation fondamentale du texte
schema: representation-texte
element: point-code
brique: generation
contrat: aucun — prépare la frontière textuelle du tokenizer
---

# Texte, Unicode et octets

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-1--observer-les-frontières-du-texte)

## Prérequis

Aucun prérequis propre au cours.

## Savoir le situer

**Ensemble** — [[generator/guardrails/schema/references/representation-texte.canvas|carte de
concepts de la représentation du texte]]. Une arête indique une relation de
représentation. Elle n'indique pas une étape d'exécution.

**Élément ouvert** — `point-code`. Il relie le caractère abstrait, la valeur
scalaire encodable, la chaîne Python, le grapheme cluster et les octets produits
par UTF-8.

**L'essentiel** — un texte ne possède pas une frontière universelle appelée
« caractère ». Le point de code, l'octet, l'élément de `str`, le grapheme
cluster visible et le token sont des unités différentes.

**Recomposer** — le tokenizer reçoit une chaîne ou des octets selon son
contrat. Toute confusion en amont sur l'encodage ou les frontières modifie la
séquence de tokens et se propage jusqu'aux logits.

![[unicode-octets.canvas]]

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

## Reconstruction

Observer les représentations sans bibliothèque externe :

```python
import unicodedata

textes = {
    "précomposé": "é",
    "décomposé": "e\u0301",
    "famille": "👨‍👩‍👧‍👦",
}

for nom, texte in textes.items():
    points = [f"U+{ord(caractere):04X}" for caractere in texte]
    octets = texte.encode("utf-8")
    print(nom, len(texte), points, octets.hex(" "))

assert unicodedata.normalize("NFC", textes["précomposé"]) == unicodedata.normalize(
    "NFC", textes["décomposé"]
)
assert textes["précomposé"].encode("utf-8") != textes["décomposé"].encode("utf-8")
```

L'expérience isole trois faits : le rendu ne fixe pas la séquence de points de
code, `len(str)` ne compte pas les octets et une normalisation peut rendre deux
séquences égales sans qu'elles l'aient été au départ.

## Décision et dépôt dans Praxis

- **Décision** — les frontières textuelles de Praxis acceptent `str`. Une
  conversion en octets nomme explicitement UTF-8 et utilise le mode strict.
- **Alternatives** — accepter arbitrairement `str | bytes`, ou normaliser toutes
  les chaînes à l'entrée.
- **Critère** — conserver une représentation sans ambiguïté tout en laissant au
  contrat métier ou au tokenizer la décision de normaliser.
- **Coût accepté** — les frontières binaires doivent décoder explicitement
  avant d'entrer dans la génération.
- **Condition de révision** — une API de tokenizer qui exige réellement des
  octets recevra un adaptateur dédié.
- **Contrat** — aucun contrat public n'est déposé avant la leçon sur la
  tokenisation.
- **Invariant et tests** — aucune fonction ne déduit un nombre de tokens de
  `len(text)` ou de `len(text.encode("utf-8"))`.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — le nombre de grapheme clusters ; Python
  n'expose pas directement l'algorithme complet de segmentation Unicode.
- **Praxis ne garantit pas encore** — la tokenisation ni le rendu incrémental.
- **Échec provoqué** — décoder `b"\xc3"` en UTF-8 strict doit échouer tant que
  l'octet suivant n'est pas disponible.
- **Ouverture ultérieure** — [[02-tokenisation-vocabulaire|Tokenisation et
  vocabulaire]] puis [[15-detokenisation-fragments|Détokenisation
  incrémentale]].

## Se tester

1. Pourquoi deux chaînes visuellement identiques peuvent-elles consommer un
   nombre de tokens différent ?
2. Que perd une frontière qui décode des octets invalides avec
   `errors="ignore"` ?
3. Pourquoi `len("👨‍👩‍👧‍👦")` ne répond-il pas à la question « combien de
   caractères l'utilisateur voit-il ? »
4. Dans quel cas une normalisation Unicode systématique invaliderait-elle un
   contrat ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#01--texte-unicode-et-octets).

## Références

- [Unicode Standard 17.0, chapitre 3](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/) —
  définitions des points de code, valeurs scalaires, unités de code et UTF-8.
- [Unicode Standard 17.0, annexe UAX #29](https://www.unicode.org/reports/tr29/) —
  frontières des grapheme clusters.
- [Documentation Python 3.14 — `str`](https://docs.python.org/3.14/library/stdtypes.html#text-sequence-type-str) —
  représentation et opérations sur les chaînes.
- [Documentation Python 3.14 — `unicodedata`](https://docs.python.org/3.14/library/unicodedata.html) —
  propriétés et normalisation Unicode.

