# Servir un modèle

> [carte du cours](../carte.md)

## Prérequis et suites

- **Suppose acquis** : [attention et KV cache](../fondamentaux/attention-et-kv-cache.md)
  — et précisément que le cache occupe de la VRAM *par séquence*, ce qui fait
  de lui la ressource qui sature en premier ; c'est la propriété qui porte tout
  le budget mémoire de cette leçon. [Les providers](../framework/providers.md)
  — l'API OpenAI-compatible comme dénominateur commun, ce qui rend deux moteurs
  interchangeables sans toucher au code appelant.
- **Débloque** : la [mesure comparée Ollama vs vLLM](benchmark.md), dont ce
  déploiement est le montage ; les [mécanismes vLLM](mecanismes-vllm.md), qui
  expliquent pourquoi le budget mémoire décide de la concurrence.

## L'essentiel

« Servir un modèle » n'est pas « appeler un modèle ». Ollama, l'outil du
quotidien, cache trois coûts qu'un serveur de production expose : le **budget
de VRAM**, le **compromis de quantisation**, et la **concurrence**. Tant qu'on
reste à un utilisateur, ces coûts sont invisibles ; c'est la charge qui les
révèle.

La thèse de ce module — celle qu'on pourrait contredire — n'est pas « vLLM est
meilleur ». C'est qu'**aucune specification ne permet de trancher a priori entre
deux moteurs** : le seul argument qui tienne est une mesure sur *sa* carte, avec
*son* modèle, sous *sa* charge. Le déploiement n'est donc pas le but, c'est le
montage de l'expérience : à la fin de cette leçon, deux moteurs servent le même
modèle sur la même RTX 2060 de 6 Go, et tout le reste du module les compare.

Cette leçon ne couvre pas la théorie de la quantisation — ce qu'un poids coûte
bit par bit est une leçon à part — ni ce qui se passe *dans* le moteur sous
charge, qui est [la charge concurrente](charge-concurrente.md).

## Le savoir

### Servir ≠ appeler : tout tient à la politique mémoire

La différence entre Ollama et un serveur de production n'est pas une différence
de qualité, c'est une différence de **politique d'occupation de la carte**.

- Ollama **charge et décharge à la demande** : le modèle entre en VRAM au
  premier appel, en sort après un délai d'inactivité (`keep_alive`). C'est le
  confort mono-usager — la carte reste libre pour autre chose entre deux usages,
  au prix d'un premier appel qui paie le chargement.
- [vLLM](vllm-sur-rtx-2060.md) **préalloue et occupe** : il réserve au démarrage
  la fraction de VRAM qu'on lui accorde et ne la rend plus. C'est le rendement
  multi-usagers — la carte est monopolisée, mais chaque requête entre sans
  rechargement.

Ce qui décide n'est donc pas « lequel est plus rapide » mais « la carte
doit-elle rester partageable ». Sur 6 Go partagés, ce choix est exclusif : les
deux moteurs ne tournent pas ensemble, et un bench honnête n'en lance qu'un à la
fois.

### Le budget VRAM est la contrainte maîtresse

Toute la difficulté du serving tient dans une addition :

```
VRAM = poids du modèle + KV cache + activations/overhead
```

Les **poids** sont fixes une fois le modèle et sa quantisation choisis. Les
**activations** sont un surcoût de fonctionnement modeste. La variable qui
décide de tout est le **[KV cache](../fondamentaux/attention-et-kv-cache.md)** :
il croît avec le nombre de requêtes actives × leur longueur de contexte. Sur une
carte, la VRAM libre après les poids **est** la capacité de concurrence — chaque
requête simultanée vit dans ce cache.

D'où l'arbitrage central, qui n'a pas de bonne réponse universelle : un modèle
plus gros (meilleur) laisse moins de place au cache (moins de concurrence). Sur
6 Go, un modèle ~3B quantisé sur 4 bits (~2 à 2,5 Go de poids, un calcul qui se
redéduit : 3 milliards de paramètres × 4 bits ÷ 8) laisse ~3 Go de cache ; un
7-8B quantisé (~4,5 Go) n'en laisse presque plus. Servir, c'est choisir où
placer le curseur — et ce choix ne se fait pas au jugé, il se mesure.

### Pourquoi deux moteurs, et pas un verdict a priori

On pourrait croire qu'un serveur « fait pour la production » bat toujours un
outil « de bureau ». C'est précisément l'erreur que le module existe pour
désamorcer. À une requête, les deux moteurs se ressemblent ; c'est en montant en
concurrence qu'ils divergent, et le sens de la divergence dépend de grandeurs
locales — la VRAM de la carte, la taille du modèle, le profil du trafic — qu'une
fiche technique ne contient pas.

Le déploiement des deux moteurs derrière la même API OpenAI-compatible n'est donc
pas une commodité : c'est ce qui rend la comparaison *équitable*. Même modèle,
même client, même jeu de prompts — seul le moteur change. C'est le
[backend commutable](../framework/providers.md) du framework mis au travail, et
c'est la seule façon d'obtenir un écart qu'on puisse attribuer au moteur et à
rien d'autre.

## Quand c'est la bonne réponse

**Déployer un serveur d'inférence dédié** quand la concurrence est réelle — une
équipe, un service interne — et que le rendement par carte compte. C'est là que
la préallocation et le batching se paient.

**Rester sur Ollama** tant que l'usage est mono-usager et interactif. Le confort
— pull de modèles, déchargement automatique, repli CPU possible — l'emporte sur
un rendement dont personne ne profite. C'est le choix du parcours, et il reste le
bon pour cet usage.

**Ne pas trancher au jugé** dans la zone grise, qui est exactement celle d'une
petite carte. À 6 Go, vLLM apporte la tenue de charge mais le cache borne vite la
fête ; où se situe le point de bascule est une question de mesure, traitée par
[le verdict](verdict-ollama-vs-vllm.md), pas de principe.

## Ce qu'on ne saura pas faire

Aucune étape n'existe encore sous `etapes/inference/` : ni le déploiement des
deux moteurs, ni le bench n'ont tourné dans ce dépôt. Tout ce qui précède décrit
le montage et l'arbitrage, pas un résultat — les chiffres de poids et de VRAM
sont des faits matériels et des calculs, pas des mesures de performance, qui
elles restent à produire.

Ce que ça laisse ouvert, et qui ne se déduit pas : quel modèle exact tient
vraiment dans 6 Go avec une marge de cache utile, et à partir de combien de
requêtes simultanées le serveur dédié se justifie sur cette carte précise.

Ce qui promouvrait ce module en leçons « refaire » : les scripts de déploiement
et de charge écrits sous `etapes/inference/`, et une première mesure d'occupation
lue à `nvidia-smi` — le budget VRAM cessant d'être une addition théorique pour
devenir une ligne relevée.

## Se tester

1. On vous dit : « un serveur de production comme vLLM est forcément plus rapide
   qu'Ollama ». Que répondez-vous, et sur quelle grandeur se joue vraiment la
   différence ?
   *Réussi si* la réponse refuse le verdict a priori, situe l'égalité à une
   requête et la divergence sous concurrence, et nomme la VRAM libre comme
   capacité de concurrence — pas « vLLM est optimisé ».
2. Vous devez faire tenir un modèle sur une carte de 6 Go et servir plusieurs
   utilisateurs. Quel arbitrage, et qu'est-ce qui le rend inévitable ?
   *Réussi si* la réponse oppose poids et KV cache dans une VRAM fixe, et
   rattache la concurrence à la place laissée au cache après les poids.
3. Pourquoi lance-t-on un seul moteur à la fois pendant le bench, et derrière la
   même API ?
   *Réussi si* la réponse cite les 6 Go partagés (préallocation exclusive) et
   l'équité de comparaison — un seul facteur qui change, le moteur.

## À retenir

- Servir n'est pas appeler : la vraie différence entre les moteurs est leur
  politique mémoire — décharger à la demande contre préallouer et occuper.
- `VRAM = poids + KV cache + activations` ; le cache est la variable, et la VRAM
  libre après les poids **est** la capacité de concurrence.
- Un plus gros modèle laisse moins de cache : servir, c'est arbitrer, et
  l'arbitrage se mesure au lieu de se deviner.
- Aucune fiche technique ne tranche entre deux moteurs : seule une mesure sur sa
  carte, son modèle, sa charge le fait — d'où deux moteurs derrière une API
  commune.

## Références

- Doc vLLM et doc Ollama — les deux moteurs comparés, à lire pour leurs
  politiques mémoire opposées plus que pour leurs API
- [Attention et KV cache](../fondamentaux/attention-et-kv-cache.md) — pourquoi le
  cache est la ressource qui borne la concurrence
- [Providers](../framework/providers.md) — l'API OpenAI-compatible qui rend la
  comparaison équitable
