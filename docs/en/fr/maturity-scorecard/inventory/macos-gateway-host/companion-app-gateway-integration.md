---
title: "macOS Gateway host - Companion App Gateway Integration Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# macOS Gateway host - Companion App Gateway Integration Maturity Note

## Résumé

L'application compagnon macOS est intégrée au Gateway host via la coordination en mode explicite, la gestion de LaunchAgent, la résolution de points de terminaison, la détection d'installation CLI et le comportement d'attachement à un existant. L'application n'intègre pas le Gateway ; elle s'attend à la CLI externe, puis gère soit launchd en mode local, soit se connecte à un Gateway distant et démarre l'hôte du nœud local.

La couverture est Beta car la plupart des preuves sont basées sur le code source/les tests unitaires/la documentation, avec moins d'automatisation complète de l'application. La qualité est Stable car le code a des limites claires entre les modes local, distant, attachement uniquement, installation CLI et sélection de point de terminaison.

## Portée de la catégorie

- Coordination du mode de connexion local/distant de l'application.
- Installation/redémarrage/désinstallation de LaunchAgent Gateway gérée par l'application via la CLI.
- Détection d'installation CLI et invite d'installation d'application.
- Vérifications de compatibilité d'attachement à un Gateway local existant.
- Résolution du point de terminaison Gateway, des identifiants et du canal de contrôle.

## Fonctionnalités

- Mode de connexion local/distant de l'application : Coordination du mode de connexion local/distant de l'application
- Installation/redémarrage/désinstallation de LaunchAgent Gateway gérée par l'application : Installation/redémarrage/désinstallation de LaunchAgent Gateway gérée par l'application via la CLI
- Détection d'installation CLI : Détection d'installation CLI et invite d'installation d'application
- Compatibilité d'attachement à un Gateway local existant : Vérifications de compatibilité d'attachement à un Gateway local existant
- Point de terminaison Gateway : Résolution du point de terminaison Gateway, des identifiants et du canal de contrôle

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : la documentation et le code source de l'application couvrent le modèle CLI externe, le contrôle launchd, le marqueur d'attachement uniquement, le comportement de saut en mode distant, le magasin de points de terminaison et la configuration du canal de contrôle.
- Signaux négatifs : les preuves de test au niveau de l'interface utilisateur pour le flux complet de l'application sont plus minces que les preuves de code source Swift/tests unitaires.
- Lacunes d'intégration : aucune voie de publication inspectée ne clique sur l'application via l'installation CLI, l'activation du Gateway local, l'attachement à un existant, le changement distant et la récupération de l'état CLI manquant.

## Score de qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl : `macOS app gateway launchd attach existing install CLI version compatibility` n'a retourné aucun résultat ouvert.
- Rapports Discrawl : `macOS app gateway install CLI` a retourné principalement des résultats de publication/support général plutôt que des défauts directs d'intégration d'application ; `mac app remote gateway ssh tunnel` a retourné une confusion utilisateur sur le comportement de l'application/nœud distant.
- Bonnes qualités : le code source de l'application a un coordinateur de mode spécifique, un gestionnaire LaunchAgent dédié, un programme d'installation CLI, un magasin de points de terminaison, un résolveur de configuration distant et un gestionnaire de tunnel plutôt que du spawning de processus ad hoc.
- Mauvaises qualités : la documentation et le comportement du produit peuvent laisser les utilisateurs incertains quant à savoir si l'application installe une CLI globale ou une CLI avec préfixe local, et si le mode distant fait du Mac un opérateur, un nœud ou les deux.
- Exclus de la qualité : les preuves basées uniquement sur la couverture ont été considérées uniquement dans le score de couverture, pas dans ce score de qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : la documentation archivée, le code source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le mode de connexion local/distant de l'application, l'installation/redémarrage/désinstallation de LaunchAgent Gateway gérée par l'application, la détection d'installation CLI, la compatibilité d'attachement à un Gateway local existant, le point de terminaison Gateway.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 des processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aligner la documentation d'installation de l'application avec le comportement réel de la source `install-cli.sh --prefix ~/.openclaw`.
- Ajouter l'automatisation au niveau de l'application pour le changement de mode local/distant et l'activation de launchd.
- Fournir un texte d'état d'application plus clair pour le Gateway local attaché par rapport au Gateway local géré par l'application.

## Preuves

### Documentation

- `docs/platforms/macos.md:9` : indique que l'application macOS possède les autorisations, gère ou s'attache au Gateway et supporte les modes local/distant.
- `docs/platforms/macos.md:141` : documente le flux d'intégration pour l'installation de CLI, la sélection du mode local/distant et l'octroi des autorisations.
- `docs/platforms/mac/bundled-gateway.md:10` : indique que l'application n'intègre plus Node/Bun/Gateway et s'attend à un `openclaw` externe.
- `docs/platforms/mac/bundled-gateway.md:27` : documente le service launchd par utilisateur géré par l'application, la gestion CLI, le basculement actif, le comportement de fermeture et l'attachement à un existant.
- `docs/platforms/mac/remote.md:66` : documente les paramètres de l'application et le comportement de test distant.

### Code source

- `apps/macos/Sources/OpenClaw/ConnectionModeCoordinator.swift:19` : le mode local arrête le nœud/les tunnels, démarre le Gateway local si la politique le dit, attend la disponibilité et configure le contrôle local.
- `apps/macos/Sources/OpenClaw/ConnectionModeCoordinator.swift:57` : le mode distant arrête le Gateway local, démarre le service de nœud, assure le tunnel de contrôle distant et configure le contrôle distant.
- `apps/macos/Sources/OpenClaw/GatewayLaunchAgentManager.swift:22` : supporte le marqueur d'écritures désactivées de launchd et le mode d'attachement uniquement.
- `apps/macos/Sources/OpenClaw/GatewayLaunchAgentManager.swift:57` : installe/désinstalle/redémarre le LaunchAgent Gateway via la CLI.
- `apps/macos/Sources/OpenClaw/GatewayProcessManager.swift:61` : ignore la gestion du Gateway local en mode distant.
- `apps/macos/Sources/OpenClaw/GatewayProcessManager.swift:99` : s'attache à un Gateway existant compatible avant d'activer launchd.
- `apps/macos/Sources/OpenClaw/GatewayProcessManager.swift:243` : signale les défaillances d'authentification/protocole lors de l'attachement à un Gateway existant.
- `apps/macos/Sources/OpenClaw/GatewayEndpointStore.swift:43` : câble les dépendances pour le mode, le jeton/mot de passe, l'hôte local et le tunnel distant.
- `apps/macos/Sources/OpenClaw/CLIInstaller.swift:5` : détecte le `openclaw` installé.
- `apps/macos/Sources/OpenClaw/CLIInstaller.swift:37` : exécute le programme d'installation CLI de l'application.

### Tests d'intégration

- `scripts/e2e/parallels/macos-smoke.ts:980` : vérifie le chargement du tableau de bord à partir d'un Gateway local sur un invité macOS.
- `scripts/e2e/parallels/macos-smoke.ts:1006` : vérifie le premier tour d'agent après la configuration de macOS.
- `scripts/e2e/parallels/macos-discord.ts:27` : configure Discord, exécute doctor, redémarre Gateway et sonde l'état des canaux sur un chemin de fumée macOS.

### Tests unitaires

- `apps/macos/Tests/OpenClawIPCTests/GatewayLaunchAgentManagerTests.swift:5` : le remplacement d'attachement uniquement écrit le marqueur et ne désinstalle pas.
- `apps/macos/Tests/OpenClawIPCTests/GatewayLaunchAgentManagerTests.swift:29` : analyse les arguments/env du plist LaunchAgent token/mot de passe.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:25` : résout les chemins de commande d'application pour `openclaw` et Node.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:148` : construit les commandes SSH pour le mode distant.
- `apps/macos/Tests/OpenClawIPCTests/CommandResolverTests.swift:210` : garde le remplacement de commande daemon local indépendant des valeurs par défaut distantes.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "macOS app gateway launchd attach existing install CLI version compatibility" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- A retourné `[]`.

### Requêtes Discrawl

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "macOS app gateway install CLI"
```

Résultats :

- A retourné des discussions de publication/support mais aucun défaut direct d'intégration Gateway d'application ouvert.
- A retourné des conseils généraux de redémarrage de Gateway qui demandent aux utilisateurs d'identifier le type d'installation : Docker, systemd, application macOS ou Gateway shell.

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "mac app remote gateway ssh tunnel"
```

Résultats :

- A retourné des conseils de support selon lesquels le mode distant de l'application devrait posséder le tunnel SSH et que Tailscale est plus simple pour l'opération app-to-remote-Gateway.
