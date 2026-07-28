---
id: conditions-arret
type: leçon
titre: Borner la génération
parcours: 0-generation
statut: brouillon
tags: [generation, stop, eos, budgets]
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
processus: generation-token
etape: condition-arret
brique: generation
contrat: praxis.generation.StopPolicy
---

# Borner la génération

> [Cartographie](../../../generator/guardrails/parcours/cartographie.md) ·
> [Laboratoire du Parcours 0](../../cas-pratique/0-generation/00-laboratoire-generation.md#expérience-16--provoquer-chaque-raison-darrêt)

## Prérequis

- [[03-tokens-controle|Tokens de contrôle]]
- [[14-boucle-autoregressive|Réinjecter le token choisi]]
- [[15-detokenisation-fragments|Reconstruire le texte généré]]

## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : ajout → détokenisation → décision d'arrêt → réponse ou
réinjection.

**Étape ouverte** —
`detokenisation → condition-arret → reponse | reinjection`.  
Input : token choisi, texte stabilisé, compteurs et signaux externes. Output :
décision `continuer` ou raison d'arrêt typée.  
Responsabilité : terminer toujours la boucle selon une priorité documentée et
sans publier un marqueur exclu.

**L'essentiel** — EOS, stop sequence et budget de sortie sont des mécanismes
différents. Une génération bornée possède au moins une limite dure indépendante
de la bonne volonté du modèle.

**Recomposer** — `continuer` réinjecte la séquence. Toute autre décision ferme
le décodeur, publie le suffixe autorisé et produit avec la réponse une raison
d'arrêt exploitable.

![[conditions-arret.canvas]]

## Connaissances

### EOS

EOS est un identifiant de vocabulaire choisi comme les autres. La politique
d'arrêt compare l'identifiant produit à un ensemble configuré. Elle peut
exclure ce token du texte visible tout en le conservant dans la trajectoire.

Forcer EOS lorsque le budget est atteint n'est pas équivalent à observer un EOS
spontané : le premier est une intervention du runtime, le second un choix du
modèle. Les raisons doivent rester distinctes.

### Stop sequences

Une stop sequence est une chaîne ou une séquence d'octets recherchée dans la
sortie reconstruite. Elle peut :

- traverser plusieurs tokens ;
- partager un préfixe avec une autre stop sequence ;
- commencer à la fin du dernier fragment reçu ;
- apparaître dans un token qui contient aussi du texte antérieur.

La publication doit donc retenir le suffixe qui pourrait encore devenir un
marqueur. Si le contrat exclut la stop sequence de la réponse, elle ne doit pas
avoir été streamée avant sa reconnaissance.

Une correspondance sur la chaîne décodée et une correspondance sur les
identifiants ne sont pas équivalentes. Plusieurs tokenisations peuvent parfois
former le même texte.

### Budget de sortie

`max_new_tokens` compte les tokens produits après le prompt. Il se distingue
d'une longueur totale comprenant l'entrée. Quand le compteur atteint le budget,
la boucle s'arrête même sans EOS.

Une valeur maximale ne réserve pas automatiquement la place correspondante
dans la fenêtre de contexte. Cette précondition sera ouverte dans la leçon
suivante sur le budget de contexte.

### Annulation, délai et erreur

Une API complète peut aussi terminer sur :

- annulation demandée ;
- délai dépassé ;
- erreur du modèle ;
- distribution invalide ;
- limite de contexte ;
- arrêt administratif ou de sécurité.

Le Parcours 0 représente déjà ces issues comme des raisons typées, mais les
politiques de retry, d'approbation et de reprise appartiennent aux Parcours 2,
5, 9 et 10.

### Priorité et simultanéité

Le dernier token autorisé peut être EOS au moment exact où le budget est
atteint. La politique doit choisir une priorité stable. Préférer `eos` conserve
l'information que le modèle a produit une fin ; préférer `max_new_tokens`
indique que la limite a été atteinte. Aucun choix n'est implicite.

La raison n'est pas un simple texte libre. Un enum ou une union typée permet
aux métriques et aux appelants de distinguer les issues sans parser un message.

## Reconstruction

Une politique minimale :

```python
from dataclasses import dataclass
from enum import StrEnum

class StopReason(StrEnum):
    EOS = "eos"
    STOP_SEQUENCE = "stop_sequence"
    MAX_NEW_TOKENS = "max_new_tokens"

@dataclass(frozen=True)
class StopDecision:
    reason: StopReason | None
    visible_text: str

def evaluer_arret(
    token_id: int,
    texte: str,
    generated_count: int,
    eos_ids: frozenset[int],
    stop_strings: tuple[str, ...],
    max_new_tokens: int,
) -> StopDecision:
    if token_id in eos_ids:
        return StopDecision(StopReason.EOS, texte)
    positions = [
        (texte.find(stop), stop)
        for stop in stop_strings
        if texte.find(stop) >= 0
    ]
    if positions:
        position, _ = min(positions)
        return StopDecision(StopReason.STOP_SEQUENCE, texte[:position])
    if generated_count >= max_new_tokens:
        return StopDecision(StopReason.MAX_NEW_TOKENS, texte)
    return StopDecision(None, texte)
```

Cette version travaille sur le texte cumulé. Un streamer réel doit aussi
retenir les suffixes qui sont des préfixes possibles d'une stop sequence.

## Décision et dépôt dans Praxis

- **Décision** — `StopPolicy` renvoie une union fermée de raisons et contrôle le
  suffixe visible.
- **Alternatives** — un booléen, une exception générique ou une chaîne libre.
- **Critère** — l'appelant doit distinguer une fin normale, une limite et un
  échec.
- **Coût accepté** — un buffer de publication dimensionné par la plus longue
  stop sequence pertinente.
- **Condition de révision** — les budgets de temps et d'outils seront composés
  dans la boucle agentique.
- **Contrat** — `praxis.generation.StopPolicy` et `StopReason`.
- **Invariant et tests** — toute boucle est bornée ; une stop sequence exclue
  n'est jamais publiée ; EOS multiples sont acceptés ; la priorité est testée.

## Limites et cas d'échec

- **La reconstruction ne prouve pas** — la correction d'un matcher de flux avec
  chevauchements complexes.
- **Praxis ne garantit pas encore** — la livraison distante d'une raison
  homogène par tous les fournisseurs.
- **Échec provoqué** — une stop sequence coupée entre deux fragments doit être
  reconnue sans fuite du marqueur.
- **Ouverture ultérieure** —
  [[18-fenetre-contexte-cout|Fenêtre de contexte et coût]] et le Parcours 2 pour
  les coupures de transport.

## Se tester

1. Pourquoi EOS et stop sequence ne sont-ils pas le même mécanisme ?
2. Quelle donnée doit être retenue pour empêcher qu'une stop sequence soit
   publiée partiellement ?
3. Quelle différence sépare `max_new_tokens` d'une longueur totale maximale ?
4. Pourquoi une raison d'arrêt typée est-elle préférable à un booléen ?
5. Que doit décider le contrat lorsqu'EOS apparaît sur le dernier token du
   budget ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#16--borner-la-génération).

## Références

- [Transformers — `GenerationConfig`, documentation `main` vérifiée le
  2026-07-27](https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig) —
  `max_new_tokens`, `stop_strings`, EOS simple ou multiple.
- [Transformers — stopping criteria](https://huggingface.co/docs/transformers/internal/generation_utils#transformers.StoppingCriteria) —
  contrat industriel de décision d'arrêt.
- [Transformers — `StopStringCriteria`, source `main`](https://github.com/huggingface/transformers/blob/main/src/transformers/generation/stopping_criteria.py) —
  correspondances traversant des frontières de tokens.

