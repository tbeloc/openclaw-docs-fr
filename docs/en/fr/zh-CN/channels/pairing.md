```markdown
---
read_when:
  - Configurer le contrôle d'accès aux messages privés
  - Appairer de nouveaux nœuds iOS/Android
  - Examiner la posture de sécurité d'OpenClaw
summary: Aperçu de l'appairage : approuver qui peut vous envoyer des messages privés + quels nœuds peuvent rejoindre
title: Appairage
x-i18n:
  generated_at: "2026-02-03T07:54:19Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c46a5c39f289c8fd0783baacd927f550c3d3ae8889a7bc7de133b795f16fa08a
  source_path: channels/pairing.md
  workflow: 15
---

# Appairage

L'« appairage » est une étape d'**approbation explicite du propriétaire** dans OpenClaw. Il est utilisé à deux endroits :

1. **Appairage des messages privés** (qui est autorisé à discuter avec le bot)
2. **Appairage des nœuds** (quels appareils/nœuds sont autorisés à rejoindre le réseau Gateway)

Contexte de sécurité : [Sécurité](/gateway/security)

## 1) Appairage des messages privés (accès au chat entrant)

Lorsqu'un canal est configuré avec la politique de messages privés `pairing`, les expéditeurs inconnus reçoivent un code court et leurs messages **ne sont pas traités** jusqu'à votre approbation.

La politique de messages privés par défaut est documentée dans : [Sécurité](/gateway/security)

Codes d'appairage :

- 8 caractères, majuscules, sans caractères ambigus (`0O1I`).
- **Expire après 1 heure**. Le bot envoie uniquement des messages d'appairage lors de la création de nouvelles demandes (environ une fois par heure par expéditeur).
- La limite par défaut des demandes d'appairage de messages privés en attente est de **3 par canal** ; les demandes supplémentaires seront ignorées jusqu'à ce qu'une expire ou soit approuvée.

### Approuver un expéditeur

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

Canaux supportés : `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`.

### Emplacement du stockage d'état

Stocké sous `~/.openclaw/credentials/` :

- Demandes en attente : `<channel>-pairing.json`
- Liste d'autorisation approuvée : `<channel>-allowFrom.json`

Traitez ces fichiers comme des informations sensibles (ils contrôlent l'accès à votre assistant).

## 2) Appairage des appareils nœuds (iOS/Android/macOS/nœuds sans interface)

Les nœuds se connectent à Gateway en tant qu'**appareils** avec `role: node`. Gateway crée une demande d'appairage d'appareil qui doit être approuvée.

### Approuver un appareil nœud

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

### Emplacement du stockage d'état

Stocké sous `~/.openclaw/devices/` :

- `pending.json` (court terme ; les demandes en attente expirent)
- `paired.json` (appareils appairés + jetons)

### Remarques

- L'ancienne API `node.pair.*` (CLI : `openclaw nodes pending/approve`) est un stockage d'appairage distinct détenu par Gateway. Les nœuds WS nécessitent toujours un appairage d'appareil.

## Documentation connexe

- Modèle de sécurité + injection d'invites : [Sécurité](/gateway/security)
- Mises à jour de sécurité (exécuter doctor) : [Mise à jour](/install/updating)
- Configuration des canaux :
  - Telegram : [Telegram](/channels/telegram)
  - WhatsApp : [WhatsApp](/channels/whatsapp)
  - Signal : [Signal](/channels/signal)
  - iMessage : [iMessage](/channels/imessage)
  - Discord : [Discord](/channels/discord)
  - Slack : [Slack](/channels/slack)
```
