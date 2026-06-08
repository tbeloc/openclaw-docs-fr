---
title: "ClawHub - Marketplace and Compatible Bundle Import Support Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# ClawHub - Marketplace and Compatible Bundle Import Support Maturity Note

## Résumé

Le support d'importation de bundles compatibles et de marketplace est relativement solide pour le sous-ensemble documenté. OpenClaw peut détecter les formats de bundles Codex, Claude et Cursor, lister les entrées de marketplace, installer les plugins de marketplace, mapper les compétences/commandes/hooks et les valeurs par défaut MCP/LSP/settings, et rejeter les chemins de marketplace distants non sécurisés. La couverture est Stable en raison d'un e2e de marketplace installé par paquet et de tests source larges. La qualité est Beta car plusieurs capacités de bundle sont intentionnellement détectées mais non exécutées et les preuves d'archive montrent un durcissement actif du schéma/métadonnées.

## Portée de la catégorie

- Détection de bundles compatibles Codex, Claude et Cursor.
- Chemins d'installation locaux, d'archive et de marketplace.
- Flux de liste, raccourci et installation de marketplace.
- Fonctionnalités mappées supportées et capacités détectées mais non exécutées.
- Sécurité des chemins de marketplace distants et protections de téléchargement d'archive.

## Fonctionnalités

- Codex: Détection de bundles compatibles Codex, Claude et Cursor
- Local: Chemins d'installation locaux, d'archive et de marketplace
- Marketplace list: Flux de liste, raccourci et installation de marketplace
- Supported mapped features: Fonctionnalités mappées supportées et capacités détectées mais non exécutées
- Remote marketplace path safety: Sécurité des chemins de marketplace distants et protections de téléchargement d'archive

## Fraîcheur de l'archive

- gitcrawl: `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl: `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score: `Stable (82%)`
- Signaux positifs: la documentation couvre clairement le support des bundles, la source valide les manifestes de marketplace et installe les entrées, et l'e2e installé par paquet prouve la liste, l'installation, l'exécution de commandes, la mise à jour et la désinstallation.
- Signaux négatifs: toutes les capacités de bundle détectées ne s'exécutent pas, et le comportement de marketplace distant montre des preuves de durcissement actif.
- Lacunes d'intégration: aucune matrice de compatibilité de marketplace tiers en direct n'a été trouvée sur les bundles réels Codex, Claude et Cursor.

## Score de qualité

- Score: `Beta (78%)`
- Bonnes qualités: les entrées de marketplace distantes sont limitées aux chemins relatifs, les téléchargements d'archive sont protégés, la résolution des raccourcis est explicite, et les capacités de bundle non supportées sont signalées au lieu d'être exécutées silencieusement.
- Mauvaises qualités: la limite de compatibilité est nécessairement partielle, et les utilisateurs peuvent s'attendre à ce que les capacités d'automatisation Claude/Cursor détectées s'exécutent alors qu'elles ne le font actuellement pas.
- Exclu de la qualité: les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution sont comptabilisées uniquement sous Couverture, pas Qualité.

## Score de complétude

- Score: `Stable (82%)`
- Instructions de surface: évaluées par rapport à `references/completeness/clawhub-and-external-plugin-distribution.md`.
- Signaux positifs: les preuves archivées de docs, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour Codex, Local, Marketplace list, Supported mapped features, Remote marketplace path safety.
- Signaux négatifs: la note archivée a précédé la notation de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuves et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes: voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une matrice de compatibilité pour les bundles réels Codex, Claude et Cursor avec les fonctionnalités mappées attendues et les fonctionnalités intentionnellement non supportées.
- Ajouter de la documentation/des exemples pour le comportement de confiance et de mise à jour du marketplace distant.

## Preuves

### Docs

- `docs/plugins/bundles.md:10`: OpenClaw peut installer des bundles Codex, Claude et Cursor.
- `docs/plugins/bundles.md:28`: les bundles s'installent à partir d'un répertoire, d'une archive ou d'un marketplace.
- `docs/plugins/bundles.md:66`: les fonctionnalités mappées supportées incluent les compétences, commandes, hooks, outils MCP, serveurs LSP et settings.
- `docs/plugins/bundles.md:199`: les agents Claude/hooks/styles de sortie, agents Cursor/hooks/règles et métadonnées inline/app Codex sont détectés mais non exécutés.
- `docs/cli/plugins.md:446`: la liste de marketplace accepte les chemins locaux, JSON de marketplace, raccourci GitHub, URLs de repo et URLs git.

### Source

- `src/plugins/bundle-manifest.ts:20`: définit les emplacements de manifeste Codex, Claude et Cursor.
- `src/plugins/marketplace.ts:878`: rejette les entrées de marketplace distantes non sécurisées telles que les chemins HTTP, les chemins absolus et les sources non-chemin.
- `src/plugins/marketplace.ts:1035`: liste les plugins de marketplace.
- `src/plugins/marketplace.ts:1059`: résout les raccourcis `plugin@marketplace`.
- `src/plugins/marketplace.ts:1105`: installe les entrées de marketplace via l'installateur de chemin normal.

### Tests d'intégration

- `scripts/e2e/lib/release-plugin-marketplace/scenario.sh:76`: liste les plugins de marketplace en JSON.
- `scripts/e2e/lib/release-plugin-marketplace/scenario.sh:79`: installe un plugin de marketplace.
- `scripts/e2e/lib/release-plugin-marketplace/scenario.sh:80`: vérifie la commande CLI appartenant au plugin après l'installation.
- `scripts/e2e/lib/release-plugin-marketplace/scenario.sh:91`: effectue une exécution à sec et une mise à jour de marketplace.
- `scripts/e2e/lib/release-plugin-marketplace/scenario.sh:96`: désinstalle le plugin de marketplace et vérifie la suppression de la commande.

### Tests unitaires

- `src/plugins/marketplace.test.ts:269`: liste les plugins à partir d'une racine de marketplace locale.
- `src/plugins/marketplace.test.ts:435`: installe les plugins de marketplace distants à partir de chemins relatifs dans le repo cloné.
- `src/plugins/marketplace.test.ts:691`: télécharge les sources de plugins d'archive via la protection SSRF.
- `src/plugins/marketplace.test.ts:1066`: signale les chemins de marketplace distants manquants comme non trouvés au lieu d'échappements.
- `src/plugins/bundle-manifest.test.ts:157`: couverture d'analyse de manifeste de bundle.

### Requêtes Gitcrawl

Requête:

- `gitcrawl search openclaw/openclaw --query "release-plugin-marketplace marketplace plugin" --limit 5 --json`

Résultats:

- Retourné #82216, concernant les plugins bundlés Codex ne s'activant pas à partir de `openclaw.json`.
- Retourné #75186, notant les RPC de navigation de marketplace de plugins manquants et les RPC de réparation de dépendances de plugins dans les APIs de gestion.
- Retourné #87141, un thread de durcissement pour les limites de fuzz de schéma/métadonnées et le comportement de fermeture en cas d'échec sur les champs de marketplace de liste de plugins Codex illisibles.

### Requêtes Discrawl

Requête:

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "marketplace plugin bundle Codex Claude install"`

Résultats:

- Retourné un résumé de version du 2026-03-23 indiquant que la version a livré la découverte de marketplace de plugins ClawHub et d'installation de bundles Claude/Codex/Cursor.
