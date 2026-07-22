# 3.1.2 Conteneur et moindre privilège

> **Leçon de la section [3.1 Garde-fous et sécurité d'abord](../3.1-garde-fous-et-securite.md)**
> · [sommaire](../../../sommaire.md) · [roadmap](../../../roadmap.md)
> **Statut** : ⚪ à venir
> **Dernière mise à jour** : 21 juillet 2026

## L'essentiel

Le hook décide, le conteneur **borne** : même si l'agent (ou une
injection) trouve un chemin que le hook ne voit pas, le processus ne
*peut* physiquement pas sortir de son périmètre. Moindre privilège
appliqué à l'agent : n'accorder que ce que la tâche exige — et
« aucun accès aux partages famille » est la ligne rouge du homelab.

## Le savoir

- **Le principe** : dimensionner les droits sur la **tâche**, pas sur
  la commodité. L'agent Jarvis lit sa doc, écrit son workspace, parle
  à HA et à Ollama — rien d'autre n'existe pour lui.
- **La traduction docker, poste par poste** :
  - **filesystem** : volumes explicites (workspace RW, doc RO), rootfs
    en lecture seule si possible (`--read-only` + tmpfs), **jamais** de
    montage des partages famille — l'absence de montage est la seule
    garantie absolue ;
  - **utilisateur** : non-root (`user:`), pas de `--privileged`,
    `cap_drop: [ALL]` puis réouverture au besoin ;
  - **réseau** : réseau docker interne, egress limité aux endpoints
    nécessaires (HA, Ollama) — un agent qui ne peut pas joindre
    l'extérieur ne peut pas exfiltrer
    ([6.2.3](../../../06-production/6.2-securite/6.2.3-threat-model-jarvis/6.2.3-threat-model-jarvis.md)) ;
  - **ressources** : limites CPU/mémoire — un agent en boucle ne
    couche pas la machine.
- **Pourquoi les deux couches** ([3.1.1](../3.1.1-hook-tool-call/3.1.1-hook-tool-call.md) +
  celle-ci) : le hook est fin mais logiciel (bug, cas non prévu) ; le
  conteneur est grossier mais physique. La défense en profondeur = le
  hook rend l'abus *improbable*, le conteneur le rend *impossible à
  l'échelle du système*.
- **Le jeton, même logique** : le token HA de la
  [3.2.1](../../3.2-outils-et-memoire/3.2.1-outil-home-assistant/3.2.1-outil-home-assistant.md)
  sera à périmètre limité — le moindre privilège s'applique aux
  credentials comme aux montages.

## En pratique

`docker-compose.yml` de l'agent : user non-root, cap_drop ALL, volumes
RO/RW explicites, réseau interne, limites — et le test d'évasion :
depuis le conteneur, tenter de lire un chemin famille et de joindre un
domaine externe ; les deux doivent échouer.

## Pièges connus

- Monter « temporairement » un volume large pour déboguer : le
  temporaire devient permanent — déboguer en copiant *dans* le
  périmètre, jamais en l'élargissant.
- Le réseau par défaut de docker : sortie internet complète — le
  moindre privilège réseau se déclare, il n'est pas le défaut.
- Confondre conteneur et sandbox parfaite : c'est de l'isolation de
  namespace, pas une VM — d'où l'intérêt de garder *aussi* le hook et
  de ne pas donner root.

## Question d'entretien

> « Votre agent est compromis par une injection : quel est le rayon des
> dégâts ? »
> La bonne réponse énumère le périmètre concret : son workspace, ses
> deux endpoints autorisés, son token HA limité — rien d'autre, par
> construction (pas de montage, pas d'egress, pas de privilège). Si on
> ne sait pas répondre à cette question, le confinement n'existe pas.

## Références

- [securite.md](../../../../homelab/architecture/securite.md) — la
  politique homelab
- Doc docker : user, cap_drop, read_only, réseaux internes
