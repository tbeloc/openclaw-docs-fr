---
title: "Linux Gateway host - Gateway Runtime and Service Control Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Linux Gateway host - Gateway Runtime and Service Control Maturity Note

## Résumé

Le comportement du runtime Gateway en avant-plan est stable pour les opérateurs normaux. La CLI documente `openclaw gateway`, `openclaw gateway run`, les gardes bind/auth, les signaux de redémarrage, les sondes de santé/disponibilité et l'accès aux journaux ; le code source implémente les gardes de démarrage, la gestion des verrous, la transmission des mises à jour et l'ajustement OOM des processus enfants Linux. La qualité reste juste à l'intérieur de la stabilité car les problèmes récents montrent certains bords de port/sonde et de chemin de redémarrage, mais le chemin d'exécution principal est mature.

## Portée de la catégorie

Inclus dans cette catégorie :

- Foreground Gateway Runtime : Couvre les contrôles visibles par l'utilisateur du Foreground Gateway Runtime, l'affichage d'état, la navigation et le comportement de rendu pour le Foreground Gateway Runtime et le contrôle des processus.
- Process Control : Couvre les contrôles visibles par l'utilisateur du Process Control, l'affichage d'état, la navigation et le comportement de rendu pour le Foreground Gateway Runtime et le contrôle des processus.
- Systemd User Service Lifecycle setup : Définit la configuration du Systemd User Service Lifecycle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Systemd User Service Lifecycle.
- Systemd User Service Lifecycle operation : Définit la configuration de l'opération Systemd User Service Lifecycle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Systemd User Service Lifecycle.
- Systemd User Service Lifecycle status : Définit la configuration du statut Systemd User Service Lifecycle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Systemd User Service Lifecycle.
- Systemd User Service Lifecycle recovery : Définit la configuration de la récupération Systemd User Service Lifecycle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Systemd User Service Lifecycle.

## Fonctionnalités

- Foreground Gateway Runtime : Couvre les contrôles visibles par l'utilisateur du Foreground Gateway Runtime, l'affichage d'état, la navigation et le comportement de rendu pour le Foreground Gateway Runtime et le contrôle des processus.
- Process Control : Couvre les contrôles visibles par l'utilisateur du Process Control, l'affichage d'état, la navigation et le comportement de rendu pour le Foreground Gateway Runtime et le contrôle des processus.
- Systemd User Service Lifecycle setup : Définit la configuration du Systemd User Service Lifecycle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Systemd User Service Lifecycle.
- Systemd User Service Lifecycle operation : Définit la configuration de l'opération Systemd User Service Lifecycle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Systemd User Service Lifecycle.
- Systemd User Service Lifecycle status : Définit la configuration du statut Systemd User Service Lifecycle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Systemd User Service Lifecycle.
- Systemd User Service Lifecycle recovery : Définit la configuration de la récupération Systemd User Service Lifecycle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le Systemd User Service Lifecycle.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (83%)`
- Justification : le runtime en avant-plan est documenté de la commande CLI aux vérifications de disponibilité, et le code source couvre la garde de démarrage, la coordination des verrous, la sécurité de l'authentification non-loopback, la gestion des redémarrages et l'ajustement des processus Linux.
- Lacunes : les docs et les références CLI ne mettent pas toutes les signatures d'échec du foreground Linux au même endroit.

## Score de qualité

- Score : `Stable (80%)`
- Justification : le chemin foreground normal est cohérent et gardé, mais les preuves d'archive actuelles montrent toujours des corrections récentes autour des courses de démarrage, des jetons de redémarrage et des incompatibilités d'options.
- Exclu de la qualité : preuves de tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.

## Score de complétude

- Score : `Stable (83%)`
- Instructions de surface : évaluées par rapport à `references/completeness/linux-gateway-host.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le Foreground Gateway Runtime, le Process Control, la configuration du Systemd User Service Lifecycle, l'opération du Systemd User Service Lifecycle, le statut du Systemd User Service Lifecycle, la récupération du Systemd User Service Lifecycle.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 des processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Aligner la gestion des options `gateway run`, health et probe afin que les opérateurs puissent réutiliser les options port/bind de manière cohérente.
- Ajouter un tableau court de dépannage du foreground Linux pour les symptômes de verrou, port en utilisation, disponibilité, authentification et redémarrage.

## Preuves

### Docs

- `docs/gateway/index.md:25-48` documente le démarrage, le statut, les journaux et une ligne de base saine.
- `docs/gateway/index.md:71-83` décrit le modèle de runtime Gateway toujours actif, le port unique, la valeur par défaut loopback, l'exigence d'authentification et les sources de secrets config/env.
- `docs/cli/gateway.md:25-48` documente les alias foreground, le comportement de la garde de démarrage, la garde d'authentification non-loopback, la mise en garde IPv4, le redémarrage SIGUSR1 et la gestion des signaux.
- `docs/cli/gateway.md:53-112` documente les options port, bind, auth, token/password, Tailscale, force, verbose et log.
- `docs/cli/gateway.md:130-170` documente le profilage, les benchmarks de démarrage/redémarrage, les sondes de santé et les vérifications WebSocket RPC.

### Source

- `src/cli/gateway-cli/run.ts:107-120` mappe les erreurs de configuration au comportement de sortie stable et définit les modes auth/Tailscale.
- `src/cli/gateway-cli/run.ts:223-232` bloque la liaison non-loopback sans authentification explicite.
- `src/cli/gateway-cli/run-loop.ts:59-97` attend la disponibilité du port et un processus enfant sain.
- `src/cli/gateway-cli/run-loop.ts:99-123` coordonne la boucle d'exécution Gateway avec la gestion des verrous et les importations de cycle de vie qui survivent aux mises à jour de paquets.
- `src/process/linux-oom-score.ts:3-27` documente la politique de score OOM des processus enfants Linux et la clé d'environnement de désactivation.

### Tests d'intégration

- `src/cli/gateway-cli/run.supervised-lock.test.ts` couvre le comportement du code de sortie et les conflits de verrous systemd sains.
- `src/gateway/server-http.probe.test.ts` couvre le comportement des sondes de santé et de disponibilité.
- `src/gateway/server/http-listen.test.ts` couvre le comportement de nouvelle tentative d'écoute sur les erreurs d'adresse en utilisation.

### Tests unitaires

- `src/infra/gateway-lock.test.ts` couvre le comportement des verrous.
- `src/process/linux-oom-score.test.ts` couvre les décisions du wrapper de processus Linux.
- `src/cli/gateway-run-argv.test.ts` couvre la construction des arguments de gateway run.

### Requêtes Gitcrawl

- La requête spécifique `openclaw gateway run foreground Linux process lock port startup readiness` n'a retourné aucun résultat.
- La requête plus large `gateway run` a retourné la PR #83489 pour une course de démarrage du service Gateway, le problème #79100 pour `gateway health/probe` rejetant `--port` tandis que `gateway run` l'accepte, la PR #84334 pour la gestion des jetons SIGUSR1 au redémarrage systemd, la PR #82894 pour le préchauffage du runtime avant la disponibilité et la PR #66735 pour la transmission du redémarrage automatique systemd.

### Requêtes Discrawl

- La requête `gateway run port` a trouvé une discussion d'opérateur sur les exigences `wss://` pour l'accès iOS/VPS, les mappages loopback hébergés, Docker compose exposant le port 18789 et les exemples `--host`/`--port` de node run.
