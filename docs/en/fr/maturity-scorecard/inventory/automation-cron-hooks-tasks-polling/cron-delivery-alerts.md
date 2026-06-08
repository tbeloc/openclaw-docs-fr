---
title: "Automation: cron, hooks, tasks, polling - Cron Delivery and Failure Alerts Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - Cron Delivery and Failure Alerts Maturity Note

## Résumé

La livraison cron est riche en fonctionnalités : les tâches peuvent annoncer sur des canaux, publier des charges utiles webhook, supprimer la livraison de secours du runner, préserver le routage du chat dernier/actuel, refléter la livraison directe dans les transcriptions, supprimer le texte intermédiaire obsolète, préférer la sortie du sous-agent descendant, et notifier les destinations d'échec. L'implémentation est puissante mais suffisamment complexe pour que les preuves d'archive montrent toujours des risques de confidentialité et de routage autour des alertes d'échec et du mode webhook.

## Portée de la catégorie

Cette catégorie couvre les modes de livraison de sortie cron, la résolution des cibles de canal, les tentatives de livraison directe, la mise en miroir des transcriptions, les destinations d'échec, les alertes d'exécution ignorée, la sensibilisation à la livraison des outils de message, la préférence de livraison du sous-agent descendant, et le nettoyage après les exécutions isolées.

## Fonctionnalités

- Livraison d'annonce de chat : Couvre la livraison d'annonce de chat sur les modes de livraison de sortie cron, la résolution des cibles de canal, les tentatives de livraison directe, la mise en miroir des transcriptions, et le comportement associé de livraison cron et d'alertes d'échec.
- Livraison webhook : Couvre la livraison webhook sur les modes de livraison de sortie cron, la résolution des cibles de canal, les tentatives de livraison directe, la mise en miroir des transcriptions, et le comportement associé de livraison cron et d'alertes d'échec.
- Destinations d'échec : Couvre les destinations d'échec sur les modes de livraison de sortie cron, la résolution des cibles de canal, les tentatives de livraison directe, la mise en miroir des transcriptions, et le comportement associé de livraison cron et d'alertes d'échec.
- Alertes d'exécution ignorée : Couvre les alertes d'exécution ignorée sur les modes de livraison de sortie cron, la résolution des cibles de canal, les tentatives de livraison directe, la mise en miroir des transcriptions, et le comportement associé de livraison cron et d'alertes d'échec.
- Aperçus de livraison : Couvre les aperçus de livraison sur les modes de livraison de sortie cron, la résolution des cibles de canal, les tentatives de livraison directe, la mise en miroir des transcriptions, et le comportement associé de livraison cron et d'alertes d'échec.

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Stable (82%)`
- Signaux positifs : La livraison a une couverture ciblée pour la livraison directe, la résolution des cibles de livraison, les alertes d'échec, les plans/aperçus de livraison, la prévention de double annonce, la livraison d'agent nommé, la distribution d'exécution sortante, la suppression d'intermédiaire obsolète, et la persistance du statut de livraison.
- Signaux négatifs : La couverture est principalement simulée et au niveau des composants. La livraison en direct multi-canaux, la confidentialité des échecs de livraison webhook, et le comportement de livraison du sous-agent descendant ne sont pas prouvés par un large scénario e2e.
- Lacunes d'intégration : Une matrice en direct devrait couvrir l'annonce, webhook, pas de livraison, destinations d'échec explicites, rejet de cible obsolète, alertes de contrôle préalable du fournisseur ignorées, et la livraison de sortie finale du sous-agent descendant sur au moins un canal de chat et un récepteur webhook.

## Score de qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl : La PR #85394 référence le schéma d'alerte d'échec et la décomposition de l'outil cron. La requête a trouvé un travail en cours près du comportement d'alerte d'exécution ignorée.
- Rapports Discrawl : Un commentaire d'examen sur la PR #31059 avertit que les alertes d'échec en mode webhook sans `to` pourraient tomber dans la livraison d'annonce et divulguer les détails d'erreur aux cibles de chat.
- Bonnes qualités : La planification de la livraison est explicite, les préfixes du sélecteur de fournisseur sont validés, la livraison directe utilise des clés d'idempotence et des boucles de tentative transitoires, les livraisons obsolètes peuvent être ignorées, et le nettoyage isolé ferme les ressources de navigateur/MCP suivies au mieux sans masquer le résultat de l'exécution.
- Mauvaises qualités : La livraison a un grand espace d'état sur les routes de canal, les envois directs, l'annonce de secours, la mise en miroir des transcriptions, le mode webhook, les alertes d'échec, et le suivi du sous-agent. L'avertissement de confidentialité de l'archive montre que les limites de mode peuvent être faciles à mal interpréter.
- Exclu de la qualité : L'inventaire des tests et la profondeur de la preuve d'exécution ; ils sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Stable (82%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la livraison d'annonce de chat, la livraison webhook, les destinations d'échec, les alertes d'exécution ignorée, les aperçus de livraison.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Le mode d'alerte d'échec devrait échouer fermé lorsque les champs de destination sont incomplets, sans secours à un destinataire plus large que celui sélectionné par l'opérateur.
- La documentation de livraison devrait inclure un tableau de routage compact pour `last`, les cibles de canal explicites, les cibles préfixées par fournisseur, le mode webhook, et les destinations d'échec.
- Un petit fixture webhook local rendrait les régressions de livraison plus faciles à prouver sans identifiants de canal réels.

## Preuves

### Docs

- `docs/automation/cron-jobs.md` documente les modes de livraison `announce`, `webhook`, et `none` ; les cibles de canal explicites ; la validation du préfixe de canal ; l'interaction avec l'outil de message ; la langue de sortie ; les destinations d'échec ; les alertes ignorées ; et le dépannage pour aucune livraison.
- `docs/automation/tasks.md` documente le nettoyage et le comportement d'achèvement pour les tâches cron et la préférence de sortie du sous-agent descendant.
- `docs/channels/discord.md` inclut le comportement de livraison cron spécifique au canal pour les annonces de texte Discord.

### Source

- `src/cron/delivery.ts`, `src/cron/delivery-plan.ts`, `src/cron/delivery-preview.ts`, `src/cron/delivery-context.ts`, `src/cron/delivery-field-schemas.ts`, et `src/cron/webhook-url.ts` implémentent la validation de livraison, la planification, l'aperçu, et la gestion des URL.
- `src/cron/isolated-agent/delivery-dispatch.ts`, `src/cron/isolated-agent/delivery-target.ts`, `src/cron/isolated-agent/delivery-outbound.runtime.ts`, et `src/cron/isolated-agent/subagent-followup.ts` implémentent la livraison directe isolée, l'idempotence, les tentatives, la mise en miroir des transcriptions, et la préférence de sortie descendante.
- `src/cron/service/initial-delivery.ts`, `src/cron/service/task-ledger.ts`, et `src/cron/service/timer.ts` alimentent le contexte de livraison initial, l'état de la tâche, et les alertes d'échec du planificateur.

### Tests d'intégration

- `src/cron/isolated-agent.direct-delivery-core-channels.test.ts` couvre la livraison directe sur les abstractions de canal principal.
- `src/cron/isolated-agent/delivery-dispatch.named-agent.test.ts` et `src/cron/isolated-agent/delivery-dispatch.double-announce.test.ts` exercent les cas de distribution de livraison isolée intégrée.
- `src/cron/isolated-agent.delivery-awareness.test.ts` couvre la sensibilisation aux messages envoyés par l'agent par rapport à la livraison de secours.

### Tests unitaires

- `src/cron/delivery.test.ts`, `src/cron/delivery-plan.test.ts`, `src/cron/delivery-preview.test.ts`, `src/cron/delivery.failure-notify.test.ts`, et `src/cron/delivery-context.test.ts` couvrent la planification et la logique d'alerte.
- `src/cron/isolated-agent/delivery-target.test.ts`, `src/cron/isolated-agent/channel-output-policy.test.ts`, et `src/cron/isolated-agent/subagent-followup.test.ts` couvrent la résolution des cibles, les règles de sortie de canal, et le suivi descendant.
- `src/cron/service.delivery-plan.test.ts`, `src/cron/service.failure-alert.test.ts`, et `src/cron/service.persists-delivered-status.test.ts` couvrent le comportement de livraison au niveau du service.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "cron delivery failure alerts announce webhook skipped" --json --limit 5`

Résultats :

- PR #85394, `refactor(cron-tool): decompose into per-action tools (WOR-317)`, inclut le schéma d'alerte d'échec et les champs d'alerte d'exécution ignorée, montrant que cette surface évolue activement.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "cron delivery failure alerts announce webhook skipped"`

Résultats :

- Un commentaire d'examen sur la PR #31059 avertit que `sendCronFailureAlert` en mode webhook sans `to` pourrait tomber dans la livraison d'annonce et divulguer le texte d'échec aux cibles de chat.
