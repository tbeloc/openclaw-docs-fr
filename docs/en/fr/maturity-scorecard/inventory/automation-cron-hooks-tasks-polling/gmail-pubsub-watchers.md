---
title: "Automation: cron, hooks, tasks, polling - Gmail Pub/Sub Watchers Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Automation: cron, hooks, tasks, polling - Gmail Pub/Sub Watchers Maturity Note

## Résumé

L'intégration Gmail PubSub est documentée et dispose d'un code de configuration/exécution ciblé, mais c'est l'un des composants d'automatisation les moins matures de cette surface. Elle dépend de Google Pub/Sub, `gog`, des hooks OpenClaw, du routage HTTPS public, et souvent du mappage de chemin Tailscale Funnel. Les preuves d'archive montrent une confusion réelle des opérateurs et un problème ouvert où Pub/Sub atteint le sujet mais OpenClaw ne traite pas les envois en Docker plus Funnel.

## Portée de la catégorie

Cette catégorie couvre `openclaw webhooks gmail setup`, la config `hooks.gmail`, `gog gmail watch start/serve`, le démarrage et le renouvellement du watcher, le routage Tailscale/Funnel, les remplacements de modèle/réflexion Gmail, la gestion des jetons de poussée, les limites d'inclusion de corps, la gestion sécurisée du contenu externe, et le routage des événements Gmail dans les exécutions de hook isolées mappées.

## Fonctionnalités

- Assistant de configuration Gmail : Couvre l'assistant de configuration Gmail dans `openclaw webhooks gmail setup`, la config `hooks.gmail`, `gog gmail watch start/serve`, le démarrage et le renouvellement du watcher, et le comportement des watchers gmail pub/sub associés.
- Démarrage/service du watcher : Couvre le démarrage/service du watcher dans `openclaw webhooks gmail setup`, la config `hooks.gmail`, `gog gmail watch start/serve`, le démarrage et le renouvellement du watcher, et le comportement des watchers gmail pub/sub associés.
- Routage Tailscale/public : Couvre le routage Tailscale/public dans `openclaw webhooks gmail setup`, la config `hooks.gmail`, `gog gmail watch start/serve`, le démarrage et le renouvellement du watcher, et le comportement des watchers gmail pub/sub associés.
- Validation du jeton de poussée : Couvre la validation du jeton de poussée dans `openclaw webhooks gmail setup`, la config `hooks.gmail`, `gog gmail watch start/serve`, le démarrage et le renouvellement du watcher, et le comportement des watchers gmail pub/sub associés.
- Routage des événements Gmail : Couvre le routage des événements Gmail dans `openclaw webhooks gmail setup`, la config `hooks.gmail`, `gog gmail watch start/serve`, le démarrage et le renouvellement du watcher, et le comportement des watchers gmail pub/sub associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (65%)`
- Signaux positifs : Les tests ciblés couvrent la résolution de la config Gmail, les assistants de configuration, le cycle de vie du watcher, l'annulation obsolète, le remplacement de processus, et le comportement de configuration CLI. Les docs expliquent à la fois la configuration de l'assistant et la configuration manuelle.
- Signaux négatifs : Le comportement le plus important est l'entrée externe en direct via Google Pub/Sub et un point de terminaison HTTPS public, et les preuves locales ne prouvent pas le chemin externe complet sous les variantes Docker/Funnel/reverse-proxy.
- Lacunes d'intégration : Preuve répétable manquante en direct ou sauvegardée par des fixtures pour Pub/Sub push payload -> `gog watch serve` -> hook OpenClaw -> exécution d'agent isolée, y compris les défaillances de jeton/chemin et le renouvellement.

## Score de qualité

- Score : `Alpha (58%)`
- Rapports Gitcrawl : Le problème #77093 signale que les envois Gmail Pub/Sub atteignent le sujet mais le point de terminaison des webhooks Gmail d'OpenClaw ne traite pas les envois réels en Docker plus la configuration Tailscale Funnel.
- Rapports Discrawl : Le fil d'intégration Discord Gmail explore à plusieurs reprises le stripping de chemin Tailscale Funnel, `serve.path`, `tailscale.path`, `tailscale.target`, et la config du jeton de poussée, indiquant que la configuration est facile à désaligner.
- Bonnes qualités : Le générateur de config d'exécution valide les champs de jeton/compte/sujet/jeton-poussée requis, les générateurs de commande gardent les drapeaux sensibles connus, le cycle de vie du watcher protège l'annulation obsolète et la réentrée, et les docs recommandent la configuration de l'assistant.
- Mauvaises qualités : Le composant a de nombreuses pièces mobiles en dehors du processus Gateway. Les erreurs de chemin/jeton/routage produisent des défaillances difficiles à déboguer, et l'archive montre que le chemin heureux documenté ne suffit pas pour les déploiements Docker/Funnel courants.
- Exclu de la qualité : L'inventaire des tests et la profondeur de la preuve d'exécution ; ils sont uniquement des entrées de couverture.

## Score de complétude

- Score : `Alpha (65%)`
- Instructions de surface : évaluées par rapport à `references/completeness/automation-cron-hooks-tasks-polling.md`.
- Signaux positifs : les preuves archivées docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour l'assistant de configuration Gmail, le démarrage/service du watcher, le routage Tailscale/public, la validation du jeton de poussée, le routage des événements Gmail.
- Signaux négatifs : la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un harnais d'intégration local qui simule les enveloppes de poussée Pub/Sub et prouve le chemin complet du watcher au hook.
- Les docs doivent inclure des exemples de chemin côte à côte pour le stripping de préfixe Tailscale Funnel par rapport au proxy inverse direct.
- Les diagnostics de configuration doivent vérifier `hooks.gmail.serve.path`, `hooks.gmail.tailscale.path`, `hooks.gmail.tailscale.target`, la réachabilité du point de terminaison public, et l'alignement du jeton hook/jeton poussée.

## Preuves

### Docs

- `docs/automation/cron-jobs.md#gmail-pubsub-integration` documente la configuration de l'assistant, la configuration manuelle du projet Google/sujet, le démarrage automatique du watcher, et les remplacements de modèle/réflexion Gmail.
- `docs/automation/gmail-pubsub.md` redirige vers la section Gmail PubSub des tâches planifiées.
- `docs/cli/webhooks.md` documente la surface de commande `openclaw webhooks gmail setup`.

### Source

- `src/hooks/gmail.ts` construit la config d'exécution du hook Gmail, la génération de jetons, les URL de hook, les args `gog` watch start/serve, la config Tailscale, et l'analyse du sujet.
- `src/hooks/gmail-watcher.ts`, `src/hooks/gmail-watcher-lifecycle.ts`, et `src/hooks/gmail-watcher-errors.ts` gèrent le cycle de vie du processus watcher et les erreurs.
- `src/hooks/gmail-setup-utils.ts`, `src/hooks/gmail-ops.ts`, et `src/cli/webhooks-cli.ts` implémentent le comportement de configuration et CLI.
- `src/gateway/hooks-mapping.ts` définit le mappage de préset Gmail, et `src/agents/model-selection-shared.ts` résout les remplacements de modèle de hook Gmail.

### Tests d'intégration

- Aucun test d'intégration Google Pub/Sub en direct complet n'a été trouvé dans l'arborescence auditée.
- `src/hooks/gmail-watcher-lifecycle.test.ts` et `src/hooks/gmail-watcher.test.ts` sont les plus proches des tests de style intégration pour le cycle de vie du processus watcher.

### Tests unitaires

- `src/hooks/gmail.test.ts`, `src/hooks/gmail-setup-utils.test.ts`, `src/hooks/gmail-watcher.test.ts`, et `src/hooks/gmail-watcher-lifecycle.test.ts` couvrent la config, les assistants de configuration, l'annulation du watcher, et le remplacement de processus.
- `src/cli/webhooks-cli.test.ts` couvre le comportement de configuration CLI.
- `src/agents/openclaw-gateway-tool.test.ts` couvre les chemins de config protégés tels que `hooks.gmail.allowUnsafeExternalContent`.

### Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "gmail pubsub watcher hooks gmail model" --json --limit 5`

Résultats :

- Le problème #77093 signale que la poussée Gmail Pub/Sub atteint le sujet mais OpenClaw ne traite pas les envois réels en Docker plus la configuration Tailscale Funnel.

Requête de secours :

`gitcrawl search openclaw/openclaw --query "Gmail PubSub Funnel" --json --limit 5`

Résultats :

- Le problème #77093 est à nouveau le résultat correspondant, mentionnant spécifiquement Docker plus Tailscale Funnel.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "gmail pubsub watcher hooks gmail model"`

Résultats :

- Aucun message Discord correspondant retourné pour cette requête exacte.

Requête de secours :

`/Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "Gmail PubSub Funnel"`

Résultats :

- Le fil d'intégration Discord Gmail explique que Tailscale Serve ne suffit pas pour les rappels Google Pub/Sub ; Funnel ou une autre URL HTTPS publique est requise.
- Le même fil donne des args `gog gmail watch serve` concrets et avertit que Funnel peut supprimer `/gmail-pubsub`, nécessitant `serve.path="/"` sauf si la cible préserve explicitement le chemin.
- Le même fil recommande de vérifier `hooks.gmail.serve.path`, `hooks.gmail.tailscale.path`, `hooks.gmail.tailscale.target`, et `hooks.gmail.pushToken`.
