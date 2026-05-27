## Limites et cas d'échec

- **La reconstruction ne prouve pas** — que les identifiants fictifs ont été
  appris avec les rôles annoncés.
- **Praxis ne garantit pas encore** — le rendu exact d'une conversation.
- **Échec provoqué** — appliquer un **BOS** dans le **Template** puis un second **BOS** par
  le post-processeur doit être détecté par un test de séquence.
- **Ouverture ultérieure** — [[04-templates-chat|Le texte réellement lu par le
  modèle]] et [[16-conditions-arret|Borner la génération]].
