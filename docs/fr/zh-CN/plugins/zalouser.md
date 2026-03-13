---
read_when:
  - 你想在 OpenClaw 中支持 Zalo Personal（非官方）
  - 你正在配置或开发 zalouser 插件
summary: Zalo Personal 插件：通过 zca-cli 进行 QR 登录 + 消息（插件安装 + 渠道配置 + CLI + 工具）
title: Zalo Personal 插件
x-i18n:
  generated_at: "2026-02-03T07:53:33Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: b29b788b023cd50720e24fe6719f02e9f86c8bca9c73b3638fb53c2316718672
  source_path: plugins/zalouser.md
  workflow: 15
---

# Zalo Personal（Plugin）

Fournir le support de Zalo Personal à OpenClaw via un plugin, en utilisant `zca-cli` pour automatiser les comptes utilisateurs Zalo ordinaires.

> **Avertissement :** L'automatisation non officielle peut entraîner la suspension/fermeture du compte. Utilisation à vos risques et périls.

## Nommage

L'identifiant du canal est `zalouser`, pour clarifier qu'il s'agit d'une automatisation **des comptes utilisateurs Zalo personnels** (non officielle). Nous réservons `zalo` pour une intégration potentielle future de l'API Zalo officielle.

## Lieu d'exécution

Ce plugin **s'exécute dans le processus Gateway**.

Si vous utilisez une Gateway distante, installez/configurez-le **sur la machine exécutant la Gateway**, puis redémarrez la Gateway.

## Installation

### Option A : Installation depuis npm

```bash
openclaw plugins install @openclaw/zalouser
```

Redémarrez ensuite la Gateway.

### Option B : Installation depuis un dossier local (développement)

```bash
openclaw plugins install ./extensions/zalouser
cd ./extensions/zalouser && pnpm install
```

Redémarrez ensuite la Gateway.

## Prérequis : zca-cli

La machine Gateway doit avoir `zca` dans `PATH` :

```bash
zca --version
```

## Configuration

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

## Outils d'agent

Nom de l'outil : `zalouser`

Opérations : `send`、`image`、`link`、`friends`、`groups`、`me`、`status`
