---
read_when:
  - 更改语音唤醒词行为或默认值
  - 添加需要唤醒词同步的新节点平台
summary: 全局语音唤醒词（Gateway 网关拥有）及其如何跨节点同步
title: 语音唤醒
x-i18n:
  generated_at: "2026-02-03T07:51:10Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: eb34f52dfcdc3fc1ae088ae1f621f245546d3cf388299fbeea62face61788c37
  source_path: nodes/voicewake.md
  workflow: 15
---

# Activation vocale (mot de réveil global)

OpenClaw traite **les mots de réveil comme une liste globale unique**, détenue par la **passerelle Gateway**.

- **Pas** de mots de réveil personnalisés par nœud.
- **N'importe quel nœud/interface utilisateur d'application peut modifier** la liste ; les modifications sont persistées par la passerelle Gateway et diffusées à tous.
- Chaque appareil conserve son propre **commutateur d'activation/désactivation de la reconnaissance vocale** (expérience utilisateur locale + permissions différentes).

## Stockage (hôte de la passerelle Gateway)

Les mots de réveil sont stockés sur la machine de la passerelle Gateway :

- `~/.openclaw/settings/voicewake.json`

Structure :

```json
{ "triggers": ["openclaw", "claude", "computer"], "updatedAtMs": 1730000000000 }
```

## Protocole

### Méthodes

- `voicewake.get` → `{ triggers: string[] }`
- `voicewake.set`, paramètre `{ triggers: string[] }` → `{ triggers: string[] }`

Remarques :

- Les mots déclencheurs sont normalisés (espaces supprimés, valeurs nulles supprimées). Une liste vide revient aux valeurs par défaut.
- Des limites sont appliquées pour des raisons de sécurité (limite de nombre/longueur).

### Événements

- `voicewake.changed` charge utile `{ triggers: string[] }`

Destinataires :

- Tous les clients WebSocket (application macOS, WebChat, etc.)
- Tous les nœuds connectés (iOS/Android), ainsi qu'une poussée initiale de « l'état actuel » lors de la connexion du nœud.

## Comportement du client

### Application macOS

- Utilise la liste globale pour contrôler les déclencheurs `VoiceWakeRuntime`.
- La modification des « mots déclencheurs » dans les paramètres d'activation vocale appelle `voicewake.set`, puis dépend de la diffusion pour maintenir les autres clients synchronisés.

### Nœud iOS

- Utilise la liste globale pour la détection de déclenchement `VoiceWakeManager`.
- La modification des mots de réveil dans les paramètres appelle `voicewake.set` (via WebSocket Gateway), tout en maintenant la réactivité de la détection locale des mots de réveil.

### Nœud Android

- Expose un éditeur de mots de réveil dans les paramètres.
- Appelle `voicewake.set` via WebSocket Gateway, ce qui synchronise les modifications partout.
