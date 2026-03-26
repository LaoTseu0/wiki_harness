# Verdict Ollama vs vLLM

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [de la mesure à la décision](analyse-et-verdict.md) — que
  la règle se donne paramétrée, jamais comme un vainqueur absolu ;
  [la charge concurrente](charge-concurrente.md) et [les mécanismes vLLM](mecanismes-vllm.md)
  — les courbes et leurs explications, dont la règle est la conclusion.
- **Débloque** : le choix d'un moteur pour un déploiement réel, et le second
  point de mesure quand une deuxième carte entre en service.

## L'essentiel

Le livrable qui referme le module : une **règle de décision** défendable et
écrite — quand Ollama suffit, quand vLLM se justifie. Pas de vainqueur absolu ;
deux outils pour deux problèmes, et la maturité consiste à refuser le faux duel.

La thèse à tenir : les courbes ne montrent jamais une supériorité, elles montrent
un **régime** de supériorité. « vLLM écrase Ollama » est faux même quand les
chiffres penchent, parce que la règle qui oublie ses paramètres — concurrence,
VRAM — se cassera au premier changement de contexte. La valeur de cette leçon
n'est pas de désigner un gagnant, c'est de produire une règle qui dise *où* elle
cesse de valoir.

Cette leçon suppose les mécanismes acquis ([mécanismes vLLM](mecanismes-vllm.md))
et ne les redonne pas ; elle en tire la conséquence décisionnelle.

## Le savoir

### Quand Ollama suffit, et pourquoi le confort l'emporte alors

- un ou deux utilisateurs, usage interactif — le homelab au quotidien ;
- besoin de commodité : pull de modèles, format GGUF, déchargement automatique,
  repli CPU possible ;
- matériel modeste où la simplicité prime sur le rendement.

Le mécanisme du choix : le rendement d'un serveur dédié n'a de valeur que si
quelqu'un le consomme. À un utilisateur, la préallocation de vLLM monopolise la
carte pour une concurrence qui n'existe pas — on paie un coût sans acheter la
contrepartie. C'est le choix du parcours pour apprendre, et il reste le bon pour
cet usage.

### Quand vLLM se justifie, et ce que ça coûte

- **concurrence réelle** — une équipe, un service interne : le débit agrégé et le
  TTFT sous charge penchent nettement ([charge concurrente](charge-concurrente.md)) ;
- besoin de rendement par carte (batching continu, PagedAttention —
  [mécanismes vLLM](mecanismes-vllm.md)) ;
- production outillée : métriques Prometheus, déploiement orchestré.

Les coûts à assumer, qui font partie de la règle : la préallocation VRAM occupe
la carte en permanence, il n'y a plus de va-et-vient de modèles à la Ollama, et
un GPU est exigé. Une règle qui vante le rendement sans nommer ces coûts est
incomplète — dans un homelab, l'impossibilité du multi-modèles compte autant que
le débit.

### La zone grise se tranche par les chiffres, pas par principe

Une petite carte de 6 Go est précisément une zone grise : vLLM y apporte la tenue
de charge, mais le KV cache borne vite la concurrence atteignable. Le **point de
bascule** — le nombre d'utilisateurs simultanés au-delà duquel vLLM se justifie
sur cette carte — est exactement ce que le bench doit localiser. Il n'a pas
encore tourné : l'annoncer maintenant serait inventer le chiffre que la démarche
existe pour produire.

### La règle se paramètre, sinon elle ne se transporte pas

Généraliser depuis 6 Go est l'erreur type : sur une carte de 24 Go, le point de
bascule se déplace, parce que plus de VRAM libre après les poids, c'est plus de
cache, donc plus de concurrence avant saturation. La règle se donne donc
**paramétrée** par la concurrence et la VRAM, pas en chiffre brut.

C'est aussi pourquoi un seul point de mesure ne fait pas une règle. Le homelab
dispose d'une seconde carte (jarvis-core, RTX 4090 24 Go) : deux points de mesure
tracent une tendance, un seul ne donne qu'une conjecture — à bencher quand cette
carte entre en service.

### Deux lectures pour « vLLM est meilleur »

Le même énoncé recouvre deux affirmations très différentes, et les confondre ruine
la crédibilité de la règle :

- **un régime de supériorité** — vrai : au-delà d'un certain niveau de
  concurrence, sur une VRAM donnée, vLLM domine. C'est ce que les chiffres
  établissent.
- **une supériorité absolue** — faux : à un utilisateur, ou sur une carte que la
  préallocation gêne, l'avantage s'inverse.

Ce qui les distingue : la règle nomme-t-elle ses paramètres ? Une conclusion qui
tient sans condition est le signe qu'on a généralisé un régime en absolu.

## Quand c'est la bonne réponse

**Choisir vLLM** quand la concurrence cible dépasse le point de bascule mesuré
pour la VRAM disponible — et seulement une fois ce point mesuré, pas supposé.

**Choisir Ollama** pour les postes individuels et l'expérimentation, où la
commodité prime et où la carte doit rester partageable.

**Refuser de trancher au principe** dans la zone grise : c'est là que la mesure
est la seule autorité, et une petite carte y est presque toujours.

## Ce qu'on ne saura pas faire

Le bench n'a pas tourné : la règle est **structurée mais pas chiffrée**. On sait
quels paramètres la commandent — concurrence, VRAM — mais pas où tombe le point
de bascule sur la RTX 2060, ni comment il se déplace sur la RTX 4090. Tant que
c'est le cas, « à tel nombre d'utilisateurs, vLLM » reste une case vide.

Ce que ça laisse ouvert, et qui ne se déduit pas : le point de bascule exact sur
6 Go, et la forme de son déplacement avec la VRAM — linéaire, ou non. Deux cartes
donneraient deux points ; il en faudrait davantage pour une loi.

Ce qui promouvrait cette leçon en « refaire » : les courbes des deux moteurs sur
les deux cartes, et la règle écrite avec son point de bascule chiffré et son
paramétrage en VRAM — le moment où la case vide se remplit d'un nombre mesuré.

## Se tester

1. « Ollama ou vLLM pour notre équipe de dix personnes ? » Comment répondez-vous
   sans avoir vos courbes sous les yeux ?
   *Réussi si* la réponse traite la question comme une question de charge, penche
   vers vLLM pour une concurrence réelle mais **conditionne** au point de bascule
   mesuré pour la VRAM disponible, au lieu d'affirmer un seuil.
2. Un rapport conclut « vLLM écrase Ollama, migrons tout ». Quelle distinction
   exigez-vous ?
   *Réussi si* la réponse sépare un régime de supériorité d'une supériorité
   absolue, et rappelle qu'à un utilisateur la préallocation de vLLM est un coût
   sans contrepartie.
3. On veut réutiliser la règle établie sur une carte de 6 Go pour une carte de
   24 Go. Que corrigez-vous ?
   *Réussi si* la réponse refuse le transport tel quel, explique que plus de VRAM
   déplace le point de bascule (plus de cache, plus de concurrence), et exige une
   règle paramétrée par la VRAM.

## À retenir

- Pas de vainqueur absolu : Ollama pour le mono-usager et la commodité, vLLM pour
  la concurrence réelle et le rendement par carte.
- Les chiffres montrent un régime de supériorité, jamais une supériorité — la
  règle qui oublie ses paramètres se casse au changement de contexte.
- Le point de bascule sur 6 Go est à mesurer, pas à annoncer : l'inventer serait
  fabriquer le résultat que le bench doit produire.
- La règle se paramètre par concurrence et VRAM ; un seul point de mesure est une
  conjecture, pas une loi.

## Références

- [De la mesure à la décision](analyse-et-verdict.md) — pourquoi la règle se
  donne paramétrée
- [Charge concurrente](charge-concurrente.md) — les courbes dont le point de
  bascule est la conclusion
