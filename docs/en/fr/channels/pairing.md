---
summary: "Aperçu de l'appairage : approuvez qui peut vous envoyer des DM + quels nœuds peuvent rejoindre"
read_when:
  - Setting up DM access control
  - Pairing a new iOS/Android node
  - Reviewing OpenClaw security posture
title: "Appairage"
---

# Appairage

L'« appairage » est l'étape d'**approbation explicite du propriétaire** d'OpenClaw.
Il est utilisé dans deux cas :

1. **Appairage DM** (qui est autorisé à communiquer avec le bot)
2. **Appairage de nœud** (quels appareils/nœuds sont autorisés à rejoindre le réseau de passerelle)

Contexte de sécurité : [Sécurité](/gateway/security)

## 1) Appairage DM (accès au chat entrant)

Lorsqu'un canal est configuré avec la politique DM `pairing`, les expéditeurs inconnus reçoivent un code court et leur message n'est **pas traité** jusqu'à votre approbation.

Les politiques DM par défaut sont documentées dans : [Sécurité](/gateway/security)

Codes d'appairage :

- 8 caractères, majuscules, sans caractères ambigus (`0O1I`).
- **Expirent après 1 heure**. Le bot n'envoie le message d'appairage que lorsqu'une nouvelle demande est créée (environ une fois par heure par expéditeur).
- Les demandes d'appairage DM en attente sont limitées à **3 par canal** par défaut ; les demandes supplémentaires sont ignorées jusqu'à ce qu'une expire ou soit approuvée.

### Approuver un expéditeur

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

Canaux supportés : `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`, `feishu`.

### Où l'état est stocké

Stocké sous `~/.openclaw/credentials/` :

- Demandes en attente : `<channel>-pairing.json`
- Liste d'approbation stockée :
  - Compte par défaut : `<channel>-allowFrom.json`
  - Compte non-défaut : `<channel>-<accountId>-allowFrom.json`

Comportement de portée du compte :

- Les comptes non-défaut lisent/écrivent uniquement leur fichier de liste d'approbation limité.
- Le compte par défaut utilise le fichier de liste d'approbation non limité au canal.

Traitez-les comme sensibles (ils contrôlent l'accès à votre assistant).

## 2) Appairage d'appareil nœud (nœuds iOS/Android/macOS/headless)

Les nœuds se connectent à la passerelle en tant qu'**appareils** avec `role: node`. La passerelle
crée une demande d'appairage d'appareil qui doit être approuvée.

### Appairer via Telegram (recommandé pour iOS)

Si vous utilisez le plugin `device-pair`, vous pouvez effectuer l'appairage initial de l'appareil entièrement depuis Telegram :

1. Dans Telegram, envoyez un message à votre bot : `/pair`
2. Le bot répond avec deux messages : un message d'instruction et un message de **code de configuration** séparé (facile à copier/coller dans Telegram).
3. Sur votre téléphone, ouvrez l'application OpenClaw iOS → Paramètres → Passerelle.
4. Collez le code de configuration et connectez-vous.
5. De retour dans Telegram : `/pair approve`

Le code de configuration est une charge utile JSON codée en base64 qui contient :

- `url` : l'URL WebSocket de la passerelle (`ws://...` ou `wss://...`)
- `bootstrapToken` : un jeton d'amorçage à courte durée de vie pour un seul appareil utilisé pour la poignée de main d'appairage initiale

Traitez le code de configuration comme un mot de passe tant qu'il est valide.

### Approuver un appareil nœud

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

### Stockage de l'état d'appairage du nœud

Stocké sous `~/.openclaw/devices/` :

- `pending.json` (courte durée ; les demandes en attente expirent)
- `paired.json` (appareils appairés + jetons)

### Remarques

- L'API `node.pair.*` héritée (CLI : `openclaw nodes pending/approve`) est un
  magasin d'appairage distinct appartenant à la passerelle. Les nœuds WS nécessitent toujours un appairage d'appareil.

## Documentation connexe

- Modèle de sécurité + injection de prompt : [Sécurité](/gateway/security)
- Mise à jour sécurisée (exécuter doctor) : [Mise à jour](/install/updating)
- Configurations de canal :
  - Telegram : [Telegram](/channels/telegram)
  - WhatsApp : [WhatsApp](/channels/whatsapp)
  - Signal : [Signal](/channels/signal)
  - BlueBubbles (iMessage) : [BlueBubbles](/channels/bluebubbles)
  - iMessage (hérité) : [iMessage](/channels/imessage)
  - Discord : [Discord](/channels/discord)
  - Slack : [Slack](/channels/slack)
