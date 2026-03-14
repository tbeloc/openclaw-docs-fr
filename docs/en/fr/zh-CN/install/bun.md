---
read_when:
  - Vous voulez la boucle de développement local la plus rapide (bun + watch)
  - Vous rencontrez des problèmes d'installation/patch/scripts de cycle de vie Bun
summary: Flux de travail Bun (expérimental) : installation et considérations par rapport à pnpm
title: Bun (expérimental)
x-i18n:
  generated_at: "2026-02-03T07:49:24Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: eb3f4c222b6bae49938d8bf53a0818fe5f5e0c0c3c1adb3e0a832ce8f785e1e3
  source_path: install/bun.md
  workflow: 15
---

# Bun (expérimental)

Objectif : Exécuter ce dépôt avec **Bun** (optionnel, non recommandé pour WhatsApp/Telegram), tout en restant aligné avec le flux de travail pnpm.

⚠️ **Non recommandé pour l'exécution de Gateway** (bugs avec WhatsApp/Telegram). Utilisez Node pour la production.

## Statut

- Bun est un runtime local optionnel pour exécuter directement TypeScript (`bun run …`, `bun --watch …`).
- `pnpm` est l'outil par défaut pour la construction et reste entièrement supporté (et utilisé par certains outils de documentation).
- Bun ne peut pas utiliser `pnpm-lock.yaml` et l'ignorera.

## Installation

Par défaut :

```sh
bun install
```

Remarque : `bun.lock`/`bun.lockb` sont dans gitignore, donc il n'y aura pas de changements de dépôt de toute façon. Si vous voulez *ne pas écrire le fichier de verrouillage* :

```sh
bun install --no-save
```

## Construction/Tests (Bun)

```sh
bun run build
bun run vitest run
```

## Scripts de cycle de vie Bun (bloqués par défaut)

À moins d'être explicitement approuvés (`bun pm untrusted` / `bun pm trust`), Bun peut bloquer les scripts de cycle de vie des dépendances.
Pour ce dépôt, les scripts généralement bloqués ne sont généralement pas nécessaires :

- `@whiskeysockets/baileys` `preinstall` : vérifie que la version majeure de Node >= 20 (nous exécutons Node 22+).
- `protobufjs` `postinstall` : émet un avertissement sur un schéma de versioning incompatible (pas d'artefacts de construction).

Si vous rencontrez des problèmes d'exécution qui nécessitent réellement ces scripts, approuvez-les explicitement :

```sh
bun pm trust @whiskeysockets/baileys protobufjs
```

## Considérations

- Certains scripts sont toujours codés en dur pour pnpm (par exemple `docs:build`, `ui:*`, `protocol:check`). Pour l'instant, exécutez ces scripts via pnpm.
