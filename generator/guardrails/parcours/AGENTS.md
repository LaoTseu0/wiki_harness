# Règles générales de travail

Ce fichier contient les règles canoniques qui valent pour toute intervention
dans le dépôt : langue, rigueur des affirmations et méthode de travail.

Le contrat propre au projet vit dans [REGLES.md](REGLES.md) et doit
être lu avant toute création ou modification de contenu :

@generator/guardrails/parcours/REGLES.md

## Langue

- Écrire en français naturel. Ne jamais construire une phrase en anglais pour
  la traduire mot à mot.
- Écarter les calques, faux-amis et collocations étrangères au français.
- Ne pas traduire en français les mots-clés techniques essentiels. Conserver
  leur forme d'origine lorsqu'ils nomment un concept, un contrat, une
  primitive, un champ ou une opération consacrée par l'écosystème. Une entrée
  de glossaire portant une définition en français simple doit les accompagner.
  Le terme ou l'expression doit être relié à cette entrée de glossaire.
- Conserver le jargon technique anglais lorsqu'il évite une traduction
  artificielle ou ambiguë.
- Employer notamment `Template`, `Frontmatter`, `Input` et `Output` dans leur
  sens technique. `Frontmatter` désigne le bloc de métadonnées placé en tête
  d'une note.
- Garder un registre écrit et précis. Écarter les béquilles de l'oral et
  l'emphase commerciale.
- Porter une seule idée principale par phrase.
- Nommer la pièce concernée. Le mot « système » ne remplace pas le nom d'un
  composant, d'un contrat ou d'un processus.
- Placer le concret avant l'abstrait : un exemple montre le mécanisme avant que
  la règle en tire une généralisation.
- Écarter l'auto-référence dans le contenu : ni annonce de plan, ni commentaire
  sur la rédaction, ni statut de production dans le corps d'une leçon.

## Rigueur

- Toute propriété affirmée porte sa cause ou le mécanisme qui la produit.
  L'adjectif-verdict seul ne démontre rien.
- Distinguer un fait observé, une déduction, une hypothèse et une décision de
  conception.
- Ne jamais inventer un incident, une mesure, une panne, un résultat
  d'expérience ou un usage réel.
- Ne jamais transformer une capacité annoncée par un outil en propriété
  générale de tous les outils de la même catégorie.
- Pour un sujet qui évolue, vérifier la documentation ou la spécification
  primaire actuelle. Nommer la version ou la date lorsqu'elle change la portée
  de l'affirmation.
- Privilégier les spécifications, documentations officielles, dépôts sources et
  articles de recherche. Une source secondaire sert à découvrir une piste, pas
  à fixer un mécanisme.
- Une mesure mentionne son protocole, son environnement et ce qu'elle permet
  réellement de conclure.
- Signaler une incertitude restante au lieu de la combler par une formulation
  vraisemblable.

## Méthode de travail

- Lire entièrement les instructions applicables avant d'agir.
- Préserver les modifications existantes et les fichiers hors du périmètre de
  la demande.
- Vérifier les liens, le code et les commandes concernés avant d'annoncer leur
  validité.
- Ne jamais déclarer qu'un contrôle passe sans l'avoir exécuté.
- Une refonte conserve les informations encore justes ou explique pourquoi
  elles disparaissent.
- Les messages de commit ne contiennent aucune mention de co-auteur généré par
  une IA.
