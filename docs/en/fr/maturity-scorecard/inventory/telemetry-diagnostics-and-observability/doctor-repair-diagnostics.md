---
title: "Observabilité - Note de Maturité des Diagnostics de Réparation Doctor"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Observabilité - Note de Maturité des Diagnostics de Réparation Doctor

## Résumé

`openclaw doctor` est la surface de diagnostics d'opérateur la plus large : elle explique les conclusions de santé, les migrations, la politique de réparation, l'état du service, l'authentification de la passerelle, l'état des plugins, la préparation des compétences et la sortie lint structurée. L'implémentation a un contrat de vérification de santé clair, mais la surface est suffisamment large pour que les vérifications nouvellement migrées et les vérifications détenues par les plugins puissent encore dériver.

## Portée de la Catégorie

- `openclaw doctor`, `openclaw doctor --fix`, `--repair`, `--yes`, `--non-interactive`, `--deep`, et `--lint`.
- Vérifications de santé structurées, conclusions, résultats de réparation, sélection de vérifications, sortie lint JSON, filtrage de sévérité et comportement de sortie.
- Vérifications doctor principales pour la configuration de la passerelle, les services, l'authentification, l'intégrité de l'état, les compétences, les plugins, le sandbox, les migrations et la santé des routes de fournisseur.
- Contrats doctor/santé du SDK de plugin.

## Fonctionnalités

- openclaw doctor : openclaw doctor, openclaw doctor --fix, --repair, --yes, --non-interactive, --deep, et --lint
- Vérifications de santé structurées : Vérifications de santé structurées, conclusions, résultats de réparation, sélection de vérifications, sortie lint JSON, filtrage de sévérité et comportement de sortie
- Vérifications doctor principales : Vérifications doctor principales pour la configuration de la passerelle, les services, l'authentification, l'intégrité de l'état, les compétences, les plugins, le sandbox, les migrations et la santé des routes de fournisseur
- Contrats doctor/santé du SDK de plugin : Comportement des contrats doctor/santé du SDK de plugin, statut et vérification visible par l'opérateur.

## Fraîcheur des Archives

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false`, et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git`, et `share.needs_update=true`.

## Score de Couverture

- Score : `Stable (80%)`
- Signaux positifs : Doctor dispose de docs dédiées, d'une source de vérification de santé structurée, de nombreux tests de commande, de tests doctor e2e et de scripts de publication/mise à jour qui exécutent les chemins de réparation.
- Signaux négatifs : La surface doctor est large, et pas chaque vérification détenue par un plugin n'a la même preuve de flux d'exécution.
- Lacunes d'intégration : Le `doctor --lint` structuré est solide pour les vérifications principales, tandis que le cycle de vie des packages de plugins et les vérifications doctor spécifiques aux canaux nécessitent une preuve de scénario récurrente.

## Score de Qualité

- Score : `Stable (81%)`
- Rapports Gitcrawl : Les rapports actuels sont principalement des durcissements actifs et des PR de migration, incluant la réparation de plugins configurés, l'ordre de contribution de santé et les limites de fuzzing de schéma/métadonnées.
- Rapports Discrawl : La requête Discord spécifique aux fonctionnalités n'a retourné aucun résultat direct de doctor-diagnostics, donc le silence des archives est traité comme neutre après les vérifications de fraîcheur.
- Bonnes qualités : Les docs et la source séparent le diagnostic en lecture seule de la mutation de réparation, exposent des ID de vérification stables et supportent la sortie lint lisible par machine.
- Mauvaises qualités : L'ampleur des vérifications signifie qu'une nouvelle migration ou un contrat de plugin peut être présent dans le code mais moins évident pour les opérateurs jusqu'à ce que les docs et les indices de réparation rattrapent.
- Exclus de la qualité : Les preuves unitaires, d'intégration, e2e, en direct et de flux d'exécution sont comptées uniquement sous Couverture, pas Qualité.

## Score de Complétude

- Score : `Stable (80%)`
- Instructions de surface : évaluées par rapport à `references/completeness/telemetry-diagnostics-and-observability.md`.
- Signaux positifs : les docs archivées, la source, les tests, Gitcrawl et les preuves Discrawl couvrent la portée de la taxonomie pour openclaw doctor, Vérifications de santé structurées, Vérifications doctor principales, Contrats doctor/santé du SDK de plugin.
- Signaux négatifs : la note archivée a précédé le score de Complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisés pour le score de Couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes Connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes Connues

- Les vérifications détenues par les plugins ne se lisent pas encore aussi uniformément documentées que les vérifications doctor principales.
- `doctor --fix --dry-run` et les rapports de diff plus riches sont décrits comme conviviales pour l'avenir par le contrat structuré mais ne constituent pas un flux de travail d'opérateur complet aujourd'hui.

## Preuves

### Docs

- `docs/cli/doctor.md` documente les postures doctor visibles par l'opérateur, le mode lint structuré, les conclusions JSON, la sélection de vérifications et les champs de vérification de santé structurés.
- `docs/gateway/doctor.md` documente le comportement de réparation et de migration, les groupes de vérifications principales, les audits de service et de superviseur et les modes non-interactifs.
- `docs/plugins/sdk-subpaths.md` répertorie `plugin-sdk/health` et `plugin-sdk/runtime-doctor` comme surfaces doctor/vérification de santé pour les auteurs de plugins.

### Source

- `src/commands/doctor.ts`, `src/commands/doctor-lint.ts`, `src/flows/doctor-core-checks.ts`, `src/flows/health-checks.ts` et `src/flows/doctor-repair-flow.ts` implémentent la détection doctor principale et le flux de réparation.
- `src/plugin-sdk/health.ts` et `src/plugin-sdk/runtime-doctor.ts` exposent les contrats de santé et doctor visibles par le SDK.
- `src/channels/plugins/doctor-contract-api.ts` et les contrats doctor des plugins de canal attachent les diagnostics spécifiques au fournisseur.

### Tests d'intégration

- `src/flows/doctor-core-checks.e2e.test.ts` exerce les vérifications de santé principales via un chemin de style e2e.
- `src/commands/doctor.runs-legacy-state-migrations-yes-mode-without.e2e.test.ts` et `src/commands/doctor.warns-state-directory-is-missing.e2e.test.ts` exercent les flux de commande doctor.
- `scripts/e2e/doctor-install-switch-docker.sh` et les scripts e2e de parcours utilisateur de publication exécutent la réparation doctor dans les scénarios d'installation/mise à jour.

### Tests unitaires

- `src/commands/doctor-lint.test.ts`, `src/commands/doctor-config-flow.test.ts`, `src/commands/doctor-gateway-services.test.ts`, `src/commands/doctor-security.test.ts` et de nombreux fichiers `src/commands/doctor/shared/*.test.ts` couvrent les vérifications et migrations ciblées.
- `src/flows/doctor-core-checks.test.ts`, `src/flows/doctor-health-contributions.test.ts` et `src/flows/bundled-health-checks.test.ts` couvrent le comportement des vérifications structurées.

### Requêtes Gitcrawl

Requête :

`gitcrawl search --json openclaw/openclaw --query "openclaw doctor diagnostics repair health check" --limit 5`

Résultats :

- 5 résultats. Les éléments pertinents incluent la PR #77219 réparant les plugins configurés avec des entrées d'exécution cassées, la PR #86627 préservant l'ordre de contribution de santé doctor, la PR #80455 supprimant les remorques `--fix` obsolètes, la PR #86210 touchant les diagnostics de résolution/statut de mémoire et la PR #87141 durcissant les limites de schéma et de métadonnées de plugin.

### Requêtes Discrawl

Requête :

`/Users/kevinlin/.local/bin/discrawl search --mode fts --limit 5 "openclaw doctor diagnostics repair health check"`

Résultats :

- 0 résultats retournés pour la requête de fonctionnalité exacte.
