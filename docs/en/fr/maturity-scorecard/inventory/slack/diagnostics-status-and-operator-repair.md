---
title: "Slack - Diagnostics, Status, and Operator Repair Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Slack - Diagnostics, Status, and Operator Repair Maturity Note

## Summary

Le support de l'opérateur Slack inclut l'état des canaux, l'inspection des comptes, les diagnostics de capacité, les résultats du docteur/sécurité, les diagnostics de portée, le comportement des sondes, la documentation de dépannage et la migration/réparation de configuration. La couverture est Beta car la couverture source et unitaire est large, mais la preuve de réparation en direct est inégale. La qualité est Beta car l'enregistrement de l'opérateur affiche toujours la découverte de portée `unknown_method`, `missing_scope`, les secrets configurés-indisponibles, les ID de canal bloqués silencieusement, et les sondes de transport qui peuvent sembler saines alors que les événements sont cassés.

## Category Scope

Cette catégorie couvre `openclaw channels status --probe`, les instantanés de compte, les champs source/statut du jeton, les diagnostics de capacité et de portée, les correctifs du docteur, les résultats de l'audit de sécurité, la documentation de dépannage, les avertissements de migration, la migration des ID de canal, les problèmes de statut et les boucles de réparation de l'opérateur.

## Features

- Channel status diagnostics: Couvre `openclaw channels status --probe`, les instantanés de compte, les champs source/statut du jeton, les diagnostics de capacité et de portée, et les conseils de réparation Slack.
- Slack account status: Couvre les instantanés de compte, les champs source/statut du jeton, les résumés de capacité et la sortie de statut Slack.
- Operator Repair: Couvre la réparation de l'opérateur sur `openclaw channels status --probe`, les instantanés de compte, les champs source/statut du jeton, les diagnostics de capacité et de portée, et le comportement de diagnostics, statut et réparation de l'opérateur associé.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Coverage Score

- Score: `Beta (74%)`
- Positive signals: L'inspection des comptes, les diagnostics de capacité, les résumés de statut, les vérifications du docteur, l'audit de sécurité, la migration de configuration, la migration des ID de canal et la copie de dépannage ont tous une couverture source et unitaire.
- Negative signals: L'assurance qualité Slack en direct ne valide pas directement la réparation du docteur, la signalisation des problèmes de statut, les chemins SecretRef-indisponibles, les replis de découverte de portée ou la réparation de statut en mode HTTP.
- Integration gaps: Ajouter des scénarios en direct/opérateur pour `channels status --probe`, `channels capabilities`, `doctor --fix`, diagnostic de portée manquante, SecretRefs `configured_unavailable`, blocage de nom de canal et vivacité Socket Mode obsolète.

## Quality Score

- Score: `Beta (72%)`
- Gitcrawl reports: `#44297`, `#75076`, `#44692`, `#44625`, `#43504`, `#63389`, et les résultats larges de `slack doctor status probe` montrent un travail actif de diagnostic de capacité/statut/portée/configuration.
- Discrawl reports: La sortie de capacité a montré que les portées de bot Slack retournaient `unknown_method` pour `auth.scopes`/`apps.permissions.info`; les threads de support ont régulièrement eu besoin de journaux, de sondes de statut, de correctifs de portée manquante, de réinstallation d'application et de conseils d'ID de canal stable.
- Good qualities: La documentation donne un ordre de dépannage pour aucune réponse de canal, DM ignorés, défaillances Socket Mode, défaillances en mode HTTP et problèmes de commande native.
- Bad qualities: Certains diagnostics nécessitent toujours d'interpréter l'état administrateur côté Slack, les sondes peuvent ne pas prouver la livraison d'événement entrant, et les listes blanches de canaux basées sur le nom peuvent bloquer silencieusement les messages.
- Excluded from quality: Nombre de tests unitaires, largeur de voie en direct et profondeur d'intégration.

## Completeness Score

- Score: `Beta (74%)`
- Surface instructions: évalué par rapport à `references/completeness/slack.md`.
- Positive signals: Les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour les diagnostics d'état des canaux, l'état du compte Slack, la réparation de l'opérateur.
- Negative signals: La note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Missing capability branches: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Ajouter un diagnostic Slack unique "pourquoi pas de réponse?" qui joint la configuration, le jeton, la portée, l'installation de l'application, l'adhésion au canal, la politique de groupe et la vivacité des événements.
- Ajouter une copie de problème de statut pour les sondes qui passent sur l'API Web tandis que les événements Socket Mode sont obsolètes ou manquants.
- Ajouter une réparation du docteur pour la dérive courante du manifeste/portée Slack où c'est sûr, ou une liste de contrôle UI Slack générée exacte où ce n'est pas sûr.

## Evidence

### Docs

- `docs/channels/slack.md` documente le comportement de l'instantané de statut, le dépannage pour aucune réponse de canal, DM ignorés, Socket Mode, mode HTTP et commandes natives.
- `docs/channels/troubleshooting.md`, `docs/gateway/troubleshooting.md` et `docs/gateway/config-channels.md` sont liés comme références de diagnostic partagées.

### Source

- `extensions/slack/src/account-inspect.ts` rapporte le mode, les sources/statuts des credentials, la politique de groupe, les modes de réponse, les actions et les paramètres de média.
- `extensions/slack/src/channel.ts` implémente les résumés de statut, les diagnostics de capacité, les sondes et les récupérations de portée.
- `extensions/slack/src/doctor.ts`, `security-doctor.ts`, `security-audit.ts` et `channel-migration.ts` implémentent les aides de réparation/audit/migration.
- `src/infra/channels-status-issues.test.ts` inclut la collecte des problèmes de statut Slack à partir des plugins de canal.

### Integration tests

- `extensions/qa-lab/src/live-transports/slack/slack-live.runtime.ts` émet des rapports d'assurance qualité Slack et des artefacts de messages observés mais ne valide pas la réparation du docteur/statut comme scénarios autonomes.
- `docs/concepts/qa-e2e-automation.md` documente les artefacts de sortie Slack en direct pour l'utilisation de rapports et de débogage.

### Unit tests

- `extensions/slack/src/channel.lazy-seams.test.ts` couvre le résumé de statut et les diagnostics de capacité du transfert SDK paresseux.
- `extensions/slack/src/doctor.test.ts`, `security-audit.test.ts`, `channel-migration.test.ts`, `probe.test.ts`, `scopes.test.ts` et `errors.test.ts` couvrent le comportement de diagnostics et de réparation.
- `extensions/slack/src/config-schema.test.ts` valide le rejet de configuration invalide qui alimente la réparation de l'opérateur.

### Gitcrawl queries

Query:

- `gitcrawl search openclaw/openclaw --query "slack doctor status probe" --json`
- `gitcrawl search openclaw/openclaw --query "Slack" --json`

Results:

- La requête de statut/sonde ciblée a retourné des rapports de statut/sonde adjacents et `#87168` montrant Slack configuré dans la sortie de santé de la passerelle.
- Les résultats Slack plus larges incluaient `#44297` signal de santé du menu d'arguments externe, `#75076` avertissements de statut avec champs de santé Slack/canal, et des correctifs de portée/configuration tels que `#44692` et le travail de portée du manifeste d'intégration.

### Discrawl queries

Query:

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Slack channels status probe doctor missing_scope"`

Results:

- A retourné des exemples de capacité/statut Slack où Slack a signalé configuré/en cours d'exécution/fonctionne tandis que la découverte de portée de bot a retourné `unknown_method`, plus des conseils de support pour inspecter `missing_scope`, `not_in_channel`, `Forbidden` et les journaux 401/403.
