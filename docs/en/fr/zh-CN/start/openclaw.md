---
read_when:
  - 新手引导新助手实例时
  - 审查安全/权限影响时
summary: 将 OpenClaw 作为个人助手运行的端到端指南，包含安全注意事项
title: 个人助手设置
x-i18n:
  generated_at: "2026-02-03T07:54:35Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 2763668c053abe34ea72c40d1306d3d1143099c58b1e3ef91c2e5a20cb2769e0
  source_path: start/openclaw.md
  workflow: 15
---

# Construire un assistant personnel avec OpenClaw

OpenClaw est une passerelle WhatsApp + Telegram + Discord + iMessage pour les agents **Pi**. Un plugin peut ajouter Mattermost. Ce guide concerne la configuration "assistant personnel" : un numéro WhatsApp dédié qui se comporte comme votre agent résident.

## ⚠️ La sécurité d'abord

Vous permettez à l'agent de :

- Exécuter des commandes sur votre machine (selon votre configuration des outils Pi)
- Lire/écrire des fichiers dans votre espace de travail
- Envoyer des messages via WhatsApp/Telegram/Discord/Mattermost (plugin)

Commencez de manière conservatrice :

- Définissez toujours `channels.whatsapp.allowFrom` (ne l'ouvrez jamais au monde entier sur votre Mac personnel).
- Utilisez un numéro WhatsApp dédié pour l'assistant.
- Le heartbeat est maintenant par défaut toutes les 30 minutes. Désactivez-le en définissant `agents.defaults.heartbeat.every: "0m"` avant de faire confiance à la configuration.

## Prérequis

- Node **22+**
- OpenClaw disponible dans PATH (recommandé : installation globale)
- Un deuxième numéro de téléphone pour l'assistant (SIM/eSIM/prépayé)

```bash
npm install -g openclaw@latest
# ou : pnpm add -g openclaw@latest
```

Depuis le code source (développement) :

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # Installe automatiquement les dépendances UI à la première exécution
pnpm build
pnpm link --global
```

## Configuration à deux téléphones (recommandée)

Vous avez besoin de ceci :

```
Votre téléphone (personnel)     Deuxième téléphone (assistant)
┌─────────────────┐           ┌─────────────────┐
│  Votre WhatsApp │  ──────▶  │   Assistant WA  │
│  +1-555-YOU     │  Messages │  +1-555-ASSIST  │
└─────────────────┘           └────────┬────────┘
                                       │ Associé via code QR
                                       ▼
                              ┌─────────────────┐
                              │  Votre Mac      │
                              │  (openclaw)     │
                              │    Agent Pi     │
                              └─────────────────┘
```

Si vous associez votre WhatsApp personnel à OpenClaw, chaque message qui vous est envoyé devient une "entrée d'agent". Ce n'est généralement pas ce que vous voulez.

## Démarrage rapide en 5 minutes

1. Appairez WhatsApp Web (affiche un code QR ; scannez-le avec le téléphone de l'assistant) :

```bash
openclaw channels login
```

2. Démarrez la passerelle (gardez-la en cours d'exécution) :

```bash
openclaw gateway --port 18789
```

3. Placez une configuration minimale dans `~/.openclaw/openclaw.json` :

```json5
{
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Maintenant, envoyez un message au numéro de l'assistant depuis un téléphone de votre liste d'autorisation.

Après l'onboarding, nous ouvrirons automatiquement le tableau de bord avec le jeton de la passerelle et imprimerons le lien avec le jeton. Pour le rouvrir plus tard : `openclaw dashboard`.

## Donner un espace de travail à l'agent (AGENTS)

OpenClaw lit les instructions d'action et la "mémoire" du répertoire de l'espace de travail de son agent.

Par défaut, OpenClaw utilise `~/.openclaw/workspace` comme espace de travail de l'agent et le crée automatiquement lors de la configuration/première exécution de l'agent (plus les fichiers de démarrage `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`). `BOOTSTRAP.md` n'est créé que lorsque l'espace de travail est tout neuf (ne devrait pas réapparaître après suppression).

Conseil : Traitez ce dossier comme la "mémoire" d'OpenClaw et transformez-le en dépôt git (de préférence privé) afin que votre `AGENTS.md` + fichiers de mémoire soient sauvegardés. Si git est installé, un nouvel espace de travail s'initialise automatiquement.

```bash
openclaw setup
```

Disposition complète de l'espace de travail + guide de sauvegarde : [Espace de travail de l'agent](/concepts/agent-workspace)
Flux de mémoire : [Mémoire](/concepts/memory)

Optionnel : Utilisez `agents.defaults.workspace` pour choisir un espace de travail différent (supporte `~`).

```json5
{
  agent: {
    workspace: "~/.openclaw/workspace",
  },
}
```

Si vous avez déjà fourni vos propres fichiers d'espace de travail à partir d'un dépôt, vous pouvez désactiver complètement la création de fichiers d'amorçage :

```json5
{
  agent: {
    skipBootstrap: true,
  },
}
```

## Configuration pour en faire un "assistant"

OpenClaw est configuré par défaut pour un bon assistant, mais vous devez généralement ajuster :

- La personnalité/les instructions dans `SOUL.md`
- Les valeurs par défaut de réflexion (si nécessaire)
- Le heartbeat (une fois que vous lui faites confiance)

Exemple :

```json5
{
  logging: { level: "info" },
  agent: {
    model: "anthropic/claude-opus-4-5",
    workspace: "~/.openclaw/workspace",
    thinkingDefault: "high",
    timeoutSeconds: 1800,
    // Commencez à 0 ; activez plus tard.
    heartbeat: { every: "0m" },
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  routing: {
    groupChat: {
      mentionPatterns: ["@openclaw", "openclaw"],
    },
  },
  session: {
    scope: "per-sender",
    resetTriggers: ["/new", "/reset"],
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 10080,
    },
  },
}
```

## Sessions et mémoire

- Fichiers de session : `~/.openclaw/agents/<agentId>/sessions/{{SessionId}}.jsonl`
- Métadonnées de session (utilisation des tokens, dernier routage, etc.) : `~/.openclaw/agents/<agentId>/sessions/sessions.json` (ancien : `~/.openclaw/sessions/sessions.json`)
- `/new` ou `/reset` démarre une nouvelle session pour ce chat (configurable via `resetTriggers`). S'il est envoyé seul, l'agent répond par un court message de bienvenue pour confirmer la réinitialisation.
- `/compact [instructions]` compresse le contexte de la session et rapporte le budget de contexte restant.

## Heartbeat (mode actif)

Par défaut, OpenClaw exécute un heartbeat toutes les 30 minutes avec l'invite :
`Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`
Définissez `agents.defaults.heartbeat.every: "0m"` pour désactiver.

- Si `HEARTBEAT.md` existe mais est en fait vide (seulement des lignes vides et des titres markdown comme `# Heading`), OpenClaw saute l'exécution du heartbeat pour économiser les appels API.
- Si le fichier n'existe pas, le heartbeat s'exécute quand même, et le modèle décide quoi faire.
- Si l'agent répond `HEARTBEAT_OK` (optionnellement avec un court remplissage ; voir `agents.defaults.heartbeat.ackMaxChars`), OpenClaw supprime la livraison sortante pour ce heartbeat.
- L'exécution du heartbeat effectue un tour d'agent complet — des intervalles plus courts consomment plus de tokens.

```json5
{
  agent: {
    heartbeat: { every: "30m" },
  },
}
```

## Entrée et sortie de médias

Les pièces jointes entrantes (images/audio/documents) peuvent être exposées à vos commandes via des modèles :

- `{{MediaPath}}` (chemin de fichier temporaire local)
- `{{MediaUrl}}` (pseudo-URL)
- `{{Transcript}}` (si la transcription audio est activée)

Les pièces jointes sortantes de l'agent : incluez `MEDIA:<path-or-url>` sur une ligne séparée (sans espaces). Exemple :

```
Voici la capture d'écran.
MEDIA:https://example.com/screenshot.png
```

OpenClaw extraira ces éléments et les enverra en tant que médias avec le texte.

## Liste de contrôle des opérations

```bash
openclaw status          # État local (identifiants, sessions, événements en file d'attente)
openclaw status --all    # Diagnostic complet (lecture seule, peut être collé)
openclaw status --deep   # Ajoute les sondes de santé de la passerelle (Telegram + Discord)
openclaw health --json   # Snapshot de santé de la passerelle (WS)
```

Les journaux se trouvent dans `/tmp/openclaw/` (par défaut : `openclaw-YYYY-MM-DD.log`).

## Étapes suivantes

- WebChat : [WebChat](/web/webchat)
- Opérations de la passerelle : [Manuel d'exécution de la passerelle](/gateway)
- Tâches planifiées + réveil : [Tâches planifiées](/automation/cron-jobs)
- Application de barre de menu macOS : [Application OpenClaw macOS](/platforms/macos)
- Application nœud iOS : [Application iOS](/platforms/ios)
- Application nœud Android : [Application Android](/platforms/android)
- État Windows : [Windows (WSL2)](/platforms/windows)
- État Linux : [Application Linux](/platforms/linux)
- Sécurité : [Sécurité](/gateway/security)
