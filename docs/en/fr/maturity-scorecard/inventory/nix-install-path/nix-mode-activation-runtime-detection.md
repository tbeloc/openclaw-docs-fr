---
title: "Chemin d'installation Nix - Note de maturité de l'activation et de l'UX de l'application"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin d'installation Nix - Note de maturité de l'activation et de l'UX de l'application

## Résumé

OpenClaw dispose d'un contrat d'activation simple et bien documenté : `OPENCLAW_NIX_MODE=1` pour les chemins Node/gateway et `openclaw.nixMode` par défaut pour l'application macOS. L'implémentation est volontairement étroite et facile à comprendre, mais la preuve est principalement au niveau unitaire et au niveau source plutôt qu'une preuve complète du runtime Nix installé.

## Portée de la catégorie

Inclus dans cette catégorie :

- Activation de l'environnement : Couvre l'activation de l'environnement sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS, et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Activation des paramètres par défaut macOS : Couvre l'activation des paramètres par défaut macOS sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS, et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Détection du mode Nix à l'exécution : Couvre la détection du mode Nix à l'exécution sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS, et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Paramètres par défaut Nix stables : Couvre les paramètres par défaut Nix stables sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement d'intégration, et la prévention de l'écriture de configuration locale.
- Bannière Managed-by-Nix : Couvre la bannière Managed-by-Nix sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement d'intégration, et la prévention de l'écriture de configuration locale.
- Contrôles de configuration en lecture seule : Couvre les contrôles de configuration en lecture seule sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement d'intégration, et la prévention de l'écriture de configuration locale.
- Saut d'intégration : Couvre le saut d'intégration sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement d'intégration, et la prévention de l'écriture de configuration locale.

## Fonctionnalités

- Activation de l'environnement : Couvre l'activation de l'environnement sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS, et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Activation des paramètres par défaut macOS : Couvre l'activation des paramètres par défaut macOS sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS, et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Détection du mode Nix à l'exécution : Couvre la détection du mode Nix à l'exécution sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS, et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Paramètres par défaut Nix stables : Couvre les paramètres par défaut Nix stables sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement d'intégration, et la prévention de l'écriture de configuration locale.
- Bannière Managed-by-Nix : Couvre la bannière Managed-by-Nix sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement d'intégration, et la prévention de l'écriture de configuration locale.
- Contrôles de configuration en lecture seule : Couvre les contrôles de configuration en lecture seule sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement d'intégration, et la prévention de l'écriture de configuration locale.
- Saut d'intégration : Couvre le saut d'intégration sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement d'intégration, et la prévention de l'écriture de configuration locale.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (42%)`
- Signaux positifs : Les tests source et Swift couvrent les chemins exacts de détection env/paramètres par défaut, y compris la suite stable des paramètres par défaut macOS.
- Signaux négatifs : La couverture n'inclut pas un processus gateway/app réel construit avec Nix prouvant que l'environnement/les paramètres par défaut sont fournis correctement par Home Manager ou NixOS.
- Lacunes d'intégration : Aucun e2e launchd/systemd/Home Manager n'a été trouvé qui démarre OpenClaw en mode Nix et observe le comportement protégé en aval.

## Score de qualité

- Score : `Alpha (52%)`
- Rapports Gitcrawl : Les recherches exactes `OPENCLAW_NIX_MODE` et `openclaw.nixMode` n'ont retourné aucun résultat GitHub ciblé, ce qui est neutre après les vérifications de fraîcheur.
- Rapports Discrawl : Un fil de février `nix-openclaw Gateway start blocked` incluait une unité systemd avec `OPENCLAW_NIX_MODE=1`, le chemin de configuration, et le répertoire d'état, montrant l'utilisation réelle de l'opérateur et l'investigation des défaillances.
- Bonnes qualités : La détection Node est intentionnellement stricte (`OPENCLAW_NIX_MODE === "1"`), et macOS résout à la fois l'env du processus et les paramètres par défaut sans dépendre de l'héritage du shell.
- Mauvaises qualités : Le contrat d'activation est divisé entre les variables d'environnement et les paramètres par défaut macOS, et les rapports actuels de l'opérateur montrent que l'activation correcte seule ne rend pas le chemin d'installation fluide.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct, et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Expérimental (42%)`
- Instructions de surface : évaluées par rapport à `references/completeness/nix-install-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl, et Discrawl couvrent la portée de la taxonomie pour l'activation de l'environnement, l'activation des paramètres par défaut macOS, la détection du mode Nix à l'exécution, les paramètres par défaut Nix stables, la bannière Managed-by-Nix, les contrôles de configuration en lecture seule, le saut d'intégration.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune fixture Nix locale ne prouve que `nix-openclaw` définit l'env/les paramètres par défaut attendus dans chaque forme de service prise en charge.
- Le chemin des paramètres par défaut macOS nécessite une sensibilisation de l'opérateur car les applications GUI n'héritent pas de l'env du shell.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/install/nix.md:53` dit que `OPENCLAW_NIX_MODE=1` est automatique avec `nix-openclaw`.
- `/Users/kevinlin/code/openclaw/docs/install/nix.md:58` documente `export OPENCLAW_NIX_MODE=1` manuel.
- `/Users/kevinlin/code/openclaw/docs/install/nix.md:61` à `:64` documente `defaults write ai.openclaw.mac openclaw.nixMode -bool true` pour l'activation de l'interface graphique macOS.

### Source

- `/Users/kevinlin/code/openclaw/src/config/paths.ts:9` à `:16` définissent le mode Nix comme `OPENCLAW_NIX_MODE === "1"` et documentent son comportement prévu.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ProcessInfo+OpenClaw.swift:8` à `:23` résout le mode Nix à partir de `OPENCLAW_NIX_MODE`, `UserDefaults.standard`, et la suite stable `ai.openclaw.mac` pour les bundles d'application.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ProcessInfo+OpenClaw.swift:27` à `:34` câble ce résolveur dans `ProcessInfo.processInfo.isNixMode`.

### Tests d'intégration

- Aucun e2e d'activation Nix réellement installé n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/config/config.nix-integration-u3-u5-u9.test.ts:24` à `:38` vérifie le comportement faux/vrai pour `OPENCLAW_NIX_MODE`.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/NixModeStableSuiteTests.swift:6` à `:24` vérifie que la suite des paramètres par défaut stables est honorée pour les bundles d'application.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/NixModeStableSuiteTests.swift:26` à `:39` vérifie que la suite stable est ignorée en dehors des bundles d'application.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "OPENCLAW_NIX_MODE" --json`

Résultats :

- A retourné `hits: []`.

Requête :

`gitcrawl search openclaw/openclaw --query "openclaw.nixMode" --json`

Résultats :

- A retourné `hits: []`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "OPENCLAW_NIX_MODE"`

Résultats :

- `nix-openclaw Gateway start blocked` le 2026-02-05 incluait un service systemd avec `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, et `OPENCLAW_NIX_MODE=1`.
- Un message du responsable le 2026-05-08 décrivait les changements de politique pour les plugins npm à l'intérieur des installations déclaratives protégées par des variables d'environnement.
