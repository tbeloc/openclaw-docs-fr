---
title: Pipeline CI
description: Comment fonctionne le pipeline CI d'OpenClaw
summary: "Graphique des jobs CI, portes de portée et équivalents de commandes locales"
read_when:
  - Vous devez comprendre pourquoi un job CI a ou n'a pas été exécuté
  - Vous déboguez des vérifications GitHub Actions défaillantes
---

# Pipeline CI

Le CI s'exécute à chaque push vers `main` et à chaque pull request. Il utilise une portée intelligente pour ignorer les jobs coûteux lorsque seule la documentation ou le code natif a changé.

## Aperçu des Jobs

| Job               | Objectif                                            | Quand il s'exécute                                |
| ----------------- | --------------------------------------------------- | ------------------------------------------------- |
| `docs-scope`      | Détecter les changements de documentation uniquement | Toujours                                          |
| `changed-scope`   | Détecter les zones modifiées (node/macos/android/windows) | PRs non-docs                                      |
| `check`           | Types TypeScript, lint, format                      | Push vers `main`, ou PRs avec changements Node   |
| `check-docs`      | Lint Markdown + vérification des liens cassés       | Changements de docs                               |
| `code-analysis`   | Vérification du seuil LOC (1000 lignes)            | PRs uniquement                                    |
| `secrets`         | Détecter les secrets divulgués                      | Toujours                                          |
| `build-artifacts` | Construire dist une fois, partager avec d'autres jobs | Changements non-docs, node                        |
| `release-check`   | Valider le contenu du pack npm                      | Après la construction                             |
| `checks`          | Tests Node/Bun + vérification du protocole         | Changements non-docs, node                        |
| `checks-windows`  | Tests spécifiques à Windows                         | Changements non-docs, windows                     |
| `macos`           | Lint/build/test Swift + tests TS                    | PRs avec changements macos                        |
| `android`         | Build Gradle + tests                                | Changements non-docs, android                     |

## Ordre de Fail-Fast

Les jobs sont ordonnés pour que les vérifications bon marché échouent avant que les jobs coûteux ne s'exécutent :

1. `docs-scope` + `code-analysis` + `check` (parallèle, ~1-2 min)
2. `build-artifacts` (bloqué par les précédents)
3. `checks`, `checks-windows`, `macos`, `android` (bloqués par la construction)

La logique de portée se trouve dans `scripts/ci-changed-scope.mjs` et est couverte par des tests unitaires dans `src/scripts/ci-changed-scope.test.ts`.

## Runners

| Runner                           | Jobs                                       |
| -------------------------------- | ------------------------------------------ |
| `blacksmith-16vcpu-ubuntu-2404`  | La plupart des jobs Linux, y compris la détection de portée |
| `blacksmith-32vcpu-windows-2025` | `checks-windows`                           |
| `macos-latest`                   | `macos`, `ios`                             |

## Équivalents Locaux

```bash
pnpm check          # types + lint + format
pnpm test           # tests vitest
pnpm check:docs     # format docs + lint + liens cassés
pnpm release:check  # valider le pack npm
```
