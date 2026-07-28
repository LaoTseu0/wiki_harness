# Praxis, Mnémos et intégration

## Praxis

Une brique est déposée à la fin du Parcours qui en ouvre les mécanismes.

| Brique Praxis | Rôle | Dépôt |
|---|---|---|
| `contracts` · `config` | types communs, configuration, erreurs | Préambule |
| `generation` | tokeniser, rendre un Template, échantillonner, arrêter | 0 |
| `inference` | décrire et mesurer un runtime local | 1 |
| `models` · `client` | contrats par capacité, transport et streaming | 2 |
| `context` · `sessions` | composer le contexte et persister les sessions | 3 |
| `control` | prompts, sorties contraintes et validation | 4 |
| `tools` · `permissions` · `approvals` | enregistrer, autoriser et exécuter une action | 5 |
| `mcp` | adapter des outils et ressources distants | 6 |
| `knowledge` · `retrieval` | ingérer, rechercher, reranker et citer | 7 |
| `memory` | écrire, retrouver, consolider et oublier | 8 |
| `loop` | exécuter une boucle mono-agent bornée | 9 |
| `state` · `checkpoints` · `workflow` · `effects` | persister et reprendre une exécution | 10 |
| `workspace` · `sandbox` · `skills` · `artifacts` | fournir un environnement d'action isolé | 11 |
| `agents` · `handoffs` · `router` | déléguer et coordonner plusieurs agents | 12 |
| `telemetry` · `evals` · `judge` | observer, rejouer et mesurer | 13 |
| `security` · `policy` · `audit` | imposer les frontières de confiance | 14 |
| `io` · `realtime` | porter la voix, la vision et les interruptions | 15 |

Le Parcours final assemble Mnémos. Il n'introduit aucun mécanisme de
persistance, de sécurité ou d'orchestration qui n'aurait pas été exercé
auparavant.

## Mnémos

La première version stable de Mnémos assure réellement :

- une conversation persistante ;
- une exécution locale par défaut ;
- des outils natifs et MCP derrière les mêmes politiques ;
- des approbations pour les effets sensibles ;
- une reprise après interruption ou redémarrage ;
- des tâches déclenchées par requête, événement ou horaire ;
- plusieurs natures de mémoire avec provenance et correction ;
- des sous-agents isolés et un état partagé explicite ;
- des entrées vocales et visuelles ;
- des traces, evals et journaux d'audit ;
- un mode dégradé lorsque le modèle, un outil ou le réseau manque ;
- une sauvegarde et une restauration documentées.

Mnémos n'est ni une plateforme multi-tenant, ni un produit commercial, ni un
prétexte pour distribuer prématurément chaque composant.

## Exigences transverses d'une Intégration

Une Intégration dépose :

- un contrat typé ;
- des erreurs définies ;
- des tests unitaires déterministes ;
- au moins un test d'intégration à la frontière réelle ;
- des mesures lorsque la propriété étudiée est quantitative ;
- des événements observables ;
- une analyse des effets de bord et des risques ;
- une configuration documentée ;
- les limites connues de la brique.

La sécurité et l'observabilité commencent avec la première frontière externe.
Leurs Parcours dédiés assemblent et éprouvent les mécanismes déjà déposés.

## Organisation du dépôt

| Chemin | Rôle |
|---|---|
| `generator/README.md` | point d'entrée de l'outillage de génération |
| `generator/guardrails/parcours/AGENTS.md` | règles générales de langue, de rigueur et de travail |
| `generator/guardrails/parcours/CADRAGE.md` | point d’entrée et routage du contrat |
| `generator/guardrails/parcours/fondations.md` | finalité et fondations pédagogiques |
| `generator/guardrails/parcours/cartographie.md` | ordre et couverture du parcours |
| `generator/guardrails/lecon/` | contrat commun et contrôles des leçons |
| `generator/guardrails/sections/` | règles propres à chaque rubrique |
| `generator/templates/sections/` | gabarits de fragments |
| `generator/profiles/` | sélections de rubriques par usage |
| `generator/lessons/` | contrats, états et fragments canoniques |
| `Wiki/parcours/` | leçons assemblées rangées par Parcours |
| `generator/guardrails/schema/processus/` | registre et Canvas complets des processus |
| `generator/guardrails/schema/references/` | Canvas canoniques non séquentiels |
| `Wiki/cas-pratique/` | exercices et expériences exécutables |
| `Wiki/corrections/` | réponses et corrections séparées des leçons |
| `Wiki/glossaire/` | définitions sans leçon propre |
| `Wiki/veille/` | état des techniques et protocoles mouvants |
| `generator/guardrails/schema/canvas/` | vues de leçon générées depuis les Canvas canoniques |
| `Praxis/` | bibliothèque générique et ses tests |
| `Mnemos/` | assistant concret et ses tests |
| `raw/` | sources brutes, non normatives |
| `generator/tools/` | préparation, assemblage et contrôles de génération |

Le contenu de `raw/` ne rejoint jamais une leçon sans demande explicite et
validation. Une note brute peut contenir une piste, pas une vérité du cours.

Praxis et Mnémos possèdent chacun leur runtime Python, leur `pyproject.toml`,
leur environnement virtuel et leurs dépendances. Aucun environnement Python ne
vit à la racine.

Les identifiants de code suivent les conventions de l'écosystème Python. Les
commentaires et docstrings pédagogiques sont en français, encodés en UTF-8. Les
imports passent par les packages ; aucun `sys.path.insert` ne masque un
packaging incomplet.

---
