# Sampling et prompting

> Fiche reformulée. Principe directeur : rien ici n'est récité depuis un manuel. L'ordre des samplers et les comportements limites ont été **mesurés au notebook 04** (moteur `llama.cpp`, donc Ollama), parce que les présentations « manuel » se contredisent entre elles et avec les moteurs réels.

---

## 0. Prérequis — des logits aux probabilités

Tout le sampling manipule deux objets que le reste du cours suppose connus. On les pose d'abord, sinon la phrase « la temperature divise les logits avant le softmax » ne veut rien dire.

**Les logits.** La dernière couche du modèle produit, à chaque étape, un score brut par token du vocabulaire. Ce sont les *logits*. Ils ne sont pas normalisés : ils peuvent être négatifs, positifs, grands ou petits. Impossible de les lire comme des probabilités en l'état.

**Le softmax.** C'est la fonction qui transforme ces scores bruts en une vraie distribution de probabilités — chaque valeur entre 0 et 1, somme égale à 1 :

$$\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

Deux étapes : on applique l'exponentielle à chaque logit (tout devient positif, et les écarts sont *amplifiés*), puis on divise par la somme totale (normalisation).

Deux propriétés à retenir, elles reviennent partout ensuite :

- **L'ordre est conservé** — le plus gros logit reste la plus grosse probabilité. Le softmax ne change pas *qui* gagne.
- **Les écarts sont accentués** — à cause de l'exponentielle, un logit un peu supérieur aux autres se retrouve avec une probabilité *nettement* supérieure. Un écart de 1 en logits peut devenir un rapport de 3 en probabilités.

---

## 1. La chaîne de sampling

### L'ordre d'application (le point central)

L'ordre réel, mesuré au notebook, est une **chaîne de samplers propre au moteur**, pas la séquence des manuels :

```
logits → top-k → top-p → temperature → tirage
```

Les présentations « manuel » placent souvent la temperature *avant* les filtres. Sur `llama.cpp`/Ollama, c'est l'inverse, et l'ordre est parfois configurable. Conséquence pratique : on ne récite pas cet ordre, on le vérifie sur son propre moteur — c'est exactement la raison pour laquelle on le mesure au notebook.

### `temperature` — régler l'assurance du modèle

La temperature divise chaque logit par un nombre $T$ **avant** le softmax :

$$\text{softmax}(z_i / T)$$

Elle ne change pas qui a le plus gros score ; elle change à quel point la distribution est tranchée.

| $T$ | Effet sur la distribution | Comportement |
|---|---|---|
| $T \to 0$ | piquée sur le gagnant (quasi-`argmax`) | sûr, répétitif |
| $T = 1$ | softmax standard | équilibré |
| $T$ élevée | aplatie, probabilités égalisées | créatif, instable |

Aux limites : $T \to 0$ tend vers l'`argmax` (toujours le token le plus probable), $T \to \infty$ tend vers une distribution uniforme (choix au hasard pur).

**« Déterministe » à $T=0$ n'est pas garanti.** Même en visant l'`argmax`, plusieurs sources peuvent faire diverger la sortie :

- **égalités de probabilités** — deux tokens au même score, le départage dépend de l'implémentation ;
- **ordre des opérations flottantes** — sur GPU, des milliers d'additions parallèles ne se somment pas toujours dans le même ordre, ce qui décale infimement les logits. Rarement visible, mais suffisant pour casser une reproductibilité *bit à bit* d'une machine à l'autre ;
- **batching** — la composition du lot peut modifier ces mêmes ordres de calcul.

Ce non-déterminisme-là n'est pas de l'aléa « voulu » : c'est un artefact matériel, distinct du tirage aléatoire décrit plus bas.

### `top-k` — couper la longue traîne

Ne garder que les **k tokens les plus probables** avant de tirer. Élimine la longue traîne de tokens absurdes qui, cumulés, finiraient par sortir de temps en temps. Seuil **fixe** : toujours k candidats, quelle que soit la forme de la distribution.

### `top-p` (nucleus) — le seuil adaptatif

Garder le **plus petit ensemble de tokens dont la probabilité cumulée atteint $p$**. Contrairement à top-k, la taille du filtre s'adapte : quelques candidats quand le modèle est sûr (une case domine), beaucoup quand il hésite (distribution plate). C'est le complément adaptatif de top-k.

### `repetition penalty` — casser les boucles

Pénalise les tokens **déjà émis** en abaissant leurs logits. Évite les boucles et les répétitions mécaniques où le modèle se verrouille sur une même formule.

### `num_predict` — le garde-fou

Plafond du nombre de tokens générés. À fixer **systématiquement** : l'incident « génération débridée » du notebook a montré ce qui se passe sans lui — le modèle ne s'arrête pas de lui-même dans certains cas.

---

## 2. Le tirage — comment on « choisit au hasard »

Une fois la distribution filtrée et tempérée, il faut en extraire *un* token. Deux briques entrent en jeu.

**L'échantillonnage par intervalles (méthode de la roulette).** On aligne les probabilités bout à bout sur le segment $[0, 1)$. Chaque token occupe une case proportionnelle à sa probabilité. On tire un nombre dans $[0, 1)$ et on lit dans quelle case il tombe. Sur de nombreux tirages, un token de probabilité 0,69 sort ~69 % du temps, puisque sa case occupe 69 % du segment. La distribution ne « décide » rien : c'est la taille des cases qui fait tout.

**Le nombre tiré vient d'un PRNG.** Ce n'est pas du vrai hasard, mais un générateur *pseudo*-aléatoire : un algorithme déterministe qui, à partir d'un état initial (la **seed**), produit une suite de nombres qui passent les tests statistiques d'aléa tout en étant entièrement reproductibles.

**Portée de la seed** — le point souvent mal compris :

- elle n'agit qu'à **une seule étape**, le tirage. La passe dans le réseau (logits) et le softmax sont déterministes ;
- mais elle agit à **chaque token généré** : le PRNG produit une suite, la seed en fixe le point de départ ;
- et son effet **se propage en cascade** : le token tiré est réinjecté dans le contexte (autorégression), ce qui modifie les logits du token suivant. Une seule graine différente peut faire diverger toute la phrase ;
- son effet dépend de la température : à $T=0$ (pas de tirage) la seed n'a **aucun** effet ; à basse température elle agit mais un token domine, donc le résultat bouge peu ; à haute température, changer de graine fait facilement basculer le choix.

À seed fixée + température + prompt identiques, la génération est reproductible (aux artefacts flottants près). C'est pourquoi beaucoup d'API exposent un paramètre `seed`.

![[ou-agit-la-seed.canvas]]

---

## 3. Prompting

Les techniques nommées ci-dessous portent les termes qu'on retrouve tels quels dans les offres et les docs.

### `zero-shot` / `few-shot`

- **zero-shot** : la consigne seule, sans exemple.
- **few-shot** : la consigne accompagnée d'exemples. Point clé : **le format des exemples *est* la spécification**. Le modèle imite la forme autant que le fond — un format d'exemple bâclé produit une sortie bâclée.

### `chain-of-thought` (CoT)

Demander les **étapes de raisonnement avant la réponse**. Améliore nettement le raisonnement sur les tâches à plusieurs étapes, au prix de tokens supplémentaires (donc de latence et de coût). Arbitrage qualité / coût à assumer.

### `ReAct`

Alterner **raisonnement et action** (Reason + Act). C'est le pattern derrière toutes les boucles d'agent — voir la [mini-boucle agent](../1.1.4-mini-boucle-agent/1.1.4-mini-boucle-agent.md). Le modèle réfléchit, agit (appel d'outil), observe le résultat, puis recommence.

### Prompt système

Fixe le **rôle**, les **contraintes d'entrée/sortie** et le **format** attendu. C'est le cadre stable dans lequel s'inscrivent les messages suivants.

---

## À retenir en une phrase par bloc

- **Sampling** : les filtres (top-k, top-p) taillent la distribution, la temperature en règle le tranchant, le tirage en extrait un token — dans un ordre propre au moteur, à mesurer soi-même.
- **Tirage** : un PRNG piloté par la seed fournit un nombre, la méthode des intervalles le convertit en token ; la seed n'agit qu'au tirage mais se propage à toute la suite.
- **Prompting** : de la consigne nue (zero-shot) à la boucle raisonnement/action (ReAct), le format qu'on montre au modèle est la spécification qu'il suit.
