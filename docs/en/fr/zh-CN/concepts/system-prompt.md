---
read_when:
  - Édition du texte des invites système, de la liste des outils ou des sections de temps/pulsation
  - Modification du guidage de l'espace de travail ou du comportement d'injection des Skills
summary: Contenu de l'invite système OpenClaw et mode d'assemblage
title: Invite système
x-i18n:
  generated_at: "2026-02-03T07:46:58Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bef4b2674ba0414ce28fd08a4c3ead0e0ebe989e7df3c88ca8a0b2abfec2a50b
  source_path: concepts/system-prompt.md
  workflow: 15
---

# Invite système

OpenClaw construit une invite système personnalisée pour chaque exécution d'agent. Cette invite est **détenue par OpenClaw** et n'utilise pas l'invite par défaut de pi-coding-agent.

L'invite est assemblée par OpenClaw et injectée dans chaque exécution d'agent.

## Structure

L'invite est conçue de manière compacte, utilisant des sections fixes :

- **Tooling** : liste actuelle des outils + brève description.
- **Safety** : rappel de sécurité court, évitant les comportements de recherche de pouvoir ou de contournement de la surveillance.
- **Skills** (si disponible) : indique au modèle comment charger les instructions Skill à la demande.
- **OpenClaw Self-Update** : comment exécuter `config.apply` et `update.run`.
- **Workspace** : répertoire de travail (`agents.defaults.workspace`).
- **Documentation** : chemin local de la documentation OpenClaw (dépôt ou paquet npm) et quand la consulter.
- **Workspace Files (injected)** : indique que les fichiers de guidage sont inclus ci-dessous.
- **Sandbox** (si activé) : indique l'exécution isolée du sandbox, le chemin du sandbox, et si l'exécution avec privilèges est disponible.
- **Current Date & Time** : heure locale de l'utilisateur, fuseau horaire et format d'heure.
- **Reply Tags** : syntaxe des balises de réponse optionnelles pour les fournisseurs pris en charge.
- **Heartbeats** : invite de pulsation et comportement de confirmation.
- **Runtime** : hôte, système d'exploitation, node, modèle, répertoire racine du dépôt (si détecté), niveau de réflexion (une ligne).
- **Reasoning** : niveau de visibilité actuel + invite de basculement /reasoning.

Les protections de sécurité dans l'invite système sont de nature consultative. Elles guident le comportement du modèle mais n'appliquent pas les politiques. Utilisez les politiques d'outils, l'approbation d'exécution, l'isolation du sandbox et les listes blanches de canaux pour l'application stricte ; les opérateurs peuvent désactiver ces éléments par conception.

## Modes d'invite

OpenClaw peut rendre une invite système plus petite pour les sous-agents. Le runtime définit un `promptMode` pour chaque exécution (pas une configuration orientée utilisateur) :

- `full` (par défaut) : inclut toutes les sections ci-dessus.
- `minimal` : pour les sous-agents ; omet **Skills**, **Memory Recall**, **OpenClaw Self-Update**, **Model Aliases**, **User Identity**, **Reply Tags**, **Messaging**, **Silent Replies** et **Heartbeats**. Tooling, **Safety**, Workspace, Sandbox, Current Date & Time (si connu), Runtime et le contexte injecté restent disponibles.
- `none` : retourne uniquement la ligne d'identité de base.

Lorsque `promptMode=minimal`, le contexte injecté supplémentaire est marqué comme **Subagent Context** plutôt que **Group Chat Context**.

## Injection de guidage de l'espace de travail

Les fichiers de guidage sont élagués puis ajoutés sous **Project Context**, permettant au modèle de voir le contexte d'identité et de configuration sans avoir à les lire explicitement :

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md` (uniquement sur un nouvel espace de travail)

Les fichiers volumineux sont tronqués avec une marque de troncature. La taille maximale de chaque fichier est contrôlée par `agents.defaults.bootstrapMaxChars` (par défaut : 20000). Les fichiers manquants injectent une brève marque de fichier manquant.

Les crochets internes peuvent intercepter cette étape via `agent:bootstrap` pour modifier ou remplacer les fichiers de guidage injectés (par exemple, remplacer `SOUL.md` par un autre rôle).

Pour vérifier combien chaque fichier injecté contribue (brut vs injecté, tronqué, plus la surcharge du schéma d'outils), utilisez `/context list` ou `/context detail`. Voir [Contexte](/concepts/context).

## Gestion du temps

Lorsque le fuseau horaire de l'utilisateur est connu, l'invite système contient une section **Current Date & Time** dédiée. Pour maintenir la stabilité du cache d'invite, elle contient maintenant uniquement le **fuseau horaire** (pas d'horloge dynamique ni de format d'heure).

Utilisez `session_status` lorsque l'agent a besoin de l'heure actuelle ; la carte d'état contient une ligne d'horodatage.

Configuration :

- `agents.defaults.userTimezone`
- `agents.defaults.timeFormat` (`auto` | `12` | `24`)

Voir [Date et heure](/date-time) pour les détails complets du comportement.

## Skills

Lorsque des Skills éligibles existent, OpenClaw injecte une **liste compacte des Skills disponibles** (`formatSkillsForPrompt`), contenant le **chemin du fichier** pour chaque Skill. L'invite indique au modèle d'utiliser `read` pour charger le SKILL.md aux emplacements listés (espace de travail, hébergé ou intégré). Si aucun Skill éligible n'existe, la section Skills est omise.

```
<available_skills>
  <skill>
    <name>...</name>
    <description>...</description>
    <location>...</location>
  </skill>
</available_skills>
```

Cela maintient l'invite de base compacte tout en supportant l'utilisation ciblée des Skills.

## Documentation

Si disponible, l'invite système contient une section **Documentation** pointant vers le répertoire de documentation OpenClaw local (`docs/` dans l'espace de travail du dépôt ou documentation du paquet npm emballée), et notant le miroir public, le dépôt source, le Discord communautaire et ClawHub (https://clawhub.com) pour la découverte de Skills. L'invite indique au modèle de consulter d'abord la documentation locale pour le comportement, les commandes, la configuration ou l'architecture d'OpenClaw, et d'exécuter lui-même `openclaw status` autant que possible (ne demander à l'utilisateur que si l'accès n'est pas possible).
