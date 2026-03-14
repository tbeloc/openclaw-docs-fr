---
summary: "Ce que contient l'invite système OpenClaw et comment elle est assemblée"
read_when:
  - Editing system prompt text, tools list, or time/heartbeat sections
  - Changing workspace bootstrap or skills injection behavior
title: "Invite système"
---

# Invite système

OpenClaw construit une invite système personnalisée pour chaque exécution d'agent. L'invite est **propriété d'OpenClaw** et n'utilise pas l'invite par défaut de pi-coding-agent.

L'invite est assemblée par OpenClaw et injectée dans chaque exécution d'agent.

## Structure

L'invite est intentionnellement compacte et utilise des sections fixes :

- **Tooling** : liste d'outils actuelle + descriptions courtes.
- **Safety** : rappel court des garde-fous pour éviter les comportements de recherche de pouvoir ou le contournement de la surveillance.
- **Skills** (si disponibles) : indique au modèle comment charger les instructions de compétences à la demande.
- **OpenClaw Self-Update** : comment exécuter `config.apply` et `update.run`.
- **Workspace** : répertoire de travail (`agents.defaults.workspace`).
- **Documentation** : chemin local vers la documentation OpenClaw (repo ou package npm) et quand la consulter.
- **Workspace Files (injectés)** : indique que les fichiers d'amorçage sont inclus ci-dessous.
- **Sandbox** (si activé) : indique l'exécution en sandbox, les chemins sandbox et si l'exécution élevée est disponible.
- **Current Date & Time** : heure locale de l'utilisateur, fuseau horaire et format d'heure.
- **Reply Tags** : syntaxe de balise de réponse optionnelle pour les fournisseurs supportés.
- **Heartbeats** : invite de battement cardiaque et comportement d'accusé de réception.
- **Runtime** : hôte, OS, node, modèle, racine du repo (si détecté), niveau de réflexion (une ligne).
- **Reasoning** : niveau de visibilité actuel + indice de basculement /reasoning.

Les garde-fous de sécurité dans l'invite système sont consultatifs. Ils guident le comportement du modèle mais n'appliquent pas la politique. Utilisez la politique d'outils, les approbations d'exécution, le sandboxing et les listes blanches de canaux pour l'application stricte ; les opérateurs peuvent les désactiver par conception.

## Modes d'invite

OpenClaw peut afficher des invites système plus petites pour les sous-agents. Le runtime définit un
`promptMode` pour chaque exécution (pas une configuration accessible à l'utilisateur) :

- `full` (par défaut) : inclut toutes les sections ci-dessus.
- `minimal` : utilisé pour les sous-agents ; omet **Skills**, **Memory Recall**, **OpenClaw
  Self-Update**, **Model Aliases**, **User Identity**, **Reply Tags**,
  **Messaging**, **Silent Replies** et **Heartbeats**. Tooling, **Safety**,
  Workspace, Sandbox, Current Date & Time (si connu), Runtime et contexte injecté
  restent disponibles.
- `none` : retourne uniquement la ligne d'identité de base.

Quand `promptMode=minimal`, les invites injectées supplémentaires sont étiquetées **Subagent
Context** au lieu de **Group Chat Context**.

## Injection d'amorçage du workspace

Les fichiers d'amorçage sont réduits et ajoutés sous **Project Context** afin que le modèle voie le contexte d'identité et de profil sans avoir besoin de lectures explicites :

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `IDENTITY.md`
- `USER.md`
- `HEARTBEAT.md`
- `BOOTSTRAP.md` (uniquement sur les nouveaux workspaces)
- `MEMORY.md` si présent, sinon `memory.md` comme alternative en minuscules

Tous ces fichiers sont **injectés dans la fenêtre de contexte** à chaque tour, ce qui
signifie qu'ils consomment des tokens. Gardez-les concis — en particulier `MEMORY.md`, qui peut
croître au fil du temps et entraîner une utilisation de contexte inopinément élevée et un compactage plus fréquent.

> **Note :** les fichiers quotidiens `memory/*.md` ne sont **pas** injectés automatiquement. Ils
> sont accessibles à la demande via les outils `memory_search` et `memory_get`, donc ils
> ne comptent pas contre la fenêtre de contexte à moins que le modèle ne les lise explicitement.

Les fichiers volumineux sont tronqués avec un marqueur. La taille maximale par fichier est contrôlée par
`agents.defaults.bootstrapMaxChars` (par défaut : 20000). Le contenu d'amorçage injecté total
entre les fichiers est limité par `agents.defaults.bootstrapTotalMaxChars`
(par défaut : 150000). Les fichiers manquants injectent un marqueur court de fichier manquant. Quand la troncature
se produit, OpenClaw peut injecter un bloc d'avertissement dans Project Context ; contrôlez cela avec
`agents.defaults.bootstrapPromptTruncationWarning` (`off`, `once`, `always`;
par défaut : `once`).

Les sessions de sous-agent injectent uniquement `AGENTS.md` et `TOOLS.md` (les autres fichiers d'amorçage
sont filtrés pour garder le contexte du sous-agent petit).

Les hooks internes peuvent intercepter cette étape via `agent:bootstrap` pour muter ou remplacer
les fichiers d'amorçage injectés (par exemple en échangeant `SOUL.md` pour une persona alternative).

Pour inspecter la contribution de chaque fichier injecté (brut vs injecté, troncature, plus surcharge de schéma d'outil), utilisez `/context list` ou `/context detail`. Voir [Context](/concepts/context).

## Gestion du temps

L'invite système inclut une section **Current Date & Time** dédiée quand le
fuseau horaire de l'utilisateur est connu. Pour maintenir la stabilité du cache d'invite, elle inclut maintenant
uniquement le **fuseau horaire** (pas d'horloge dynamique ni de format d'heure).

Utilisez `session_status` quand l'agent a besoin de l'heure actuelle ; la carte de statut
inclut une ligne d'horodatage.

Configurez avec :

- `agents.defaults.userTimezone`
- `agents.defaults.timeFormat` (`auto` | `12` | `24`)

Voir [Date & Time](/date-time) pour les détails complets du comportement.

## Skills

Quand des compétences éligibles existent, OpenClaw injecte une liste compacte de **compétences disponibles**
(`formatSkillsForPrompt`) qui inclut le **chemin de fichier** pour chaque compétence. L'invite
instruit le modèle à utiliser `read` pour charger le SKILL.md à l'emplacement indiqué (workspace, géré ou fourni). Si aucune compétence n'est éligible, la
section Skills est omise.

```
<available_skills>
  <skill>
    <name>...</name>
    <description>...</description>
    <location>...</location>
  </skill>
</available_skills>
```

Cela garde l'invite de base petite tout en permettant l'utilisation ciblée de compétences.

## Documentation

Quand disponible, l'invite système inclut une section **Documentation** qui pointe vers le
répertoire de documentation OpenClaw local (soit `docs/` dans le workspace du repo soit la
documentation du package npm fournie) et note également le miroir public, le repo source, le Discord communautaire et
ClawHub ([https://clawhub.com](https://clawhub.com)) pour la découverte de compétences. L'invite instruit le modèle à consulter d'abord la documentation locale
pour le comportement, les commandes, la configuration ou l'architecture d'OpenClaw, et à exécuter
`openclaw status` lui-même quand possible (ne demandant à l'utilisateur que quand il n'y a pas accès).
