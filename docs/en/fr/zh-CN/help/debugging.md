---
read_when:
  - Vous devez vérifier la sortie du modèle brut pour rechercher des fuites de raisonnement
  - Vous souhaitez exécuter Gateway en mode surveillance lors de l'itération
  - Vous avez besoin d'un flux de travail de débogage reproductible
summary: Outils de débogage : mode surveillance, flux de modèle brut et traçage des fuites de raisonnement
title: Débogage
x-i18n:
  generated_at: "2026-02-03T07:47:23Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 504c824bff4790006c8b73600daca66b919e049178e9711e6e65b6254731911a
  source_path: help/debugging.md
  workflow: 15
---

# Débogage

Cette page présente les outils de débogage pour la sortie en continu, en particulier lorsque le fournisseur mélange le raisonnement au texte normal.

## Remplacements de débogage à l'exécution

Utilisez `/debug` dans le chat pour définir des remplacements de configuration **à l'exécution uniquement** (en mémoire, non écrits sur le disque).
`/debug` est désactivé par défaut ; activez-le via `commands.debug: true`.
C'est pratique lorsque vous devez basculer des paramètres peu fréquents sans éditer `openclaw.json`.

Exemples :

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
```

`/debug reset` efface tous les remplacements et revient à la configuration sur le disque.

## Mode surveillance de Gateway

Pour une itération rapide, exécutez Gateway sous un observateur de fichiers :

```bash
pnpm gateway:watch --force
```

Cela correspond à :

```bash
tsx watch src/entry.ts gateway --force
```

Ajoutez n'importe quel drapeau CLI de Gateway après `gateway:watch`, et il sera transmis à chaque redémarrage.

## Fichier de configuration dev + Gateway dev (--dev)

Utilisez un fichier de configuration dev pour isoler l'état et lancez une configuration de débogage sécurisée et jetable. Il y a **deux** drapeaux `--dev` :

- **`--dev` global (fichier de configuration) :** Isole l'état sous `~/.openclaw-dev` et définit par défaut le port Gateway à `19001` (les ports dérivés se déplacent en conséquence).
- **`gateway --dev` :** Indique à Gateway de créer automatiquement une configuration par défaut + un espace de travail s'il manque** (et ignore BOOTSTRAP.md).

Flux recommandé (fichier de configuration dev + amorçage dev) :

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

Si vous n'avez pas installé globalement, exécutez l'interface de ligne de commande via `pnpm openclaw ...`.

Cela exécute :

1. **Isolation du profil** (`--dev` global)
   - `OPENCLAW_PROFILE=dev`
   - `OPENCLAW_STATE_DIR=~/.openclaw-dev`
   - `OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`
   - `OPENCLAW_GATEWAY_PORT=19001` (le navigateur/canevas se déplace en conséquence)

2. **Amorçage dev** (`gateway --dev`)
   - Écrit une configuration minimale s'il manque (`gateway.mode=local`, liaison loopback).
   - Définit `agent.workspace` sur l'espace de travail dev.
   - Définit `agent.skipBootstrap=true` (pas de BOOTSTRAP.md).
   - Remplit les fichiers d'espace de travail s'il manque :
     `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`.
   - Identité par défaut : **C3‑PO** (robot de protocole).
   - Ignore les fournisseurs de canaux en mode dev (`OPENCLAW_SKIP_CHANNELS=1`).

Flux de réinitialisation (recommencer à zéro) :

```bash
pnpm gateway:dev:reset
```

Remarque : `--dev` est un drapeau de fichier de configuration **global** qui peut être avalé par certains exécuteurs.
Si vous devez l'épeler explicitement, utilisez la forme de variable d'environnement :

```bash
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

`--reset` efface la configuration, les identifiants, les sessions et l'espace de travail dev (en utilisant `trash`, pas `rm`), puis recrée les paramètres dev par défaut.

Conseil : Si une Gateway non-dev est en cours d'exécution (launchd/systemd), arrêtez-la d'abord :

```bash
openclaw gateway stop
```

## Journaux de flux brut (OpenClaw)

OpenClaw peut enregistrer le **flux d'assistant brut** avant tout filtrage/formatage.
C'est le meilleur moyen de voir si le raisonnement arrive sous forme d'incréments de texte pur (ou sous forme de bloc de pensée séparé).

Activez via l'interface de ligne de commande :

```bash
pnpm gateway:watch --force --raw-stream
```

Remplacement de chemin optionnel :

```bash
pnpm gateway:watch --force --raw-stream --raw-stream-path ~/.openclaw/logs/raw-stream.jsonl
```

Variables d'environnement équivalentes :

```bash
OPENCLAW_RAW_STREAM=1
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl
```

Fichier par défaut :

`~/.openclaw/logs/raw-stream.jsonl`

## Journaux de bloc brut (pi-mono)

Pour capturer les **blocs OpenAI compatibles bruts** avant d'être analysés en blocs, pi-mono expose un enregistreur séparé :

```bash
PI_RAW_STREAM=1
```

Chemin optionnel :

```bash
PI_RAW_STREAM_PATH=~/.pi-mono/logs/raw-openai-completions.jsonl
```

Fichier par défaut :

`~/.pi-mono/logs/raw-openai-completions.jsonl`

> Remarque : Ceci n'est émis que par les processus du fournisseur `openai-completions` utilisant pi-mono.

## Considérations de sécurité

- Les journaux de flux brut peuvent contenir des invites complètes, des sorties d'outils et des données utilisateur.
- Conservez les journaux localement et supprimez-les après le débogage.
- Si vous partagez des journaux, nettoyez d'abord les clés et les informations d'identification personnelle.
