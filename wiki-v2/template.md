# Gabarit d'une leçon

Ce fichier fixe la forme de toute leçon de la V2. Ce n'est pas une leçon : on ne le lit pas dans le parcours, on s'y conforme en écrivant. C'est un contrat — une leçon qui ne le tient pas ne rentre pas.

Deux échecs de la V1 le guident.

- **Le plan partait dans tous les sens.** Désormais chaque leçon déclare, en tête, ce dont elle dépend et ce qu'elle débloque. 
- **La langue était approximative.** Une section entière la cadre, et la liste de contrôle la sanctionne. Une leçon juste sur le fond mais mal formulé ne sera pas valider.

## Le mouvement : du tout aux parties, puis retour au tout

Une leçon descend du tout vers les parties, puis remonte. Ce n'est pas un ornement : c'est la forme du dépôt. Le framework est le tout ; chaque leçon en détache une pièce pour la comprendre ; la promotion la repose dans le tout.

| Phase   | Rubrique              | Geste mental                             |
| ------- | --------------------- | ---------------------------------------- |
| Info    | `Prérequis et suites` | ce dont ça dépend, ce que ça ouvre       |
| Tout    | `Savoir le situer`    | voir la machine entière, situer la pièce |
| —       | `L'essentiel`         | la thèse, vérifiable                     |
| —       | `Recomposer`          | reposer la pièce, prédire ailleurs       |
| Parties | `Connaissances`       | décomposer, exposer le mécanisme         |


**`Recomposer` n'est pas un résumé.** Résumer, c'est redire les parties en plus court. Recomposer, c'est remettre la pièce dans l'ensemble et en tirer une compréhension sur son utilité dans son ensemble. Il est obligatoire.

## Deux niveaux : refaire ou situer

| Niveau | On doit savoir… | Squelette |
|---|---|---|
| **Refaire** | le réimplémenter et prédire son comportement | A |
| **Situer** | l'expliquer, le reconnaître, décider quand l'employer | B |

Le niveau se déclare dans l'en-tête, il ne se devine pas. Une leçon « situer » peut être promue « refaire » plus tard ; l'inverse n'arrive pas. Dans le doute, prendre A : une étape de trop coûte moins cher qu'une boîte noire.

## L'en-tête

Chaque leçon s'ouvre sur un bloc de métadonnées. Il n'est pas décoratif : c'est lui qui rend le parcours vérifiable par un outil. Les prérequis pointent vers des leçons qui existent ; l'étape existe dans `etapes/` ; la brique promise existe dans `src/framework/`. Un contrôle échoue si l'un ment.

```yaml
---
titre: Le sampling
niveau: refaire            # refaire | situer
statut: prévue             # prévue | écrite | mesurée
mouvement: 1-la-physique
prérequis: [tokenisation, le-template-de-chat]
débloque: [prompting, structured-output]
processus: generation-token          # ou : aucun
étape: sampler                        # l'étape ouverte dans le processus
promeut: framework/sampling.py        # ou : aucune — <raison en une ligne>
---
```

`statut` dit où en est la leçon, sans le commenter dans le corps : `prévue` (titre réservé), `écrite` (savoir complet, réel encore troué), `mesurée` (l'étape a tourné, les chiffres sont là).

## La langue

Le fond juste ne suffit pas. La V1 a échoué là-dessus ; la V2 en fait un motif de rejet.

- **Registre écrit, précis.** Pas de béquilles de l'oral (« du coup », « en gros », « un peu »), pas d'emphase commerciale (« puissant », « incontournable »).
- **Une phrase, une idée.** Phrases courtes par défaut. Un paragraphe défend une seule affirmation.
- **Toute propriété affirmée porte sa cause.** Interdit : l'adjectif-verdict seul (« instable », « coûteux »). On donne le mécanisme qui le produit, ou on se tait.
- **Nommer la pièce, pas « le système ».** Si la phrase reste vraie en remplaçant le nom par « le système », elle n'explique rien.
- **Le concret avant l'abstrait.** L'exemple porte la règle ; la règle ne flotte pas seule.
- **Pas d'auto-référence.** Ni « dans cette leçon nous allons voir », ni statut, ni date, ni note sur sa propre rédaction dans le corps.
- **Le terme technique est un lien** à sa première occurrence utile : vers la leçon qui le traite, sinon vers `glossaire/` (définition créée si absente). Le glossaire ne garde que ce qui n'a pas de leçon.

## Les trois interdits

Ils priment sur tout, et un modèle qui rédige ne peut pas les respecter par bonne volonté — ils se vérifient après coup.

1. **Ne jamais inventer une mesure.** Aucun chiffre de performance, latence, taille ou score ne s'écrit sans avoir été produit ici. « Mesuré à l'étape N », répété sans le chiffre, le matériel et le modèle, est la même faute déguisée en preuve. Un chiffre qui se **redéduit** du mécanisme — un écart d'un logit fait un rapport d'environ 2,7 en probabilité — n'est pas une mesure : il s'écrit librement, avec le calcul qui le produit.
2. **Ne jamais inventer un vécu.** Un incident, une panne, une erreur de parcours ne se racontent que s'ils ont eu lieu. Pas d'anecdote plausible, pas de « on observe souvent que ».
3. **Ne jamais livrer la solution d'un exercice non fait.** Le code de `cas-pratique/` est un squelette à trous avec son protocole.

Emplacement à ne pas combler tant que l'étape n'a pas tourné :

```markdown
<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->
```

## `Savoir le situer` et son schéma

La leçon ne décrit pas son schéma : elle déclare quel **processus** elle traverse et quelle **étape** elle ouvre. Deux lignes, jamais plus.

```markdown
## Savoir le situer

- **Processus** : [d'un texte à un token](../_processus/generation-token.md)
- **L'étape ouverte** : `sampler` — entrent des logits, sort un identifiant de token

![[sampling.canvas]]
```

Le schéma se **génère**, il ne se dessine pas. Le processus est décrit une seule fois dans `_processus/` ; les leçons n'en redonnent jamais leur version, et une mécanique fausse se corrige à un seul endroit. Un `.canvas` édité à la main sera écrasé.

```bash
python outils/canvas.py            # régénère tout
python outils/canvas.py --verifier # échoue si un schéma est périmé
```

Une leçon « situer » qui ne porte sur aucun processus n'a pas de schéma, et c'est normal.

## Squelette A — « refaire »

```markdown
---
<en-tête complet>
---

# Titre

> [cartographie](../cartographie.md) · étape : [`NN_sujet.py`](../etapes/…)

## Où ça s'emboîte
## Prérequis et suites
## L'essentiel
## Le savoir
## En pratique
## Mesures
<!-- À MESURER — ne rien écrire ici sans avoir exécuté l'étape -->
## Recomposer
## Pièges connus
## Se tester
## Ce que ça change dans le framework
## À retenir
## Références
```

## Squelette B — « situer »

Pas d'étape, donc pas de mesure ni de promotion. Le tout n'est plus une chaîne qui tourne mais un paysage ; la recomposition devient un critère de décision.

```markdown
---
<en-tête ; processus, étape, promeut : aucun>
---

# Titre

> [cartographie](../cartographie.md)

## Prérequis et suites
## L'essentiel
## Le savoir
## Quand c'est la bonne réponse
## Ce qu'on ne saura pas faire
## Se tester
## À retenir
## Références
```

## La liste de contrôle

Chaque ligne se répond par oui ou non. Un seul non, la leçon repasse.

1. Le niveau (refaire / situer) est-il déclaré, et le bon squelette employé ?
2. L'en-tête est-il complet, et chacun de ses liens pointe-t-il vers une cible réelle ?
3. La leçon tient-elle sur **un** concept, sans « et » dans son titre ?
4. `Où ça s'emboîte` nomme-t-il un processus existant et une étape réelle, sans redécrire la chaîne ?
5. Le schéma se génère-t-il, et `--verifier` passe-t-il ?
6. Toute notion supposée connue est-elle liée à sa leçon, ou posée sur place en trois lignes ?
7. Toute propriété affirmée porte-t-elle son mécanisme, jamais l'adjectif-verdict seul ?
8. Chaque levier est-il donné avec sa portée — où il agit, à quelle fréquence, ce qu'il propage, ce qui l'annule ?
9. `Recomposer` produit-il une prédiction sur autre chose, plutôt qu'un résumé ?
10. Tout chiffre a-t-il été produit ici, avec son matériel et son modèle — ou l'emplacement est-il vide et marqué ?
11. Les pièges rencontrés sont-ils séparés des pièges anticipés, et racontés en entier ?
12. La langue tient-elle la section « La langue » — registre, une idée par phrase, aucune auto-référence ?
13. La leçon dit-elle ce qu'elle dépose dans le framework, ou pourquoi rien ?

---

**Note sur la génération.** Les contrôles qui portent sur le vécu et le mesuré (10, 11) ne sont pas satisfiables par un modèle : il ne peut que les fabriquer de façon plausible. Une leçon générée est donc **complète sur le savoir et volontairement trouée sur le réel**. Les trous se comblent à l'exécution, par la personne qui a fait l'étape.
