---
id: templates-chat
type: leçon
titre: Le texte réellement lu par le modèle
parcours: 0-generation
statut: brouillon
tags: [generation, chat-template, messages]
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
processus: generation-token
etape: chat-template
brique: generation
contrat: praxis.generation.ChatTemplate
---

# Le texte réellement lu par le modèle

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-4--rendre-le-template-de-chat)

## Prérequis

- [[02-tokenisation-vocabulaire|Tokenisation et vocabulaire]]
- [[03-tokens-controle|Tokens de contrôle]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : messages → Template de chat → tokenisation → inférence →
boucle.

**Étape ouverte** — `messages → chat-template → tokenisation`.  
Input : une liste ordonnée de messages et les options du tour. Output : une
séquence sérialisée ou directement tokenisée.  
Responsabilité : reproduire exactement le format appris par le modèle.

**L'essentiel** — un modèle decoder-only ne reçoit pas une liste de messages.
Le Template transforme les rôles et contenus en une séquence unique où les
délimiteurs, espaces et tokens de contrôle font partie de l'entrée.

**Recomposer** — le texte produit devient l'Input du tokenizer. Une différence
de Template change tous les identifiants à partir de son premier écart et donc
la trajectoire de génération.

![[templates-chat.canvas]]

## Connaissances

### Les messages sont une structure applicative

Une interface de chat manipule des objets tels que :

```python
[
    {"role": "system", "content": "Réponds brièvement."},
    {"role": "user", "content": "État du serveur ?"},
]
```

Le Transformer decoder-only reçoit une séquence d'identifiants. Le Template
doit donc encoder l'ordre, les rôles, les frontières de messages et le point où
une réponse est attendue.

Deux modèles entraînés avec des formats différents peuvent employer les mêmes
noms de rôles tout en exigeant des séquences incompatibles. Un Template n'est
pas interchangeable parce qu'il « ressemble » à ChatML ou à une autre
convention.

### Le moindre séparateur fait partie du prompt

Un retour à la ligne, un espace ou un token de fin de tour modifie le texte puis
la tokenisation. Les espaces ajoutés par un moteur de Template ne sont pas une
question esthétique. Ils deviennent des données du modèle.

Dans Transformers, le Template est généralement une expression Jinja associée
au tokenizer. `apply_chat_template()` reçoit notamment `messages` et
`add_generation_prompt`. Les tokens déclarés dans la carte des tokens spéciaux
sont accessibles au Template.

### Ouvrir un nouveau tour ou continuer le dernier

`add_generation_prompt=True` demande au Template d'ajouter, lorsqu'il en
possède un, le préfixe qui annonce un nouveau message assistant. Certains
Templates n'en ont pas besoin ; l'option peut alors ne rien changer.

Continuer un message assistant déjà commencé est un autre contrat. Ajouter le
préfixe d'un nouveau tour dans ce cas sépare le préremplissage de sa suite.
Les API distinguent donc l'ouverture d'un nouveau message et la continuation du
dernier message.

### Sérialiser puis tokeniser sans double ajout

Deux chemins doivent être comparés :

```python
ids_directs = tokenizer.apply_chat_template(messages, tokenize=True)
texte = tokenizer.apply_chat_template(messages, tokenize=False)
ids_separes = tokenizer.encode(texte, add_special_tokens=False)
```

Si le Template contient déjà les marqueurs requis, la seconde tokenisation
désactive leur ajout automatique. Le contrat utile est l'égalité des
identifiants finaux, pas seulement l'égalité de deux chaînes affichées.

### Un Template ne protège pas les instructions

Les délimiteurs aident le modèle à reconnaître les rôles appris. Ils ne
constituent pas une séparation de privilèges comparable à celle d'un processus
ou d'une sandbox. Le contenu utilisateur reste dans le contexte du modèle et
peut tenter d'influencer son comportement.

Praxis conserve donc le rôle comme métadonnée en dehors du texte sérialisé.
Les politiques d'autorisation ne lisent jamais le texte généré comme une preuve
d'autorité.

## Reconstruction

Rendre visible la sérialisation avec un Template jouet :

```python
ROLE = {
    "system": "<|system|>",
    "user": "<|user|>",
    "assistant": "<|assistant|>",
}
FIN_TOUR = "<|end|>"

def rendre(messages: list[dict[str, str]], *, ouvrir_assistant: bool) -> str:
    morceaux = []
    for message in messages:
        morceaux.extend(
            [ROLE[message["role"]], "\n", message["content"], FIN_TOUR, "\n"]
        )
    if ouvrir_assistant:
        morceaux.extend([ROLE["assistant"], "\n"])
    return "".join(morceaux)
```

Afficher `repr(rendre(...))` rend les retours à la ligne et les espaces
observables. Encoder ensuite cette valeur avec un vrai tokenizer montre que
toute variation de sérialisation modifie les identifiants.

## Décision et dépôt dans Praxis

- **Décision** — `ChatTemplate` transforme des messages typés en identifiants en
  passant par le Template livré avec le tokenizer.
- **Alternatives** — maintenir un Template global Praxis ; laisser chaque
  appelant concaténer les messages.
- **Critère** — la séquence doit rester compatible avec le checkpoint et
  reproductible à partir de ses artefacts.
- **Coût accepté** — Praxis conserve l'identité et la révision du Template dans
  les traces de génération.
- **Condition de révision** — un modèle sans Template fourni exige un adaptateur
  explicitement configuré et testé sur son format d'entraînement.
- **Contrat** — `praxis.generation.ChatTemplate`.
- **Invariant et tests** — ordre des messages préservé ; rôle inconnu refusé ;
  rendu déterministe ; aucune duplication de BOS/EOS ; égalité entre la voie
  directe et la voie texte puis tokenisation.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — que le Template jouet correspond à un
  modèle réel.
- **Praxis ne garantit pas encore** — que le modèle suivra le rôle déclaré.
- **Échec provoqué** — ajouter ou retirer un retour à la ligne doit modifier la
  séquence et faire échouer un test snapshot des identifiants.
- **Ouverture ultérieure** — le Parcours 2 normalisera les capacités des
  fournisseurs ; le Parcours 14 ouvrira la frontière de confiance.

## Se tester

1. Pourquoi deux listes de messages identiques peuvent-elles produire des
   générations différentes avec deux checkpoints ?
2. Quelle erreur produit l'enchaînement `apply_chat_template(tokenize=False)`
   puis `encode(add_special_tokens=True)` lorsque le Template contient déjà
   BOS ?
3. Quelle différence sémantique sépare l'ouverture d'un tour assistant et la
   continuation d'un message assistant ?
4. Pourquoi le rôle `system` ne doit-il pas être utilisé par la politique
   d'autorisation comme une preuve de privilège ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#04--le-texte-réellement-lu-par-le-modèle).

## Références

- [Transformers — Writing a chat template, documentation vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/en/chat_templating_writing) —
  variables, tokens spéciaux et contrôle des espaces.
- [Transformers — Chat templates](https://huggingface.co/docs/transformers/chat_templating) —
  `add_generation_prompt`, continuation et tokenisation.
- [Model card SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) —
  exemple concret de Template appliqué avant la génération locale.

