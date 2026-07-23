# Clean code production-grade

> [carte du cours](../carte.md)

## L'essentiel

« Production-grade » veut dire quelque chose de précis : du code
qu'un collègue peut modifier sans peur. Cinq
pratiques concrètes — typing, Pydantic, pytest, packaging,
docstrings — appliquées **à la promotion** de chaque brique, pas en
grand soir final.

## Le savoir

- **Typing** : signatures annotées partout, `mypy`/`pyright` en CI
  locale ; `typing.Protocol` pour les interfaces de briques (pas
  d'héritage forcé). Le type est la première documentation.
- **Pydantic aux frontières** : tout ce qui entre ou sort du framework
  (configs, messages, sorties LLM, payloads d'API) passe par un modèle
  validé — l'intérieur peut rester en dataclasses légères.
- **pytest** : les evals du domaine retrieval **sont** des tests (assertion sur
  un score) ; ajouter les tests unitaires des briques (client mocké,
  outils, troncature) et les tests contractuels des providers.
  Convention : un fichier de test par brique.
- **Packaging** : `pyproject.toml`, layout `src/`, install éditable
  (`pip install -e .`) — c'est ce qui permet aux autres domaines
  d'importer le framework proprement
  ([tests, typing, packaging](../framework/tests-typing-packaging.md)
  fait le même mouvement côté RAG).
- **Docstrings** : minimales dans le code (convention du parcours — le
  `.md` compagnon porte la pédagogie) ; une docstring = le contrat, pas
  le tutoriel.

## En pratique

À chaque promotion de brique : annoter → modéliser les frontières en
Pydantic → écrire les tests → déclarer dans `pyproject.toml` → relire
la docstring comme un contrat. Ordre fixe, ~une heure par brique.

## Pièges connus

- Le grand refactoring « qualité » en fin de parcours : la qualité se
  paie en continu ou se paie très cher.
- Typer sans vérifier : des annotations jamais passées à mypy mentent
  en silence.
- Tester le LLM au lieu du code : les tests unitaires mockent le
  client ; le comportement du modèle, lui, se mesure aux evals.

## Se tester

> « Qu'est-ce qui distingue votre code d'un script de data scientist ? »
> Interfaces typées et vérifiées, validation aux frontières, tests qui
> tournent sans GPU, packaging installable, et des evals chiffrées pour
> la partie probabiliste — la réponse tient dans le repo.

## Références

- mypy / pyright ; Pydantic v2 ; pytest ; doc packaging Python
  (`pyproject.toml`, src layout)
