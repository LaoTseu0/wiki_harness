# Observabilité

> [carte du cours](../carte.md)

## Vue d'ensemble

Tracer chaque appel — prompt, réponse, latence, tokens, **coût** —
parce qu'un système qu'on ne voit pas ne se débogue pas et ne se paye
pas en conscience. Trois leçons dans l'ordre d'installation : l'outil
(Langfuse self-hosté), les traces (modules 2 et 3 instrumentés), la
comptabilité (le coût en continu, même en local).

## Contenu

- **[6.1.1 Langfuse self-hosté](langfuse-self-hoste.md)**
      — un conteneur de plus au homelab
- **[6.1.2 Tracer les appels](tracer-les-appels.md)**
      — modules 2 et 3 : latence, tokens, spans par maillon
- **[6.1.3 Suivi des coûts](suivi-des-couts.md)**
      — coût équivalent API pour le local, en continu

## Synthèse

L'observabilité est ce qui transforme les intuitions du parcours en
faits : « le RAG est lent » devient « le retrieval prend 40 ms, la
génération 2,3 s », et « le local est gratuit » devient un coût
équivalent API chiffré. Les traces sont aussi le prolongement naturel
des [evals](../retrieval/evals.md) :
les evals notent des sorties, les traces expliquent *comment* elles ont
été produites. **Auto-contrôle** : depuis une réponse ratée en
production, savoir remonter en un clic à ses chunks, son prompt et ses
latences.

## Références

- [Roadmap couche T](../_archive/roadmap.md) — observabilité, le
  différenciateur senior
