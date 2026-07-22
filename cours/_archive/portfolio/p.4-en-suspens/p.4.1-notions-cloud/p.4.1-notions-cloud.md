# P.4.1 Notions cloud

> **Leçon de la section [P.4 En suspens](../p.4-en-suspens.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ✅ arbitré le 21 juillet 2026
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Le seul vrai **angle mort** d'un homelab local-only : le cloud. Décision
du 21 juillet 2026 — version minimale, sans en faire un chantier : un
backend commutable local/cloud (déjà de l'architecture utile) + savoir
*situer* les offres managées. Ni certification, ni migration, ni dette
de temps.

## Le savoir

- **Le problème** : les offres demandent AWS Bedrock / Azure OpenAI /
  Vertex AI (~60 %, [roadmap §10.1](../../../roadmap.md)) ; un profil
  100 % local a là son unique lacune assumée.
- **L'arbitrage retenu** (minimal, à fort levier) :
  1. **backend commutable local/cloud**
     ([2.4.2](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.2-backend-commutable/2.4.2-backend-commutable.md)) :
     l'abstraction provider bascule la génération vers une API cloud
     par config — ce n'est pas une concession au cloud, c'est de
     l'architecture (réversibilité, la réponse d'entretien
     souveraineté ↔ pointe) ;
  2. **situer les offres managées** : ce que sont Bedrock (catalogue
     multi-modèles AWS), Azure OpenAI (GPT sur Azure, conformité
     entreprise), Vertex AI (Google) — souvent API OpenAI-compatibles
     ([couche 4](../../../roadmap.md)), argument RGPD/région à
     connaître ;
  3. **optionnel** : un petit déploiement d'un module sur un free tier,
     *sans en faire un chantier*.
- **Pourquoi minimal** : le métier visé est AI Engineer, pas Cloud
  Engineer ; savoir *situer* et *basculer* couvre 90 % du besoin
  d'entretien, le reste s'apprend sur le poste. Sur-investir le cloud
  détournerait du différenciateur (le local maîtrisé).
- **La trace de décision** : arbitré et daté (21 juillet 2026) dans la
  [roadmap §10.4](../../../roadmap.md) et le
  [sommaire P.4](../../../sommaire.md) — cette leçon en est la version
  développée.

## En pratique

Rien de neuf à construire au-delà du backend commutable du module 2 ;
une page de veille situant Bedrock/Azure/Vertex (définition, quand,
argument souveraineté), et éventuellement une démo free-tier si
l'occasion se présente — sans y consacrer un module.

## Pièges connus

- Sur-investir le cloud : transformer un angle mort mineur en chantier
  majeur déséquilibre le parcours — minimal et daté.
- Le laisser vraiment vide : « je ne connais pas le cloud » ferme des
  portes ; savoir situer + basculer les rouvre à faible coût.
- Confondre situer et maîtriser : l'honnêteté (« je sais situer et
  basculer, je n'ai pas opéré en prod ») vaut mieux qu'un bluff
  démontable.

## Question d'entretien

> « Votre profil est très local — et le cloud ? »
> Angle mort assumé et traité au minimum utile : backend commutable
> local/cloud (architecture de réversibilité), et je sais situer
> Bedrock/Azure OpenAI/Vertex et l'argument souveraineté — le métier
> visé est AI Engineer, le cloud s'opère sur le poste.

## Références

- [2.4.2 Backend commutable](../../../02-homelab-rag/2.4-service-et-craftsmanship/2.4.2-backend-commutable/2.4.2-backend-commutable.md)
  — la réalisation concrète
- [Roadmap §10.4](../../../roadmap.md) — l'arbitrage daté
