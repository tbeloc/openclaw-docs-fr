---
title: "Automation: cron, hooks, tasks, polling - Event Ingress Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - Event Ingress Maturity Note

## Résumé

L'interrogation d'entrée de canal et les moniteurs webhook sont matures pour les canaux à fort trafic tels que Telegram et Zalo, avec une documentation détaillée, un comportement au démarrage, une gestion des baux/sessions, des chiens de garde et des tests. Le plafond de qualité est limité par l'enregistrement vécu : la détection de stagnation d'interrogation, l'exclusion mutuelle webhook/interrogation, la dérive de schéma, le blocage au démarrage et les défaillances réseau sont des risques opérationnels fréquents.

## Portée de la catégorie

Inclus dans cette catégorie :

- Interrogation longue Telegram : Couvre l'interrogation longue Telegram sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Mode webhook Telegram : Couvre le mode webhook Telegram sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Mode interrogation/webhook Zalo : Couvre le mode interrogation/webhook Zalo sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Diagnostics de stagnation d'interrogation : Couvre les diagnostics de stagnation d'interrogation sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Secours de surveillance iMessage : Couvre le secours de surveillance iMessage sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Assistant de configuration Gmail : Couvre l'assistant de configuration Gmail sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- Démarrage/service du moniteur : Couvre le démarrage/service du moniteur sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- Routage Tailscale/public : Couvre le routage Tailscale/public sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- Validation du jeton de notification : Couvre la validation du jeton de notification sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- Routage des événements Gmail : Couvre le routage des événements Gmail sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- POST /hooks/wake : Couvre POST /hooks/wake sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- POST /hooks/agent : Couvre POST /hooks/agent sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Webhooks mappés : Couvre les webhooks mappés sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Politique d'authentification des webhooks : Couvre la politique d'authentification des webhooks sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Dispatch asynchrone : Couvre le dispatch asynchrone sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.

## Fonctionnalités

- Interrogation longue Telegram : Couvre l'interrogation longue Telegram sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Mode webhook Telegram : Couvre le mode webhook Telegram sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Mode interrogation/webhook Zalo : Couvre le mode interrogation/webhook Zalo sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Diagnostics de stagnation d'interrogation : Couvre les diagnostics de stagnation d'interrogation sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Secours de surveillance iMessage : Couvre le secours de surveillance iMessage sur les modes d'interrogation longue et webhook au niveau du canal, en particulier Telegram et Zalo ; vivacité d'interrogation, baux, seuils de chien de garde et comportement d'interrogation et webhook de canal associé.
- Assistant de configuration Gmail : Couvre l'assistant de configuration Gmail sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- Démarrage/service du moniteur : Couvre le démarrage/service du moniteur sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- Routage Tailscale/public : Couvre le routage Tailscale/public sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- Validation du jeton de notification : Couvre la validation du jeton de notification sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- Routage des événements Gmail : Couvre le routage des événements Gmail sur `openclaw webhooks gmail setup`, configuration `hooks.gmail`, `gog gmail watch start/serve`, démarrage et renouvellement du moniteur, et comportement du moniteur pub/sub Gmail associé.
- POST /hooks/wake : Couvre POST /hooks/wake sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- POST /hooks/agent : Couvre POST /hooks/agent sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Webhooks mappés : Couvre les webhooks mappés sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Politique d'authentification des webhooks : Couvre la politique d'authentification des webhooks sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.
- Dispatch asynchrone : Couvre le dispatch asynchrone sur `/hooks/wake`, `/hooks/agent`, webhooks mappés sous `/hooks/<name>`, extraction de jeton et comportement des webhooks http associé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : Telegram et Zalo ont une couverture ciblée pour l'état d'interrogation, l'état du transport, la vivacité, les baux, les sessions, l'état du webhook, les gestionnaires webhook, le cycle de vie et les réponses médias d'interrogation.
- Signaux négatifs : L'interrogation longue dépend du comportement réel du réseau, de la mise en veille de l'hôte, de l'état du proxy/DNS/TLS, du comportement de l'API Telegram/Zalo et de la charge de la boucle d'événements de la passerelle. Les tests locaux ne peuvent pas couvrir tous les modes de défaillance.
- Lacunes d'intégration : Ajouter un harnais de défaillance réseau pour les moniteurs Telegram/Zalo qui simule le délai d'expiration d'interrogation longue, la mise en veille de l'hôte, le conflit webhook actif, la dérive de configuration de schéma et le redémarrage après les stagnations de boucle d'événements.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : La PR #73884 corrige les redémarrages faux de stagnation d'interrogation Telegram ; la requête de secours a trouvé le problème #86535 où le détecteur de stagnation d'interrogation Telegram traite la mise en veille comme une stagnation `getUpdates` active.
- Rapports Discrawl : Les commentaires d'examen sur les PR #41153, #70579 et #57737 se concentrent sur les seuils de chien de garde de stagnation d'interrogation et la dérive de métadonnées de schéma ; les rapports d'utilisateurs mentionnent le blocage séquentiel au démarrage sur le premier sondage Telegram sous charge de boucle d'événements.
- Bonnes qualités : Telegram a un `pollingStallThresholdMs` configurable, une protection de bail pour un interrogateur actif par jeton, un comportement de redémarrage de transport-dirty et une documentation pour webhook vs interrogation longue. Zalo documente et teste l'exclusion mutuelle interrogation/webhook et le comportement de réponse médias.
- Mauvaises qualités : La santé d'interrogation est sensible aux stagnations de boucle d'événements, à la mise en veille, à la dérive de schéma et aux défaillances réseau. L'enregistrement des bogues du monde réel est actif et spécifique au canal.
- Exclu de la qualité : Inventaire des tests et profondeur de preuve d'exécution ; ce ne sont que des entrées de couverture.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'interrogation longue Telegram, le mode webhook Telegram, le mode interrogation/webhook Zalo, les diagnostics de stagnation d'interrogation, le secours de surveillance iMessage, l'assistant de configuration Gmail, le démarrage/service du moniteur, le routage Tailscale/public, la validation du jeton de notification, le routage des événements Gmail, POST /hooks/wake, POST /hooks/agent, les webhooks mappés, la politique d'authentification des webhooks, le dispatch asynchrone.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et de l'enregistrement des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les chiens de garde d'interrogation doivent distinguer la mise en veille de l'hôte/pause de boucle d'événements des stagnations de requête API actives.
- La génération de schéma de configuration de canal doit rester liée aux champs d'exécution comme `pollingStallThresholdMs`.
- Le démarrage doit éviter les dépendances d'interrogation de canal en série qui peuvent bloquer toute la passerelle sous charge de boucle d'événements.

# Preuve

## Docs

- `docs/channels/telegram.md` documente le long polling par défaut, le mode webhook, `pollingStallThresholdMs`, les conflits getUpdates, le dépannage de la vivacité, et les sondes doctor/status.
- `docs/channels/zalo.md` documente le long-polling par défaut, le mode webhook, et l'exclusion mutuelle entre les modes polling et webhook.
- `docs/channels/troubleshooting.md` inclut les diagnostics de stagnation du polling.
- `docs/channels/imessage-from-bluebubbles.md` note le comportement de surveillance iMessage avec un repli au polling.

## Source

- `extensions/telegram/src/monitor.ts`, `extensions/telegram/src/monitor-polling.runtime.ts`, `extensions/telegram/src/polling-liveness.ts`, `extensions/telegram/src/polling-lease.ts`, `extensions/telegram/src/polling-session.ts`, `extensions/telegram/src/polling-status.ts`, et `extensions/telegram/src/webhook-status.ts` implémentent la surveillance du polling/webhook Telegram.
- `extensions/zalo/src/monitor.ts`, `extensions/zalo/src/monitor.webhook.ts`, `extensions/zalo/src/monitor-durable.ts`, et `extensions/zalo/src/outbound-media.ts` implémentent le comportement du polling/webhook Zalo.
- `extensions/imessage/src/approval-reaction-poller.ts` implémente un chemin de polling d'approbation iMessage.

## Tests d'intégration

- `extensions/zalo/src/monitor.webhook-e2e.test.ts` couvre le comportement du webhook Zalo.
- `extensions/zalo/src/monitor.polling.media-reply.test.ts` couvre le polling Zalo avec les réponses médias.
- Les tests du moniteur Telegram sont principalement des tests d'exécution plutôt que des e2e d'API en direct.

## Tests unitaires

- `extensions/telegram/src/polling-status.test.ts`, `extensions/telegram/src/polling-transport-state.test.ts`, `extensions/telegram/src/polling-session.test.ts`, `extensions/telegram/src/polling-liveness.test.ts`, `extensions/telegram/src/polling-lease.test.ts`, et `extensions/telegram/src/webhook-status.test.ts` couvrent les composants du moniteur Telegram.
- `extensions/zalo/src/monitor.lifecycle.test.ts`, `extensions/zalo/src/monitor.webhook.test.ts`, `extensions/zalo/src/monitor.polling.media-reply.test.ts`, et `extensions/zalo/src/monitor.image.polling.test.ts` couvrent le comportement Zalo.
- `extensions/imessage/src/approval-reaction-poller.test.ts` couvre le polling de réaction iMessage.

## Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "channel polling webhook getUpdates polling stall Zalo Telegram" --json --limit 5`

Résultats :

- Aucun résultat pour la requête exacte.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "pollingStallThresholdMs" --json --limit 5`

Résultats :

- PR #73884 corrige les redémarrages de fausse stagnation du polling Telegram.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "poll loop" --json --limit 5`

Résultats :

- Le problème #86535 signale que le détecteur de stagnation du polling Telegram traite la mise en veille de l'hôte/la pause de la boucle d'événements comme une stagnation active de `getUpdates`.

## Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "pollingStallThresholdMs"`

Résultats :

- La fermeture de PR #41153 indique que le main actuel renforce la détection de stagnation du polling Telegram avec une valeur par défaut de 120s et un remplacement configurable par compte.
- L'examen de PR #70579 avertit que la dérive de la validation du schéma pourrait rejeter les configurations `pollingStallThresholdMs` ajustées.
- L'examen de PR #57737 avertit que les métadonnées du schéma fourni doivent être régénérées lors de l'ajout de `pollingStallThresholdMs`.

Requête de secours :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "poll loop"`

Résultats :

- Le rapport d'utilisateur Discord indique que le démarrage du compte Telegram peut bloquer séquentiellement au premier polling lorsque la charge de la boucle d'événements est élevée, causant des délais d'attente et des stagnations de plusieurs minutes.
