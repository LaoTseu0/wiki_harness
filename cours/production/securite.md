# 6.2 Sécurité

> **Module 6 — 06-production** · [sommaire](../../sommaire.md) ·
> [roadmap](../../roadmap.md)
> **Statut** : ⚪ à venir · **Passage** : transverse, démarre avec le
> module 2
> **Dernière mise à jour** : 21 juillet 2026

## Vue d'ensemble

Connaître les attaques par cœur, les mener soi-même, documenter les
défenses — en vocabulaire métier. Trois leçons : le référentiel (OWASP
Top 10 LLM), la pratique offensive (tests adversariaux sur son propre
système), et la synthèse défensive (le threat model de Jarvis, en
termes qu'un recruteur comprend).

## Contenu

- [ ] **[6.2.1 OWASP Top 10 LLM](6.2.1-owasp-top-10-llm/6.2.1-owasp-top-10-llm.md)**
      — lire et savoir restituer
- [ ] **[6.2.2 Tests adversariaux](6.2.2-tests-adversariaux/6.2.2-tests-adversariaux.md)**
      — attaquer son RAG/agent, documenter les défenses
- [ ] **[6.2.3 Threat model Jarvis](6.2.3-threat-model-jarvis/6.2.3-threat-model-jarvis.md)**
      — la page threat model en vocabulaire métier

## Synthèse

La sécurité du parcours n'est pas un module isolé mais la
**capitalisation** de ce qui est déjà en place : le confinement du
module 3, la lecture seule du module 5, l'injection éprouvée en
[5.3.1](../../05-homelab-mcp/5.3-securite/5.3.1-prompt-injection-indirecte/5.3.1-prompt-injection-indirecte.md).
OWASP donne le vocabulaire, les tests adversariaux donnent les preuves,
le threat model donne le récit. **Auto-contrôle** : savoir répondre à
« quels risques pour un agent avec accès fichiers ? » (question n°5) en
citant OWASP ET sa propre démo.

## Références

- [Roadmap couche T](../../roadmap.md) — sécurité et éthique
- OWASP GenAI, Simon Willison ([roadmap §7](../../roadmap.md))
