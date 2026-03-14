---
read_when:
  - Vous souhaitez gérer les crochets d'agent
  - Vous souhaitez installer ou mettre à jour des crochets
summary: Référence CLI：`openclaw hooks`（crochets d'agent）
title: hooks
x-i18n:
  generated_at: "2026-02-03T10:04:32Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: e2032e61ff4b9135cb2708d92eb7889ac627b85a5fc153e3d5b84265f7bd7bc6
  source_path: cli/hooks.md
  workflow: 15
---

# `openclaw hooks`

Gérez les crochets d'agent (pour les commandes `/new`, `/reset`, etc. et l'automatisation pilotée par les événements lancés par la passerelle Gateway).

Contenu connexe：

- Crochets：[Crochets](/automation/hooks)
- Crochets de plugin：[Plugin](/tools/plugin#plugin-hooks)

## Lister tous les crochets

```bash
openclaw hooks list
```

Liste tous les crochets découverts dans l'espace de travail, les répertoires hébergés et les répertoires intégrés.

**Options：**

- `--eligible`：affiche uniquement les crochets éligibles (qui répondent aux exigences)
- `--json`：sortie au format JSON
- `-v, --verbose`：affiche les informations détaillées, y compris les exigences manquantes

**Exemple de sortie：**

```
Hooks (3/3 ready)

Ready:
  🚀 boot-md ✓ - Run BOOT.md on gateway startup
  📝 command-logger ✓ - Log all command events to a centralized audit file
  💾 session-memory ✓ - Save session context to memory when /new command is issued
```

**Exemple (mode détaillé)：**

```bash
openclaw hooks list --verbose
```

Affiche les exigences manquantes pour les crochets non éligibles.

**Exemple (JSON)：**

```bash
openclaw hooks list --json
```

Retourne du JSON structuré pour une utilisation programmatique.

## Obtenir les informations du crochet

```bash
openclaw hooks info <name>
```

Affiche les informations détaillées d'un crochet spécifique.

**Paramètres：**

- `<name>`：nom du crochet (par exemple `session-memory`)

**Options：**

- `--json`：sortie au format JSON

**Exemple：**

```bash
openclaw hooks info session-memory
```

**Sortie：**

```
💾 session-memory ✓ Ready

Save session context to memory when /new command is issued

Details:
  Source: openclaw-bundled
  Path: /path/to/openclaw/hooks/bundled/session-memory/HOOK.md
  Handler: /path/to/openclaw/hooks/bundled/session-memory/handler.ts
  Homepage: https://docs.openclaw.ai/automation/hooks#session-memory
  Events: command:new

Requirements:
  Config: ✓ workspace.dir
```

## Vérifier l'éligibilité des crochets

```bash
openclaw hooks check
```

Affiche un résumé de l'état d'éligibilité des crochets (combien sont prêts, combien ne le sont pas).

**Options：**

- `--json`：sortie au format JSON

**Exemple de sortie：**

```
Hooks Status

Total hooks: 4
Ready: 4
Not ready: 0
```

## Activer un crochet

```bash
openclaw hooks enable <name>
```

Active un crochet spécifique en l'ajoutant à la configuration (`~/.openclaw/config.json`).

**Remarque：** Les crochets gérés par des plugins affichent `plugin:<id>` dans `openclaw hooks list` et
ne peuvent pas être activés/désactivés ici. Activez/désactivez plutôt le plugin.

**Paramètres：**

- `<name>`：nom du crochet (par exemple `session-memory`)

**Exemple：**

```bash
openclaw hooks enable session-memory
```

**Sortie：**

```
✓ Enabled hook: 💾 session-memory
```

**Actions effectuées：**

- Vérifie que le crochet existe et est éligible
- Met à jour `hooks.internal.entries.<name>.enabled = true` dans la configuration
- Enregistre la configuration sur le disque

**Après activation：**

- Redémarrez la passerelle Gateway pour recharger les crochets (redémarrez l'application de la barre de menu sur macOS, ou redémarrez le processus Gateway en environnement de développement).

## Désactiver un crochet

```bash
openclaw hooks disable <name>
```

Désactive un crochet spécifique en mettant à jour la configuration.

**Paramètres：**

- `<name>`：nom du crochet (par exemple `command-logger`)

**Exemple：**

```bash
openclaw hooks disable command-logger
```

**Sortie：**

```
⏸ Disabled hook: 📝 command-logger
```

**Après désactivation：**

- Redémarrez la passerelle Gateway pour recharger les crochets

## Installer un crochet

```bash
openclaw hooks install <path-or-spec>
```

Installez un paquet de crochet à partir d'un dossier local/archive ou npm.

**Actions effectuées：**

- Copie le paquet de crochet vers `~/.openclaw/hooks/<id>`
- Active le crochet installé dans `hooks.internal.entries.*`
- Enregistre les informations d'installation sous `hooks.internal.installs`

**Options：**

- `-l, --link`：lie le répertoire local au lieu de le copier (l'ajoute à `hooks.internal.load.extraDirs`)

**Formats d'archive supportés：** `.zip`、`.tgz`、`.tar.gz`、`.tar`

**Exemples：**

```bash
# Répertoire local
openclaw hooks install ./my-hook-pack

# Archive locale
openclaw hooks install ./my-hook-pack.zip

# Paquet NPM
openclaw hooks install @openclaw/my-hook-pack

# Lier le répertoire local sans copier
openclaw hooks install -l ./my-hook-pack
```

## Mettre à jour un crochet

```bash
openclaw hooks update <id>
openclaw hooks update --all
```

Mettez à jour les paquets de crochets installés (installations npm uniquement).

**Options：**

- `--all`：met à jour tous les paquets de crochets suivis
- `--dry-run`：affiche les modifications qui seront apportées, mais ne les écrit pas

## Crochets intégrés

### session-memory

Enregistre le contexte de la session en mémoire lorsque vous exécutez `/new`.

**Activation：**

```bash
openclaw hooks enable session-memory
```

**Sortie：** `~/.openclaw/workspace/memory/YYYY-MM-DD-slug.md`

**Voir：** [Documentation session-memory](/automation/hooks#session-memory)

### command-logger

Enregistre tous les événements de commande dans un fichier d'audit centralisé.

**Activation：**

```bash
openclaw hooks enable command-logger
```

**Sortie：** `~/.openclaw/logs/commands.log`

**Afficher les journaux：**

```bash
# Commandes récentes
tail -n 20 ~/.openclaw/logs/commands.log

# Sortie formatée
cat ~/.openclaw/logs/commands.log | jq .

# Filtrer par action
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

**Voir：** [Documentation command-logger](/automation/hooks#command-logger)

### boot-md

Exécute `BOOT.md` au démarrage de la passerelle Gateway (après le démarrage du canal).

**Événements**：`gateway:startup`

**Activation**：

```bash
openclaw hooks enable boot-md
```

**Voir：** [Documentation boot-md](/automation/hooks#boot-md)
