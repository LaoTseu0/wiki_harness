---
id: tokenisation-vocabulaire
type: leçon
titre: Tokenisation et vocabulaire
parcours: 0-generation
statut: brouillon
tags: [generation, tokenisation, bpe, sentencepiece]
created: 2026-07-27
updated: 2026-07-28
verified: 2026-07-27
processus: generation-token
etape: tokenisation
brique: generation
contrat: praxis.generation.Tokenizer
---

# Tokenisation et vocabulaire

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-2--ouvrir-le-tokenizer)

## Prérequis

- [[01-unicode-octets|Texte, Unicode et octets]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : Template de chat → tokenisation → inférence → transformation
des logits → sampling → boucle et arrêt.

**Étape ouverte** — `chat-template → tokenisation → inference`.  
**Input** : texte sérialisé. **Output** : identifiants du [[glossaire/vocabulaire|vocabulaire]].  
Responsabilité : appliquer les règles exactes du [[glossaire/tokenizer|tokenizer]] associé au modèle.

**L'essentiel** — le **tokenizer** transforme une séquence textuelle en
identifiants discrets. Son **vocabulaire**, sa normalisation, son pré-découpage et
son algorithme font partie du contrat du modèle.

**Recomposer** — changer de **tokenizer** change les identifiants envoyés à la
table d'embeddings. Même si le texte affiché reste identique, le modèle reçoit
alors une autre entrée.

![[tokenisation-vocabulaire.canvas]]

## Connaissances

### Le pipeline d'un **tokenizer**

Un **tokenizer** industriel peut enchaîner plusieurs mécanismes :

1. une normalisation éventuelle ;
2. un pré-**tokenizer** qui trouve des frontières candidates ;
3. un modèle de segmentation, par exemple [[glossaire/bpe|BPE]] ou Unigram ;
4. une correspondance entre unités et identifiants ;
5. un post-traitement qui ajoute éventuellement des [[glossaire/token|tokens]] spéciaux.

Réduire la tokenisation à `texte.split(" ")` perd la ponctuation, les espaces,
les langues sans séparateurs et la possibilité de représenter les mots absents
du **vocabulaire**.

### Le **vocabulaire**

Le **vocabulaire** est une correspondance finie entre des unités tokenisées et des
entiers. L'identifiant n'a pas de sens universel : `42` ne désigne pas le même
**token** dans deux **vocabulaires** différents. Les poids d'embedding ont été appris
avec une correspondance précise ; permuter deux identifiants sans permuter les
poids change le modèle.

La taille du **vocabulaire** règle un compromis. Un grand **vocabulaire** peut
représenter davantage de fragments fréquents avec peu de **tokens**, mais agrandit
la table d'embeddings et la projection de sortie. Un petit **vocabulaire** réduit
ces matrices, mais allonge les séquences.

### **BPE**

Le Byte Pair Encoding adapté aux sous-mots part d'unités de base et apprend des
fusions sur un corpus. À chaque itération d'entraînement, une paire adjacente
fréquente devient une nouvelle unité. Le **vocabulaire** final réunit les unités de
base et les unités apprises.

À l'encodage, le **tokenizer** applique les règles apprises et leur priorité. Il ne
recalcule pas les fréquences sur le texte de l'utilisateur. Deux **tokenizers**
**BPE** peuvent donc produire des segmentations différentes avec le même texte.

Une variante byte-level part des 256 valeurs d'octet, généralement rendues sous
une forme interne imprimable. Cette base peut représenter toute chaîne d'octets
sans **token** inconnu, mais elle permet aussi qu'un **token** isolé corresponde à un
fragment UTF-8 incomplet.

### [[glossaire/sentencepiece|SentencePiece]] n'est pas un synonyme de **BPE**

**SentencePiece** est une bibliothèque et un format d'entraînement applicables
directement au texte brut. Elle peut utiliser **BPE** ou un modèle Unigram. Elle
représente notamment l'espace par un symbole interne, souvent `▁`, afin que la
segmentation ne dépende pas d'un découpage préalable en mots.

Dire qu'un modèle « utilise **SentencePiece** » ne suffit donc pas pour déduire son
algorithme, sa normalisation, son traitement des octets inconnus ou son
**vocabulaire**. Il faut inspecter les artefacts du **tokenizer**.

### Encodage, décodage et aller-retour

`decode(encode(text)) == text` est une propriété souhaitable, mais elle dépend
des normalisations et des options de nettoyage. Un **tokenizer** qui normalise
avant la segmentation peut produire un texte canonique différent de l'original.

Le décodage d'un **token** isolé n'est pas nécessairement un inverse local de
l'encodage. Certaines règles reconstituent les espaces ou accumulent plusieurs
fragments byte-level. L'aller-retour se vérifie sur une séquence complète et
avec des options explicites.

## Reconstruction

Apprendre un **BPE** miniature sur un corpus volontairement réduit :

```python
from collections import Counter

corpus = {
    tuple("bas") + ("</w>",): 5,
    tuple("basse") + ("</w>",): 3,
    tuple("base") + ("</w>",): 4,
}

def paires(mots: dict[tuple[str, ...], int]) -> Counter[tuple[str, str]]:
    resultat: Counter[tuple[str, str]] = Counter()
    for symboles, frequence in mots.items():
        resultat.update(
            {paire: frequence for paire in zip(symboles, symboles[1:])}
        )
    return resultat

def fusionner(
    mots: dict[tuple[str, ...], int], paire: tuple[str, str]
) -> dict[tuple[str, ...], int]:
    fusion = "".join(paire)
    resultat = {}
    for symboles, frequence in mots.items():
        nouveaux = []
        index = 0
        while index < len(symboles):
            if tuple(symboles[index:index + 2]) == paire:
                nouveaux.append(fusion)
                index += 2
            else:
                nouveaux.append(symboles[index])
                index += 1
        resultat[tuple(nouveaux)] = frequence
    return resultat

for _ in range(4):
    paire, _ = paires(corpus).most_common(1)[0]
    print("fusion", paire)
    corpus = fusionner(corpus, paire)
```

Cette reconstruction montre l'apprentissage des fusions. Elle ne reproduit ni
le pré-**tokenizer**, ni les optimisations, ni toutes les règles d'égalité d'un
**tokenizer** de production.

## Décision et dépôt dans Praxis

- **Décision** — `Tokenizer` expose `encode`, `decode`, `count` et son identité
  reproductible. Praxis adapte le **tokenizer** fourni avec le modèle.
- **Alternatives** — un **tokenizer** unique pour tous les modèles, ou des appels
  directs à une bibliothèque dans toute la base de code.
- **Critère** — les identifiants doivent rester compatibles avec les poids du
  modèle et les appels doivent être testables sans dépendre d'une classe
  concrète.
- **Coût accepté** — l'adaptateur conserve les options exactes et refuse les
  conversions implicites.
- **Condition de révision** — des modalités non textuelles pourront étendre le
  contrat avec un `Processor` au Parcours 15.
- **Contrat** — `praxis.generation.Tokenizer`.
- **Invariant et tests** — un **tokenizer** est associé à une révision
  d'artefacts ; le comptage utilise `encode` ; les tests couvrent espaces,
  accents composés, emoji, code et **tokens** spéciaux.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — qu'un **BPE** miniature produit une
  segmentation utile pour un modèle entraîné.
- **Praxis ne garantit pas encore** — la compatibilité du Template de chat ou
  le traitement des **tokens** spéciaux.
- **Échec provoqué** — encoder avec le **tokenizer** d'un autre [[glossaire/checkpoint|checkpoint]] doit
  être considéré comme une incompatibilité, même si la taille du **vocabulaire**
  coïncide.
- **Ouverture ultérieure** — [[03-tokens-controle|Tokens de contrôle]] et
  [[04-templates-chat|Template de chat]].

## Se tester

1. Pourquoi l'identifiant de **token** `42` ne peut-il pas être stocké sans
   identifier aussi le **tokenizer** ?
2. Quelle différence sépare l'apprentissage **BPE** de l'encodage d'un nouveau
   texte ?
3. Un **tokenizer** byte-level garantit-il qu'un **token** isolé est du texte UTF-8
   affichable ?
4. Pourquoi « **SentencePiece** » ne permet-il pas à lui seul de connaître la
   segmentation utilisée ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#02--tokenisation-et-vocabulaire).

## Références

- [Sennrich et al., *Neural Machine Translation of Rare Words with Subword
  Units*, v5](https://arxiv.org/abs/1508.07909) — adaptation de **BPE** aux
  sous-mots.
- [Kudo et Richardson, *SentencePiece*, v1](https://arxiv.org/abs/1808.06226) —
  entraînement depuis le texte brut et modèles **BPE** ou Unigram.
- [Transformers — Tokenization algorithms, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/main/tokenizer_summary) —
  pipeline et comparaison des familles de **tokenizers**.
- [Tokenizers — composants](https://huggingface.co/docs/tokenizers/components) —
  normalizer, pre-**tokenizer**, model, post-processor et decoder.
