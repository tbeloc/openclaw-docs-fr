---
title: "Slack - Socket/http Transport and Runtime Lifecycle Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Socket/http Transport and Runtime Lifecycle Maturity Note

## Résumé

Slack dispose à la fois du mode Socket et des transports HTTP Request URL implémentés et documentés, avec une politique de reconnexion, des instantanés d'état, l'enregistrement des routes HTTP et une couverture QA en direct pour le mode Socket. La qualité est inférieure aux autres familles Slack principales car les preuves d'archive contiennent des défaillances récurrentes du mode Socket dans le monde réel : délais d'expiration de pong, plantages de reconnexion, blocages WSS zombies, tempêtes multi-agents et perte d'entrée silencieuse.

## Portée de la catégorie

Cette catégorie couvre le démarrage/reconnexion/backoff du mode Socket, l'enregistrement de l'URL de demande HTTP et la vérification du secret de signature, la sélection du mode de transport, le cycle de vie multi-compte, l'état/vivacité et le comportement de démarrage/saut du runtime.

## Fonctionnalités

- Socket : Couvre Socket sur le démarrage/reconnexion/backoff du mode Socket, l'enregistrement de l'URL de demande HTTP et la vérification du secret de signature, la sélection du mode de transport, le cycle de vie multi-compte, l'état/vivacité et le comportement de démarrage/saut du runtime.
- Transport HTTP : Couvre l'enregistrement de l'URL de demande HTTP, la vérification du secret de signature, la sélection du mode de transport, le cycle de vie multi-compte, l'état/vivacité et le comportement de démarrage/saut du runtime HTTP Slack.
- Cycle de vie du runtime : Couvre le cycle de vie du runtime sur le démarrage/reconnexion/backoff du mode Socket, l'enregistrement de l'URL de demande HTTP et la vérification du secret de signature, la sélection du mode de transport, le cycle de vie multi-compte, l'état/vivacité et le comportement de démarrage/saut du runtime.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (77%)`
- Signaux positifs : Le démarrage du mode Socket, la politique de reconnexion, la validation du mode HTTP, les exigences de secret de signature, l'enregistrement du chemin webhook, les instantanés de compte et le comportement canary du canal Socket Mode en direct ont une couverture source et test explicite.
- Signaux négatifs : Le mode HTTP a moins de preuves en direct que le mode Socket, et la couverture en direct n'exerce pas tous les modes de défaillance réseau/proxy, multi-workspace et reconnexion.
- Lacunes d'intégration : Besoin de tests de transport en direct ou rejouées pour les URL de demande HTTP, le comportement du délai d'expiration de pong proxy/NAT, le redémarrage de socket obsolète, la gestion de la reconnexion 408 et la concurrence du mode Socket multi-compte.

## Score de qualité

- Score : `Alpha (68%)`
- Rapports Gitcrawl : `#62784`, `#81491`, `#58519`, `#59945`, `#83712`, `#77249` et `#57852` montrent des modes de défaillance récurrents du mode Socket pong/reconnect/silent-outage.
- Rapports Discrawl : Les fils de support décrivent les abandons du mode Socket Slack, les plantages 408, les boucles pong 5s/15s et les conseils d'utiliser le mode HTTP lorsque le conteneur ou la sortie du pare-feu ne peut pas maintenir WSS sain.
- Bonnes qualités : Les docs expliquent maintenant la sélection du transport, les champs d'URL HTTP, les secrets de signature, les sondes d'état, le backoff de redémarrage et les exigences de token spécifiques au transport.
- Mauvaises qualités : L'enregistrement de l'opérateur en direct montre toujours que les défaillances de transport peuvent laisser Slack apparemment configuré tandis que les événements entrants s'arrêtent, ce qui est un risque important de fiabilité et de récupération.
- Exclu de la qualité : Nombre de tests unitaires, largeur de voie en direct et profondeur d'intégration.

## Score de complétude

- Score : `Beta (77%)`
- Instructions de surface : évaluées par rapport à `references/completeness/slack.md`.
- Signaux positifs : les docs archivées, la source, le test, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour Socket, le transport HTTP et le cycle de vie du runtime.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter la couverture de voie en direct de l'URL de demande HTTP avec vérification de la signature de demande et vérifications de collision `webhookPath` multi-compte.
- Ajouter des simulations de reconnexion ciblées pour les réponses 408, la famine de la boucle d'événements, les WSS zombies et la contention du mode Socket multi-agent.
- Promouvoir les avertissements de santé du transport dans l'état visible par l'opérateur lorsque les sondes réussissent mais que la vivacité des événements est obsolète.

## Preuves

### Docs

- `docs/channels/slack.md` contient un tableau de comparaison des transports, des onglets de configuration du mode Socket et HTTP, le réglage du mode Socket et la résolution des problèmes pour les deux styles de connexion.
- `docs/channels/slack.md` documente `clientPingTimeout`, `serverPingTimeout`, le backoff de redémarrage, les erreurs d'authentification rapide et les exigences `webhookPath` HTTP.

### Source

- `extensions/slack/src/monitor/provider.ts` résout le mode Slack, les identifiants bot/app/signing-secret, démarre le mode Socket, enregistre les routes HTTP, enregistre les tentatives de reconnexion et ignore les erreurs d'authentification non récupérables.
- `extensions/slack/src/http/registry.ts` et `extensions/slack/src/http/plugin-routes.ts` implémentent l'enregistrement des routes HTTP et la gestion des charges utiles.
- `extensions/slack/src/account-inspect.ts` rapporte les champs d'état des identifiants spécifiques au mode.
- `extensions/slack/src/monitor/reconnect-policy.ts` définit le comportement de la politique de reconnexion.

### Tests d'intégration

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` exécute la voie QA en direct Slack sur le mode Socket en utilisant les tokens app/bot SUT.
- `docs/concepts/qa-e2e-automation.md` documente la configuration de la voie en direct Slack et les scénarios en direct standard.
- Aucune voie HTTP Request URL en direct équivalente n'a été trouvée.

### Tests unitaires

- `extensions/slack/src/config-schema.test.ts` valide le réglage du transport du mode Socket et les exigences de secret de signature HTTP.
- `extensions/slack/src/monitor/provider.reconnect.test.ts` couvre l'état de santé du socket, les états de déconnexion, la copie de nouvelle tentative, le détail du journal SDK et le comportement de tentative maximale.
- `extensions/slack/src/http/plugin-routes.test.ts` et `extensions/slack/src/http/registry.test.ts` couvrent le comportement des routes HTTP.
- `extensions/slack/src/channel.test.ts` couvre les exigences de token app du mode Socket.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search issues "Slack socket mode HTTP webhook signing secret reconnect" -R openclaw/openclaw --state all --json number,title,state,url,updatedAt --limit 10`
- `gitcrawl search openclaw/openclaw --query "slack socket mode" --json`

Résultats :

- La recherche de problème ciblée a retourné `[]`.
- La requête plus large a retourné les risques du mode Socket incluant `#62784` connexions concurrentes/tempête de délai d'expiration de pong, `#81491` panne silencieuse après reconnexions échouées, `#58519` famine de la boucle d'événements et perte de message silencieuse, `#59945` boucle de redémarrage sur erreur de sentinelle de rédaction, `#83712` famine de socket pendant SQLite VACUUM, `#77249` WSS zombie nécessitant un redémarrage et `#57852` plantage de reconnexion 408.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack socket mode reconnect pong timeout"`

Résultats :

- A retourné des rapports opérationnels de sockets Slack s'arrêtant après les délais d'expiration de pong, les plantages de reconnexion 408 et les conseils selon lesquels le mode HTTP peut être plus fiable pour les environnements proxy/conteneur hostiles.
