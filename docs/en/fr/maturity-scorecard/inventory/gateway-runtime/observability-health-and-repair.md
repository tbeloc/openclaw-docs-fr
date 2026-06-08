---
version: 3
---

# Matrice des fonctionnalités WebSocket du runtime Gateway - Santé, diagnostics et réparation

## Résumé

L'observabilité, la santé et la réparation sont largement implémentées : Gateway expose des snapshots de santé/statut, des sondes HTTP de vivacité/disponibilité, des sondes de lecture WebSocket, des sondes de disponibilité de canal, `logs.tail`, `openclaw logs --follow`, des diagnostics de stabilité, l'export de diagnostics, les diagnostics déclenchés par chat, et une large surface de réparation/vérification `doctor`. La couverture est **Partielle** car il existe des preuves réelles de flux Gateway/serveur pour le comportement de santé/disponibilité et de sonde WebSocket, mais l'export de diagnostics, la persistance du enregistreur de stabilité, la récupération du suivi de journal et la plupart des boucles de réparation doctor sont couverts principalement par des tests au niveau unitaire/commande plutôt que par des scénarios réels de Gateway ou de réparation supervisée.

La qualité est **Moyenne** car la confidentialité/la rédaction et la conception diagnostique bornée sont solides, mais les recherches d'archives montrent des décalages récurrents de santé/statut, des faux négatifs/faux avertissements doctor, des régressions de diagnostics, des bugs de fiabilité de suivi de journal et des lacunes d'attentes d'opérateurs autour de la profondeur de réparation doctor.

## Fonctionnalités

- Snapshots de santé : snapshots `health` et `status`.
- Disponibilité du canal : sondage de disponibilité du canal via la Gateway en cours d'exécution.
- Diagnostics de stabilité : sortie de l'enregistreur de stabilité.
- Diagnostics de charge utile : diagnostics `payload.large`.
- Exports de diagnostics : contenu d'export de diagnostics, modèle de confidentialité et déclencheurs CLI/chat.
- Vérifications Doctor : vérifications doctor pour la fraîcheur du protocole UI, la dérive de service, la dérive d'authentification/appairage, les collisions de port, les meilleures pratiques sandbox/runtime et les problèmes d'installation source.
- Suivi de journal : suivi de journal et visibilité des signaux opérationnels.

## Fraîcheur de l'archive

- `gitcrawl doctor --json` : `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `api_supported=false`, `github_token_present=false`, `repository_count=2`.
- `discrawl status --json` : `generated_at=2026-05-30T00:04:12Z`, `state=current`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `share.needs_update=true`.

## Couverture

Score : **68**

Étiquette : **Partielle**

Signaux positifs :

- Les docs Gateway exposent une ligne de base de santé d'opérateur avec `openclaw gateway status`, `openclaw status` et `openclaw logs --follow`, plus `gateway status --require-rpc` pour la preuve RPC de portée lecture dans `docs/gateway/index.md:40`.
- Le sondage de disponibilité du canal est documenté comme sondage en direct par compte lorsque Gateway est accessible, avec repli sur configuration uniquement lorsqu'il ne l'est pas, dans `docs/gateway/index.md:52`.
- Les attentes de vivacité/disponibilité/récupération d'écart opérationnels sont documentées autour de la connexion WebSocket/`hello-ok`, `gateway status`, `channels status --probe`, `health` et `system-presence` dans `docs/gateway/index.md:331`.
- Les docs d'export de diagnostics décrivent le statut assaini, la santé, les journaux, la forme de configuration et les événements de stabilité sans charge utile, plus l'approbation explicite par chat et le routage de groupe privé, dans `docs/gateway/diagnostics.md:10` et `docs/gateway/diagnostics.md:36`.
- Les docs Doctor énumèrent la fraîcheur du protocole UI, les invites de redémarrage de santé, la réparation sandbox, la dérive de service, les avertissements de statut de canal, la dérive d'authentification/appairage, les vérifications de meilleures pratiques runtime et les diagnostics de port dans `docs/gateway/doctor.md:131` et `docs/gateway/doctor.md:525`.
- Les gestionnaires RPC Gateway principaux exposent `health`, `status`, `channels.status`, `logs.tail` et `diagnostics.stability` via la table de méthode WebSocket dans `src/gateway/server-methods.ts:248`.
- Il existe une preuve réelle de flux Gateway/serveur pour les points de terminaison de sonde HTTP et la vivacité/disponibilité de pré-étape dans `src/gateway/server-http.probe.test.ts:36`, `src/gateway/server-http.probe.test.ts:246` et `src/gateway/server-http.probe.test.ts:289`.
- Il existe une preuve réelle de flux Gateway/serveur pour le comportement de sonde WebSocket authentifiée, les sondes non-mutantes de première fois et les sondes de détail de périphérique en cache retournant des snapshots de santé/statut/configuration dans `src/gateway/probe.auth.integration.test.ts:71`.

Signaux négatifs :

- L'export de diagnostics a une couverture unitaire et des docs solides, mais aucune preuve E2E chat-à-approbation-à-export en direct n'a été trouvée pour une conversation réelle Gateway/canal.
- La couverture de l'enregistreur de stabilité est synthétique dans `src/gateway/gateway-stability.test.ts:31` ; aucun scénario réel de charge Gateway/sortie fatale/bundle persisté n'a été trouvé.
- Doctor a des docs larges et de nombreux tests ciblés, mais les boucles de réparation pour la fraîcheur du protocole UI, la dérive de service, la dérive d'authentification/appairage, la récupération de collision de port, les problèmes d'installation source et les meilleures pratiques sandbox/runtime ne sont pas couverts comme un flux réel Gateway ou de réparation supervisée.
- `openclaw logs --follow` a des tests au niveau commande et des correctifs historiques, mais aucune preuve réelle de déconnexion/reconnexion Gateway transitoire n'a été trouvée dans les preuves actuelles.

Lacunes d'intégration :

- Aucune preuve de flux chat `/diagnostics` de bout en bout via Telegram/Discord/autre canal, approbation exec, export CLI, route de groupe privé et rapport final.
- Aucune preuve d'export de diagnostics en direct contre une Gateway réellement malsaine où le statut/la santé échouent mais les journaux/configuration/stabilité locaux sont toujours collectés.
- Aucune preuve d'enregistreur de stabilité en direct pour le churn de session Gateway réel, `payload.large`, la persistance du bundle de sortie fatale et `gateway stability --bundle latest`.
- Aucune preuve de réparation doctor en direct qui commence à partir d'un état de service/configuration/authentification/appairage/port/UI/installation source obsolète et vérifie le comportement Gateway réparé par la suite.
- Aucune preuve réelle de reconnexion `logs --follow` contre une Gateway en cours d'exécution qui est brièvement arrêtée/redémarrée.

## Qualité

Score : **62**

Label : **Moyen**

### Rapports gitcrawl

- La requête `gitcrawl search openclaw/openclaw --query "gateway diagnostics" --mode keyword --limit 10 --json` a retourné 10 résultats, incluant la PR fermée #70324 « Improve gateway diagnostics export for support reports », l'issue ouverte #72883 « gateway config.patch blocks diagnostics.cacheTrace.* even with content capture disabled », les régressions diagnostics OpenTelemetry/Prometheus fermées #18794, #3201, #4317, #77206, #77390, la PR #75928 pour le support diagnostics cron/run, et les PRs #74560/#74561 autour des régressions de contrat diagnostics.
- La requête `gitcrawl search openclaw/openclaw --query "gateway doctor" --mode keyword --limit 10 --json` a retourné 10 résultats : PR ouverte #84340 « Doctor: expose extra gateway service findings » ; PRs fermées #69947, #69896, #53197 ; PR ouverte #84224 « fix(doctor): handle gateway SecretRefs in auth checks » ; PR fermée #80055 « Doctor: add health-check contract and --lint validation » ; PRs ouvertes #62338, #83715, #86627 ; PR docs fermée #77613.
- La requête `gitcrawl search openclaw/openclaw --query "gateway health status" --mode keyword --limit 10 --json` a retourné 10 résultats : issue fermée #13602, PRs fermées #36422, #80277, #57374, issues fermées #71974, #49758, #27619, #59287, #59511, et issue ouverte #42538 « Bug: health endpoint returns incorrect running=false for WhatsApp ».
- La requête `gitcrawl search openclaw/openclaw --query "payload.large stability diagnostics" --mode keyword --limit 10 --json` a retourné 6 résultats : PRs fermées #70324, #82674, #82937, PRs ouvertes #86160 et #81402, et issue fermée #83795.
- La requête `gitcrawl search openclaw/openclaw --query "gateway port collision doctor service drift" --mode keyword --limit 10 --json` a retourné 1 résultat : PR fermée #84475 « fix(gateway): include openclaw bin in service PATH ».
- La requête `gitcrawl search openclaw/openclaw --query "openclaw logs follow gateway" --mode keyword --limit 10 --json` a retourné 10 résultats : PRs fermées #45140, #75059, #56475, #75372 et issues fermées #74782, #66841, #74583, #83656, #32986, #45080.

### Rapports discrawl

- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway diagnostics"` a retourné 10 résultats, menés par le rapport de mainteneur du 2026-05-27 indiquant que le travail qualité/diagnostics couvrait les suivis de redémarrage doctor, la signalisation des verrous de session obsolètes, la persistance des transcriptions, les conseils de nettoyage des répertoires temporaires et la couverture d'aperçu Telegram, plus un rapport clawtributor du 2026-05-25 indiquant que les travaux de rafraîchissement/heartbeat/cron de la santé de la passerelle pourraient interférer avec les exécutions de réponse actives et qu'un profileur opt-in peut être activé avec `OPENCLAW_DIAGNOSTICS=profiler openclaw gateway run`.
- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway doctor"` a retourné 10 résultats, incluant un rapport de bug du 2026-05-27 indiquant qu'un schéma d'outil dynamique non supporté a planté un tour d'assistant tandis que `openclaw doctor` n'a pas détecté le problème de schéma fatal, un rapport du 2026-05-26 indiquant qu'une passerelle lente n'a pas été aidée par doctor, et un rapport PR #84224 sur les faux avertissements SecretRef dans doctor/lint.
- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway health status"` a retourné 10 résultats, incluant les notes de mainteneur du 2026-05-25 sur les sondes de santé/cycle de vie de la passerelle, les commandes utilisateur du 2026-05-21 pour `gateway stop`, `gateway restart` et `gateway status --deep`, la vérification de santé réelle du 2026-05-16 `200 {"ok":true,"status":"live"}`, les plaintes de commande CLI lente du 2026-05-12, et les bizarreries de mise à niveau/redémarrage/sonde du 2026-05-11.
- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "payload.large stability diagnostics"` a retourné 0 résultats.
- La requête `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "logs --follow gateway"` a retourné 10 résultats, incluant un rapport Slack Socket Mode du 2026-05-25 où `openclaw logs --follow` n'a montré aucun événement de message entrant malgré une connectivité apparente, et les notes de version bêta demandant aux testeurs de fournir des extraits de journal pour les régressions de passerelle/canal.

### Bonnes qualités

- La santé/statut sont unifiés derrière la RPC de la passerelle et réutilisent la santé mise en cache avec des vérifications de dérive d'exécution, le mode sonde, les champs sensibles à l'administrateur et la santé de la boucle d'événements dans `src/gateway/server-methods/health.ts:99`.
- Les sondes de passerelle ne sont pas mutantes jusqu'à l'existence d'un jeton d'appareil opérateur mis en cache, utilisent l'identité CLI de portée de lecture et récupèrent les instantanés de santé/statut/présence/config après `hello-ok` dans `src/gateway/probe.ts:223` et `src/gateway/probe.ts:356`.
- Le sondage de disponibilité du canal exécute les hooks de plugin `probeAccount` et `auditAccount` uniquement lorsqu'ils sont demandés et configurés, avec la tuyauterie timeout/avertissement dans `src/gateway/server-methods/channels.ts:285`.
- Les enregistrements de stabilité sont intentionnellement des faits opérationnels sans charge utile avec une capacité limitée, des résumés pour la mémoire et `payload.large`, et des identifiants de session édités dans `src/logging/diagnostic-stability.ts:14`, `src/logging/diagnostic-stability.ts:509` et `src/logging/diagnostic-stability.ts:569`.
- L'export de diagnostics construit un manifeste avec `payloadFree: true` et `rawLogsIncluded: false`, inclut des fichiers config/log/status/health/stability assainis et enregistre les notes de confidentialité dans `src/logging/diagnostic-support-export.ts:58` et `src/logging/diagnostic-support-export.ts:548`.
- La rédaction est explicite pour les secrets, les champs de charge utile, les identifiants, les champs de config privés, les préfixes de chemin, les messages de journal non sûrs et les champs de journal non sûrs dans `src/logging/diagnostic-support-redaction.ts:8` et `src/logging/diagnostic-support-log-redaction.ts:8`.
- `openclaw logs --follow` réessaie les erreurs de transport transitoires, évite les boucles sur les défaillances d'authentification/politique/appairage, émet des avis de reconnexion et supporte la parité des avis JSON dans `src/cli/logs-cli.ts:323` et `src/cli/logs-cli.ts:526`.
- Doctor est intentionnellement large et dispose de garde-fous pour la dérive de service, les unités systemd actives, la propriété du superviseur externe, la fraîcheur du protocole UI, les images Docker sandbox, les diagnostics de port et les meilleures pratiques de chemin d'exécution (`src/commands/doctor-gateway-services.ts:528`, `src/commands/doctor-ui.ts:13`, `src/commands/doctor-sandbox.ts:279`, `src/daemon/service-audit.ts:47`).

### Mauvaises qualités

- L'archive montre des régressions répétées dans la correction de la santé/statut pour l'état d'exécution du canal, en particulier WhatsApp et Telegram (`gitcrawl` #71974, #42538, #59287).
- Doctor n'est toujours pas un oracle complet de disponibilité d'exécution : les rapports Discord montrent qu'il a manqué les défaillances fatales de projection de schéma d'outil actif et n'a pas aidé un cas de passerelle lente/non réactive.
- Plusieurs améliorations doctor sont toujours ouvertes ou récemment actives : résultats de service de passerelle supplémentaires (#84340), vérifications d'authentification de passerelle conscientes de SecretRef (#84224), garde-fous de réparation de config plus récente (#83715), surface de santé FTS5 (#62338) et classement des résultats doctor (#86627).
- Les diagnostics et log-follow ont historiquement produit plusieurs régressions autour des drapeaux de config, des plugins diagnostics groupés, OpenTelemetry/Prometheus, les déconnexions transitoires, les journaux de fichiers obsolètes et la mutation d'appareil appairé involontaire.

## Lacunes connues

- Les capacités implémentées dans le champ d'application incluent les instantanés RPC de santé/statut de la passerelle, les sondes HTTP de vivacité/disponibilité peu profondes, les sondes de lecture WebSocket, le sondage de disponibilité du canal, `diagnostics.stability`, l'enregistrement de stabilité sans charge utile, l'export de diagnostics, les diagnostics déclenchés par chat, les vérifications/réparations `doctor`, `logs.tail` et `openclaw logs --follow`.
- Les lacunes de couverture restent pour l'export de diagnostics en direct, le flux d'approbation/export/route privée réel de chat `/diagnostics`, la charge du stabilité-recorder en direct et la persistance du bundle de sortie fatal, les flux de réparation doctor supervisés et le comportement de reconnexion réel de `logs --follow`.
- Les lacunes documentées mais manquantes et opérationnelles incluent la validation active du schéma d'outil dans doctor, les vérifications d'authentification de passerelle conscientes de SecretRef, les résultats de service de passerelle supplémentaires et de meilleurs chemins de débogage lorsque la passerelle est lente ou non réactive.
- La preuve de décalage source/docs est limitée aux rapports de correction d'exécution soutenus par archive, en particulier le désaccord santé/statut pour l'état du canal comme l'issue WhatsApp ouverte #42538.
- Les lacunes d'attentes des utilisateurs et des mainteneurs sont représentées par GitHub #84340, GitHub #84224, les rapports Discord sur les omissions doctor de schéma d'outil et le diagnostic de passerelle lente, et les demandes historiques de fiabilité de `logs --follow`.

## Preuves

### Docs

- `docs/gateway/index.md:40`: ensemble de commandes de vérification de santé et ligne de base saine.
- `docs/gateway/index.md:52`: sondage de disponibilité du canal en direct via Gateway accessible.
- `docs/gateway/index.md:111`: précédence port/bind et `doctor --fix` ou `gateway install --force` après modifications de port.
- `docs/gateway/index.md:135`: les commandes d'opérateur incluent status, deep status, logs et doctor.
- `docs/gateway/index.md:152`: détection de passerelle multiple via status/deep et probe.
- `docs/gateway/index.md:331`: attentes de récupération liveness/readiness/gap.
- `docs/gateway/index.md:350`: les signatures d'échec courantes incluent conflit de port et incompatibilité d'authentification.
- `docs/gateway/diagnostics.md:10`: l'export combine l'état sanitisé, la santé, les logs, la forme de config et les événements de stabilité sans charge utile.
- `docs/gateway/diagnostics.md:36`: commande chat `/diagnostics`, approbation d'exécution explicite, route de groupe privé et comportement fail-closed.
- `docs/gateway/diagnostics.md:75`: contenu d'export et collecte de secours Gateway non saine.
- `docs/gateway/diagnostics.md:92`: modèle de confidentialité pour les données opérationnelles incluses et le contenu omis/redacté.
- `docs/gateway/diagnostics.md:112`: enregistreur de stabilité, avertissements liveness, `payload.large`, inspection de bundle et export.
- `docs/gateway/diagnostics.md:176`: diagnostics activés par défaut, snapshots de pression mémoire opt-in.
- `docs/gateway/doctor.md:10`: doctor corrige la config/l'état obsolète, vérifie la santé et fournit les étapes de réparation.
- `docs/gateway/doctor.md:18`: modes headless/automation pour `--yes`, `--fix`, `--lint`, `--fix --force`, `--non-interactive` et `--deep`.
- `docs/gateway/doctor.md:131`: résumé de santé/UI/update, gateway/services/supervisors, auth/security/pairing et workspace/source checks.
- `docs/gateway/doctor.md:438`: rapport de dérive d'appairage d'appareil et d'authentification.
- `docs/gateway/doctor.md:493`: authentification par jeton de passerelle locale et comportement SecretRef.
- `docs/gateway/doctor.md:509`: vérification de santé de Gateway et invite de redémarrage.
- `docs/gateway/doctor.md:525`: avertissements d'état du canal et réparation de config du superviseur.
- `docs/gateway/doctor.md:549`: diagnostics runtime/port et meilleures pratiques runtime.
- `docs/cli/gateway.md:225`: surface de commande d'export de diagnostics CLI.

### Source

- `src/gateway/server-methods.ts:223`: `health` contourne l'autorisation de portée de méthode après l'authentification de connexion.
- `src/gateway/server-methods.ts:248`: les gestionnaires principaux enregistrent `logs.tail`, `health`, `status`, `channels.status` et `diagnostics.stability`.
- `src/gateway/server-methods/health.ts:99`: implémentation du gestionnaire health/status.
- `src/gateway/server-methods/channels.ts:285`: `channels.status` valide les paramètres de probe, résout runtime/config et exécute les hooks probe/audit.
- `src/gateway/probe.ts:43`: `GatewayProbeResult` inclut auth, health, status, presence et snapshot de config.
- `src/gateway/probe.ts:223`: point d'entrée `probeGateway` et politique d'identité d'appareil non-mutante.
- `src/gateway/probe.ts:356`: le client probe utilise la portée de lecture et récupère les détails health/status/presence/config après la connexion.
- `src/gateway/server-methods/logs.ts:10`: `logs.tail` RPC valide les paramètres et lit la queue de log configurée.
- `src/logging/log-tail.ts:26`: résolution de log roulant et secours au log roulant le plus récent.
- `src/logging/log-tail.ts:150`: la queue de log configurée limite les limites et redacte les lignes sensibles.
- `src/cli/logs-cli.ts:96`: `openclaw logs` récupère les logs via Gateway RPC, secours journal systemd ou secours fichier local.
- `src/cli/logs-cli.ts:323`: classification de retry follow transitoire.
- `src/cli/logs-cli.ts:477`: enregistrement CLI `openclaw logs --follow --json`.
- `src/cli/logs-cli.ts:526`: avis de reconnexion et sortie JSON pour le mode follow.
- `src/logging/diagnostic.ts:1158`: le battement de cœur diagnostique démarre l'enregistreur de stabilité et l'échantillonneur liveness.
- `src/logging/diagnostic-stability.ts:14`: forme d'événement de stabilité sans charge utile.
- `src/logging/diagnostic-stability.ts:196`: les événements diagnostiques sont sanitisés avant enregistrement.
- `src/logging/diagnostic-stability.ts:509`: `payload.large` enregistre surface/action/bytes/limit/count/channel/plugin/reason.
- `src/logging/diagnostic-stability.ts:544`: comportement de drop du tampon annulaire borné.
- `src/logging/diagnostic-stability.ts:569`: résumés mémoire et `payload.large`.
- `src/logging/diagnostic-stability.ts:702`: API d'abonnement et snapshot de l'enregistreur.
- `src/logging/diagnostic-support-export.ts:58`: champs de confidentialité du manifeste.
- `src/logging/diagnostic-support-export.ts:315`: collecte de snapshot status/health sanitisée.
- `src/logging/diagnostic-support-export.ts:367`: queue de log sanitisée.
- `src/logging/diagnostic-support-export.ts:446`: confidentialité du résumé et contenu.
- `src/logging/diagnostic-support-export.ts:548`: assemblage d'artefact d'export de diagnostics.
- `src/logging/diagnostic-support-redaction.ts:8`: regex de redaction pour secret, payload, identifier et champs de config privée.
- `src/logging/diagnostic-support-redaction.ts:195`: préfixes de redaction du répertoire d'état et du chemin home.
- `src/logging/diagnostic-support-log-redaction.ts:8`: politique de champ de log sûr et omis.
- `src/logging/diagnostic-support-log-redaction.ts:130`: métadonnées d'omission de message de log non sûr.
- `src/cli/gateway-cli/register.ts:563`: câblage `openclaw gateway stability` et `--export`.
- `src/cli/gateway-cli/register.ts:645`: câblage `openclaw gateway diagnostics export`.
- `src/auto-reply/reply/commands-diagnostics.ts:23`: constantes de commande `/diagnostics`, URL de docs et messages de route privée.
- `src/auto-reply/reply/commands-diagnostics.ts:73`: autorisation, routage privé de groupe et dispatch de commande diagnostics.
- `src/auto-reply/reply/commands-diagnostics.ts:550`: formatage du résultat d'exécution diagnostics.
- `src/commands/doctor-ui.ts:13`: réparation de fraîcheur du protocole Control UI.
- `src/commands/doctor-gateway-daemon-flow.ts:222`: diagnostics de port et rapport d'erreur gateway récent.
- `src/commands/doctor-gateway-services.ts:528`: garde-fous de réparation de dérive de service.
- `src/commands/doctor-sandbox.ts:279`: vérifications Docker/backend/image du sandbox.
- `src/daemon/service-audit.ts:47`: les codes de problème d'audit de service incluent path, token, port, proxy env, runtime et dérive de superviseur.

### Tests d'intégration

- `src/gateway/server-http.probe.test.ts:36`: `/ready` retourne la disponibilité détaillée pour les requêtes locales.
- `src/gateway/server-http.probe.test.ts:59`: la disponibilité non authentifiée à distance retourne uniquement l'état de disponibilité.
- `src/gateway/server-http.probe.test.ts:246`: `/healthz` reste superficiel même quand readiness rapporte des canaux défaillants.
- `src/gateway/server-http.probe.test.ts:268`: `/healthz` fonctionne avant le chargement de la config Gateway.
- `src/gateway/server-http.probe.test.ts:289`: les probes sont servis avant les étapes de requête bloquées.
- `src/gateway/probe.auth.integration.test.ts:71`: le RPC status authentifié local direct reste lié à l'appareil.
- `src/gateway/probe.auth.integration.test.ts:87`: les probes authentifiés locaux pour la première fois sont non-mutants et ne créent pas de fichiers pairing/device-auth.
- `src/gateway/probe.auth.integration.test.ts:108`: l'authentification d'appareil en cache active les RPC probe détaillés pour health/status/config.
- `src/agents/bash-tools.exec-host-gateway.test.ts:627`: le suivi d'approbation diagnostics utilise `openclaw gateway diagnostics export --json` avec livraison de suivi direct.
- `test/openclaw-launcher.e2e.test.ts:539`: message de récupération source-install pour les arbres source non construits.

### Tests unitaires

- `src/gateway/gateway-stability.test.ts:31`: la charge de stabilité Gateway synthétique émet des événements message/session/memory/`payload.large`.
- `src/gateway/gateway-stability.test.ts:110`: capacité de l'enregistreur, drops, résumé mémoire, résumé `payload.large` et absence d'identifiants de session.
- `src/logging/diagnostic-support-export.test.ts:54`: la fixture d'export de diagnostics inclut des secrets faux, chat privé, corps webhook et `payload.large`.
- `src/logging/diagnostic-support-export.test.ts:238`: les entrées d'export attendues incluent config, diagnostics, health, logs, manifest, stability, status et summary.
- `src/logging/diagnostic-support-export.test.ts:251`: l'export omet les tokens, chat privé, corps webhook, identifiants account/message, hostnames, cookies, clés AWS, JWTs et identifiants de session tout en préservant `payload.large`.
- `src/logging/diagnostic-support-export.test.ts:278`: les logs sanitisés omettent les session ids/keys et le texte de payload non sûr tout en gardant les champs opérationnels sûrs.
- `src/logging/diagnostic-support-export.test.ts:315`: les snapshots status, health et config sont redactés.
- `src/cli/logs-cli.test.ts:173`: les lectures de log loopback implicites utilisent l'identité passive du client Gateway/backend.
- `src/cli/logs-cli.test.ts:207`: les URLs Gateway explicites utilisent l'identité CLI client normale.
- `src/auto-reply/reply/commands-diagnostics.test.ts:285`: `/diagnostics` met en file d'attente l'approbation diagnostics Gateway avec sécurité allowlist, approbation always-ask, suivi direct, texte d'avertissement et lien de docs.
- `src/auto-reply/reply/commands-diagnostics.test.ts:315`: la route Telegram native est préservée pour les suivis diagnostics.
- `src/auto-reply/reply/commands-diagnostics.test.ts:353`: les diagnostics indisponibles d'approbation se replient sur une réponse d'avertissement sensible visible.
- `src/auto-reply/reply/commands-diagnostics.test.ts:543`: les diagnostics de groupe échouent fermés quand aucune route propriétaire privée n'existe.
- `src/auto-reply/reply/commands-diagnostics.test.ts:567`: les confirmations diagnostics de groupe routent en privé.
- `src/auto-reply/reply/commands-diagnostics.test.ts:604`: les diagnostics nécessitent un propriétaire.
- `src/commands/doctor-gateway-daemon-flow.test.ts:327`: le doctor normal saute l'inspection de connexion de port; le doctor deep rapporte les clients Gateway établis.
- `src/commands/doctor-gateway-daemon-flow.test.ts:401`: les écouteurs Gateway attendus suppriment les notes de port occupé, les écouteurs inattendus les gardent.
- `src/commands/doctor-gateway-daemon-flow.test.ts:555`: le handoff de redémarrage récent saute l'invite de redémarrage uniquement quand la santé réussit et demande quand la sonde de santé échoue.

### Requêtes gitcrawl

- `gitcrawl search openclaw/openclaw --query "gateway diagnostics" --mode keyword --limit 10 --json`
  - Résultat: 10 résultats; les résultats exacts notables incluaient PR #70324 fermée "Improve gateway diagnostics export for support reports", problème ouvert #72883 "gateway config.patch blocks diagnostics.cacheTrace.\* even with content capture disabled", problème fermé #76628, problème fermé #77206, problème fermé #18794, problème fermé #3201, problème fermé #4317, PR fermée #75928, problème fermé #77390, PR fermées #74560/#74561.
- `gitcrawl search openclaw/openclaw --query "gateway doctor" --mode keyword --limit 10 --json`
  - Résultat: PR ouverte #84340 "Doctor: expose extra gateway service findings"; PR fermée #69947 "fix: quiet noninteractive doctor checks"; PR fermée #69896 "Fix doctor bundled runtime dependency ordering"; PR fermée #53197 "fix(doctor): honor --fix in non-interactive mode"; PR ouverte #84224 "fix(doctor): handle gateway SecretRefs in auth checks"; PR fermée #80055 "Doctor: add health-check contract and --lint validation"; PR ouverte #62338 "doctor(memory): surface FTS5 unavailable state in doctor checks"; PR ouverte #83715 "[codex] Guard doctor repairs for newer configs"; PR ouverte #86627 "Keep core doctor health in contribution order"; PR fermée #77613 "docs(doctor): clarify configured plugin repair".
- `gitcrawl search openclaw/openclaw --query "gateway health status" --mode keyword --limit 10 --json`
  - Résultat: problème fermé #13602 "Add /health endpoint for AWS ALB and Kubernetes probes"; PR fermée #36422 "gateway: keep health channel runtime state consistent with channels.status"; PR fermée #80277 "fix(status): surface model-pricing health degradation"; problème fermé #71974 "Bug: WhatsApp channel health JSON reports running=false/connected=false while status --deep shows OK/LINKED"; problème fermé #49758 "Bug: `status` / `gateway probe` / `health --json` misreport local gateway + Telegram state on 2026.3.13"; PR fermée #57374 "fix(gateway): use configured probe auth during restart health checks"; problème fermé #27619 "Dashboard API: System health endpoint returns hardcoded mock data"; problème ouvert #42538 "Bug: health endpoint returns incorrect running=false for WhatsApp"; problème fermé #59287 "[Bug]: openclaw health --json reports telegram.running=false while probe succeeds and status --deep shows Telegram OK"; problème fermé #59511 "[Bug]: node openclaw.mjs gateway run can not use `http://127.0.0.1:18789/health` link to get openclaw status".
- `gitcrawl search openclaw/openclaw --query "payload.large stability diagnostics" --mode keyword --limit 10 --json`
  - Résultat: PR fermée #70324 "Improve gateway diagnostics export for support reports"; PR fermée #82674 "fix(gateway): capture opt-in memory pressure snapshots"; PR fermée #82937 "fix: yield diagnostic event drains"; PR ouverte #86160 "fix(codex): preserve semantic native threads across compaction"; problème fermé #83795 "[Feature]: OpenClaw trace emission should include captureContent"; PR ouverte #81402 "refactor: move runtime state to SQLite".
- `gitcrawl search openclaw/openclaw --query "gateway port collision doctor service drift" --mode keyword --limit 10 --json`
  - Résultat: PR fermée #84475 "fix(gateway): include openclaw bin in service PATH".
- `gitcrawl search openclaw/openclaw --query "openclaw logs follow gateway" --mode keyword --limit 10 --json`
  - Résultat: PR fermée #45140 "fix(cli): retry logs --follow on transient gateway connect (#45080)"; PR fermée #75059 "fix(cli): auto-reconnect logs --follow on transient gateway disconnect #74782"; problème fermé #74782 "Feature: `openclaw logs --follow` should auto-reconnect instead of exiting on transient gateway disconnect"; problème fermé #66841 "openclaw logs --follow can show stale/misleading old-version file logs after side-by-side cutover"; problème fermé #74583 "[Bug]: openclaw logs --follow keeps disconnecting, making live log monitoring unusable"; problème fermé #83656 "openclaw logs --follow registers as paired device, rewrites paired.json"; PR fermée #56475 "fix(cli): reuse websocket for `logs --follow`"; PR fermée #75372 "feat(cli/logs): announce --follow gateway reconnect and add JSON notice parity"; problème fermé #32986 "Bug: `openclaw logs --follow` triggers Feishu /open-apis/bot/v3/info probe every second via post-connect health refresh"; problème fermé #45080 "openclaw logs --follow偶发连接失败：handshake timeout".

### Requêtes discrawl

- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway diagnostics"`
  - Résultat: 10 résultats. Résultats notables: `[maintainers] 2026-05-27T18:46:50Z` rapport de mainteneur citant le travail qualité/diagnostics autour des suivis de redémarrage doctor, rapport de retry de verrou de session obsolète, persistance de transcription, guidance de nettoyage de répertoire temporaire et couverture d'aperçu Telegram; `[clawtributors] 2026-05-25T09:21:53Z` rapport de performance PR Telegram/OpenClaw en direct disant que les rafraîchissements de santé Gateway et le travail heartbeat/cron pourraient interférer avec les exécutions de réponse actives et le profileur opt-in utilise `OPENCLAW_DIAGNOSTICS=profiler openclaw gateway run`.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway doctor"`
  - Résultat: 10 résultats. Résultats notables: `[clawtributors] 2026-05-27T00:54:44Z` rapport de bug que le schéma d'outil dynamique non supporté a échoué le tour d'assistant avant le contenu et doctor ne l'a pas attrapé; `[clawtributors] 2026-05-26T07:31:00Z` rapport PR #84224 sur le faux avertissement `openclaw doctor` / `doctor --lint` pour les SecretRefs de jeton gateway résolus; `[general] 2026-05-26T06:55:31Z` rapport d'utilisateur qu'après la mise à jour vers 2026.5.22 la Gateway s'est chargée extrêmement lentement et doctor n'a pas aidé.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "gateway health status"`
  - Résultat: 10 résultats. Résultats notables: `[maintainers] 2026-05-25T18:16:12Z` rapport de mainteneur citant la santé Gateway, les probes de cycle de vie, l'échantillonnage RSS, le comportement de démarrage/redémarrage; `[general] 2026-05-21T17:29:38Z` commandes `openclaw gateway stop`, `openclaw gateway restart`, `openclaw gateway status --deep`; `[Vincent <> Molty - The Crustacean Kabal] 2026-05-16T08:48:24Z` état PID launchd en cours d'exécution et vérification de santé `200 {"ok":true,"status":"live"}`; `[clawtributors] 2026-05-12T15:56:50Z` plainte de commande lente `gateway status` / `plugins list`; `[clawtributors] 2026-05-11T13:58:08Z` bizarrerie de mise à niveau/redémarrage/probe.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "payload.large stability diagnostics"`
  - Résultat: 0 résultats.
- `DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "logs --follow gateway"`
  - Résultat: 10 résultats. Résultats notables: `[users-helping-users] 2026-05-25T14:12:20Z` rapport Socket Mode Slack où Gateway se connecte et le sortant fonctionne mais aucun événement entrant n'apparaît et `openclaw logs --follow` n'affiche aucun événement de message entrant; `[maintainers/general/clawtributors] 2026-05-25T06:34Z` note de version bêta demande aux testeurs de fournir OS, méthode d'installation, version, commande/action et extrait de log pertinent pour les régressions.
