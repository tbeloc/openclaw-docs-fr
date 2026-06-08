---
title: "Observabilité - Note de Maturité du Moniteur de Santé des Canaux"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité du Moniteur de Santé des Canaux

## Résumé

Le moniteur de santé des canaux offre aux opérateurs un comportement de redémarrage automatique pour les runtimes de canaux obsolètes, déconnectés, arrêtés et bloqués. Il dispose d'une logique de politique solide, de limites de débit, de périodes de refroidissement et de remplacements par compte, mais les preuves d'archives en direct montrent que ce domaine reste une source fréquente de confusion et de demandes de réparation spécifiques aux canaux.

## Portée de la Catégorie

- Boucle de moniteur de santé en arrière-plan pour les comptes de canaux configurés.
- Paramètres d'activation/désactivation par compte.
- Grâce au démarrage, grâce à la connexion, détection d'activité de transport obsolète, gestion des occupations/blocages, refroidissements de redémarrage et redémarrages maximum par heure.
- Journalisation des redémarrages et évaluation des snapshots de runtime.
- Adjacent mais hors de portée : propositions manuelles `channels.start` / `channels.stop` / `channels.restart`, qui ne sont pas encore la même fonctionnalité.

## Fonctionnalités

- Boucle de moniteur de santé en arrière-plan : Boucle de moniteur de santé en arrière-plan pour les comptes de canaux configurés
- Paramètres d'activation/désactivation par compte : Comportement, statut et vérification visibles par l'opérateur des paramètres d'activation/désactivation par compte.
- Grâce au démarrage : Grâce au démarrage, grâce à la connexion, détection d'activité de transport obsolète, gestion des occupations/blocages, refroidissements de redémarrage et redémarrages maximum par heure
- Journalisation des redémarrages : Journalisation des redémarrages et évaluation des snapshots de runtime

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (82%)`
- Signaux positifs : Le moniteur et la politique disposent de tests ciblés pour les fenêtres de grâce, les sockets obsolètes, les canaux occupés bloqués, les comptes désactivés, les arrêts manuels, les refroidissements et les plafonds horaires.
- Signaux négatifs : La preuve en direct varie selon le canal en amont et n'est pas également représentée sur tous les fournisseurs qui exposent les paramètres du moniteur de santé.
- Lacunes d'intégration : L'archive montre des scénarios de dégradation réels de Discord, Telegram, WhatsApp, Weixin et Feishu qui nécessitent une preuve de fumée de version récurrente.

## Score de Qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : Plusieurs problèmes en direct et PR se regroupent autour de l'état de santé des canaux, des redémarrages bloqués/déconnectés et des demandes des opérateurs pour la récupération manuelle des canaux.
- Rapports Discrawl : Les fils de support montrent que les redémarrages du moniteur de santé peuvent être utiles mais aussi difficiles à interpréter lorsqu'une passerelle reste active tandis qu'un canal/compte est dégradé.
- Bonnes qualités : L'implémentation utilise une politique neutre par rapport au fournisseur, des horodatages d'activité de transport explicites, des vérifications à vol unique, des refroidissements et des plafonds de redémarrage.
- Mauvaises qualités : Le comportement du moniteur de santé apparaît toujours comme un sujet d'assistance car les runtimes de canaux peuvent être bruyants, spécifiques en amont et difficiles à réparer sans redémarrage complet de la passerelle.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux de runtime ne sont comptées que sous Couverture, pas Qualité.

## Score de Complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la Boucle de moniteur de santé en arrière-plan, les Paramètres d'activation/désactivation par compte, la Grâce au démarrage, la Journalisation des redémarrages.
- Signaux négatifs : la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Les opérateurs manquent toujours d'un flux de redémarrage de canal manuel entièrement documenté pour les comptes bloqués.
- Certaines versions plus anciennes manquaient de clés de configuration de moniteur par canal, ce qui apparaît dans l'archive Discord comme une friction de validation de schéma.

## Preuves

### Docs

- `docs/gateway/health.md` documente `gateway.channelHealthCheckMinutes`, `gateway.channelStaleEventThresholdMinutes`, `gateway.channelMaxRestartsPerHour` et les remplacements de moniteur par fournisseur/compte.
- Les docs de canaux tels que `docs/channels/telegram.md` et `docs/channels/discord.md` décrivent les blocages d'interrogation, les délais d'expiration READY du runtime et les redémarrages pilotés par le moniteur.

### Source

- `src/gateway/channel-health-monitor.ts` implémente la boucle en arrière-plan, l'itération des comptes, le refroidissement du redémarrage, le plafond horaire, la journalisation des redémarrages et les appels d'arrêt/démarrage.
- `src/gateway/channel-health-policy.ts` implémente les vérifications de compte géré, la classification occupée/bloquée, la grâce au démarrage, l'état déconnecté, l'activité de transport obsolète et le mappage des raisons de redémarrage.
- `src/gateway/server-channels.ts` câble l'activation du moniteur et la résolution des comptes dans les snapshots de runtime des canaux.
- `src/config/types.gateway.ts` et les schémas de configuration des canaux exposent le minutage du moniteur et les paramètres par fournisseur.

### Tests d'intégration

- `src/gateway/server-reload-handlers.ts` et les tests associés couvrent le redémarrage du moniteur de santé lorsque le rechargement de la configuration modifie les champs surveillés.
- Les scripts e2e de canal en direct tels que `scripts/e2e/npm-telegram-live-docker.sh` et les scripts de parcours utilisateur de version exécutent le docteur et les flux de canal qui peuvent révéler les régressions du moniteur.

### Tests unitaires

- `src/gateway/channel-health-monitor.test.ts` couvre le redémarrage, l'omission, la grâce, le plafond, le refroidissement, le socket obsolète et le comportement d'arrêt.
- `src/gateway/channel-health-policy.test.ts` couvre les raisons d'évaluation et le mappage des raisons de redémarrage.
- `src/config/schema.test.ts` inclut les entrées de schéma de configuration de santé des canaux de passerelle.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "gateway health status probe channel health monitor" --limit 5`

Résultats :

- 5 résultats. Les signaux pertinents incluent la PR #80805 restaurant la réactivité de la santé des canaux, le problème #75153 demandant la récupération manuelle des canaux après les redémarrages du moniteur de santé, le problème #79304 sur les délais d'expiration d'initialisation du runtime Weixin et la PR #76701 supprimant le bruit du délai d'expiration du ping du bot Feishu.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "gateway health status probe channel health monitor"`

Résultats :

- 5 résultats. Les exemples d'archive Discord incluent `health-monitor: restarting (reason: stuck)`, `health-monitor: restarting (reason: disconnected)`, `Polling stall detected` et les échecs de schéma de version plus ancienne pour `channels.telegram.healthMonitor.enabled` et `channels.discord.healthMonitor.enabled`.
