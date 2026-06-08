---
title: "Chemin d'installation Nix - Note de maturité UX du mode Nix sur macOS"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Chemin d'installation Nix - Note de maturité UX du mode Nix sur macOS

## Résumé

L'application macOS présente un comportement concret du mode Nix : paramètres par défaut de suite stable, saut de l'intégration, désactivation de la sauvegarde de configuration et une bannière visible « géré par Nix ». C'est un signal fort de qualité source pour le côté GUI du chemin d'installation Nix, mais la preuve s'arrête avant un `.app` installé lancé à partir d'un profil Nix/Home Manager.

## Portée de la catégorie

Cette catégorie couvre la gestion par défaut de `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention des écritures de configuration locale.

## Fonctionnalités

- Paramètres par défaut Nix stables : Couvre les paramètres par défaut Nix stables dans la gestion par défaut de `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention des écritures de configuration locale.
- Bannière « géré par Nix » : Couvre la bannière « géré par Nix » dans la gestion par défaut de `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention des écritures de configuration locale.
- Contrôles de configuration en lecture seule : Couvre les contrôles de configuration en lecture seule dans la gestion par défaut de `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention des écritures de configuration locale.
- Saut de l'intégration : Couvre le saut de l'intégration dans la gestion par défaut de `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention des écritures de configuration locale.

## Fraîcheur des archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Expérimental (45%)`
- Signaux positifs : Les tests Swift couvrent la détection du mode Nix de suite stable, et la source montre que les paramètres/l'intégration/les écritures de configuration répondent au mode Nix.
- Signaux négatifs : Aucune preuve e2e d'application macOS installée ne prouve que les paramètres par défaut écrits par une configuration Nix-gérée launchd/Home Manager sont lus par le bundle d'application livré.
- Lacunes d'intégration : Aucune preuve d'automatisation d'interface utilisateur/capture d'écran n'a été trouvée pour la bannière Nix ou le contrôle de sauvegarde désactivé dans une installation Nix réelle.

## Score de qualité

- Score : `Alpha (50%)`
- Rapports Gitcrawl : `Managed by Nix` et `Nix mode banner` n'ont retourné aucun résultat GitHub ciblé, ce qui est neutre après les vérifications de fraîcheur.
- Rapports Discrawl : Une réponse Discord de mars 2026 note que la documentation peut utiliser « banner » pour signifier un indice d'interface utilisateur en mode lecture seule pour Nix, montrant que la terminologie orientée opérateur existe mais n'est pas fortement soutenue par les problèmes.
- Bonnes qualités : L'application gère explicitement l'héritage d'environnement GUI, utilise une suite de paramètres par défaut stables pour survivre à la rotation des identifiants de bundle, désactive les sauvegardes de configuration et affiche les chemins de configuration/état dans la bannière.
- Mauvaises qualités : Ce comportement est spécifique à macOS et dépend toujours de l'empaquetage externe écrivant correctement les paramètres par défaut dans la suite attendue.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'ont pas été utilisées pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Expérimental (45%)`
- Instructions de surface : évaluées par rapport à `references/completeness/nix-install-path.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les paramètres par défaut Nix stables, la bannière « géré par Nix », les contrôles de configuration en lecture seule, le saut de l'intégration.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aucune preuve d'application installée à partir d'un bundle `.app` construit avec Nix.
- La documentation dit « L'interface utilisateur affiche une bannière de mode Nix en lecture seule », mais la preuve locale est au niveau source plutôt que soutenue par des captures d'écran.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/install/nix.md:61` à `:64` documente la commande defaults de macOS.
- `/Users/kevinlin/code/openclaw/docs/install/nix.md:73` dit que l'interface utilisateur affiche une bannière de mode Nix en lecture seule.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ProcessInfo+OpenClaw.swift:8` à `:23` résout le mode Nix à partir de l'env, des paramètres par défaut standard et de la suite stable.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/Onboarding.swift:31` à `:34` ignore l'intégration en mode Nix.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ConfigSettings.swift:167` à `:168` affiche le texte en lecture seule en mode Nix.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ConfigSettings.swift:196` à `:197` désactive le bouton Enregistrer en mode Nix.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/OpenClawConfigFile.swift:64` empêche les écritures de configuration en mode Nix de production.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/SettingsRootView.swift:104` à `:151` affiche une bannière `Managed by Nix` avec les chemins de configuration et d'état.

### Tests d'intégration

- Aucune preuve d'application installée, de capture d'écran ou d'intégration Home Manager launchd n'a été trouvée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/NixModeStableSuiteTests.swift:6` à `:39` vérifie le comportement de suite stable pour les bundles d'application et les contextes non-application.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/ConfigStoreTests.swift:73` à `:135` couvre le comportement du magasin de configuration avec des chemins de configuration explicites.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "Managed by Nix" --json`

Résultats :

- A retourné `hits: []`.

Requête :

`gitcrawl search openclaw/openclaw --query "Nix mode banner" --json`

Résultats :

- A retourné `hits: []`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Managed by Nix"`

Résultats :

- A retourné un message large de déploiements de chemin doré sur les documents gérés par Nix ; aucun problème d'interface utilisateur d'application macOS ciblé.

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "Nix mode banner"`

Résultats :

- A retourné une réponse d'assistance du 2026-03-03 clarifiant que la documentation peut utiliser « banner » pour signifier un indice d'interface utilisateur tel que le mode lecture seule pour Nix.
