# Filtres métadonnées

> [carte du cours](../carte.md)

## L'essentiel

Chercher « backup » dans *toute* la doc quand on sait que la réponse
vit dans `architecture/` est un handicap volontaire. Les filtres
métadonnées **restreignent la recherche vectorielle à un sous-ensemble
du payload** (dossier, type de doc) — exigés tels quels par les offres
seniors, et gratuits chez nous : les métadonnées existent depuis le
[chunking](chunking.md).

## Le savoir

- **La mécanique Qdrant** : un objet `filter` dans la requête
  (`must` / `should` / `must_not` sur les champs du payload) — la
  recherche ANN ne considère que les points qui matchent.
- **Pre- vs post-filtering, le point d'architecture** :
  - *post* (naïf) : chercher top-k puis filtrer — risque de top-k vide
    si le filtre est sélectif ;
  - *pre* (Qdrant) : le filtre s'applique **pendant** la traversée
    HNSW, avec des index de payload pour rester rapide — déclarer un
    index sur les champs filtrés souvent (`fichier_source`, `type`).
- **D'où viennent les filtres à l'exécution** :
  1. explicites (paramètre d'API — la
     [2.4.1](service-fastapi.md)
     l'exposera) ;
  2. déduits de la question (« dans la doc réseau… » → filtre
     `reseau/`) — un LLM léger peut extraire le filtre : ce sont les
     « filtres dynamiques » du context engineering
     ([roadmap couche 0](../_archive/roadmap.md)) ;
  3. de sécurité (périmètre par utilisateur) — hors scope homelab,
     mais LE cas entreprise à mentionner en entretien.
- **Effet sur les scores** : filtrer améliore la *précision* (moins de
  candidats hors sujet) mais peut tuer le *rappel* si le filtre est
  faux — mesurer les deux dans
  [2.2.5](evals-comparatives.md).

## En pratique

Ajouter `filtres` à la signature `chercher(question, k, filtres)` de
`rag_commun` (déjà prévue par l'interface de la brique retrieval),
indexer les champs de payload, et ajouter au jeu d'evals 2-3 questions
où le filtre change la donne.

## Pièges connus

- Filtrer sur un champ non indexé : correct mais lent — Qdrant scanne ;
  déclarer les index de payload.
- Le filtre déduit trop zélé : « backup » → filtre `backup/` alors que
  la réponse vit dans `architecture/nas.md` — un filtre déduit doit
  pouvoir s'élargir en cas de top-k vide (fallback sans filtre).
- Incohérence de vocabulaire : filtrer `type: "doc"` alors que
  l'indexation a écrit `type: "documentation"` — les métadonnées sont
  un contrat, à valider comme tel.

## Se tester

> « À quoi servent les métadonnées dans un RAG en production ? »
> Citations (source exacte), filtres de pertinence (dossier/type),
> périmètres de sécurité par utilisateur, et debug (d'où vient ce
> chunk ?) — elles se décident au chunking, pas après coup.

## Références

- Doc Qdrant : filtering et payload indexes
- [Roadmap couche 0](../_archive/roadmap.md) — « RAG et filtres
  dynamiques » dans le context engineering
