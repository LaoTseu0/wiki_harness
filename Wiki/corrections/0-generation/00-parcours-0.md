---
id: correction-parcours-0-generation
type: correction
titre: Corrections du Parcours 0
parcours: 0-generation
created: 2026-07-27
updated: 2026-07-27
verified: 2026-07-27
---

# Corrections du Parcours 0

Ces corrections donnent le raisonnement attendu. Elles ne donnent aucun temps
de calcul, token choisi ou résultat de modèle fictif. Les valeurs du
[laboratoire](../../cas-pratique/0-generation/00-laboratoire-generation.md)
dépendent du checkpoint, de sa révision et de l'environnement réellement
exécuté.

## 01 · Texte, Unicode et octets

1. Deux rendus identiques peuvent utiliser des séquences de points de code
   différentes, par exemple `U+00E9` contre `U+0065 U+0301`. Le tokenizer
   segmente la représentation reçue ; sans normalisation commune, ses tokens
   peuvent donc différer.
2. `errors="ignore"` supprime les octets qui ne forment pas une séquence valide.
   Le texte obtenu ne permet plus de reconstruire l'entrée ni de distinguer une
   donnée corrompue d'une donnée réellement absente.
3. L'emoji de famille réunit plusieurs points de code, dont des caractères de
   jointure, dans un grapheme cluster. `len(str)` compte les éléments de la
   chaîne Python, pas les unités perçues.
4. Une normalisation invalide un contrat lorsque la séquence exacte est
   normative : signature, hash, identifiant externe, mot de passe ou entrée
   déjà tokenisée et versionnée.

Dans le laboratoire, le surrogate isolé doit échouer en encodage UTF-8 strict.
Il peut exister dans une chaîne Python, mais n'est pas une valeur scalaire
Unicode.

## 02 · Tokenisation et vocabulaire

1. `42` n'est qu'un index. Pour lui redonner son unité et sélectionner la bonne
   ligne d'embedding, il faut le vocabulaire et sa révision.
2. L'entraînement BPE apprend une liste ordonnée de fusions à partir des
   fréquences du corpus. L'encodage applique ces règles déjà apprises ; il ne
   réentraîne pas le tokenizer sur la requête.
3. Non. Une base byte-level garantit la représentation des octets, mais un
   token ou un fragment peut s'arrêter au milieu d'une séquence UTF-8.
4. SentencePiece peut porter un modèle BPE ou Unigram et plusieurs options de
   normalisation et de byte fallback. Le nom de la bibliothèque ne fixe pas ces
   choix.

La comparaison correcte du laboratoire porte sur les identifiants et les
options d'encodage. L'affichage des tokens reste un outil d'inspection.

## 03 · Tokens de contrôle

1. Une chaîne `<eos>` n'arrête la boucle que si le tokenizer la transforme en
   un identifiant configuré comme EOS et si la politique d'arrêt inspecte cet
   identifiant.
2. Une fin de tour permet à une conversation de continuer avec un autre rôle.
   EOS termine une génération selon la politique du runtime. Un modèle peut
   utiliser deux identifiants pour préserver cette différence.
3. Le Template peut déjà émettre BOS ou une fin de tour. Un post-processeur
   exécuté ensuite ajoute une seconde occurrence et déplace tout le préfixe.
4. Le padding n'est pas du contenu. Sans masque, l'attention lui attribue des
   clés et valeurs accessibles comme aux autres positions.

Le laboratoire doit exporter la configuration observée. Une valeur absente ne
doit pas être remplacée par un identifiant « habituel ».

## 04 · Le texte réellement lu par le modèle

1. Chaque checkpoint a appris des délimiteurs, rôles et espaces précis. Deux
   Templates peuvent sérialiser la même structure applicative en deux séquences
   différentes.
2. Si le rendu contient déjà BOS, `add_special_tokens=True` peut l'ajouter une
   seconde fois. L'entrée réelle ne correspond plus à celle produite par la
   voie directe.
3. Ouvrir un tour ajoute le préfixe d'un nouveau message assistant. Continuer
   conserve le dernier message assistant comme préfixe de la même unité.
4. Le rôle `system` reste du texte dans le contexte du modèle. Il n'apporte
   aucune preuve cryptographique ni autorité sur un outil réel.

Le bon oracle est l'égalité des identifiants entre les deux voies, avec les
mêmes options. Une égalité visuelle des textes ne suffit pas.

## 05 · Embeddings de tokens

1. La table sélectionne la même ligne pour le même identifiant. Les positions
   reçoivent ensuite des informations et contextes différents par RoPE,
   attention et couches successives.
2. Il faut appliquer la même permutation aux lignes de la table d'embeddings,
   aux lignes de la projection vocabulaire et à toute configuration indexée par
   token. Oublier une seule frontière change le comportement.
3. La table du modèle transforme des identifiants en vecteurs internes appris
   pour l'inférence. Une base de documents conserve des vecteurs et des
   métadonnées destinés à retrouver des sources externes.
4. Non. Deux tenseurs peuvent avoir la même forme sans partager leur stockage
   ou leurs paramètres. La configuration et le graphe du modèle font foi.

Un identifiant hors vocabulaire doit échouer avant que le laboratoire
n'interprète une forme ou une distance.

## 06 · Représenter la position

1. Le masque causal interdit certaines relations, principalement le futur.
   RoPE module les scores autorisés selon les positions et leur déplacement.
2. Dans l'implémentation Llama inspectée, les rotations s'appliquent aux
   requêtes et aux clés. Les valeurs ne sont pas tournées par ce mécanisme.
3. Le produit de deux vecteurs tournés dépend de la différence des angles. Deux
   couples ayant le même déplacement relatif ont donc le même terme relatif
   dans la reconstruction à une fréquence.
4. La capacité d'allocation n'entraîne pas le modèle à exploiter ces positions.
   La fréquence, le scaling et la plage d'entraînement influencent la qualité.

Appliquer la rotation à `V` dans l'expérience est une variante inventée. Elle
ne doit pas être présentée comme une autre exécution du même checkpoint.

## 07 · L'attention causale

1. Sans division, la variance des produits scalaires tend à croître avec la
   dimension. Softmax se sature alors plus facilement, ce qui concentre les
   poids et réduit les gradients utiles pendant l'entraînement.
2. La clé sert à calculer la compatibilité avec la requête. La valeur transporte
   le vecteur agrégé lorsque cette clé reçoit du poids.
3. Mettre les scores interdits à `-inf` avant softmax leur donne une probabilité
   nulle tout en renormalisant les positions autorisées. Masquer après laisse
   une masse manquante.
4. Non. Un poids décrit une contribution locale dans une tête et une couche. Il
   ne suffit pas à expliquer causalement la sortie finale.
5. GQA réduit le nombre de têtes de clés et valeurs et donc notamment la taille
   du cache KV, en les partageant entre plusieurs têtes de requêtes.

L'invariant pratique est une somme de poids proche de un sur les positions
autorisées et zéro sur le futur.

## 08 · Residual stream et normalisation

1. L'addition exige deux tenseurs de même forme. La projection de sortie de
   l'attention ramène donc les têtes concaténées à la dimension cachée.
2. RMSNorm ne soustrait pas la moyenne des composantes ; elle remet à l'échelle
   selon leur racine moyenne quadratique.
3. Non. Pré-norm et post-norm composent les opérations dans un autre ordre.
   Avec les mêmes poids, elles calculent une autre fonction.
4. RMSNorm agit sur les composantes cachées d'une position. Softmax normalise
   les scores sur les candidats du vocabulaire ou les clés d'attention.

Une mise à jour nulle doit laisser le résidu inchangé. Ce test vérifie la
connexion résiduelle, pas la qualité d'un bloc réel.

## 09 · Le MLP d'une couche

1. L'attention mélange des informations entre positions. Le MLP dense courant
   transforme chaque position indépendamment avec les mêmes poids.
2. La composition de deux fonctions linéaires reste linéaire. La non-linéarité
   permet une fonction qui ne se réduit pas à une seule matrice.
3. Une projection passée par SiLU module composante par composante une seconde
   projection. La porte contrôle ainsi ce qui traverse vers la projection de
   retour.
4. Les projections vers et depuis la dimension intermédiaire contiennent un
   nombre de poids et d'opérations proportionnel à cette largeur.

Le hook du laboratoire observe une implémentation. Son chemin de module ne
devient pas un contrat Praxis.

## 10 · De la représentation aux logits

1. Un logit est un score réel non normalisé. Il peut valoir `5`, `-3` ou toute
   autre valeur sans être une proportion.
2. Pour le prochain token, la boucle prend les logits de la dernière position
   non masquée du préfixe.
3. Softmax multiplie alors tous les numérateurs par le même facteur exponentiel,
   qui s'annule avec le dénominateur.
4. Dans la projection, EOS n'est qu'un indice doté d'un score. Après le choix,
   la politique d'arrêt interprète cet identifiant.

Le laboratoire doit montrer un logit pour chaque entrée du vocabulaire, y
compris les tokens spéciaux, sans qualifier le top-10 de « certitudes ».

## 11 · Des logits à une distribution

1. Soustraire le maximum est une translation commune. Elle laisse tous les
   écarts identiques et évite les grands exposants positifs.
2. \(p_i/p_j=\exp(z_i-z_j)\). Le dénominateur commun disparaît.
3. La distribution modélise la continuité textuelle sous les poids et le
   préfixe. Elle n'est pas entraînée comme un estimateur universel de vérité.
4. Chaque token ajoute une log-probabilité négative ou nulle. Une somme brute
   pénalise mécaniquement la longueur ; il faut annoncer une normalisation ou
   un autre critère.

L'écart avec `torch.softmax` doit être enregistré depuis l'exécution. La
correction n'impose aucune valeur universelle.

## 12 · Transformer la distribution

1. La température change les probabilités et donc la masse cumulée utilisée par
   top-p. Top-p peut masquer des candidats que la température n'aura ensuite
   plus la possibilité de réintroduire.
2. Top-k conserve un nombre fixe de candidats. Top-p conserve une masse cible
   et laisse varier leur nombre.
3. Le seuil vaut \(\alpha p_{\max}\). Quand le maximum augmente, les petites
   probabilités doivent être plus élevées pour rester.
4. Repetition penalty applique une transformation multiplicative dépendant du
   signe à chaque token déjà vu. La présence applique une soustraction fixe et
   la fréquence une soustraction proportionnelle au compte, dans la famille
   additive décrite.
5. Non. Greedy maximise le prochain choix seulement. Ce token change les
   distributions futures et peut conduire à une séquence globale moins
   probable qu'une autre branche.

Le CSV du laboratoire doit conserver l'ordre. Deux lignes avec les mêmes
valeurs mais un ordre différent décrivent deux configurations distinctes.

## 13 · Tirer le prochain token

1. Initialiser une fois crée une suite de valeurs pseudo-aléatoires consommées
   au fil des tours. Réinitialiser à chaque tour rejoue toujours le premier
   état.
2. Un autre composant peut consommer une valeur entre deux tours et décaler
   toutes les valeurs suivantes.
3. Il faut au minimum le checkpoint, le tokenizer, le Template, l'entrée, les
   transformations ordonnées, les versions, le device, la précision, les
   algorithmes déterministes et l'état du RNG.
4. Pas nécessairement. Les calculs et arrondis peuvent différer, surtout devant
   des logits très proches ou des kernels non déterministes.
5. Une stratégie stochastique produit une distribution de résultats. Une seule
   seed peut être favorable ou défavorable sans représenter cette distribution.

La première portée raisonnable est : mêmes entrées et état, même
implémentation, même environnement. Toute extension doit être testée.

## 14 · Réinjecter le token choisi

1. Le token rejoint le préfixe conditionnel. Le passage suivant reçoit donc un
   autre Input et peut changer tous ses logits ; les écarts s'accumulent.
2. Le RNG avance exactement avec les tirages. Le cache, le décodeur, les
   compteurs et la séquence avancent avec leurs événements respectifs.
3. Pendant l'entraînement, les tokens cibles sont connus et le masque causal
   autorise le calcul parallèle de plusieurs positions. À l'inférence, la
   position suivante dépend d'un token encore non choisi.
4. Même si EOS n'arrive jamais ou si le modèle boucle, le budget donne un
   nombre maximal de tours et garantit la terminaison de cette boucle.

Les tests doivent employer un modèle scripté. Un modèle réel ne fournit pas un
oracle déterministe assez précis pour tester chaque branche de contrôle.

## 15 · Reconstruire le texte généré

1. Les règles de fusion, espaces, byte fallback et nettoyage peuvent dépendre
   des tokens voisins. Le décodage local perd cet état.
2. Il doit le conserver sans sortie en attendant un octet de continuation. Si
   le flux est finalisé, le mode strict signale une séquence incomplète.
3. Les identifiants servent à la réinjection, aux comptes, à EOS et à la trace.
   Le texte visible peut avoir supprimé les tokens spéciaux.
4. Le décodeur garantit la validité textuelle. La politique de publication
   retient encore un suffixe susceptible de devenir une stop sequence.

Si le tokenizer réel n'exhibe aucun fragment incomplet dans le corpus choisi,
ce résultat ne réfute pas le mécanisme ; l'expérience UTF-8 artificielle en
isole la possibilité.

## 16 · Borner la génération

1. EOS compare un identifiant choisi à une configuration. Une stop sequence
   recherche du texte ou des octets reconstruits et peut traverser plusieurs
   tokens.
2. Il faut retenir tout suffixe qui est aussi le préfixe d'une stop sequence,
   jusqu'à ce qu'une suite confirme ou invalide la correspondance.
3. `max_new_tokens` compte uniquement la sortie. Une longueur totale ajoute
   les tokens du prompt.
4. Une raison typée permet aux appelants, traces et métriques de distinguer les
   branches sans analyser un texte d'erreur.
5. Le contrat choisit une priorité et la teste. Préférer EOS conserve le fait
   que le modèle a produit sa fin ; un autre produit peut privilégier la limite.

Le booléen `stopped` est insuffisant : il perd la cause et donc la décision
possible de retry, d'affichage ou de diagnostic.

## 17 · Prefill, decode et cache KV

1. Tout le prompt est connu pendant le prefill. Pendant le decode, seule la
   nouvelle position vient d'être choisie ; les suivantes n'existent pas.
2. Le cache évite de recalculer les clés et valeurs des positions passées dans
   chaque couche.
3. La nouvelle requête doit encore être comparée aux clés conservées. Leur
   nombre augmente avec la longueur dans une attention complète.
4. Checkpoint, architecture, préfixe tokenisé, positions, masque et
   configuration de cache doivent rester compatibles.
5. Non. Le cache est un état d'accélération d'une inférence et d'un préfixe. Il
   n'applique aucune politique d'écriture, de provenance ou de rappel de
   connaissance.

L'équivalence avec et sans cache se teste sur les identifiants greedy et les
logits selon une tolérance annoncée. Les chronométrages viennent seulement
après échauffement.

## 18 · Fenêtre de contexte et coût

1. Le Template ajoute rôles, séparateurs et tokens de contrôle. Le modèle reçoit
   cette séquence finale, pas le seul contenu utilisateur.
2. Une allocation prouve que le runtime accepte une taille. La qualité à cette
   longueur exige une évaluation du checkpoint et de sa stratégie de position.
3. Le cache évite de recalculer les représentations passées. La nouvelle
   requête compare encore ses scores aux clés accessibles, donc le coût
   d'attention du pas croît linéairement avec leur nombre.
4. La latence inclut projections, MLP, transferts, kernels, batch, précision et
   matériel. L'asymptotique isole une croissance, pas une durée.
5. Une troncature silencieuse peut supprimer une instruction, couper un message
   ou changer le Template. Le Parcours 3 portera une politique explicite
   d'éviction et de compaction.

Les tests de frontière n'ont pas besoin d'allouer la capacité maximale réelle.
Une petite capacité fictive prouve les inégalités ; les mesures matérielles
restent séparées.

## Correction architecturale du laboratoire

Une séparation satisfaisante contient :

```text
Tokenizer ──> ChatTemplate ──> NextTokenModel
                                  │ logits
                                  ▼
                           LogitsPipeline
                                  │ distribution
                                  ▼
                              Sampler
                                  │ token_id
                                  ▼
GenerationLoop ──> TokenDecoder ──> StopPolicy
```

Les dépendances pointent vers des contrats, pas vers le modèle SmolLM2. Le
checkpoint n'apparaît que dans l'adaptateur du laboratoire.

Les tests unitaires utilisent des données jouets et un modèle scripté. Le test
d'intégration charge le modèle local et vérifie les invariants observables :
formes, bornes, équivalence du cache et raison d'arrêt. Une sortie linguistique
précise n'est pas un oracle stable.

