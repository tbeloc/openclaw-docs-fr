---
title: "ClawHub - Note de Maturité pour l'Inventaire, l'Inspection, le Diagnostic et le Dépannage des Opérateurs"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# ClawHub - Note de Maturité pour l'Inventaire, l'Inspection, le Diagnostic et le Dépannage des Opérateurs

## Résumé

Les diagnostics des opérateurs sont larges et utiles : lister, inspecter, inspecter à l'exécution,
diagnostiquer, actualiser le registre, tables de dépannage, guidance des chemins bloqués et
la réparation de l'état des dépendances sont tous documentés. La couverture est Beta car les preuves de commande et
d'unité sont larges mais la preuve Gateway-vs-état-froid est inégale. La qualité
est Beta car les preuves d'archive montrent que `inspect` et `doctor` peuvent toujours manquer l'
état qui importe réellement pour une Gateway en cours d'exécution.

## Portée de la Catégorie

- `plugins list`, `plugins inspect`, inspection à l'exécution, `plugins doctor`, et
  `plugins registry`.
- Index de plugin local et état du registre froid persistant.
- Dépannage de la configuration obsolète, chemins bloqués, dépendances, plugins manquants,
  propriété dupliquée et configuration invalide.
- Vérification à l'exécution après redémarrage de la Gateway.

## Fonctionnalités

- plugins list: plugins list, plugins inspect, inspection à l'exécution, plugins doctor, et
- Index de plugin local : Index de plugin local et état du registre froid persistant
- Dépannage de la configuration obsolète : Dépannage de la configuration obsolète, chemins bloqués, dépendances, plugins manquants,
- Vérification à l'exécution après Gateway : Vérification à l'exécution après redémarrage de la Gateway

## Fraîcheur de l'Archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Beta (76%)`
- Signaux positifs : la documentation explique l'état froid par rapport à l'exécution, la source expose
  les commandes inspect/doctor/registry, et les tests couvrent la configuration obsolète, le
  nettoyage des dépendances, les enregistrements d'installation et le nettoyage de la désinstallation.
- Signaux négatifs : les preuves d'archive GitHub incluent des cas visibles par l'utilisateur où
  l'inspection/diagnostic CLI semblait sain tandis que le daemon longue durée ou l'état du fournisseur
  ne l'était pas.
- Lacunes d'intégration : une gate installée par paquet en direct devrait comparer le registre froid,
  l'inspection à l'exécution, le statut de la Gateway et le comportement réel des commandes/outils possédés par les plugins.

## Score de Qualité

- Score : `Beta (74%)`
- Bonnes qualités : la documentation dit explicitement aux utilisateurs quand redémarrer, quand
  utiliser l'inspection à l'exécution et quand `doctor --fix` est le bon chemin de réparation.
- Mauvaises qualités : la surface de l'outil a plusieurs vues chevauchantes de l'état du plugin, et le
  mode de défaillance le plus important est souvent dans la Gateway en cours d'exécution,
  pas le registre froid.
- Exclu de la qualité : les preuves de test unitaire, intégration, e2e, live et runtime-flow
  sont comptées uniquement sous Couverture, pas Qualité.

## Score de Complétude

- Score : `Beta (76%)`
- Instructions de surface : évaluées par rapport à `references/completeness/clawhub-and-external-plugin-distribution.md`.
- Signaux positifs : les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour plugins list, Index de plugin local, Dépannage de la configuration obsolète, Vérification à l'exécution après Gateway.
- Signaux négatifs : la note archivée a précédé le scoring de Complétude process-version-3, donc ce score est initialisé à partir de la même largeur de preuves et du registre de lacunes connues utilisé pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Ajouter un bundle de diagnostic en une seule commande qui lie l'index de plugin, le registre froid,
  l'inspection à l'exécution, la santé RPC de la Gateway et l'exécution de commandes possédées par les plugins.
- Rendre `plugins doctor` plus explicite quand il n'a pas vérifié le processus Gateway en cours d'exécution.

## Preuves

### Docs

- `docs/tools/plugin.md:104` : l'inspection à l'exécution vérifie les outils enregistrés, les hooks, les services, les méthodes Gateway et les commandes CLI.
- `docs/tools/plugin.md:193` : doctor répare les ids de plugin obsolètes, les incompatibilités allowlist/tool et les chemins de plugin bundlés hérités.
- `docs/tools/plugin.md:253` : le dépannage couvre list-vs-runtime, la propriété dupliquée, les plugins manquants, la configuration invalide, les chemins bloqués, le mode Nix, l'échec des dépendances et la forme du paquet.
- `docs/cli/plugins.md:296` : `plugins list` est un modèle de lecture froid et non une sonde d'exécution en direct.
- `docs/cli/plugins.md:416` : `plugins doctor` rapporte les erreurs de chargement, les diagnostics de manifeste, les avis de compatibilité et les références de configuration obsolète.
- `docs/cli/plugins.md:428` : `plugins registry` inspecte ou reconstruit le registre froid persistant.

### Source

- `src/cli/plugins-cli.ts:64` : enregistre `plugins list`.
- `src/cli/plugins-cli.ts:87` : enregistre `plugins inspect`.
- `src/cli/plugins-cli.ts:183` : enregistre `plugins registry`.
- `src/cli/plugins-cli.ts:193` : enregistre `plugins doctor`.
- `src/plugins/uninstall.ts:538` : la planification de désinstallation supprime les références de configuration et d'enregistrement d'installation que les diagnostics lisent plus tard.

### Tests d'intégration

- `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:45` : enregistre l'inspection à l'exécution après l'installation.
- `scripts/e2e/lib/release-plugin-marketplace/scenario.sh:76` : enregistre la liste JSON de la marketplace avant l'installation.
- `scripts/e2e/lib/release-plugin-marketplace/scenario.sh:101` : vérifie l'état du plugin désinstallé après la désinstallation.

### Tests unitaires

- `src/commands/doctor/shared/stale-plugin-config.test.ts:53` : trouve les références de politique et d'entrée de plugin obsolètes.
- `src/commands/doctor/shared/stale-plugin-config.test.ts:84` : supprime les références de politique obsolètes sans modifier les références valides.
- `src/commands/doctor/shared/stale-plugin-config.test.ts:317` : utilise les enregistrements d'installation persistants manquants comme preuve de canal obsolète.
- `src/plugins/uninstall.test.ts:745` : nettoie les références de politique obsolètes quand le code du plugin et les enregistrements d'installation sont disparus.
- `src/plugins/uninstall.test.ts:1512` : ne supprime jamais les chemins d'installation configurés arbitrairement.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "plugins list inspect doctor plugin registry install state" --limit 5 --json`

Résultats :

- A retourné #75186 pour les RPCs de gestion de plugins couvrant list, inspect, doctor, registry status/refresh et install.
- A retourné #87347, où `plugins inspect` et `plugins doctor` ont montré Brave chargé ou sain tandis que `web_search` n'avait toujours pas de fournisseur.
- A retourné #78105, qui demandait un chemin allowlist vide actionnable en utilisant `plugins list/inspect`.
- A retourné #78196, où les plugins d'extension ont été ignorés par le chargeur Gateway mais sont apparus dans l'inspection/diagnostic CLI.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "plugins inspect doctor registry status plugin issues"`

Résultats :

- N'a retourné aucun résultat, donc les preuves d'archive Discord n'ont pas ajouté plus de preuves spécifiques aux diagnostics.
