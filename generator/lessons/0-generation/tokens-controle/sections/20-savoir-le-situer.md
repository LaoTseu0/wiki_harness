## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : Template de chat → tokenisation → inférence → sampling →
détokenisation → arrêt.

**Étape ouverte** — `chat-template → tokenisation → inference`.  
Input : texte sérialisé et politique de tokens spéciaux. Output : identifiants,
y compris les marqueurs attendus par le modèle.  
Responsabilité : distinguer le contenu des marqueurs réservés sans les ajouter
deux fois.

**L'essentiel** — un token de contrôle est une entrée réservée du vocabulaire.
Son identifiant ne produit un comportement particulier que si l'entraînement,
le Template ou la boucle de génération lui donne ce rôle.

**Recomposer** — les marqueurs de début, de rôle et de fin structurent la
séquence avant l'inférence. Les marqueurs de fin reviennent ensuite dans les
conditions d'arrêt.

![[tokens-controle.canvas]]
