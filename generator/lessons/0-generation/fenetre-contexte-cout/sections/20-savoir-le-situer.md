## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : sampling → ajout au contexte → décodage → arrêt ou
réinjection.

**Étape ouverte** — `sampling → ajout-token → detokenisation`.  
Input : token choisi, longueur courante et capacité du modèle. Output : séquence
étendue si la capacité le permet.  
Responsabilité : empêcher que l'entrée plus la sortie dépasse la fenêtre
effective et rendre le budget explicite.

**L'essentiel** — la fenêtre se mesure en positions ou tokens après application
du Template. Elle borne ensemble le préfixe et les tokens conservés pour la
suite ; elle n'est ni un nombre de caractères ni un budget de sortie.

**Recomposer** — chaque ajout consomme une position et agrandit le cache. Quand
la capacité manque, la boucle doit s'arrêter ou appliquer une politique de
contexte décidée ailleurs, jamais tronquer silencieusement.

![[fenetre-contexte-cout.canvas]]
