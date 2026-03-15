---
title: IRC
description: Connectez OpenClaw aux canaux IRC et aux messages directs.
summary: "Configuration du plugin IRC, contrôles d'accès et dépannage"
read_when:
  - You want to connect OpenClaw to IRC channels or DMs
  - You are configuring IRC allowlists, group policy, or mention gating
---

Utilisez IRC quand vous voulez OpenClaw dans les canaux classiques (`#room`) et les messages directs.
IRC est fourni en tant que plugin d'extension, mais il est configuré dans la config principale sous `channels.irc`.

## Démarrage rapide

1. Activez la config IRC dans `~/.openclaw/openclaw.json`.
2. Définissez au minimum :

```json
{
  "channels": {
    "irc": {
      "enabled": true,
      "host": "irc.libera.chat",
      "port": 6697,
      "tls": true,
      "nick": "openclaw-bot",
      "channels": ["#openclaw"]
    }
  }
}
```

3. Démarrez/redémarrez la passerelle :

```bash
openclaw gateway run
```

## Paramètres de sécurité par défaut

- `channels.irc.dmPolicy` par défaut à `"pairing"`.
- `channels.irc.groupPolicy` par défaut à `"allowlist"`.
- Avec `groupPolicy="allowlist"`, définissez `channels.irc.groups` pour spécifier les canaux autorisés.
- Utilisez TLS (`channels.irc.tls=true`) sauf si vous acceptez intentionnellement le transport en texte clair.

## Contrôle d'accès

Il y a deux « portes » distinctes pour les canaux IRC :

1. **Accès au canal** (`groupPolicy` + `groups`) : si le bot accepte les messages d'un canal ou non.
2. **Accès de l'expéditeur** (`groupAllowFrom` / par canal `groups["#channel"].allowFrom`) : qui est autorisé à déclencher le bot dans ce canal.

Clés de configuration :

- Liste blanche DM (accès expéditeur DM) : `channels.irc.allowFrom`
- Liste blanche expéditeur groupe (accès expéditeur canal) : `channels.irc.groupAllowFrom`
- Contrôles par canal (canal + expéditeur + règles de mention) : `channels.irc.groups["#channel"]`
- `channels.irc.groupPolicy="open"` autorise les canaux non configurés (**toujours contrôlés par mention par défaut**)

Les entrées de liste blanche doivent utiliser des identités d'expéditeur stables (`nick!user@host`).
La correspondance de nick nu est mutable et n'est activée que quand `channels.irc.dangerouslyAllowNameMatching: true`.

### Piège courant : `allowFrom` est pour les DM, pas les canaux

Si vous voyez des logs comme :

- `irc: drop group sender alice!ident@host (policy=allowlist)`

…cela signifie que l'expéditeur n'était pas autorisé pour les messages **groupe/canal**. Corrigez-le en :

- définissant `channels.irc.groupAllowFrom` (global pour tous les canaux), ou
- définissant les listes blanches d'expéditeur par canal : `channels.irc.groups["#channel"].allowFrom`

Exemple (autoriser n'importe qui dans `#tuirc-dev` à parler au bot) :

```json5
{
  channels: {
    irc: {
      groupPolicy: "allowlist",
      groups: {
        "#tuirc-dev": { allowFrom: ["*"] },
      },
    },
  },
}
```

## Déclenchement de réponse (mentions)

Même si un canal est autorisé (via `groupPolicy` + `groups`) et l'expéditeur est autorisé, OpenClaw utilise par défaut le **contrôle par mention** dans les contextes de groupe.

Cela signifie que vous pouvez voir des logs comme `drop channel … (missing-mention)` sauf si le message inclut un motif de mention qui correspond au bot.

Pour faire répondre le bot dans un canal IRC **sans avoir besoin d'une mention**, désactivez le contrôle par mention pour ce canal :

```json5
{
  channels: {
    irc: {
      groupPolicy: "allowlist",
      groups: {
        "#tuirc-dev": {
          requireMention: false,
          allowFrom: ["*"],
        },
      },
    },
  },
}
```

Ou pour autoriser **tous** les canaux IRC (pas de liste blanche par canal) et toujours répondre sans mentions :

```json5
{
  channels: {
    irc: {
      groupPolicy: "open",
      groups: {
        "*": { requireMention: false, allowFrom: ["*"] },
      },
    },
  },
}
```

## Note de sécurité (recommandée pour les canaux publics)

Si vous autorisez `allowFrom: ["*"]` dans un canal public, n'importe qui peut inviter le bot.
Pour réduire le risque, limitez les outils pour ce canal.

### Mêmes outils pour tout le monde dans le canal

```json5
{
  channels: {
    irc: {
      groups: {
        "#tuirc-dev": {
          allowFrom: ["*"],
          tools: {
            deny: ["group:runtime", "group:fs", "gateway", "nodes", "cron", "browser"],
          },
        },
      },
    },
  },
}
```

### Outils différents par expéditeur (le propriétaire a plus de pouvoir)

Utilisez `toolsBySender` pour appliquer une politique plus stricte à `"*"` et une plus souple à votre nick :

```json5
{
  channels: {
    irc: {
      groups: {
        "#tuirc-dev": {
          allowFrom: ["*"],
          toolsBySender: {
            "*": {
              deny: ["group:runtime", "group:fs", "gateway", "nodes", "cron", "browser"],
            },
            "id:eigen": {
              deny: ["gateway", "nodes", "cron"],
            },
          },
        },
      },
    },
  },
}
```

Notes :

- Les clés `toolsBySender` doivent utiliser `id:` pour les valeurs d'identité d'expéditeur IRC :
  `id:eigen` ou `id:eigen!~eigen@174.127.248.171` pour une correspondance plus forte.
- Les clés non préfixées héritées sont toujours acceptées et correspondent comme `id:` uniquement.
- La première politique d'expéditeur correspondante gagne ; `"*"` est le fallback générique.

Pour plus d'informations sur l'accès au groupe par rapport au contrôle par mention (et comment ils interagissent), voir : [/channels/groups](/fr/channels/groups).

## NickServ

Pour vous identifier avec NickServ après la connexion :

```json
{
  "channels": {
    "irc": {
      "nickserv": {
        "enabled": true,
        "service": "NickServ",
        "password": "your-nickserv-password"
      }
    }
  }
}
```

Enregistrement optionnel unique à la connexion :

```json
{
  "channels": {
    "irc": {
      "nickserv": {
        "register": true,
        "registerEmail": "bot@example.com"
      }
    }
  }
}
```

Désactivez `register` après l'enregistrement du nick pour éviter les tentatives REGISTER répétées.

## Variables d'environnement

Le compte par défaut supporte :

- `IRC_HOST`
- `IRC_PORT`
- `IRC_TLS`
- `IRC_NICK`
- `IRC_USERNAME`
- `IRC_REALNAME`
- `IRC_PASSWORD`
- `IRC_CHANNELS` (séparées par des virgules)
- `IRC_NICKSERV_PASSWORD`
- `IRC_NICKSERV_REGISTER_EMAIL`

## Dépannage

- Si le bot se connecte mais ne répond jamais dans les canaux, vérifiez `channels.irc.groups` **et** si le contrôle par mention supprime les messages (`missing-mention`). Si vous voulez qu'il réponde sans pings, définissez `requireMention:false` pour le canal.
- Si la connexion échoue, vérifiez la disponibilité du nick et le mot de passe du serveur.
- Si TLS échoue sur un réseau personnalisé, vérifiez l'hôte/port et la configuration du certificat.
