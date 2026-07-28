# Registre des processus

Ce dossier contient les vues holistiques canoniques du cours.

Un processus décrit une transformation ordonnée possédant un Input global, un
Output global et un flux de données ou de contrôle. Une architecture, une
taxonomie ou une simple carte de concepts n'est pas enregistrée ici.

## Registre

| Identifiant | Parcours | Input global | Output global | Canvas | Statut |
|---|---:|---|---|---|---|
| `pipeline-evenements-async` | Préambule | configuration et source d'événements | résultats ou fin qualifiée | [[pipeline-evenements-async.canvas\|ouvrir]] | cadré |
| `generation-token` | 0 | messages structurés | texte généré et raison d'arrêt | [[generation-token.canvas\|ouvrir]] | cadré |
| `inference-transformer` | 0 | identifiants de tokens et cache éventuel | logits du prochain token | [[inference-transformer.canvas\|ouvrir]] | cadré |
| `service-inference-locale` | 1 | modèle, matériel et requêtes | réponses servies et métriques | — | inventorié |
| `requete-modele-streaming` | 2 | requête canonique | événements normalisés ou erreur typée | — | inventorié |
| `construction-contexte` | 3 | journal de session et sources | contexte borné pour une inférence | — | inventorié |
| `generation-structuree` | 4 | intention et contrainte de forme | valeur validée ou échec explicite | — | inventorié |
| `execution-outil` | 5 | appel proposé par le modèle | résultat d'outil typé et traçable | — | inventorié |
| `connexion-mcp` | 6 | client et serveur MCP | capacités découvertes et appels transportés | — | inventorié |
| `ingestion-documentaire` | 7 | sources documentaires | index versionné et interrogeable | — | inventorié |
| `retrieval-requete` | 7 | question et index | contexte sourcé et borné | — | inventorié |
| `memoire-agentique` | 8 | événement candidat | mémoire consolidée, rappelée ou oubliée | — | inventorié |
| `boucle-agent` | 9 | objectif et état initial | réponse finale, délégation ou arrêt | — | inventorié |
| `workflow-durable` | 10 | commande et état persistant | résultat reprenable et historique d'exécution | — | inventorié |
| `action-workspace` | 11 | intention de modification | changement vérifié ou refus explicite | — | inventorié |
| `delegation-sous-agent` | 12 | tâche déléguable et budget | résultat fusionné et état partagé réconcilié | — | inventorié |
| `evaluation-agent` | 13 | cas, trace et critères | mesures, diagnostic et décision de régression | — | inventorié |
| `action-securisee` | 14 | action candidate et contexte de confiance | autorisation, approbation ou refus audité | — | inventorié |
| `interaction-temps-reel` | 15 | audio, image ou événement entrant | réponse multimodale synchronisée | — | inventorié |
| `cycle-mnemos` | 16 | intention quotidienne | action domestique accomplie et mémorisée | — | inventorié |

Les statuts ont un sens précis :

- `inventorié` — Input, Output et Parcours sont connus, mais le flux doit encore
  être cadré ;
- `cadré` — le Canvas canonique existe et peut être référencé par une leçon ;
- `validé` — le Canvas a été confronté aux leçons, aux reconstructions et aux
  cas d'échec du Parcours.

Une leçon ne référence jamais un processus seulement `inventorié`. Son Canvas
est d'abord cadré, puis la leçon reprend ses identifiants stables.

## Contrat d'identité

- le nom du fichier est `<identifiant-du-processus>.canvas` ;
- l'identifiant est stable après sa première utilisation par une leçon ;
- chaque étape structurelle possède un identifiant de nœud stable ;
- une leçon reprend ces valeurs dans `processus` et `etape` ;
- deux Canvas ne décrivent pas deux versions concurrentes du même processus.

Une modification structurelle se fait dans le Canvas canonique. Les vues
contextualisées des leçons sont ensuite régénérées dans
`generator/guardrails/schema/canvas/`.

## Grammaire visuelle

Le flux principal se lit de gauche à droite. Une boucle de retour passe sous le
flux principal. Les annotations portent un identifiant commençant par `note:`
et ne représentent pas une étape.

Dans une vue de leçon générée :

- `ÉTAPE OUVERTE` en violet désigne le mécanisme étudié ;
- `AMONT` en cyan désigne ses prédécesseurs directs ;
- `AVAL` en vert désigne ses successeurs directs ;
- les autres étapes restent neutres.

La couleur accompagne toujours un libellé : le sens reste lisible sans couleur.
Le contrat complet est défini dans
[REGLES](../../parcours/REGLES.md#doctrine-visuelle).
