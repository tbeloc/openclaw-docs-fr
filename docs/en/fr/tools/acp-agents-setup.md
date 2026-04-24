---
summary: "Configuration des agents ACP : config du harnais acpx, configuration des plugins, permissions"
read_when:
  - Installation ou configuration du harnais acpx pour Claude Code / Codex / Gemini CLI
  - Activation du pont MCP plugin-tools ou OpenClaw-tools
  - Configuration des modes de permission ACP
title: "Agents ACP — configuration"
---

Pour l'aperçu, le runbook opérateur et les concepts, voir [Agents ACP](/fr/tools/acp-agents).
Cette page couvre la configuration du harnais acpx, la configuration des plugins pour les ponts MCP et
la configuration des permissions.

## Support du harnais acpx (actuel)

Alias de harnais intégrés acpx actuels :

- `claude`
- `codex`
- `copilot`
- `cursor` (Cursor CLI : `cursor-agent acp`)
- `droid`
- `gemini`
- `iflow`
- `kilocode`
- `kimi`
- `kiro`
- `openclaw`
- `opencode`
- `pi`
- `qwen`

Lorsqu'OpenClaw utilise le backend acpx, préférez ces valeurs pour `agentId` sauf si votre configuration acpx définit des alias d'agent personnalisés.
Si votre installation Cursor locale expose toujours ACP comme `agent acp`, remplacez plutôt la commande d'agent `cursor` dans votre configuration acpx au lieu de modifier la valeur par défaut intégrée.

L'utilisation directe de la CLI acpx peut également cibler des adaptateurs arbitraires via `--agent <command>`, mais cette échappatoire brute est une fonctionnalité de la CLI acpx (pas le chemin normal `agentId` d'OpenClaw).

## Configuration requise

Ligne de base ACP principale :

```json5
{
  acp: {
    enabled: true,
    // Optionnel. La valeur par défaut est true ; définissez false pour suspendre la distribution ACP tout en conservant les contrôles /acp.
    dispatch: { enabled: true },
    backend: "acpx",
    defaultAgent: "codex",
    allowedAgents: [
      "claude",
      "codex",
      "copilot",
      "cursor",
      "droid",
      "gemini",
      "iflow",
      "kilocode",
      "kimi",
      "kiro",
      "openclaw",
      "opencode",
      "pi",
      "qwen",
    ],
    maxConcurrentSessions: 8,
    stream: {
      coalesceIdleMs: 300,
      maxChunkChars: 1200,
    },
    runtime: {
      ttlMinutes: 120,
    },
  },
}
```

La configuration de liaison de thread est spécifique à l'adaptateur de canal. Exemple pour Discord :

```json5
{
  session: {
    threadBindings: {
      enabled: true,
      idleHours: 24,
      maxAgeHours: 0,
    },
  },
  channels: {
    discord: {
      threadBindings: {
        enabled: true,
        spawnAcpSessions: true,
      },
    },
  },
}
```

Si la génération ACP liée au thread ne fonctionne pas, vérifiez d'abord le drapeau de fonctionnalité de l'adaptateur :

- Discord : `channels.discord.threadBindings.spawnAcpSessions=true`

Les liaisons de conversation actuelle ne nécessitent pas la création de thread enfant. Elles nécessitent un contexte de conversation actif et un adaptateur de canal qui expose les liaisons de conversation ACP.

Voir [Référence de configuration](/fr/gateway/configuration-reference).

## Configuration des plugins pour le backend acpx

Les installations récentes livrent le plugin de runtime `acpx` fourni activé par défaut, donc ACP
fonctionne généralement sans étape d'installation manuelle de plugin.

Commencez par :

```text
/acp doctor
```

Si vous avez désactivé `acpx`, l'avez refusé via `plugins.allow` / `plugins.deny`, ou souhaitez
basculer vers une extraction de développement local, utilisez le chemin de plugin explicite :

```bash
openclaw plugins install acpx
openclaw config set plugins.entries.acpx.enabled true
```

Installation de l'espace de travail local pendant le développement :

```bash
openclaw plugins install ./path/to/local/acpx-plugin
```

Ensuite, vérifiez la santé du backend :

```text
/acp doctor
```

### Configuration de la commande et de la version acpx

Par défaut, le plugin `acpx` fourni utilise son binaire épinglé local au plugin (`node_modules/.bin/acpx` à l'intérieur du package du plugin). Le démarrage enregistre le backend comme non prêt et une tâche de fond vérifie `acpx --version` ; si le binaire est manquant ou ne correspond pas, il exécute `npm install --omit=dev --no-save acpx@<pinned>` et re-vérifie. La passerelle reste non-bloquante tout au long.

Remplacez la commande ou la version dans la configuration du plugin :

```json
{
  "plugins": {
    "entries": {
      "acpx": {
        "enabled": true,
        "config": {
          "command": "../acpx/dist/cli.js",
          "expectedVersion": "any"
        }
      }
    }
  }
}
```

- `command` accepte un chemin absolu, un chemin relatif (résolu à partir de l'espace de travail OpenClaw) ou un nom de commande.
- `expectedVersion: "any"` désactive la correspondance stricte des versions.
- Les chemins `command` personnalisés désactivent l'auto-installation locale du plugin.

Voir [Plugins](/fr/tools/plugin).

### Installation automatique des dépendances

Lorsque vous installez OpenClaw globalement avec `npm install -g openclaw`, les dépendances
du runtime acpx (binaires spécifiques à la plateforme) sont installées automatiquement
via un hook postinstall. Si l'installation automatique échoue, la passerelle démarre toujours
normalement et signale la dépendance manquante via `openclaw acp doctor`.

### Pont MCP plugin tools

Par défaut, les sessions ACPX n'exposent **pas** les outils enregistrés par les plugins OpenClaw
au harnais ACP.

Si vous souhaitez que les agents ACP tels que Codex ou Claude Code appellent les outils des plugins
OpenClaw installés tels que la récupération/stockage de mémoire, activez le pont dédié :

```bash
openclaw config set plugins.entries.acpx.config.pluginToolsMcpBridge true
```

Ce que cela fait :

- Injecte un serveur MCP intégré nommé `openclaw-plugin-tools` dans l'amorçage de la session ACPX.
- Expose les outils de plugin déjà enregistrés par les plugins OpenClaw installés et activés.
- Garde la fonctionnalité explicite et désactivée par défaut.

Notes de sécurité et de confiance :

- Cela élargit la surface d'outils du harnais ACP.
- Les agents ACP n'ont accès qu'aux outils de plugin déjà actifs dans la passerelle.
- Traitez cela comme la même limite de confiance que de laisser ces plugins s'exécuter dans
OpenClaw lui-même.
- Examinez les plugins installés avant de l'activer.

Les `mcpServers` personnalisés fonctionnent toujours comme avant. Le pont plugin-tools intégré est
une commodité opt-in supplémentaire, pas un remplacement pour la configuration générique du serveur MCP.

### Pont MCP OpenClaw tools

Par défaut, les sessions ACPX n'exposent **pas** non plus les outils OpenClaw intégrés via
MCP. Activez le pont core-tools séparé lorsqu'un agent ACP a besoin d'outils intégrés sélectionnés
tels que `cron` :

```bash
openclaw config set plugins.entries.acpx.config.openClawToolsMcpBridge true
```

Ce que cela fait :

- Injecte un serveur MCP intégré nommé `openclaw-tools` dans l'amorçage de la session ACPX.
- Expose les outils OpenClaw intégrés sélectionnés. Le serveur initial expose `cron`.
- Garde l'exposition des outils principaux explicite et désactivée par défaut.

### Configuration du délai d'expiration du runtime

Le plugin `acpx` fourni par défaut transforme le runtime intégré en un délai d'expiration de 120 secondes.
Cela donne aux harnais plus lents tels que Gemini CLI suffisamment de temps pour terminer
le démarrage et l'initialisation d'ACP. Remplacez-le si votre hôte a besoin d'une limite de runtime différente :

```bash
openclaw config set plugins.entries.acpx.config.timeoutSeconds 180
```

Redémarrez la passerelle après avoir modifié cette valeur.

### Configuration de l'agent de sonde de santé

Le plugin `acpx` fourni sonde un agent de harnais lors de la décision si le backend de runtime
intégré est prêt. Il est défini par défaut sur `codex`. Si votre déploiement utilise un agent ACP
par défaut différent, définissez l'agent de sonde sur le même id :

```bash
openclaw config set plugins.entries.acpx.config.probeAgent claude
```

Redémarrez la passerelle après avoir modifié cette valeur.

## Configuration des permissions

Les sessions ACP s'exécutent de manière non-interactive — il n'y a pas de TTY pour approuver ou refuser
les invites de permission d'écriture de fichier et d'exécution de shell. Le plugin acpx fournit deux clés
de configuration qui contrôlent la façon dont les permissions sont gérées :

Ces permissions du harnais ACPX sont séparées des approbations d'exécution OpenClaw et séparées des
drapeaux de contournement du backend CLI tels que Claude CLI `--permission-mode bypassPermissions`.
ACPX `approve-all` est le commutateur de rupture de verre au niveau du harnais pour les sessions ACP.

### `permissionMode`

Contrôle les opérations que l'agent du harnais peut effectuer sans demander.

| Valeur          | Comportement                                                    |
| --------------- | --------------------------------------------------------------- |
| `approve-all`   | Approuver automatiquement toutes les écritures de fichiers et les commandes shell. |
| `approve-reads` | Approuver automatiquement les lectures uniquement ; les écritures et l'exécution nécessitent des invites. |
| `deny-all`      | Refuser toutes les invites de permission.                       |

### `nonInteractivePermissions`

Contrôle ce qui se passe lorsqu'une invite de permission serait affichée mais qu'aucun TTY interactif n'est disponible (ce qui est toujours le cas pour les sessions ACP).

| Valeur | Comportement                                                          |
| ------ | --------------------------------------------------------------------- |
| `fail` | Abandonner la session avec `AcpRuntimeError`. **(par défaut)**        |
| `deny` | Refuser silencieusement la permission et continuer (dégradation gracieuse). |

### Configuration

Définissez via la configuration du plugin :

```bash
openclaw config set plugins.entries.acpx.config.permissionMode approve-all
openclaw config set plugins.entries.acpx.config.nonInteractivePermissions fail
```

Redémarrez la passerelle après avoir modifié ces valeurs.

> **Important :** OpenClaw utilise actuellement par défaut `permissionMode=approve-reads` et `nonInteractivePermissions=fail`. Dans les sessions ACP non-interactives, toute écriture ou exécution qui déclenche une invite de permission peut échouer avec `AcpRuntimeError: Permission prompt unavailable in non-interactive mode`.
>
> Si vous devez restreindre les permissions, définissez `nonInteractivePermissions` sur `deny` afin que les sessions se dégradent gracieusement au lieu de planter.

## Connexes

- [Agents ACP](/fr/tools/acp-agents) — aperçu, runbook opérateur, concepts
- [Sous-agents](/fr/tools/subagents)
- [Routage multi-agent](/fr/concepts/multi-agent)
