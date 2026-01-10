# 6.1 Observabilité

> **Module 6 — 06-production** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md)
> **Statut** : ⚪ à venir · **Passage** : transverse, démarre avec le
> module 2
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Tracer chaque appel — prompt, réponse, latence, tokens, **coût** —
parce qu'un système qu'on ne voit pas ne se débogue pas et ne se paye
pas en conscience. Trois leçons dans l'ordre d'installation : l'outil
(Langfuse self-hosté), les traces (modules 2 et 3 instrumentés), la
comptabilité (le coût en continu, même en local).

## Contenu

- [ ] **[6.1.1 Langfuse self-hosté](6.1.1-langfuse-self-hoste/6.1.1-langfuse-self-hoste.md)**
      — un conteneur de plus au homelab
- [ ] **[6.1.2 Tracer les appels](6.1.2-tracer-les-appels/6.1.2-tracer-les-appels.md)**
      — modules 2 et 3 : latence, tokens, spans par maillon
- [ ] **[6.1.3 Suivi des coûts](6.1.3-suivi-des-couts/6.1.3-suivi-des-couts.md)**
      — coût équivalent API pour le local, en continu

## Synthèse

L'observabilité est ce qui transforme les intuitions du parcours en
faits : « le RAG est lent » devient « le retrieval prend 40 ms, la
génération 2,3 s », et « le local est gratuit » devient un coût
équivalent API chiffré. Les traces sont aussi le prolongement naturel
des [evals](../../02-homelab-rag/2.1-v0.0.1-rag-a-la-main/2.1.7-evals/2.1.7-evals.md) :
les evals notent des sorties, les traces expliquent *comment* elles ont
été produites. **Auto-contrôle** : depuis une réponse ratée en
production, savoir remonter en un clic à ses chunks, son prompt et ses
latences.

## Références

- [Roadmap couche T](../../roadmap.md) — observabilité, le
  différenciateur senior
