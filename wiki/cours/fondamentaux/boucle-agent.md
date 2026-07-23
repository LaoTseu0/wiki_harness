# Mini-boucle d'agent

> [carte du cours](../carte.md) · étape : [`07_agent.py`](../../etapes/fondamentaux/07_agent.py)

## L'essentiel

Un agent n'est **rien d'autre** qu'une boucle while autour du function
calling : réfléchir → appeler un outil → lire le résultat →
recommencer, jusqu'à ce que le modèle réponde sans outil (ou qu'un
plafond l'arrête). Le pattern Pi : 4 outils, ~200 lignes. Tout le
« agentic AI » des offres d'emploi tient là-dedans.

## Le savoir

- **La boucle** : tant que la réponse contient un `tool_call`, exécuter
  et renvoyer ; sinon, c'est la réponse finale. Ajouter `MAX_TOURS` —
  un agent sans plafond est une facture (ou une boucle) infinie.
- **Les 4 outils canoniques** : `read` / `write` / `edit` / `bash` —
  suffisants pour des tâches réelles sur des fichiers. C'est la
  « manual implementation » des référentiels.
- **Le sandboxing dès le premier jour** :
  - périmètre `workspace/` + **garde anti path-traversal** (résoudre le
    chemin, vérifier qu'il reste sous la racine) ;
  - **validation humaine** des commandes shell avant exécution
    (human-in-the-loop) — le germe du hook `tool_call` du
    [garde-fous et sécurité d'abord](../agent/garde-fous.md).
- **Leçons d'incidents** (vécues, à raconter) :
  - le modèle a fait une **typo dans un argument** (fichier mal nommé) ;
  - il a auto-corrigé `rm` → `del` selon la plateforme ;
  - il a **nié une suppression** pourtant prouvée par le listing — un
    tool result s'interprète encore par génération probabiliste :
    *les outils fiabilisent les données, pas le raisonnement* ;
  - contre-épreuve à faire un jour : rejouer ces incidents sur un
    modèle nettement plus grand (jarvis-core, RTX 4090) pour trier ce
    qui est artefact de taille de ce qui est défaut de nature —
    « teubé par taille, pas par nature » est une hypothèse, pas un
    acquis.

## En pratique

[07_agent.py](../../etapes/fondamentaux/07_agent.py) : sandbox `workspace/` (ignoré par
git), `ecrire_fichier` **écrit par Anthony** (try/except au-delà de la
spec), validation humaine, MAX_TOURS.

## Pièges connus

- Donner `bash` sans validation humaine « parce que c'est local » — un
  agent est exactement aussi dangereux que ses outils.
- Ne pas tracer les tours : sans log de chaque tool_call, un
  comportement erratique est indébogable.
- Prompt système d'agent trop long : chaque tour le re-paye
  (→ [prompt caching](../inference/prompt-caching.md)).

## Se tester

> Quels risques ouvre un agent qui a accès aux fichiers ?
> *Réussi si* la réponse nomme au moins trois surfaces distinctes —
> path-traversal, commandes destructives, exfiltration par outil,
> injection via le contenu lu — et associe à chacune sa défense :
> sandbox, moindre privilège, liste noire plus validation humaine,
> plafond de tours.

## Références

- Le pattern Pi — le harnais minimal dont cette boucle est la copie
- [securite.md §5 du homelab](../../../../homelab/architecture/securite.md)
  — les non-négociables
