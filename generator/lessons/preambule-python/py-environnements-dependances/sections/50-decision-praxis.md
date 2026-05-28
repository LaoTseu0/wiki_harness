## Décision et dépôt dans Praxis

- **Décision** — Praxis et Mnémos posséderont chacun leur `pyproject.toml`, leur
  `.venv` et leur **lockfile**. Aucun environnement Python ne vivra à la racine.
- **Frontend** — **uv** gérera l'interpréteur, la résolution, le **lockfile**, la
  synchronisation et l'exécution.
- **Backend initial** — `uv_build` construira les packages Python purs.
- **Alternatives** — `venv` + pip + build, Hatchling, PDM et Poetry restent des
  confrontations possibles.
- **Critère** — conserver les métadonnées standard tout en obtenant une
  reconstruction rapide et un échec explicite lorsque le **lockfile** dérive.
- **Coût accepté** — `uv.lock` dépend de **uv** et `uv_build` suit un rythme de
  version rapide.
- **Condition de révision** — besoin d'extensions natives, de scripts de build
  complexes ou d'une interopérabilité que l'export `pylock.toml` ne couvre pas.
- **Contrat** — aucun contrat Python public n'est encore déposé. La leçon
  prépare le contenant des futurs contrats de Praxis.
