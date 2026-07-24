# Sampling

> [carte du cours](../carte.md) · étape : [`04_sampling.ipynb`](../../etapes/fondamentaux/04_sampling.ipynb)

## Où ça s'emboîte

- **Processus** : [d'un texte à un token](../_processus/generation-token.md)
- **L'étape ouverte** : `filtres` · `temperature` · `tirage` — entre un logit par token du vocabulaire, sort un token unique

![[sampling.canvas]]

## Prérequis et suites

- **Suppose acquis** — trois objets que la suite manipule à chaque phrase,
  donc posés ici en plus d'être liés :
  - les [logits](../glossaire/logits.md) : le score brut que la dernière
    couche attribue à chaque token du vocabulaire, à chaque étape. Non
    normalisés, positifs ou négatifs, illisibles comme probabilités.
  - le [softmax](../glossaire/softmax.md) : la fonction qui les convertit en
    distribution. Deux propriétés seulement, ce sont les seules dont on se
    servira — il **conserve l'ordre** (le plus gros logit reste la plus grosse
    probabilité), et il **amplifie les écarts**, parce qu'il passe par
    l'exponentielle : un écart de 1 en logits ressort en rapport d'environ 2,7
    en probabilités.
  - l'[autorégression](../glossaire/autoregression.md) : un token à la fois,
    chacun réinjecté dans l'entrée du suivant, sans retour en arrière. Sans
    elle, la portée de la seed plus bas est incompréhensible.
- **Débloque** : le [prompting](prompting.md), qui décide de ce qu'il y a dans
  la distribution ; le [structured output](structured-output.md), qui contraint
  le tirage au lieu de le subir ; et tout réglage d'agent où une sortie
  instable est un bug et non une fantaisie.

## L'essentiel

À chaque token, le modèle ne produit pas du texte : il produit une
**distribution de probabilités sur tout son vocabulaire**. Ce qu'on appelle sa
« créativité », son « instabilité » ou son « déterminisme » ne sont pas des
propriétés du modèle — ce sont des propriétés du réglage appliqué après lui, sur
cette distribution. Et ce réglage se vérifie : chaque levier a un réglage sous
lequel il ne fait plus rien, constatable en trois essais.

Borne : cette leçon traite de **comment on puise** dans la distribution. Ce qui
détermine **ce qu'elle contient** est l'objet de [prompting](prompting.md).
Forcer la sortie à respecter une grammaire — du JSON valide — est celui de
[structured output](structured-output.md).

## Le savoir

### La chaîne, et ce qui est réellement établi sur son ordre

Le processus place trois étapes entre le modèle et le token. Les **filtres**
décident *qui a le droit de participer*, la **temperature** *avec quels poids*,
le **tirage** *qui sort*.

Ce que l'étape mesure, c'est que **le filtre a le dernier mot sur la
temperature** : à `T=1.5`, ajouter `top_k=1` rend la sortie identique trois fois
sur trois. C'est une observation sur le résultat, pas sur l'ordre du code — un
filtre qui ne laisse qu'un candidat produit un tirage déterministe quel que soit
le moment où la temperature s'applique. L'ordre réel de la chaîne de samplers
dans le moteur, et le fait qu'il soit parfois configurable, n'ont pas été
vérifiés ici : à lire dans sa configuration plutôt qu'à réciter d'un manuel, les
manuels plaçant souvent la temperature avant les filtres.

<!-- À MESURER — l'ordre d'application des samplers du moteur : le lire dans sa
     configuration, ou concevoir une expérience qui le discrimine réellement -->

### Les leviers

**`temperature`** divise chaque logit par $T$ avant le softmax. Les deux
propriétés posées plus haut suffisent à prédire son effet : puisque le softmax
**conserve l'ordre**, elle ne change jamais *qui* est en tête ; puisqu'il
**amplifie les écarts**, réduire les écarts en amont produit une distribution
d'autant plus plate. $T \to 0$ tend vers l'[argmax](../glossaire/argmax.md),
$T$ grande vers l'uniforme.

**`top-k`** ne garde que les k tokens de plus gros logit. Seuil **fixe** :
toujours k candidats, que le modèle soit sûr de lui ou non.

**`top-p`** (nucleus) garde le plus petit ensemble dont la probabilité cumulée
atteint p. Seuil **adaptatif** : peu de candidats quand une case domine,
beaucoup quand la distribution est plate. C'est le complément de top-k, pas son
concurrent.

**`repetition penalty`** abaisse le logit des tokens déjà émis. Il agit donc sur
un ensemble qui grandit à mesure que la sortie s'allonge — c'est le seul levier
dont le poids augmente en cours de génération.

**`num_predict` n'est pas un sampler.** Il ne touche ni les logits, ni la
distribution, ni le tirage : c'est le plafond de la **boucle** qui répète tout
ce qui précède. Le ranger parmi les filtres brouille la chaîne ; il se règle
pour une autre raison, exposée dans les pièges.

La portée de chacun, dont la dernière colonne est celle qu'on oublie :

| Levier | Où il agit | À quelle fréquence | Ce qu'il propage | Ce qui l'annule |
|---|---|---|---|---|
| `temperature` | sur les logits, avant le softmax | à chaque token | par le token tiré, qui devient contexte | `top_k=1`, ou un `top_p` assez serré pour ne laisser qu'un candidat — **mesuré** |
| `top-k` | sur les logits triés | à chaque token | idem | `top_k=0` (désactivé) |
| `top-p` | sur la probabilité cumulée | à chaque token | idem | `top_p=1.0` |
| `repetition penalty` | sur les logits des tokens déjà émis | à chaque token, sur un ensemble croissant | il se renforce lui-même | sa valeur neutre ; et il est sans effet sur le premier token, rien n'ayant été émis |
| `seed` | sur le tirage, nulle part ailleurs | à chaque token — elle amorce une suite | **tout** : le token tiré devient contexte et décale les logits suivants | `T=0` : sans tirage, le générateur n'est pas consulté |
| `num_predict` | sur la boucle, pas sur la chaîne | une fois par requête | rien, il coupe | un token d'arrêt qui arrive avant le plafond |

### Le tirage : ce qui choisit réellement

Une fois la distribution filtrée et tempérée, il reste à en extraire *un* token.
Ce n'est ni le modèle ni la distribution qui choisit : c'est **un nombre tiré au
hasard, comparé à des intervalles**.

On aligne les probabilités bout à bout sur le segment $[0, 1)$ ; chaque token
occupe une case aussi large que sa probabilité. On tire un nombre dans $[0, 1)$,
on regarde dans quelle case il tombe, c'est lui. Un token à 0,69 sort environ
69 % du temps parce que sa case couvre 69 % du segment — il n'y a rien d'autre
dans la machine.

Le nombre, lui, sort d'un **PRNG** : pas du vrai hasard, mais un algorithme
déterministe qui, à partir d'un état initial — la **seed** —, produit une suite
qui passe les tests statistiques d'aléa tout en étant entièrement reproductible.

![[ou-agit-la-seed.canvas]]

La seed n'agit donc qu'à **une seule étape**, mais **à chaque token**, et son
effet **se propage en cascade** : le token tiré est réinjecté dans le contexte,
ce qui modifie les logits du suivant. Une graine différente peut faire diverger
toute la phrase à partir d'un seul token d'écart. À seed, température et prompt
identiques, la génération est reproductible — c'est pourquoi beaucoup d'API
exposent ce paramètre.

### Une sortie stable ne dit pas pourquoi elle est stable

Quatre réglages différents produisent le même symptôme à l'écran — trois essais,
trois sorties identiques — et l'étape les a tous les quatre mesurés : `T=0`,
`top_k=1`, un `top_p` serré, une `seed` fixée. Voir la stabilité ne dit pas
laquelle on regarde, et les quatre ne se corrigent pas de la même façon.

Le test qui les discrimine : **changer la seed sans rien toucher d'autre**. Si
la sortie bouge, c'est le tirage qui était figé, et la distribution comptait
plusieurs candidats. Si elle ne bouge pas, c'est qu'il n'en restait qu'un — le
coupable est un filtre ou une température nulle, pas le générateur.

### Le déterminisme à $T=0$ n'est pas garanti

Même en visant l'argmax, la sortie peut diverger d'une exécution à l'autre :
**égalités de probabilités** (deux tokens au même score, le départage dépend de
l'implémentation) ; **ordre des opérations flottantes** (sur GPU, des milliers
d'additions parallèles ne se somment pas toujours dans le même ordre, ce qui
décale infimement les logits) ; **batching**, qui modifie ces mêmes ordres de
calcul ; et sur une architecture [MoE](../glossaire/moe.md), le routage des
experts dépend de la composition du lot.

Ce non-déterminisme n'est pas de l'aléa voulu : c'est un **artefact matériel**,
d'une autre nature que le tirage. Les deux se ressemblent à l'écran et se
distinguent par leur réponse à la seed — l'aléa du tirage se fige en la fixant,
l'artefact non. Pour de la reproductibilité réelle, il faut figer bien plus que
la temperature : seed, version du modèle, serveur.

## En pratique

[04_sampling.ipynb](../../etapes/fondamentaux/04_sampling.ipynb). Le protocole
tient en trois idées :

- **un dict de scénarios** — chaque configuration est une entrée
  `{"temperature": …, "top_p": …}`, la boucle les parcourt et rejoue trois
  essais chacune. On lit les configurations côte à côte au lieu de commenter et
  décommenter des lignes.
- **`**options`** — les arguments nommés sont ramassés dans un dictionnaire
  transmis tel quel à Ollama : ajouter un levier ne demande aucune modification
  de la fonction d'appel.
- **l'isolation de variable** — `top_p=1.0, top_k=0` neutralisent les défauts du
  [Modelfile](../glossaire/modelfile.md) pour n'observer que le levier étudié.
  Sans ça, on mesure le Modelfile.

**À prédire avant de lancer.** Écrire les réponses, puis les confronter :

1. À `T=1.5` avec `top_k=1`, combien de sorties différentes sur trois, et pourquoi ?
2. À `T=1.2`, `top_p=0.5` donne-t-il plus ou moins de variété que `top_p=1.0` ?
3. `seed=42` à `T=0.8` fige la sortie — sera-t-elle **la même** que celle obtenue à `T=0` ?
4. Quel réglage rend la seed sans effet ?

La troisième est celle qui sépare « stable » de « le plus probable ».

## Mesures

Ollama `http://192.168.1.57:11434`, modèle `qwen3:4b-instruct-2507-q4_K_M`,
`num_predict=300`, même question à chaque fois, trois essais par configuration.

| Configuration | Sorties distinctes sur 3 | Ce qu'on observe |
|---|---|---|
| `T=0.0`, `top_p=1.0`, `top_k=0` | 1 | trois fois la même phrase, au caractère près |
| `T=0.8` | 3 | divergence **locale** : un adjectif (« léger » / « simple ») ou la fin de phrase change, la structure tient |
| `T=1.5` | 3 | dégradation **occasionnelle** : une sortie part en vrille (mots anglais « element », « atomic », accord faux, et une erreur factuelle — « des molécules comme l'eau (H₂) ») ; une autre garde la bonne phrase avec un seul mot anglais (« abundant ») ; la troisième reste correcte |
| `T=1.5`, `top_k=1` | 1 | le filtre annule la temperature |
| `T=1.2`, `top_p=0.5` | 1 | un top-p serré l'annule aussi |
| `T=1.2`, `top_p=1.0` | 3 | dont une réponse qui part en auto-correction et laisse un idéogramme chinois au milieu du français |
| `T=0.8`, `seed=42` | 1 | stable, mais sur une phrase **différente** de celle de `T=0` |

Deux enseignements que le tableau seul ne donne pas :

- à haute température, la dégradation n'est pas systématique mais **tirée**.
  « Haute température = charabia » est faux ; c'est « haute température =
  charabia de temps en temps », ce qui est bien plus difficile à déboguer.
- la dernière ligne sépare deux notions qu'on confond : `seed=42` à `T=0.8`
  donne une sortie **reproductible sans être la plus probable**. Figer n'est pas
  optimiser.

<!-- À MESURER — ce qui a démenti la prédiction : à remplir en confrontant les
     quatre réponses écrites avant l'exécution -->

## Recomposer

**Ce que ça change à ce qu'on croyait déjà savoir.** « Le modèle est créatif,
instable, déterministe » ne veut rien dire : ces mots décrivent la forme d'une
distribution et la façon d'y puiser, tous deux réglés *après* le modèle, de
l'extérieur, sans toucher un seul poids. Deux personnes qui font tourner le même
modèle et n'observent pas le même comportement ne parlent pas du même système —
elles parlent de deux réglages.

**Ce qu'on peut désormais prédire ailleurs.** Le décodage contraint de
[structured output](structured-output.md) est un filtre : il retire du
vocabulaire tout token qui casserait la grammaire. Il doit donc écraser la
temperature exactement comme `top_k=1` le fait ici — on peut prédire qu'un JSON
produit sous contrainte forte restera stable *même à température élevée*, et que
monter la température pour « varier » les sorties d'un extracteur n'aura presque
aucun effet. Corollaire pour la [boucle d'agent](boucle-agent.md) : une sortie
d'agent qui varie d'un tour à l'autre est un réglage de sampling avant d'être un
problème de prompt, et c'est la seed qu'il faut fixer d'abord pour savoir lequel
des deux on débogue.

## Pièges connus

**Rencontrés.**

- *Génération débridée, le 19/07.* Symptôme : un appel à `temperature=1.5` sur
  une question ouverte ne rend jamais la main — GPU à fond, puis timeout côté
  client. Hypothèse : le modèle boucle. Cause réelle : à température haute, la
  probabilité du token d'arrêt est aplatie comme celle des autres ; le modèle
  peut ne jamais le tirer et générer jusqu'à épuisement. Rien dans la chaîne de
  sampling n'arrête ça, parce que ce n'est pas un problème de sampling mais de
  boucle. Correctif : `num_predict=300` posé par défaut dans la fonction
  d'appel, surchargeable. C'est la raison pour laquelle toute API sérieuse
  impose un `max_tokens`.
- *Le Modelfile masquait l'effet qu'on croyait mesurer.* Symptôme : monter la
  temperature ne changeait presque rien. Test discriminant : interroger
  `/api/show`, qui révèle que le modèle embarque ses propres défauts de sampling
  — `temperature 0.7, top_k 20, top_p 0.8`. Cause : une option absente de la
  requête retombe sur le défaut du [Modelfile](../glossaire/modelfile.md) ;
  régler *seulement* la temperature laissait `top_p=0.8` actif, qui coupait la
  distribution aux favoris et neutralisait ce qu'on croyait observer. On mesurait
  le Modelfile. D'où `top_p=1.0, top_k=0` dans tout le protocole.

**Anticipés** — non vérifiés à ce jour.

- Bouger la temperature et le top-p en même temps : les deux agissent sur la
  même distribution, leurs effets ne se lisent pas séparément. Un levier à la
  fois.
- Un `repetition penalty` élevé sur une tâche où la répétition est légitime —
  une énumération, du code, un tableau — devrait dégrader la sortie en forçant
  des synonymes là où il faudrait le même mot.

## Se tester

1. **Pourquoi la temperature ne change-t-elle jamais quel token est le plus
   probable ?** *Réussi si* la réponse invoque la conservation de l'ordre par le
   softmax, et non un argument d'intensité.
2. **On observe trois sorties identiques sur trois essais. Quelles causes
   possibles, et quelle manipulation unique permet de trancher ?** *Réussi si*
   au moins trois des quatre causes sont citées, et si la manipulation proposée
   est de changer la seed seule.
3. **`seed=42` rend-il la sortie identique à celle obtenue à `T=0` ?** *Réussi
   si* la réponse distingue *reproductible* de *le plus probable*, et dit que la
   seed fige **un** chemin de tirage sans le rendre optimal.

## Ce que ça change dans le framework

Rien n'est promu **par cette leçon**. Le client
[`llm/ollama.py`](../../src/framework/llm/ollama.py) existe désormais, promu
par [chat, historique et contexte](chat-historique-contexte.md), mais il
transporte les options de sampling sans en imposer aucune. La brique que
cette leçon désigne est l'étage au-dessus : une fonction qui accepte
des options de sampling arbitraires et **impose un plafond de tokens par
défaut**, surchargeable. Les deux incidents ci-dessus disent pourquoi ce
garde-fou appartient au client et non à l'appelant — un oubli côté appelant
coûte un GPU bloqué. Elle ira dans `llm/` quand la leçon sera acquise et pas
seulement lue, avec l'exposition explicite de la seed, sans laquelle rien de ce
qui précède n'est reproductible.

## À retenir

- Le modèle produit une distribution, pas du texte ; tout le reste est un
  réglage appliqué après lui.
- Le softmax conserve l'ordre et amplifie les écarts : ces deux propriétés
  suffisent à prédire l'effet de la temperature.
- Les filtres décident qui participe, la temperature avec quels poids, le tirage
  qui sort — et un filtre qui ne laisse qu'un candidat annule la temperature.
- `num_predict` n'est pas un sampler : c'est la borne de la boucle, un garde-fou
  et non un réglage de style.
- Le tirage, c'est un nombre de PRNG comparé à des intervalles ; la seed n'agit
  que là, mais à chaque token, et son effet se propage par l'autorégression.
- Une sortie stable a quatre causes possibles ; seule la seed les discrimine.
- « Déterministe à `T=0` » n'est pas garanti : ex æquo, flottants, batching, MoE.

## Références

- 3Blue1Brown, série sur les transformers — l'intuition visuelle du softmax, et
  de ce que « amplifier les écarts » veut dire.
- L'API `/api/show` d'Ollama — lire les défauts de sampling qu'un modèle embarque
  avant de conclure quoi que ce soit d'une mesure.
