# Garde-fous : l'agent naît confiné

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [la mini-boucle d'agent](../fondamentaux/boucle-agent.md)
  — les trois gardes posées à la main (périmètre, validation humaine, borne de
  tours), et surtout que les arguments produits par le modèle sont des **entrées
  non fiables**. Cette dernière propriété ressert partout ici : c'est parce qu'on
  ne fait confiance ni au modèle ni à ce qui l'influence qu'un garde-fou doit
  être une **contrainte** et non une consigne. [Le function calling](../fondamentaux/function-calling.md)
  — le cycle dont l'exécution d'un outil est le maillon qu'on vient border.
- **Débloque** : [les deux capacités du domaine suivant](outils-et-memoire.md)
  — un outil qui *agit* sur la maison ne s'accorde qu'une fois les deux
  périmètres en place. L'ordre n'est pas décoratif, c'est le sujet de cette
  leçon.

## L'essentiel

Un agent qui écrit sur le disque et lance des commandes ne se sécurise pas par
une couche finale ajoutée quand tout marche : **il naît confiné**. Le harnais
installe deux périmètres *avant* la première capacité — un périmètre logiciel
qui intercepte les appels d'outils ([hook `tool_call`](hook-tool-call.md)) et un
périmètre système qui borne le processus ([conteneur à moindre
privilège](conteneur-moindre-privilege.md)).

La thèse : la défense en profondeur n'est pas la **somme** des deux couches,
c'est leur **produit** — parce que leurs modes de défaillance sont indépendants.
Et l'**ordre** — garde-fous d'abord, capacités ensuite — n'est pas une bonne
manière parmi d'autres : c'est ce qui supprime la fenêtre pendant laquelle
l'agent pourrait tout faire.

Cette leçon ne détaille aucun des deux mécanismes — elle les situe l'un par
rapport à l'autre. L'interception fine est dans [le hook](hook-tool-call.md), le
confinement système dans [le conteneur](conteneur-moindre-privilege.md).

## Le savoir

### Deux périmètres, deux natures

Les deux couches ne filtrent pas la même chose, et c'est ce qui les rend
complémentaires plutôt que redondantes.

- **Le hook filtre ce que l'agent *demande*.** À chaque appel d'outil, notre
  code décide *avant* l'exécution. Contrôle fin — il voit la commande exacte et
  ses arguments — mais **logiciel**, donc contournable : si l'agent trouve un
  chemin d'action qui ne passe pas par un appel d'outil hooké, ou si la politique
  a un trou, le hook ne voit rien.
- **Le conteneur borne ce que le processus *peut*.** Volumes montés, utilisateur
  non-root, réseau interne : le processus ne *peut* physiquement pas lire un
  partage qui n'est pas monté ni joindre un hôte hors de son réseau. Contrôle
  grossier — il ne distingue pas une écriture légitime d'une écriture néfaste
  dans le même dossier — mais **infranchissable** à l'échelle où il agit.

Fin et contournable d'un côté, grossier et infranchissable de l'autre : aucune
des deux propriétés n'est celle qu'on voudrait seule.

### Pourquoi le produit, pas la somme

L'intérêt des deux couches tient à une propriété précise : **leurs défaillances
sont indépendantes**. Un bug dans la politique du hook — un motif oublié dans la
liste noire — ne donne aucun pouvoir supplémentaire sur les namespaces du
conteneur. Une tentative d'évasion du conteneur est hors de portée d'un
processus non-root aux capabilities retirées, *que le hook l'ait laissée passer
ou non*.

Le résultat se lit comme une multiplication : le hook rend l'abus
**improbable** (il faut trouver le trou dans la politique), le conteneur le rend
**impossible à l'échelle du système** (le trou trouvé ne mène nulle part). Pour
qu'un dégât sorte du périmètre, il faudrait franchir les deux en même temps — et
comme les deux barrières ne cèdent pas aux mêmes causes, la probabilité jointe
s'effondre. Une seule couche, aussi fine soit-elle, laisse toujours son propre
mode de défaillance ouvert.

### L'ordre est une décision de conception

« Sécurité d'abord » se traduit littéralement dans l'ordre où les pièces
arrivent. Accorder l'outil qui agit *puis* brancher les garde-fous ouvre une
fenêtre — courte peut-être, mais réelle — pendant laquelle l'agent dispose de la
capacité sans la contrainte. L'ordre inverse n'a pas de fenêtre : tant que le
hook et le conteneur ne sont pas en place, aucune capacité effectrice n'existe.

C'est tout ce que veut dire « l'agent naît confiné » : non pas un slogan, mais
l'absence de cet intervalle. Le même raisonnement gouverne l'organisation du
domaine — on pose les bornes, ensuite seulement on donne
[l'outil qui agit](outils-et-memoire.md).

## Quand c'est la bonne réponse

**Les deux couches** dès qu'un agent exécute des outils à **effet de bord** sur
un système réel — fichiers, commandes, API domotique. C'est exactement le
passage de « lire » à « agir » de la [mini-boucle](../fondamentaux/boucle-agent.md),
et c'est là qu'il devient dangereux parce que rien dans le code ne signale
qu'on a franchi la ligne.

**Le conteneur seul, hook au repos**, pour un agent purement lecture ou
génération sans effet de bord : il n'y a pas d'action à suspendre, donc la
décision `ask` du hook ne se déclenche jamais — mais le processus reste borné,
parce qu'un bug ou une injection peut toujours tenter d'élargir ce périmètre.

**Ni l'un ni l'autre** quand un humain relit et lance chaque action lui-même :
il n'y a plus d'agent autonome, la validation est en amont et non dans un hook.
Mais alors on a renoncé à l'autonomie, ce qui est un autre projet — pas une
manière de se passer de garde-fous.

## Ce qu'on ne saura pas faire

Cette leçon situe les deux périmètres ; elle ne les construit pas. Le mécanisme
de l'interception est dans [le hook](hook-tool-call.md), celui du confinement
dans [le conteneur](conteneur-moindre-privilege.md). Elle ne mesure pas non plus
le **rayon d'une compromission** — c'est le test d'évasion de la leçon conteneur
qui le rend concret.

Ce qui promouvrait ce domaine en « refaire » : une étape sous `wiki/etapes/agent/`
qui intercepte réellement les appels et un test d'évasion du conteneur, avec le
`deny` et le log observés plutôt qu'affirmés.

## Se tester

1. On vous dit que le hook filtre déjà tout ce que l'agent demande — pourquoi
   garder un conteneur en plus ?
   *Réussi si* la réponse oppose deux modes de défaillance indépendants : le
   hook est logiciel donc faillible et contournable (chemin non hooké, motif
   oublié), le conteneur borne physiquement ce que le hook raterait — et note
   que c'est leur produit, pas leur somme, qui fait la défense.
2. Une équipe propose de livrer l'outil d'action tout de suite et de « brancher
   les garde-fous juste après ». Qu'est-ce que cet ordre ouvre ?
   *Réussi si* la réponse nomme la fenêtre où l'agent dispose de la capacité
   sans la contrainte, et explique que l'ordre inverse n'a pas de fenêtre parce
   qu'aucune capacité effectrice n'existe tant que les bornes ne sont pas là.
3. Un agent ne fait que lire de la documentation et répondre. Laquelle des deux
   couches gardez-vous, et laquelle ne sert plus ?
   *Réussi si* la réponse garde le conteneur (il borne le processus quoi qu'il
   arrive) et constate que l'`ask` du hook reste inactif faute d'action à
   valider — sans conclure qu'un agent lecture est sans risque.

## À retenir

- Un agent qui agit naît confiné : les deux périmètres se posent avant la
  première capacité, jamais après.
- Le hook filtre ce que l'agent demande (fin, contournable) ; le conteneur borne
  ce que le processus peut (grossier, infranchissable).
- La défense en profondeur est le produit des deux, pas leur somme, parce que
  leurs défaillances sont indépendantes.
- L'ordre garde-fous → capacités supprime la fenêtre pendant laquelle l'agent
  agirait sans borne ; l'ordre inverse la laisse ouverte.

## Références

- [securite.md §5 du homelab](../../../../homelab/architecture/securite.md) —
  les non-négociables d'origine, dont ces deux périmètres sont la traduction
