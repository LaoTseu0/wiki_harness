## Connaissances

### Les messages sont une structure applicative

Une interface de chat manipule des objets tels que :

```python
[
    {"role": "system", "content": "Réponds brièvement."},
    {"role": "user", "content": "État du serveur ?"},
]
```

Le Transformer decoder-only reçoit une séquence d'identifiants. Le Template
doit donc encoder l'ordre, les rôles, les frontières de messages et le point où
une réponse est attendue.

Deux modèles entraînés avec des formats différents peuvent employer les mêmes
noms de rôles tout en exigeant des séquences incompatibles. Un Template n'est
pas interchangeable parce qu'il « ressemble » à ChatML ou à une autre
convention.

### Le moindre séparateur fait partie du prompt

Un retour à la ligne, un espace ou un token de fin de tour modifie le texte puis
la tokenisation. Les espaces ajoutés par un moteur de Template ne sont pas une
question esthétique. Ils deviennent des données du modèle.

Dans Transformers, le Template est généralement une expression Jinja associée
au tokenizer. `apply_chat_template()` reçoit notamment `messages` et
`add_generation_prompt`. Les tokens déclarés dans la carte des tokens spéciaux
sont accessibles au Template.

### Ouvrir un nouveau tour ou continuer le dernier

`add_generation_prompt=True` demande au Template d'ajouter, lorsqu'il en
possède un, le préfixe qui annonce un nouveau message assistant. Certains
Templates n'en ont pas besoin ; l'option peut alors ne rien changer.

Continuer un message assistant déjà commencé est un autre contrat. Ajouter le
préfixe d'un nouveau tour dans ce cas sépare le préremplissage de sa suite.
Les API distinguent donc l'ouverture d'un nouveau message et la continuation du
dernier message.

### Sérialiser puis tokeniser sans double ajout

Deux chemins doivent être comparés :

```python
ids_directs = tokenizer.apply_chat_template(messages, tokenize=True)
texte = tokenizer.apply_chat_template(messages, tokenize=False)
ids_separes = tokenizer.encode(texte, add_special_tokens=False)
```

Si le Template contient déjà les marqueurs requis, la seconde tokenisation
désactive leur ajout automatique. Le contrat utile est l'égalité des
identifiants finaux, pas seulement l'égalité de deux chaînes affichées.

### Un Template ne protège pas les instructions

Les délimiteurs aident le modèle à reconnaître les rôles appris. Ils ne
constituent pas une séparation de privilèges comparable à celle d'un processus
ou d'une sandbox. Le contenu utilisateur reste dans le contexte du modèle et
peut tenter d'influencer son comportement.

Praxis conserve donc le rôle comme métadonnée en dehors du texte sérialisé.
Les politiques d'autorisation ne lisent jamais le texte généré comme une preuve
d'autorité.
