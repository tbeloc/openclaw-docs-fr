---
title: "Microsoft Teams - Diagnostics and Repair Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Microsoft Teams - Diagnostics and Repair Maturity Note

## Summary

Les diagnostics Teams sont utiles une fois que les identifiants existent : l'assistant de configuration signale l'état des identifiants, les vérifications de sonde contrôlent les jetons bot et Graph, la documentation couvre les erreurs de configuration courantes, et les erreurs d'envoi incluent des conseils exploitables. La couverture reste Alpha car l'audit n'a pas trouvé de scénario de réparation en direct détenu par OpenClaw pour l'installation propre, le consentement administrateur, les autorisations Graph, le médecin d'application Teams, le cache de manifeste obsolète ou les modifications de point de terminaison webhook.

## Category Scope

Cette catégorie couvre l'état de l'assistant de configuration, les invites d'identifiants, la détection des identifiants env, la documentation de configuration, les conseils `teams app doctor`, les vérifications de jetons de sonde, la création de rapports sur les rôles/portées Graph, l'état des jetons délégués, les avertissements de configuration, les hooks de santé des canaux, la documentation des délais d'expiration des webhooks et les conseils d'erreur pour les défaillances d'authentification, de limitation, transitoires, permanentes, réseau et proxy révoqué.

## Features

- Setup status: Couvre l'état de configuration dans l'état de l'assistant de configuration, les invites d'identifiants, la détection des identifiants env, la documentation de configuration et le comportement de diagnostic et de réparation associé.
- Probe and scope reporting: Couvre la création de rapports sur les sondes et les portées dans l'état de l'assistant de configuration, les invites d'identifiants, la détection des identifiants env, la documentation de configuration et le comportement de diagnostic et de réparation associé.
- Teams app doctor: Couvre le médecin d'application Teams dans l'état de l'assistant de configuration, les invites d'identifiants, la détection des identifiants env, la documentation de configuration et le comportement de diagnostic et de réparation associé.
- Webhook and health diagnostics: Couvre les diagnostics de webhook et de santé dans l'état de l'assistant de configuration, les invites d'identifiants, la détection des identifiants env, la documentation de configuration et le comportement de diagnostic et de réparation associé.
- Operator repair paths: Couvre les chemins de réparation des opérateurs dans l'état de l'assistant de configuration, les invites d'identifiants, la détection des identifiants env, la documentation de configuration et le comportement de diagnostic et de réparation associé.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, and `openai_key_present=true`.
- discrawl: `discrawl status --json` succeeded with `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, and `share.needs_update=true`.

## Coverage Score

- Score: `Alpha (58%)`
- Positive signals: La documentation couvre les défaillances courantes de configuration de Teams ; la source implémente l'état de configuration, la sonde, la création de rapports sur les rôles/portées Graph et les conseils d'erreur d'envoi.
- Negative signals: Aucun scénario de réparation en direct par l'opérateur n'a été trouvé pour le médecin d'application Teams, le cache de manifeste obsolète, l'échec de la permission RSC, l'échec du consentement administrateur Graph ou la réparation du point de terminaison webhook.
- Integration gaps: Preuve de réparation manquante qui commence par des identifiants cassés, consentement Graph manquant, URL de service invalide, manifeste obsolète, chargement latéral bloqué et états de webhook inaccessibles.

## Quality Score

- Score: `Alpha (64%)`
- Gitcrawl reports: La requête de diagnostic/sonde ciblée a retourné `[]` ; la recherche Teams large a mis en surface le travail actif du SDK Teams, des pièces jointes, du locataire Graph et des informations sur les membres que les diagnostics devraient aider les opérateurs à comprendre.
- Discrawl reports: La requête de diagnostic ciblée n'a retourné aucune ligne ; la recherche Teams large a montré des commentaires d'opérateurs sur la complexité de la configuration de Teams.
- Good qualities: La sonde signale l'état du jeton bot et du jeton Graph, la documentation inclut des étapes de dépannage concrètes, l'assistant de configuration peut détecter les identifiants env et les erreurs d'envoi ont des conseils spécifiques au canal.
- Bad qualities: Le chemin de diagnostic le plus fort pointe toujours les opérateurs vers les outils CLI/administrateur Microsoft, et OpenClaw ne possède pas encore un scénario de réparation durable pour la dérive du consentement administrateur ou du manifeste d'application.
- Excluded from quality: Nombre de tests de sonde, nombre de tests de configuration et absence de tests de réparation en direct.

## Completeness Score

- Score: `Alpha (58%)`
- Surface instructions: évalué par rapport à `references/completeness/microsoft-teams.md`.
- Positive signals: les documents archivés, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour l'état de configuration, la création de rapports sur les sondes et les portées, le médecin d'application Teams, les diagnostics de webhook et de santé, les chemins de réparation des opérateurs.
- Negative signals: la note archivée a précédé la notation de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Missing capability branches: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Known Gaps

- Ajouter des fiches de réparation pour les identifiants manquants, le mauvais secret, le consentement Graph manquant, la permission RSC bloquée, le manifeste obsolète, le mauvais chemin webhook, l'URL `serviceUrl` invalide et la dérive du cache d'application Teams.
- Ajouter un wrapper ou une liste de contrôle qui enregistre la sortie `teams app doctor` dans un artefact OpenClaw durable.
- Ajouter des diagnostics qui distinguent les portées déclarées dans le manifeste des portées accordées par le locataire.

## Evidence

### Docs

- `docs/channels/msteams.md` documente `teams app doctor`, les symptômes de délai d'expiration du webhook, les erreurs de téléchargement du manifeste d'application, le dépannage des permissions RSC, le comportement de réinstallation/cache de l'application, le dépannage des canaux sans réponse et les références à la documentation de configuration Microsoft.
- `docs/gateway/config-channels.md` documente le chemin de configuration `channels.msteams` et établit un lien vers la documentation Teams complète.
- `docs/gateway/health.md` inclut Microsoft Teams parmi les surfaces de remplacement du moniteur de canal intégré.

### Source

- `extensions/msteams/src/setup-core.ts` et `setup-surface.ts` implémentent l'état de configuration, les invites d'identifiants et la finalisation de la configuration.
- `extensions/msteams/src/probe.ts` vérifie l'acquisition de jetons bot, les rôles/portées des jetons Graph et l'état des jetons délégués.
- `extensions/msteams/src/errors.ts` classe les erreurs d'authentification, de limitation, transitoires, permanentes, réseau, flux de contenu et proxy révoqué et formate les conseils spécifiques à Teams.
- `extensions/msteams/src/doctor.ts` collecte les avertissements de liste d'autorisation mutable.
- `extensions/msteams/src/channel.ts` expose l'intégration de l'état/sonde et les avertissements de sécurité.
- `extensions/msteams/src/webhook-timeouts.ts` applique le renforcement du délai d'expiration du webhook.

### Integration tests

- Aucun scénario de configuration/diagnostic/réparation Teams en direct n'a été trouvé par `rg`.
- `monitor.test.ts` fournit une preuve de délai d'expiration HTTP local, mais pas une réparation de configuration de bout en bout côté Microsoft.

### Unit tests

- `extensions/msteams/src/setup-surface.test.ts` couvre l'état de configuration et les invites.
- `extensions/msteams/src/probe.test.ts` couvre les identifiants manquants et les résultats d'acquisition de jetons.
- `extensions/msteams/src/errors.test.ts` couvre la classification des erreurs et les conseils.
- `extensions/msteams/src/channel.test.ts` couvre la validation du schéma cloud/URL de service.
- `extensions/msteams/src/cloud.test.ts` couvre les défaillances limites cloud/URL de service.

### Gitcrawl queries

Query:

- `gitcrawl search openclaw/openclaw --query "msteams doctor probe setup diagnostics credentials" --json --limit 10`

Results:

- La requête de diagnostic ciblée a retourné `[]`.

### Discrawl queries

Query:

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "msteams doctor probe diagnostics credentials"`
- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --limit 10 "Microsoft Teams"`

Results:

- La requête de diagnostic ciblée n'a retourné aucune ligne.
- La requête Microsoft Teams large a retourné des commentaires d'opérateurs sur la complexité de la configuration/administration Microsoft et le souhait d'un rapport Microsoft Teams.
