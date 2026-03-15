---
summary: "Référence CLI pour `openclaw hooks` (hooks d'agent)"
read_when:
  - You want to manage agent hooks
  - You want to install or update hooks
title: "hooks"
---

# `openclaw hooks`

Gérez les hooks d'agent (automations pilotées par événements pour des commandes comme `/new`, `/reset` et le démarrage de la passerelle).

Connexes :

- Hooks : [Hooks](/automation/hooks)
- Hooks de plugin : [Plugins](/tools/plugin#plugin-hooks)

## Lister tous les hooks

```bash
openclaw hooks list
```

Listez tous les hooks découverts à partir des répertoires workspace, managed et bundled.

**Options :**

- `--eligible` : Afficher uniquement les hooks éligibles (conditions remplies)
- `--json` : Sortie au format JSON
- `-v, --verbose` : Afficher les informations détaillées, y compris les conditions manquantes

**Exemple de sortie :**

```
Hooks (4/4 ready)

Ready:
  🚀 boot-md ✓ - Run BOOT.md on gateway startup
  📎 bootstrap-extra-files ✓ - Inject extra workspace bootstrap files during agent bootstrap
  📝 command-logger ✓ - Log all command events to a centralized audit file
  💾 session-memory ✓ - Save session context to memory when /new command is issued
```

**Exemple (verbose) :**

```bash
openclaw hooks list --verbose
```

Affiche les conditions manquantes pour les hooks non éligibles.

**Exemple (JSON) :**

```bash
openclaw hooks list --json
```

Retourne du JSON structuré pour une utilisation programmatique.

## Obtenir les informations d'un hook

```bash
openclaw hooks info <name>
```

Affiche les informations détaillées sur un hook spécifique.

**Arguments :**

- `<name>` : Nom du hook (par exemple, `session-memory`)

**Options :**

- `--json` : Sortie au format JSON

**Exemple :**

```bash
openclaw hooks info session-memory
```

**Sortie :**

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

## Vérifier l'éligibilité des hooks

```bash
openclaw hooks check
```

Affiche un résumé du statut d'éligibilité des hooks (combien sont prêts vs. non prêts).

**Options :**

- `--json` : Sortie au format JSON

**Exemple de sortie :**

```
Hooks Status

Total hooks: 4
Ready: 4
Not ready: 0
```

## Activer un hook

```bash
openclaw hooks enable <name>
```

Activez un hook spécifique en l'ajoutant à votre configuration (`~/.openclaw/config.json`).

**Remarque :** Les hooks gérés par des plugins affichent `plugin:<id>` dans `openclaw hooks list` et
ne peuvent pas être activés/désactivés ici. Activez/désactivez le plugin à la place.

**Arguments :**

- `<name>` : Nom du hook (par exemple, `session-memory`)

**Exemple :**

```bash
openclaw hooks enable session-memory
```

**Sortie :**

```
✓ Enabled hook: 💾 session-memory
```

**Ce qu'il fait :**

- Vérifie si le hook existe et est éligible
- Met à jour `hooks.internal.entries.<name>.enabled = true` dans votre configuration
- Enregistre la configuration sur le disque

**Après activation :**

- Redémarrez la passerelle pour que les hooks se rechargent (redémarrage de l'application de la barre de menu sur macOS, ou redémarrage de votre processus de passerelle en dev).

## Désactiver un hook

```bash
openclaw hooks disable <name>
```

Désactivez un hook spécifique en mettant à jour votre configuration.

**Arguments :**

- `<name>` : Nom du hook (par exemple, `command-logger`)

**Exemple :**

```bash
openclaw hooks disable command-logger
```

**Sortie :**

```
⏸ Disabled hook: 📝 command-logger
```

**Après désactivation :**

- Redémarrez la passerelle pour que les hooks se rechargent

## Installer des hooks

```bash
openclaw hooks install <path-or-spec>
openclaw hooks install <npm-spec> --pin
```

Installez un pack de hooks à partir d'un dossier/archive local ou npm.

Les spécifications npm sont **registry-only** (nom du package + version **exacte** optionnelle ou
**dist-tag**). Les spécifications Git/URL/fichier et les plages semver sont rejetées. Les installations de dépendances s'exécutent avec `--ignore-scripts` pour la sécurité.

Les spécifications nues et `@latest` restent sur la piste stable. Si npm résout l'une ou l'autre
à une préversion, OpenClaw s'arrête et vous demande d'opter explicitement avec une
balise de préversion telle que `@beta`/`@rc` ou une version de préversion exacte.

**Ce qu'il fait :**

- Copie le pack de hooks dans `~/.openclaw/hooks/<id>`
- Active les hooks installés dans `hooks.internal.entries.*`
- Enregistre l'installation sous `hooks.internal.installs`

**Options :**

- `-l, --link` : Liez un répertoire local au lieu de le copier (l'ajoute à `hooks.internal.load.extraDirs`)
- `--pin` : Enregistrez les installations npm comme `name@version` exacte résolu dans `hooks.internal.installs`

**Archives supportées :** `.zip`, `.tgz`, `.tar.gz`, `.tar`

**Exemples :**

```bash
# Local directory
openclaw hooks install ./my-hook-pack

# Local archive
openclaw hooks install ./my-hook-pack.zip

# NPM package
openclaw hooks install @openclaw/my-hook-pack

# Link a local directory without copying
openclaw hooks install -l ./my-hook-pack
```

## Mettre à jour les hooks

```bash
openclaw hooks update <id>
openclaw hooks update --all
```

Mettez à jour les packs de hooks installés (installations npm uniquement).

**Options :**

- `--all` : Mettre à jour tous les packs de hooks suivis
- `--dry-run` : Afficher ce qui changerait sans écrire

Lorsqu'un hash d'intégrité stocké existe et que le hash d'artefact récupéré change,
OpenClaw affiche un avertissement et demande une confirmation avant de continuer. Utilisez
le global `--yes` pour contourner les invites dans les exécutions CI/non-interactives.

## Hooks groupés

### session-memory

Enregistre le contexte de session en mémoire lorsque vous émettez `/new`.

**Activer :**

```bash
openclaw hooks enable session-memory
```

**Sortie :** `~/.openclaw/workspace/memory/YYYY-MM-DD-slug.md`

**Voir :** [documentation session-memory](/automation/hooks#session-memory)

### bootstrap-extra-files

Injecte des fichiers bootstrap supplémentaires (par exemple, `AGENTS.md` / `TOOLS.md` locaux au monorepo) pendant `agent:bootstrap`.

**Activer :**

```bash
openclaw hooks enable bootstrap-extra-files
```

**Voir :** [documentation bootstrap-extra-files](/automation/hooks#bootstrap-extra-files)

### command-logger

Enregistre tous les événements de commande dans un fichier d'audit centralisé.

**Activer :**

```bash
openclaw hooks enable command-logger
```

**Sortie :** `~/.openclaw/logs/commands.log`

**Afficher les journaux :**

```bash
# Recent commands
tail -n 20 ~/.openclaw/logs/commands.log

# Pretty-print
cat ~/.openclaw/logs/commands.log | jq .

# Filter by action
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

**Voir :** [documentation command-logger](/automation/hooks#command-logger)

### boot-md

Exécute `BOOT.md` au démarrage de la passerelle (après le démarrage des canaux).

**Événements** : `gateway:startup`

**Activer** :

```bash
openclaw hooks enable boot-md
```

**Voir :** [documentation boot-md](/automation/hooks#boot-md)
