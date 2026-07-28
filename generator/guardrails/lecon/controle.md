# Contrôles des leçons et du dépôt

## Liste de contrôle d'une leçon

Une leçon ne rejoint le parcours que si chaque réponse est positive :

1. Le Frontmatter est-il complet et cohérent ?
2. La leçon tient-elle sur un concept ?
3. Ses prérequis sont-ils disponibles et liés ?
4. Le processus et ses étapes voisines, ou l'ensemble et ses relations
   directes, sont-ils exacts ?
5. Toutes les notions exigées par la cartographie sont-elles couvertes quelque
   part ?
6. Chaque propriété importante porte-t-elle son mécanisme ?
7. Chaque levier porte-t-il sa portée et ses limites ?
8. La reconstruction isole-t-elle réellement le mécanisme ?
9. La décision Praxis nomme-t-elle ses alternatives et son critère ?
10. Si la leçon dépose un contrat, existe-t-il et ses invariants sont-ils
    testés ? Sinon, l'absence est-elle justifiée ?
11. Les questions de `Se tester` vérifient-elles autre chose qu'une récitation ?
12. Les mesures sont-elles reproductibles ?
13. Les sources sont-elles primaires, actuelles et précisément rattachées ?
14. La langue respecte-t-elle `AGENTS.md` ?
15. Le Canvas canonique, la pièce ouverte et la vue générée sont-ils cohérents ?

## Liste de contrôle d'un Parcours

Un Parcours n'est terminé que si :

1. chaque notion de la cartographie possède une destination ;
2. aucune notion majeure n'est enseignée à deux endroits ;
3. le graphe des prérequis ne contient pas de cycle accidentel ;
4. les processus et schémas référencés possèdent un Canvas complet et valide ;
5. les reconstructions s'assemblent dans l'Intégration ;
6. le cas pratique mobilise les mécanismes annoncés ;
7. les contrats Praxis et leurs tests existent ;
8. l'incrément du fil rouge Mnémos emploie réellement la brique.

## Contrôles du dépôt

Les contrôles automatisés vivent dans `generator/tools/`. Ils doivent à terme
vérifier :

- Frontmatter, identifiants et Parcours ;
- liens morts et fichiers orphelins ;
- notions de la cartographie sans destination ;
- briques et contrats Praxis inexistants ;
- rubriques obligatoires ;
- processus, schémas, références de la cartographie et vues Canvas périmées ;
- vocabulaire explicitement proscrit ;
- tests et dépendances entre briques Praxis.

Les contrats, états, fragments et sorties assemblées se vérifient avec :

```bash
python generator/tools/validate_lessons.py
python generator/tools/assemble_lesson.py --verifier
```

Les Canvas se régénèrent et se vérifient avec :

```bash
python generator/tools/canvas.py
python generator/tools/canvas.py --verifier
```
