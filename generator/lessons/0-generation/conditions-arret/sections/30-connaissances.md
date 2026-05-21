## Connaissances

### **EOS**

**EOS** est un identifiant de vocabulaire choisi comme les autres. La politique
d'arrêt compare l'identifiant produit à un ensemble configuré. Elle peut
exclure ce token du texte visible tout en le conservant dans la trajectoire.

Forcer **EOS** lorsque le budget est atteint n'est pas équivalent à observer un **EOS**
spontané : le premier est une intervention du [[glossaire/runtime|runtime]], le second un choix du
modèle. Les raisons doivent rester distinctes.

### **Stop sequences**

Une **stop sequence** est une chaîne ou une séquence d'octets recherchée dans la
sortie reconstruite. Elle peut :

- traverser plusieurs tokens ;
- partager un préfixe avec une autre **stop sequence** ;
- commencer à la fin du dernier fragment reçu ;
- apparaître dans un token qui contient aussi du texte antérieur.

La publication doit donc retenir le suffixe qui pourrait encore devenir un
marqueur. Si le contrat exclut la **stop sequence** de la réponse, elle ne doit pas
avoir été streamée avant sa reconnaissance.

Une correspondance sur la chaîne décodée et une correspondance sur les
identifiants ne sont pas équivalentes. Plusieurs tokenisations peuvent parfois
former le même texte.

### Budget de sortie

`max_new_tokens` compte les tokens produits après le prompt. Il se distingue
d'une longueur totale comprenant l'entrée. Quand le compteur atteint le budget,
la boucle s'arrête même sans **EOS**.

Une valeur maximale ne réserve pas automatiquement la place correspondante
dans la fenêtre de contexte. Cette précondition sera ouverte dans la leçon
suivante sur le budget de contexte.

### Annulation, délai et erreur

Une API complète peut aussi terminer sur :

- annulation demandée ;
- délai dépassé ;
- erreur du modèle ;
- distribution invalide ;
- limite de contexte ;
- arrêt administratif ou de sécurité.

Le Parcours 0 représente déjà ces issues comme des raisons typées, mais les
politiques de retry, d'approbation et de reprise appartiennent aux Parcours 2,
5, 9 et 10.

### Priorité et simultanéité

Le dernier token autorisé peut être **EOS** au moment exact où le budget est
atteint. La politique doit choisir une priorité stable. Préférer `eos` conserve
l'information que le modèle a produit une fin ; préférer `max_new_tokens`
indique que la limite a été atteinte. Aucun choix n'est implicite.

La raison n'est pas un simple texte libre. Un enum ou une union typée permet
aux métriques et aux appelants de distinguer les issues sans parser un message.
