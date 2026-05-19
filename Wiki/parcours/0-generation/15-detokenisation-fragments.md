---
id: detokenisation-fragments
type: leçon
titre: Reconstruire le texte généré
parcours: 0-generation
statut: brouillon
tags: [generation, detokenisation, streaming, utf8]
created: 2026-07-27
updated: 2026-07-28
verified: 2026-07-27
processus: generation-token
etape: detokenisation
brique: generation
contrat: praxis.generation.TokenDecoder
---

# Reconstruire le texte généré

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-15--décoder-un-flux-sans-le-corrompre)

## Prérequis

- [[01-unicode-octets|Texte, Unicode et octets]]
- [[02-tokenisation-vocabulaire|Tokenisation et vocabulaire]]
- [[14-boucle-autoregressive|Réinjecter le token choisi]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : sampling → ajout du [[glossaire/token|token]] → [[glossaire/detokenisation|détokenisation]] → arrêt ou
réinjection.

**Étape ouverte** —
`ajout-token → detokenisation → condition-arret`.  
**Input** : nouvel identifiant et état du décodeur. **Output** : zéro ou plusieurs
caractères sûrs à accumuler.  
Responsabilité : reconstruire le texte sans supposer qu'un **token** est une unité
[[glossaire/utf-8|UTF-8]] ou un fragment concaténable.

**L'essentiel** — le décodage est une opération sur la séquence et peut porter
un état. Un **token** byte-level isolé peut finir au milieu d'un caractère ; le
stream ne doit émettre que le préfixe textuel définitivement décodable.

**Recomposer** — le texte accumulé alimente l'affichage et les stop sequences.
Les identifiants restent parallèlement la source de vérité pour la réinjection
et les arrêts par **token**.

![[detokenisation-fragments.canvas]]

## Connaissances

### Le **token** n'est pas sa chaîne d'affichage

Les interfaces d'inspection montrent souvent une représentation lisible d'un
**token**. Cette représentation peut échapper des octets, remplacer les espaces par
un symbole ou afficher un **token** spécial. La concaténer n'est pas
nécessairement l'algorithme de décodage.

Le décodeur du tokenizer connaît les conventions du modèle : fusion des
sous-mots, restauration des espaces, byte fallback, **tokens** spéciaux et options
de nettoyage.

### Un fragment **UTF-8** peut être incomplet

Le caractère `é` précomposé s'encode en `C3 A9`. Si deux **tokens** ou deux
fragments transportent séparément `C3` puis `A9`, le premier octet ne peut pas
être décodé seul en mode strict.

Le bon comportement consiste à conserver l'octet incomplet, attendre la suite
et n'émettre `é` qu'après réception de la séquence valide. Remplacer
immédiatement `C3` par `�` rend la corruption irréversible.

### Décodage incrémental

Un décodeur incrémental conserve l'état nécessaire entre les appels. Pour
**UTF-8**, cet état comprend notamment les octets de fin encore incomplets. Quand
`final=True`, toute séquence incomplète restante devient une erreur selon la
politique configurée.

Un tokenizer peut avoir une logique supplémentaire au-dessus d'**UTF-8**. Le
contrat général de Praxis ne doit donc pas exposer uniquement
`bytes.decode("utf-8")`.

### Deux stratégies pour streamer

1. utiliser l'API de décodage incrémental du tokenizer ;
2. redécoder la séquence cumulée et n'émettre que le suffixe nouvellement
   stabilisé.

La seconde stratégie est plus coûteuse et demande de gérer les corrections de
frontière ou de nettoyage. Elle reste préférable à `decode([token])` puis
concaténation lorsque le tokenizer n'offre pas de stream.

### **Tokens** spéciaux et texte visible

`skip_special_tokens=True` peut masquer BOS, EOS ou des marqueurs de rôle.
Cette option convient souvent à l'affichage, mais elle perd des informations de
contrôle. Praxis conserve séparément :

- les identifiants complets ;
- les fragments visibles ;
- les événements de contrôle.

Un EOS peut ainsi arrêter la boucle sans apparaître dans le texte rendu.

### [[glossaire/buffer|Buffer]] de sortie

Le fragment décodable n'est pas forcément immédiatement publiable. Une stop
sequence peut commencer à sa fin. La politique d'arrêt peut retenir un petit
suffixe ambigu jusqu'à savoir s'il appartient au texte ou au marqueur d'arrêt.

Le décodeur produit du texte valide ; la politique de publication décide ce qui
peut sortir vers l'utilisateur.

## Reconstruction

Le décodeur **UTF-8** incrémental de Python :

```python
import codecs

decodeur = codecs.getincrementaldecoder("utf-8")(errors="strict")

assert decodeur.decode(bytes.fromhex("c3"), final=False) == ""
assert decodeur.decode(bytes.fromhex("a9"), final=False) == "é"
assert decodeur.decode(b"", final=True) == ""
```

Une variante doit fournir seulement `C3`, puis appeler `final=True` : le mode
strict signale alors que le flux se termine au milieu d'une séquence.

## Décision et dépôt dans Praxis

- **Décision** — `TokenDecoder` reçoit les identifiants dans l'ordre et renvoie
  des fragments textuels stabilisés plus des événements de contrôle.
- **Alternatives** — décoder chaque **token** séparément ; redécoder toute la
  séquence à chaque tour sans contrat de stabilité.
- **Critère** — ne jamais produire de texte invalide ni perdre les identifiants
  nécessaires au contrôle.
- **Coût accepté** — un petit état de décodage et éventuellement un suffixe
  retenu.
- **Condition de révision** — le [[glossaire/streaming|streaming]] multimodal ajoutera d'autres types de
  fragments au Parcours 15.
- **Contrat** — `praxis.generation.TokenDecoder`.
- **Invariant et tests** — concaténer les fragments émis donne le même texte que
  le décodage complet, avec les mêmes options ; aucun `�` n'est inventé en mode
  strict.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — le comportement du décodeur d'un
  tokenizer SentencePiece ou byte-level particulier.
- **Praxis ne garantit pas encore** — que chaque fragment décodable est déjà
  publiable devant une stop sequence.
- **Échec provoqué** — finaliser un flux au milieu d'un caractère doit produire
  une erreur typée.
- **Ouverture ultérieure** — [[16-conditions-arret|Borner la génération]] et le
  Parcours 2 pour le **streaming** de transport.

## Se tester

1. Pourquoi `decode([token_id])` puis concaténation peut-il différer de
   `decode(token_ids)` ?
2. Que doit faire le décodeur lorsqu'il reçoit seulement l'octet `C3` ?
3. Pourquoi conserver les identifiants après avoir produit le texte ?
4. Quelle frontière sépare un fragment décodable d'un fragment publiable ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#15--reconstruire-le-texte-généré).

## Références

- [Unicode Standard 17.0, chapitre 3](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/) —
  séquences **UTF-8** bien formées.
- [Python 3.14 — codecs incrémentaux](https://docs.python.org/3.14/library/codecs.html#incremental-encoding-and-decoding) —
  état, `final` et équivalence avec le décodage complet.
- [Tokenizers — decoders](https://huggingface.co/docs/tokenizers/api/decoders) —
  décodeurs BPE, ByteLevel, Metaspace et ByteFallback.
- [Transformers — streamers](https://huggingface.co/docs/transformers/internal/generation_utils#streamers) —
  interfaces de rendu progressif à comparer.

