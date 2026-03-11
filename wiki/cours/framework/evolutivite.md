# Évolutivité sans friction

> [carte du cours](../carte.md)

## L'essentiel

Le critère d'architecture du framework tient en une phrase : **ajouter
un outil, un provider ou un agent = créer un fichier, zéro modification
du cœur**. Si une extension demande d'éditer trois fichiers existants,
l'architecture a une dette — c'est mesurable, donc c'est un test.

## Le savoir

- **Le principe** : ouvert à l'extension, fermé à la modification (le
  O de SOLID) — appliqué avec les moyens simples de Python, pas avec
  une usine à gaz.
- **Le mécanisme : le registre**. Chaque type extensible a un point
  d'enregistrement unique :

  ```python
  # outils/meteo.py — un fichier, rien d'autre à toucher
  @registre.outil
  class Meteo:
      nom = "meteo"
      description = "Prévisions pour une ville"
      schema = MeteoArgs  # modèle Pydantic
      def run(self, args: MeteoArgs) -> str: ...
  ```

  Trois implémentations possibles, par ordre de simplicité : import
  explicite d'un package `outils/` (suffisant ici), découverte par
  décorateur au chargement, entry points de packaging (pour des
  plugins tiers — hors périmètre).
- **La même mécanique partout** : outils (`registre.outil`), providers
  (`registre.provider("ollama")`), agents (préréglages boucle +
  outils + garde-fous). Un seul pattern à apprendre.
- **Ce que ça achète** : le domaine agent ajoutera `home_assistant`
  ([outil home_assistant](../agent/outil-home-assistant.md))
  sans toucher au cœur — la preuve vivante que le critère tient.

## En pratique

Test d'architecture à automatiser : écrire un outil jouet dans un
nouveau fichier, vérifier qu'il apparaît dans `tools/list` de l'agent
sans qu'aucun fichier du cœur n'ait changé (`git diff --stat` vide hors
du nouveau fichier).

## Pièges connus

- Le registre global muable importé partout : préférer un registre
  construit explicitement au démarrage (testable, pas d'effets de bord
  d'import).
- L'extension « presque sans friction » : si le nouveau provider doit
  aussi être ajouté à un `Enum` central, le critère est déjà cassé.
- Sur-généraliser : un système de plugins avec hooks, priorités et
  events pour trois outils — la friction déplacée, pas supprimée.

## Se tester

> « Comment concevez-vous un système extensible sans le
> sur-concevoir ? »
> Un point d'extension par besoin *avéré*, un registre simple, un test
> qui vérifie le critère « un fichier suffit » — et l'exemple concret
> de l'outil ajouté au domaine agent.

## Références

- Le principe ouvert/fermé (SOLID) ; entry points Python (pour situer
  la version industrielle du pattern)
