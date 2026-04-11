# Gabarit d'une leçon

Ce fichier fixe la forme de toute leçon de la V2. Ce n'est pas une leçon : on ne le lit pas dans le parcours, on s'y conforme en écrivant. C'est un contrat — une leçon qui ne le tient pas ne rentre pas.

Deux échecs de la V1 le guident.

- **Le plan partait dans tous les sens.** Désormais chaque leçon déclare, en tête, ce dont elle dépend et ce qu'elle débloque.
- **La langue était approximative.** Les conventions de langage d'AGENTS.md la cadrent, et la liste de contrôle la sanctionne. Une leçon juste sur le fond mais mal formulée ne sera pas validée.

## Frontmatter

Chaque leçon s'ouvre sur un bloc de métadonnées. Il n'est pas décoratif : `promeut` pointe une brique qui existe dans `src/hosef/`, et un contrôle échoue si elle ment. Le reste identifie et date la note : `id` (slug stable, unique dans le dépôt), `type`, `tags`, `created`, `updated`.

```yaml
---
id: sampling
type: leçon
titre: Le sampling
tags: [generation, sampling]
created: 2026-07-24
updated: 2026-07-24
promeut: hosef/sampling.py        # ou : aucune — <raison en une ligne>
---
```

Les prérequis, ce que la leçon débloque, le processus et l'étape ne sont plus dans le frontmatter : ils vivent dans le corps — `Prérequis et suites` et `Savoir le situer` — écrits une seule fois.

## Les trois interdits

Ils priment sur tout, et un modèle qui rédige ne peut pas les respecter par bonne volonté — ils se vérifient après coup.

1. **Ne jamais inventer une mesure.** Aucun chiffre de performance, latence, taille ou score ne s'écrit sans avoir été produit ici. « Mesuré à l'étape N », répété sans le chiffre, le matériel et le modèle, est la même faute déguisée en preuve. Un chiffre qui se **redéduit** du mécanisme — un écart d'un logit fait un rapport d'environ 2,7 en probabilité — n'est pas une mesure : il s'écrit librement, avec le calcul qui le produit.
2. **Ne jamais inventer un vécu.** Un incident, une panne, une erreur de parcours ne se racontent que s'ils ont eu lieu. Pas d'anecdote plausible, pas de « on observe souvent que ».
3. **Ne jamais livrer la solution d'un exercice non fait.** Le code de `cas-pratique/` est un squelette à trous avec son protocole.

Tant que l'étape n'a pas tourné, le chiffre est **absent** — pas de section réservée, pas de cadre à combler. Il se coud dans `Connaissances` le jour où il existe, contre l'affirmation qu'il prouve, avec son matériel et son modèle.

## `Savoir le situer` et son schéma

La leçon ne décrit pas son schéma : elle déclare quel **processus** elle traverse et quelle **étape** elle ouvre. Deux lignes, jamais plus.

```markdown
## Savoir le situer

- **Processus** : [d'un texte à un token](../_processus/generation-token.md)
- **L'étape ouverte** : `sampler` — Input : des logits ; Output : un identifiant de token
- **L'essentiel**
- **Recomposer**

![[sampling.canvas]]
```

Le schéma se **génère**, il ne se dessine pas. Le processus est décrit une seule fois dans `_processus/` ; les leçons n'en redonnent jamais leur version, et une mécanique fausse se corrige à un seul endroit. Un `.canvas` édité à la main sera écrasé.

```bash
python outils/canvas.py            # régénère tout
python outils/canvas.py --verifier # échoue si un schéma est périmé
```

Une leçon « situer » qui ne porte sur aucun processus n'a pas de schéma, et c'est normal.

## Le squelette

Un seul plan, quel que soit le niveau.

```markdown
---
<frontmatter complet>
---

# Titre

> [cartographie](../cartographie.md) · cas pratique : [`NN_sujet.py`](../cas-pratique/…)

## Prérequis et suites
---
## Savoir le situer
---
## Connaissances
---
## Ce que ça dépose dans Hosef
## Références
```

Une leçon « situer » sans cas pratique réduit le sous-titre à `> [cartographie](../cartographie.md)` seul, omet le processus et l'étape dans `Savoir le situer`, et porte `promeut : aucune` dans le frontmatter. `Ce que ça dépose dans Hosef` dit alors pourquoi rien.

## Ce que contient chaque rubrique

Le squelette donne la forme ; cette section dit ce qui la remplit, et jusqu'où pousser. Chaque rubrique a **un** travail. Le référentiel — la liste de notions sous chaque Parcours dans [cartographie](cartographie.md) — fixe l'exhaustif : une notion qu'il cite et que la leçon tait est un trou. Chaque *écueil* ci-dessous rejoue une ligne de la liste de contrôle, il n'ajoute aucune règle.

Partout : registre impersonnel (« on »), une idée par phrase, le concret avant la règle, le jargon technique en anglais. On nomme la pièce, jamais « le système ».

### Le titre et le sous-titre

- **Rôle** — nommer la pièce, sans détour.
- **Contenu** — un seul concept, aucun « et ». Le sous-titre porte deux ancres : le lien vers la cartographie, et — si la leçon a un exercice — le lien vers son `cas-pratique/`.
- **Écueil** — un titre qui couvre deux notions ; c'est le signe qu'il faut deux leçons.

### `Prérequis et suites`

- **Rôle** — orienter avant d'entrer : ce qu'on tient déjà, ce que ça ouvre.
- **Contenu** — les prérequis rendus en liens, chacun avec la raison de sa présence en cinq mots. Puis ce que la leçon débloque, en liens. C'est ici, et non dans le frontmatter, que vivent les dépendances.
- **Forme** — deux listes courtes, aucune prose de remplissage.
- **Écueil** — recopier les slugs sans dire à quoi chacun sert ; nommer un prérequis que la leçon n'utilise jamais.

### `Savoir le situer` — le tout, puis l'arc H-A-H

Rubrique composite : faire voir la machine entière, y placer la pièce, énoncer la thèse, reposer la pièce en idée. Quatre sous-parties, toutes en puces, dans cet ordre. Les deux premières décrivent le schéma ; une leçon « situer » sans processus les omet.

- **`Processus`** — le processus traversé, en lien vers `_processus/`. On le nomme, on ne redécrit pas la chaîne.
- **`L'étape ouverte`** — l'étape que la leçon ouvre, avec sa signature (Input → Output).
- **`L'essentiel`** — la thèse, une à trois phrases. L'affirmation centrale, écrite pour être vérifiable — celle que retient qui s'arrête là. Portante, pas une phrase d'introduction.
- **`Recomposer`** — reposer la pièce dans la machine et **en tirer une prédiction sur autre chose**. Jamais un résumé. Pour une leçon « situer », c'est ici que tombe le critère de décision : quand tendre la main vers cette pièce.

### `Connaissances` — les parties, l'exhaustif

- **Rôle** — le corps. Décomposer la pièce, exposer chaque levier.
- **Contenu** — couvrir **tous** les leviers que le référentiel liste pour cette notion ; aucun laissé dans l'ombre. Une sous-notion qui mérite sa leçon part en lien ; une mineure se pose en trois lignes ou file au glossaire. Contre chaque levier, trois choses collées : sa **portée** (où il agit, à quelle fréquence, ce qu'il propage, ce qui l'annule), son **mode de rupture** (le piège, le rencontré distingué de l'anticipé), son **chiffre** mesuré quand l'étape a tourné — matériel et modèle à l'appui, absent sinon.
- **Forme** — un `###` par levier si utile. Paragraphes courts, une idée chacun.
- **Écueil** — un levier sans sa portée ; une propriété posée par l'adjectif-verdict seul ; un chiffre sans provenance ; une notion du référentiel oubliée.

### `Ce que ça dépose dans Hosef` — le retour au tout, en code

- **Rôle** — nommer la brique que la leçon repose dans le framework.
- **Contenu** — si `promeut` pointe un module : son nom, sa surface publique (fonction ou classe exposée), et en quoi c'est le mécanisme qu'on vient d'apprendre, rendu réutilisable. Ça répond à la ligne *Intégration* du Parcours dans la cartographie. Si `promeut : aucune` : « Rien : cette leçon situe, elle n'implémente pas — <raison> ».
- **Forme** — courte. Une signature esquissée est bienvenue ; l'implémentation complète, non.
- **Écueil** — décrire un code qui ne colle pas au `promeut` de l'en-tête ; livrer la solution de l'exercice.

### `Références`

- **Rôle** — où creuser, et sur quoi la leçon s'appuie.
- **Contenu** — les sources premières (papiers, doc officielle, notes de `raw/` qui ont nourri la leçon), chacune avec la raison de l'ouvrir. Aucune citation inventée.
- **Forme** — liste courte.
- **Écueil** — l'URL nue ; une référence qui ne fait que répéter la leçon.

## La liste de contrôle

Chaque ligne se répond par oui ou non. Un seul non, la leçon repasse.

1. Le niveau (refaire / situer) se lit-il sans ambiguïté — un processus et une étape présents pour « refaire », absents pour « situer » ?
2. Le frontmatter est-il complet, et `promeut` pointe-t-il vers une cible réelle, ou porte-t-il sa raison d'être « aucune » ?
3. La leçon tient-elle sur **un** concept, sans « et » dans son titre ?
4. `Savoir le situer` nomme-t-il un processus existant et une étape réelle, sans redécrire la chaîne ?
5. Le schéma se génère-t-il, et `--verifier` passe-t-il ?
6. Toute notion supposée connue est-elle liée à sa leçon, ou posée sur place en trois lignes ?
7. Toute propriété affirmée porte-t-elle son mécanisme, jamais l'adjectif-verdict seul ?
8. Chaque levier est-il donné avec sa portée — où il agit, à quelle fréquence, ce qu'il propage, ce qui l'annule ?
9. `Recomposer` produit-il une prédiction sur autre chose, plutôt qu'un résumé ?
10. Tout chiffre est-il produit ici, cousu dans `Connaissances` contre l'affirmation qu'il prouve, avec son matériel et son modèle — ou simplement absent ?
11. Les pièges cités dans `Connaissances` distinguent-ils le rencontré de l'anticipé, sans anecdote inventée ?
12. La langue tient-elle les conventions d'AGENTS.md — registre, une idée par phrase, aucune auto-référence ?
13. La leçon dit-elle ce qu'elle dépose dans Hosef, ou pourquoi rien ?

---

**Note sur la génération.** Les contrôles qui portent sur le vécu et le mesuré (10, 11) ne sont pas satisfiables par un modèle : il ne peut que les fabriquer de façon plausible. Une leçon générée est donc **complète sur le savoir et volontairement trouée sur le réel**. Les trous se comblent à l'exécution, par la personne qui a fait l'étape.
