## Connaissances

### Le pipeline d'un tokenizer

Un tokenizer industriel peut enchaîner plusieurs mécanismes :

1. une normalisation éventuelle ;
2. un pré-tokenizer qui trouve des frontières candidates ;
3. un modèle de segmentation, par exemple BPE ou Unigram ;
4. une correspondance entre unités et identifiants ;
5. un post-traitement qui ajoute éventuellement des tokens spéciaux.

Réduire la tokenisation à `texte.split(" ")` perd la ponctuation, les espaces,
les langues sans séparateurs et la possibilité de représenter les mots absents
du vocabulaire.

### Le vocabulaire

Le vocabulaire est une correspondance finie entre des unités tokenisées et des
entiers. L'identifiant n'a pas de sens universel : `42` ne désigne pas le même
token dans deux vocabulaires différents. Les poids d'embedding ont été appris
avec une correspondance précise ; permuter deux identifiants sans permuter les
poids change le modèle.

La taille du vocabulaire règle un compromis. Un grand vocabulaire peut
représenter davantage de fragments fréquents avec peu de tokens, mais agrandit
la table d'embeddings et la projection de sortie. Un petit vocabulaire réduit
ces matrices, mais allonge les séquences.

### BPE

Le Byte Pair Encoding adapté aux sous-mots part d'unités de base et apprend des
fusions sur un corpus. À chaque itération d'entraînement, une paire adjacente
fréquente devient une nouvelle unité. Le vocabulaire final réunit les unités de
base et les unités apprises.

À l'encodage, le tokenizer applique les règles apprises et leur priorité. Il ne
recalcule pas les fréquences sur le texte de l'utilisateur. Deux tokenizers
BPE peuvent donc produire des segmentations différentes avec le même texte.

Une variante byte-level part des 256 valeurs d'octet, généralement rendues sous
une forme interne imprimable. Cette base peut représenter toute chaîne d'octets
sans token inconnu, mais elle permet aussi qu'un token isolé corresponde à un
fragment UTF-8 incomplet.

### SentencePiece n'est pas un synonyme de BPE

SentencePiece est une bibliothèque et un format d'entraînement applicables
directement au texte brut. Elle peut utiliser BPE ou un modèle Unigram. Elle
représente notamment l'espace par un symbole interne, souvent `▁`, afin que la
segmentation ne dépende pas d'un découpage préalable en mots.

Dire qu'un modèle « utilise SentencePiece » ne suffit donc pas pour déduire son
algorithme, sa normalisation, son traitement des octets inconnus ou son
vocabulaire. Il faut inspecter les artefacts du tokenizer.

### Encodage, décodage et aller-retour

`decode(encode(text)) == text` est une propriété souhaitable, mais elle dépend
des normalisations et des options de nettoyage. Un tokenizer qui normalise
avant la segmentation peut produire un texte canonique différent de l'original.

Le décodage d'un token isolé n'est pas nécessairement un inverse local de
l'encodage. Certaines règles reconstituent les espaces ou accumulent plusieurs
fragments byte-level. L'aller-retour se vérifie sur une séquence complète et
avec des options explicites.
