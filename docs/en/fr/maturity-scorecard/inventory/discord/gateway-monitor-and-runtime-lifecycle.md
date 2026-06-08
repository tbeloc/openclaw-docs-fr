---
title: "Discord - Gateway Monitor and Runtime Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Discord - Gateway Monitor and Runtime Lifecycle Maturity Note

## Résumé

Le moniteur de passerelle Discord et le cycle de vie du runtime sont implémentés avec une supervision runtime substantielle : démarrage conscient du compte, résolution des jetons et ID d'application, échelonnement du démarrage, secours des métadonnées de passerelle, boucles d'attente/reconnexion READY, état de battement cardiaque/reconnexion, limitation d'envoi de passerelle sortante, redémarrages du moniteur de santé, sémantique d'arrêt manuel et sondes d'état en direct. Le composant n'est pas Stable car les preuves actuelles des problèmes et des archives Discord montrent toujours des défaillances visibles par l'opérateur autour des blocages READY, de la famine de la boucle d'événements, des délais d'expiration du battement cardiaque, des réponses en double, de la priorité de démarrage multi-compte et du comportement de limite de débit/secours.

## Portée de la catégorie

Cette note couvre le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur de runtime, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque, le démarrage du moniteur de compte, la recherche de démarrage du jeton/ID d'application, la recherche des métadonnées de passerelle, les limites de débit de passerelle, la remise du cycle de vie du gestionnaire de canaux, la supervision du moniteur de santé des canaux, les surfaces de statut/sonde et le comportement d'arrêt/redémarrage. Elle exclut la politique de routage des messages Discord, le comportement des threads/forums, l'UX de configuration des bots, le rendu des commandes, les détails des médias vocaux et la livraison des messages au niveau de l'application, sauf lorsque ces chemins exposent le comportement du cycle de vie de la passerelle.

## Fonctionnalités

- Démarrage du moniteur de compte : Couvre le démarrage du moniteur de compte sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur de runtime, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement associé du moniteur de passerelle et du cycle de vie du runtime.
- Cycle de vie de la passerelle WebSocket : Couvre le cycle de vie de la passerelle WebSocket sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur de runtime, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement associé du moniteur de passerelle et du cycle de vie du runtime.
- Gestion de la reconnexion et du battement cardiaque : Couvre la gestion de la reconnexion et du battement cardiaque sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur de runtime, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement associé du moniteur de passerelle et du cycle de vie du runtime.
- Limites de débit et métadonnées de passerelle : Couvre les limites de débit et les métadonnées de passerelle sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur de runtime, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement associé du moniteur de passerelle et du cycle de vie du runtime.
- Statut, sonde et récupération du moniteur de santé : Couvre le statut, la sonde et la récupération du moniteur de santé sur le chemin de démarrage du moniteur de passerelle Discord, le cycle de vie du fournisseur de runtime, le client de passerelle WebSocket, la gestion de la reconnexion/battement cardiaque et le comportement associé du moniteur de passerelle et du cycle de vie du runtime.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (78%)`
- Signaux positifs : Un runtime QA en direct Discord démarre un vrai enfant de passerelle, injecte un compte Discord nommé, attend que `channels.status` signale le compte Discord comme `running`, `connected` et non `restartPending`, puis exerce les messages de canal Discord en direct et l'enregistrement des commandes natives. Une vérification de fumée en direct séparée et contrôlée vérifie l'identité du bot Discord réel et les métadonnées `/gateway/bot`. Les tests de flux de runtime exercent la reconnexion du délai d'expiration READY, le drainage du socket de démarrage obsolète, la reconnexion répétée jusqu'à READY, les transitions d'état de reconnexion du runtime, la politique de redémarrage du moniteur de santé, le comportement de la sonde de démarrage, l'échelonnement du démarrage multi-compte, la limitation d'envoi sortant de la passerelle, le contournement du battement cardiaque, l'épuisement de la reconnexion, la gestion de la fermeture fatale, le nettoyage du minuteur de battement cardiaque et la concurrence d'identification.
- Signaux négatifs : La voie en direct prouve le démarrage à la connexion et le flux de messages, mais pas une vraie reconnexion Discord après une chute de socket, une vraie récupération du délai d'expiration du battement cardiaque, un redémarrage en direct du moniteur de santé d'un compte Discord, un vrai secours de limite de débit `/gateway/bot` ou une priorité de démarrage multi-compte sous les limites de démarrage de session Discord. La vérification de fumée en direct couvre l'identité REST et les métadonnées uniquement, pas un cycle de vie READY WebSocket. Les preuves du flux de runtime sont solides, mais une grande partie est synthétique plutôt que de bout en bout par rapport à la passerelle en direct de Discord.
- Lacunes d'intégration : Ajouter un scénario de cycle de vie de passerelle Discord en direct canonique qui démarre deux comptes, affirme l'ordre/l'échelonnement du démarrage, atteint READY, induit ou simule une fermeture de socket via le harnais en direct, vérifie la reconnexion/RESUMED ou READY frais, vérifie les horodatages d'état et `lastDisconnect` et vérifie le comportement de redémarrage du moniteur de santé sans dépendre des exécutions pnpm larges. Ajouter une preuve en direct de secours de métadonnées/limite de débit pour `/gateway/bot` et une preuve en direct de démarrage bloqué qui `gatewayReadyTimeoutMs` produit un statut visible par l'opérateur.

## Score de qualité

- Score : `Beta (76%)`
- Rapports Gitcrawl : Les résultats ouverts actuels pour `Discord gateway` incluent #81107 pour une boucle de déduplication de commande de compétence Discord causant une saturation du CPU et bloquant la disponibilité de la passerelle, #83212 pour Discord restant désactivé sans un avertissement d'entrée de plugin, #87656 pour les envois de SecretRef d'env de compte nommé échouant tandis que le démarrage du fournisseur réussit, #77429 pour le démarrage multi-compte nécessitant une priorité par défaut/principale, #80344 pour le délai d'expiration du battement cardiaque voix/passerelle sous la famine de la boucle d'événements, #83366 pour la famine de la boucle d'événements de la passerelle causant les délais d'expiration Discord/session et #79794 pour une régression READY de la passerelle Discord. Les résultats de limite de débit plus larges incluent #87467 pour un secours de limite de débit automatique restant épinglé après la récupération primaire. Les résultats fermés `Discord gateway` montrent l'agitation corrigée récente autour de READY ne se déclenchant jamais, les courses de disponibilité de démarrage à froid et les plantages de tentative maximale de reconnexion.
- Rapports Discrawl : Les résultats de l'archive Discord montrent des traces d'opérateur en direct avec les délais d'expiration de récupération de démarrage Discord, le code de fermeture websocket 1000, les avertissements de vivacité pendant `channels.discord.start-account` et `Gateway heartbeat ACK timeout`. D'autres threads répètent les délais d'expiration des demandes de passerelle, les délais d'expiration de la poignée de main, le statut/sonde expirant, les réponses en double liées aux délais d'expiration de l'écouteur, les défaillances READY 4014/disallowed-intents et les redémarrages du moniteur de santé suivis de la recherche de l'ID d'application de démarrage et des journaux de déploiement de commande. Les discussions de version disent que le démarrage du canal/passerelle et la réutilisation des métadonnées se sont améliorés dans les bêtas récentes, mais la même archive contient toujours des demandes de fin mai pour valider les chemins de passerelle/perf et les rapports d'utilisateurs de blocages de délai d'expiration intermittents.
- Bonnes qualités : La source sépare la résolution du compte, le démarrage du fournisseur, la création du client du moniteur, la construction du plugin de passerelle, la supervision du cycle de vie de la passerelle, le transport WebSocket, la limitation d'envoi sortant, la limitation d'identification partagée, l'observation du statut, la politique de santé et le cycle de vie du gestionnaire de canaux. Elle évite les moniteurs de compte avec le même jeton en double, échoue rapidement sur les SecretRefs indisponibles avant le démarrage du fournisseur, analyse les ID d'application à partir des jetons avant le secours REST, se replie sur les défaillances transitoires des métadonnées de passerelle, enregistre les phases de démarrage, limite l'activité du transport, traite les intentions interdites comme une condition d'arrêt, met en mémoire tampon les erreurs de passerelle précoces jusqu'à ce que le cycle de vie s'attache, supprime les erreurs de démontage tardif, déduplique les démarrages de compte simultanés, distingue l'arrêt manuel de la redémarrage de récupération et limite les redémarrages du moniteur de santé.
- Mauvaises qualités : Le cycle de vie est en couches et subtil : la propre boucle de reconnexion de passerelle de Discord, la supervision READY au niveau du moniteur, le redémarrage automatique du gestionnaire de canaux et le redémarrage global du moniteur de santé peuvent tous agir sur le même compte. Plusieurs rapports actuels montrent que la famine de la boucle d'événements ou le travail de démarrage peuvent toujours bloquer la disponibilité malgré le code du cycle de vie. Le démarrage dépend de la recherche des métadonnées de l'ID d'application et `/gateway/bot` sauf si l'analyse de la configuration/jeton réussit, donc les limites de débit et les arrêts réseau restent visibles par l'opérateur. L'ordre de démarrage multi-compte et la parité SecretRef de compte nommé fuient toujours dans le comportement du cycle de vie. La résolution des réponses en double montre également que le délai d'expiration de l'écouteur de passerelle est facile à confondre avec la durée de vie du runtime de l'agent.
- Exclu de la qualité : Les tests unitaires, les tests d'intégration, les tests en direct, la profondeur des tests de flux de runtime, la couverture des tests et les tests absents n'ont pas été utilisés pour augmenter ou diminuer ce score de qualité.

## Score de complétude

- Score : `Beta (78%)`
- Instructions de surface : évaluées par rapport à `references/completeness/discord.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour le démarrage du moniteur de compte, le cycle de vie de la passerelle WebSocket, la gestion de la reconnexion et du battement cardiaque, les limites de débit et les métadonnées de passerelle, le statut, la sonde et la récupération du moniteur de santé.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve de reconnexion en direct de première classe pour Discord gateway READY, reconnexion, RESUMED ou READY frais, horodatages d'état et redémarrage du moniteur de santé.
- Prioriser ou clairement afficher `channels.discord.defaultAccount` pendant le démarrage multi-compte afin que le compte principal ne soit pas retardé derrière les comptes secondaires.
- Rendre la résolution des jetons de compte nommé identique pour le démarrage du fournisseur, les envois d'outils de message, les actions de recherche/admin, les sondes et la sortie d'état.
- Convertir la famine de la boucle d'événements et les longues phases de démarrage en un statut plus clair face à l'opérateur plutôt qu'une boucle générique déconnectée ou de délai d'expiration READY.
- Exposer le secours des métadonnées de passerelle et l'état de la limite de débit dans le statut/docteur afin que les opérateurs puissent distinguer l'accélération de l'API Discord des défaillances du jeton du bot, de l'intention ou de la disponibilité WebSocket.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:96` documente la configuration sécurisée des jetons, `openclaw gateway`, le redémarrage du service/propagation d'env, et le paramètre `applicationId` pour ignorer la recherche d'application au démarrage limitée en débit.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1550` documente les tours Discord longue durée ou les réponses en double, nomme `channels.discord.eventQueue.listenerTimeout` et les remplacements au niveau du compte, et clarifie que cela contrôle le travail du listener de passerelle Discord, pas la durée de vie du tour d'agent.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1583` documente les avertissements de délai d'expiration des métadonnées `/gateway/bot`, le repli sur l'URL de passerelle par défaut de Discord, les boutons de délai d'expiration config/env, et la valeur par défaut de 30s avec un maximum de 120s.
- `/Users/kevinlin/code/openclaw/docs/channels/discord.md:1595` documente les boutons de délai d'expiration READY au démarrage et à l'exécution, les replis env, les valeurs par défaut, les valeurs maximales, et les avertissements de décalage de démarrage multi-compte.
- `/Users/kevinlin/code/openclaw/docs/gateway/health.md:36` documente l'intervalle du moniteur de santé du canal, le seuil d'obsolescence, les redémarrages max/heure, les désactivations par fournisseur et par compte, et indique que Discord est couvert.
- `/Users/kevinlin/code/openclaw/docs/cli/channels.md:40` documente `channels status --probe` comme le chemin de sonde/statut en direct par compte et avertit que les lignes de session ne sont pas des signaux de santé de socket.
- `/Users/kevinlin/code/openclaw/docs/cli/channels.md:64` documente que `channels remove` soutenu par l'exécution demande à la passerelle en cours d'exécution d'arrêter le compte sélectionné avant les mises à jour de configuration.
- `/Users/kevinlin/code/openclaw/docs/gateway/config-channels.md:334` documente le comportement du jeton Discord/compte par défaut, les boutons de reconnexion vocale, le mode de diffusion, et le mappage automatique de présence à partir de la disponibilité à l'exécution.

### Source

- `/Users/kevinlin/code/openclaw/extensions/discord/src/accounts.ts:108` résout les comptes activés à partir de la configuration d'exécution sélectionnée, de la source/statut du jeton, et de la configuration de compte fusionnée.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/accounts.ts:144` sélectionne un propriétaire pour les jetons de bot en double, préférant les jetons configurés au repli env, et désactive les moniteurs d'exécution de jeton en double.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/channel.ts:222` calcule le décalage de démarrage par ordre de compte soutenu par jeton activé, et `/Users/kevinlin/code/openclaw/extensions/discord/src/channel.ts:660` échoue rapidement sur les SecretRefs indisponibles, applique le délai de démarrage, démarre la sonde asynchrone, et appelle `monitorDiscordProvider` avec les hooks d'exécution/statut au niveau du compte.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.ts:309` enregistre les phases de démarrage de l'ID d'application et utilise l'ID configuré, l'analyse du jeton, ou le repli REST ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.ts:422` crée le client du moniteur/superviseur de passerelle ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.ts:598` cède le contrôle à `runDiscordGatewayLifecycle`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/probe.ts:177` analyse les ID d'application à partir des jetons de bot et `/Users/kevinlin/code/openclaw/extensions/discord/src/probe.ts:205` revient à `/oauth2/applications/@me`, préservant les erreurs de limite de débit 429.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/gateway-plugin.ts:129` publie le client de passerelle avant la récupération des métadonnées, récupère `/gateway/bot` avec délai d'expiration/repli, évite les sockets en double, crée des sockets `ws` avec support de délai d'expiration de poignée de main/proxy, capture l'activité WebSocket, et émet l'activité de transport.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.ts:22` définit les valeurs par défaut/variables env du délai d'expiration READY ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.ts:324` attend READY et se reconnecte avec backoff en cas de délai d'expiration ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.ts:406` enregistre la passerelle, l'observateur de statut, l'écouteur d'activité de transport, et la gestion des erreurs de cycle de vie.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/gateway-supervisor.ts:72` classe les intentions non autorisées, l'épuisement de la reconnexion, les erreurs de passerelle fatales, et les événements non fatals ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/gateway-supervisor.ts:116` met en mémoire tampon les événements précoces et supprime les erreurs de démontage/suppression tardifs.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.ts:75` possède l'état WebSocket/session/reprise/reconnexion/battement cardiaque de la passerelle ; `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.ts:177` gère le comportement des messages/fermeture/erreur de socket ; `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.ts:296` redémarre en cas de battement cardiaque ACK manqué ; `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.ts:379` marque READY/RESUMED connecté ; `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.ts:408` se reconnecte avec backoff exponentiel plafonné et tentatives maximales.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway-rate-limit.ts:1` implémente la fenêtre de passerelle sortante 120 envois/60s, met en file d'attente les envois non critiques, expose le statut restant/réinitialisation/en file d'attente, et vide après réinitialisation.
- `/Users/kevinlin/code/openclaw/src/gateway/server-channels.ts:388` démarre les comptes de canal via les hooks de plugin, déduplique les démarrages concurrents, réserve les contrôleurs d'abandon avant les attentes, définit le statut d'exécution, cède à `startAccount`, suit les sorties/erreurs, et redémarre automatiquement avec backoff jusqu'au plafond de redémarrage du canal.
- `/Users/kevinlin/code/openclaw/src/gateway/server-channels.ts:697` arrête les comptes via abandon, hooks d'arrêt de plugin, attente gracieuse, suivi d'arrêt manuel, et gestion du délai d'expiration de récupération.
- `/Users/kevinlin/code/openclaw/src/gateway/channel-health-monitor.ts:76` exécute des vérifications de santé périodiques en vol unique, ignore les comptes désactivés/manuels, applique le refroidissement et les plafonds horaires, et redémarre les comptes malsains via arrêt/réinitialisation/démarrage.
- `/Users/kevinlin/code/openclaw/src/gateway/server-runtime-startup-services.ts:25` démarre le moniteur de santé du canal à partir de la configuration de passerelle sauf s'il est désactivé, et `/Users/kevinlin/code/openclaw/src/gateway/server.impl.ts:1548` démarre les services de canal/exécution lors du démarrage post-attachement de la passerelle.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:289` définit les scénarios Discord en direct pour l'écho canari, le contrôle des mentions, l'enregistrement des commandes natives, la jonction vocale automatique, les réactions de statut, et la réponse d'attachement de fil.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:500` injecte une configuration Discord en direct avec le canal Discord activé, le jeton de compte nommé, le compte par défaut, les listes blanches de guilde/canal, et les paramètres vocaux/statut optionnels.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:1319` interroge le `channels.status` de passerelle en direct jusqu'à ce que le compte Discord soit en cours d'exécution, connecté, et non en attente de redémarrage, échouant avec le dernier statut d'exécution s'il ne se connecte jamais.
- `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:1630` démarre la passerelle de voie en direct et `/Users/kevinlin/code/openclaw/extensions/qa-lab/src/live-transports/discord/discord-live.runtime.ts:1664` contrôle tous les scénarios Discord en direct sur le compte connecté.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/live-smoke.live.test.ts:11` utilise un vrai `DISCORD_BOT_TOKEN` quand `DISCORD_LIVE_TEST` est activé pour vérifier l'identité du bot et les métadonnées `/gateway/bot`.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/acp-bind-here.integration.test.ts:133` fournit des preuves de flux d'exécution Discord adjacentes en liant une conversation Discord DM à une session ACP et en affirmant que le prochain tour Discord s'achemine vers cette session liée.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/discord/src/channel.test.ts:532` vérifie que la sonde de démarrage asynchrone ne bloque pas le démarrage du moniteur et que les métadonnées de sonde obsolètes sont effacées sur les sondes dégradées/levées.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/channel.test.ts:646` vérifie que les comptes multi-bot ultérieurs sont décalés de 10 secondes.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.test.ts:361` vérifie que le délai d'expiration READY au démarrage se reconnecte avec backoff puis récupère ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.test.ts:396` vérifie le drainage de socket de démarrage obsolète avant reconnexion ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.test.ts:431` vérifie les tentatives READY répétées.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.test.ts:478` vérifie les erreurs de passerelle de démarrage non fatales et fatales en file d'attente ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.test.ts:669` vérifie le statut de reconnexion d'exécution quand READY revient ; `/Users/kevinlin/code/openclaw/extensions/discord/src/monitor/provider.lifecycle.test.ts:698` vérifie l'arrêt forcé quand la reconnexion d'exécution s'ouvre mais n'atteint jamais READY.
- `/Users/kevinlin/code/openclaw/src/gateway/channel-health-monitor.test.ts:308` vérifie le redémarrage du canal déconnecté, l'omission de l'exécution active occupée, le redémarrage occupé obsolète, la grâce de démarrage, le redémarrage arrêté/abandonné, le refroidissement, et le comportement max redémarrages/heure.
- `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.test.ts:296` vérifie la mise en file d'attente des événements de passerelle sortante quand la fenêtre 120 envois est épuisée et le contournement du battement cardiaque critique ; `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.test.ts:484` vérifie le comportement d'épuisement de reconnexion/fermeture fatale ; `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.test.ts:525` vérifie le nettoyage du minuteur de battement cardiaque ; `/Users/kevinlin/code/openclaw/extensions/discord/src/internal/gateway.test.ts:593` vérifie l'espacement de concurrence d'identification.

### Requêtes Gitcrawl

Requête :

```text
gitcrawl doctor --json
```

Résultats :

- Réussi ; fraîcheur enregistrée : version=0.2.1, last_sync_at=2026-05-28T19:09:52.784704Z, thread_count=29810, open_thread_count=11181, cluster_count=18594, repository_count=2.

Requête :

```text
gitcrawl search issues "Discord gateway" -R openclaw/openclaw --state open --json number,title,url,state --limit 10
```

Résultats :

- Retourné les problèmes ouverts pertinents pour la passerelle/cycle de vie #81107, #83212, #87656, #77429, #80344, #83366, #79794, et #29725. Les signaux directs les plus forts étaient le blocage de disponibilité, le délai d'expiration du battement cardiaque de la passerelle, la famine de la boucle d'événements, READY ne se déclenchant jamais, la priorité de démarrage multi-compte, et le fournisseur de démarrage réussissant tandis que les envois de compte nommé échouent.

Requête :

```text
gitcrawl search issues "Discord gateway" -R openclaw/openclaw --state closed --json number,title,url,state --limit 10
```

Résultats :

- Retourné le churn autour de READY ne se déclenchant jamais, les courses de disponibilité au démarrage à froid, les plantages maxReconnectAttempts, les conditions de course de fermeture WebSocket 1005, et les blocages de démarrage à compte unique : #74617, #55569, #56472, #56732, #57195, #59927, #57075, #56492, et #61703.

Requête :

```text
gitcrawl search issues "Discord rate limit" -R openclaw/openclaw --state open --json number,title,url,state --limit 10
```

Résultats :

- Retourné #87467, un rapport ouvert que le repli automatique de limite de débit reste épinglé après la récupération primaire, plus les rapports d'observabilité adjacents de limite de débit et de perte de message.

Requête :

```text
gitcrawl search issues "Discord applicationId" -R openclaw/openclaw --state all --json number,title,url,state --limit 10
```

Résultats :

- Retourné #77359 et #79445, montrant que les problèmes d'ID d'application et d'identité de compte apparaissent toujours dans les rapports de divergence d'enregistrement de commande multi-compte et d'envoi/lecture.

Requête :

```text
gitcrawl search issues "Discord gateway READY timeout reconnect application id startup" -R openclaw/openclaw --state open --json number,title,url,state --limit 10
gitcrawl search issues "Discord gateway monitor reconnect rate limit /gateway/bot" -R openclaw/openclaw --state open --json number,title,url,state --limit 10
gitcrawl search issues "Discord duplicate bot token multiple accounts gateway monitor" -R openclaw/openclaw --state open --json number,title,url,state --limit 10
gitcrawl search issues "Discord eventQueue listenerTimeout duplicate replies" -R openclaw/openclaw --state all --json number,title,url,state --limit 10
```

Résultats :

- Les trois premières requêtes spécifiques ouvertes n'ont retourné aucun résultat direct, ce qui est une preuve négative utile après que la requête `Discord gateway` plus large ait retourné des problèmes pertinents. La requête de réponse en double n'a également retourné aucun résultat gitcrawl direct, donc la preuve de réponse en double provient de docs et Discrawl à la place.

### Requêtes Discrawl

Requête :

```text
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord gateway READY timeout"
```

Résultats :

- Retourné une trace d'opérateur en direct du 2026-05-16 avec délai d'expiration de récupération de démarrage Discord, fermeture WebSocket 1000 de passerelle, avertissement de vivacité lors de `channels.discord.start-account`, et `Gateway heartbeat ACK timeout`. Retourné également le chatter de version/test que les correctifs de reconnexion Discord identify et les chemins de passerelle/perf étaient des domaines d'intérêt bêta actifs.

Requête :

```text
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord gateway metadata"
```

Résultats :

- Retourné les messages de fin mai de version/responsable sur une fermeture de fuite de métadonnées Discord et le cache de métadonnées de passerelle/réutilisation de chemin chaud. Retourné également les conseils de version demandant aux testeurs bêta d'exercer les chemins de passerelle/perf incluant le statut, les instantanés d'authentification/env, les métadonnées de plugin, les lectures de session, et les caches de métadonnées stables.

Requête :

```text
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord rate limited application lookup"
```

Résultats :

- Retourné aucun résultat direct. Compte tenu des vérifications de fraîcheur réussies, ceci est traité comme neutre pour le composant ; les docs/source montrent toujours la recherche d'application explicite et les atténuations de limite de débit de métadonnées.

Requête :

```text
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord duplicate replies listenerTimeout"
```

Résultats :

- Retourné les conseils de support liant les réponses en double et les gestionnaires Discord bloqués à `channels.discord.eventQueue.listenerTimeout` et `channels.discord.inboundWorker.runTimeoutMs`, incluant des exemples de configuration multi-compte au niveau du compte répétés et des liens de docs. Ces résultats soutiennent un écart de qualité autour de la confusion de l'opérateur, pas une entrée de score de couverture.

Requête :

```text
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord disallowed intents Message Content Intent"
```

Résultats :

- Retourné plusieurs fils de support expliquant que 4014/intentions non autorisées et l'intention de contenu de message manquante peuvent faire que la passerelle se connecte au niveau de la couche TCP/WebSocket mais n'atteigne jamais READY ou ne traite les messages entrants, plus les listes de contrôle pour activer les intentions et redémarrer la passerelle.

Requête :

```text
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord multiple bots same token"
DISCRAWL_NO_AUTO_UPDATE=1 discrawl search --limit 10 "Discord applicationId"
```

Résultats :

- Les résultats multi-bot ont montré une discussion d'opérateur répétée sur les comptes de bot Discord séparés, les ID de compte, les liaisons, les canaux partagés, et l'évitement des deux bots répondant. Les résultats d'ID d'application incluaient l'examen de PR/commentaire autour de la déconnexion de la passerelle avant que le démarrage d'ID manquant ne lève et les journaux en direct où le démarrage a résolu `applicationId`, déployé les commandes, récupéré l'identité du bot, puis plus tard frappé les problèmes de synchronisation de passerelle/poignée de main.
