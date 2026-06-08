---
title: "Automation: cron, hooks, tasks, polling - HTTP Webhooks Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - HTTP Webhooks Maturity Note

## Résumé

Les hooks HTTP exposent l'entrée d'automatisation externe pour les exécutions d'agent wake et isolées. Le contrat a des valeurs par défaut de sécurité fortes : chemin dédié, authentification bearer ou `x-openclaw-token`, rejet des jetons de requête, listes blanches d'agents, portes de préfixe de clé de session, transformations de hooks mappées et limites de contenu externe. La couverture et la qualité sont limitées par les frictions d'intégration côté utilisateur et les demandes ouvertes pour les comportements de webhook associés.

## Portée de la catégorie

Cette catégorie couvre `/hooks/wake`, `/hooks/agent`, les hooks mappés sous `/hooks/<name>`, l'extraction de jetons, les limites de corps de requête, la politique de chemin/IP client, les contrôles d'agent/session autorisés, les clés d'idempotence, l'enveloppe de charge utile, la distribution asynchrone et les aides d'entrée du plugin webhook.

## Fonctionnalités

- POST /hooks/wake : Couvre POST /hooks/wake sur `/hooks/wake`, `/hooks/agent`, les hooks mappés sous `/hooks/<name>`, l'extraction de jetons et le comportement des webhooks http associés.
- POST /hooks/agent : Couvre POST /hooks/agent sur `/hooks/wake`, `/hooks/agent`, les hooks mappés sous `/hooks/<name>`, l'extraction de jetons et le comportement des webhooks http associés.
- Hooks mappés : Couvre les hooks mappés sur `/hooks/wake`, `/hooks/agent`, les hooks mappés sous `/hooks/<name>`, l'extraction de jetons et le comportement des webhooks http associés.
- Politique d'authentification des hooks : Couvre la politique d'authentification des hooks sur `/hooks/wake`, `/hooks/agent`, les hooks mappés sous `/hooks/<name>`, l'extraction de jetons et le comportement des webhooks http associés.
- Distribution asynchrone : Couvre la distribution asynchrone sur `/hooks/wake`, `/hooks/agent`, les hooks mappés sous `/hooks/<name>`, l'extraction de jetons et le comportement des webhooks http associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs : Une couverture de style unitaire et intégration existe pour la gestion des requêtes de hook, la politique de confiance/session, la résolution de mapping, le délai d'expiration de la requête, les gardes de plugin webhook et l'extension webhooks groupée.
- Signaux négatifs : Les intégrations externes réelles sont plus difficiles à prouver localement ; les configurations de webhook Gmail/Tailscale et de canal montrent que l'entrée de bout en bout dépend des détails de chemin/jeton du proxy inverse en dehors du gestionnaire principal.
- Lacunes d'intégration : Un seul fixture e2e devrait configurer un gestionnaire de hook Gateway, POST les requêtes `wake`, `agent` et hook mappé, valider les défaillances de politique de jeton/session/agent et prouver que l'exécution/événement résultant apparaît dans l'état de tâche ou de session.

## Score de qualité

- Score : `Beta (70%)`
- Rapports Gitcrawl : La PR #62528 demande `/hooks/message` avec parité d'authentification, la PR #83118 demande l'authentification tokenFile secrets, le problème #77093 signale que Gmail Pub/Sub push ne traite pas dans Docker plus Tailscale Funnel, et le problème #64556 signale que `hooks.mappings[].agentId`/`sessionKey` est ignoré pour `action="wake"`.
- Rapports Discrawl : La PR #69267 ajoute la journalisation pour les erreurs de passerelle de hook 4xx car les POST webhook invalides laissaient auparavant aucune trace ; les conseils des utilisateurs Discord mettent l'accent sur les moteurs de flux de travail externes pour les flux Telegram déterministes avec intervention humaine et listent `/hooks/agent` et `/hooks/wake` comme entrée d'exécution de worker.
- Bonnes qualités : L'authentification est centralisée, les jetons de chaîne de requête sont rejetés, la sélection de clé de session est optionnelle et liée au préfixe, les mappages modélisés nécessitent des portes de préfixe et le contenu externe mappé peut être enveloppé comme non fiable.
- Mauvaises qualités : La débogage et la configuration d'intégration restent des points faibles. Plusieurs rapports se regroupent autour des défaillances de validation silencieuses, des ergonomies manquantes d'authentification-secret et des incompatibilités de chemin/jeton avec les vrais proxies inverses.
- Exclu de la qualité : L'inventaire des tests et la profondeur de la preuve d'exécution ; ils sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour POST /hooks/wake, POST /hooks/agent, Hooks mappés, Politique d'authentification des hooks, Distribution asynchrone.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Les réponses 4xx des hooks ont besoin de journaux cohérents et exploitables et d'une résolution des problèmes côté opérateur.
- Le support des fichiers de jetons et une gestion des secrets plus sûre réduiraient la pression de risque de configuration.
- La sémantique de l'action de wake mappée doit être explicite pour les champs d'agent/session afin que les opérateurs sachent quels champs s'appliquent.

## Preuves

### Docs

- `docs/automation/cron-jobs.md#webhooks` documente `/hooks/wake`, `/hooks/agent`, les hooks mappés, les en-têtes d'authentification, le rejet des jetons de requête, les agents autorisés, les contrôles de clé de session et les limites de sécurité.
- `docs/automation/webhook.md` redirige vers la documentation des webhooks de tâches planifiées.
- `docs/cli/webhooks.md` documente la configuration du CLI webhook, y compris la configuration de Gmail.

### Source

- `src/gateway/hooks.ts` résout la configuration du hook, l'extraction de jeton, l'analyse du corps, les agents autorisés, la politique de clé de session, les champs de livraison et la normalisation de la charge utile.
- `src/gateway/server/hooks.ts` et `src/gateway/server/hooks-request-handler.ts` implémentent la distribution de requête et la gestion HTTP.
- `src/gateway/hooks-mapping.ts` implémente les transformations de hook mappé prédéfini et personnalisé, la correspondance de chemin, les modèles et le confinement du chemin de transformation.
- `src/gateway/hooks-policy.ts` et `src/gateway/server/hook-client-ip-config.ts` implémentent les aides de politique.
- `src/plugin-sdk/webhook-ingress.ts`, `src/plugin-sdk/webhook-request-guards.ts`, `src/plugin-sdk/webhook-targets.ts` et `extensions/webhooks/` implémentent les aides webhook côté plugin et le plugin webhooks groupé.

### Tests d'intégration

- `src/gateway/server/hooks.agent-trust.test.ts` exerce les limites de confiance de distribution de hook.
- `src/gateway/server-http.hooks-request-timeout.test.ts` couvre le comportement du délai d'expiration de la requête.
- `extensions/webhooks/index.test.ts` et `extensions/webhooks/src/http.test.ts` exercent le chemin du plugin webhooks groupé.

### Tests unitaires

- `src/gateway/hooks.test.ts`, `src/gateway/hooks-mapping.test.ts`, `src/gateway/hooks-test-helpers.ts` et `src/gateway/server.hooks.test.ts` couvrent l'analyse de hook principal et le comportement de mapping.
- `src/plugin-sdk/webhook-request-guards.test.ts`, `src/plugin-sdk/webhook-memory-guards.test.ts` et `src/plugin-sdk/webhook-targets.test.ts` couvrent les aides de garde SDK.
- `src/gateway/server/hooks.agent-trust.test.ts` couvre les détails de la politique de confiance d'agent/session.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "hooks agent wake token allowedSessionKey" --json --limit 5`

Résultats :

- Aucun résultat pour la requête exacte.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "webhook token hook" --json --limit 5`

Résultats :

- La PR #62528 demande l'entrée `/hooks/message` avec parité d'authentification webhook.
- La PR #83118 demande les secrets d'authentification tokenFile partagés entre les hooks de passerelle et l'exécution/configuration de Gmail.
- Le problème #77093 signale que les vrais pushes Gmail Pub/Sub atteignent le sujet mais ne traitent pas via le chemin webhook/watcher.
- La PR #64126 référence la comparaison de secret partagé pour la validation du jeton de hook.
- Le problème #64556 signale que le hook mappé `agentId` et `sessionKey` sont ignorés pour les actions de wake.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "hooks agent wake token allowedSessionKey"`

Résultats :

- Aucun message Discord correspondant retourné pour cette requête exacte.

Requête de secours :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "webhook token hook"`

Résultats :

- La discussion de la PR #69267 ajoute la journalisation pour les erreurs de passerelle de hook 4xx, y compris le jeton en requête, la charge utile invalide, l'agent non autorisé, les erreurs de clé de session, les requêtes non autorisées et les points de terminaison manquants.
- Les conseils de flux de travail Discord recommandent la propriété de flux de travail externe pour l'orchestration Telegram déterministe difficile et traitent `/hooks/agent` et `/hooks/wake` comme entrée d'exécution de worker OpenClaw.
