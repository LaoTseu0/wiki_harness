# Régimes d'agents : une boucle, plusieurs exploitations

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la mini-boucle d'agent](../fondamentaux/boucle-agent.md)
  — la boucle réfléchir / agir / observer, l'invariant dont on va comparer les
  régimes ; [les garde-fous](garde-fous.md) et [outils et mémoire](outils-et-memoire.md)
  — ce que tout régime doit reprendre à son compte, quel que soit qui écrit la
  boucle.
- **Débloque** : rien de neuf en capacité — c'est le zoom arrière du domaine.
  Mais le régime retenu conditionne [la note de conception](note-de-conception.md),
  qui doit justifier le choix.

## L'essentiel

La même boucle d'agent existe sous **quatre régimes** — manuelle, harnais, SDK,
graphe — et selon **deux modes de vie** — éphémère ou persistant. Savoir les
situer, c'est savoir défendre un choix d'architecture plutôt que le subir.

La thèse : la **boucle est un invariant, le régime est un choix d'exploitation**.
Ce qui change d'un régime à l'autre n'est pas la mécanique réfléchir → agir →
observer — elle est identique partout — mais ce que chacun **prend en charge** et
ce qu'il **confisque**. Et le choix se défend par des critères — contrôle,
observabilité, coût d'entrée —, jamais par la mode.

Cette leçon ne réimplémente aucun régime : le comparatif détaillé est dans
[quatre régimes, même boucle](quatre-regimes.md), le mode persistant dans [mode
RPC/SDK](mode-rpc-sdk.md), et la capitalisation du tout dans [la note de
conception](note-de-conception.md).

## Le savoir

### La boucle est l'invariant

Réfléchir → agir → observer se retrouve à l'identique dans les quatre régimes.
Ce qui diffère, c'est la **répartition du travail** entre nous et le régime : qui
écrit la boucle, qui trace les appels, qui insère les garde-fous. Nommer
l'invariant est précisément ce qui rend la comparaison possible — on ne compare
pas des boucles différentes, on compare des répartitions d'un même travail.

### Le régime est un choix d'exploitation, défendable par critères

Trois critères suffisent à situer un régime, et ce sont eux qu'on oppose à la
mode.

- **Le contrôle** : qui écrit la boucle, et comment on y insère un garde-fou —
  soi-même (manuel), via des hooks (harnais), via des callbacks (SDK), en
  déclarant un flux (graphe).
- **L'observabilité** : ce qu'on voit quand ça rate — tout, si c'est notre code ;
  ce que le régime veut bien exposer, sinon.
- **Le coût d'entrée** : ce qu'il faut apprendre et écrire avant d'obtenir un
  agent qui tourne.

Le détail chiffré par le vécu est le sujet de [quatre régimes](quatre-regimes.md) ;
ici, il suffit de retenir que le choix suit le besoin, et qu'un besoin se nomme
avec ces trois axes.

### Éphémère ou persistant, une seconde dimension

Le mode de vie est **orthogonal** au régime : n'importe lequel des quatre peut
vivre le temps d'une session, ou tenir un service ouvert. Le passage à
persistant ne change pas la boucle non plus — il déplace la gestion de contexte
et le human-in-the-loop vers des formes **asynchrones**, ce qui est le sujet de
[mode RPC/SDK](mode-rpc-sdk.md). Confondre les deux dimensions — croire qu'un SDK
« est » persistant, ou qu'un harnais « est » interactif — fait rater la moitié
des combinaisons possibles.

## Quand c'est la bonne réponse

- **Manuel** pour comprendre, ou pour des besoins très spécifiques que le contrôle
  total justifie malgré son coût.
- **Harnais** pour l'interactif outillé et le développement quotidien.
- **SDK** pour embarquer un agent dans un produit.
- **Graphe** pour un workflow multi-étapes contraint, avec reprise sur état.

Et sur l'autre dimension : **persistant** seulement quand un déclencheur
non-humain le justifie — un événement domotique plutôt qu'un humain au clavier —
ou quand le contexte partagé entre requêtes a une vraie valeur. Sinon l'éphémère
coûte moins : pas de dérive de session, pas de human-in-the-loop asynchrone à
concevoir.

## Ce qu'on ne saura pas faire

Cette leçon situe ; elle ne fait tourner aucun régime. Le comparatif ne vaut que
rempli avec le vécu, sur une même tâche — c'est le travail de
[quatre régimes](quatre-regimes.md).

Ce qui promouvrait ce groupe en « refaire » : le même agent à quelques outils
refait dans les quatre régimes, et un tableau contrôle / observabilité / coût
rempli par mesure et non par recopie de documentation.

## Se tester

1. On vous demande de trancher entre « framework d'agents » et « boucle maison ».
   Quelle est la vraie question ?
   *Réussi si* la réponse voit que les deux ne s'excluent pas — même boucle en
   dessous — et déplace le débat vers des critères (contrôle, observabilité, coût
   d'entrée), un régime se pratiquant tandis que les autres se situent.
2. On vous confie un bot de triage de mails. Quel régime prenez-vous, et sur quoi
   fondez-vous le choix ?
   *Réussi si* la réponse justifie par les trois critères (par exemple harnais ou
   SDK selon qu'on l'embarque dans un produit), pas par la popularité d'un outil.
3. Qu'est-ce qui distingue un agent éphémère d'un agent persistant, et de quel
   axe relève cette distinction ?
   *Réussi si* la réponse identifie le cycle de vie — orthogonal au régime — qui
   déplace la gestion de contexte et le human-in-the-loop vers des formes
   asynchrones.

## À retenir

- La boucle réfléchir/agir/observer est l'invariant ; le régime est un choix
  d'exploitation qui redistribue le même travail.
- Trois critères situent un régime : contrôle, observabilité, coût d'entrée — et
  ils battent la mode.
- Éphémère / persistant est une dimension orthogonale au régime, pas une
  cinquième option.
- Le choix se défend, il ne se subit pas : un régime se pratique, les autres se
  situent.

## Références

- [architecture/jarvis.md du homelab](../../../../homelab/architecture/jarvis.md)
  — le projet dont ce domaine construit l'agent
