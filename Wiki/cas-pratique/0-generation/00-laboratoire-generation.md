---
id: cas-parcours-0-generation
type: cas-pratique
titre: Suivre et reconstruire une génération
parcours: 0-generation
statut: brouillon
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
---

# Suivre et reconstruire une génération

## Objectif observable

Partir d'une liste de messages, produire les identifiants exacts lus par un
petit modèle local, inspecter ses logits, reconstruire la pipeline de sampling
et exécuter une boucle autorégressive bornée.

À la fin du laboratoire, un dossier d'artefacts doit permettre de répondre
précisément :

- quel modèle, quel tokenizer et quel Template ont été utilisés ;
- quelle séquence d'identifiants a été envoyée ;
- comment chaque transformation a modifié les candidats ;
- pourquoi chaque token a été choisi ;
- à quelle condition la boucle s'est arrêtée ;
- quel écart de coût a été réellement mesuré avec et sans cache.

Le laboratoire ne cherche pas à obtenir une bonne réponse de SmolLM2-135M. Ce
modèle compact sert à rendre le mécanisme manipulable sur CPU.

## Prérequis matériels et logiciels

- Python compatible avec la version de PyTorch résolue ;
- `uv` pour créer et verrouiller l'environnement ;
- suffisamment d'espace pour les poids et le cache Hugging Face ;
- accès réseau pour le premier téléchargement, puis mode hors ligne possible ;
- Git pour conserver le code du laboratoire, sans versionner les poids ni
  `.venv`.

Le modèle de référence est
[`HuggingFaceTB/SmolLM2-135M-Instruct`](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct).
Un autre modèle peut être utilisé, mais il constitue alors une expérience
distincte et ne partage pas les résultats.

## État initial

Créer un projet jetable hors de Praxis. Depuis PowerShell :

```powershell
uv init --app generation-lab
Set-Location generation-lab
uv add torch transformers huggingface-hub
uv add --group test pytest
```

Ajouter au `.gitignore` :

```gitignore
.venv/
artifacts/
__pycache__/
.pytest_cache/
```

Créer :

```text
generation-lab/
├── pyproject.toml
├── uv.lock
├── src/
│   └── generation_lab/
│       ├── __init__.py
│       ├── experiment.py
│       ├── sampling.py
│       ├── stopping.py
│       └── loop.py
├── tests/
│   ├── test_sampling.py
│   ├── test_stopping.py
│   └── test_loop.py
└── artifacts/                 # non versionné
```

La résolution de dépendances et le téléchargement n'ont pas été exécutés dans
ce dépôt. Conserver les versions réellement inscrites dans `uv.lock`.

## Manifeste reproductible

Avant toute génération, interroger la révision du modèle :

```python
from huggingface_hub import HfApi

MODEL_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"
MODEL_REVISION = HfApi().model_info(MODEL_ID).sha
```

Charger ensuite le tokenizer et le modèle avec cette révision exacte. Enregistrer
dans `artifacts/manifest.json` :

- `model_id` et `model_revision` ;
- versions de Python, PyTorch, Transformers et Hugging Face Hub ;
- système d'exploitation, device et dtype ;
- seed ;
- messages exacts ;
- configuration de génération ;
- hash du `uv.lock`.

Ne pas recopier dans le manifeste un token d'authentification ni un chemin
personnel inutile.

## Expérience 1 · Observer les frontières du texte

Écrire une fonction qui reçoit :

```python
["é", "e\u0301", "👨‍👩‍👧‍👦", "\ud800"]
```

Pour chaque entrée, conserver :

- `repr(text)` ;
- points de code ;
- longueurs de `str` et des octets UTF-8 ;
- formes NFC et NFD ;
- erreur éventuelle en encodage UTF-8 strict.

### Critère de réussite

Le rapport distingue une chaîne visuellement identique, sa séquence de points
de code et ses octets. Le surrogate isolé n'est pas présenté comme une valeur
scalaire UTF-8 valide.

## Expérience 2 · Ouvrir le tokenizer

Charger le tokenizer avec `revision=MODEL_REVISION`. Pour un corpus contenant
français, espaces répétés, code, emoji et chaîne décomposée, conserver :

- texte original ;
- tokens d'inspection ;
- identifiants ;
- nombre de tokens ;
- texte décodé avec options explicites ;
- égalité ou différence de l'aller-retour.

Implémenter en parallèle le BPE miniature de la leçon et conserver ses quatre
premières fusions. Ne pas comparer la qualité de ce BPE jouet au tokenizer du
modèle.

### Variation à provoquer

Comparer `é` et `e\u0301`, puis les mêmes valeurs normalisées en NFC. Expliquer
quelle étape modifie le comptage.

## Expérience 3 · Identifier les tokens de contrôle

Exporter sans hypothèse préalable :

```python
tokenizer.special_tokens_map
tokenizer.all_special_ids
tokenizer.all_special_tokens
```

Associer chaque token déclaré à son identifiant. Rechercher dans la
configuration de génération les identifiants EOS et padding réellement
utilisés.

### Variation à provoquer

Construire une séquence avec le Template, puis tenter une seconde tokenisation
avec et sans ajout automatique de tokens spéciaux. Conserver les deux listes
d'identifiants et localiser la duplication éventuelle.

## Expérience 4 · Rendre le Template de chat

Utiliser ces messages :

```python
MESSAGES = [
    {"role": "system", "content": "Réponds en une phrase factuelle."},
    {"role": "user", "content": "Décris le rôle d'un cache KV."},
]
```

Conserver :

- le Template brut du tokenizer ;
- `repr()` du texte rendu ;
- identifiants produits directement par `apply_chat_template(tokenize=True)` ;
- identifiants produits par rendu texte puis `encode(...,
  add_special_tokens=False)` ;
- différence avec `add_generation_prompt=False`.

### Critère de réussite

Les deux voies correctes produisent les mêmes identifiants. Toute différence
est expliquée par une option ou une étape observée, pas par une supposition.

## Expérience 5 · Inspecter les embeddings

Avec `model.eval()` et `torch.no_grad()` :

- obtenir `model.get_input_embeddings()` ;
- enregistrer la forme de sa matrice ;
- sélectionner les embeddings des identifiants du prompt ;
- vérifier que deux occurrences d'un même identifiant ont le même vecteur
  initial ;
- vérifier qu'un identifiant hors vocabulaire échoue.

Ne pas interpréter une distance observée comme une définition sémantique.

## Expérience 6 · Faire tourner RoPE

Implémenter la rotation 2D de la leçon et vérifier l'identité pour deux paires
de positions ayant le même déplacement.

Inspecter ensuite la configuration RoPE du checkpoint : type, base, scaling,
dimension et longueur maximale lorsqu'ils sont exposés. Distinguer les valeurs
absentes des valeurs supposées par défaut dans le code de la version installée.

### Variation à provoquer

Appliquer RoPE à `Q` et `K`, puis à `V` également. Expliquer pourquoi la seconde
expérience ne reproduit plus l'architecture inspectée.

## Expérience 7 · Reconstruire une tête d'attention

Écrire une tête à une seule dimension de batch et sans autograd :

- projections déjà fournies sous forme de `Q`, `K`, `V` ;
- scaling ;
- masque causal ;
- softmax stable ;
- somme pondérée des valeurs.

Conserver la matrice des scores avant masque, après masque et après softmax.

### Panne à provoquer

Masquer après softmax. Montrer l'invariant cassé et corriger en masquant avant
la normalisation.

## Expérience 8 · Suivre le residual stream

Implémenter RMSNorm et deux sous-blocs fictifs :

```text
y = x + attention(norm(x))
z = y + mlp(norm(y))
```

Conserver `x`, les deux valeurs normalisées, les deux mises à jour, `y` et `z`.
Vérifier les formes et le comportement quand une mise à jour vaut zéro.

### Variation à provoquer

Déplacer la normalisation après l'addition avec les mêmes fonctions. Comparer
les valeurs sans prétendre comparer deux modèles entraînés.

## Expérience 9 · Ouvrir le MLP

Implémenter SiLU et la porte SwiGLU simplifiée. Avec un hook limité au
laboratoire, relever les formes d'entrée et de sortie du premier MLP du modèle.

Le chemin de module est propre à l'architecture inspectée. Le hook ne rejoint
pas l'API de Praxis.

### Critère de réussite

La sortie du MLP retrouve la dimension cachée et chaque position est traitée
sans accès direct aux autres positions dans ce sous-bloc.

## Expérience 10 · Projeter vers le vocabulaire

Exécuter un passage avant sur le prompt tokenisé :

```python
outputs = model(**inputs, use_cache=False)
next_logits = outputs.logits[0, -1]
```

Conserver :

- forme complète des logits ;
- taille du vocabulaire ;
- dix logits maximaux avec identifiants et représentation de token ;
- présence du ou des EOS dans le vecteur ;
- configuration de partage des embeddings lorsqu'elle est exposée.

Ne pas appeler les logits « probabilités » dans l'artefact.

## Expérience 11 · Normaliser les logits

Implémenter softmax stable dans `sampling.py`. Tester :

- somme proche de un ;
- invariance à l'ajout d'une constante ;
- conservation de l'argmax ;
- refus de `NaN`, de `+inf`, d'une liste vide et d'un vecteur entièrement
  masqué ;
- poids nul pour un candidat isolé à `-inf` ;
- comparaison à `torch.softmax` avec une tolérance annoncée.

Conserver le maximum de l'écart absolu observé. Cette valeur est un résultat du
laboratoire, pas une constante du cours.

## Expérience 12 · Déformer une même distribution

Sur une copie immuable des mêmes logits, appliquer séparément :

- températures `0.5`, `1.0` et `2.0` ;
- top-k avec plusieurs valeurs ;
- top-p avec plusieurs seuils ;
- min-p avec plusieurs seuils ;
- repetition penalty ;
- présence et fréquence additives.

Produire `artifacts/sampling.csv` avec, pour chaque configuration :

- nombre de candidats conservés ;
- probabilité maximale ;
- entropie ;
- cinq premiers candidats ;
- ordre exact des transformations.

### Variation à provoquer

Comparer `température → top-p` à `top-p → température`. Conserver un cas où les
candidats diffèrent, ou conclure honnêtement qu'aucun des logits testés n'a
produit de différence et construire alors une distribution jouet qui l'exhibe.

## Expérience 13 · Tirer et reproduire

Injecter un `torch.Generator` ou un générateur local explicitement seedé.

1. Produire deux séries avec mêmes poids, même seed et même environnement.
2. Consommer un tirage supplémentaire avant la seconde série.
3. Lancer un chemin greedy sans RNG.
4. Refaire l'expérience après redémarrage du processus.

Conserver les séries et l'état environnemental. Ne conclure qu'à la portée
réellement testée.

## Expérience 14 · Exécuter la boucle autorégressive

Construire d'abord la boucle avec un modèle scripté. Les tests doivent couvrir :

- un token ajouté par tour ;
- logits transformés avant le sampler ;
- budget maximal ;
- EOS ;
- distribution invalide ;
- erreur du modèle.

Brancher ensuite le modèle réel sans cache. Conserver pour chaque tour :

```json
{
  "step": 0,
  "input_length": 0,
  "selected_token_id": 0,
  "selected_token_repr": "",
  "selected_probability": 0.0,
  "visible_fragment": "",
  "stop_reason": null
}
```

Les zéros montrent la forme attendue, pas un résultat.

## Expérience 15 · Décoder un flux sans le corrompre

Tester d'abord les fragments UTF-8 `C3` puis `A9` avec un décodeur incrémental.

Avec le tokenizer réel, comparer :

1. décodage de chaque identifiant puis concaténation ;
2. décodage cumulatif de toute la séquence ;
3. streamer fourni par la bibliothèque, si son contrat est applicable.

Conserver toute divergence. Si aucun token du texte choisi ne coupe une
séquence UTF-8, le noter et conserver l'expérience artificielle comme preuve du
mécanisme.

## Expérience 16 · Provoquer chaque raison d'arrêt

Avec le modèle scripté, provoquer séparément :

- EOS ;
- chacune de deux stop sequences, dont une traverse deux fragments ;
- `max_new_tokens` ;
- distribution invalide ;
- limite de contexte.

Provoquer aussi EOS sur le dernier token du budget pour tester la priorité
choisie. Vérifier qu'une stop sequence exclue n'apparaît jamais dans les
fragments publiés.

## Expérience 17 · Comparer avec et sans cache

Produire en greedy la même courte séquence :

- par recalcul du préfixe complet ;
- avec un cache dynamique explicite.

Comparer les identifiants et les logits à chaque pas avec une tolérance
documentée. Mesurer ensuite, après échauffement :

- durée du prefill ;
- durée de chaque pas de decode ;
- tokens par seconde sur la portion mesurée ;
- mémoire du cache lorsque le runtime et le device permettent une mesure
  fiable.

Effectuer plusieurs répétitions et conserver toutes les valeurs brutes. Ne pas
comparer des chronométrages comprenant le premier téléchargement ou le
chargement du modèle.

## Expérience 18 · Atteindre la frontière de contexte

Lire la capacité configurée puis construire des prompts de longueurs
croissantes. Le compteur utilise `apply_chat_template(..., tokenize=True)`.

Avant d'exécuter une requête :

```text
input_tokens + reserved_output <= effective_capacity
```

Tester les trois frontières :

- égalité exacte ;
- dépassement d'un token ;
- prompt qui tient avant Template mais dépasse après Template.

Ne pas lancer une allocation dangereuse pour le matériel. La validation du
budget peut être testée avec une capacité fictive.

## Résultats à conserver

```text
artifacts/
├── manifest.json
├── unicode.json
├── tokenizer.json
├── chat-template.txt
├── special-tokens.json
├── architecture.json
├── sampling.csv
├── trajectory.jsonl
├── stopping.json
├── cache-timings.csv
└── context-boundaries.json
```

Chaque fichier contient les entrées et la configuration qui permettent
d'interpréter ses résultats. Un graphique sans données brutes ne suffit pas.

## Critères de réussite du Parcours 0

- le texte est distingué de ses points de code, octets et tokens ;
- le Template et le tokenizer exacts produisent une séquence traçable ;
- l'inférence fournit un logit par candidat ;
- la pipeline de transformations est ordonnée et laisse au moins un candidat ;
- le sampler utilise un RNG propre au run ;
- la boucle est bornée et chaque étape produit un événement ;
- le décodage incrémental ne corrompt aucun fragment ;
- chaque arrêt possède une raison typée ;
- avec et sans cache, le chemin greedy est équivalent dans la tolérance testée ;
- aucune conclusion de performance n'est avancée sans résultats bruts.

## Pannes et variations supplémentaires

- remplacer le tokenizer par celui d'un autre checkpoint ;
- retirer `add_generation_prompt` ;
- dupliquer BOS ;
- masquer les positions futures après softmax ;
- réinitialiser la seed à chaque tour ;
- publier immédiatement tout suffixe d'une stop sequence ;
- réutiliser un cache avec un autre prompt ;
- compter les caractères au lieu des tokens.

Chaque panne doit casser un invariant ou produire une différence explicable.
Une différence non comprise reste un résultat à diagnostiquer, pas une preuve.

## Nettoyage

Après conservation des résultats utiles :

```powershell
Set-Location ..
Remove-Item -Recurse -LiteralPath '.\generation-lab'
```

Avant la suppression, résoudre le chemin absolu et vérifier qu'il désigne
uniquement le projet jetable. Les poids partagés dans le cache Hugging Face ne
sont pas supprimés automatiquement.

## Références

- [Model card SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) —
  modèle compact et exemple officiel de chargement.
- [Transformers — génération](https://huggingface.co/docs/transformers/main_classes/text_generation) —
  API industrielle comparée à la reconstruction.
- [Transformers — caches KV](https://huggingface.co/docs/transformers/kv_cache) —
  stratégies de cache actuelles.
- [PyTorch — reproductibilité](https://docs.pytorch.org/docs/stable/notes/randomness.html) —
  portée des mesures déterministes.
