---
title: "WhatsApp - Note de Maturité du Reconnexion et du Médecin de Santé d'Exécution"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# WhatsApp - Note de Maturité du Reconnexion et du Médecin de Santé d'Exécution

## Résumé

La santé d'exécution WhatsApp, la reconnexion et le comportement du médecin sont en Bêta. La source dispose d'un véritable contrôleur de connexion avec des instantanés d'état d'authentification, un backoff de reconnexion, une logique de battement cardiaque/surveillance, une détection de transport obsolète/silence d'application, des problèmes de statut, un arrêt et des vérifications de réactivité du médecin. La qualité reste en Bêta car les preuves d'archive montrent toujours une volatilité de socket obsolète, de tempête de reconnexion et de session Baileys dans les flux de travail d'opérateur actuels.

## Portée de la Catégorie

- Cycle de vie du socket Baileys, état du contrôleur de connexion, décisions de reconnexion, politique de battement cardiaque et surveillance, adaptateur de statut, activité d'écouteur actif, comportement de redémarrage de la Passerelle et vérifications de réactivité du médecin.
- Dépannage d'opérateur pour les boucles de reconnexion, les sockets obsolètes, les avertissements d'exécution Bun/Node et les états sans écouteur actif/fournisseur accepté.
- Hors de portée : la connexion QR de première fois elle-même et la sémantique des fonctionnalités de message après l'existence d'un écouteur sain.

## Fonctionnalités

- Cycle de vie du socket Baileys : Cycle de vie du socket Baileys, état du contrôleur de connexion, décisions de reconnexion et statut de réparation.
- Dépannage d'opérateur : Dépannage d'opérateur pour les boucles de reconnexion, les sockets obsolètes, Bun/Node

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de Couverture

- Score : `Bêta (78%)`
- Signaux positifs : la documentation décrit le comportement de reconnexion et le dépannage ; la source centralise l'état du contrôleur, les décisions de reconnexion, le battement cardiaque/surveillance, l'activité d'écouteur actif, l'arrêt, le statut d'authentification et les problèmes de statut du médecin ; les tests d'exécution couvrent le comportement de reconnexion et de surveillance.
- Signaux négatifs : les preuves d'archive actuelles incluent le blocage de la boucle d'événements, les tempêtes de reconnexion, les sockets obsolètes et les oscillations WSL2/timeout.
- Lacunes d'intégration : aucun scénario en direct localisé ne prouve continuellement la détection de socket obsolète, le redémarrage de silence d'application, le redémarrage de silence de transport, le redémarrage de la Passerelle, la réactivité du médecin et la récupération d'opérateur dans une seule voie.

## Score de Qualité

- Score : `Bêta (72%)`
- Rapports Gitcrawl : `whatsapp reconnect watchdog Baileys gateway restart` a surfacé #78165 pour `channels.whatsapp.start-account` bloquant la boucle d'événements et déclenchant des tempêtes de reconnexion, plus #73602 pour les oscillations WSL2 Baileys 405/timeout de reconnexion.
- Rapports Discrawl : la même requête a retourné une discussion de socket obsolète où un watchdog de 30 minutes émet le statut 499 et la logique de socket obsolète peut redémarrer même si le socket est sain, avec la solution de contournement `gateway.channelHealthCheckMinutes: 0`.
- Bonnes qualités : la politique de reconnexion est explicite, les seuils de battement cardiaque sont limités, les instantanés de statut distinguent l'authentification et l'état du contrôleur, l'activité d'écouteur actif est suivie et la documentation du médecin connecte les sockets obsolètes aux actions d'opérateur.
- Mauvaises qualités : l'exécution repose sur WhatsApp Web et le comportement de Baileys en dehors du contrôle d'OpenClaw, et les heuristiques de socket obsolète peuvent être bruyantes sur les hôtes lents, WSL2 ou les hôtes avec des blocages de boucle d'événements.
- Exclu de la qualité : la couverture des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution réel n'a pas augmenté ni diminué ce score de Qualité.

## Score de Complétude

- Score : `Bêta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/whatsapp.md`.
- Signaux positifs : les preuves de documentation archivée, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le cycle de vie du socket Baileys, le dépannage d'opérateur.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter une preuve de santé en direct à long terme pour les sockets obsolètes, les redémarrages de Passerelle, les redémarrages de battement cardiaque et la sortie du médecin.
- Réduire les faux positifs dans les heuristiques de socket obsolète ou faciliter l'ajustement de la vérification de santé pour les hôtes contraints.
- Séparer les erreurs du fournisseur Baileys, les blocages de boucle d'événements d'hôte et les défaillances d'écouteur de Passerelle dans les diagnostics visibles par l'opérateur.

## Preuves

### Documentation

- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:155` documente le socket détenu par la Passerelle, la boucle de reconnexion, l'exigence d'écouteur actif et le comportement du proxy.
- `/Users/kevinlin/code/openclaw/docs/channels/whatsapp.md:592` documente le dépannage pour les boucles de reconnexion, le proxy QR, l'absence d'écouteur actif, l'acceptation du fournisseur, le groupe ignoré et les avertissements Bun.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:149` documente les avertissements de migration d'authentification WhatsApp hérités.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:173` et `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:354` documentent les vérifications de réactivité de WhatsApp.
- `/Users/kevinlin/code/openclaw/docs/gateway/doctor.md:553` documente les avertissements Node par rapport à Bun/gestionnaire de version.

### Source

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/session.ts:132` crée le socket Baileys, le magasin d'authentification, récupère la version, gère l'agent proxy, QR, la mise à jour de connexion et l'état de déconnexion.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/session.ts:313` attend la connexion.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/connection-controller.ts:189` gère l'attente de connexion, le redémarrage 515 et l'effacement déconnecté.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/connection-controller.ts:262` maintient l'état du contrôleur et les instantanés de reconnexion.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/connection-controller.ts:487` décide du comportement de reconnexion et de backoff.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/connection-controller.ts:607` implémente les vérifications de battement cardiaque et de surveillance pour le silence de transport et d'application.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/reconnect.ts:14` définit la politique de battement cardiaque et de reconnexion par défaut.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/status-issues.ts:1` expose les problèmes de statut WhatsApp.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/doctor.ts:1` implémente les vérifications du médecin WhatsApp.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply.web-auto-reply.connection-and-logging.e2e.test.ts:147` couvre le comportement de reconnexion.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/auto-reply.web-auto-reply.connection-and-logging.e2e.test.ts:522` couvre le comportement de surveillance et de silence calme/transport/application.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:489` attend l'état de canal en cours d'exécution et stable.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/whatsapp/whatsapp-live.runtime.ts:1192` exécute l'assurance qualité en direct avec bail de credential, déballage d'archive d'authentification, nouvelle tentative de pilote et artefacts.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/connection-controller.test.ts:47` couvre l'état du contrôleur de connexion, la barrière d'authentification, les instantanés, l'activité de transport et le comportement de blocage.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/reconnect.test.ts:1` couvre la politique de reconnexion.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/status-issues.test.ts:1` couvre le comportement des problèmes de statut.
- `/Users/kevinlin/code/openclaw/extensions/whatsapp/src/doctor.test.ts:1` couvre le comportement du médecin.
- `/Users/kevinlin/code/openclaw/src/commands/doctor-whatsapp-responsiveness.test.ts:19` couvre les vérifications de réactivité du médecin et le comportement du processus TUI local.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "whatsapp reconnect watchdog Baileys gateway restart" --json`

Résultats :

- A surfacé #78165 où `channels.whatsapp.start-account` bloque la boucle d'événements pendant environ 40 secondes et déclenche une tempête de reconnexion.
- A surfacé #73602 où WhatsApp oscille et l'interrogation Telegram s'arrête sur WSL2 avec les reconnexions Baileys 405/timeout.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl --json search "whatsapp reconnect watchdog Baileys gateway restart" --limit 5`

Résultats :

- A retourné une discussion de socket obsolète où un watchdog de 30 minutes émet le statut 499 et la logique de socket obsolète peut redémarrer même si le socket est sain ; la solution de contournement est notée comme `gateway.channelHealthCheckMinutes: 0`.
