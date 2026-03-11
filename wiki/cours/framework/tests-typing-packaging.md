# Tests, typing, packaging

> [carte du cours](../carte.md)

## L'essentiel

Pas de domaine « qualité » séparé : le craftsmanship monte *avec* les
leçons, ou il ne monte pas.
Ici, le RAG reçoit ses premiers tests pytest (les evals en sont le
germe), son typing, et son packaging : les trois gestes qui font d'un
projet un **candidat à la promotion** en brique du framework.

## Le savoir

- **Trois étages de tests, trois vitesses** :
  1. **unitaires** (ms, sans réseau) : chunking (sections préservées,
     blocs de code insécables), similarité (valeurs connues), fusion
     RRF, parsing — le cœur déterministe ;
  2. **intégration** (s, service local) : la chaîne sur un mini-corpus
     de test avec provider mocké ou Ollama local — `POST /ask` renvoie
     sources et schéma valides ;
  3. **evals-as-tests** : `assert score_retrieval >= baseline` — la
     non-régression de la
     [evals du RAG](../retrieval/evals.md)
     devient un test marqué `@pytest.mark.eval` (lent, GPU) qu'on
     lance avant chaque tag.
  Le mock vit à la frontière provider
  ([backend commutable](providers.md)) —
  l'abstraction paye immédiatement.
- **Typing** : signatures annotées sur `rag_commun`, `mypy` en local ;
  les modèles Pydantic du service comptent double (validation à
  l'exécution + types statiques).
- **Packaging à la promotion** : `pyproject.toml`, layout `src/`,
  `pip install -e .` — le domaine MCP importera `homelab_rag` proprement
  au lieu de bricoler des chemins. Détail des pratiques dans
  [clean code production-grade](../framework/clean-code.md).
- **Le trio minimal** : tests, packaging, revue. Chacun répond à une
  question qu'on se posera sur la brique six mois plus tard — est-elle
  encore juste, s'installe-t-elle, quelqu'un d'autre l'a-t-il lue.

## En pratique

`tests/` avec les trois étages, marqueurs pytest (`-m "not eval"` pour
le rapide), mypy sans erreur sur la bibliothèque, `pyproject.toml` —
et le critère de fin : un `pip install -e .` + `pytest -m "not eval"`
verts depuis un clone frais.

## Pièges connus

- Tester le modèle au lieu du code : les tests rapides mockent le
  LLM ; le comportement du modèle appartient aux evals — mélanger les
  deux rend la CI non déterministe.
- Le mini-corpus de test qui dérive du vrai : le garder minuscule
  (3 documents) et **dédié** — les evals, elles, tournent sur le vrai
  corpus.
- Packager sans `src/` layout : les imports passent en local et cassent
  installé — le layout `src/` force l'honnêteté.

## Se tester

> « Comment testez-vous un système dont le cœur est non déterministe ? »
> Séparer : unitaires rapides sur le déterministe (chunking, fusion,
> parsing), intégration avec LLM mocké à la frontière provider, et
> evals chiffrées pour le probabiliste — trois vitesses, trois
> marqueurs, une baseline en assertion.

## Références

- [Clean code production-grade](../framework/clean-code.md)
  — le référentiel complet des pratiques
- Doc pytest (markers) ; doc packaging (`src/` layout)
