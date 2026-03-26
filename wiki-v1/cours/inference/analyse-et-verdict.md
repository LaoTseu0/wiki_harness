# De la mesure à la décision

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [un benchmark honnête](benchmark.md) — les courbes
  produites proprement ; [la charge concurrente](charge-concurrente.md) — les
  courbes précises que cette leçon apprend à lire puis à trancher.
- **Débloque** : [les mécanismes vLLM](mecanismes-vllm.md), qui fournissent les
  explications ; [le verdict](verdict-ollama-vs-vllm.md), qui écrit la règle de
  décision. Cette leçon dit ce qui relie les deux.

## L'essentiel

Un benchmark ne vaut que par ce qu'on en fait. Produire des courbes est le
milieu du travail, pas la fin : il reste à les **expliquer**, puis à en tirer une
**règle de décision**. La thèse de cette leçon est que ces deux gestes sont liés
par un troisième, souvent sauté — le **mécanisme**.

Deux propositions qu'on peut contredire :

1. **Une cassure de courbe qu'on ne sait pas nommer est une courbe à laquelle on
   ne peut pas se fier** — parce qu'on ne sait pas si elle décrit le moteur ou un
   défaut de la mesure.
2. **Une décision sans mécanisme est une opinion déguisée en donnée** — elle
   généralise un chiffre local sans savoir ce qui le produit, donc sans savoir où
   il cesse de valoir.

Cette leçon ne donne pas les mécanismes eux-mêmes — c'est
[mécanismes vLLM](mecanismes-vllm.md) — ni le contenu de la règle — c'est
[le verdict](verdict-ollama-vs-vllm.md). Elle porte le passage de l'un à l'autre.

## Le savoir

### Expliquer sépare le comportement de l'artefact

Une cassure dans une courbe a deux lectures possibles : un **comportement** du
moteur (le cache sature, la file s'allonge) ou un **artefact** de la mesure (le
réseau a hoqueté, une salve était trop courte). À l'œil, les deux se ressemblent
— une inflexion soudaine.

Ce qui les sépare est de pouvoir **rattacher la cassure à un mécanisme nommé**.
Si l'inflexion du débit de vLLM correspond au moment où le KV cache se remplit et
où les préemptions apparaissent dans les logs
([mécanismes vLLM](mecanismes-vllm.md)), c'est un comportement. Si elle ne
correspond à rien de nommable, c'est le premier suspect d'artefact — et l'on
remesure avant de conclure. Le mécanisme est le test qui distingue les deux, et
c'est pourquoi expliquer n'est pas un ornement de la mesure mais sa validation.

### La décision se paramètre, elle ne s'absolutise

« vLLM gagne » est un verdict faux même quand la courbe lui donne raison, parce
qu'il généralise une mesure faite à une VRAM donnée, sur un trafic donné. La même
mesure sur une carte de 24 Go ou sur un trafic homogène donnerait une autre
conclusion.

La sortie honnête n'est donc pas un gagnant mais une **règle paramétrée** :
*au-delà de tel niveau de concurrence, et avec telle VRAM, tel moteur*. Ce sont
les mécanismes qui fournissent les paramètres — la concurrence parce que le
batching en dépend, la VRAM parce que le cache la borne. Une règle qui ne cite
pas ces paramètres n'a pas identifié ce qui fait pencher la balance, et se
cassera dès qu'on change de contexte. Le contenu de la règle est
[le verdict](verdict-ollama-vs-vllm.md) ; ce qui précède dit seulement pourquoi
elle doit être paramétrée.

### La boucle qui referme le module

Le module est une démarche d'ingénierie en miniature, et elle se lit comme une
boucle : **déployer** ([servir un modèle](deploiement.md)) → **mesurer**
([benchmark honnête](benchmark.md)) → **expliquer** → **décider**
([verdict](verdict-ollama-vs-vllm.md)). Chaque étape conditionne la suivante — on
ne mesure bien que ce qu'on a monté proprement, on n'explique que ce qu'on a
mesuré, on ne décide que ce qu'on a expliqué. Sauter l'explication, c'est décider
sur une corrélation ; c'est exactement l'erreur que cette leçon existe pour
interdire.

## Quand c'est la bonne réponse

**Expliquer avant de décider** dès qu'une décision d'infrastructure dépend du
résultat. Le mécanisme est ce qui rend la décision transférable à un contexte
voisin.

**Se contenter de la courbe brute** quand on documente sans décider — un relevé
d'état, pas un choix. Mais dès qu'on écrit « donc on prend X », l'explication
redevient obligatoire.

**Refuser le verdict absolu** toujours : même quand un moteur domine nettement,
la règle se donne paramétrée, sinon elle ment sur son domaine de validité.

## Ce qu'on ne saura pas faire

Aucune courbe n'a été produite dans ce dépôt : il n'y a donc rien à expliquer ni
à trancher pour l'instant. Cette leçon décrit la méthode du passage
mesure → décision, pas un verdict — qui, lui, attend le bench.

Ce que ça laisse ouvert : on ne sait pas encore quelles cassures apparaîtront
réellement, donc lesquelles seront des comportements et lesquelles des artefacts.
La distinction elle-même ne se fera qu'avec des logs sous les yeux.

Ce qui promouvrait cette leçon en « refaire » : les courbes du bench annotées
mécanisme par mécanisme — une flèche, une explication — et une règle de décision
écrite, paramétrée par la concurrence et la VRAM, adossée aux chiffres.

## Se tester

1. La courbe de débit de vLLM casse nettement à un certain niveau de charge. Que
   faites-vous avant d'écrire « vLLM sature à ce point » ?
   *Réussi si* la réponse cherche à rattacher la cassure à un mécanisme nommé
   (cache plein, préemptions dans les logs) et, à défaut, remesure — la cassure
   pouvant être un artefact.
2. Un rapport conclut « vLLM est le meilleur moteur ». Pourquoi est-ce faux même
   si les courbes le montrent ici ?
   *Réussi si* la réponse note que le verdict généralise une mesure locale (une
   VRAM, un trafic) et exige une règle paramétrée par la concurrence et la VRAM.
3. On vous propose de sauter l'explication des courbes pour aller droit à la
   décision, « les chiffres parlent d'eux-mêmes ». Que répondez-vous ?
   *Réussi si* la réponse identifie qu'on déciderait alors sur une corrélation
   sans savoir ce qui la produit, donc sans savoir où elle cesse de valoir.

## À retenir

- Mesurer est le milieu du travail : il reste à expliquer, puis à décider — et le
  mécanisme relie les deux.
- Une cassure qu'on ne sait pas nommer peut être un artefact autant qu'un
  comportement ; le mécanisme est le test qui les sépare.
- Une décision sans mécanisme est une opinion : elle généralise un chiffre local
  sans connaître son domaine de validité.
- La règle de décision se donne paramétrée par la concurrence et la VRAM, jamais
  comme un vainqueur absolu.

## Références

- [Mécanismes vLLM](mecanismes-vllm.md) — les explications qui valident les
  cassures de courbe
- [Verdict Ollama vs vLLM](verdict-ollama-vs-vllm.md) — la règle de décision, une
  fois le pont franchi
- [Un benchmark honnête](benchmark.md) — la courbe que cette leçon apprend à
  exploiter
