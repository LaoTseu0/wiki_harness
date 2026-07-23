# Prompting

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** :
  - l'[autorégression](../glossaire/autoregression.md), posée ici parce que
    toute la leçon en découle : le modèle ne fait jamais qu'une chose, **prolonger
    un préfixe**, un token à la fois, chacun réinjecté dans l'entrée du suivant.
    Il n'existe pas de canal séparé pour « la consigne » d'un côté et « les
    données » de l'autre — tout est le même texte à prolonger. Cette propriété
    unique explique les quatre techniques ci-dessous.
  - le [template de chat](template-de-chat.md), qui aplatit la liste de messages
    en ce texte unique : c'est lui qui décide où atterrit réellement un
    « prompt système ».
  - le [sampling](sampling.md), pour ne pas attribuer au prompt ce qui relève du
    tirage.
- **Débloque** : le [function calling](function-calling.md) et la
  [boucle d'agent](boucle-agent.md), qui sont l'un des patterns ci-dessous
  effectivement implémenté.

## L'essentiel

Le prompting n'est pas un art de la formulation : c'est le **choix du préfixe**
que le modèle va prolonger. Toutes les techniques nommées — few-shot,
chain-of-thought, ReAct, prompt système — sont des façons de placer dans ce
préfixe quelque chose qui rende la suite souhaitée plus probable. Elles n'ont
aucun autre pouvoir, et c'est ce qui permet de prédire quand chacune marche.

Corollaire immédiat et contre-intuitif : le modèle n'a aucun moyen de distinguer
ce qu'on lui montre *pour la forme* de ce qu'on lui montre *pour le fond*. Tout
ce qui est dans le préfixe est matière à imitation.

Borne : le prompting décide de **ce qu'il y a dans la distribution** ; la façon
d'y puiser est l'objet de [sampling](sampling.md), et forcer la sortie à
respecter une grammaire celui de [structured output](structured-output.md).

## Le savoir

### `zero-shot` et `few-shot`

**zero-shot** : la consigne seule. **few-shot** : la consigne plus des exemples.

Le mécanisme est celui du préfixe : les exemples sont le précédent le plus
proche et le plus récent dont dispose le modèle au moment de produire le token
suivant. Il ne les « comprend » pas comme une spécification — il les prolonge.

De là suit la seule règle qui compte : **le format des exemples *est* la
spécification**. Puisque rien ne sépare la forme du fond dans le préfixe, un
exemple ne transmet pas que son contenu, il transmet aussi sa longueur, sa
ponctuation, son niveau de détail, sa structure. Deux conséquences qu'on subit
souvent sans les voir : un exemple bâclé produit une sortie bâclée, et trois
exemples courts imposent une réponse courte même quand on voulait du détail.

### `chain-of-thought`

Demander les étapes de raisonnement **avant** la réponse.

Le mécanisme tient à un fait de coût : chaque token est produit par une quantité
de calcul **fixe** — une passe dans le réseau. Une question difficile ne reçoit
donc pas davantage de calcul qu'une question facile, sauf si on lui fait produire
plus de tokens. Les étapes intermédiaires achètent ces passes supplémentaires, et
comme elles entrent dans le préfixe, la réponse finale se conditionne sur son
propre raisonnement au lieu de devoir tout faire en une passe.

Ce qui explique aussi le prix : les tokens de raisonnement se paient en
[latence et en contexte](tokenisation.md) comme les autres, et ils ne servent à
rien si la tâche tenait déjà dans une passe.

### `ReAct`

Alterner raisonnement et action — *Reason + Act*.

Le mécanisme prolonge le précédent d'un cran : le résultat d'un outil, réinjecté
dans le préfixe, est **la seule façon de faire entrer dans le calcul une
information qui n'est ni dans les poids ni dans le prompt initial**. Le modèle
réfléchit, émet un appel d'outil, l'observation revient dans le contexte, et le
tour suivant se conditionne dessus.

C'est le pattern derrière toutes les boucles d'agent. Il est implémenté à la
main en [function calling](function-calling.md), puis mis en boucle en
[boucle d'agent](boucle-agent.md).

### Le prompt système

Il fixe le rôle, les contraintes d'entrée/sortie et le format attendu.

Son mécanisme est positionnel, et c'est ce qui le distingue d'un message
ordinaire : le [template de chat](template-de-chat.md) le place en **tête** du
texte aplati. Il est donc présent à chaque passe, pour chaque token, du premier
au dernier — d'où son influence disproportionnée à sa longueur. Et parce qu'il
est un préfixe **stable**, c'est la portion la moins chère à conserver d'un appel
à l'autre : voir [attention et KV cache](attention-et-kv-cache.md) et
[prompt caching](../inference/prompt-caching.md).

Un prompt système qui change à chaque requête perd cet avantage deux fois : il
n'est plus mis en cache, et il n'est plus le cadre stable qu'il prétend être.

## Quand c'est la bonne réponse

| Technique | À employer quand | À ne pas employer quand | Alors, plutôt |
|---|---|---|---|
| **few-shot** | la sortie a une forme précise, difficile à décrire mais facile à montrer | la forme est déjà descriptible en une phrase — les exemples coûtent du contexte pour rien | zero-shot, ou un schéma en [structured output](structured-output.md) |
| **chain-of-thought** | la tâche a plusieurs étapes dépendantes et une réponse fausse vient d'un saut logique | la tâche tient en une passe — extraction, classification, reformulation | zero-shot ; le raisonnement n'achète que de la latence |
| **ReAct** | la réponse dépend d'une information absente des poids et du prompt | tout ce qu'il faut est déjà dans le contexte | un appel simple, sans boucle ni outil |
| **prompt système** | la contrainte vaut pour tous les tours | la contrainte ne vaut que pour ce tour-ci | la mettre dans le message, pour ne pas polluer le cadre |

Le critère commun : **une technique de prompting ne se justifie que par ce
qu'elle ajoute au préfixe**. Si on ne sait pas dire ce qu'elle y met, elle ne
fait rien d'autre que consommer du contexte.

## Ce qu'on ne saura pas faire

Cette leçon permet de **choisir** une technique et de dire pourquoi elle devrait
marcher. Elle ne permet pas de dire de combien : aucun arbitrage chiffré ici,
donc aucune réponse à « le chain-of-thought vaut-il son coût sur *cette*
tâche ? ». Les affirmations de gain qu'on lit partout sont invérifiables tant
qu'on n'a pas mesuré sur son propre modèle.

Elle ne dit rien non plus de la robustesse : ce qui arrive à un prompt quand
l'entrée est hostile relève de la
[prompt injection indirecte](../mcp/prompt-injection-indirecte.md), et la
propriété « rien ne sépare la consigne des données » y devient une faille et non
une commodité.

Ce qui la promouvrait en leçon « refaire » : une étape qui mesure, sur une même
tâche et un même modèle, le coût en tokens et l'écart de qualité entre zero-shot,
few-shot et chain-of-thought — avec un critère de réussite décidé avant de lancer.

## Se tester

1. **Pourquoi un few-shot dont les exemples sont tous courts produit-il des
   réponses courtes, même si on demande du détail ?** *Réussi si* la réponse
   invoque l'absence de séparation entre forme et fond dans le préfixe, et non
   une « habitude » du modèle.
2. **Pourquoi le chain-of-thought aide-t-il, alors que le modèle a déjà toute sa
   capacité de calcul ?** *Réussi si* la réponse porte sur le calcul *par token*
   qui est fixe, et sur les passes supplémentaires achetées par les tokens
   intermédiaires.
3. **Une consigne placée en prompt système et la même consigne répétée à chaque
   message : quelle différence concrète ?** *Réussi si* la réponse mentionne la
   position en tête du texte aplati **et** la conséquence sur le cache.

## À retenir

- Le modèle prolonge un préfixe ; le prompting, c'est le choix de ce préfixe, et
  rien d'autre.
- Rien ne sépare la forme du fond dans le préfixe : le format des exemples est la
  spécification, longueur et structure comprises.
- Le calcul par token est fixe : les tokens de raisonnement sont des passes
  supplémentaires achetées, pas une intelligence supplémentaire.
- ReAct est la seule façon de faire entrer dans le calcul ce qui n'est ni dans
  les poids ni dans le prompt.
- Le prompt système agit par sa position en tête : présent à chaque passe, et
  seul candidat sérieux à la mise en cache.
- Une technique qui n'ajoute rien d'identifiable au préfixe ne fait que consommer
  du contexte.

## Références

- Les termes *zero-shot*, *few-shot*, *chain-of-thought* et *ReAct* se retrouvent
  tels quels dans les documentations des fournisseurs — les y lire pour vérifier
  ce que chacun met derrière, les définitions divergeant d'un acteur à l'autre.
- La documentation de son propre modèle, section *template* — pour savoir où
  atterrit vraiment un prompt système avant d'en déduire quoi que ce soit.
