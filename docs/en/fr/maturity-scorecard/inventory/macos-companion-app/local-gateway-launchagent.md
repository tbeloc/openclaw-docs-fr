---
title: "Application compagnon macOS - Note de maturité Local Gateway et Launchagent"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Application compagnon macOS - Note de maturité Local Gateway et Launchagent

## Résumé

Le mode local est un flux de travail d'opérateur réel : l'application s'attache à une Gateway existante, gère le LaunchAgent par utilisateur via la CLI, évite le démarrage local de la Gateway en mode distant, expose les chemins de santé/journaux, et dispose de tests ciblés autour de launchd et de l'empaquetage. La couverture est Beta car le cycle de vie est implémenté via des chemins CLI/launchd avec des preuves de support ciblées, mais aucun scénario d'application en direct complet n'a été trouvé. La qualité est Alpha car les preuves d'archive montrent que les défaillances de mise à jour/redémarrage de LaunchAgent, de conflit de port, de TCC et d'env-wrapper restent des risques opérationnels à fort impact.

## Portée des catégories

- Attachement/démarrage/arrêt de la Gateway en mode local.
- Installation/mise à jour/redémarrage/désinstallation de LaunchAgent via des appels CLI gérés par l'application.
- Détection d'écouteur existant, protection des ports et chemin du journal launchd.
- Hors de portée : service Gateway Linux/systemd.

## Fonctionnalités

- Attachement/démarrage/arrêt de la Gateway en mode local : comportement, statut et vérification visible par l'opérateur de l'attachement/démarrage/arrêt de la Gateway en mode local.
- Installation/mise à jour/redémarrage/désinstallation de LaunchAgent : installation/mise à jour/redémarrage/désinstallation de LaunchAgent via des appels CLI gérés par l'application
- Détection d'écouteur existant : détection d'écouteur existant, protection des ports et chemin du journal launchd

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : la documentation couvre l'exigence CLI externe, le LaunchAgent détenu par l'application, le comportement d'attachement à l'existant, la compatibilité des versions et les vérifications de fumée. La source dispose de gardes local/distant explicites, de sondes de santé d'attachement à l'existant, de commandes launchd et de comportement de gardien de port. Les tests Swift et TS couvrent le gestionnaire launchd, le gestionnaire de processus Gateway, les scripts de package et les aides de redémarrage/mise à jour.
- Signaux négatifs : les tests ne prouvent pas la mise à jour destructive de LaunchAgent auto-gérée ou le comportement de redémarrage de Gateway à long terme géré par l'application sur un système installé réel.
- Lacunes d'intégration : besoin d'un scénario d'application signée qui active launchd, survit à la fermeture de l'application, met à jour/redémarre la Gateway, détecte un service obsolète et récupère sans réparation shell manuelle.

## Score de qualité

- Score : `Alpha (65%)`
- Rapports Gitcrawl : les résultats incluent la PR #81725 pour ignorer la réparation CLI de la gateway lorsque l'application possède launchd, le problème #65619 pour la résolution de liaison de loopback à `0.0.0.0`, le problème #78049 pour l'accès aux dossiers TCC gérés par launchd Gateway, le problème #86104 pour le relancement de mise à jour unique, le problème #87199 pour env-wrapper/`gateway run` manquant, et le problème #87402 pour le conflit de port d'écouteur géré lors du redémarrage.
- Rapports Discrawl : l'archive du responsable inclut les défaillances de mise à jour automatique v2026.5.12 sur les instances LaunchAgent macOS, la réparation SSH manuelle, le nettoyage de LaunchAgent de mise à jour transitoire obsolète et une note de version indiquant que la récupération de LaunchAgent macOS était un domaine de correction majeur.
- Bonnes qualités : la source évite délibérément la génération de Gateway en tant que processus enfant, utilise le chemin du démon CLI externe, s'attache aux gateways saines existantes et ignore les écritures launchd en modes attach-only/distant.
- Mauvaises qualités : les modes de défaillance opérationnelle peuvent laisser le service hors ligne ou entrer en conflit avec les flux de mise à jour/redémarrage. Plusieurs rapports actuels impliquent des états launchd, de permission ou d'écouteur non évidents.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution réel n'a pas été utilisée pour augmenter ou diminuer la qualité.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-companion-app.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'attachement/démarrage/arrêt de la Gateway en mode local, l'installation/mise à jour/redémarrage/désinstallation de LaunchAgent, la détection d'écouteur existant.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Besoin d'un vrai QA de mise à jour automatique destructive de LaunchAgent macOS, incluant les états package-current/service-offline.
- Besoin d'un chemin de récupération orienté application pour les défaillances d'env-wrapper, de travail de mise à jour obsolète, de conflit de port et de dossier protégé par TCC.
- Besoin de preuves de version répétées pour le démarrage, redémarrage, mise à jour et santé de la Gateway locale à partir d'une application signée empaquetée.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/platforms/mac/bundled-gateway.md` documente l'installation CLI externe, le LaunchAgent détenu par l'application, le comportement d'attachement à l'existant, le chemin du journal launchd, la compatibilité des versions et la vérification de fumée.
- `/Users/kevinlin/code/openclaw/docs/platforms/macos.md` documente le mode local, l'étiquette LaunchAgent et le dépannage pour les arrêts silencieux et la protection de respawn launchd.
- `/Users/kevinlin/code/openclaw/docs/platforms/mac/child-process.md` documente que l'application gère la Gateway via launchd et ne la génère pas en tant que processus enfant.

### Source

- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/GatewayProcessManager.swift` gère l'activation en mode local, les sondes d'attachement à l'existant, l'actualisation de l'environnement, l'activation de launchd, l'actualisation du journal et l'omission du mode distant.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/GatewayLaunchAgentManager.swift` achemine les modifications launchd via les commandes du démon `openclaw gateway` et résout le chemin de statut/journal.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/ConnectionModeCoordinator.swift` démarre la Gateway locale et le canal de contrôle en mode local, et arrête la Gateway locale en modes distant/non configuré.
- `/Users/kevinlin/code/openclaw/apps/macos/Sources/OpenClaw/PortGuardian.swift` détecte les écouteurs de port attendus et inattendus.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/test/scripts/restart-mac.test.ts`, `package-mac-app.test.ts` et `package-mac-dist.test.ts` couvrent le comportement du script de redémarrage/empaquetage de l'application.
- Aucun scénario complet de mise à jour/récupération de LaunchAgent en direct n'a été trouvé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/apps/macos/Tests/OpenClawIPCTests/GatewayProcessManagerTests.swift`, `GatewayLaunchAgentManagerTests.swift`, `LaunchAgentManagerTests.swift`, `LaunchctlTests.swift`, `GatewayAutostartPolicyTests.swift` et couverture de `PortGuardian` dans `LowCoverageHelperTests.swift`.
- `/Users/kevinlin/code/openclaw/src/daemon/launchd*.ts` dispose de tests Gateway daemon plus larges en dehors de l'application native.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "macOS LaunchAgent gateway local mode" --json`

Résultats :

- PR #81725 `macOS: skip CLI gateway repair when app owns launchd`.
- Problème #65619 `macOS: gateway bind=loopback resolves to 0.0.0.0 and refuses to start`.
- Problème #78049 `macOS launchd-managed Gateway cannot reliably access TCC-protected folders via CLI tools`.
- Problème #86104 `macOS: launchctl submit can relaunch one-shot update jobs after clean exit`.
- Problème #87199 `macOS LaunchAgent generated by 2026.5.22 uses env-wrapper and missing gateway run`.
- Problème #87402 `Gateway restart treats managed listener as port conflict`.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "macOS LaunchAgent gateway"`

Résultats :

- 14 mai 2026 rapport du responsable : défaillance de mise à jour automatique v2026.5.12 sur trois instances LaunchAgent macOS ; une réparation manuelle en dehors d'OpenClaw a été nécessaire.
- 8 mai 2026 note du responsable : LaunchAgent de mise à jour transitoire obsolète a répétitivement tué les redémarrages de Gateway et laissé la Gateway canonique désactivée.
- 6 mai 2026 note PR : bugs launchd `disable` et `kickstart` inutiles corrigés.
