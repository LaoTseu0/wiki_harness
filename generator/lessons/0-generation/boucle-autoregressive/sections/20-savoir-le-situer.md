## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : inférence → choix → ajout → décodage → décision d'arrêt →
réinjection.

**Étape ouverte** —
`condition-arret → reinjection → inference`.  
**Input** : séquence étendue, état du run et décision de continuer. **Output** : nouvel
**Input** du modèle pour le pas suivant.  
Responsabilité : faire du [[glossaire/token|token]] choisi une partie immuable du préfixe suivant.

**L'essentiel** — la [[glossaire/boucle-autoregressive|boucle autorégressive]] choisit un **token**, l'ajoute au
préfixe et recommence jusqu'à une condition d'arrêt. Le modèle causal produit
une distribution pour chaque nouvelle position.

**Recomposer** — chaque tour repasse par l'inférence, les transformations et le
[[glossaire/sampling|sampling]]. Le **token** réinjecté modifie toutes les distributions suivantes ; une
divergence locale devient une nouvelle trajectoire.

![[boucle-autoregressive.canvas]]
