# Structured output

> [carte du cours](../carte.md) · étape : [`08_structured.py`](../../etapes/fondamentaux/08_structured.py)

## Où ça s'emboîte

- **Processus** : [d'une tâche à un résultat](../_processus/boucle-outils.md)
- **L'étape ouverte** : `schema` · `contrainte` — entre une classe Pydantic, sort le jeu des tokens que la génération a encore le droit de produire

![[structured-output.canvas]]

## Prérequis et suites

- **Suppose acquis** : [le sampling](sampling.md) — et précisément que le
  modèle rend un [logit](../glossaire/logits.md) **par token du vocabulaire**,
  que le [softmax](../glossaire/softmax.md) normalise sur ce qui reste, et que
  le tirage n'a lieu qu'à la toute fin ; [la tokenisation](tokenisation.md) —
  un token est un morceau de texte de longueur variable, pas un caractère. Ces
  trois propriétés resservent : la première explique comment une grammaire
  s'impose sans rien changer au modèle, la deuxième pourquoi contraindre
  *déplace* les probabilités au lieu de les élaguer, la troisième pourquoi la
  même contrainte ne produit pas le même effet sur deux modèles.
- **Débloque** : [le function calling](function-calling.md), dont le champ
  `tools` est le même mécanisme sous un autre nom ; toute brique qui rend des
  données à du code plutôt qu'à un humain — [les evals](../retrieval/evals.md),
  [le LLM-as-judge](../framework/llm-as-judge.md).

## L'essentiel

Dès qu'un LLM alimente du code, sa sortie doit être **du JSON valide et
conforme à un schéma**, pas « à peu près du JSON ». Trois régimes existent, et
la leçon affirme qu'aucun ne remplace les deux autres : demander poliment
n'obtient rien de fiable, contraindre le décodage garantit **la forme et
seulement la forme**, valider après coup est le seul endroit où le *sens* peut
être vérifié.

Le corollaire est la partie qui se retient mal : un JSON impeccable à l'écran
ne prouve rien sur le modèle qui l'a produit, parce que deux mécanismes très
différents produisent exactement la même sortie. Savoir lequel on regarde
change ce qu'on peut en conclure.

Cette leçon ne couvre pas ce qu'on *fait* du schéma une fois l'objet obtenu —
le dispatch et l'exécution sont [le function calling](function-calling.md) — ni
la validation du contenu par un autre modèle, qui est
[le LLM-as-judge](../framework/llm-as-judge.md).

## Le savoir

### Les trois régimes, et ce que chacun ne peut pas faire

**Demander poliment.** Une consigne dans le prompt système : « réponds
uniquement en JSON ». C'est du prompt, donc une préférence statistique — rien
n'interdit au modèle d'entourer sa réponse d'une clôture markdown, d'ajouter une
phrase d'introduction ou d'inventer une clé. Le coût de l'échec est reporté sur
l'appelant, qui découvre le problème à `json.loads`.

**Contraindre le décodage.** Le champ `format` d'Ollama reçoit un schéma JSON
— chez d'autres fournisseurs, `response_format` ou *JSON mode*. Le serveur
n'envoie plus ce schéma au modèle comme du texte à respecter : il en fait une
machine à états, et s'en sert pour **interdire des tokens pendant la
génération**. La forme devient impossible à violer.

**Valider et réessayer.** `model_validate_json()` de Pydantic relit la sortie
et vérifie ce que la grammaire ne regarde pas : les types, les bornes, les
contraintes déclarées. En cas d'échec, l'erreur elle-même repart au modèle
comme message utilisateur — un message d'erreur est une information exploitable,
pas un constat de défaite.

Les trois ne sont pas trois niveaux de qualité entre lesquels on choisit :
ce sont trois portées différentes, et le régime 2 ne rend pas le régime 3
inutile — c'est même l'inverse qui est vrai, comme la suite le montre.

### Ce qu'une grammaire fait réellement, étape par étape

La formulation « le serveur force le JSON » ne permet de prédire aucun de ses
effets de bord. Le mécanisme est plus simple et plus instructif.

Le schéma JSON est compilé en **automate** : à tout moment de la génération,
l'état courant définit l'ensemble des chaînes de caractères qui peuvent
légalement suivre. Le serveur traduit cet ensemble en **masque sur le
vocabulaire** — pour chaque token, l'automate peut-il l'accepter ? Les logits
des tokens refusés sont mis à moins l'infini avant le softmax, ce qui leur
donne une probabilité nulle. Puis le [sampling](sampling.md) se déroule
normalement sur ce qui reste : les filtres, la temperature, le tirage, tous
inchangés.

Trois conséquences se déduisent de là, et aucune n'est intuitive :

- **La contrainte n'est pas un filtre de plus au même endroit.** Elle agit
  *avant* top-k et top-p, sur la totalité du vocabulaire, et pour une raison
  qui ne dépend pas des probabilités. Un token peut être à la fois le plus
  probable de très loin et interdit.
- **Contraindre déplace la distribution, il ne l'élague pas.** Le softmax
  normalise sur les survivants : la masse de probabilité retirée aux tokens
  masqués est **redistribuée** sur les autres. Si le modèle « voulait » écrire
  une phrase d'excuse et que seul `{` est permis, ce n'est pas une version
  atténuée de sa réponse qu'on obtient, c'est une continuation qui pouvait être
  très loin dans son classement.
- **Le masque porte sur des tokens, pas sur des caractères.** Un token du
  vocabulaire peut valoir `":` ou `",\n  "`. L'automate doit donc raisonner sur
  des morceaux de longueur variable, et le jeu des tokens permis à une position
  donnée dépend du vocabulaire du modèle. La même contrainte n'a pas exactement
  le même effet sur deux modèles, et ce n'est pas un défaut d'implémentation :
  c'est la [tokenisation](tokenisation.md) qui remonte.

### Le levier `format`, avec sa portée

- **Où il agit** : à l'étape `contrainte`, entre la sortie du modèle et les
  filtres de sampling. Jamais dans le prompt — le modèle ne « sait » pas qu'il
  est contraint.
- **À quelle fréquence** : à **chaque token**, pas une fois par requête. C'est
  ce qui le distingue d'une consigne de prompt et ce qui explique son coût :
  l'automate avance à chaque pas de génération.
- **Ce qu'il propage** : la syntaxe, la présence des clés requises, les types
  déclarables dans un schéma JSON. Rien d'autre. Le contenu des chaînes reste
  entièrement libre, donc entièrement hallucinable.
- **Ce qui l'annule** : un schéma qui n'interdit rien. `{"type": "object"}`
  sans `properties` accepte n'importe quel objet, et un champ optionnel de type
  `str` accepte la chaîne vide — l'automate est alors satisfait par une sortie
  vide de sens. Le levier s'annule aussi entièrement chez un fournisseur qui
  traite `format` comme une simple consigne de prompt : même champ, même nom,
  mécanisme absent.

### Le même JSON, deux mécanismes — savoir lequel on regarde

C'est l'erreur que la leçon existe pour empêcher. Une sortie parfaitement
formée peut venir de deux endroits :

- **le modèle l'a apprise** — le format était fréquent dans son corpus, il le
  reproduit ; c'est probabiliste, donc ça tiendra la plupart du temps et
  cassera sans prévenir ;
- **la grammaire l'a rendue obligatoire** — aucune autre sortie n'était
  atteignable ; la forme est garantie par construction.

Rien à l'écran ne les distingue. Ce qui les distingue : **retirer le champ
`format` et rejouer**. Si la sortie reste valide sur des entrées variées, le
modèle sait le faire ; si elle se dégrade, c'était la grammaire. Le banc de
l'étape existe pour ça — il fait tourner les deux modes sur les mêmes textes.

L'enjeu n'est pas académique. Croire que « le modèle produit du JSON propre »
alors que c'est la grammaire, c'est retirer la contrainte le jour où elle
gênera — pour gagner de la latence, pour passer sur un autre fournisseur — et
découvrir la régression en production.

### Ce que la grammaire laisse passer, et que seul un validateur voit

Trois défauts survivent à un décodage contraint, tous constatés à l'étape :

- **le champ optionnel absent alors que l'information était dans le texte** —
  l'automate n'a aucune notion de ce qui *aurait dû* être extrait ;
- **la chaîne vide** — elle satisfait `str`, donc elle satisfait le schéma ;
- **le contenu faux** — un nom de machine plausible mais absent du texte passe
  toutes les vérifications de forme.

D'où le régime 3, et d'où les contraintes sémantiques : `Field(min_length=1)`,
des bornes, des validateurs. Elles ne relèvent plus de la grammaire — ce sont
des règles de *sens*, exprimées en Python et vérifiées après coup. Une partie
d'entre elles n'est même pas exprimable ainsi, et demande un juge.

## En pratique

[08_structured.py](../../etapes/fondamentaux/08_structured.py) : une classe
Pydantic `Serveur` (`nom`, `role`, `ram_go` optionnel, `services`), deux
démonstrations opposées — poliment puis contraint — et `extraire()` à écrire :
la boucle de retry qui renvoie l'erreur de validation au modèle, et lève au
lieu de rendre `None` après trois essais.

**À prédire avant de lancer** :

- combien de fois faut-il rejouer la démo A avant qu'une sortie casse
  `json.loads` ? Le premier passage réussira peut-être — ce n'est pas une
  réfutation, c'est la définition d'un mécanisme probabiliste.
- sur le second texte, qui ne mentionne aucune quantité de mémoire : que
  contient `ram_go` en mode contraint ? Et le champ `services` ?
- en mode contraint, la boucle de retry peut-elle s'exécuter plus d'une fois ?
  Sous quelle condition exactement — quel genre d'erreur reste possible quand
  la forme est garantie ?
- on remplace `ram_go: int | None` par `ram_go: int` et on rejoue sur le texte
  qui n'en parle pas : que fait la grammaire, et qu'obtient-on ?

## Mesures

<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->

## Recomposer

**Ce que ça change à ce qu'on croyait savoir.** Le pipeline du
[sampling](sampling.md) se relit autrement : on l'avait vu comme une suite de
réglages qui *taillent* une distribution produite par le modèle, tous
gouvernés par les probabilités. La grammaire montre qu'un masque peut être posé
pour une raison entièrement extérieure au modèle — une machine à états qui ne
sait rien du sens — et que le tirage n'y voit que du feu. Le sampling n'est pas
« la façon dont le modèle choisit » : c'est un emplacement où plusieurs
autorités peuvent intervenir, et la seule pièce qui décide vraiment est celle
qui écrit dans les logits en dernier.

Le champ `tools` du [function calling](function-calling.md) cesse du même coup
d'être une fonctionnalité à part : c'est un schéma annoncé, exactement comme
ici. Ce qui reste ouvert — et que la leçon d'à côté pose sans le trancher —
c'est si un fournisseur donné applique une vraie grammaire aux appels d'outils
ou se contente d'inscrire les schémas dans le prompt. Les deux existent, et
c'est encore la même question : quel mécanisme produit la sortie propre.

**Ce qu'on peut prédire ailleurs.** Puisque contraindre redistribue la masse de
probabilité au lieu de l'élaguer, on peut prédire qu'un schéma **trop** serré
dégrade la qualité du contenu, pas seulement la latence : forcer un champ
énuméré à trois valeurs quand la bonne réponse n'y est pas oblige le modèle à
en produire une fausse, avec la même assurance. À vérifier le jour où
[les evals](../retrieval/evals.md) donneront de quoi comparer autre chose que
la forme.

## Pièges connus

- **Rencontrés** :
  - *« Mets null si l'information est absente » a produit des null sur des
    champs présents.* La consigne, écrite pour éviter l'invention, a été
    appliquée trop largement : des informations pourtant contenues dans le
    texte sont ressorties nulles. Le prompt fait partie du contrat au même
    titre que le schéma, et une consigne défensive a un coût en rappel. Réflexe
    transférable : toute consigne ajoutée pour supprimer un défaut se teste sur
    les cas qui marchaient déjà — sinon on échange un mode d'échec contre un
    autre, moins visible.
  - *En régime « poliment », la sortie est arrivée enrobée.* Clôtures markdown
    autour du JSON, texte d'accompagnement : ce qui casse `json.loads` n'est
    presque jamais le JSON lui-même, c'est ce qu'il y a autour.
  - *L'auto-correction par renvoi de l'erreur fonctionne.* Le modèle, à qui
    l'on rend le message d'erreur de Pydantic, produit une sortie corrigée au
    tour suivant. C'est le même ressort que le refus rendu à l'agent : une
    erreur explicite est une donnée d'entrée.
- **Anticipés** — non vérifiés à ce jour :
  - *Un schéma profondément imbriqué peut coûter cher en génération.* L'automate
    avance à chaque token, et les objets imbriqués allongent la sortie autant
    que sa structure. Non mesuré ici.
  - *Le retry sans borne.* `extraire()` lève après trois essais ; une version
    qui réessaierait indéfiniment sur une entrée que le modèle n'arrive pas à
    satisfaire est une facture ouverte — la même faute que la boucle sans
    plafond de [l'agent](boucle-agent.md).

## Se tester

1. Une sortie JSON est parfaitement valide sur vingt entrées d'affilée. Que
   peut-on en conclure sur le modèle, et quelle manipulation faut-il faire
   avant de conclure quoi que ce soit ?
   *Réussi si* la réponse refuse de conclure sans avoir retiré la contrainte et
   rejoué, et nomme les deux mécanismes qui produisent la même sortie.
2. Votre schéma déclare `priorite: Literal["basse", "haute"]`. Le texte décrit
   une urgence moyenne. Que produit le décodage contraint, et pourquoi est-ce
   pire qu'une erreur ?
   *Réussi si* la réponse dit que le modèle produira l'une des deux valeurs
   permises, sans marque d'incertitude, et rattache ça au masque : la bonne
   réponse n'était pas atteignable, la masse a été redistribuée sur les
   survivantes.
3. Un collègue propose de supprimer la validation Pydantic « puisque le
   décodage contraint garantit déjà le schéma ». Que répondez-vous, avec un
   exemple qui passe la grammaire et pas la validation ?
   *Réussi si* l'exemple porte sur le sens et non la forme — chaîne vide, champ
   optionnel omis alors que l'information existait, valeur hors bornes.

## Ce que ça change dans le framework

Rien n'est promu pour l'instant, et la raison est identifiable : `extraire()`
mélange trois responsabilités qu'une brique devrait séparer — construire le
prompt d'extraction, appeler le modèle, boucler sur la validation. La boucle de
retry est la seule des trois qui soit réutilisable telle quelle ; les deux
autres dépendent du fournisseur et du cas d'usage.

Le deuxième usage concret manque, et il est connu : le jour où
[les evals](../retrieval/evals.md) demanderont une sortie structurée, on saura
si la brique doit recevoir une classe Pydantic ou un schéma déjà compilé, et si
le renvoi d'erreur au modèle appartient à la brique ou à l'appelant. C'est le
critère de [promotion](../framework/promotion.md) : l'interface attend le
deuxième usage.

Ce que la leçon dépose sans code : le client de
[`llm/ollama.py`](../../src/framework/llm/ollama.py) devra transporter le champ
`format` sans l'interpréter. Une brique qui déciderait de contraindre ou non à
la place de l'appelant imposerait la leçon à tout le code qui l'appelle.

## À retenir

- Trois régimes, trois portées : le prompt n'obtient rien de garanti, la
  grammaire garantit la forme, la validation est le seul endroit où le sens est
  vérifié.
- Une grammaire est un masque sur les logits, posé avant les filtres de
  sampling et réévalué à chaque token.
- Contraindre redistribue la masse de probabilité au lieu de l'élaguer : la
  sortie obtenue peut être très loin de ce que le modèle « voulait » écrire.
- Le masque porte sur des tokens : la même contrainte ne produit pas le même
  effet sur deux vocabulaires.
- Un JSON valide à l'écran ne dit pas lequel des deux mécanismes l'a produit —
  retirer la contrainte et rejouer est la seule façon de savoir.

## Références

- Doc `format` / structured outputs d'Ollama — et, chez le fournisseur qu'on
  vise, la question à trancher : vraie grammaire ou consigne de prompt
- Pydantic v2 : `model_validate_json`, `model_json_schema`, `Field`,
  validateurs — le schéma envoyé au serveur est produit par la classe
- GBNF / grammaires de `llama.cpp` — pour voir l'automate à nu, quand le schéma
  JSON cache trop le mécanisme
