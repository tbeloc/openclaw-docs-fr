---
title: "Observabilité - Note de Maturité de la Santé et de la Réparation"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité de la Santé et de la Réparation

## Résumé

La surface de sonde de santé et de statut est un point d'entrée d'opérateur mature pour vérifier la disponibilité de la passerelle, l'état par canal, l'état du compte, la disponibilité des agents, les résumés du magasin de sessions, la santé de la tarification des modèles et la santé de la boucle d'événements. L'écart principal n'est pas le contrat de sonde lui-même, mais les rapports d'opérateur récurrents où un canal semble sain alors qu'un compte spécifique ou un chemin de livraison est dégradé.

## Portée de la Catégorie

Inclus dans cette catégorie :

- Boucle de surveillance de la santé en arrière-plan : Boucle de surveillance de la santé en arrière-plan pour les comptes de canal configurés
- Paramètres d'activation/désactivation par compte : Comportement des paramètres d'activation/désactivation par compte, statut et vérification visible par l'opérateur.
- Grâce au démarrage : Grâce au démarrage, grâce de connexion, détection d'activité de transport obsolète, gestion des blocages/arrêts, délais de refroidissement de redémarrage et redémarrages maximum par heure
- Journalisation des redémarrages : Journalisation des redémarrages et évaluation des instantanés d'exécution
- openclaw doctor : openclaw doctor, openclaw doctor --fix, --repair, --yes, --non-interactive, --deep, et --lint
- Vérifications de santé structurées : Vérifications de santé structurées, résultats, résultats de réparation, sélection de vérification, sortie JSON lint, filtrage de sévérité et comportement de sortie
- Vérifications de docteur de base : Vérifications de docteur de base pour la configuration de la passerelle, les services, l'authentification, l'intégrité de l'état, les compétences, les plugins, le bac à sable, les migrations et la santé de la route du fournisseur
- Contrats de docteur/santé du SDK de plugin : Comportement des contrats de docteur/santé du SDK de plugin, statut et vérification visible par l'opérateur.
- openclaw status : openclaw status, openclaw status --all, et openclaw status --deep
- openclaw health : openclaw health, openclaw health --verbose, et openclaw health --json
- Santé RPC de la passerelle : Santé RPC de la passerelle et statut
- Instantanés de santé en cache : Instantanés de santé en cache, actualisation de sonde en direct, champs sensibles contrôlés par la portée d'administrateur d'opérateur et attachement de santé de boucle d'événements

## Fonctionnalités

- Boucle de surveillance de la santé en arrière-plan : Boucle de surveillance de la santé en arrière-plan pour les comptes de canal configurés
- Paramètres d'activation/désactivation par compte : Comportement des paramètres d'activation/désactivation par compte, statut et vérification visible par l'opérateur.
- Grâce au démarrage : Grâce au démarrage, grâce de connexion, détection d'activité de transport obsolète, gestion des blocages/arrêts, délais de refroidissement de redémarrage et redémarrages maximum par heure
- Journalisation des redémarrages : Journalisation des redémarrages et évaluation des instantanés d'exécution
- openclaw doctor : openclaw doctor, openclaw doctor --fix, --repair, --yes, --non-interactive, --deep, et --lint
- Vérifications de santé structurées : Vérifications de santé structurées, résultats, résultats de réparation, sélection de vérification, sortie JSON lint, filtrage de sévérité et comportement de sortie
- Vérifications de docteur de base : Vérifications de docteur de base pour la configuration de la passerelle, les services, l'authentification, l'intégrité de l'état, les compétences, les plugins, le bac à sable, les migrations et la santé de la route du fournisseur
- Contrats de docteur/santé du SDK de plugin : Comportement des contrats de docteur/santé du SDK de plugin, statut et vérification visible par l'opérateur.
- openclaw status : openclaw status, openclaw status --all, et openclaw status --deep
- openclaw health : openclaw health, openclaw health --verbose, et openclaw health --json
- Santé RPC de la passerelle : Santé RPC de la passerelle et statut
- Instantanés de santé en cache : Instantanés de santé en cache, actualisation de sonde en direct, champs sensibles contrôlés par la portée d'administrateur d'opérateur et attachement de santé de boucle d'événements

## Fraîcheur de l'Archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (84%)`
- Signaux positifs : La santé et le statut sont exposés dans les docs, CLI, la passerelle RPC, les méthodes RPC orientées Control UI et les suites serveur/authentification ; les chemins de sonde en direct et de sonde en cache sont tous deux exercés.
- Signaux négatifs : La preuve en environnement réel est la plus forte pour le statut de passerelle de base et plus faible pour les sondes de compte par fournisseur sur chaque canal.
- Lacunes d'intégration : Les flux de travail des opérateurs s'appuient toujours sur des commandes de suivi par canal lorsqu'un runtime de canal est partiellement dégradé malgré un processus de passerelle sain.

## Score de Qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl : Les rapports de santé/statut ouverts montrent des cas de non-concordance canal-compte et de dégradation d'exécution plutôt qu'une API de santé cassée.
- Rapports Discrawl : Les rapports d'archive Discord recommandent à plusieurs reprises `openclaw status --all`, `openclaw gateway status` et `openclaw channels status --probe` pour le triage d'instabilité de canal.
- Bonnes qualités : La source sépare les instantanés en cache des sondes en direct, masque les champs sensibles sauf si l'appelant a la portée d'administrateur et attache la santé de la boucle d'événements le cas échéant.
- Mauvaises qualités : Le vocabulaire de sonde laisse encore place à la confusion de l'opérateur lorsqu'une passerelle est accessible mais qu'un canal/compte spécifique est bloqué ou désynchronisé.
- Exclu de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution sont comptées uniquement sous Couverture, pas Qualité.

## Score de Complétude

- Score : `Stable (84%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : Les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la Boucle de surveillance de la santé en arrière-plan, les Paramètres d'activation/désactivation par compte, la Grâce au démarrage, la Journalisation des redémarrages, openclaw doctor, les Vérifications de santé structurées, les Vérifications de docteur de base, les Contrats de docteur/santé du SDK de plugin, openclaw status, openclaw health, la Santé RPC de la passerelle, les Instantanés de santé en cache.
- Signaux négatifs : La note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- La sémantique de santé inter-canaux n'est pas également riche pour chaque fournisseur.
- La formulation du statut pourrait mieux distinguer la disponibilité de la passerelle de la santé de livraison au niveau du compte.

## Preuves

### Docs

- `docs/gateway/health.md` documente les vérifications rapides, les diagnostics approfondis, la configuration du moniteur de santé, la gestion des défaillances et la sortie dédiée `openclaw health`.
- `docs/cli/health.md` documente les drapeaux `openclaw health` et le comportement de sonde en cache par rapport à en direct.
- `docs/gateway/protocol.md` documente les méthodes RPC `health` et système/statut associées.

### Source

- `src/gateway/server-methods/health.ts` implémente RPC `health` et `status`, actualisation d'instantané en cache, détection de différence d'exécution, fusion de santé de tarification de modèle et vérifications de portée de champ sensible.
- `src/commands/health.ts`, `src/commands/health-format.ts` et `src/commands/status.ts` fournissent le formatage et la sonde de santé/statut orientés CLI.
- `src/gateway/server-methods/channels.ts` contribue aux détails de statut par canal et de santé de boucle d'événements à la surface de l'opérateur.

### Tests d'intégration

- `src/gateway/server.auth.control-ui.suite.ts` exerce l'accès au statut et à la santé authentifiés via le serveur de passerelle.
- `src/gateway/server.roles-allowlist-update.test.ts` exerce les appels de santé nœud/client via le chemin de passerelle.
- `scripts/e2e/kitchen-sink-rpc-walk.mjs` inclut la couverture de marche RPC de passerelle pour les méthodes de diagnostics orientées opérateur.

### Tests unitaires

- `src/gateway/server-methods/server-methods.test.ts` exerce l'actualisation du cache de santé, les sondes en direct, la gestion de la boucle d'événements et le comportement RPC adjacent `logs.tail`.
- `src/commands/health.test.ts` exerce le comportement et le formatage d'instantané de santé.
- `src/commands/health.snapshot.test.ts` maintient le rendu d'instantané de santé stable.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "gateway health status probe channel health monitor" --limit 5`

Résultats :

- 5 résultats. Les éléments ouverts les plus pertinents étaient PR #80805 `SUP-1563 restore channel responsiveness health`, issue #75153 demandant la récupération CLI de démarrage/arrêt/redémarrage de canal, issue #79304 sur la course d'exécution Weixin après redémarrage de passerelle, PR #76701 sur le bruit de délai d'expiration de démarrage Feishu et PR #78186 utilisant `openclaw health` comme preuve de réactivité de passerelle.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "gateway health status probe channel health monitor"`

Résultats :

- 5 résultats. L'archive incluait des fils Discord et Telegram d'instabilité d'exécution où le support demande aux opérateurs `openclaw --version`, `openclaw status --all`, `openclaw gateway status` et `openclaw channels status --probe` ; un fil rapporte un processus de passerelle qui reste sain tandis que les runtimes de canal Telegram et Discord redémarrent ou se déconnectent.
