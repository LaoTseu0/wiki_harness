# CHALLENGE.md — le cours passé au crible d'un apprenant sérieux

> **Exercice du 21 juillet 2026.** J'ai lu l'intégralité des `.md` du repo dans
> l'ordre de numérotation, en me posant à chaque paragraphe la question :
> « est-ce que je comprends vraiment, ou est-ce que je hoche la tête ? »
> **Périmètre** : les sections sécurité (`3.1-garde-fous-et-securite`,
> `5.3-securite`, `6.2-securite`) ont été **volontairement exclues** de cette
> lecture (consigne de session). Le rapport ne dit donc rien de ce pan du cours.
> Catégories : `[FLOU]` expliqué mais pas réexplicable · `[TROU]` étape ou
> justification manquante · `[DOUTE]` affirmation contestable, à vérifier.

---

## 1. Le sens du cours (reformulation)

Le fil rouge : partir du homelab (Jarvis) et **refaire soi-même chaque couche
de la stack LLM** — appel HTTP brut, sampling, outils, boucle d'agent, RAG,
MCP, serveur d'inférence, observabilité, multimodal — en Python pur contre un
petit modèle local, puis l'outiller (Qdrant, LlamaIndex, Langfuse), puis
promouvoir le tout en **framework maison** que les modules suivants consomment
(dogfooding). Chaque module produit un livrable **mesuré** (evals, tableaux,
courbes) converti en preuve d'employabilité (README canonique, post, pitch).

La thèse pédagogique implicite : (1) on ne débogue que ce qu'on a écrit —
« à la main d'abord, le framework ensuite » ; (2) **les pannes du petit modèle
sont le matériau** (« teubé par taille, pas par nature ») ; (3) sans mesure
c'est une démo, pas de l'ingénierie ; (4) la validation d'un savoir est la
question d'entretien qu'il permet d'affronter.

Fondamental pour l'auteur : les mécanismes au niveau HTTP/JSON, les evals, les
coûts. Accessoire : les frameworks (à situer), le cloud (minimal), le
fine-tuning (culture), le multi-agents (scepticisme assumé).

**Là où le sens m'échappe** : le repo est à la fois un *cours* et le *journal*
du parcours d'Anthony. Les leçons du module 1 racontent du vécu ; celles des
modules 2.2+ sont écrites **avant d'être vécues**, avec des « Pièges connus »
au ton de l'expérience et des résultats attendus précis (« recall@k attendu
≈ 1 », « Qdrant seul ne devrait *rien* changer »). Je ne peux pas distinguer,
en lisant, ce qui a été éprouvé de ce qui est anticipé — voir le verdict.

---

## 2. Challenges par module

### Module 1 — 01-llm-from-scratch

**1. `[DOUTE]` L'ordre du pipeline de sampling se contredit d'un fichier à
l'autre.**
[1.1.2](01-llm-from-scratch/1.1-socle-sans-framework/1.1.2-sampling-et-prompting/1.1.2-sampling-et-prompting.md),
« Le savoir » : « l'ordre d'application : logits → **temperature** → top-k →
top-p → tirage ». Mais le [README](01-llm-from-scratch/README.md) (step 04) :
« probabilities → **top-k/top-p filters** → temperature → draw », et la
[PROGRESSION](01-llm-from-scratch/PROGRESSION.md) : « prompt → probabilités →
filtres top-k/top-p → temperature → tirage ».
→ *Question* : lequel des deux ordres est celui que mon notebook 04 a réellement
mesuré ? Si je récite la leçon 1.1.2 en entretien, je contredis mon propre
journal d'expérience.
→ *Pourquoi ça compte* : la leçon annonce « l'ordre d'application » comme LE
savoir de la section ; un cours qui prétend démonter la boîte noire ne peut pas
laisser deux mécaniques incompatibles cohabiter. (Au passage : llama.cpp, sous
Ollama, applique par défaut les filtres *avant* la température — c'est la
version README qui colle à l'expérience, pas la leçon.)

**2. `[TROU]` La compaction n'a pas de procédure pour la deuxième fois.**
[1.1.1](01-llm-from-scratch/1.1-socle-sans-framework/1.1.1-chat-cli-historique-contexte/1.1.1-chat-cli-historique-contexte.md) :
compaction = « résumer les anciens tours par un appel LLM et placer le résumé
**en system** » ; piège : « Résumer avec le résumé précédent dans l'entrée →
dérive cumulative ».
→ *Question* : si je repars de `[system + résumé]` et que la conversation
regonfle, ma deuxième compaction inclut *forcément* le premier résumé dans son
entrée — exactement le piège dénoncé. Quelle est la procédure correcte
(résumer seulement les tours nouveaux ? concaténer les résumés ?) ?
→ *Pourquoi ça compte* : la gestion de contexte est présentée comme LA
conséquence du stateless ; sans réponse, je ne sais pas faire tourner un chat
long réel.

**3. `[DOUTE]` « C'est ReAct implémenté » — sans le R.**
[1.1.3](01-llm-from-scratch/1.1-socle-sans-framework/1.1.3-function-calling-a-la-main/1.1.3-function-calling-a-la-main.md) :
« C'est **ReAct** (Reasoning + Acting) implémenté : le modèle alterne
raisonnement et action ».
→ *Question* : dans 06_outils.py, où est la trace de raisonnement explicite ?
ReAct (Yao et al., cité en référence) fait générer des étapes « Thought: »
*avant* chaque action ; du function calling natif n'en produit pas. Un
intervieweur qui a lu le papier me demandera la différence — la leçon ne me
permet pas de répondre.
→ *Pourquoi ça compte* : le cours assimile un pattern de prompting (ReAct) à un
mécanisme d'API (tool calling) ; comprendre la nuance, c'est comprendre ce que
le « raisonnement » d'un agent est réellement.

**4. `[DOUTE]` Le prompt caching d'Ollama expliqué par une « session » qui
n'existe pas.**
[1.2.4](01-llm-from-scratch/1.2-glossaire-executable/1.2.4-prompt-caching/1.2.4-prompt-caching.md) :
« serveurs locaux (Ollama : `keep_alive` + **réutilisation de session**) ».
→ *Question* : l'API `/api/chat` d'Ollama est stateless (c'est la leçon 1.1.1) —
qu'est-ce qu'une « session » ici ? `keep_alive` garde le *modèle* chargé, et le
runner réutilise le KV cache du *dernier* prompt s'il partage un préfixe. Ce
n'est ni une session ni garanti multi-clients.
→ *Pourquoi ça compte* : l'exercice proposé (TTFT froid/chaud) est bon, mais si
le mécanisme énoncé est faux, j'interpréterai mal mes mesures (ex. deux clients
alternés qui « cassent » le cache l'un de l'autre).

**5. `[TROU]` Deux conventions semver incompatibles cohabitent.**
[1.3.6](01-llm-from-scratch/1.3-framework-maison/1.3.6-sortie-precoce-semver/1.3.6-sortie-precoce-semver.md) :
« 0.0.x = briques qui arrivent, **0.x.0 = jalon de génération** (les
générations du RAG : **0.0.1 → 0.0.2 → 0.0.3** dans la numérotation du
cours) » — la phrase se contredit elle-même. Et la
[PROGRESSION du module 2](02-homelab-rag/PROGRESSION.md) : « jalons tagués
**0.1.0** (à la main), **0.2.0** (Qdrant), **0.3.0** (LlamaIndex) ».
→ *Question* : quand je taggerai la fin de la v« 0.0.1 » du RAG, j'écris
`v0.0.1` ou `v0.1.0` ?
→ *Pourquoi ça compte* : le versionnage est promu « décision structurante du
21 juillet 2026 » et sert de clé aux comparaisons d'evals (« rejouables depuis
les tags ») — une clé ambiguë casse la traçabilité qu'elle devait garantir.

**6. `[FLOU]` Le non-déterminisme des MoE, invoqué sans mécanisme.**
[1.1.2](01-llm-from-scratch/1.1-socle-sans-framework/1.1.2-sampling-et-prompting/1.1.2-sampling-et-prompting.md),
question d'entretien : « Non garanti : ex æquo…, non-associativité des
flottants selon le batching, **architectures MoE** ».
→ *Question* : pourquoi une architecture MoE casse-t-elle le déterminisme à
T=0 ? Je ne sais pas le réexpliquer (routage d'experts dépendant du batch) — je
ne peux que le réciter.
→ *Pourquoi ça compte* : c'est la réponse d'entretien type de la leçon ; un
« pourquoi ? » de relance me met à nu.

### Module 2 — 02-homelab-rag

**1. `[DOUTE]` Deux endpoints d'embeddings, et la norme = 1 qui en dépend.**
[2.1.1](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.1-embeddings/2.1.1-embeddings.md) :
« L'API : `POST /api/embeddings` chez Ollama » et « les vecteurs sortent
normalisés (‖v‖ = 1, vérifié dans le script) ». Mais la
[PROGRESSION](02-homelab-rag/PROGRESSION.md) : « premier embedding : texte →
vecteur via **`/api/embed`** ».
→ *Question* : Ollama expose les deux endpoints, et ils ne se comportent pas
pareil (le récent `/api/embed` normalise, le legacy `/api/embeddings`
renvoie des vecteurs *non normalisés*). Lequel mon code utilise-t-il, et la
norme = 1 est-elle une propriété du modèle ou de l'endpoint ?
→ *Pourquoi ça compte* : tout le raccourci « cosinus = produit scalaire »
([2.1.2](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.2-similarite-cosinus/2.1.2-similarite-cosinus.md))
repose sur cette norme. Si quelqu'un reprend la leçon avec l'endpoint cité, ses
scores seront faux en silence — le genre exact de piège que le cours adore.

**2. `[TROU]` « Jamais de seuil absolu »… sauf pour dire « je ne sais pas ».**
[PROGRESSION](02-homelab-rag/PROGRESSION.md) : « le score absolu ne veut rien
dire … **seul le classement compte** (d'où le top-k, jamais de seuil
absolu) ». Mais
[2.1.5](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.5-recherche-top-k/2.1.5-recherche-top-k.md) :
« un top-k dont le meilleur score est bas **signale une question hors
corpus** — matière première du « je ne sais pas » ».
→ *Question* : si les valeurs absolues n'ont pas de sens, comment un « meilleur
score bas » peut-il signaler quoi que ce soit ? Avec quel seuil, calibré
comment ?
→ *Pourquoi ça compte* : le « je ne sais pas » est LA fierté du module (zéro
hallucination) ; son déclencheur retrieval repose sur une notion que le cours
vient d'invalider deux leçons plus tôt.

**3. `[TROU]` Le score « hallucination » n'a pas de définition opératoire.**
[2.1.7](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.7-evals/2.1.7-evals.md) :
« **hallucination** : la réponse affirme-t-elle quelque chose d'absent des
sources ? (0/12) » — dans une leçon intitulée « Déterministe d'abord : exact
match sur la source, présence de mots-clés attendus ».
→ *Question* : « affirmer quelque chose d'absent des sources » n'est pas
vérifiable par mot-clé. Comment 0/12 a-t-il été *calculé* — script, ou lecture
humaine ? Si c'est humain, le score n'est pas rejouable en non-régression.
→ *Pourquoi ça compte* : c'est le chiffre le plus mis en avant du module
(« zéro hallucination ») et le seul dont je ne peux pas reconstruire la mesure.

**4. `[FLOU]` « Scores identiques = zéro hallucination » — le raisonnement
saute une étape.**
[2.1](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1-v0.0.1-rag-a-la-main.md) /
[PROGRESSION](02-homelab-rag/PROGRESSION.md) : « Les deux scores identiques =
**zéro hallucination** (chaque échec est un échec de *retrieval*) ».
→ *Question* : 7/12 et 7/12 ne prouvent rien si ce ne sont pas les *mêmes* 5
questions qui échouent des deux côtés — l'égalité d'agrégats n'implique pas la
correspondance cas par cas. Est-elle vérifiée question par question ?
→ *Pourquoi ça compte* : c'est le raisonnement de diagnostic par couche que le
cours érige en méthode ; tel qu'écrit, il m'apprend une inférence invalide.

**5. `[DOUTE]` 12 questions ne peuvent pas porter l'ablation à 5 configurations.**
[2.2.5](02-homelab-rag/2.2-v0.0.2-qdrant-retrieval-avance/2.2.5-evals-comparatives/2.2.5-evals-comparatives.md) :
« rejouer deux fois avant de crier au progrès d'un point » — c'est la seule
concession statistique du module.
→ *Question* : sur 12 questions, 1 point = 8,3 %. Quel delta est significatif ?
L'ablation ligne à ligne (« chaque point gagné attribué à sa cause ») peut-elle
distinguer un vrai gain d'un coup de dé, notamment pour le re-ranking dont on
attend un delta de 1-2 points ?
→ *Pourquoi ça compte* : « mesurer, toujours » est le principe n°3 du cours —
mesurer sans notion d'incertitude, c'est l'illusion de la mesure.

**6. `[TROU]` Le budget de contexte n'est jamais confronté à la fenêtre
réellement servie par Ollama.**
[2.1.6](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.6-rag-complet/2.1.6-rag-complet.md) :
« le contexte reste borné (k × taille de chunk : **le budget se calcule**) »,
avec des chunks « ~200-800 tokens »
([2.1.3](02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.3-chunking/2.1.3-chunking.md)).
→ *Question* : k=6 × 800 tokens + system + question dépasse la fenêtre par
défaut d'Ollama (`num_ctx`), qui **tronque silencieusement**. Aucune leçon du
module ne nomme `num_ctx` ni ce mode de panne — alors qu'il peut à lui seul
expliquer des échecs de génération « sachant le bon contexte ».
→ *Pourquoi ça compte* : le module 1 a fait de la troncature silencieuse un
thème central ([1.1.1](01-llm-from-scratch/1.1-socle-sans-framework/1.1.1-chat-cli-historique-contexte/1.1.1-chat-cli-historique-contexte.md)) ;
le module 2 l'oublie à l'endroit où elle mord le plus.

**7. `[DOUTE]` « Juge ≠ générateur » interdit l'identité, pas la faiblesse.**
[2.3.2](02-homelab-rag/2.3-v0.0.3-llamaindex-outillage-standard/2.3.2-llm-as-judge/2.3.2-llm-as-judge.md) :
« **juge ≠ générateur**, jamais Qwen3 4B jugeant Qwen3 4B », juge conseillé :
« un modèle local *différent* (autre famille, **si possible** plus gros) ».
→ *Question* : le biais d'auto-préférence est-il vraiment le premier problème,
ou est-ce la *capacité* du juge ? Un juge 4B d'une autre famille respecte la
règle mais juge mal ; un gros modèle s'auto-jugeant la viole mais juge mieux.
La leçon ne hiérarchise pas les deux risques.
→ *Pourquoi ça compte* : la règle est répétée trois fois dans le repo (roadmap,
sommaire, leçon) — un intervieweur qui pousse (« et si vous n'avez qu'un seul
gros modèle ? ») me trouvera sans réponse.

### Module 3 — jarvis-agent *(section 3.1 sécurité exclue de la lecture)*

**1. `[TROU]` La consolidation mémoire n'a aucun critère opératoire.**
[3.2.2](03-jarvis-agent/3.2-outils-et-memoire/3.2.2-memoire-versionnee/3.2.2-memoire-versionnee.md) :
« `session_shutdown` → **l'agent consolide ce qu'il a appris** dans les
fichiers » ; piège : « la consolidation est une *sélection* ».
→ *Question* : sélection selon quoi ? Quel prompt, quels critères
d'admission (« décisions durables » vs « bruit »), qui tranche les conflits
avec la mémoire existante ? La leçon donne le *où* (git) et le *pourquoi*
(audit), jamais le *comment* de l'étape la plus difficile.
→ *Pourquoi ça compte* : c'est le cœur du pattern « external memory » vanté
comme différenciateur ; sans mécanisme de sélection, je sais versionner une
mémoire, pas la construire.

**2. `[FLOU]` Le human-in-the-loop asynchrone est nommé, pas conçu.**
[3.3.1](03-jarvis-agent/3.3-comparaison-regimes-agents/3.3.1-mode-rpc-sdk/3.3.1-mode-rpc-sdk.md) :
« le human-in-the-loop doit trouver sa forme asynchrone (**file d'approbation**
plutôt que prompt bloquant) ».
→ *Question* : que devient l'action en attente — timeout ? expiration quand le
contexte a changé (la commande approuvée à H+6 est-elle encore sûre) ? que
fait l'agent pendant ce temps ?
→ *Pourquoi ça compte* : c'est exactement le point où un agent persistant
devient dangereux ou inutilisable ; « file d'approbation » est un nom, pas une
conception.

**3. `[FLOU]` « Recyclage périodique » de session : aucun déclencheur.**
[3.3.1](03-jarvis-agent/3.3-comparaison-regimes-agents/3.3.1-mode-rpc-sdk/3.3.1-mode-rpc-sdk.md) :
« une session qui vit des jours dérive (contexte, état) — prévoir **recyclage
périodique** et resurrection propre ».
→ *Question* : recycler sur quel signal — n tours, n tokens, un score de dérive
mesuré ? « La dérive » est constatée mais jamais définie ni mesurée (alors que
le cours mesure tout le reste).
→ *Pourquoi ça compte* : sans critère, je recyclerai au feeling — l'inverse de
la discipline du cours.

### Module 4 — ollama-vs-vllm-bench

**1. `[DOUTE]` Tout le module benche sur 6 Go alors que le homelab a une 4090.**
[4.1.1](04-ollama-vs-vllm-bench/4.1-deploiement/4.1.1-vllm-sur-rtx-2060/4.1.1-vllm-sur-rtx-2060.md) :
« le faire tenir sur une RTX 2060 à **6 Go** — contrainte qui force à
comprendre chaque mégaoctet ». Or la
[PROGRESSION du module 1](01-llm-from-scratch/PROGRESSION.md) : « jarvis-core
(**RTX 4090**) volontairement laissé de côté **pendant l'apprentissage** ».
→ *Question* : le module 4 n'est plus « l'apprentissage » de base — pourquoi le
choix de la 2060 n'est-il jamais rediscuté ici ? Le verdict
([4.3.2](04-ollama-vs-vllm-bench/4.3-analyse-et-verdict/4.3.2-verdict-ollama-vs-vllm/4.3.2-verdict-ollama-vs-vllm.md))
liste bien le piège « Généraliser depuis 6 Go » mais ne mentionne pas la carte
24 Go disponible à la maison, qui rendrait la « zone grise » mesurable au lieu
d'extrapolée.
→ *Pourquoi ça compte* : le module vend une « règle paramétrée (concurrence,
VRAM) » — avec deux points de mesure (6 et 24 Go), la règle serait une droite ;
avec un seul, c'est une conjecture.

**2. `[DOUTE]` La formule du KV cache est incomplète — et fausse pour Qwen3.**
[4.3.1](04-ollama-vs-vllm-bench/4.3-analyse-et-verdict/4.3.1-mecanismes-vllm/4.3.1-mecanismes-vllm.md) :
« chaque requête active occupe `2 × couches × têtes × dim × tokens` ».
→ *Question* : il manque la taille du type (×2 octets en fp16), et « têtes »
devrait être les têtes **KV** (GQA), pas les têtes d'attention. Qwen3 utilise
le GQA : compter les têtes d'attention surestime le cache d'un facteur ~4. Avec
la formule de la leçon, mon budget VRAM de
[4.1.1](04-ollama-vs-vllm-bench/4.1-deploiement/4.1.1-vllm-sur-rtx-2060/4.1.1-vllm-sur-rtx-2060.md)
est faux.
→ *Pourquoi ça compte* : « le KV cache, c'est la concurrence » est LE message
du module — la seule formule quantitative donnée doit être juste.

**3. `[TROU]` Le bench mesure la vitesse, jamais la qualité — alors que
l'outillage existe.**
[4.1.1](04-ollama-vs-vllm-bench/4.1-deploiement/4.1.1-vllm-sur-rtx-2060/4.1.1-vllm-sur-rtx-2060.md),
piège : « AWQ vs GGUF q4_K_M … qualité proche **mais pas identique** — le dire
dans le README ».
→ *Question* : pourquoi « le dire » au lieu de « le mesurer » ? Le jeu d'evals
du module 2 rejoué sur les deux moteurs (le backend commutable de
[2.4.2](02-homelab-rag/2.4-service-et-craftsmanship/2.4.2-backend-commutable/2.4.2-backend-commutable.md)
le permet par construction) chiffrerait l'écart de qualité entre quantisations.
→ *Pourquoi ça compte* : un verdict perf-seul peut recommander vLLM là où sa
quantisation dégrade les réponses — le cours rate ici sa propre croisade
(« chiffrer, pas ressentir »).

### Module 5 — homelab-mcp *(section 5.3 sécurité exclue de la lecture)*

**1. `[TROU]` Quand exposer en MCP plutôt qu'en outil natif ? Le cours vit la
tension sans la trancher.**
[Roadmap](roadmap.md), couche 0 : « le **rejet de MCP par Pi** pour son coût en
contexte » ; [5.1](05-homelab-mcp/5.1-serveur/5.1-serveur.md) : « MCP est nommé
dans ~60 % des offres — **le pari du module est déjà gagné** » ;
[3.2.1](03-jarvis-agent/3.2-outils-et-memoire/3.2.1-outil-home-assistant/3.2.1-outil-home-assistant.md) :
« deux canaux de distribution (outil de harnais vs protocole), même
savoir-faire ».
→ *Question* : le même homelab est exposé deux fois (registerTool au module 3,
MCP au module 5). À quel moment un outil *doit-il* passer en MCP — combien de
hosts, quel coût en contexte toléré ? Le seul arbitrage donné est de marché
(« les offres le demandent »), jamais technique.
→ *Pourquoi ça compte* : le cours m'apprend à me méfier des adoptions par la
mode, puis adopte MCP… par le marché. Il me manque la règle de décision que
l'intervieweur exigera (« pourquoi MCP et pas un outil direct ? »).

**2. `[FLOU]` Le « coût en contexte » de MCP, invoqué partout, chiffré nulle part.**
[5.1.1](05-homelab-mcp/5.1-serveur/5.1.1-serveur-mcp-python/5.1.1-serveur-mcp-python.md) :
« chaque outil découvert entre dans la fenêtre du host … **trois outils bien
décrits, pas quinze** ».
→ *Question* : combien de tokens coûte concrètement mon serveur de trois outils
dans la fenêtre de Claude Code ? C'est mesurable en une commande — pourquoi
n'est-ce l'exercice d'aucune leçon, alors que ce coût a justifié le rejet de
MCP par Pi ?
→ *Pourquoi ça compte* : « 3 pas 15 » est une règle de pouce posée sans le
chiffre qui la fonderait — pour un cours anti-boîte-noire, c'est une boîte
noire économique.

**3. `[FLOU]` « Concevoir stateless dès le début » — critère nommé, pas outillé.**
[5.1.2](05-homelab-mcp/5.1-serveur/5.1.2-transports-stdio-http/5.1.2-transports-stdio-http.md) :
« le SDK rend la bascule [stdio → HTTP] triviale — **si** le serveur n'a pas
d'état par client caché ».
→ *Question* : comment vérifie-t-on l'absence d'état caché *avant* de basculer
(test à deux clients concurrents ? revue de quoi ?) ? Le « si » porte tout le
risque de la section et reste sans méthode.
→ *Pourquoi ça compte* : c'est précisément le genre de bug silencieux
(marche en stdio, casse en HTTP) que le cours aime transformer en leçon — ici
il n'y a que l'avertissement.

### Module 6 — production *(section 6.2 sécurité exclue de la lecture)*

**1. `[FLOU]` Le « coût équivalent API » repose entièrement sur un choix non
spécifié.**
[6.1.3](06-production/6.1-observabilite/6.1.3-suivi-des-couts/6.1.3-suivi-des-couts.md) :
« on déclare un prix de référence (ex. **le tarif d'un modèle cloud
comparable**) » ; piège : « prendre l'équivalent raisonnable et le documenter ».
→ *Question* : comparable selon quoi — paramètres, MMLU, prix du marché ?
Qwen3 4B n'a pas d'équivalent API évident ; entre un tarif « mini » et un
tarif « frontier », ma métrique varie d'un facteur 10-50, et avec elle toutes
les conclusions locales vs cloud.
→ *Pourquoi ça compte* : la leçon promet « l'outil de décision local vs API » ;
un outil de décision dont le paramètre central est « au jugé » décide de ce
qu'on veut lui faire dire.

**2. `[DOUTE]` L'empreinte de Langfuse v3 sur le matériel homelab n'est jamais
chiffrée.**
[6.1.1](06-production/6.1-observabilite/6.1.1-langfuse-self-hoste/6.1.1-langfuse-self-hoste.md) :
« ClickHouse + Postgres + Redis + MinIO — **vérifier RAM/disque disponibles
avant** » ; « le service le plus « gros » du homelab jusqu'ici ».
→ *Question* : sur le NUC qui sert déjà Ollama (et bientôt Qdrant), ce
quintuple service tient-il ? Aucun ordre de grandeur (RAM totale requise,
rétention) n'est donné, alors que le cours chiffre la VRAM au mégaoctet près au
module 4.
→ *Pourquoi ça compte* : si l'observabilité cannibalise les ressources du
système observé, la leçon « ne jamais dégrader ce qu'on mesure »
([6.1.2](06-production/6.1-observabilite/6.1.2-tracer-les-appels/6.1.2-tracer-les-appels.md))
se joue aussi au niveau infra.

**3. `[TROU]` L'envoi asynchrone des traces peut perdre exactement les traces
qui comptent.**
[6.1.2](06-production/6.1-observabilite/6.1.2-tracer-les-appels/6.1.2-tracer-les-appels.md) :
« envoi asynchrone (ne jamais bloquer la réponse pour tracer) » et, piège :
« les erreurs et timeouts sont **les traces les plus précieuses** ».
→ *Question* : que deviennent les traces quand Langfuse est indisponible ou que
le process meurt avant le flush — perte silencieuse ? buffer disque ? Les deux
consignes (async + ne pas perdre les échecs) tirent en sens opposés et la
leçon ne dit pas comment les concilier.
→ *Pourquoi ça compte* : un système d'observabilité qui perd préférentiellement
les traces d'incident donne une confiance inversée.

### Module 7 — multimodal

**1. `[TROU]` « Marquer la confiance » d'un OCR par VLM — avec quoi ?**
[7.3.1](07-multimodal/7.3-ouvertures/7.3.1-camera-et-ocr/7.3.1-camera-et-ocr.md) :
« un VLM hallucine du texte ; pour des documents importants, **marquer la
confiance** et garder l'original ».
→ *Question* : un VLM ne fournit pas de score de confiance calibré (à la
différence d'un OCR classique type Tesseract). Avec quel mécanisme est-ce que
je « marque la confiance » — auto-évaluation du modèle (notoirement mal
calibrée), double passe, comparaison à un OCR dédié ?
→ *Pourquoi ça compte* : c'est le garde-fou proposé pour des documents
*famille* importants ; s'il n'est pas implémentable, il est pire qu'absent (il
rassure).

**2. `[FLOU]` Wake word et VAD fusionnés d'un slash.**
[7.1.1](07-multimodal/7.1-documenter-existant/7.1.1-etude-de-cas-stt-tts/7.1.1-etude-de-cas-stt-tts.md) :
« **wake word / VAD** : détecter la parole avant de transcrire » ; piège : « la
latence perçue commence à la détection ».
→ *Question* : wake word (reconnaître « Jarvis ») et VAD (détecter qu'on parle)
sont deux mécanismes différents avec des latences différentes — lequel des deux
Jarvis utilise-t-il, et lequel démarre le chrono de « latence perçue » ?
→ *Pourquoi ça compte* : la leçon prétend m'apprendre à « mapper les termes du
marché sur Whisper/Piper » — le mapping commence par ne pas confondre deux
termes.

**3. `[FLOU]` « ✅ acquis techniquement » pour un pipeline que personne n'a
encore mesuré.**
[7.1.1](07-multimodal/7.1-documenter-existant/7.1.1-etude-de-cas-stt-tts/7.1.1-etude-de-cas-stt-tts.md) :
« **Statut : ✅ acquis techniquement** (pipeline en prod) · ⚪ à documenter » ;
auto-contrôle de la section : « savoir donner la latence de bout en bout du
pipeline vocal, brique par brique ».
→ *Question* : au standard du cours lui-même (« un projet LLM sans évaluation
chiffrée est une démo »), un pipeline jamais instrumenté est-il « acquis » ?
Aujourd'hui, personne dans ce repo ne peut passer l'auto-contrôle.
→ *Pourquoi ça compte* : c'est le seul endroit du cours où le ✅ précède la
mesure — une entorse au principe fondateur, sur le module vitrine du CV.

### Transverse — portfolio

Section solide : le canon README (problème/archi/métriques/recul), la règle
« terme + preuve » du
[vocabulaire](transverse-portfolio/p.3-pitch/p.3.2-vocabulaire-des-offres/p.3.2-vocabulaire-des-offres.md)
et l'arbitrage cloud minimal
([P.4.1](transverse-portfolio/p.4-en-suspens/p.4.1-notions-cloud/p.4.1-notions-cloud.md))
sont cohérents avec le reste et auto-appliqués. Rien à challenger qui ne soit
déjà couvert par les modules.

---

## 3. Les 10 questions fondamentales auxquelles le cours ne répond pas encore

1. **Les pannes d'un 4B sont-elles le bon matériau ?** Le cours affirme que
   Qwen3 4B est « teubé par taille, pas par nature »
   ([PROGRESSION 1](01-llm-from-scratch/PROGRESSION.md)) — mais quels échecs
   observés (suppression niée, typo d'argument) sont des artefacts de taille et
   lesquels sont fondamentaux ? Jamais testé contre un modèle plus grand, alors
   que la 4090 est disponible.
2. **Que se passe-t-il dans le transformer ?** Attention, softmax, KV — la
   couche 0 est déléguée à 3Blue1Brown/Karpathy et n'a ni leçon ni exercice,
   alors que le glossaire promet « la preuve portable qu'**aucune couche n'est
   magique** ».
3. **Que fait la tokenisation à *mon* texte ?** Français accentué, YAML, code —
   les conséquences (coûts, chunking, comptage) sont affirmées en couche 0 mais
   jamais manipulées dans un exercice.
4. **Que voit réellement le modèle ?** Le template de chat qui fusionne
   system/messages/outils en un seul texte — c'est lui qui rend les tool_calls
   possibles — n'est jamais ouvert ; Ollama le cache et le cours le laisse
   caché.
5. **Quelle fenêtre me sert réellement Ollama** (`num_ctx`), et comment
   détecter sa troncature silencieuse ? (voir challenge module 2.6)
6. **Quel delta d'eval est significatif** sur 12-30 questions ? Aucune notion
   d'incertitude statistique dans tout le parcours.
7. **Comment mesurer une hallucination sans humain ?** La métrique phare du
   module 2 n'a pas de définition opératoire déterministe (challenge 2.3).
8. **Pourquoi la géométrie des embeddings encode-t-elle le sens** (entraînement
   contrastif), et où casse-t-elle (négations, nombres, dates) ? Le cours
   utilise les embeddings comme un acquis, jamais comme un objet d'étude.
9. **Comment évaluer la gestion de contexte elle-même ?** Que perd exactement
   une compaction, mesuré comment ? Les evals du cours notent le RAG, jamais la
   mémoire de conversation.
10. **Quand un standard vaut-il son coût ?** Pi a rejeté MCP pour son coût en
    contexte, le module 5 l'adopte pour le marché — la règle de décision
    technique (tokens vs interopérabilité) n'existe nulle part (challenge 5.1).

*(La sécurité — injections, garde-fous, threat model — est traitée par le cours
mais exclue de cette lecture ; ce rapport ne peut ni la valider ni la
challenger.)*

---

## 4. Verdict d'apprenant

**Ce que ce cours m'a réellement fait comprendre.** La mécanique de bout en
bout au niveau HTTP/JSON : un appel LLM est un POST, le modèle est stateless,
un agent est une boucle while, un tool_call est une demande que *mon* code
exécute, la chaîne RAG se diagnostique maillon par maillon. Les leçons
d'incidents du module 1 (génération débridée, résumé ignoré en `user`,
suppression niée, `rm`→`del`) sont la meilleure pédagogie du repo : du vécu
daté, reproductible, avec la leçon tirée. La discipline transversale — jeu
d'evals figé, ablation une variable à la fois, « chaque chiffre a une
histoire » — est une vraie culture d'ingénierie, pas un vernis. Et la
structure fixe des leçons (Essentiel / Savoir / Pièges / Question d'entretien)
rend le test de Feynman praticable : sur les leçons *vécues* (1.1.x, 2.1.1,
2.1.2), je sais réexpliquer sans relire.

**Où j'ai l'illusion de comprendre.** Trois zones.

1. **Sous l'API.** Transformer, tokenisation, entraînement des embeddings,
   template de chat : le cours me donne le *vocabulaire* (PagedAttention, GQA,
   nucleus sampling) sans jamais me faire toucher le mécanisme. Je risque
   exactement ce que le cours moque chez les autres : réciter « le framework
   s'en occupe », version infra — « PagedAttention s'en occupe ».
2. **Les leçons écrites avant d'être vécues.** Des sections 2.2 à 7, les
   « Pièges connus » et les résultats attendus sont rédigés au ton de
   l'expérience pour des exercices ⚪ jamais faits. En lisant, j'ai *cru*
   apprendre du vécu ; en vérifiant les statuts, c'est de l'anticipation
   (plausible, souvent juste — mais la différence entre « je sais » et « je
   prédis » est précisément ce que le cours prétend m'enseigner). Les
   incohérences relevées (ordre de sampling, endpoints d'embeddings, semver)
   sont typiques de ce mode d'écriture : personne ne s'est encore cogné dessus.
3. **Le format question-d'entretien.** Chaque leçon me fournit une réponse
   prête à dire. C'est efficace — et c'est un piège : je peux *performer* la
   compréhension sans l'avoir (le challenge MoE, module 1.6, en est le test :
   je récite la réponse, je ne survis pas au « pourquoi ? » suivant). Le cours
   fabrique en moi, s'il est mal utilisé, le candidat-perroquet qu'il dénonce ;
   son antidote — faire les exercices, pas seulement lire les leçons — n'est
   écrit nulle part aussi explicitement qu'il le faudrait.

Au total : un cours dont la colonne vertébrale (à la main d'abord, mesurer
toujours, une leçon = un mécanisme) tient, et dont les faiblesses sont
presque toutes du même type — **des affirmations écrites avec l'assurance de
la mesure avant que la mesure ait eu lieu**. La bonne nouvelle : le cours
contient lui-même l'outil de sa correction (ses evals, ses bancs d'essai, sa
règle « chaque défaut caché est repris en main ou accepté et noté »). Il
suffit de l'appliquer à ses propres leçons.
