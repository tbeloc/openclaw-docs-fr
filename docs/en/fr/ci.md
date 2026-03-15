---
title: Pipeline CI
description: Comment fonctionne le pipeline CI d'OpenClaw
summary: "Graphique des tâches CI, portes de portée et équivalents de commandes locales"
read_when:
  - You need to understand why a CI job did or did not run
  - You are debugging failing GitHub Actions checks
---

# Pipeline CI

Le CI s'exécute à chaque push vers `main` et à chaque pull request. Il utilise une portée intelligente pour ignorer les tâches coûteuses lorsque seules des zones non liées ont changé.

## Aperçu des tâches

| Tâche             | Objectif                                                | Quand elle s'exécute               |
| ----------------- | ------------------------------------------------------- | ---------------------------------- |
| `docs-scope`      | Détecter les modifications limitées à la documentation  | Toujours                           |
| `changed-scope`   | Détecter les zones modifiées (node/macos/android/windows) | Modifications non-doc              |
| `check`           | Types TypeScript, lint, format                          | Non-docs, modifications node       |
| `check-docs`      | Lint Markdown + vérification des liens cassés            | Documentation modifiée             |
| `secrets`         | Détecter les secrets divulgués                          | Toujours                           |
| `build-artifacts` | Construire dist une fois, partager avec `release-check` | Pushes vers `main`, modifications node |
| `release-check`   | Valider le contenu du pack npm                          | Pushes vers `main` après la construction |
| `checks`          | Tests Node + vérification du protocole sur les PRs ; compatibilité Bun sur push | Non-docs, modifications node |
| `compat-node22`   | Compatibilité du runtime Node minimum supporté          | Pushes vers `main`, modifications node |
| `checks-windows`  | Tests spécifiques à Windows                             | Non-docs, modifications pertinentes à windows |
| `macos`           | Lint/build/test Swift + tests TS                        | PRs avec modifications macos       |
| `android`         | Build Gradle + tests                                    | Non-docs, modifications android    |

## Ordre de défaillance rapide

Les tâches sont ordonnées pour que les vérifications bon marché échouent avant que les tâches coûteuses ne s'exécutent :

1. `docs-scope` + `changed-scope` + `check` + `secrets` (parallèle, portes bon marché en premier)
2. PRs : `checks` (test Node Linux divisé en 2 shards), `checks-windows`, `macos`, `android`
3. Pushes vers `main` : `build-artifacts` + `release-check` + compatibilité Bun + `compat-node22`

La logique de portée se trouve dans `scripts/ci-changed-scope.mjs` et est couverte par des tests unitaires dans `src/scripts/ci-changed-scope.test.ts`.

## Exécuteurs

| Exécuteur                        | Tâches                                     |
| -------------------------------- | ------------------------------------------ |
| `blacksmith-16vcpu-ubuntu-2404`  | La plupart des tâches Linux, y compris la détection de portée |
| `blacksmith-32vcpu-windows-2025` | `checks-windows`                           |
| `macos-latest`                   | `macos`, `ios`                             |

## Équivalents locaux

```bash
pnpm check          # types + lint + format
pnpm test           # vitest tests
pnpm check:docs     # docs format + lint + broken links
pnpm release:check  # validate npm pack
```
