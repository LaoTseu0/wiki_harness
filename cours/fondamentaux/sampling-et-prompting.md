# 1.1.2 Sampling et prompting

> **Leçon de la section [1.1 Socle sans framework](../1.1-socle-sans-framework.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ✅ acquis (20 juillet 2026)
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

À chaque token, le modèle produit une **distribution de probabilités**
sur tout son vocabulaire. Le sampling décide comment tirer dans cette
distribution ; le prompting décide ce qu'elle contient. Les deux
leviers se règlent, se mesurent, et s'expliquent en entretien.

## Le savoir

**Sampling** — l'ordre d'application **mesuré au notebook 04** (défaut
llama.cpp, donc Ollama) : logits → filtres **top-k → top-p** →
**temperature** → tirage. Les présentations « manuel » placent souvent
la temperature avant les filtres ; l'ordre réel est une chaîne de
samplers propre au moteur, parfois configurable — raison de plus pour
l'avoir mesuré soi-même plutôt que récité.

- **temperature** : divise les logits avant le softmax. T → 0 :
  quasi-argmax (répétitif, sûr) ; T élevée : distribution aplatie
  (créatif, instable). « Déterministe » à T=0 n'est **pas garanti** :
  égalités de probabilités, ordre des opérations flottantes, batching.
- **top-k** : ne garder que les k tokens les plus probables (coupe la
  longue traîne absurde).
- **top-p (nucleus)** : garder le plus petit ensemble dont la
  probabilité cumulée atteint p — adaptatif là où top-k est fixe.
- **repetition penalty** : pénalise les tokens déjà émis — évite les
  boucles.
- **num_predict** (garde-fou) : plafond de tokens générés — l'incident
  « génération débridée » du notebook a montré pourquoi on le fixe
  toujours.

**Prompting** — les techniques nommées (les offres utilisent ces
termes) :

- **zero-shot** : la consigne seule ; **few-shot** : avec exemples —
  le format des exemples *est* la spécification ;
- **chain-of-thought (CoT)** : demander les étapes avant la réponse —
  améliore le raisonnement, coûte des tokens ;
- **ReAct** : alterner raisonnement et action — le pattern derrière
  toutes les boucles d'agent
  ([1.1.4](../1.1.4-mini-boucle-agent/1.1.4-mini-boucle-agent.md)) ;
- prompt système : rôle, contraintes d'entrée/sortie, format.

## En pratique

[04_sampling.ipynb](04_sampling.ipynb) : protocole en dict de
scénarios + `**options`, effets mesurés paramètre par paramètre sur des
cas concrets — écrit en grande partie par Anthony.

## Pièges connus

- Régler temperature ET top-p agressivement en même temps : les effets
  se composent mal ; bouger un levier à la fois.
- CoT sur une tâche d'extraction simple : plus lent, pas meilleur — la
  technique se choisit par tâche.
- Croire qu'un few-shot « montre le style » : il fixe aussi la
  *longueur* et la *structure* attendues, souvent à l'insu de l'auteur.

## Question d'entretien

> « Temperature 0, c'est déterministe ? »
> Non garanti : ex æquo dans la distribution, non-associativité des
> flottants selon le batching, architectures MoE (le routage des
> experts dépend de la composition du batch : la même requête ne
> rencontre pas toujours les mêmes voisines, donc pas les mêmes
> arrondis ni les mêmes experts saturés). Pour de la reproductibilité,
> il faut figer bien plus que la temperature (seed, version du modèle,
> serveur).

## Références

- 3Blue1Brown (série transformers) — l'intuition du softmax
- Playground de tokenizer (OpenAI/HF) — voir ce que le modèle voit
