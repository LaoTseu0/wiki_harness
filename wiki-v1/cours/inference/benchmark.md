# Un benchmark honnête

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [servir un modèle](deploiement.md) — les deux moteurs
  déployés derrière la même API, sans quoi il n'y a rien à comparer
  équitablement. La règle de mesure du repo, aussi : *un pipeline LLM sans
  évaluation chiffrée est une démo* ([carte](../carte.md)).
- **Débloque** : le choix de [quelles métriques collecter](metriques-debit-latence.md)
  et de [comment charger](charge-concurrente.md) ; puis
  [l'analyse](analyse-et-verdict.md), qui explique la courbe que ce cadre
  produit.

## L'essentiel

Chiffrer, pas ressentir. Mais chiffrer mal est pire que ne pas chiffrer, parce
qu'un chiffre inspire une confiance qu'une impression n'obtient pas. La thèse de
cette leçon tient en deux propositions qu'on peut contredire :

1. **Le livrable d'un benchmark est une courbe, pas un vainqueur.** À une
   requête, deux moteurs se valent ; c'est la montée en charge qui les sépare.
   Un « X est plus rapide que Y » cache le régime où c'est vrai et celui où
   c'est faux.
2. **Un chiffre de performance sans ses conditions ne se compare à rien.**
   « 40 tokens/s » ne veut rien dire sans le modèle, la quantisation, la
   longueur de prompt et le nombre de requêtes concurrentes qui l'ont produit.

Cette leçon porte la **discipline** de la mesure. Elle ne dit pas *quelles*
métriques collecter — c'est [débit et latence](metriques-debit-latence.md) — ni
*comment* fabriquer la charge — c'est [la charge concurrente](charge-concurrente.md).
Elle dit pourquoi, sans ces deux-là faits correctement, aucun chiffre ne tient.

## Le savoir

### Définir les métriques avant de mesurer, et pourquoi l'ordre compte

Décider ce qui compte *après* avoir vu les résultats, c'est se donner le droit de
choisir la métrique qui arrange la conclusion. Le même bench « prouve » alors
tout et son contraire selon qu'on regarde le débit ou la latence.

Fixer les métriques *avant* est ce qui rend le résultat réfutable : on annonce ce
qu'on va regarder, et on le regarde quoi qu'il dise. C'est la différence entre une
mesure et une plaidoirie. Le mécanisme est le même que celui d'une prédiction
écrite avant l'exécution — sa valeur vient de ce qu'elle peut être démentie.

### Un chiffre voyage avec ses conditions, sinon il ne voyage pas

Un débit de génération dépend d'au moins quatre grandeurs hors du moteur : le
modèle et sa quantisation, la longueur du prompt (qui détermine le coût du
prefill), le plafond de tokens générés, et la concurrence. Deux de ces quatre
changent d'un moteur à l'autre par défaut — les templates de chat diffèrent, donc
le nombre de tokens du prompt aussi.

La conséquence pratique est une règle : **on fixe et on publie ces conditions
avec chaque chiffre**. Un tableau de résultats sans sa colonne de conditions
n'est pas une mesure comparable, c'est une anecdote datée. Et l'oubli le plus
coûteux est le silencieux : comparer deux moteurs sur des prompts de longueurs
différentes fait attribuer au moteur un écart qui venait du prompt.

### Le livrable est une courbe, parce que la vérité est un régime

Un moteur peut exceller à une requête et s'effondrer à vingt, ou l'inverse. Un
seul point de mesure ne capture pas cela ; il fige un régime et le fait passer
pour la règle. La courbe — une métrique en fonction de la concurrence — est le
seul objet qui montre *où* passe la frontière entre les deux régimes, et c'est
cette frontière qui porte la décision.

D'où le protocole en trois points de charge (typiquement 1, 5, 20 requêtes
simultanées) plutôt qu'un seul : trois points suffisent à révéler une pente et
une éventuelle cassure, là où un point n'affirme rien.

### Deux causes pour « les deux moteurs donnent le même chiffre »

Symptôme identique — la mesure ne sépare pas les moteurs — et deux origines
opposées :

- **On mesure au mauvais point de charge.** À une seule requête, les moteurs se
  ressemblent par construction : rien ne discrimine tant qu'il n'y a pas de file.
  La correction est de monter en concurrence, pas de changer de métrique.
- **La métrique ne capte pas la différence.** Le débit par requête peut masquer
  un écart qui n'apparaît que sur le débit *agrégé*. La correction est de
  regarder la bonne grandeur, définie à l'avance.

Ce qui les distingue : refaire la mesure à concurrence élevée. Si l'écart
apparaît, c'était le point de charge ; s'il reste absent, c'est la métrique — ou
les moteurs sont réellement équivalents pour cet usage, ce qui est aussi un
résultat.

## Quand c'est la bonne réponse

**Bencher** quand une décision dépend du résultat et que les fiches techniques ne
la tranchent pas. Sans décision en jeu, mesurer est un exercice.

**Publier une courbe** dès que la concurrence fait partie de la question. C'est
presque toujours le cas pour un serveur, presque jamais pour un script local
mono-usager.

**Se contenter d'un point** uniquement quand l'usage cible est un point — un seul
utilisateur, un seul profil de requête. Alors la courbe est un luxe, mais les
conditions restent obligatoires.

## Ce qu'on ne saura pas faire

Le script de charge n'est pas écrit et aucune courbe n'a été produite : tout ce
qui précède est une méthode, pas un résultat. On ne sait donc pas encore quelle
forme prennent réellement les courbes sur cette carte — seulement quelles
propriétés une mesure doit avoir pour être défendable.

Ce que ça laisse ouvert : combien de salves et combien de points de charge
suffisent pour que la variance à forte concurrence ne noie pas le signal ; c'est
une question qui ne se tranche qu'en voyant la dispersion réelle.

Ce qui promouvrait cette leçon en « refaire » : le script de charge sous
`etapes/inference/`, versionné, et les trois courbes produites avec leur colonne
de conditions — le moment où la discipline cesse d'être une consigne pour devenir
une figure.

## Se tester

1. Un README annonce « notre serveur fait 45 tokens/s ». Que manque-t-il pour que
   ce chiffre serve à quelqu'un d'autre ?
   *Réussi si* la réponse réclame les conditions — modèle, quantisation, longueur
   de prompt, concurrence — et note que sans elles le chiffre ne se compare à
   rien.
2. On vous propose de choisir la métrique à mettre en avant une fois les mesures
   faites, « pour raconter une histoire claire ». Où est le piège ?
   *Réussi si* la réponse identifie le choix a posteriori comme ce qui rend le
   bench non réfutable, et exige de fixer les métriques avant de mesurer.
3. À une requête, Ollama et vLLM donnent le même débit. Peut-on conclure qu'ils
   se valent ?
   *Réussi si* la réponse refuse de conclure, rattache l'égalité au point de
   charge (rien ne discrimine sans file), et demande la courbe sous concurrence.

## À retenir

- Le livrable d'un benchmark est une courbe, pas un vainqueur : la vérité est un
  régime, et un point unique le fige en règle.
- Un chiffre de performance voyage avec ses conditions — modèle, quantisation,
  longueur de prompt, concurrence — ou ne voyage pas.
- Définir les métriques avant de mesurer est ce qui rend le résultat réfutable,
  comme une prédiction écrite avant l'exécution.
- « Les deux moteurs donnent le même chiffre » a deux causes : mauvais point de
  charge, ou mauvaise métrique — la mesure à forte concurrence les sépare.

## Références

- [Débit et latence](metriques-debit-latence.md) — les métriques que ce cadre
  suppose définies d'avance
- [Charge concurrente](charge-concurrente.md) — la charge réaliste et
  reproductible que ce cadre exige
- [Analyse et verdict](analyse-et-verdict.md) — ce qu'on fait de la courbe une
  fois honnête
