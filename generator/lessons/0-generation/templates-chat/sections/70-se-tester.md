## Se tester

1. Pourquoi deux listes de messages identiques peuvent-elles produire des
   générations différentes avec deux checkpoints ?
2. Quelle erreur produit l'enchaînement `apply_chat_template(tokenize=False)`
   puis `encode(add_special_tokens=True)` lorsque le Template contient déjà
   BOS ?
3. Quelle différence sémantique sépare l'ouverture d'un tour assistant et la
   continuation d'un message assistant ?
4. Pourquoi le rôle `system` ne doit-il pas être utilisé par la politique
   d'autorisation comme une preuve de privilège ?

[Vérifier les réponses](../../corrections/0-generation/00-parcours-0.md#04--le-texte-réellement-lu-par-le-modèle).
