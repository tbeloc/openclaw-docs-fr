---
read_when:
  - Débogage de scripts de développement Node uniquement ou échec du mode watch
  - Dépannage des plantages du chargeur tsx/esbuild dans OpenClaw
summary: Explication et solution du plantage Node + tsx "__name is not a function"
title: Plantage Node + tsx
x-i18n:
  generated_at: "2026-02-01T20:24:52Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f9e9bd2281508337a0696126b0db2d47a2d0f56de7a11872fbc0ac4689f9ad41
  source_path: debug/node-issue.md
  workflow: 14
---

# Plantage Node + tsx "\_\_name is not a function"

## Aperçu

Lors de l'exécution d'OpenClaw avec `tsx` via Node, une erreur se produit lors de la phase de démarrage :

```
[openclaw] Failed to start CLI: TypeError: __name is not a function
    at createSubsystemLogger (.../src/logging/subsystem.ts:203:25)
    at .../src/agents/auth-profiles/constants.ts:25:20
```

Ce problème est apparu après le passage des scripts de développement de Bun à `tsx` (commit `2871657e`, 2026-01-06). Le même chemin d'exécution fonctionne correctement sous Bun.

## Environnement

- Node : v25.x (observé sur v25.3.0)
- tsx : 4.21.0
- Système d'exploitation : macOS (d'autres plateformes exécutant Node 25 peuvent également reproduire le problème)

## Étapes de reproduction (Node uniquement)

```bash
# À la racine du dépôt
node --version
pnpm install
node --import tsx src/entry.ts status
```

## Reproduction minimale dans le dépôt

```bash
node --import tsx scripts/repro/tsx-name-repro.ts
```

## Vérification des versions de Node

- Node 25.3.0 : échec
- Node 22.22.0 (Homebrew `node@22`) : échec
- Node 24 : pas encore installé, nécessite une vérification

## Explication / Hypothèses

- `tsx` utilise esbuild pour transformer TS/ESM. Le `keepNames` d'esbuild génère une fonction auxiliaire `__name` et enveloppe les définitions de fonction avec `__name(...)`.
- Le plantage indique que `__name` existe mais n'est pas une fonction à l'exécution, ce qui signifie que la fonction auxiliaire est manquante ou écrasée dans le chemin du chargeur de Node 25.
- D'autres utilisateurs d'esbuild ont également signalé des problèmes similaires de fonction auxiliaire `__name` manquante ou réécrite.

## Historique des régressions

- `2871657e` (2026-01-06) : scripts passés de Bun à tsx, rendant Bun optionnel.
- Avant cela (chemin Bun), `openclaw status` et `gateway:watch` fonctionnaient correctement.

## Solutions de contournement

- Utiliser Bun pour les scripts de développement (solution de repli temporaire actuelle).
- Utiliser Node + tsc watch, puis exécuter les artefacts compilés :
  ```bash
  pnpm exec tsc --watch --preserveWatchOutput
  node --watch openclaw.mjs status
  ```
- Confirmé localement : `pnpm exec tsc -p tsconfig.json` + `node openclaw.mjs status` fonctionne correctement sur Node 25.
- Si possible, désactiver keepNames d'esbuild dans le chargeur TS (pour éviter l'insertion de la fonction auxiliaire `__name`) ; tsx ne fournit actuellement pas cette option de configuration.
- Tester `tsx` sur Node LTS (22/24) pour confirmer si ce problème est spécifique à Node 25.

## Références

- https://opennext.js.org/cloudflare/howtos/keep_names
- https://esbuild.github.io/api/#keep-names
- https://github.com/evanw/esbuild/issues/1031

## Prochaines étapes

- Reproduire sur Node 22/24 pour confirmer s'il s'agit d'une régression de Node 25.
- Tester la version nightly de `tsx`, ou épingler à une version antérieure si une régression connue existe.
- Si reproductible sur Node LTS, soumettre une reproduction minimale en amont avec la trace de pile `__name`.
