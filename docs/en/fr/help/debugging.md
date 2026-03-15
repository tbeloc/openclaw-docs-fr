---
summary: "Outils de débogage : mode watch, flux de modèle brut et traçage des fuites de raisonnement"
read_when:
  - You need to inspect raw model output for reasoning leakage
  - You want to run the Gateway in watch mode while iterating
  - You need a repeatable debugging workflow
title: "Débogage"
---

# Débogage

Cette page couvre les assistants de débogage pour la sortie en streaming, en particulier lorsqu'un fournisseur mélange le raisonnement au texte normal.

## Remplacements de débogage à l'exécution

Utilisez `/debug` dans le chat pour définir des remplacements de configuration **à l'exécution uniquement** (mémoire, pas disque).
`/debug` est désactivé par défaut ; activez-le avec `commands.debug: true`.
C'est pratique lorsque vous devez basculer des paramètres obscurs sans éditer `openclaw.json`.

Exemples :

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
```

`/debug reset` efface tous les remplacements et revient à la configuration sur disque.

## Mode watch de la passerelle

Pour une itération rapide, exécutez la passerelle sous le observateur de fichiers :

```bash
pnpm gateway:watch
```

Cela correspond à :

```bash
node --watch-path src --watch-path tsconfig.json --watch-path package.json --watch-preserve-output scripts/run-node.mjs gateway --force
```

Ajoutez tous les drapeaux CLI de la passerelle après `gateway:watch` et ils seront transmis à chaque redémarrage.

## Profil dev + passerelle dev (--dev)

Utilisez le profil dev pour isoler l'état et configurer une installation sûre et jetable pour le débogage. Il y a **deux** drapeaux `--dev` :

- **`--dev` global (profil) :** isole l'état sous `~/.openclaw-dev` et définit par défaut le port de la passerelle à `19001` (les ports dérivés se décalent avec lui).
- **`gateway --dev` : indique à la passerelle de créer automatiquement une configuration par défaut + espace de travail** en cas de manque (et ignorer BOOTSTRAP.md).

Flux recommandé (profil dev + bootstrap dev) :

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

Si vous n'avez pas encore d'installation globale, exécutez l'interface de ligne de commande via `pnpm openclaw ...`.

Ce que cela fait :

1. **Isolation du profil** (`--dev` global)
   - `OPENCLAW_PROFILE=dev`
   - `OPENCLAW_STATE_DIR=~/.openclaw-dev`
   - `OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`
   - `OPENCLAW_GATEWAY_PORT=19001` (le navigateur/canvas se décalent en conséquence)

2. **Bootstrap dev** (`gateway --dev`)
   - Écrit une configuration minimale en cas de manque (`gateway.mode=local`, liaison loopback).
   - Définit `agent.workspace` sur l'espace de travail dev.
   - Définit `agent.skipBootstrap=true` (pas de BOOTSTRAP.md).
   - Amorce les fichiers de l'espace de travail en cas de manque :
     `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`.
   - Identité par défaut : **C3‑PO** (droïde de protocole).
   - Ignore les fournisseurs de canaux en mode dev (`OPENCLAW_SKIP_CHANNELS=1`).

Flux de réinitialisation (démarrage à zéro) :

```bash
pnpm gateway:dev:reset
```

Remarque : `--dev` est un drapeau de profil **global** et est consommé par certains exécuteurs.
Si vous devez l'épeler, utilisez la forme de variable d'environnement :

```bash
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

`--reset` efface la configuration, les identifiants, les sessions et l'espace de travail dev (en utilisant `trash`, pas `rm`), puis recrée la configuration dev par défaut.

Conseil : si une passerelle non-dev est déjà en cours d'exécution (launchd/systemd), arrêtez-la d'abord :

```bash
openclaw gateway stop
```

## Journalisation du flux brut (OpenClaw)

OpenClaw peut enregistrer le **flux brut de l'assistant** avant tout filtrage/formatage.
C'est le meilleur moyen de voir si le raisonnement arrive sous forme de deltas de texte brut (ou sous forme de blocs de réflexion séparés).

Activez-le via l'interface de ligne de commande :

```bash
pnpm gateway:watch --raw-stream
```

Remplacement de chemin optionnel :

```bash
pnpm gateway:watch --raw-stream --raw-stream-path ~/.openclaw/logs/raw-stream.jsonl
```

Variables d'environnement équivalentes :

```bash
OPENCLAW_RAW_STREAM=1
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl
```

Fichier par défaut :

`~/.openclaw/logs/raw-stream.jsonl`

## Journalisation des chunks bruts (pi-mono)

Pour capturer les **chunks OpenAI-compat bruts** avant qu'ils ne soient analysés en blocs, pi-mono expose un enregistreur séparé :

```bash
PI_RAW_STREAM=1
```

Chemin optionnel :

```bash
PI_RAW_STREAM_PATH=~/.pi-mono/logs/raw-openai-completions.jsonl
```

Fichier par défaut :

`~/.pi-mono/logs/raw-openai-completions.jsonl`

> Remarque : ceci n'est émis que par les processus utilisant le fournisseur `openai-completions` de pi-mono.

## Notes de sécurité

- Les journaux de flux bruts peuvent inclure des invites complètes, une sortie d'outil et des données utilisateur.
- Conservez les journaux localement et supprimez-les après le débogage.
- Si vous partagez des journaux, nettoyez d'abord les secrets et les informations personnelles.
