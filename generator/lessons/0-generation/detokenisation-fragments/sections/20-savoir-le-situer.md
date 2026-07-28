## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]].  
Input global : messages structurés. Output global : texte généré et raison
d'arrêt.  
Grandes étapes : sampling → ajout du token → détokenisation → arrêt ou
réinjection.

**Étape ouverte** —
`ajout-token → detokenisation → condition-arret`.  
Input : nouvel identifiant et état du décodeur. Output : zéro ou plusieurs
caractères sûrs à accumuler.  
Responsabilité : reconstruire le texte sans supposer qu'un token est une unité
UTF-8 ou un fragment concaténable.

**L'essentiel** — le décodage est une opération sur la séquence et peut porter
un état. Un token byte-level isolé peut finir au milieu d'un caractère ; le
stream ne doit émettre que le préfixe textuel définitivement décodable.

**Recomposer** — le texte accumulé alimente l'affichage et les stop sequences.
Les identifiants restent parallèlement la source de vérité pour la réinjection
et les arrêts par token.

![[detokenisation-fragments.canvas]]
