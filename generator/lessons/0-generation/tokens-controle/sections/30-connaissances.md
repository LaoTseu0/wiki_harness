## Connaissances

### Réservé ne signifie pas magique

Un tokenizer peut déclarer des tokens spéciaux comme `bos_token`,
`eos_token`, `unk_token`, `pad_token` ou des tokens additionnels. Cette
déclaration permet de les reconnaître, de retrouver leurs identifiants et,
selon l'API, de les exclure du texte décodé.

Le modèle ne lit toutefois que des identifiants. Un token devient un marqueur
de début de séquence, de fin de tour ou de rôle parce que les données
d'entraînement et le runtime l'emploient ainsi. Inventer une chaîne
`<|assistant|>` dans un tokenizer qui ne la connaît pas ne crée pas un rôle.

### [[glossaire/bos|BOS]], [[glossaire/eos|EOS]] et fin de tour

- **BOS** marque éventuellement le début d'une séquence.
- **EOS** est un identifiant que la boucle peut traiter comme une fin de
  génération.
- **Fin de tour** sépare parfois deux messages sans signifier la fin absolue de
  toute conversation.

Ces rôles peuvent partager un identifiant ou utiliser des identifiants
distincts selon le modèle. Certains runtimes acceptent plusieurs identifiants
**EOS**. Aucun code générique ne doit supposer qu'il existe exactement un **BOS**, un
**EOS** ou un marqueur de fin de tour.

### [[glossaire/padding|Padding]] et token inconnu

Le **padding** aligne des séquences de longueurs différentes dans un batch. Le
masque d'attention doit empêcher les positions de remplissage de contribuer
comme du contenu. Réutiliser **EOS** comme **padding** peut être un choix de
configuration, mais il ne rend pas les deux concepts identiques.

Le token inconnu représente une unité que le tokenizer ne sait pas encoder.
Les tokenizers byte-level peuvent éviter ce cas pour une entrée encodable, mais
ce n'est pas une propriété de tous les tokenizers.

### L'ajout automatique peut dupliquer les marqueurs

Une API `encode(..., add_special_tokens=True)` peut exécuter un
post-processeur. Un **Template** de chat peut déjà émettre **BOS**, **EOS** ou des fins de
tour. Appliquer ensuite une seconde couche d'ajout automatique produit une
séquence différente de celle attendue.

La seule vérification fiable consiste à observer les identifiants finaux et à
les comparer au **Template** et à la configuration du tokenizer.

### Le contenu peut ressembler à un marqueur

Un tokenizer peut configurer un token réservé pour qu'une chaîne correspondante
soit reconnue comme une unité indivisible. Le comportement dépend de ses
options de normalisation et de découpage.

Cette reconnaissance n'est pas une barrière de sécurité. Si un utilisateur
écrit une chaîne qui ressemble à un délimiteur, seul le **Template** exact et
l'entraînement du modèle déterminent l'effet. La sécurité des instructions sera
traitée au Parcours 14.
