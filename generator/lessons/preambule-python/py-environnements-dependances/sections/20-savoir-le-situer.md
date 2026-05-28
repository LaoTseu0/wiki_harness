## Savoir le situer

**Ensemble** —
[[generator/guardrails/schema/references/environnement-projet-python.canvas|architecture d'un projet Python]].  
Les groupes représentent des frontières versionnées, locales ou distribuées.
Chaque arête nomme une relation ; sa direction ne représente pas le temps.

**Élément ouvert** — `environnement-virtuel`.  
L'interpréteur de base le fonde, le [[glossaire/frontend-de-projet|frontend de projet]] le crée et le
synchronise, `pyproject.toml` en contraint le contenu, le [[glossaire/lockfile|lockfile]] précise la
résolution et `site-packages` reçoit les distributions installées.

**L'essentiel** — Un [[glossaire/environnement-virtuel|environnement virtuel]] est une matérialisation locale et
jetable. La déclaration appartient à `pyproject.toml`, la résolution exacte au
**lockfile** et l'état installé à `.venv`.

**Recomposer** — Supprimer `.venv` ne supprime ni l'intention du projet ni sa
résolution. Une synchronisation peut le reconstruire. Modifier directement son
contenu crée au contraire un état qui n'est expliqué ni par `pyproject.toml` ni
par le **lockfile**.

![[py-environnements-dependances.canvas]]
