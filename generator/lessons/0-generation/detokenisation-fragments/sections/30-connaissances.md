## Connaissances

### Le token n'est pas sa chaîne d'affichage

Les interfaces d'inspection montrent souvent une représentation lisible d'un
token. Cette représentation peut échapper des octets, remplacer les espaces par
un symbole ou afficher un token spécial. La concaténer n'est pas
nécessairement l'algorithme de décodage.

Le décodeur du tokenizer connaît les conventions du modèle : fusion des
sous-mots, restauration des espaces, byte fallback, tokens spéciaux et options
de nettoyage.

### Un fragment UTF-8 peut être incomplet

Le caractère `é` précomposé s'encode en `C3 A9`. Si deux tokens ou deux
fragments transportent séparément `C3` puis `A9`, le premier octet ne peut pas
être décodé seul en mode strict.

Le bon comportement consiste à conserver l'octet incomplet, attendre la suite
et n'émettre `é` qu'après réception de la séquence valide. Remplacer
immédiatement `C3` par `�` rend la corruption irréversible.

### Décodage incrémental

Un décodeur incrémental conserve l'état nécessaire entre les appels. Pour
UTF-8, cet état comprend notamment les octets de fin encore incomplets. Quand
`final=True`, toute séquence incomplète restante devient une erreur selon la
politique configurée.

Un tokenizer peut avoir une logique supplémentaire au-dessus d'UTF-8. Le
contrat général de Praxis ne doit donc pas exposer uniquement
`bytes.decode("utf-8")`.

### Deux stratégies pour streamer

1. utiliser l'API de décodage incrémental du tokenizer ;
2. redécoder la séquence cumulée et n'émettre que le suffixe nouvellement
   stabilisé.

La seconde stratégie est plus coûteuse et demande de gérer les corrections de
frontière ou de nettoyage. Elle reste préférable à `decode([token])` puis
concaténation lorsque le tokenizer n'offre pas de stream.

### Tokens spéciaux et texte visible

`skip_special_tokens=True` peut masquer BOS, EOS ou des marqueurs de rôle.
Cette option convient souvent à l'affichage, mais elle perd des informations de
contrôle. Praxis conserve séparément :

- les identifiants complets ;
- les fragments visibles ;
- les événements de contrôle.

Un EOS peut ainsi arrêter la boucle sans apparaître dans le texte rendu.

### Buffer de sortie

Le fragment décodable n'est pas forcément immédiatement publiable. Une stop
sequence peut commencer à sa fin. La politique d'arrêt peut retenir un petit
suffixe ambigu jusqu'à savoir s'il appartient au texte ou au marqueur d'arrêt.

Le décodeur produit du texte valide ; la politique de publication décide ce qui
peut sortir vers l'utilisateur.
