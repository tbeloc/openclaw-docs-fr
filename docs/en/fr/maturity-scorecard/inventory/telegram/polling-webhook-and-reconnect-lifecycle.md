---
title: "Telegram - Runtime Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Telegram - Runtime Lifecycle Maturity Note

## Résumé

Le cycle de vie du runtime Telegram est un composant réellement en version Bêta. Le long polling est le mode par défaut, le mode webhook est documenté et implémenté, et le runtime inclut désormais les baux, la persistance des décalages, l'ingress isolé, la surveillance de la vivacité du watchdog, le basculement réseau et les problèmes de statut. Le composant reste en dessous de Stable en raison des preuves d'archive montrant des régressions récentes autour des blocages de polling, du comportement IPv6/transport et de la récupération spécifique à l'hôte.

## Portée de la catégorie

Inclus dans cette catégorie :

- Démarrage du runner de long polling : démarrage du runner de long polling, protection contre les pollers dupliqués, mise à jour des décalages et cycle de vie du compte.
- Démarrage du listener webhook : démarrage du listener webhook, validation des secrets, dispatch d'événements asynchrone et local
- Reconnexion : reconnexion, erreurs réseau récupérables, getUpdates bloqué, pinces de délai d'attente et gestion de la récupération.
- Redémarrage : comportement de redémarrage et de récupération après rotation de jeton, arrêts de processus et rechargements de compte.

## Fonctionnalités

- Démarrage du runner de long polling : démarrage du runner de long polling, protection contre les pollers dupliqués, mise à jour des décalages et cycle de vie du compte.
- Démarrage du listener webhook : démarrage du listener webhook, validation des secrets, dispatch d'événements asynchrone et local
- Reconnexion : reconnexion, erreurs réseau récupérables, getUpdates bloqué, pinces de délai d'attente et gestion de la récupération.
- Redémarrage : comportement de redémarrage et de récupération après rotation de jeton, arrêts de processus et rechargements de compte.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Bêta (78%)`
- Signaux positifs :
  les chemins de démarrage du polling, webhook, timeout, lease, liveness, status, network et gateway
  ont des tests ciblés, et les harnais package/live exercent des allers-retours réels
  avec l'API Telegram Bot.
- Signaux négatifs :
  la preuve en direct récurrente est concentrée sur les réponses aux mentions de groupe et les chemins de commande,
  pas la matrice complète de redémarrage sur les hôtes, l'ingress webhook, les environnements proxy
  et la rotation de jeton.
- Lacunes d'intégration :
  ajouter une preuve de version pour le mode webhook, la récupération des conflits webhook actifs, le basculement IPv6,
  le comportement réseau WSL2/VPS et la récupération du long-poll bloqué.

## Score de qualité

- Score : `Bêta (72%)`
- Rapports Gitcrawl :
  le cycle de vie du polling et du réseau reste actif : #86535, #86541, #73884, #75498,
  #73602 et #86031.
- Rapports Discrawl :
  les utilisateurs ont signalé des plantages de long-poll après 20-30 minutes, les mainteneurs ont lié ces
  rapports aux travaux de stabilité du polling et des canaux Telegram, et les notes de version
  appellent à plusieurs reprises le durcissement de la récupération/inbox Telegram.
- Bonnes qualités :
  le runtime persiste les décalages uniquement après le dispatch, refuse les pollers dupliqués,
  reconstruit les transports sales, limite la récupération réseau aux erreurs de polling et
  affiche le statut de polling obsolète.
- Mauvaises qualités :
  la mise en réseau de l'hôte, le comportement du proxy, les lacunes de sommeil et le comportement du transport de l'API Bot
  créent toujours une instabilité visible par l'opérateur et une charge de support.
- Exclu de la qualité :
  la couverture unitaire, la couverture d'intégration, l'étendue de l'assurance qualité en direct et le nombre de tests n'ont pas
  été utilisés comme entrées de qualité.

## Score de complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telegram.md`.
- Signaux positifs : les preuves d'archive, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le démarrage du runner de long polling, le démarrage du listener webhook, la reconnexion et le redémarrage.
- Signaux négatifs : la note archivée a précédé le scoring de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même étendue de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve webhook en direct et une preuve de récupération des conflits à côté de la preuve de long-poll.
- Enregistrer la fumée de version par classe d'hôte pour VPS, WSL2, réseaux IPv6-first et
  l'egress de l'API Telegram Bot en proxy.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/telegram.md` documente les valeurs par défaut du long
  polling, le mode webhook, la persistance des décalages, les seuils de blocage du polling,
  les pinces de délai d'attente, les contrôles proxy/DNS et le dépannage.
- `/Users/kevinlin/code/openclaw/docs/channels/troubleshooting.md` est lié pour
  les diagnostics inter-canaux.

### Source

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/monitor.ts` sélectionne
  le mode webhook ou polling, enregistre le contexte du runtime d'approbation, acquiert les baux de polling,
  persiste les décalages et redémarre après les défaillances réseau récupérables.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/monitor-polling.runtime.ts`
  possède la session de polling et le watchdog.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/monitor-webhook.runtime.ts`
  possède le démarrage et le dispatch du webhook.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/polling-lease.ts`,
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/polling-status.ts`
  et `/Users/kevinlin/code/openclaw/extensions/telegram/src/status-issues.ts`
  implémentent les surfaces de bail et de statut opérateur.
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/fetch.ts` et
  `/Users/kevinlin/code/openclaw/extensions/telegram/src/network-errors.ts`
  implémentent le transport, le proxy, le DNS et la politique d'erreur récupérable.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-rtt-driver.mjs`
  vérifie l'API Bot `getMe`, `sendMessage` et `getUpdates` par rapport aux
  identifiants Telegram réels.
- `/Users/kevinlin/code/openclaw/scripts/e2e/npm-telegram-live-runner.ts`
  exécute les scénarios en direct Telegram installés par package.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/telegram/telegram-live.runtime.ts`
  définit les scénarios de canari en direct, commande, mention, réponse et streaming.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/telegram/src/monitor.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/polling-session.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/polling-liveness.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/polling-lease.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/webhook.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/webhook-status.test.ts`
- `/Users/kevinlin/code/openclaw/extensions/telegram/src/request-timeouts.test.ts`

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "polling stall" --json`

Résultats :

- #86535 problème ouvert : le détecteur de blocage de polling traite le sommeil comme un blocage
  `getUpdates` actif.
- #86541 PR ouvert : ignorer les lacunes de sommeil du polling.
- #73884 PR ouvert : éviter les redémarrages de blocage de polling faux.
- #75498 problème ouvert : réponses Telegram Web UI uniquement, streaming partiel, blocage du polling
  et pollution de session après mise à niveau.
- #73602 problème ouvert : WhatsApp flaps et blocages de polling Telegram sur WSL2.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "telegram polling stall"`

Résultats :

- `users-helping-users`, 2026-05-12 : le long polling Telegram a cessé de répondre
  à plusieurs reprises après 20-30 minutes sur un VPS.
- `maintainers`, 2026-05-12 : les mainteneurs ont lié plusieurs rapports de configuration Telegram
  au problème #78473.
- `releases`, 2026-05-14 : les notes de version ont appelé le worker isolé, la bobine locale durable
  et la détection de blocage basée sur `getUpdates`.
