---
title: "ClawHub - Catalog Discovery Maturity Note"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# ClawHub - Catalog Discovery Maturity Note

## Résumé

La découverte ClawHub est présente dans l'interface CLI et la documentation destinées aux utilisateurs, mais la maturité est Alpha/Beta-edge car OpenClaw consomme principalement le catalogue distant plutôt que de posséder ou de prouver le service de catalogue complet. La commande recherche les familles `code-plugin` et `bundle-plugin` installables, affiche les indices d'installation et documente ClawHub comme surface de découverte principale. Les preuves manquantes sont l'assurance qualité du catalogue en direct, la preuve de la version du service de catalogue et la couverture des régressions des métadonnées d'affichage.

## Portée de la catégorie

Inclus dans cette catégorie :

- openclaw plugins search en tant que ClawHub : openclaw plugins search en tant que commande de recherche de plugin ClawHub
- Métadonnées des résultats de recherche : nom du package, famille, canal, version, résumé, et
- Distinction entre la recherche de plugin : Distinction entre la recherche de plugin et la recherche de compétence
- Échec de la recherche de catalogue : Échec de la recherche de catalogue et comportement de résultat vide

## Fonctionnalités

- openclaw plugins search en tant que ClawHub : openclaw plugins search en tant que commande de recherche de plugin ClawHub
- Métadonnées des résultats de recherche : nom du package, famille, canal, version, résumé, et
- Distinction entre la recherche de plugin : Distinction entre la recherche de plugin et la recherche de compétence
- Échec de la recherche de catalogue : Échec de la recherche de catalogue et comportement de résultat vide
- Recherche de catalogue de compétences : Rechercher, lister, inspecter et installer les compétences suivies par ClawHub à partir de l'interface CLI.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (66%)`
- Signaux positifs : la documentation décrit le comportement de recherche ClawHub et de sélection de source ; la commande CLI filtre les familles de packages de plugin installables et dispose de tests unitaires pour le formatage de la recherche et les chemins d'erreur.
- Signaux négatifs : aucune preuve d'intégration de recherche ClawHub en direct ou porte de version end-to-end du service de catalogue n'a été trouvée dans l'audit du référentiel OpenClaw.
- Lacunes d'intégration : les métadonnées d'affichage, la disponibilité du package, l'état de l'analyse et les indices d'installation sont consommés à partir de ClawHub mais ne sont pas prouvés par une matrice de version ici.

## Score de qualité

- Score : `Beta (72%)`
- Bonnes qualités : l'interface CLI a un contrat étroit et lisible, fixe les limites, déduplique les résultats de famille, sépare la recherche de plugin et de compétence, et affiche des indices d'installation concrets.
- Mauvaises qualités : le catalogue visible par l'utilisateur dépend de la qualité des métadonnées ClawHub distantes, et les preuves d'archive montrent que les métadonnées d'affichage recevaient toujours des commentaires bêta.
- Exclus de la qualité : les preuves de test unitaire, intégration, e2e, en direct et de flux d'exécution ne sont comptées que sous Couverture, pas Qualité.

## Score de complétude

- Score : `Alpha (66%)`
- Instructions de surface : évaluées par rapport à `references/completeness/clawhub-and-external-plugin-distribution.md`.
- Signaux positifs : les preuves archivées de documentation, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour openclaw plugins search en tant que ClawHub, Métadonnées des résultats de recherche, Distinction entre la recherche de plugin, Échec de la recherche de catalogue, Recherche de catalogue de compétences.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Known Gaps` et `## Evidence` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter une preuve en direct du package installé pour `openclaw plugins search` par rapport à la route de recherche de package ClawHub de production ou de staging.
- Ajouter une fixture de métadonnées de catalogue qui prouve le résumé, le nom d'affichage, le canal, la dernière version, l'état de l'analyse/disponibilité et le rendu des indices d'installation ensemble.

## Preuves

### Documentation

- `docs/tools/plugin.md:35` : le guide de démarrage rapide indique aux utilisateurs de rechercher des packages de plugin publics sur ClawHub.
- `docs/tools/plugin.md:42` : ClawHub est documenté comme la surface de découverte principale.
- `docs/cli/plugins.md:129` : `plugins search` interroge ClawHub et recherche des packages de plugin, pas des compétences.
- `docs/cli/plugins.md:306` : la recherche est documentée comme une recherche de catalogue distant qui ne modifie pas l'état local.
- `docs/plugins/community.md:10` : les plugins communautaires utilisent ClawHub comme surface de découverte publique principale.

### Source

- `src/cli/plugins-cli.ts:75` : enregistre `openclaw plugins search`.
- `src/cli/plugins-search-command.ts:16` : limite la recherche de plugin aux familles `code-plugin` et `bundle-plugin`.
- `src/cli/plugins-search-command.ts:57` : formate la famille, le canal, la version, le résumé et l'indice d'installation.
- `src/cli/plugins-search-command.ts:82` : fixe les limites de recherche avant d'interroger.
- `src/infra/clawhub.ts:940` : appelle `/api/v1/packages/search` avec les paramètres de requête, de famille et de limite.

### Tests d'intégration

- Aucun test d'intégration de recherche ClawHub en direct avec package installé n'a été trouvé pour ce composant.

### Tests unitaires

- `src/cli/plugins-search-command.test.ts:41` : couverture de recherche au niveau de la commande.
- `src/infra/clawhub.test.ts:745` : le JSON de recherche ClawHub mal formé est rejeté pour les API de recherche.

### Requêtes Gitcrawl

Requête :

- `gitcrawl search openclaw/openclaw --query "ClawHub catalog metadata display package lookup install hints" --limit 5 --json`
- `gitcrawl search openclaw/openclaw --query "ClawHub plugin display metadata" --limit 10 --json`

Résultats :

- La première requête n'a retourné aucun résultat.
- La deuxième requête a trouvé #87486, un fil de commentaires bêta mentionnant les noms d'affichage ClawHub, et #86612, un problème d'exécution qui incluait un contexte d'installation de plugin externe officiel.

### Requêtes Discrawl

Requête :

- `DISCRAWL_NO_AUTO_UPDATE=1 /Users/kevinlin/.local/bin/discrawl search --mode hybrid --limit 5 "ClawHub plugin display metadata catalog"`

Résultats :

- N'a retourné aucun résultat, donc les preuves d'archive Discord n'ont pas ajouté de preuve d'affichage de catalogue en direct.
