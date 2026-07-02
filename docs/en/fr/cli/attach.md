---
summary: "Référence CLI pour `openclaw attach` (lancer Claude Code avec une subvention Gateway MCP limitée)"
read_when:
  - Vous voulez que Claude Code utilise les outils OpenClaw Gateway MCP
  - Vous avez besoin d'une subvention MCP temporaire liée à une session pour un harnais externe
title: "CLI Attach"
---

`openclaw attach` lance Claude Code avec une configuration MCP temporaire stricte liée
à une session Gateway.

```sh
openclaw attach
openclaw attach --session agent:main:telegram:123 --ttl 600000
openclaw attach --print-config
```

Options :

- `--session <key>` lie la subvention à une session Gateway. Par défaut, la session principale.
- `--ttl <ms>` demande une TTL de subvention positive en millisecondes. La Gateway applique son propre plafond.
- `--bin <path>` sélectionne le binaire Claude Code. Par défaut `claude`.
- `--print-config` écrit le `.mcp.json` temporaire, affiche la commande de lancement et l'env, et laisse la subvention active jusqu'à l'expiration de la TTL.

Le jeton porteur est transmis via des variables d'environnement, pas argv. OpenClaw
lance Claude Code avec `--strict-mcp-config --mcp-config <path>` afin que les serveurs
MCP Claude ambiants ne rejoignent pas la session attachée. Les lancements normaux révoquent
la subvention à la fermeture du processus Claude Code.

Voir aussi : [Gateway CLI](/fr/cli/gateway), [MCP CLI](/fr/cli/mcp), et [ACP CLI](/fr/cli/acp).
