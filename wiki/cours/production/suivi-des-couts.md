# Suivi des coûts

> [carte du cours](../carte.md)

## L'essentiel

« Le local est gratuit » est une illusion comptable. La leçon installe
le **coût équivalent API** : chaque appel local est valorisé au tarif
qu'il aurait coûté chez un provider cloud — la métrique citée dans
toutes les offres LLMOps, et l'outil de décision local vs API.

## Le savoir

- **La mécanique** : Langfuse calcule les coûts depuis les comptes de
  tokens et une **table de prix par modèle** ; pour les modèles
  locaux, on déclare un prix de référence — « comparable » par
  **classe de taille et de qualité**, pas par prestige ; et plutôt
  qu'un chiffre unique, une **fourchette** (un tarif « mini », un
  tarif « standard ») : la conclusion locale vs cloud montre alors sa
  sensibilité au choix au lieu d'en dépendre en silence → chaque
  trace porte son coût équivalent, les dashboards agrègent par
  jour/module/modèle.
- **Ce que le chiffre permet** :
  - **dimensionner** : « le RAG consomme ~N M tokens/mois ≈ X €/mois
    en API » — la base du raisonnement local vs cloud
 ;
  - **arbitrer le routage**
    ([routage multi-agentique](../framework/routage-multi-agentique.md)) :
    les décisions coût/latence/qualité se prennent sur des coûts
    tracés, pas estimés ;
  - **détecter les dérives** : un agent qui boucle
    ([mini-boucle d'agent](../fondamentaux/boucle-agent.md))
    ou un prompt qui enfle se voient sur la courbe avant de se voir
    ailleurs.
- **L'honnêteté du modèle de coût local** : le coût équivalent API
  n'est pas le coût réel (électricité, amortissement GPU) — les deux
  se calculent : ~0,2 kWh × prix pour une soirée de RTX 2060, vs le
  même volume au tarif API. L'écart *dans les deux sens* selon le
  volume est exactement le discours d'entretien.
- **Le réflexe par requête** : le service RAG renvoie déjà ses
  métriques ([service FastAPI](../framework/service.md)) —
  y ajouter le coût ferme la boucle : chaque réponse connaît son prix.

## En pratique

Déclarer les prix de référence dans Langfuse (Qwen3 4B ↔ un tarif
cloud comparable documenté), dashboard coûts/jour par projet, et une
note dans le README du domaine production : consommation mensuelle mesurée,
équivalent API, coût électrique estimé — trois chiffres, une
conclusion.

## Pièges connus

- Choisir un prix de référence flatteur (le modèle cloud le plus
  cher) : la comparaison ne convainc personne — prendre l'équivalent
  raisonnable et le documenter.
- Compter les tokens à l'estime : utiliser les comptes exacts renvoyés
  par l'API ([chat CLI, historique et contexte](../fondamentaux/chat-historique-contexte.md)) —
  ils sont déjà dans les traces.
- Ignorer les coûts cachés du cloud dans l'autre sens (egress,
  rate limits, montée de gamme forcée) : la comparaison honnête cite
  ses limites des deux côtés.

## Se tester

> « Local ou API : comment décidez-vous, chiffres en main ? »
> Tokens/mois mesurés en traces, valorisés au tarif API équivalent,
> contre coût réel local (énergie + amortissement) — chez moi : X
> M tokens/mois ≈ Y € API vs Z € local — et le point de bascule est
> une fonction du volume, pas une opinion.

## Références

- Doc Langfuse : model pricing, dashboards de coûts
