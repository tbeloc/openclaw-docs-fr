---
read_when:
  - Vous souhaitez implémenter une automatisation événementielle pour /new, /reset, /stop et les événements du cycle de vie des agents
  - Vous souhaitez construire, installer ou déboguer des hooks
summary: Hooks : automatisation événementielle pour les commandes et événements du cycle de vie
title: Hooks
x-i18n:
  generated_at: "2026-02-03T07:50:59Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 853227a0f1abd20790b425fa64dda60efc6b5f93c1b13ecd2dcb788268f71d79
  source_path: automation/hooks.md
  workflow: 15
---

# Hooks

Les Hooks fournissent un système événementiel extensible pour exécuter automatiquement des actions en réponse aux commandes et événements des agents. Les Hooks sont découverts automatiquement à partir de répertoires et peuvent être gérés via des commandes CLI, de la même manière que les Skills dans OpenClaw.

## Mise en route

Les Hooks sont de petits scripts qui s'exécutent lorsqu'un événement se produit. Il existe deux types :

- **Hooks** (cette page) : s'exécutent dans la passerelle Gateway lorsqu'un événement d'agent est déclenché, comme `/new`, `/reset`, `/stop` ou les événements du cycle de vie.
- **Webhooks** : webhooks HTTP externes qui permettent à d'autres systèmes de déclencher du travail dans OpenClaw. Voir [Webhook Hooks](/automation/webhook) ou utilisez `openclaw webhooks` pour les commandes d'assistant Gmail.

Les Hooks peuvent également être regroupés dans des plugins ; voir [Plugins](/tools/plugin#plugin-hooks).

Cas d'usage courants :

- Enregistrer un instantané de la mémoire lors de la réinitialisation d'une session
- Conserver une piste d'audit des commandes pour le dépannage ou la conformité
- Déclencher une automatisation ultérieure au démarrage ou à la fin d'une session
- Écrire des fichiers dans l'espace de travail de l'agent ou appeler des API externes lorsqu'un événement est déclenché

Si vous pouvez écrire une petite fonction TypeScript, vous pouvez écrire un hook. Les Hooks sont découverts automatiquement et vous pouvez les activer ou les désactiver via la CLI.

## Aperçu

Le système de hooks vous permet de :

- Enregistrer le contexte de session dans la mémoire lors de `/new`
- Enregistrer toutes les commandes pour l'audit
- Déclencher une automatisation personnalisée sur les événements du cycle de vie des agents
- Étendre le comportement d'OpenClaw sans modifier le code principal

## Mise en route

### Hooks fournis

OpenClaw est livré avec trois hooks fournis découverts automatiquement :

- **💾 session-memory** : enregistre le contexte de session dans l'espace de travail de l'agent lorsque vous émettez `/new` (par défaut `~/.openclaw/workspace/memory/`)
- **📝 command-logger** : enregistre tous les événements de commande dans `~/.openclaw/logs/commands.log`
- **🚀 boot-md** : exécute `BOOT.md` au démarrage de la passerelle Gateway (nécessite l'activation des hooks internes)

Lister les hooks disponibles :

```bash
openclaw hooks list
```

Activer un hook :

```bash
openclaw hooks enable session-memory
```

Vérifier l'état du hook :

```bash
openclaw hooks check
```

Obtenir des informations détaillées :

```bash
openclaw hooks info session-memory
```

### Onboarding

Pendant l'onboarding (`openclaw onboard`), vous serez invité à activer les hooks recommandés. L'assistant découvrira automatiquement les hooks éligibles et les présentera pour sélection.

## Découverte des Hooks

Les Hooks sont découverts automatiquement à partir de trois répertoires (par ordre de priorité) :

1. **Hooks d'espace de travail** : `<workspace>/hooks/` (par agent, priorité la plus élevée)
2. **Hooks gérés** : `~/.openclaw/hooks/` (installés par l'utilisateur, partagés entre les espaces de travail)
3. **Hooks fournis** : `<openclaw>/dist/hooks/bundled/` (fournis avec OpenClaw)

Le répertoire des hooks gérés peut être un **hook unique** ou un **paquet de hooks** (répertoire de paquet).

Chaque hook est un répertoire contenant :

```
my-hook/
├── HOOK.md          # Métadonnées + documentation
└── handler.ts       # Implémentation du gestionnaire
```

## Paquets de Hooks (npm/archives)

Les paquets de hooks sont des paquets npm standard qui exportent un ou plusieurs hooks via `openclaw.hooks` dans `package.json`. Installez-les avec :

```bash
openclaw hooks install <path-or-spec>
```

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
Les paquets de hooks peuvent être livrés avec des dépendances ; elles seront installées sous `~/.openclaw/hooks/<id>`.

## Structure des Hooks

### Format HOOK.md

Le fichier `HOOK.md` contient des métadonnées dans le frontmatter YAML, plus la documentation Markdown :

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

### Champs de métadonnées

L'objet `metadata.openclaw` supporte :

- **`emoji`** : emoji d'affichage pour la CLI (par exemple `"💾"`)
- **`events`** : tableau des événements à écouter (par exemple `["command:new", "command:reset"]`)
- **`export`** : export nommé à utiliser (par défaut `"default"`)
- **`homepage`** : URL de documentation
- **`requires`** : exigences optionnelles
  - **`bins`** : fichiers binaires requis dans PATH (par exemple `["git", "node"]`)
  - **`anyBins`** : au moins un de ces fichiers binaires doit exister
  - **`env`** : variables d'environnement requises
  - **`config`** : chemins de configuration requis (par exemple `["workspace.dir"]`)
  - **`os`** : plateformes requises (par exemple `["darwin", "linux"]`)
- **`always`** : contourner les vérifications d'éligibilité (booléen)
- **`install`** : méthode d'installation (pour les hooks fournis : `[{"id":"bundled","kind":"bundled"}]`)

### Implémentation du gestionnaire

Le fichier `handler.ts` exporte une fonction `HookHandler` :

```typescript
import type { HookHandler } from "../../src/hooks/hooks.js";

const myHandler: HookHandler = async (event) => {
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

#### Contexte d'événement

Chaque événement contient :

```typescript
{
  type: 'command' | 'session' | 'agent' | 'gateway',
  action: string,              // e.g., 'new', 'reset', 'stop'
  sessionKey: string,          // Session identifier
  timestamp: Date,             // When the event occurred
  messages: string[],          // Push messages here to send to user
  context: {
    sessionEntry?: SessionEntry,
    sessionId?: string,
    sessionFile?: string,
    commandSource?: string,    // e.g., 'whatsapp', 'telegram'
    senderId?: string,
    workspaceDir?: string,
    bootstrapFiles?: WorkspaceBootstrapFile[],
    cfg?: OpenClawConfig
  }
}
```

## Types d'événements

### Événements de commande

Déclenchés lorsqu'une commande d'agent est émise :

- **`command`** : tous les événements de commande (écouteur générique)
- **`command:new`** : lorsque la commande `/new` est émise
- **`command:reset`** : lorsque la commande `/reset` est émise
- **`command:stop`** : lorsque la commande `/stop` est émise

### Événements d'agent

- **`agent:bootstrap`** : avant l'injection des fichiers d'amorçage de l'espace de travail (les hooks peuvent modifier `context.bootstrapFiles`)

### Événements de passerelle Gateway

Déclenchés au démarrage de la passerelle Gateway :

- **`gateway:startup`** : après le démarrage des canaux et le chargement des hooks

### Hooks de résultats d'outils (API de plugin)

Ces hooks ne sont pas des écouteurs de flux d'événements ; ils permettent aux plugins d'ajuster de manière synchrone les résultats d'outils avant qu'OpenClaw ne les persiste.

- **`tool_result_persist`** : transforme les résultats d'outils avant qu'ils ne soient écrits dans l'enregistrement de session. Doit être synchrone ; retourne la charge utile de résultat d'outil mise à jour ou `undefined` pour la laisser inchangée. Voir [Boucle d'agent](/concepts/agent-loop).

### Événements futurs

Types d'événements prévus :

- **`session:start`** : au démarrage d'une nouvelle session
- **`session:end`** : à la fin d'une session
- **`agent:error`** : lorsque l'agent rencontre une erreur
- **`message:sent`** : lorsqu'un message est envoyé
- **`message:received`** : lorsqu'un message est reçu

## Création de Hooks personnalisés

### 1. Choisir un emplacement

- **Hooks d'espace de travail** (`<workspace>/hooks/`) : par agent, priorité la plus élevée
- **Hooks gérés** (`~/.openclaw/hooks/`) : partagés entre les espaces de travail

### 2. Créer la structure de répertoire

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
import type { HookHandler } from "../../src/hooks/hooks.js";

const handler: HookHandler = async (event) => {
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

### Configuration par Hook

Les Hooks peuvent avoir une configuration personnalisée :

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

L'ancien format de configuration reste valide pour la compatibilité rétroactive :

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

**Migration** : utilisez le nouveau système basé sur la découverte pour les nouveaux hooks. Les gestionnaires hérités sont chargés après les hooks basés sur les répertoires.

## Commandes CLI

### Lister les Hooks

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

### Informations sur les Hooks

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

## Hooks fournis

### session-memory

Enregistre le contexte de session dans la mémoire lorsque vous émettez `/new`.

**Événements** : `command:new`

**Exigences** : `workspace.dir` doit être configuré

**Sortie** : `<workspace>/memory/YYYY-MM-DD-slug.md` (par défaut `~/.openclaw/
