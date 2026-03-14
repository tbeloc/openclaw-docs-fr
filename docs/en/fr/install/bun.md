---
summary: "Flux de travail Bun (expérimental) : installations et pièges par rapport à pnpm"
read_when:
  - Vous voulez la boucle de développement local la plus rapide (bun + watch)
  - Vous rencontrez des problèmes d'installation/patch/scripts de cycle de vie Bun
title: "Bun (Expérimental)"
---

# Bun (expérimental)

Objectif : exécuter ce dépôt avec **Bun** (optionnel, non recommandé pour WhatsApp/Telegram)
sans diverger des flux de travail pnpm.

⚠️ **Non recommandé pour le runtime Gateway** (bugs WhatsApp/Telegram). Utilisez Node pour la production.

## Statut

- Bun est un runtime local optionnel pour exécuter TypeScript directement (`bun run …`, `bun --watch …`).
- `pnpm` est le défaut pour les builds et reste entièrement supporté (et utilisé par certains outils de documentation).
- Bun ne peut pas utiliser `pnpm-lock.yaml` et l'ignorera.

## Installation

Par défaut :

```sh
bun install
```

Remarque : `bun.lock`/`bun.lockb` sont gitignorés, donc il n'y a pas de churn de dépôt de toute façon. Si vous voulez _aucune écriture de fichier de verrouillage_ :

```sh
bun install --no-save
```

## Build / Test (Bun)

```sh
bun run build
bun run vitest run
```

## Scripts de cycle de vie Bun (bloqués par défaut)

Bun peut bloquer les scripts de cycle de vie des dépendances sauf s'ils sont explicitement approuvés (`bun pm untrusted` / `bun pm trust`).
Pour ce dépôt, les scripts couramment bloqués ne sont pas requis :

- `@whiskeysockets/baileys` `preinstall` : vérifie que la version majeure de Node >= 20 (OpenClaw utilise par défaut Node 24 et supporte toujours Node 22 LTS, actuellement `22.16+`).
- `protobufjs` `postinstall` : émet des avertissements sur les schémas de version incompatibles (pas d'artefacts de build).

Si vous rencontrez un vrai problème d'exécution qui nécessite ces scripts, approuvez-les explicitement :

```sh
bun pm trust @whiskeysockets/baileys protobufjs
```

## Mises en garde

- Certains scripts codent toujours en dur pnpm (par exemple `docs:build`, `ui:*`, `protocol:check`). Exécutez-les via pnpm pour l'instant.
