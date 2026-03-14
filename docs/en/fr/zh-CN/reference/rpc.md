---
read_when:
  - 添加或更改外部 CLI 集成
  - 调试 RPC 适配器（signal-cli、imsg）
summary: 外部 CLI（signal-cli、imsg）的 RPC 适配器和 Gateway 网关模式
title: RPC 适配器
x-i18n:
  generated_at: "2026-02-03T07:53:44Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c04edc952390304a22a3a4763aca00a0311b38d390477ec0be5fe485ec257fa7
  source_path: reference/rpc.md
  workflow: 15
---

# Adaptateur RPC

OpenClaw intègre les CLI externes via JSON-RPC. Deux modes sont actuellement utilisés.

## Mode A : Démon HTTP (signal-cli)

- `signal-cli` s'exécute en tant que démon, utilisant JSON-RPC via HTTP.
- Le flux d'événements est SSE (`/api/v1/events`).
- Sonde de santé : `/api/v1/check`.
- Lorsque `channels.signal.autoStart=true`, OpenClaw gère le cycle de vie.

Pour la configuration et les points de terminaison, voir [Signal](/channels/signal).

## Mode B : Sous-processus stdio (imsg)

- OpenClaw génère `imsg rpc` en tant que sous-processus.
- JSON-RPC utilise un format délimité par des sauts de ligne via stdin/stdout (un objet JSON par ligne).
- Aucun port TCP requis, aucun démon requis.

Méthodes principales utilisées :

- `watch.subscribe` → notifications (`method: "message"`)
- `watch.unsubscribe`
- `send`
- `chats.list` (sonde/diagnostic)

Pour la configuration et l'adressage (préférer `chat_id`), voir [iMessage](/channels/imessage).

## Guide de l'adaptateur

- La passerelle gère les processus (démarrage/arrêt liés au cycle de vie du fournisseur).
- Maintenez la résilience du client RPC : délais d'expiration, redémarrage à la sortie.
- Privilégiez les ID stables (par exemple `chat_id`) plutôt que les chaînes d'affichage.
