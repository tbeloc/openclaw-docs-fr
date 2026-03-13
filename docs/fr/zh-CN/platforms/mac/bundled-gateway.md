---
read_when:
  - 打包 OpenClaw.app
  - 调试 macOS Gateway 网关 launchd 服务
  - 为 macOS 安装 Gateway 网关 CLI
summary: macOS 上的 Gateway 网关运行时（外部 launchd 服务）
title: macOS 上的 Gateway 网关
x-i18n:
  generated_at: "2026-02-03T07:52:30Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4a3e963d13060b123538005439213e786e76127b370a6c834d85a369e4626fe5
  source_path: platforms/mac/bundled-gateway.md
  workflow: 15
---

# Gateway sur macOS (launchd externe)

OpenClaw.app n'inclut plus Node/Bun ou le runtime Gateway. L'application macOS s'attend à avoir un CLI `openclaw` **externe** installé, ne lancera pas Gateway en tant que sous-processus, mais gérera plutôt un service launchd par utilisateur pour maintenir Gateway en exécution (ou se connectera à un Gateway local existant s'il est déjà en cours d'exécution).

## Installation du CLI (obligatoire pour le mode local)

Vous devez avoir Node 22+ installé sur votre Mac, puis installer `openclaw` globalement :

```bash
npm install -g openclaw@<version>
```

Le bouton **Installer CLI** de l'application macOS exécute le même processus via npm/pnpm (l'utilisation de bun comme runtime Gateway n'est pas recommandée).

## Launchd (Gateway en tant que LaunchAgent)

Étiquette :

- `bot.molt.gateway` (ou `bot.molt.<profile>` ; les anciens `com.openclaw.*` peuvent toujours exister)

Emplacement du Plist (par utilisateur) :

- `~/Library/LaunchAgents/bot.molt.gateway.plist`
  (ou `~/Library/LaunchAgents/bot.molt.<profile>.plist`)

Gestionnaire :

- L'application macOS a les permissions pour installer/mettre à jour le LaunchAgent en mode local.
- Le CLI peut également l'installer : `openclaw gateway install`.

Comportement :

- "OpenClaw Active" active/désactive le LaunchAgent.
- La fermeture de l'application **n'arrêtera pas** Gateway (launchd le maintient en vie).
- Si Gateway s'exécute déjà sur le port configuré, l'application s'y connectera au lieu de lancer une nouvelle instance.

Journaux :

- stdout/err de launchd : `/tmp/openclaw/openclaw-gateway.log`

## Compatibilité des versions

L'application macOS vérifie que la version de Gateway correspond à sa propre version. Si elle n'est pas compatible, mettez à jour le CLI global pour qu'il corresponde à la version de l'application.

## Test de fumée

```bash
openclaw --version

OPENCLAW_SKIP_CHANNELS=1 \
OPENCLAW_SKIP_CANVAS_HOST=1 \
openclaw gateway --port 18999 --bind loopback
```

Ensuite :

```bash
openclaw gateway call health --url ws://127.0.0.1:18999 --timeout 3000
```
