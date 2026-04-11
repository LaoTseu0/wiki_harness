# La mémoire du harnais

La mémoire est le cœur du harnais : c'est elle qui sépare un agent qui repart de zéro à chaque session d'un assistant qui connaît la personne qu'il sert. C'est aussi le sous-système le plus ambitieux, et celui où l'on se noie le plus vite si l'on confond ce qu'une mémoire *est*, *où* elle est rangée, et *comment* elle évolue.

Ce fichier fixe l'architecture. Il précède le découpage du Parcours 6.

## Trois axes, à ne pas confondre

Une idée de mémoire répond à trois questions distinctes. Les mélanger est ce qui produit le « grand magasin vectoriel fourre-tout » :

- **Le rôle** — à quoi elle sert. La question du *pourquoi*.
- **Le substrat** — où et comment elle est rangée. La question du *où*.
- **La dynamique** — comment elle naît, vieillit, meurt. La question du *quand*.

Un **magasin** est un rôle posé sur un substrat, avec sa méthode de rappel. Un **processus** est une dynamique qui s'exécute sur les magasins pour les entretenir. Tout le fichier tient dans ces deux mots.

Les quatre rôles cognitifs — travail, épisodique, sémantique, procédural — ne disparaissent pas : ils sont l'axe *rôle*. Ce qui manquait, c'étaient les deux autres axes. Les voici.

## Degré zéro : la mémoire de travail

La mémoire de travail, c'est la fenêtre de contexte elle-même — ce que le modèle a sous les yeux au tour en cours. Elle est déjà construite : c'est la brique `context` du Parcours 2. Elle ne se range nulle part et ne survit pas au tour. Tout le reste de ce fichier est de la mémoire **à long terme** : ce qui doit survivre à la fenêtre, donc être rangé dehors et rappelé dedans.

## Les magasins

| Magasin | Rôle | Substrat | Rappel |
|---|---|---|---|
| **Vectoriel** | le sens : faits, documents, dits passés | index d'embeddings (SQLite, puis Qdrant) | par similarité |
| **Stateful** | l'état exact : préférences, buts, état d'une tâche | clé-valeur / SQLite | par clé, déterministe |
| **Graphe temporel** | les entités et leurs liens dans le temps | graphe (nœuds, arêtes datées) | traversée + score + fenêtre de temps |
| **Wiki-LLM** | la connaissance consolidée, auto-rédigée | pages markdown liées + index | par titre, lien, puis similarité |

### Vectoriel — le rappel par le sens
Le RAG du Parcours 6, dans son rôle de mémoire : on transforme le texte en vecteur, on le range, on rappelle les plus proches. C'est flou par construction — on retrouve « ce qui ressemble », jamais « la valeur exacte de X ». D'où le magasin suivant.

### Stateful — le rappel par la clé
Tout ce qu'un rappel flou abîmerait : le prénom de l'utilisateur, la langue choisie, l'état d'une tâche en cours. On l'écrit sous une clé, on le relit à l'identique. Substrat : une table SQLite, ou un simple clé-valeur. Tenir la distinction vectoriel / stateful est le premier devoir du harnais — sinon il « se souvient à peu près » de ce prénom.

### Graphe temporel — les liens qui vieillissent
Les faits ne sont pas indépendants : *Alice travaille avec Bob*, *depuis mars*, *sur le projet X*. Un graphe le tient : nœuds (entités, événements), arêtes (relations datées). Deux mécanismes le rendent vivant :

- **le score** — chaque arête porte un poids : importance × fréquence de rappel.
- **le decay** — ce poids décroît avec le temps sans rappel, en exponentielle sur Δt. Ce qui ne ressert plus s'efface de soi-même ; ce qu'on réactive remonte.

C'est la courbe de l'oubli, mise en équation. Le rappel classe par score × pertinence, dans une fenêtre de temps.

### Wiki-LLM — la connaissance que l'agent s'écrit
L'idée, qu'on rattache à Karpathy : la mémoire la plus utile n'est pas le tas d'épisodes bruts, mais ce que l'agent en a *tiré*, rédigé, rangé. Le harnais tient un wiki — des pages markdown liées, qu'il écrit et relit — exactement comme ce dépôt de cours. Distinct du vectoriel : celui-ci rend des bouts bruts, le wiki rend une page triée, dédupliquée, qu'on peut relire d'un coup d'œil. C'est la mémoire sémantique, mais *rédigée* au lieu d'*accumulée*.

## Les processus

Sans entretien, un magasin grossit sans fin, et le rappel se dégrade : chaque recherche ramène de plus en plus de vieux souvenirs sans intérêt. Trois processus l'entretiennent. Ils lisent et modifient les magasins en tâche de fond, entre deux sessions.

### Scoring et decay — la courbe d'oubli
Pas réservé au graphe : tout élément de mémoire porte un score, qui décroît sans usage et remonte au rappel. Le rappel pondère par ce score ; ce qui tombe sous un seuil devient candidat à l'oubli. C'est ce qui empêche l'ancien de noyer le pertinent.

### La consolidation — le mode Dream
Entre deux sessions, une passe de « sommeil ». Elle **filtre** (jette le bruit), **fusionne** (déduplique), **promeut** (un épisode répété devient une page de wiki ; des faits épars deviennent une arête de graphe) et **oublie** (élague sous le seuil). C'est le processus qui transforme l'expérience brute en connaissance rangée — et qui déplace un souvenir d'un magasin vers un autre.

### L'auto-apprentissage — l'expérience devient procédure
Une trajectoire réussie est une procédure à garder ; une trajectoire échouée, un piège à ne pas refaire. L'auto-apprentissage distille les trajectoires (Parcours 8) en mémoire procédurale : des skills, ou des pages de wiki « comment faire X ». Le harnais s'améliore à l'usage, sans qu'on touche aux poids du modèle.

## La brique Hosef `memory`

Hosef expose une **interface de rappel commune** — `write`, `recall(requête, quand, budget)` — derrière laquelle les quatre magasins se branchent, et un **ordonnanceur** pour les processus (le Dream tourne sur planning). Substrat par défaut : **SQLite** — une extension vectorielle, une table d'état, une table de graphe, un seul fichier local — avec Qdrant en montée de charge. Hosef fournit les magasins et les processus ; le harnais décide ce qu'il consolide et quand lancer ces passes.

## Ce que ça impose au Parcours 6

Un ordre de construction, du sûr vers l'ambitieux, chaque marche mesurée avant la suivante :

1. **Vectoriel** — le RAG à la main, déjà prévu.
2. **Stateful** — la table SQLite, le rappel par clé.
3. **Graphe temporel** — nœuds, arêtes, la formule de decay.
4. **Wiki-LLM** — l'agent écrit et relit ses pages.
5. **Processus** — scoring / decay, puis le Dream, puis l'auto-apprentissage.

Les deux dernières marches sont à la frontière : on en construit une version minimale, on la mesure contre la mémoire sans elle, et on ne garde que ce qui fait mieux que la référence. Une mémoire savante ne se garde que si elle prouve qu'elle aide.

## Ce qui reste ouvert

- **Le wiki-LLM est-il un magasin ou la sortie de la consolidation ?** Posé ici comme magasin — l'agent y écrit directement — et le Dream y promeut aussi. À trancher : deux voies d'écriture, ou une seule.
- **Un score unique, ou un par magasin ?** Hypothèse de départ : une même formule, calibrée par magasin. Les mesures trancheront.
