---
title: "macOS Gateway host - CLI Setup Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# macOS Gateway host - CLI Setup Maturity Note

## Résumé

L'hôte macOS Gateway dispose d'un chemin de prérequis CLI et runtime concret. La documentation couvre les scripts d'installation, les exigences Node, la réparation PATH, les conseils npm/pnpm/bun, et l'attente de l'application macOS que `openclaw` soit installé en externe. Le code source soutient le flux de détection/installation CLI de l'application et le chemin de préfixe local du programme d'installation CLI.

La couverture est Stable car la documentation, le code source, les garde-fous runtime et les flux de fumée Parallels macOS exercent tous ce chemin. La qualité est Beta car les preuves d'archive actuelles montrent toujours une dérive package-manager/runtime sur macOS, en particulier après les opérations Homebrew ou de mise à jour.

## Portée de la catégorie

Inclus dans cette catégorie :

- Programme d'installation hébergé : chemins d'installation du programme d'installation hébergé et de préfixe local sur macOS
- Recommandation Node 24 : recommandation Node 24 et plancher de compatibilité Node 22.19+
- Installation CLI déclenchée par l'application : installation CLI déclenchée par l'application et découverte runtime
- Dérive PATH shell et version-manager : dérive PATH shell, package-manager et version-manager qui affectent l'hôte Gateway.

## Fonctionnalités

- Programme d'installation hébergé : chemins d'installation du programme d'installation hébergé et de préfixe local sur macOS
- Recommandation Node 24 : recommandation Node 24 et plancher de compatibilité Node 22.19+
- Installation CLI déclenchée par l'application : installation CLI déclenchée par l'application et découverte runtime
- Dérive PATH shell et version-manager : dérive PATH shell, package-manager et version-manager qui affectent l'hôte Gateway.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : documentation du programme d'installation, documentation Node, code source du programme d'installation CLI de l'application, vérifications du localisateur runtime et couverture de fumée d'installation/mise à jour Parallels macOS couvrent tous le chemin d'installation principal.
- Signaux négatifs : la couverture en direct la plus forte est orientée vers la fumée de version et ne couvre pas exhaustivement les combinaisons Homebrew, npm global, préfixe local, version-manager et installation déclenchée par l'application.
- Lacunes d'intégration : il n'existe pas de couloir en direct unique qui commence à partir d'un bureau macOS propre, installe la CLI via l'application, vérifie Node/PATH, puis prouve le démarrage launchd Gateway à partir de cette même installation gérée par l'application.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : `macOS install openclaw CLI Node PATH command not found` a retourné l'ouverture #80387 pour la commande `openclaw` disparaissant après une mise à niveau majeure de Node Homebrew. `self-update macOS LaunchAgent not loaded gateway` a retourné l'ouverture #75250 pour la dérive mixte Homebrew Node/runtime/plugin cache.
- Rapports Discrawl : `macOS install openclaw command not found` a retourné des fils de support de mise à jour/installation macOS récents, y compris une note de récupération du 2026-04-18 où une réparation d'agent a laissé la CLI manquante ou PATH-cassée et la récupération recommandée était de réexécuter le programme d'installation à partir du Terminal.
- Bonnes qualités : la documentation indique clairement le plancher Node, l'application détecte `openclaw`, le flux d'installation de l'application utilise le `install-cli.sh` hébergé avec les drapeaux JSON/no-onboard, et la documentation CLI sépare l'installation complète de l'installation de préfixe local.
- Mauvaises qualités : la surface d'installation traverse PATH shell, gestionnaires Node, Homebrew, globals npm, préfixes locaux et processus non interactifs lancés par l'application ; le signal d'archive montre que ces limites peuvent toujours casser le démarrage Gateway visible par l'utilisateur.
- Exclu de la qualité : les preuves de couverture uniquement ont été considérées uniquement dans le score de couverture, pas dans ce score de qualité.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le programme d'installation hébergé, la recommandation Node 24, l'installation CLI déclenchée par l'application et la dérive PATH shell et version-manager.
- Signaux négatifs : la note archivée a précédé le score de complétude du processus-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- L'installation déclenchée par l'application devrait avoir une porte de version qui vérifie la commande exacte que l'application exécute, puis prouve `openclaw gateway status` à partir de la CLI installée.
- La récupération après mise à niveau majeure Homebrew/Node reste un élément de surveillance actif.
- Les conseils PATH sont répartis entre la documentation d'installation, Node et l'application macOS plutôt que dans un seul runbook d'hôte macOS.

## Preuves

### Documentation

- `docs/platforms/macos.md:9` : l'application macOS possède les permissions et gère ou s'attache à la Gateway, avec support de préférence d'installation CLI.
- `docs/platforms/mac/bundled-gateway.md:10` : l'application ne regroupe plus Node, Bun ou Gateway et s'attend à une CLI `openclaw` externe.
- `docs/platforms/mac/bundled-gateway.md:15` : documente la valeur par défaut Node 24, la compatibilité Node 22.19+, l'installation globale npm et la préférence d'installation CLI de l'application.
- `docs/install/installer.md:67` : documente le flux `install.sh`, Node 24, Git, installation npm/git, actualisation du service post-installation, doctor et onboarding.
- `docs/install/installer.md:178` : documente l'installation de préfixe local `install-cli.sh` et l'actualisation des services chargés.
- `docs/install/node.md:10` : documente Node 22.19+ requis et Node 24 recommandé.
- `docs/install/node.md:87` : documente le dépannage PATH lorsque les shells ne peuvent pas trouver Node/npm/openclaw.

### Source

- `apps/macos/Sources/OpenClaw/CLIInstaller.swift:5` : détecte si `openclaw` est installé et capture les métadonnées CLI.
- `apps/macos/Sources/OpenClaw/CLIInstaller.swift:37` : exécute le flux d'installation CLI de l'application et affiche la sortie d'installation.
- `apps/macos/Sources/OpenClaw/CLIInstaller.swift:63` : installe vers `~/.openclaw` via `curl -fsSL https://openclaw.bot/install-cli.sh | bash -s -- --json --no-onboard --prefix ... --version ...`.
- `apps/macos/Sources/OpenClaw/GatewayLaunchAgentManager.swift:151` : résout les commandes `openclaw gateway` avec un PATH préféré pour le mode local géré par l'application.
- `src/cli/daemon-cli/install.ts:80` : valide runtime, port, config, wrapper et `gateway.mode=local` par défaut avant d'installer le service.
- `src/commands/daemon-install-helpers.ts:246` : construit le PATH du service à partir de répertoires runtime explicites et de données d'environnement préservées.

### Tests d'intégration

- `scripts/e2e/parallels/macos-smoke.ts:757` : installe la dernière version dans un invité macOS via le chemin du programme d'installation de version.
- `scripts/e2e/parallels/macos-smoke.ts:827` : effectue l'onboarding local non interactif avec `--install-daemon`.
- `scripts/e2e/parallels/macos-smoke.ts:873` : exerce une mise à jour de dev via le flux de mise à jour package/git.
- `scripts/e2e/parallels/macos-smoke.ts:923` : vérifie `openclaw gateway status --deep --require-rpc` après installation/mise à jour.

### Tests unitaires

- `apps/macos/Tests/OpenClawIPCTests/RuntimeLocatorTests.swift:16` : accepte un runtime Node 22.19 valide.
- `apps/macos/Tests/OpenClawIPCTests/RuntimeLocatorTests.swift:31` : rejette Node 22.18.9 comme non supporté.
- `apps/macos/Tests/OpenClawIPCTests/RuntimeLocatorTests.swift:77` : inclut les chemins recherchés dans les messages d'erreur.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:25` : résout les chemins de commande `openclaw` et Node fallback.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:138` : honore les chemins de commande préférés.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "macOS install openclaw CLI Node PATH command not found" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Ouverture #80387 : `[Bug]: Openclaw command disappears after brew upgrade installs a new Node major`.
- Les autres problèmes retournés étaient des rapports runtime/channel plus larges et moins directement liés à l'installation CLI macOS.

Requête :

```bash
gitcrawl search issues "macOS install openclaw CLI Node PATH command not found" -R openclaw/openclaw --state closed --json number,title,url,state --limit 5
```

Résultats :

- Retourné `[]`.

### Requêtes Discrawl

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "macOS install openclaw command not found"
```

Résultats :

- Retourné un fil de récupération du 2026-04-18 où une réparation macOS a laissé la CLI manquante/PATH-cassée et la récupération conseillée était de réexécuter le programme d'installation à partir du Terminal.
- Retourné une discussion de packaging macOS du 2026-05-27 autour de l'échec de la construction du wrapper `openclaw-qmd`.
- Retourné une dérive de dépendance package/runtime du 2026-04-22 après une mise à jour globale npm.
