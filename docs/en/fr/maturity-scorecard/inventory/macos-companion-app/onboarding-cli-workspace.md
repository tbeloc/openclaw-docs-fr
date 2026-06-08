---
title: "Application compagne macOS - Note de Maturité de Configuration Locale"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagne macOS - Note de Maturité de Configuration Locale

## Résumé

Le chemin de première exécution est implémenté comme une fenêtre d'intégration native avec sélection de page locale/distante, configuration des permissions, installation de CLI, démarrage de l'assistant Gateway, sélection de l'espace de travail et isolation du chat d'intégration. La couverture est Bêta car le flux natif est implémenté avec des vérifications de smoke et d'empaquetage de support, mais l'audit n'a pas trouvé de scénario d'installation d'application macOS sur machine vierge reproductible qui prouve l'installation, les permissions, le démarrage de Gateway, un tour de chat et la configuration de l'espace de travail ensemble. La qualité est Bêta : l'UX est large et bien documentée, tandis que les preuves d'archive montrent toujours une dérive d'intégration/configuration et des responsables demandant un smoke de bêta d'installation vierge.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Attachement/démarrage/arrêt du Gateway en mode local : Comportement, statut et vérification visible par l'opérateur du Gateway en mode local.
- Installation/mise à jour/redémarrage/désinstallation de LaunchAgent : Installation/mise à jour/redémarrage/désinstallation de LaunchAgent via des appels CLI gérés par l'application
- Détection d'écouteur existant : Détection d'écouteur existant, protection des ports et chemin du journal launchd
- Flux d'intégration native de première exécution : Flux d'intégration native de première exécution et marqueur d'achèvement
- Découverte de CLI : Découverte de CLI et chemin d'invite/installation « Installer CLI »
- Sélection de l'espace de travail local : Sélection de l'espace de travail local et démarrage de l'assistant Gateway
- Séparation de la session WebChat d'intégration : Comportement, statut et vérification visible par l'opérateur de la séparation de la session WebChat d'intégration.

## Fonctionnalités

- Attachement/démarrage/arrêt du Gateway en mode local : Comportement, statut et vérification visible par l'opérateur du Gateway en mode local.
- Installation/mise à jour/redémarrage/désinstallation de LaunchAgent : Installation/mise à jour/redémarrage/désinstallation de LaunchAgent via des appels CLI gérés par l'application
- Détection d'écouteur existant : Détection d'écouteur existant, protection des ports et chemin du journal launchd
- Flux d'intégration native de première exécution : Flux d'intégration native de première exécution et marqueur d'achèvement
- Découverte de CLI : Découverte de CLI et chemin d'invite/installation « Installer CLI »
- Sélection de l'espace de travail local : Sélection de l'espace de travail local et démarrage de l'assistant Gateway
- Séparation de la session WebChat d'intégration : Comportement, statut et vérification visible par l'opérateur de la séparation de la session WebChat d'intégration.

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Bêta (72%)`
- Signaux positifs : La source inclut l'ordre des pages d'intégration native, la branchement local/distant, le démarrage de l'assistant Gateway, l'isolation de la session de chat d'intégration, la détection de CLI et l'installation de CLI. Les tests Swift exercent les pages d'intégration et les vues de l'assistant. Les tests d'empaquetage couvrent le comportement du bundle/script d'installation macOS.
- Signaux négatifs : Les tests disponibles sont principalement des vérifications unitaires, smoke et de scripts d'empaquetage. Ils ne prouvent pas le scénario candidat complet d'une application fraîchement installée à travers les permissions, l'attachement du Gateway local, `system.run`, la capture d'écran et la livraison de messages.
- Lacunes d'intégration : Manque un smoke de version macOS d'installation vierge durable qui installe l'application, accorde les invites TCC, installe CLI depuis l'application, démarre/attache Gateway, écrit la configuration de l'espace de travail et envoie un tour de chat d'intégration.

## Score de Qualité

- Score : `Bêta (72%)`
- Rapports Gitcrawl : Les résultats de requête incluent la PR #47263 pour améliorer l'UX d'intégration macOS et la configuration de gateway, la question #65345 pour l'alignement docs/code sur les config/APIs/intégration, et la PR #87255 pour un bug de chemin de config impliquant les écritures d'intégration.
- Rapports Discrawl : La discussion de version demande un smoke d'installation vierge humaine sur macOS, et les notes de version appellent le durcissement d'installation/mise à jour plutôt qu'une preuve d'installation d'application établie.
- Bonnes qualités : Le flux d'intégration est conscient du mode, évite la configuration interactive en mode Nix, isole le chat d'intégration, redémarre les sessions d'assistant perdues une fois, et donne une invite CLI post-intégration uniquement quand le mode local en a besoin.
- Mauvaises qualités : La source et les docs diffèrent sur les noms d'hôte d'installation (`openclaw.bot/install-cli.sh` dans la source par rapport aux docs d'installation publics sous `openclaw.ai`), et les preuves d'archive montrent que l'alignement configuration/intégration reste actif.
- Exclu de la qualité : La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la Qualité.

## Score de Complétude

- Score : `Bêta (72%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves docs archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'attachement/démarrage/arrêt du Gateway en mode local, l'installation/mise à jour/redémarrage/désinstallation de LaunchAgent, la détection d'écouteur existant, le flux d'intégration native de première exécution, la découverte de CLI, la sélection de l'espace de travail local, la séparation de la session WebChat d'intégration.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Besoin d'un scénario d'application vierge documenté qui exécute le flux de première exécution complet par rapport à un vrai bundle d'application signé.
- Besoin d'un meilleur alignement docs/source autour de l'URL d'installation de CLI pilotée par l'application et du repli attendu du gestionnaire de paquets.
- Besoin d'une vue « qu'est-ce qui a échoué » orientée opérateur pour l'installation de CLI, l'assistant, le chemin de l'espace de travail et les défaillances d'attachement du Gateway en un seul endroit.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` documente l'application comme compagne de barre de menu, modes local/distant, installation de CLI, liste de contrôle des permissions et flux d'intégration typique.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/bundled-gateway.md` indique que l'application macOS s'attend à une installation CLI externe et que le bouton Installer CLI utilise npm, pnpm, puis bun.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/dev-setup.md` documente la configuration de développeur et de CLI.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/Onboarding.swift` définit l'ordre des pages d'intégration pour les modes local, distant et non configuré, marque l'achèvement et crée un `OpenClawChatViewModel` avec la clé de session `onboarding`.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/OnboardingWizard.swift` démarre l'assistant Gateway en mode local, soumet les étapes de l'assistant et réessaie une fois quand une session d'assistant est perdue.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/CLIInstaller.swift` résout les chemins CLI installés et exécute le script d'installation JSON avec une version et un préfixe.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/CLIInstallPrompter.swift` invite les utilisateurs du mode local post-intégration quand la CLI est manquante.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/package-mac-app.test.ts` vérifie le comportement du script d'empaquetage macOS, la sécurité du fichier de verrouillage d'installation de dépendance, le ciblage du processus d'application et l'inclusion dans la voie CI macOS.
- `/Users/kevinlin/code/openclaw/test/scripts/codesign-mac-app.test.ts` et `/Users/kevinlin/code/openclaw/test/scripts/notarize-mac-artifact.test.ts` valident l'hygiène du script de version et les vérifications de fermeture d'échec.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/OnboardingCoverageTests.swift` exerce les pages d'intégration.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/OnboardingViewSmokeTests.swift`, `OnboardingWizardStepViewTests.swift` et `OnboardingRemoteAuthPromptTests.swift` couvrent le rendu d'intégration et le comportement d'invite d'authentification distante.
- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/CLIInstallerTests.swift` couvre le comportement d'aide d'installation de CLI.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS onboarding CLI install" --json`

Résultats :

- PR #47263 `Improve macOS onboarding UX and gateway setup`.
- Issue #65345 `Docs/code alignment questions across config, APIs, and onboarding`.
- PR #87255 `fix(config): skip .openclaw append when OPENCLAW_HOME already names a state dir`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS Install CLI"`

Résultats :

- 2026-05-23 le message du responsable demande un smoke macOS/Linux/Windows propre couvrant l'installation vierge, la mise à niveau, le démarrage de Gateway, un tour de chat, le chargement de plugin et les journaux.
- 2026-05-27 la note de version dit que les chemins d'installation/mise à jour ont été durcis, y compris les bootstraps de runner macOS.
