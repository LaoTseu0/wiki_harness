# Progression — 02-homelab-rag (Module 2)

> **Double rôle** : (1) re-briefer Claude en début de session — *commencer
> chaque session par « lis PROGRESSION.md »* — et (2) consolider
> l'apprentissage d'Anthony en rendant le parcours visible.
> **Tenu à jour par Claude à chaque étape franchie.**
> Roadmap complète : [../roadmap.md](../roadmap.md) (ce projet = Module 2).
> Module précédent : [../01-llm-from-scratch/PROGRESSION.md](../01-llm-from-scratch/PROGRESSION.md).
> Dernière mise à jour : 20 juillet 2026

---

## Le projet

Un RAG sur la doc du homelab : poser « qu'est-ce qu'on avait décidé pour
le backup du NAS ? » et obtenir une réponse **sourcée** depuis les `.md`
de ce repo. Trois versions successives (à la main → Qdrant → LlamaIndex),
avec des **evals dès la v1** — la partie la plus valorisable du module.

- Corpus : les `.md` du repo homelab (architecture/, serveurs/, guides/,
  exploration/…) — ~17 fichiers de vraie doc. **Depuis l'extraction du
  21 juillet 2026, homelab est un repo frère** : `RACINE` pointe vers
  `../homelab` (les deux repos doivent être côte à côte).
- Embeddings : via l'Ollama de jarvis-central (`http://192.168.1.57:11434`),
  modèle `nomic-embed-text` (à puller — constat du 20 juillet : seul
  Qwen3 4B est présent).
- Génération : Qwen3 4B, comme au Module 1.
- Outillage : mise + venv auto (`mise.toml` et `requirements.txt` à la
  racine du repo — un seul moteur Python pour tous les modules,
  décision du 21 juillet 2026), httpx.

## Checklist v1 — le RAG entièrement à la main

- [x] **01_embeddings.py** — premier embedding : texte → vecteur via
      `/api/embed` ; 768 dims quelle que soit la longueur du texte,
      norme toujours égale à 1
- [x] **02_similarite.py** — `similarite_cosinus()` **écrite par Anthony
      du premier coup** (squelette à trous, protocole de test fourni avec
      valeurs attendues — les 5 paires OK) ; détour pédagogique réussi par
      la géométrie (schémas + widget interactif : flèches, Pythagore,
      produit scalaire = alignement, division par les normes = on ne garde
      que l'angle)
- [ ] **03_chunking.py** — découper les `.md` du repo en chunks
      (par sections markdown), avec le fichier source gardé en métadonnée
- [ ] **04_indexer.py** — pipeline chunk → embedding → SQLite
      (l'index complet du corpus, reconstructible)
- [ ] **05_rechercher.py** — question → embedding → top-k chunks
      les plus proches (le « R » de RAG, sans génération)
- [ ] **06_rag.py** — la chaîne complète : retrieval → prompt avec
      contexte → réponse avec citations des fichiers sources
- [ ] **07_evals.py** — jeu de questions/réponses attendues sur la doc,
      score automatisé déterministe (retrieval + génération), baseline chiffrée
      *(→ étendre le jeu vers ~30 et ajouter le LLM-as-judge)*

> **Exercices 03→07 préparés le 20 juillet 2026** (session Anthony absent) —
> squelettes à trous avec valeurs attendues **réelles**, à faire par Anthony.
> Toute la chaîne a été écrite en entier puis **vérifiée de bout en bout**
> par Claude (les trous remplis tournent et sortent les valeurs annoncées),
> puis les trous ont été ré-ouverts : le *scaffolding* est donc connu-bon,
> seule la logique reste à écrire. Ordre imposé : **03 → recopier
> `decouper_en_sections` dans `rag_commun.py` → 04 → 05 → 06 → 07**.
> - `rag_commun.py` : bibliothèque partagée (embedder + similarite_cosinus
>   déjà remplies depuis 01/02 ; `decouper_en_sections` = 1er trou, à
>   recopier du 03). La « promotion en bibliothèque » du code validé.
> - `evals/questions.json` : 12 questions à mot-clé factuel attendu.
> - `schemas/*.png` : 6 schémas (pipeline, chunking, indexation, top-k,
>   grounding, evals) — support visuel, générés avec matplotlib.
> - **Baseline v1 mesurée : retrieval 7/12, génération 7/12.** Les deux
>   scores identiques = **zéro hallucination** (chaque échec est un échec
>   de *retrieval* ; quand le bon chunk manque, le modèle dit « je ne
>   sais pas »). La v1 est honnête mais sa recherche est médiocre — c'est
>   le point de départ chiffré que la v2 (Qdrant, hybride, meilleur
>   chunking) doit battre. Cause racine des 5 échecs : le gros chunk
>   « (intro) » d'`etat.md` (7830 car.) dilue les faits précis, et le
>   bon *fichier* ressort parfois sans le bon *chunk*.

## Checklist v2 — Qdrant + retrieval hybride

- [ ] migrer le stockage vers **Qdrant** (conteneur docker sur le homelab)
- [ ] retrieval hybride (BM25 + vecteurs), re-ranking, filtres métadonnées
- [ ] re-passer les evals : tableau comparatif v1 → v2

## Checklist v3 — LlamaIndex + outillage standard

- [ ] refaire la chaîne en **LlamaIndex** ; documenter ce que le framework
      apporte / cache
- [ ] passer le jeu d'evals dans **RAGAS** ou **DeepEval**
- [ ] tableau final v1 → v2 → v3 dans le README
- [ ] réponse d'entretien rédigée : **RAG vs fine-tuning**, pourquoi RAG ici

## Notions acquises (validées en pratique)

| Notion | Vue dans | L'essentiel |
|---|---|---|
| Embedding = coordonnées du sens | 01 | texte → vecteur 768 floats (analogie RGB : ressemblance devenue distance calculable) ; taille fixe quelle que soit la longueur du texte ; aucune dimension n'a de sens seule |
| Vecteurs Ollama normés à 1 | 01 | `/api/embed` renvoie des vecteurs de norme 1 (vérifié) → le dénominateur du cosinus vaut ~1, cos ≈ produit scalaire |
| Norme = Pythagore en 768D | 02 | somme des carrés = longueur² ; `sqrt` défait les carrés pour revenir à une longueur |
| Produit scalaire = alignement | 02 | somme des produits terme à terme ; grand si les flèches sont d'accord, 0 si perpendiculaires, négatif si opposées — mais mélange direction et longueur |
| Cosinus = angle pur | 02 | produit scalaire / (norme × norme) : la division retire les longueurs, seule la direction (le sens) reste |
| `zip(v1, v2)` + expression génératrice | 02 | parcourir deux listes en parallèle ; `sum(a*b for a, b in zip(...))` = produit scalaire en une ligne |
| L'espace est multilingue | test 02 | question FR vs sa traduction EN : 0.81, la paire la plus proche du banc — le sens a une position, pas la langue ; un RAG FR peut interroger de la doc EN |
| Le score absolu ne veut rien dire | test 02 | backup NAS vs tarte aux pommes : 0.53, pas 0 — les scores se tassent dans une bande étroite ; **seul le classement compte** (d'où le top-k, jamais de seuil absolu) |

## Points de vigilance / à revoir

- Leçon du Module 1 (exercice 08) : pour les exercices denses, fournir un
  **squelette à trous** ou découper en sous-fonctions — c'est l'assemblage
  qui coûte, pas la syntaxe. **Validé sur l'exercice 02** : fonction juste
  du premier coup.
- Anthony apprend mieux avec du **visuel** : les schémas (SVG/widgets
  interactifs) pour les concepts géométriques/abstraits ont très bien
  fonctionné pour produit scalaire/norme/cosinus — réutiliser l'approche
  (chunking, espace vectoriel, HNSW à venir).
- Les énoncés d'exercices doivent **spécifier toutes les valeurs attendues**.
- **Le corpus est vivant** (constat du 21 juillet 2026) : la doc homelab
  évolue pendant le module — un `exploration.md` vide apparu à la racine
  a fait passer le compte de 19 à 20 fichiers (0 section, il est vide).
  Réflexe : si les valeurs attendues divergent, vérifier d'abord si le
  corpus a bougé avant de chercher le bug dans le code. C'est exactement
  le problème que les evals de non-régression détectent en production.
- `nomic-embed-text` : ajouté à `deploiement/jarvis-central/installer.sh`
  (config-as-code, réflexe d'Anthony) — déployer via commit + git pull +
  `./installer.sh` sur jarvis-central avant le premier script.

## Conventions du projet

- Scripts numérotés `NN_sujet.py`, commentaires en français sans accents
  dans le code (compat encodage console Windows).
- Fichier `.md` compagnon (convention 21 juillet 2026, dès l'exercice 03) :
  chaque `NN_sujet.py` a un `NN_sujet.md` court (concept, objectif, valeurs
  attendues) ; docstring minimale dans le script ; bonus : ces `.md` sont
  indexables par le RAG.
- Versionnage semver (décision du 21 juillet 2026) : plus de « v1/v2/v3 »
  fermées — les générations du RAG sont des jalons tagués 0.1.0 (à la
  main), 0.2.0 (Qdrant), 0.3.0 (LlamaIndex) ; tout livrable sort tôt en
  0.0.1 et évolue incrémentalement.
- Chaque étape : Claude explique le concept → écrit/teste le script →
  Anthony bidouille → questions → cocher ici.
