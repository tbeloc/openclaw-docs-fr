---
title: "Hôte macOS Gateway - Note de Maturité des Diagnostics et de l'Observabilité"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Hôte macOS Gateway - Note de Maturité des Diagnostics et de l'Observabilité

## Résumé

L'observabilité de l'hôte macOS Gateway est solide. Les opérateurs disposent de chemins stdout/stderr launchd, de diagnostics d'application JSONL, de `gateway status --deep`, de vérifications du service/plateforme du docteur, de runbooks de dépannage Gateway, de conseils ENETDOWN, de vérifications de mise à jour obsolète, de diagnostics de pression mémoire et de sondes de canal/service.

La couverture est Stable car la documentation/source/tests couvrent les principales surfaces de diagnostic. La qualité est Stable car les surfaces d'opérateur sont spécifiques et exploitables, bien que les défaillances graves de mise à jour/launchd nécessitent toujours plusieurs commandes et emplacements de journaux.

## Portée de la catégorie

Inclus dans cette catégorie :

- Chemins de journaux LaunchAgent : chemins de journaux LaunchAgent et chemins de journaux de diagnostic d'application
- openclaw gateway status --deep : openclaw gateway status --deep, sonde gateway, commandes doctor, health et logs
- Gateway cesse silencieusement de répondre : Gateway cesse silencieusement de répondre, défaillance de mise en veille/réveil ENETDOWN, conflits de port, configuration invalide et runbooks de pression mémoire
- Tâches de mise à jour obsolète : tâches de mise à jour obsolète, dérive de configuration de service et diagnostics d'environnement LaunchAgent

## Fonctionnalités

- Chemins de journaux LaunchAgent : chemins de journaux LaunchAgent et chemins de journaux de diagnostic d'application
- openclaw gateway status --deep : openclaw gateway status --deep, sonde gateway, commandes doctor, health et logs
- Gateway cesse silencieusement de répondre : Gateway cesse silencieusement de répondre, défaillance de mise en veille/réveil ENETDOWN, conflits de port, configuration invalide et runbooks de pression mémoire
- Tâches de mise à jour obsolète : tâches de mise à jour obsolète, dérive de configuration de service et diagnostics d'environnement LaunchAgent

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (80%)`
- Signaux positifs : la documentation couvre les échelles de commandes et les défaillances spécifiques à macOS ; la source implémente les localisateurs de journaux et les diagnostics JSONL ; les tests couvrent les chemins de journaux, les diagnostics de statut, les stderr obsolètes, les remplacements d'environnement launchctl et le nettoyage des mises à jour obsolètes.
- Signaux négatifs : la preuve d'observabilité est large mais non empaquetée comme un seul flux de bundle de support macOS qui capture chaque artefact de journaux et de statut pertinent.
- Lacunes d'intégration : besoin d'une preuve de version qui injecte une défaillance launchd, une perte d'écouteur de type ENETDOWN, une tâche de mise à jour obsolète et une configuration invalide, puis valide les diagnostics visibles par l'opérateur.

## Score de qualité

- Score : `Stable (83%)`
- Rapports Gitcrawl : `gateway status deep macOS ENETDOWN stale updater memory pressure` n'a retourné aucun résultat ouvert, et la requête de diagnostics antérieure pour `macOS gateway diagnostics logs launchd stability ENETDOWN status deep` n'a également retourné aucun résultat.
- Rapports Discrawl : `macOS gateway silently stops responding ENETDOWN` n'a retourné aucun résultat imprimé, tandis que les recherches launchd/update ont retourné des modèles de support de statut/deep-status concrets que la documentation/source adresse maintenant.
- Bonnes qualités : la documentation est orientée commandes, les chemins de journaux sont explicites, les diagnostics d'application sont JSONL avec rotation, le statut rassemble les détails de service/env/runtime/config/audit/probe, et le docteur dispose de modes de réparation plus des vérifications de plateforme/service.
- Mauvaises qualités : les incidents launchd/update graves nécessitent toujours que les opérateurs combinent manuellement `gateway status --deep`, doctor, launchctl, fichiers journaux, nettoyage des mises à jour obsolètes et diagnostics d'application.
- Exclu de la qualité : les preuves de couverture uniquement ont été considérées uniquement dans le score de couverture, pas dans ce score de qualité.

## Score de complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/macos-gateway-host.md`.
- Signaux positifs : la documentation archivée, la source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les chemins de journaux LaunchAgent, openclaw gateway status --deep, Gateway cesse silencieusement de répondre, Tâches de mise à jour obsolète.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version de processus 3, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Un seul bundle de support macOS devrait collecter les diagnostics d'application, stdout/stderr launchd, `launchctl print`, `gateway status --deep`, la sortie du docteur et l'état de mise à jour obsolète.
- Le dépannage pourrait lier les diagnostics d'application directement à partir du runbook launchd Gateway.
- Les conseils ENETDOWN/sleep-wake devraient être inclus dans le runbook principal de l'hôte macOS, pas seulement dans le dépannage Gateway.

## Preuves

### Documentation

- `docs/platforms/mac/bundled-gateway.md:50` : documente les journaux et les vérifications de compatibilité de version.
- `docs/platforms/macos.md:173` : documente les commandes CLI de débogage telles que `openclaw-mac connect/discover`.
- `docs/cli/gateway.md:267` : documente `gateway status --deep`, les exigences RPC et la dérive de configuration.
- `docs/cli/gateway.md:323` : documente `gateway probe`, les avertissements et la détection de plusieurs Gateway.
- `docs/gateway/doctor.md:10` : documente le docteur comme outil de réparation/migration.
- `docs/gateway/doctor.md:166` : documente les vérifications Gateway, service, superviseur, runtime et collision de port.
- `docs/gateway/troubleshooting.md:12` : donne une échelle de commandes d'opérateur.
- `docs/gateway/troubleshooting.md:457` : documente macOS Gateway cesse silencieusement de répondre, ENETDOWN, porte de respawn launchd, pmset et conseils de surveillance.
- `docs/gateway/troubleshooting.md:509` : documente les diagnostics de pression mémoire.
- `docs/gateway/troubleshooting.md:545` : documente la réparation de configuration invalide.

### Source

- `apps/macos/Sources/OpenClaw/LogLocator.swift:3` : définit les répertoires de journaux sous `/tmp/openclaw` et les chemins stdout/log Gateway.
- `apps/macos/Sources/OpenClaw/LogLocator.swift:48` : résout les chemins de journaux LaunchAgent.
- `apps/macos/Sources/OpenClaw/DiagnosticsFileLog.swift:3` : définit la journalisation diagnostique JSONL et la rotation.
- `apps/macos/Sources/OpenClaw/DiagnosticsFileLog.swift:18` : stocke les diagnostics sous `~/Library/Logs/OpenClaw/diagnostics.jsonl`.
- `apps/macos/Sources/OpenClaw/DiagnosticsFileLog.swift:34` : ajoute des enregistrements de diagnostic.
- `src/cli/daemon-cli/status.gather.ts:493` : rassemble la commande/env/runtime du service, l'audit de configuration, la configuration CLI-vs-daemon, l'URL de port/sonde, la remise de redémarrage profond, les services supplémentaires, les tâches launchd de mise à jour obsolète, la sonde d'authentification SecretRef, la santé RPC, la santé PID obsolète et la dernière erreur.
- `src/daemon/launchd.ts:291` : trouve les tâches de mise à jour obsolète.
- `src/daemon/launchd.ts:387` : analyse le port de service à partir des arguments/env du programme launchd.
- `src/daemon/launchd.ts:410` : émet des conseils d'amorçage de session GUI.

### Tests d'intégration

- `scripts/e2e/parallels/macos-smoke.ts:923` : exécute `gateway status --deep --require-rpc` dans un invité macOS.
- `scripts/e2e/parallels/macos-discord.ts:27` : exécute le docteur, le redémarrage Gateway et la sonde de canal dans le cadre du smoke Discord macOS.
- `src/daemon/launchd.integration.e2e.test.ts:246` : prouve un chemin de réparation launchd manquant-bootstrap.

### Tests unitaires

- `apps/macos/Tests/OpenClawIPCTests/LogLocatorTests.swift:6` : vérifie la résolution du chemin de journaux d'application et LaunchAgent.
- `src/daemon/restart-logs.test.ts:39` : vérifie les journaux macOS LaunchAgent sous `~/Library/Logs/openclaw`.
- `src/daemon/diagnostics.test.ts:23` : vérifie la suppression stderr launchd et la gestion stderr obsolète.
- `src/commands/doctor-platform-notes.launchctl-env-overrides.test.ts:19` : teste les avertissements de remplacement de jeton launchctl et les conseils de désactivation.
- `src/commands/doctor-platform-notes.launchctl-env-overrides.test.ts:124` : teste l'avertissement de tâche de mise à jour obsolète et le nettoyage.
- `src/cli/daemon-cli/status.gather.test.ts:455` : affiche les remises de redémarrage et les tâches launchd de mise à jour obsolète dans le statut profond.
- `src/cli/daemon-cli/status.gather.test.ts:616` : utilise la validation de configuration consciente du plugin dans la collecte de statut.

### Requêtes Gitcrawl

Requête :

```bash
gitcrawl search issues "macOS gateway diagnostics logs launchd stability ENETDOWN status deep" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Retourné `[]`.

Requête :

```bash
gitcrawl search issues "gateway status deep macOS ENETDOWN stale updater memory pressure" -R openclaw/openclaw --state open --json number,title,url,state --limit 5
```

Résultats :

- Retourné `[]`.

### Requêtes Discrawl

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "macOS gateway silently stops responding ENETDOWN"
```

Résultats :

- La commande a réussi et n'a retourné aucun résultat imprimé.

Requête :

```bash
DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 5 "gateway service launchd"
```

Résultats :

- Retourné des rapports de support où `gateway status --deep`, l'état de la tâche launchd, les tâches de mise à jour obsolète et la dérive de service étaient centraux au diagnostic de l'opérateur.
