---
summary: "Plugin Zalo Personal : connexion QR + messagerie via zca-js natif (installation plugin + config canal + outil)"
read_when:
  - Vous voulez le support Zalo Personal (non officiel) dans OpenClaw
  - Vous configurez ou développez le plugin zalouser
title: "Plugin Zalo Personal"
---

# Zalo Personal (plugin)

Support Zalo Personal pour OpenClaw via un plugin, utilisant `zca-js` natif pour automatiser un compte utilisateur Zalo normal.

> **Avertissement :** L'automatisation non officielle peut entraîner la suspension/interdiction du compte. Utilisez à vos risques et périls.

## Nommage

L'identifiant du canal est `zalouser` pour clarifier qu'il automatise un **compte utilisateur Zalo personnel** (non officiel). Nous réservons `zalo` pour une intégration potentielle future avec l'API officielle Zalo.

## Où il s'exécute

Ce plugin s'exécute **à l'intérieur du processus Gateway**.

Si vous utilisez une Gateway distante, installez/configurez-le sur la **machine exécutant la Gateway**, puis redémarrez la Gateway.

Aucun binaire CLI externe `zca`/`openzca` n'est requis.

## Installation

### Option A : installer depuis npm

```bash
openclaw plugins install @openclaw/zalouser
```

Redémarrez la Gateway après.

### Option B : installer depuis un dossier local (dev)

```bash
openclaw plugins install ./extensions/zalouser
cd ./extensions/zalouser && pnpm install
```

Redémarrez la Gateway après.

## Config

La configuration du canal se trouve sous `channels.zalouser` (pas `plugins.entries.*`) :

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

## CLI

```bash
openclaw channels login --channel zalouser
openclaw channels logout --channel zalouser
openclaw channels status --probe
openclaw message send --channel zalouser --target <threadId> --message "Hello from OpenClaw"
openclaw directory peers list --channel zalouser --query "name"
```

## Outil Agent

Nom de l'outil : `zalouser`

Actions : `send`, `image`, `link`, `friends`, `groups`, `me`, `status`

Les actions de message de canal supportent également `react` pour les réactions aux messages.
