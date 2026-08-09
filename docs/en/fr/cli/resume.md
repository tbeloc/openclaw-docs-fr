---
summary: "Référence CLI pour attacher la TUI à une session Gateway récente"
read_when:
  - You want to continue an existing Gateway session in the terminal
  - You want to find a recent session by key, display name, or label
  - You connect the TUI to a remote Gateway
title: "Resume"
---

# `openclaw resume`

Attachez l'interface utilisateur du terminal à une session Gateway existante. La session reste sur
la Gateway ; `resume` la sélectionne et ouvre la [TUI](/fr/cli/tui) existante.

```bash
openclaw resume
openclaw resume <query>
```

Sans requête, OpenClaw affiche jusqu'à 50 sessions actives au cours des sept
derniers jours. Avec une requête, une clé de session exacte gagne ; sinon OpenClaw nécessite une
sous-chaîne unique ou une correspondance floue sur les clés de session, les noms d'affichage et les étiquettes.

Le sélecteur omet les lignes `global` nues car elles n'identifient pas un agent
propriétaire. Pour en attacher une, passez une clé complète telle que
`openclaw resume agent:main:global`.

Si une requête est ambiguë, OpenClaw affiche les candidats correspondants et se termine avec
le statut 1. Si aucune session récente ne correspond, il suggère le sélecteur et
[`openclaw sessions`](/fr/cli/sessions), puis se termine avec le statut 1.

## Options

| Flag                         | Default                          | Description                                                         |
| ---------------------------- | -------------------------------- | ------------------------------------------------------------------- |
| `--url <url>`                | `gateway.remote.url` from config | URL WebSocket de la Gateway.                                              |
| `--token <token>`            | (none)                           | Jeton Gateway si requis.                                          |
| `--password <pass>`          | (none)                           | Mot de passe Gateway si requis.                                       |
| `--tls-fingerprint <sha256>` | `gateway.remote.tlsFingerprint`  | Empreinte digitale du certificat TLS attendue pour une Gateway `wss://` épinglée. |

`resume` utilise la même URL Gateway, l'authentification et la résolution TLS que
[`openclaw tui`](/fr/cli/tui). Il ne démarre jamais une Gateway automatiquement. Si la
Gateway configurée est indisponible, démarrez-la ou réparez-la et réexécutez la commande.

`resume` résout les SecretRefs d'authentification Gateway configurés pour l'authentification par jeton/mot de passe
si possible (fournisseurs `env`/`file`/`exec`).

La précédence de la cible Gateway est `--url` explicite, puis `OPENCLAW_GATEWAY_URL`,
puis `gateway.remote.url` quand `gateway.mode` est `remote`, puis la Gateway
loopback locale. Pour cette Gateway locale, `OPENCLAW_GATEWAY_PORT` prend
la précédence sur le port actif enregistré par une Gateway en cours d'exécution, qui prend
la précédence sur le `gateway.port` configuré ou par défaut.

## Exemples

```bash
# Choose from recent sessions
openclaw resume

# Exact key
openclaw resume agent:main:bugfix

# Unique display-name or label fragment
openclaw resume bugfix

# Remote Gateway override
openclaw resume bugfix --url wss://gateway.example.com --token <token>
```

## Connexes

- [TUI](/fr/cli/tui)
- [Sessions](/fr/cli/sessions)
- [Guide TUI](/fr/web/tui)
