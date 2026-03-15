---
summary: "Hooks: event-driven automation for commands and lifecycle events"
read_when:
  - You want event-driven automation for /new, /reset, /stop, and agent lifecycle events
  - You want to build, install, or debug hooks
title: "Hooks"
---

# Hooks

Les hooks fournissent un système événementiel extensible pour automatiser les actions en réponse aux commandes et événements des agents. Les hooks sont automatiquement découverts à partir de répertoires et peuvent être gérés via des commandes CLI, de la même manière que les skills fonctionnent dans OpenClaw.

## Getting Oriented

Les hooks sont de petits scripts qui s'exécutent quand quelque chose se produit. Il y a deux types :

- **Hooks** (cette page) : s'exécutent à l'intérieur de la Gateway quand des événements d'agent se déclenchent, comme `/new`, `/reset`, `/stop`, ou des événements de cycle de vie.
- **Webhooks** : webhooks HTTP externes qui permettent à d'autres systèmes de déclencher du travail dans OpenClaw. Voir [Webhook Hooks](/automation/webhook) ou utiliser `openclaw webhooks` pour les commandes d'aide Gmail.

Les hooks peuvent également être regroupés à l'intérieur de plugins ; voir [Plugins](/tools/plugin#plugin-hooks).

Utilisations courantes :

- Enregistrer un snapshot de mémoire quand vous réinitialisez une session
- Maintenir un journal d'audit des commandes pour le dépannage ou la conformité
- Déclencher une automatisation de suivi quand une session démarre ou se termine
- Écrire des fichiers dans l'espace de travail de l'agent ou appeler des API externes quand des événements se déclenchent

Si vous pouvez écrire une petite fonction TypeScript, vous pouvez écrire un hook. Les hooks sont découverts automatiquement, et vous les activez ou les désactivez via la CLI.

## Overview

Le système de hooks vous permet de :

- Enregistrer le contexte de session en mémoire quand `/new` est émis
- Enregistrer toutes les commandes pour l'audit
- Déclencher des automatisations personnalisées sur les événements du cycle de vie de l'agent
- Étendre le comportement d'OpenClaw sans modifier le code principal

## Getting Started

### Bundled Hooks

OpenClaw est livré avec quatre hooks regroupés qui sont automatiquement découverts :

- **💾 session-memory** : Enregistre le contexte de session dans votre espace de travail d'agent (par défaut `~/.openclaw/workspace/memory/`) quand vous émettez `/new`
- **📎 bootstrap-extra-files** : Injecte des fichiers de bootstrap d'espace de travail supplémentaires à partir de modèles glob/chemin configurés pendant `agent:bootstrap`
- **📝 command-logger** : Enregistre tous les événements de commande dans `~/.openclaw/logs/commands.log`
- **🚀 boot-md** : Exécute `BOOT.md` quand la gateway démarre (nécessite que les hooks internes soient activés)

Lister les hooks disponibles :

```bash
openclaw hooks list
```

Activer un hook :

```bash
openclaw hooks enable session-memory
```

Vérifier le statut des hooks :

```bash
openclaw hooks check
```

Obtenir des informations détaillées :

```bash
openclaw hooks info session-memory
```

### Onboarding

Pendant l'onboarding (`openclaw onboard`), vous serez invité à activer les hooks recommandés. L'assistant découvre automatiquement les hooks éligibles et les présente pour sélection.

## Hook Discovery

Les hooks sont automatiquement découverts à partir de trois répertoires (dans l'ordre de précédence) :

1. **Workspace hooks** : `<workspace>/hooks/` (par agent, plus haute précédence)
2. **Managed hooks** : `~/.openclaw/hooks/` (installés par l'utilisateur, partagés entre les espaces de travail)
3. **Bundled hooks** : `<openclaw>/dist/hooks/bundled/` (livrés avec OpenClaw)

Les répertoires de hooks gérés peuvent être soit un **hook unique** soit un **hook pack** (répertoire de package).

Chaque hook est un répertoire contenant :

```
my-hook/
├── HOOK.md          # Métadonnées + documentation
└── handler.ts       # Implémentation du handler
```

## Hook Packs (npm/archives)

Les hook packs sont des packages npm standard qui exportent un ou plusieurs hooks via `openclaw.hooks` dans
`package.json`. Installez-les avec :

```bash
openclaw hooks install <path-or-spec>
```

Les spécifications npm sont réservées au registre (nom du package + version exacte optionnelle ou dist-tag).
Les spécifications Git/URL/fichier et les plages semver sont rejetées.

Les spécifications nues et `@latest` restent sur la piste stable. Si npm résout l'une ou l'autre
à une préversion, OpenClaw s'arrête et vous demande d'opter explicitement avec une
balise de préversion telle que `@beta`/`@rc` ou une version de préversion exacte.

Exemple `package.json` :

```json
{
  "name": "@acme/my-hooks",
  "version": "0.1.0",
  "openclaw": {
    "hooks": ["./hooks/my-hook", "./hooks/other-hook"]
  }
}
```

Chaque entrée pointe vers un répertoire de hook contenant `HOOK.md` et `handler.ts` (ou `index.ts`).
Les hook packs peuvent expédier des dépendances ; elles seront installées sous `~/.openclaw/hooks/<id>`.
Chaque entrée `openclaw.hooks` doit rester à l'intérieur du répertoire du package après la résolution du symlink ;
les entrées qui s'échappent sont rejetées.

Note de sécurité : `openclaw hooks install` installe les dépendances avec `npm install --ignore-scripts`
(pas de scripts de cycle de vie). Gardez les arbres de dépendances des hook packs "pur JS/TS" et évitez les packages qui dépendent
de builds `postinstall`.

## Hook Structure

### HOOK.md Format

Le fichier `HOOK.md` contient des métadonnées en frontmatter YAML plus de la documentation Markdown :

```markdown
---
name: my-hook
description: "Short description of what this hook does"
homepage: https://docs.openclaw.ai/automation/hooks#my-hook
metadata:
  { "openclaw": { "emoji": "🔗", "events": ["command:new"], "requires": { "bins": ["node"] } } }
---

# My Hook

Detailed documentation goes here...

## What It Does

- Listens for `/new` commands
- Performs some action
- Logs the result

## Requirements

- Node.js must be installed

## Configuration

No configuration needed.
```

### Metadata Fields

L'objet `metadata.openclaw` supporte :

- **`emoji`** : Emoji d'affichage pour la CLI (par exemple, `"💾"`)
- **`events`** : Tableau des événements à écouter (par exemple, `["command:new", "command:reset"]`)
- **`export`** : Export nommé à utiliser (par défaut `"default"`)
- **`homepage`** : URL de documentation
- **`requires`** : Exigences optionnelles
  - **`bins`** : Binaires requis sur PATH (par exemple, `["git", "node"]`)
  - **`anyBins`** : Au moins l'un de ces binaires doit être présent
  - **`env`** : Variables d'environnement requises
  - **`config`** : Chemins de configuration requis (par exemple, `["workspace.dir"]`)
  - **`os`** : Plates-formes requises (par exemple, `["darwin", "linux"]`)
- **`always`** : Contourner les vérifications d'éligibilité (booléen)
- **`install`** : Méthodes d'installation (pour les hooks regroupés : `[{"id":"bundled","kind":"bundled"}]`)

### Handler Implementation

Le fichier `handler.ts` exporte une fonction `HookHandler` :

```typescript
const myHandler = async (event) => {
  // Only trigger on 'new' command
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log(`[my-hook] New command triggered`);
  console.log(`  Session: ${event.sessionKey}`);
  console.log(`  Timestamp: ${event.timestamp.toISOString()}`);

  // Your custom logic here

  // Optionally send message to user
  event.messages.push("✨ My hook executed!");
};

export default myHandler;
```

#### Event Context

Chaque événement inclut :

```typescript
{
  type: 'command' | 'session' | 'agent' | 'gateway' | 'message',
  action: string,              // e.g., 'new', 'reset', 'stop', 'received', 'sent'
  sessionKey: string,          // Session identifier
  timestamp: Date,             // When the event occurred
  messages: string[],          // Push messages here to send to user
  context: {
    // Command events:
    sessionEntry?: SessionEntry,
    sessionId?: string,
    sessionFile?: string,
    commandSource?: string,    // e.g., 'whatsapp', 'telegram'
    senderId?: string,
    workspaceDir?: string,
    bootstrapFiles?: WorkspaceBootstrapFile[],
    cfg?: OpenClawConfig,
    // Message events (see Message Events section for full details):
    from?: string,             // message:received
    to?: string,               // message:sent
    content?: string,
    channelId?: string,
    success?: boolean,         // message:sent
  }
}
```

## Types d'événements

### Événements de commande

Déclenchés lorsque des commandes d'agent sont émises :

- **`command`** : Tous les événements de commande (écouteur général)
- **`command:new`** : Lorsque la commande `/new` est émise
- **`command:reset`** : Lorsque la commande `/reset` est émise
- **`command:stop`** : Lorsque la commande `/stop` est émise

### Événements de session

- **`session:compact:before`** : Juste avant que la compaction résume l'historique
- **`session:compact:after`** : Après que la compaction se termine avec les métadonnées du résumé

Les charges utiles des hooks internes émettent celles-ci comme `type: "session"` avec `action: "compact:before"` / `action: "compact:after"` ; les écouteurs s'abonnent avec les clés combinées ci-dessus.
L'enregistrement du gestionnaire spécifique utilise le format de clé littérale `${type}:${action}`. Pour ces événements, enregistrez `session:compact:before` et `session:compact:after`.

### Événements d'agent

- **`agent:bootstrap`** : Avant que les fichiers d'amorçage de l'espace de travail ne soient injectés (les hooks peuvent muter `context.bootstrapFiles`)

### Événements de passerelle

Déclenchés au démarrage de la passerelle :

- **`gateway:startup`** : Après le démarrage des canaux et le chargement des hooks

### Événements de message

Déclenchés lorsque des messages sont reçus ou envoyés :

- **`message`** : Tous les événements de message (écouteur général)
- **`message:received`** : Lorsqu'un message entrant est reçu de n'importe quel canal. Se déclenche tôt dans le traitement avant la compréhension des médias. Le contenu peut contenir des espaces réservés bruts comme `<media:audio>` pour les pièces jointes multimédias qui n'ont pas encore été traitées.
- **`message:transcribed`** : Lorsqu'un message a été entièrement traité, y compris la transcription audio et la compréhension des liens. À ce stade, `transcript` contient le texte de transcription complet pour les messages audio. Utilisez ce hook lorsque vous avez besoin d'accès au contenu audio transcrit.
- **`message:preprocessed`** : Se déclenche pour chaque message après que toute compréhension des médias + liens soit terminée, donnant aux hooks accès au corps entièrement enrichi (transcriptions, descriptions d'images, résumés de liens) avant que l'agent ne le voie.
- **`message:sent`** : Lorsqu'un message sortant est envoyé avec succès

#### Contexte des événements de message

Les événements de message incluent un contexte riche sur le message :

```typescript
// contexte message:received
{
  from: string,           // Identifiant de l'expéditeur (numéro de téléphone, ID utilisateur, etc.)
  content: string,        // Contenu du message
  timestamp?: number,     // Horodatage Unix à la réception
  channelId: string,      // Canal (par exemple, "whatsapp", "telegram", "discord")
  accountId?: string,     // ID de compte du fournisseur pour les configurations multi-comptes
  conversationId?: string, // ID de chat/conversation
  messageId?: string,     // ID de message du fournisseur
  metadata?: {            // Données supplémentaires spécifiques au fournisseur
    to?: string,
    provider?: string,
    surface?: string,
    threadId?: string,
    senderId?: string,
    senderName?: string,
    senderUsername?: string,
    senderE164?: string,
  }
}

// contexte message:sent
{
  to: string,             // Identifiant du destinataire
  content: string,        // Contenu du message envoyé
  success: boolean,       // Si l'envoi a réussi
  error?: string,         // Message d'erreur si l'envoi a échoué
  channelId: string,      // Canal (par exemple, "whatsapp", "telegram", "discord")
  accountId?: string,     // ID de compte du fournisseur
  conversationId?: string, // ID de chat/conversation
  messageId?: string,     // ID de message retourné par le fournisseur
  isGroup?: boolean,      // Si ce message sortant appartient à un contexte de groupe/canal
  groupId?: string,       // Identifiant de groupe/canal pour la corrélation avec message:received
}

// contexte message:transcribed
{
  body?: string,          // Corps entrant brut avant enrichissement
  bodyForAgent?: string,  // Corps enrichi visible à l'agent
  transcript: string,     // Texte de transcription audio
  channelId: string,      // Canal (par exemple, "telegram", "whatsapp")
  conversationId?: string,
  messageId?: string,
}

// contexte message:preprocessed
{
  body?: string,          // Corps entrant brut
  bodyForAgent?: string,  // Corps enrichi final après compréhension des médias/liens
  transcript?: string,    // Transcription lorsqu'un audio était présent
  channelId: string,      // Canal (par exemple, "telegram", "whatsapp")
  conversationId?: string,
  messageId?: string,
  isGroup?: boolean,
  groupId?: string,
}
```

#### Exemple : Hook de journalisation des messages

```typescript
const isMessageReceivedEvent = (event: { type: string; action: string }) =>
  event.type === "message" && event.action === "received";
const isMessageSentEvent = (event: { type: string; action: string }) =>
  event.type === "message" && event.action === "sent";

const handler = async (event) => {
  if (isMessageReceivedEvent(event as { type: string; action: string })) {
    console.log(`[message-logger] Received from ${event.context.from}: ${event.context.content}`);
  } else if (isMessageSentEvent(event as { type: string; action: string })) {
    console.log(`[message-logger] Sent to ${event.context.to}: ${event.context.content}`);
  }
};

export default handler;
```

### Hooks de résultat d'outil (API de plugin)

Ces hooks ne sont pas des écouteurs de flux d'événements ; ils permettent aux plugins d'ajuster de manière synchrone les résultats des outils avant qu'OpenClaw ne les persiste.

- **`tool_result_persist`** : transformer les résultats des outils avant qu'ils ne soient écrits dans la transcription de session. Doit être synchrone ; retournez la charge utile de résultat d'outil mise à jour ou `undefined` pour la conserver telle quelle. Voir [Boucle d'agent](/concepts/agent-loop).

### Événements de hook de plugin

Hooks du cycle de vie de compaction exposés via le runner de hook de plugin :

- **`before_compaction`** : S'exécute avant la compaction avec les métadonnées de compte/jeton
- **`after_compaction`** : S'exécute après la compaction avec les métadonnées du résumé de compaction

### Événements futurs

Types d'événements prévus :

- **`session:start`** : Lorsqu'une nouvelle session commence
- **`session:end`** : Lorsqu'une session se termine
- **`agent:error`** : Lorsqu'un agent rencontre une erreur

## Créer des hooks personnalisés

### 1. Choisir un emplacement

- **Hooks d'espace de travail** (`<workspace>/hooks/`) : Par agent, priorité la plus élevée
- **Hooks gérés** (`~/.openclaw/hooks/`) : Partagés entre les espaces de travail

### 2. Créer la structure de répertoires

```bash
mkdir -p ~/.openclaw/hooks/my-hook
cd ~/.openclaw/hooks/my-hook
```

### 3. Créer HOOK.md

```markdown
---
name: my-hook
description: "Does something useful"
metadata: { "openclaw": { "emoji": "🎯", "events": ["command:new"] } }
---

# My Custom Hook

This hook does something useful when you issue `/new`.
```

### 4. Créer handler.ts

```typescript
const handler = async (event) => {
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log("[my-hook] Running!");
  // Your logic here
};

export default handler;
```

### 5. Activer et tester

```bash
# Verify hook is discovered
openclaw hooks list

# Enable it
openclaw hooks enable my-hook

# Restart your gateway process (menu bar app restart on macOS, or restart your dev process)

# Trigger the event
# Send /new via your messaging channel
```

## Configuration

### Nouveau format de configuration (recommandé)

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": { "enabled": true },
        "command-logger": { "enabled": false }
      }
    }
  }
}
```

### Configuration par hook

Les hooks peuvent avoir une configuration personnalisée :

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "my-hook": {
          "enabled": true,
          "env": {
            "MY_CUSTOM_VAR": "value"
          }
        }
      }
    }
  }
}
```

### Répertoires supplémentaires

Charger les hooks à partir de répertoires supplémentaires :

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "load": {
        "extraDirs": ["/path/to/more/hooks"]
      }
    }
  }
}
```

### Format de configuration hérité (toujours supporté)

L'ancien format de configuration fonctionne toujours pour la compatibilité rétroactive :

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/handlers/my-handler.ts",
          "export": "default"
        }
      ]
    }
  }
}
```

Remarque : `module` doit être un chemin relatif à l'espace de travail. Les chemins absolus et la traversée en dehors de l'espace de travail sont rejetés.

**Migration** : Utilisez le nouveau système basé sur la découverte pour les nouveaux hooks. Les gestionnaires hérités sont chargés après les hooks basés sur les répertoires.

## Commandes CLI

### Lister les hooks

```bash
# List all hooks
openclaw hooks list

# Show only eligible hooks
openclaw hooks list --eligible

# Verbose output (show missing requirements)
openclaw hooks list --verbose

# JSON output
openclaw hooks list --json
```

### Informations sur les hooks

```bash
# Show detailed info about a hook
openclaw hooks info session-memory

# JSON output
openclaw hooks info session-memory --json
```

### Vérifier l'éligibilité

```bash
# Show eligibility summary
openclaw hooks check

# JSON output
openclaw hooks check --json
```

### Activer/Désactiver

```bash
# Enable a hook
openclaw hooks enable session-memory

# Disable a hook
openclaw hooks disable command-logger
```

## Référence des hooks groupés

### session-memory

Enregistre le contexte de session en mémoire lorsque vous émettez `/new`.

**Événements**: `command:new`

**Exigences**: `workspace.dir` doit être configuré

**Sortie**: `<workspace>/memory/YYYY-MM-DD-slug.md` (par défaut `~/.openclaw/workspace`)

**Ce qu'il fait**:

1. Utilise l'entrée de session pré-réinitialisation pour localiser la bonne transcription
2. Extrait les 15 dernières lignes de conversation
3. Utilise l'LLM pour générer un slug de nom de fichier descriptif
4. Enregistre les métadonnées de session dans un fichier mémoire daté

**Exemple de sortie**:

```markdown
# Session: 2026-01-16 14:30:00 UTC

- **Session Key**: agent:main:main
- **Session ID**: abc123def456
- **Source**: telegram
```

**Exemples de noms de fichiers**:

- `2026-01-16-vendor-pitch.md`
- `2026-01-16-api-design.md`
- `2026-01-16-1430.md` (horodatage de secours si la génération du slug échoue)

**Activer**:

```bash
openclaw hooks enable session-memory
```

### bootstrap-extra-files

Injecte des fichiers d'amorçage supplémentaires (par exemple, `AGENTS.md` / `TOOLS.md` locaux au monorepo) lors de `agent:bootstrap`.

**Événements**: `agent:bootstrap`

**Exigences**: `workspace.dir` doit être configuré

**Sortie**: Aucun fichier écrit; le contexte d'amorçage est modifié en mémoire uniquement.

**Configuration**:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "bootstrap-extra-files": {
          "enabled": true,
          "paths": ["packages/*/AGENTS.md", "packages/*/TOOLS.md"]
        }
      }
    }
  }
}
```

**Notes**:

- Les chemins sont résolus par rapport à l'espace de travail.
- Les fichiers doivent rester dans l'espace de travail (vérification realpath).
- Seuls les noms de base d'amorçage reconnus sont chargés.
- La liste d'autorisation des sous-agents est préservée (`AGENTS.md` et `TOOLS.md` uniquement).

**Activer**:

```bash
openclaw hooks enable bootstrap-extra-files
```

### command-logger

Enregistre tous les événements de commande dans un fichier d'audit centralisé.

**Événements**: `command`

**Exigences**: Aucune

**Sortie**: `~/.openclaw/logs/commands.log`

**Ce qu'il fait**:

1. Capture les détails de l'événement (action de commande, horodatage, clé de session, ID de l'expéditeur, source)
2. Ajoute au fichier journal au format JSONL
3. S'exécute silencieusement en arrière-plan

**Exemples d'entrées de journal**:

```jsonl
{"timestamp":"2026-01-16T14:30:00.000Z","action":"new","sessionKey":"agent:main:main","senderId":"+1234567890","source":"telegram"}
{"timestamp":"2026-01-16T15:45:22.000Z","action":"stop","sessionKey":"agent:main:main","senderId":"user@example.com","source":"whatsapp"}
```

**Afficher les journaux**:

```bash
# Afficher les commandes récentes
tail -n 20 ~/.openclaw/logs/commands.log

# Affichage joli avec jq
cat ~/.openclaw/logs/commands.log | jq .

# Filtrer par action
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

**Activer**:

```bash
openclaw hooks enable command-logger
```

### boot-md

Exécute `BOOT.md` au démarrage de la passerelle (après le démarrage des canaux).
Les hooks internes doivent être activés pour que cela s'exécute.

**Événements**: `gateway:startup`

**Exigences**: `workspace.dir` doit être configuré

**Ce qu'il fait**:

1. Lit `BOOT.md` depuis votre espace de travail
2. Exécute les instructions via le gestionnaire d'agents
3. Envoie tous les messages sortants demandés via l'outil de message

**Activer**:

```bash
openclaw hooks enable boot-md
```

## Bonnes pratiques

### Gardez les gestionnaires rapides

Les hooks s'exécutent lors du traitement des commandes. Gardez-les légers:

```typescript
// ✓ Bon - travail asynchrone, retour immédiat
const handler: HookHandler = async (event) => {
  void processInBackground(event); // Déclencher et oublier
};

// ✗ Mauvais - bloque le traitement des commandes
const handler: HookHandler = async (event) => {
  await slowDatabaseQuery(event);
  await evenSlowerAPICall(event);
};
```

### Gérez les erreurs avec élégance

Enveloppez toujours les opérations risquées:

```typescript
const handler: HookHandler = async (event) => {
  try {
    await riskyOperation(event);
  } catch (err) {
    console.error("[my-handler] Failed:", err instanceof Error ? err.message : String(err));
    // Ne pas lever - laisser les autres gestionnaires s'exécuter
  }
};
```

### Filtrez les événements tôt

Retournez tôt si l'événement n'est pas pertinent:

```typescript
const handler: HookHandler = async (event) => {
  // Gérer uniquement les commandes 'new'
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  // Votre logique ici
};
```

### Utilisez des clés d'événement spécifiques

Spécifiez les événements exacts dans les métadonnées si possible:

```yaml
metadata: { "openclaw": { "events": ["command:new"] } } # Spécifique
```

Plutôt que:

```yaml
metadata: { "openclaw": { "events": ["command"] } } # Général - plus de surcharge
```

## Débogage

### Activer la journalisation des hooks

La passerelle enregistre le chargement des hooks au démarrage:

```
Registered hook: session-memory -> command:new
Registered hook: bootstrap-extra-files -> agent:bootstrap
Registered hook: command-logger -> command
Registered hook: boot-md -> gateway:startup
```

### Vérifier la découverte

Lister tous les hooks découverts:

```bash
openclaw hooks list --verbose
```

### Vérifier l'enregistrement

Dans votre gestionnaire, enregistrez quand il est appelé:

```typescript
const handler: HookHandler = async (event) => {
  console.log("[my-handler] Triggered:", event.type, event.action);
  // Votre logique
};
```

### Vérifier l'éligibilité

Vérifiez pourquoi un hook n'est pas éligible:

```bash
openclaw hooks info my-hook
```

Recherchez les exigences manquantes dans la sortie.

## Tests

### Journaux de la passerelle

Surveillez les journaux de la passerelle pour voir l'exécution des hooks:

```bash
# macOS
./scripts/clawlog.sh -f

# Autres plates-formes
tail -f ~/.openclaw/gateway.log
```

### Testez les hooks directement

Testez vos gestionnaires isolément:

```typescript
import { test } from "vitest";
import myHandler from "./hooks/my-hook/handler.js";

test("my handler works", async () => {
  const event = {
    type: "command",
    action: "new",
    sessionKey: "test-session",
    timestamp: new Date(),
    messages: [],
    context: { foo: "bar" },
  };

  await myHandler(event);

  // Affirmer les effets secondaires
});
```

## Architecture

### Composants principaux

- **`src/hooks/types.ts`**: Définitions de type
- **`src/hooks/workspace.ts`**: Analyse de répertoire et chargement
- **`src/hooks/frontmatter.ts`**: Analyse des métadonnées HOOK.md
- **`src/hooks/config.ts`**: Vérification d'éligibilité
- **`src/hooks/hooks-status.ts`**: Rapport de statut
- **`src/hooks/loader.ts`**: Chargeur de module dynamique
- **`src/cli/hooks-cli.ts`**: Commandes CLI
- **`src/gateway/server-startup.ts`**: Charge les hooks au démarrage de la passerelle
- **`src/auto-reply/reply/commands-core.ts`**: Déclenche les événements de commande

### Flux de découverte

```
Démarrage de la passerelle
    ↓
Analyser les répertoires (espace de travail → géré → groupé)
    ↓
Analyser les fichiers HOOK.md
    ↓
Vérifier l'éligibilité (bins, env, config, os)
    ↓
Charger les gestionnaires à partir des hooks éligibles
    ↓
Enregistrer les gestionnaires pour les événements
```

### Flux d'événement

```
L'utilisateur envoie /new
    ↓
Validation de la commande
    ↓
Créer un événement hook
    ↓
Déclencher le hook (tous les gestionnaires enregistrés)
    ↓
Le traitement des commandes continue
    ↓
Réinitialisation de session
```

## Dépannage

### Hook non découvert

1. Vérifiez la structure du répertoire:

   ```bash
   ls -la ~/.openclaw/hooks/my-hook/
   # Devrait afficher: HOOK.md, handler.ts
   ```

2. Vérifiez le format HOOK.md:

   ```bash
   cat ~/.openclaw/hooks/my-hook/HOOK.md
   # Devrait avoir un préambule YAML avec nom et métadonnées
   ```

3. Lister tous les hooks découverts:

   ```bash
   openclaw hooks list
   ```

### Hook non éligible

Vérifiez les exigences:

```bash
openclaw hooks info my-hook
```

Recherchez les éléments manquants:

- Binaires (vérifier PATH)
- Variables d'environnement
- Valeurs de configuration
- Compatibilité du système d'exploitation

### Hook non exécuté

1. Vérifiez que le hook est activé:

   ```bash
   openclaw hooks list
   # Devrait afficher ✓ à côté des hooks activés
   ```

2. Redémarrez votre processus de passerelle pour que les hooks se rechargent.

3. Vérifiez les journaux de la passerelle pour les erreurs:

   ```bash
   ./scripts/clawlog.sh | grep hook
   ```

### Erreurs du gestionnaire

Vérifiez les erreurs TypeScript/import:

```bash
# Tester l'import directement
node -e "import('./path/to/handler.ts').then(console.log)"
```

## Guide de migration

### De la configuration héritée à la découverte

**Avant**:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/handlers/my-handler.ts"
        }
      ]
    }
  }
}
```

**Après**:

1. Créer le répertoire du hook:

   ```bash
   mkdir -p ~/.openclaw/hooks/my-hook
   mv ./hooks/handlers/my-handler.ts ~/.openclaw/hooks/my-hook/handler.ts
   ```

2. Créer HOOK.md:

   ```markdown
   ---
   name: my-hook
   description: "My custom hook"
   metadata: { "openclaw": { "emoji": "🎯", "events": ["command:new"] } }
   ---

   # My Hook

   Does something useful.
   ```

3. Mettre à jour la configuration:

   ```json
   {
     "hooks": {
       "internal": {
         "enabled": true,
         "entries": {
           "my-hook": { "enabled": true }
         }
       }
     }
   }
   ```

4. Vérifier et redémarrer votre processus de passerelle:

   ```bash
   openclaw hooks list
   # Devrait afficher: 🎯 my-hook ✓
   ```

**Avantages de la migration**:

- Découverte automatique
- Gestion CLI
- Vérification d'éligibilité
- Meilleure documentation
- Structure cohérente

## Voir aussi

- [Référence CLI: hooks](/cli/hooks)
- [README des hooks groupés](https://github.com/openclaw/openclaw/tree/main/src/hooks/bundled)
- [Webhook Hooks](/automation/webhook)
- [Configuration](/gateway/configuration#hooks)
