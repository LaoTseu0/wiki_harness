# La promotion

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : au moins une leçon dont l'étape tourne — sinon il n'y
  a rien à promouvoir. [Architecture modulaire](architecture-modulaire.md)
  pour savoir où une brique atterrit.
- **Débloque** : la règle 2 de la [carte](../carte.md) — « une leçon acquise
  laisse du code dans `src/framework/` ». Sans mécanisme, cette règle est un
  vœu ; avec, c'est ce qui empêche le cours d'être une collection de textes.

## L'essentiel

Une étape et une brique de framework n'ont pas le même métier, et **le même
fichier ne peut pas faire les deux**. L'étape existe pour qu'un mécanisme
devienne évident : elle a des `print`, des trous, des constantes en haut, un
`while True` qui lit l'entrée standard. La brique existe pour être rappelée
par du code qui ne sait rien de la leçon : elle n'affiche rien, ne décide
rien, et rend des données.

La promotion est le passage de l'un à l'autre. Ce n'est ni une copie ni un
refactoring cosmétique : c'est la relecture qui **révèle ce que le script
laissait passer**, parce qu'un script qu'on regarde tourner masque ce qu'un
test rendrait visible.

Cette leçon ne couvre pas *où* range la brique — c'est
[architecture modulaire](architecture-modulaire.md) — ni *quand on publie*,
qui est [sortie précoce et semver](sortie-precoce-semver.md).

## Le savoir

### Le critère d'entrée n'est pas « la leçon est lue »

Une brique monte quand le code écrit à la main tourne **et** qu'on sait dire
pourquoi chaque ligne est là. Le deuxième membre fait tout le travail : il
disqualifie le code recopié qui marche. Tant qu'une ligne est là « parce que
sinon ça plante », la leçon n'est pas acquise et la brique attendra.

Ce critère se vérifie tout seul à l'écriture des tests. Un mécanisme compris
se teste ; un mécanisme recopié produit des tests qui rejouent
l'implémentation ligne à ligne, ce qui ne prouve rien.

### Ce que la promotion retire

Trois choses, toujours les mêmes :

- **l'affichage** — un `print` dans une brique est une décision prise à la
  place de l'appelant ;
- **les globales de module** — l'étape lit `MODEL` et `OLLAMA_URL` en haut du
  fichier ; la brique les reçoit, sinon elle n'est utilisable qu'une fois par
  processus ;
- **les trous d'exercice** — le squelette à compléter appartient à l'étape,
  qui reste en place et garde ses trous pour la personne suivante.

### Ce que la promotion ajoute — et qui n'était pas visible avant

C'est le point non évident. Réécrire pour rendre testable **déplace la
frontière entre transport et logique**, et ce déplacement fait apparaître les
défauts.

Dans [`llm/ollama.py`](../../src/framework/llm/ollama.py), le parsing a été
séparé de l'appel HTTP (`Reponse.depuis_ollama`, `morceaux_ndjson`) pour être
testable sans serveur. La séparation faite, une question se pose qu'aucun
script ne posait : que vaut un tour dont Ollama ne renvoie pas les compteurs ?
L'étape affichait `"?"` et passait à la suite ; la brique doit choisir, et le
choix se documente.

Dans [`contexte.py`](../../src/framework/contexte.py), deux défauts du script
n'ont survécu à aucun test :

- `tronquer` prenait la tranche sur la liste entière. Sur une conversation
  plus courte que le seuil, la tranche reprend le message system, qu'on
  reconcatène ensuite devant : le contexte le paye deux fois. Invisible à
  l'œil, immédiat dans un test à trois messages.
- `compacter` repartait de l'historique complet. À la deuxième compaction, le
  résumé précédent redevenait matière à résumer — la dérive cumulative que la
  leçon [chat, historique et contexte](../fondamentaux/chat-historique-contexte.md)
  annonce. La brique transporte le résumé acquis à part, et ne soumet au
  modèle que les tours nouveaux.

Aucun des deux n'a été trouvé en lisant le script. Les deux ont été trouvés
en écrivant l'assertion.

### Ce qui disqualifie une brique

- **Elle n'a qu'un usage.** L'interface attend le *deuxième* usage concret —
  un `Protocol` avec une seule implémentation décrit cette implémentation, pas
  un contrat. C'est pourquoi `llm/` ne contient qu'`ollama.py` et aucune
  classe de base : le deuxième provider n'existe pas encore.
- **On ne peut pas la nommer sans raconter la leçon.** Si le nom du module
  doit être `demo_de_ce_qui_se_passe_quand`, ce n'est pas une brique.
- **Elle décide à la place de l'appelant.** Une brique qui choisit un modèle,
  un seuil ou une stratégie impose la leçon à tout le code qui l'appelle.

### La dépendance se paramètre, elle ne s'importe pas

`compacter` a besoin d'un appel au modèle. La version étape appelait la
fonction `appeler()` du même fichier ; la brique reçoit une fonction de
résumé. Ce n'est pas de la pureté d'école : c'est ce qui permet de tester le
comportement anti-dérive **sans serveur**, en passant une fonction qui note ce
qu'on lui a soumis. Une brique qui importe son fournisseur ne se teste qu'en
l'ayant sous la main.

## Quand c'est la bonne réponse

**Promouvoir** quand un deuxième endroit du cours va rappeler le même
mécanisme, et qu'on sait dire lequel. Le RAG rappellera le client LLM ; la
boucle d'agent rappellera la gestion de contexte.

**Ne pas promouvoir** quand la leçon produit du savoir et pas du code —
[attention et KV cache](../fondamentaux/attention-et-kv-cache.md) ne laisse
aucune fonction, seulement une contrainte sur l'ordre d'un prompt. La rubrique
« ce que ça change dans le framework » se remplit alors d'une phrase qui dit
pourquoi rien ne monte. C'est une réponse valide, pas un aveu.

**Attendre** quand la brique est identifiée mais que le deuxième usage
n'existe pas. L'écrire d'avance, c'est deviner l'interface dont on aura
besoin, et se tromper.

## Ce qu'on ne saura pas faire

Cette leçon ne dit pas comment une brique **évolue** une fois promue : ce que
coûte un changement d'interface quand trois domaines l'appellent déjà, et
comment on le fait sans tout casser. C'est
[évolutivité sans friction](evolutivite.md), et ça ne se traite qu'avec
plusieurs consommateurs réels — donc pas encore.

Elle ne dit pas non plus quand une brique **redescend** : le cas où le code
promu s'avère faux ou inutile, et ce qu'on fait de la leçon qui l'annonçait.

## Se tester

1. Une étape tourne et donne le bon résultat, mais son auteur ne sait pas dire
   pourquoi une ligne est là. Promouvoir ou pas ?
   *Réussi si* la réponse porte sur le critère d'entrée — la ligne inexpliquée
   suffit à bloquer, quel que soit le résultat.
2. Vous promouvez une fonction qui a besoin d'appeler le modèle. Deux
   conceptions s'offrent : importer le client, ou le recevoir. Laquelle, et
   quel test devient possible ?
   *Réussi si* la réponse nomme le test qui n'exige pas de serveur, pas
   seulement « c'est plus propre ».
3. Vous avez un client Ollama qui marche. Faut-il écrire l'interface
   `ClientLLM` maintenant ?
   *Réussi si* la réponse tient au nombre d'implémentations existantes, et
   dit ce que décrirait un `Protocol` écrit à une seule.

## À retenir

- L'étape et la brique ont deux métiers : l'une montre, l'autre sert.
- Le critère d'entrée est « on sait dire pourquoi chaque ligne est là », pas
  « ça tourne ».
- Rendre testable déplace la frontière transport/logique, et c'est ce
  déplacement qui fait apparaître les défauts du script.
- L'interface attend le deuxième usage concret.
- La dépendance se reçoit en paramètre, pour que le test n'ait pas besoin du
  serveur.

## Références

- [Architecture modulaire](architecture-modulaire.md) — les briques et le sens
  de leurs dépendances
- [Sortie précoce et semver](sortie-precoce-semver.md) — ce qu'on fait de la
  brique une fois montée
- [`src/framework/README.md`](../../src/framework/README.md) — l'adresse et
  ce qui y est arrivé
