# Registre des schémas non séquentiels

Ce registre complète les processus. Il contient les architectures, cartes de
concepts, arbres de décision, cycles de vie et cartes de responsabilités qui
servent de repères holistiques aux leçons sans flux temporel.

## Registre

| Identifiant | Type | Parcours | Portée | Canvas | Statut |
|---|---|---:|---|---|---|
| `environnement-projet-python` | architecture | Préambule | déclaration, résolution, environnement et distribution d'un projet Python | [[references/environnement-projet-python.canvas\|ouvrir]] | cadré |
| `representation-texte` | carte de concepts | 0 | caractère abstrait, point de code, encodage, octets et unité visible | [[references/representation-texte.canvas\|ouvrir]] | cadré |

Les statuts suivent le même contrat que les processus :

- `inventorié` — le besoin et la portée sont connus ;
- `cadré` — le Canvas canonique existe et peut être référencé ;
- `validé` — la carte a été confrontée aux leçons et aux cas d'échec.

## Contrat d'identité

- le fichier canonique vit dans `generator/guardrails/schema/references/` ;
- son nom est `<identifiant-du-schema>.canvas` ;
- son identifiant et ceux de ses éléments sont stables ;
- une leçon reprend ces valeurs dans `schema` et `element` ;
- le type déclaré ici fixe la signification des groupes et des arêtes.

Une correction se fait dans le Canvas canonique. Les vues contextualisées sont
ensuite régénérées dans `generator/guardrails/schema/canvas/`.

## Lecture d'une vue de leçon

- `ÉLÉMENT OUVERT` en violet désigne la pièce étudiée ;
- `RELATION DIRECTE` en cyan désigne les éléments qui lui sont reliés ;
- les autres éléments restent neutres.

Ces couleurs ne créent aucun ordre temporel. Le sens de chaque relation est
porté par le libellé de son arête.
