---
read_when:
  - 设置基于 ACP 的 IDE 集成
  - 调试到 Gateway 网关的 ACP 会话路由
summary: 运行用于 IDE 集成的 ACP 桥接器
title: acp
x-i18n:
  generated_at: "2026-02-03T07:44:38Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0c09844297da250bc1a558423e7e534d6b6be9045de12d797c07ecd64a0c63ed
  source_path: cli/acp.md
  workflow: 15
---

# acp

Exécutez un pont ACP (Agent Client Protocol) qui communique avec la passerelle OpenClaw Gateway.

Cette commande communique avec l'IDE en utilisant le protocole ACP via stdio et transfère les invites à la passerelle Gateway via WebSocket. Elle mappe les sessions ACP aux clés de session Gateway.

## Utilisation

```bash
openclaw acp

# Remote Gateway
openclaw acp --url wss://gateway-host:18789 --token <token>

# Attach to an existing session key
openclaw acp --session agent:main:main

# Attach by label (must already exist)
openclaw acp --session-label "support inbox"

# Reset the session key before the first prompt
openclaw acp --session agent:main:main --reset-session
```

## Client ACP (Débogage)

Utilisez le client ACP intégré pour vérifier l'intégrité de l'installation du pont sans IDE.
Il démarre le pont ACP et vous permet d'entrer des invites de manière interactive.

```bash
openclaw acp client

# Point the spawned bridge at a remote Gateway
openclaw acp client --server-args --url wss://gateway-host:18789 --token <token>

# Override the server command (default: openclaw)
openclaw acp client --server "node" --server-args openclaw.mjs acp --url ws://127.0.0.1:19001
```

## Comment utiliser

Utilisez ACP lorsqu'un IDE (ou un autre client) utilise le protocole Agent Client Protocol et que vous souhaitez qu'il pilote une session de passerelle OpenClaw Gateway.

1. Assurez-vous que la passerelle Gateway est en cours d'exécution (localement ou à distance).
2. Configurez la cible de la passerelle Gateway (configuration ou drapeaux).
3. Configurez votre IDE pour exécuter `openclaw acp` via stdio.

Exemple de configuration (persistant) :

```bash
openclaw config set gateway.remote.url wss://gateway-host:18789
openclaw config set gateway.remote.token <token>
```

Exemple d'exécution directe (sans écrire dans la configuration) :

```bash
openclaw acp --url wss://gateway-host:18789 --token <token>
```

## Sélection d'agent

ACP ne sélectionne pas directement d'agent. Il achemine via la clé de session Gateway.

Utilisez une clé de session avec portée d'agent pour cibler un agent spécifique :

```bash
openclaw acp --session agent:main:main
openclaw acp --session agent:design:main
openclaw acp --session agent:qa:bug-123
```

Chaque session ACP mappe à une seule clé de session Gateway. Un agent peut avoir plusieurs sessions ; sauf si vous remplacez la clé ou l'étiquette, ACP utilise par défaut une session isolée `acp:<uuid>`.

## Configuration de l'éditeur Zed

Ajoutez un agent ACP personnalisé dans `~/.config/zed/settings.json` (ou utilisez l'interface de paramètres de Zed) :

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": ["acp"],
      "env": {}
    }
  }
}
```

Pour cibler une passerelle Gateway ou un agent spécifique :

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": [
        "acp",
        "--url",
        "wss://gateway-host:18789",
        "--token",
        "<token>",
        "--session",
        "agent:design:main"
      ],
      "env": {}
    }
  }
}
```

Dans Zed, ouvrez le panneau Agent et sélectionnez « OpenClaw ACP » pour démarrer une session.

## Mappage de session

Par défaut, une session ACP reçoit une clé de session Gateway isolée avec le préfixe `acp:`.
Pour réutiliser une session connue, transmettez la clé de session ou l'étiquette :

- `--session <key>` : Utilisez une clé de session Gateway spécifique.
- `--session-label <label>` : Résolvez une session existante par étiquette.
- `--reset-session` : Générez un nouvel ID de session pour cette clé (même clé, nouvel historique de conversation).

Si votre client ACP prend en charge les métadonnées, vous pouvez remplacer par session :

```json
{
  "_meta": {
    "sessionKey": "agent:main:main",
    "sessionLabel": "support inbox",
    "resetSession": true
  }
}
```

En savoir plus sur les clés de session dans [/concepts/session](/concepts/session).

## Options

- `--url <url>` : URL WebSocket de la passerelle Gateway (par défaut gateway.remote.url après configuration).
- `--token <token>` : Jeton d'authentification de la passerelle Gateway.
- `--password <password>` : Mot de passe d'authentification de la passerelle Gateway.
- `--session <key>` : Clé de session par défaut.
- `--session-label <label>` : Étiquette de session par défaut à résoudre.
- `--require-existing` : Échouez si la clé/étiquette de session n'existe pas.
- `--reset-session` : Réinitialisez la clé de session avant la première utilisation.
- `--no-prefix-cwd` : N'ajoutez pas le préfixe du répertoire de travail aux invites.
- `--verbose, -v` : Sortie des journaux détaillés vers stderr.

### Options `acp client`

- `--cwd <dir>` : Répertoire de travail pour la session ACP.
- `--server <command>` : Commande du serveur ACP (par défaut : `openclaw`).
- `--server-args <args...>` : Arguments supplémentaires à transmettre au serveur ACP.
- `--server-verbose` : Activez les journaux détaillés du serveur ACP.
- `--verbose, -v` : Journaux client détaillés.
