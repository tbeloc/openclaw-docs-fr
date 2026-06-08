---
title: "Slack - Native Controls and Approvals Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Native Controls and Approvals Maturity Note

## Summary

La prise en charge des commandes slash Slack inclut un seul chemin de commande `/openclaw`, un mode de commande natif explicite, des menus d'arguments natifs, un routage de session cible de commande, des chargeurs de commandes de plugin et de compétence, des différences d'URL en mode HTTP par rapport au mode Socket, et une copie d'autorisation. Le composant est en version bêta : les commandes natives sont implémentées et documentées, mais elles nécessitent un enregistrement manuel de l'application Slack, le mode automatique est intentionnellement désactivé, et les preuves d'archive montrent des cas limites non résolus de préfixe de commande, de configuration obsolète et de routage de session.

## Normalization

Catégorie active après normalisation de la taxonomie des canaux.

- Catégorie normalisée : `Native Controls and Approvals`
- Fusionnée à partir de : `Commands, Actions, and Approvals`
- Report de score : minimum conservateur des scores des catégories sources fusionnées.

## Category Scope

Inclus dans cette catégorie :

- Slash Commands : Couvre les Slash Commands dans le mode de commande slash configuré, les commandes slash natives, les attentes d'enregistrement de commande, les clés de session, et le comportement de routage des commandes slash natives et des commandes natives associées.
- Native Command Routing : Couvre le routage des commandes natives dans le mode de commande slash configuré, les commandes slash natives, les attentes d'enregistrement de commande, les clés de session, et le comportement de routage des commandes slash natives et des commandes natives associées.
- Interactive Replies : Couvre les réponses interactives dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- App Home : Couvre l'App Home dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- Assistant Events : Couvre les événements assistant dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- Native Approvals : Couvre les approbations natives dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.
- Actions : Couvre les actions dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.
- Security-sensitive Ops : Couvre les opérations sensibles à la sécurité dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.
- Interactive Replies : Couvre les réponses interactives dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- App Home : Couvre l'App Home dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- Assistant Events : Couvre les événements assistant dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- Native Approvals : Couvre les approbations natives dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.
- Actions : Couvre les actions dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.
- Security-sensitive Ops : Couvre les opérations sensibles à la sécurité dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.

## Features

- Slash Commands : Couvre les Slash Commands dans le mode de commande slash configuré, les commandes slash natives, les attentes d'enregistrement de commande, les clés de session, et le comportement de routage des commandes slash natives et des commandes natives associées.
- Native Command Routing : Couvre le routage des commandes natives dans le mode de commande slash configuré, les commandes slash natives, les attentes d'enregistrement de commande, les clés de session, et le comportement de routage des commandes slash natives et des commandes natives associées.
- Interactive Replies : Couvre les réponses interactives dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- App Home : Couvre l'App Home dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- Assistant Events : Couvre les événements assistant dans le comportement de publication/ouverture de l'App Home, les événements de fil de discussion Slack assistant démarrés/contexte modifié, les actions de bloc, les soumissions modales, et le comportement associé des réponses interactives, de l'app home et des événements assistant.
- Native Approvals : Couvre les approbations natives dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.
- Actions : Couvre les actions dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.
- Security-sensitive Ops : Couvre les opérations sensibles à la sécurité dans les approbations natives et de plugin Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé des approbations natives, des actions et des opérations sensibles à la sécurité.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Beta (76%)`
- Positive signals: Les docs, les sources et les tests unitaires/runtime couvrent le mode de commande configuré, le mode explicite natif, les menus d'arguments natifs, les clés de session cible de commande, l'autorisation, les commandes de plugin, les commandes de compétence et les exigences d'URL HTTP.
- Negative signals: La voie Slack en direct standard n'inclut pas de scénario de commande slash, et l'enregistrement manuel de la commande côté Slack n'est pas automatiquement vérifié.
- Integration gaps: Ajouter des scénarios en direct pour le comportement du menu `/openclaw /help`, `/help` natif, `/stop`, `/approve`, `/model`, les expéditeurs de commande non autorisés, les URL de commande HTTP et la visibilité des commandes natives de plugin/compétence.

## Quality Score

- Score: `Beta (72%)`
- Gitcrawl reports: `#38302`, `#39605`, `#71665`, `#63059`, `#44297`, `#64578`, and `#74077` montrent le routage des commandes, l'enregistrement natif, le menu externe et le travail des commandes en mode progression.
- Discrawl reports: Les commentaires des responsables indiquent que la gestion des commandes natives Slack est implémentée pour le mode natif explicite, tandis que `commands.native: "auto"` reste intentionnellement désactivé et le problème `#39605` reste ouvert pour le routage de configuration capturée Discord/Slack.
- Good qualities: Les docs Slack avertissent explicitement que Slack ne crée ni ne supprime pas automatiquement les commandes slash et expliquent les différentes exigences d'URL Socket/HTTP.
- Bad qualities: L'enregistrement manuel de l'application Slack est facile à dériver de la configuration OpenClaw, et la visibilité des commandes natives/plugin a suffisamment de portes pour confondre les utilisateurs et les examinateurs.
- Excluded from quality: Nombre de tests unitaires, largeur de voie en direct et profondeur d'intégration.

## Completeness Score

- Score: `Beta (76%)`
- Surface instructions: évaluées par rapport à `references/completeness/slack.md`.
- Positive signals: Les preuves archivées des docs, sources, tests, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les Slash Commands, Native Command Routing, Interactive Replies, App Home, Assistant Events, Native Approvals, Actions, Security-sensitive Ops.
- Negative signals: La note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Missing capability branches: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Ajouter une voie de commande slash native en direct qui prouve le routage de session cible de commande dans les DM, les canaux et les fils de discussion.
- Ajouter des fragments de manifeste d'application Slack générés pour chaque ensemble de commandes natives activé.
- Ajouter une sortie d'état qui compare le `commands.native` configuré par rapport aux attentes d'enregistrement réelles de l'application Slack.

## Evidence

### Docs

- `docs/channels/slack.md` documente les commandes slash natives optionnelles, les exigences d'URL en mode HTTP, `channels.slack.slashCommand`, `commands.native`, les menus d'arguments natifs, les clés de session slash isolées et le dépannage pour les commandes natives/slash.
- `docs/tools/slash-commands.md` est la référence du catalogue de commandes partagées liée.

### Source

- `extensions/slack/src/monitor/slash.ts` analyse les charges slash, résout l'accès, les clés de session cible de commande, le mode natif, les commandes de plugin, les commandes de compétence et les menus d'arguments interactifs.
- `extensions/slack/src/monitor/commands.ts`, `slash-commands.runtime.ts`, `slash-dispatch.runtime.ts`, `slash-plugin-commands.runtime.ts`, and `slash-skill-commands.runtime.ts` implémentent la correspondance et la distribution des commandes.
- `extensions/slack/src/http/plugin-routes.ts` achemine les charges de commande slash HTTP.

### Integration tests

- Aucun scénario Slack slash-command en direct standard n'a été trouvé dans `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts`.
- Les tests de réponse/session partagés exercent les clés de session slash Slack et le comportement de routage des commandes dans les tests au niveau du processus.

### Unit tests

- `extensions/slack/src/monitor/slash.test.ts` and `slash.test-harness.ts` couvrent le comportement des commandes slash Slack.
- `extensions/slack/src/monitor/slash-commands.runtime.ts` est exercé par les tests de commandes runtime.
- `src/auto-reply/reply/session.test.ts` couvre les clés de session slash Slack et la gestion de la session cible.
- `src/plugins/commands.test.ts` couvre les spécifications de commandes de plugin natives du fournisseur Slack.

### Gitcrawl queries

Query:

- `gitcrawl search openclaw/openclaw --query "slack slash command" --json`

Results:

- Retourné `#38302` préfixe de commande native par compte, `#39605` commandes slash natives ignorant `session.dmScope`, `#39617` PR de routage de rechargement de configuration, `#44297` signal de santé de secours de menu d'argument externe, `#71665` commandes natives Slack via Socket Mode, `#63059` Slack `/stop`, et commentaires d'examen de commande de plugin sur `#64578`.

### Discrawl queries

Query:

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack slash command native commands"`

Results:

- Retourné des commentaires de responsable/GitHub en miroir confirmant la gestion des commandes natives Slack pour le mode natif explicite, en gardant `#39605` ouvert pour le routage de configuration capturée Slack/Discord, et en préservant les avertissements d'enregistrement de commande manuel.
