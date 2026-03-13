# Liaisons ACP persistants pour les canaux Discord et les sujets Telegram

Statut : Brouillon

## Résumé

Introduire des liaisons ACP persistantes qui mappent :

- Les canaux Discord (et les fils existants, si nécessaire), et
- Les sujets de forum Telegram dans les groupes/supergroupes (`chatId:topic:topicId`)

aux sessions ACP de longue durée, avec l'état de liaison stocké dans les entrées `bindings[]` de niveau supérieur utilisant des types de liaison explicites.

Cela rend l'utilisation d'ACP dans les canaux de messagerie à fort trafic prévisible et durable, permettant aux utilisateurs de créer des canaux/sujets dédiés tels que `codex`, `claude-1` ou `claude-myrepo`.

## Pourquoi

Le comportement actuel d'ACP lié aux fils est optimisé pour les flux de travail éphémères des fils Discord. Telegram n'a pas le même modèle de fil ; il a des sujets de forum dans les groupes/supergroupes. Les utilisateurs veulent des « espaces de travail » ACP stables et toujours actifs dans les surfaces de chat, pas seulement des sessions de fil temporaires.

## Objectifs

- Supporter la liaison ACP durable pour :
  - Les canaux/fils Discord
  - Les sujets de forum Telegram (groupes/supergroupes)
- Rendre la source de vérité de liaison pilotée par la configuration.
- Garder `/acp`, `/new`, `/reset`, `/focus` et le comportement de livraison cohérents entre Discord et Telegram.
- Préserver les flux de liaison temporaire existants pour une utilisation ad hoc.

## Non-objectifs

- Refonte complète des internals d'exécution/session ACP.
- Suppression des flux de liaison éphémère existants.
- Expansion à chaque canal dans la première itération.
- Implémentation des sujets de messages directs de canal Telegram (`direct_messages_topic_id`) dans cette phase.
- Implémentation des variantes de sujets de chat privé Telegram dans cette phase.

## Direction UX

### 1) Deux types de liaison

- **Liaison persistante** : sauvegardée dans la configuration, réconciliée au démarrage, destinée aux canaux/sujets « espace de travail nommé ».
- **Liaison temporaire** : runtime uniquement, expire selon la politique d'inactivité/âge maximal.

### 2) Comportement des commandes

- `/acp spawn ... --thread here|auto|off` reste disponible.
- Ajouter des contrôles de cycle de vie de liaison explicites :
  - `/acp bind [session|agent] [--persist]`
  - `/acp unbind [--persist]`
  - `/acp status` inclut si la liaison est `persistent` ou `temporary`.
- Dans les conversations liées, `/new` et `/reset` réinitialisent la session ACP liée sur place et gardent la liaison attachée.

### 3) Identité de conversation

- Utiliser les IDs de conversation canoniques :
  - Discord : ID de canal/fil.
  - Sujet Telegram : `chatId:topic:topicId`.
- Ne jamais clé les liaisons Telegram par ID de sujet nu seul.

## Modèle de configuration (proposé)

Unifier le routage et la configuration de liaison ACP persistante dans `bindings[]` de niveau supérieur avec discriminateur `type` explicite :

```jsonc
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace-main",
        "runtime": { "type": "embedded" },
      },
      {
        "id": "codex",
        "workspace": "~/.openclaw/workspace-codex",
        "runtime": {
          "type": "acp",
          "acp": {
            "agent": "codex",
            "backend": "acpx",
            "mode": "persistent",
            "cwd": "/workspace/repo-a",
          },
        },
      },
      {
        "id": "claude",
        "workspace": "~/.openclaw/workspace-claude",
        "runtime": {
          "type": "acp",
          "acp": {
            "agent": "claude",
            "backend": "acpx",
            "mode": "persistent",
            "cwd": "/workspace/repo-b",
          },
        },
      },
    ],
  },
  "acp": {
    "enabled": true,
    "backend": "acpx",
    "allowedAgents": ["codex", "claude"],
  },
  "bindings": [
    // Liaisons de routage (comportement existant)
    {
      "type": "route",
      "agentId": "main",
      "match": { "channel": "discord", "accountId": "default" },
    },
    {
      "type": "route",
      "agentId": "main",
      "match": { "channel": "telegram", "accountId": "default" },
    },
    // Liaisons de conversation ACP persistantes
    {
      "type": "acp",
      "agentId": "codex",
      "match": {
        "channel": "discord",
        "accountId": "default",
        "peer": { "kind": "channel", "id": "222222222222222222" },
      },
      "acp": {
        "label": "codex-main",
        "mode": "persistent",
        "cwd": "/workspace/repo-a",
        "backend": "acpx",
      },
    },
    {
      "type": "acp",
      "agentId": "claude",
      "match": {
        "channel": "discord",
        "accountId": "default",
        "peer": { "kind": "channel", "id": "333333333333333333" },
      },
      "acp": {
        "label": "claude-repo-b",
        "mode": "persistent",
        "cwd": "/workspace/repo-b",
      },
    },
    {
      "type": "acp",
      "agentId": "codex",
      "match": {
        "channel": "telegram",
        "accountId": "default",
        "peer": { "kind": "group", "id": "-1001234567890:topic:42" },
      },
      "acp": {
        "label": "tg-codex-42",
        "mode": "persistent",
      },
    },
  ],
  "channels": {
    "discord": {
      "guilds": {
        "111111111111111111": {
          "channels": {
            "222222222222222222": {
              "enabled": true,
              "requireMention": false,
            },
            "333333333333333333": {
              "enabled": true,
              "requireMention": false,
            },
          },
        },
      },
    },
    "telegram": {
      "groups": {
        "-1001234567890": {
          "topics": {
            "42": {
              "requireMention": false,
            },
          },
        },
      },
    },
  },
}
```

### Exemple minimal (pas de surcharges ACP par liaison)

```jsonc
{
  "agents": {
    "list": [
      { "id": "main", "default": true, "runtime": { "type": "embedded" } },
      {
        "id": "codex",
        "runtime": {
          "type": "acp",
          "acp": { "agent": "codex", "backend": "acpx", "mode": "persistent" },
        },
      },
      {
        "id": "claude",
        "runtime": {
          "type": "acp",
          "acp": { "agent": "claude", "backend": "acpx", "mode": "persistent" },
        },
      },
    ],
  },
  "acp": { "enabled": true, "backend": "acpx" },
  "bindings": [
    {
      "type": "route",
      "agentId": "main",
      "match": { "channel": "discord", "accountId": "default" },
    },
    {
      "type": "route",
      "agentId": "main",
      "match": { "channel": "telegram", "accountId": "default" },
    },

    {
      "type": "acp",
      "agentId": "codex",
      "match": {
        "channel": "discord",
        "accountId": "default",
        "peer": { "kind": "channel", "id": "222222222222222222" },
      },
    },
    {
      "type": "acp",
      "agentId": "claude",
      "match": {
        "channel": "discord",
        "accountId": "default",
        "peer": { "kind": "channel", "id": "333333333333333333" },
      },
    },
    {
      "type": "acp",
      "agentId": "codex",
      "match": {
        "channel": "telegram",
        "accountId": "default",
        "peer": { "kind": "group", "id": "-1009876543210:topic:5" },
      },
    },
  ],
}
```

Notes :

- `bindings[].type` est explicite :
  - `route` : routage d'agent normal.
  - `acp` : liaison de harnais ACP persistante pour une conversation appariée.
- Pour `type: "acp"`, `match.peer.id` est la clé de conversation canonique :
  - Canal/fil Discord : ID de canal/fil brut.
  - Sujet Telegram : `chatId:topic:topicId`.
- `bindings[].acp.backend` est optionnel. Ordre de secours du backend :
  1. `bindings[].acp.backend`
  2. `agents.list[].runtime.acp.backend`
  3. `acp.backend` global
- `mode`, `cwd` et `label` suivent le même modèle de surcharge (`surcharge de liaison -> défaut d'exécution d'agent -> comportement global/par défaut`).
- Garder `session.threadBindings.*` et `channels.discord.threadBindings.*` existants pour les politiques de liaison temporaire.
- Les entrées persistantes déclarent l'état souhaité ; le runtime réconcilie les sessions/liaisons ACP réelles.
- Une liaison ACP active par nœud de conversation est le modèle prévu.
- Compatibilité rétroactive : `type` manquant est interprété comme `route` pour les entrées héritées.

### Sélection du backend

- L'initialisation de session ACP utilise déjà la sélection de backend configurée lors du spawn (`acp.backend` aujourd'hui).
- Cette proposition étend la logique de spawn/réconciliation pour préférer les surcharges de liaison ACP typées :
  - `bindings[].acp.backend` pour la surcharge locale de conversation.
  - `agents.list[].runtime.acp.backend` pour les défauts par agent.
- Si aucune surcharge n'existe, garder le comportement actuel (défaut `acp.backend`).

## Ajustement architectural dans le système actuel

### Réutiliser les composants existants

- `SessionBindingService` supporte déjà les références de conversation agnostiques du canal.
- Les flux de spawn/bind ACP supportent déjà la liaison via les APIs de service.
- Telegram porte déjà le contexte de sujet/fil via `MessageThreadId` et `chatId`.

### Composants nouveaux/étendus

- **Adaptateur de liaison Telegram** (parallèle à l'adaptateur Discord) :
  - enregistrer l'adaptateur par compte Telegram,
  - résoudre/lister/lier/délier/toucher par ID de conversation canonique.
- **Résolveur/index de liaison typée** :
  - diviser `bindings[]` en vues `route` et `acp`,
  - garder `resolveAgentRoute` sur les liaisons `route` uniquement,
  - résoudre l'intention ACP persistante à partir des liaisons `acp` uniquement.
- **Résolution de liaison entrante pour Telegram** :
  - résoudre la session liée avant la finalisation de route (Discord le fait déjà).
- **Réconciliateur de liaison persistante** :
  - au démarrage : charger les liaisons `type: "acp"` de niveau supérieur configurées, assurer l'existence des sessions ACP, assurer l'existence des liaisons.
  - au changement de configuration : appliquer les deltas en toute sécurité.
- **Modèle de basculement** :
  - aucun secours de liaison ACP local au canal n'est lu,
  - les liaisons ACP persistantes sont sourcées uniquement à partir des entrées `bindings[].type="acp"` de niveau supérieur.

## Livraison par phases

### Phase 1 : Fondation du schéma de liaison typée

- Étendre le schéma de configuration pour supporter le discriminateur `bindings[].type` :
  - `route`,
  - `acp` avec objet de surcharge `acp` optionnel (`mode`, `backend`, `cwd`, `label`).
- Étendre le schéma d'agent avec descripteur d'exécution pour marquer les agents natifs ACP (`agents.list[].runtime.type`).
- Ajouter le fractionnement d'analyseur/indexeur pour les liaisons de route vs ACP.

### Phase 2 : Résolution d'exécution + parité Discord/Telegram

- Résoudre les liaisons ACP persistantes à partir des entrées `type: "acp"` de niveau supérieur pour :
  - Les canaux/fils Discord,
  - Les sujets de forum Telegram (IDs canoniques `chatId:topic:topicId`).
- Implémenter l'adaptateur de liaison Telegram et la parité de surcharge de session liée entrante avec Discord.
- Ne pas inclure les variantes de sujet direct/privé Telegram dans cette phase.

### Phase 3 : Parité des commandes et réinitialisations

- Aligner le comportement de `/acp`, `/new`, `/reset` et `/focus` dans les conversations liées Telegram/Discord.
- Assurer que la liaison survit aux flux de réinitialisation comme configuré.

### Phase 4 : Durcissement

- Meilleure diagnostique (`/acp status`, journaux de réconciliation au démarrage).
- Gestion des conflits et vérifications de santé.

## Garde-fous et politique

- Respecter l'activation ACP et les restrictions de bac à sable exactement comme aujourd'hui.
- Garder le scoping de compte explicite (`accountId`) pour éviter les fuites entre comptes.
- Échouer fermé sur le routage ambigu.
- Garder le comportement de politique de mention/accès explicite par configuration de canal.

## Plan de test

- Unité :
  - normalisation d'ID de conversation (en particulier les IDs de sujet Telegram),
  - chemins de création/mise à jour/suppression du réconciliateur,
  - flux `/acp bind --persist` et unbind.
- Intégration :
  - résolution de sujet Telegram entrant -> session ACP liée,
  - résolution de canal/fil Discord entrant -> précédence de liaison persistante.
