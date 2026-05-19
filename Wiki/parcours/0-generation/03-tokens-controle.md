---
id: tokens-controle
type: leçon
titre: Tokens de contrôle
parcours: 0-generation
statut: brouillon
tags: [generation, tokenisation, special-tokens]
created: 2026-07-27
updated: 2026-07-28
verified: 2026-07-27
processus: generation-token
etape: tokenisation
brique: generation
contrat: praxis.generation.SpecialTokens
---

# Tokens de contrôle

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-3--identifier-les-tokens-de-contrôle)

## Prérequis

- [[02-tokenisation-vocabulaire|Tokenisation et vocabulaire]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : [[glossaire/template|Template]] de chat → tokenisation → inférence → sampling →
détokenisation → arrêt.

**Étape ouverte** — `chat-template → tokenisation → inference`.  
**Input** : texte sérialisé et politique de tokens spéciaux. **Output** : identifiants,
y compris les marqueurs attendus par le modèle.  
Responsabilité : distinguer le contenu des marqueurs réservés sans les ajouter
deux fois.

**L'essentiel** — un [[glossaire/token-de-controle|token de contrôle]] est une entrée réservée du vocabulaire.
Son identifiant ne produit un comportement particulier que si l'entraînement,
le **Template** ou la boucle de génération lui donne ce rôle.

**Recomposer** — les marqueurs de début, de rôle et de fin structurent la
séquence avant l'inférence. Les marqueurs de fin reviennent ensuite dans les
conditions d'arrêt.

![[tokens-controle.canvas]]

## Connaissances

### Réservé ne signifie pas magique

Un tokenizer peut déclarer des tokens spéciaux comme `bos_token`,
`eos_token`, `unk_token`, `pad_token` ou des tokens additionnels. Cette
déclaration permet de les reconnaître, de retrouver leurs identifiants et,
selon l'API, de les exclure du texte décodé.

Le modèle ne lit toutefois que des identifiants. Un token devient un marqueur
de début de séquence, de fin de tour ou de rôle parce que les données
d'entraînement et le runtime l'emploient ainsi. Inventer une chaîne
`<|assistant|>` dans un tokenizer qui ne la connaît pas ne crée pas un rôle.

### [[glossaire/bos|BOS]], [[glossaire/eos|EOS]] et fin de tour

- **BOS** marque éventuellement le début d'une séquence.
- **EOS** est un identifiant que la boucle peut traiter comme une fin de
  génération.
- **Fin de tour** sépare parfois deux messages sans signifier la fin absolue de
  toute conversation.

Ces rôles peuvent partager un identifiant ou utiliser des identifiants
distincts selon le modèle. Certains runtimes acceptent plusieurs identifiants
**EOS**. Aucun code générique ne doit supposer qu'il existe exactement un **BOS**, un
**EOS** ou un marqueur de fin de tour.

### [[glossaire/padding|Padding]] et token inconnu

Le **padding** aligne des séquences de longueurs différentes dans un batch. Le
masque d'attention doit empêcher les positions de remplissage de contribuer
comme du contenu. Réutiliser **EOS** comme **padding** peut être un choix de
configuration, mais il ne rend pas les deux concepts identiques.

Le token inconnu représente une unité que le tokenizer ne sait pas encoder.
Les tokenizers byte-level peuvent éviter ce cas pour une entrée encodable, mais
ce n'est pas une propriété de tous les tokenizers.

### L'ajout automatique peut dupliquer les marqueurs

Une API `encode(..., add_special_tokens=True)` peut exécuter un
post-processeur. Un **Template** de chat peut déjà émettre **BOS**, **EOS** ou des fins de
tour. Appliquer ensuite une seconde couche d'ajout automatique produit une
séquence différente de celle attendue.

La seule vérification fiable consiste à observer les identifiants finaux et à
les comparer au **Template** et à la configuration du tokenizer.

### Le contenu peut ressembler à un marqueur

Un tokenizer peut configurer un token réservé pour qu'une chaîne correspondante
soit reconnue comme une unité indivisible. Le comportement dépend de ses
options de normalisation et de découpage.

Cette reconnaissance n'est pas une barrière de sécurité. Si un utilisateur
écrit une chaîne qui ressemble à un délimiteur, seul le **Template** exact et
l'entraînement du modèle déterminent l'effet. La sécurité des instructions sera
traitée au Parcours 14.

## Reconstruction

Rendre les rôles explicites avec une configuration minimale :

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class SpecialTokens:
    bos_ids: tuple[int, ...]
    eos_ids: frozenset[int]
    pad_id: int | None
    role_ids: dict[str, int]

TOKENS = SpecialTokens(
    bos_ids=(1,),
    eos_ids=frozenset({2, 7}),
    pad_id=0,
    role_ids={"user": 10, "assistant": 11},
)

def est_fin(token_id: int, tokens: SpecialTokens) -> bool:
    return token_id in tokens.eos_ids

assert est_fin(7, TOKENS)
assert not est_fin(TOKENS.pad_id, TOKENS)
```

Les nombres sont ceux d'un vocabulaire fictif. L'expérience montre pourquoi le
runtime transporte des identifiants issus du tokenizer au lieu de constantes
globales supposées universelles.

## Décision et dépôt dans Praxis

- **Décision** — Praxis charge les identifiants spéciaux depuis l'artefact du
  tokenizer et les fige dans `SpecialTokens`.
- **Alternatives** — coder en dur les chaînes ou les identifiants ; laisser
  chaque boucle relire librement la configuration.
- **Critère** — une même politique doit être testable et liée à la révision du
  tokenizer.
- **Coût accepté** — la configuration représente des ensembles et des valeurs
  optionnelles plutôt qu'un unique `eos_id`.
- **Condition de révision** — les modèles multimodaux pourront ajouter des
  catégories de tokens réservés sans modifier la sémantique de **BOS** ou **EOS**.
- **Contrat** — `praxis.generation.SpecialTokens`.
- **Invariant et tests** — aucune valeur n'est inventée ; **padding** n'arrête pas
  la génération sauf configuration explicite ; les marqueurs ne sont ajoutés
  qu'une fois.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — que les identifiants fictifs ont été
  appris avec les rôles annoncés.
- **Praxis ne garantit pas encore** — le rendu exact d'une conversation.
- **Échec provoqué** — appliquer un **BOS** dans le **Template** puis un second **BOS** par
  le post-processeur doit être détecté par un test de séquence.
- **Ouverture ultérieure** — [[04-templates-chat|Le texte réellement lu par le
  modèle]] et [[16-conditions-arret|Borner la génération]].

## Se tester

1. Pourquoi une chaîne nommée `<eos>` n'arrête-t-elle pas nécessairement le
   modèle ?
2. Dans quel cas **EOS** et fin de tour doivent-ils rester distincts ?
3. Comment l'ajout automatique de tokens spéciaux peut-il corrompre un **Template**
   de chat pourtant correct ?
4. Pourquoi un token de **padding** doit-il être accompagné d'un masque ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#03--tokens-de-contrôle).

## Références

- [Transformers — Special tokens](https://huggingface.co/docs/transformers/main_classes/tokenizer#transformers.SpecialTokensMixin) —
  contrat des tokens spéciaux dans les tokenizers.
- [Transformers — `GenerationConfig`, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig) —
  **EOS** simple ou multiple, **BOS** et **padding** pendant la génération.
- [Transformers — Chat templates](https://huggingface.co/docs/transformers/chat_templating) —
  interaction entre **Template**, tokenisation et ajout de tokens spéciaux.

