# Chunking

> [carte du cours](../carte.md) · étape : [`03_chunking.py`](../../etapes/retrieval/03_chunking.py)

## L'essentiel

On n'indexe jamais des documents entiers : on les découpe en **chunks**
— l'unité de retrieval. Trop petit : le sens se disperse ; trop grand :
le vecteur se dilue et le contexte déborde. Ici, le découpage suit la
**structure des `.md`** (par sections), avec le fichier source en
métadonnée — condition des citations.

## Le savoir

- **Pourquoi découper** : (1) la fenêtre du modèle d'embeddings est
  limitée ([2.1.1](embeddings.md)) ; (2) un
  vecteur qui moyenne dix sujets n'est proche de rien (dilution) ;
  (3) au retrieval on veut injecter le passage pertinent, pas 40 Ko.
- **Les stratégies, par sophistication croissante** :
  - taille fixe + chevauchement (baseline naïve, coupe au milieu des
    phrases) ;
  - récursive par séparateurs (paragraphes → phrases → mots — le
    défaut de LangChain, à savoir situer) ;
  - **structurelle** (choix du module) : les `.md` du homelab ont déjà
    des sections `##` sémantiquement cohérentes — le document est
    pré-découpé par son auteur ;
  - sémantique (couper aux ruptures de similarité entre phrases) —
    coûteuse, rarement nécessaire.
- **Métadonnées dès maintenant** : chaque chunk porte
  `{fichier_source, titre_de_section}` minimum — c'est ce qui permet
  les citations en [2.1.6](rag-complet.md)
  et les filtres en
  [2.2.4](filtres-metadonnees.md).
- **Ordres de grandeur** : viser ~200-800 tokens par chunk ; une
  section très longue se re-découpe, une minuscule se fusionne avec sa
  voisine ou garde son titre pour le contexte.

## En pratique

[03_chunking.py](../../etapes/retrieval/03_chunking.py) : parser les `.md` du corpus
homelab, découper par sections, attacher les métadonnées, afficher la
distribution des tailles (le premier réflexe de debug).

## Pièges connus

- Couper les blocs de code ou tableaux en deux : un demi-`docker
  compose` ne se retrouve jamais — traiter les blocs comme insécables.
- Perdre le titre : « ## Backup du NAS » est souvent le seul endroit où
  le sujet du chunk est nommé — le préfixer au texte du chunk.
- Optimiser le chunking à l'aveugle : c'est LE paramètre qui bouge les
  scores retrieval — ne le régler qu'avec les
  [evals](evals.md) comme juge.

## Se tester

> « Votre RAG répond mal : en quoi le chunking peut-il être coupable ? »
> Chunks trop grands (dilution du vecteur), trop petits (sens
> incomplet), coupés au mauvais endroit (l'info à cheval sur deux
> chunks), ou sans titre (le sujet n'est plus dans le texte) — et ça se
> diagnostique en regardant les chunks remontés, pas en devinant.

## Références

- [Schéma 02_chunking](../_schemas/retrieval/02_chunking.png)
- Doc text splitters de LangChain — pour situer ce que la v0.0.3
  automatisera
