---
title: Plugins - Authoring and Packaging Plugins Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Plugins - Authoring and Packaging Plugins Maturity Note

## Summary

La création et l'empaquetage de plugins constituent la surface de capacité publique combinée pour les auteurs. OpenClaw fournit aux auteurs de plugins un chemin documenté via `building-plugins`, l'aperçu du Plugin SDK et le catalogue des points d'entrée, des conseils de sous-chemin ciblés, des cartes d'export générées et des shims de compatibilité pour les anciens flux d'auteur. Il définit également le contrat de package et de manifeste via `openclaw.plugin.json`, `package.json#openclaw`, les métadonnées de compatibilité et la validation de la publication/installation.

La catégorie reste Beta sur la couverture et la qualité. Les preuves d'empaquetage sont plus solides que les preuves d'importation du SDK public, mais la catégorie fusionnée doit rester limitée à la création : la preuve de création la plus solide est toujours la couverture d'importation de package empaqueté représentatif et la couverture de smoke de type plutôt que la validation exhaustive du parcours d'auteur sur toute la surface du SDK public, les commandes de validation détenues par la taxonomie ont été bloquées localement par des défaillances d'authentification du registre, et les preuves d'archive montrent toujours des réparations de compatibilité actives plus une pression plus large pour simplifier la surface orientée auteur.

## Category Scope

- Le parcours d'auteur documenté pour construire des plugins avec le Plugin SDK public.
- Les importations du Plugin SDK racine et ciblées que les auteurs de plugins peuvent utiliser dans les installations source et empaquetées.
- Les exigences du manifeste de plugin natif dans `openclaw.plugin.json`, y compris l'identité, le schéma de configuration, les contrats déclarés et les métadonnées de configuration de canal.
- Les métadonnées de package de plugin externe sous `package.json#openclaw`, y compris la compatibilité, le runtime, la compilation et les métadonnées d'installation.
- La découverte des points d'entrée, les conseils sur le statut de support et les shims de migration qui aident les auteurs à passer entre les anciens et les nouveaux modèles de création.
- La carte d'export générée et les règles d'aliasing qui font que ces importations orientées auteur se résolvent dans les contextes source, dist et package installé.
- L'application au moment de l'installation et de la publication pour les manifestes mal formés, les métadonnées de compatibilité de package mal formées, les fichiers de manifeste manquants et l'exhaustivité des artefacts empaquetés.
- Les hooks de gouvernance qui maintiennent la surface du SDK orientée auteur alignée avec l'inventaire enregistré.
- Hors de portée : le cycle de vie du runtime après l'acceptation d'un contrat de plugin, la qualité du comportement des capacités individuelles de canal, fournisseur, mémoire ou média, et le comportement du runtime spécifique au canal/fournisseur au-delà de ce que le manifeste ou le contrat de package déclare à l'avance.

## Features

- Point d'entrée SDK racine : Les auteurs de plugins utilisent le point d'entrée du Plugin SDK racine supporté lorsque le contrat de haut niveau est suffisant.
- Importations SDK ciblées : Les auteurs de plugins utilisent les sous-chemins du Plugin SDK ciblés au lieu de s'appuyer sur un seul point d'entrée fourre-tout.
- Découverte des points d'entrée : Les auteurs de plugins découvrent les points d'entrée publics supportés et leur statut de support à partir de la documentation du SDK et du catalogue des points d'entrée.
- Shims de migration : Les sous-chemins dépréciés ou de compatibilité continuent à se résoudre pendant les migrations d'auteur.
- Manifeste de plugin : `openclaw.plugin.json` déclare l'identité du plugin, les capacités et le schéma de configuration.
- Métadonnées de package : `package.json` porte les métadonnées `openclaw` requises pour les flux de découverte et de publication.
- Compatibilité du runtime : Les packages de plugin déclarent la compatibilité du runtime et de l'API de plugin supportée.
- Retour de validation : La validation du contrat de manifeste et de package échoue rapidement sur les métadonnées mal formées ou incohérentes.

## Archive Freshness

- gitcrawl: `gitcrawl doctor --json` succeeded with `last_sync_at` `2026-05-28T19:09:52.784704Z`, `thread_count` `29810`, `open_thread_count` `11181`, and db path `/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`.
- discrawl: `discrawl status --json` succeeded with `generated_at` `2026-05-30T00:38:20Z`, state `current`, summary `1487536 messages across 25831 channels`, and `last_sync_at` `2026-05-29T19:27:40Z`.

## Coverage Score

- Score: `Beta (77%)`
- Positive signals:
  - The release-check flow creates a packed external TypeScript consumer and verifies representative public SDK imports from the packed package: `openclaw/plugin-sdk`, `channel-entry-contract`, `config-contracts`, `provider-entry`, and `runtime-env` (`/Users/kevinlin/code/openclaw/scripts/release-check.ts:563`, `/Users/kevinlin/code/openclaw/scripts/release-check.ts:609`, `/Users/kevinlin/code/openclaw/scripts/fixtures/packed-plugin-sdk-type-smoke.ts:1`).
  - Release checks validate built `dist/plugin-sdk` exports, enforce size checks on critical entrypoints, and execute a real import smoke for `openclaw/plugin-sdk/core` from the built package (`/Users/kevinlin/code/openclaw/scripts/release-check.ts:1045`, `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1096`, `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1120`).
  - The Windows cross-OS release-check lane runs an installed-package runtime probe that imports `openclaw/plugin-sdk/plugin-runtime` and exercises start/stop behavior against the installed artifact (`/Users/kevinlin/code/openclaw/scripts/openclaw-cross-os-release-checks.ts:2778`, `/Users/kevinlin/code/openclaw/scripts/openclaw-cross-os-release-checks.ts:2847`, `/Users/kevinlin/code/openclaw/scripts/openclaw-cross-os-release-checks.ts:2860`).
  - Packaging proof is stronger than the authoring import surface: release checks perform a real `npm pack`, install the packed tarball into an isolated prefix, verify the packed package surface, run packaged CLI smoke, run bundled-plugin postinstall, run `openclaw plugins doctor`, and run packed bundled-plugin activation smoke before release (`/Users/kevinlin/code/openclaw/scripts/release-check.ts:680`, `/Users/kevinlin/code/openclaw/scripts/release-check.ts:700`, `/Users/kevinlin/code/openclaw/scripts/release-check.ts:781`).
  - Package-contract tests prove compatible npm fallback behavior, staged manifest and package metadata overlays, ClawHub package-contract rejection for missing `openclaw.compat.pluginApi`, and packed release artifact integrity (`/Users/kevinlin/code/openclaw/src/plugins/install.npm-spec.e2e.test.ts:305`, `/Users/kevinlin/code/openclaw/test/plugin-npm-package-manifest.test.ts:177`, `/Users/kevinlin/code/openclaw/test/plugin-clawhub-release.test.ts:58`, `/Users/kevinlin/code/openclaw/test/release-check.test.ts:635`).
- Negative signals:
  - The installed-package import smoke is still narrow. `CRITICAL_PLUGIN_SDK_IMPORT_SMOKE_SPECIFIERS` currently contains only `openclaw/plugin-sdk/core`, so the release path does not import the full public subpath set from a packed install (`/Users/kevinlin/code/openclaw/scripts/release-check.ts:148`, `/Users/kevinlin/code/openclaw/scripts/release-check.ts:153`).
  - I did not find a recurring packed-install sweep that imports every generated public SDK subpath and validates its paired `types` and runtime entry against the published export map.
  - The strongest package-contract proof is still local npm install and packed release validation; I did not find equivalent recurring proof for a full ClawHub publish-install-upgrade roundtrip across multiple host/plugin compatibility floors.
  - Post-upgrade compatibility diagnostics for manifest drift and skipped or incompatible installs are still tracked in open work rather than already settled into the mainline operator workflow.
  - Taxonomy-owned surface validation commands were attempted for this surface but blocked locally before real validation because dependency installation failed with 403 registry auth errors for `@microsoft/teams.cards` and `@microsoft/teams.api` with `No authorization header was set for the request`. Per the scoring policy, that is a local validation blocker rather than product evidence.
  - Archive evidence still shows user-visible regressions and active fixes around stale or missing subpath exports, which indicates the current integration net does not yet fully cover upgrade and compatibility paths.
- Integration gaps:
  - Add a packed-install sweep that imports every generated public SDK subpath and validates both runtime and `types` targets before publish.
  - Add recurring external-plugin upgrade smokes for deprecated, compatibility, and owner-gated subpaths, especially Codex-related compatibility paths.
  - Add recurring ClawHub publish/install compatibility coverage that proves package metadata through publish, discovery, selection, and install.
  - Land post-upgrade contract diagnostics so manifest drift, skipped plugins, and incompatible API floors have settled runtime/operator evidence outside open PRs.
  - Add broader cross-OS installed-package coverage for scoped alias resolution instead of relying on a small representative set.

Coverage labels:

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

At shared boundaries, choose the higher maturity label.

Coverage measures integration, e2e, live, or real runtime-flow evidence across
the category. Unit tests can provide supporting context but never make a feature covered by
themselves.

## Score de Qualité

- Score : `Beta (74%)`
- Rapports Gitcrawl :
  - `gitcrawl threads openclaw/openclaw --numbers 80219 --include-closed --json` montre un problème d'architecture de surface entière documentant la dérive de publication par liste, l'expansion des exports, et l'absence d'un modèle de support unique et faisant autorité pour la surface SDK publique.
  - `gitcrawl threads openclaw/openclaw --numbers 86087,81213 --include-closed --json` montre des régressions bêta ouvertes où la gestion de `openclaw/plugin-sdk/codex-native-task-runtime` crée toujours des défaillances visibles par l'utilisateur ou un comportement d'export confus lors des exécutions soutenues par Codex.
  - `gitcrawl threads openclaw/openclaw --numbers 86130,87119 --include-closed --json` montre des correctifs ouverts pour restaurer les exports de compatibilité et empêcher la résolution de sous-chemin délimité de tomber dans `root-alias.cjs`, ce qui signifie que cette catégorie se durcit toujours activement contre les bugs de correction et de mise à niveau.
- Rapports Discrawl :
  - `discrawl --json search "plugin sdk subpath" --limit 10` a retourné des résultats de canal de mainteneur et d'archive GitHub en miroir qui renforcent les problèmes récurrents de sous-chemin SDK : utilisation d'assistant public dépréciée signalée sur la PR `#80967`, un hook de chargeur réservé aux tests fuyant dans le SDK public sur la PR `#77205`, et les attentes des plugins externes autour des assistants SDK racine manquants sur le problème `#68279`.
  - Les résultats discrawl sont mitigés plutôt que catastrophiques : ils montrent un examen et une correction actifs du mainteneur, mais ils montrent également la même catégorie générant des conversations de support et de compatibilité répétées.
- Bonnes qualités :
  - La documentation est claire sur les imports de sous-chemin étroit, en évitant les coutures de commodité de marque fournisseur ou canal pour le nouveau code, et en traitant les coutures d'assistant fourni réservé comme des API non générales (`/Users/kevinlin/code/openclaw/docs/plugins/sdk-overview.md:26`, `/Users/kevinlin/code/openclaw/docs/plugins/sdk-overview.md:49`, `/Users/kevinlin/code/openclaw/docs/plugins/sdk-subpaths.md:9`, `/Users/kevinlin/code/openclaw/docs/plugins/sdk-subpaths.md:50`).
  - La source a un pipeline d'inventaire vers export déterministe, avec des constantes de classification partagées pour les coutures fournies réservées, les façades fournies soutenues, et les points d'entrée possédés par le plugin public (`/Users/kevinlin/code/openclaw/scripts/lib/plugin-sdk-entries.mjs:20`, `/Users/kevinlin/code/openclaw/src/plugin-sdk/entrypoints.ts:36`, `/Users/kevinlin/code/openclaw/src/plugin-sdk/entrypoints.ts:42`, `/Users/kevinlin/code/openclaw/src/plugin-sdk/entrypoints.ts:56`).
  - L'aliasing du chargeur est prudent : il valide les racines de package de confiance, restreint la syntaxe de sous-chemin, et contrôle les coutures réservées au propriétaire uniquement avant de publier les cartes d'alias délimitées (`/Users/kevinlin/code/openclaw/src/plugins/sdk-alias.ts:58`, `/Users/kevinlin/code/openclaw/src/plugins/sdk-alias.ts:70`, `/Users/kevinlin/code/openclaw/src/plugins/sdk-alias.ts:387`, `/Users/kevinlin/code/openclaw/src/plugins/sdk-alias.ts:752`).
  - La surface SDK racine est intentionnellement minuscule plutôt qu'un baril fourre-tout, ce qui réduit la dérive accidentelle de surface racine (`/Users/kevinlin/code/openclaw/src/plugin-sdk/index.ts:1`).
  - Des outils de gouvernance existent pour la synchronisation des exports, la détection de dérive de ligne de base API, la budgétisation de surface, et la création de rapports de limite (`/Users/kevinlin/code/openclaw/package.json:1560`, `/Users/kevinlin/code/openclaw/package.json:1562`, `/Users/kevinlin/code/openclaw/package.json:1564`, `/Users/kevinlin/code/openclaw/package.json:1568`, `/Users/kevinlin/code/openclaw/scripts/generate-plugin-sdk-api-baseline.ts:16`, `/Users/kevinlin/code/openclaw/scripts/check-plugin-sdk-subpath-exports.mjs:17`, `/Users/kevinlin/code/openclaw/scripts/plugin-sdk-surface-report.mjs:23`).
  - La documentation du manifeste sépare clairement les métadonnées natives `openclaw.plugin.json` des métadonnées de package, et le code de contrat de package normalise les champs de compatibilité dans un petit package isolé (`/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:9`, `/Users/kevinlin/code/openclaw/docs/plugins/building-plugins.md:61`, `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:20`, `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:46`).
  - Le code au moment de l'installation échoue fermé pour `openclaw.compat.pluginApi` mal formé, `openclaw.install.minHostVersion` invalide, plages d'API de plugin incompatibles, et `openclaw.plugin.json` manquant (`/Users/kevinlin/code/openclaw/src/plugins/package-compat.ts:7`, `/Users/kevinlin/code/openclaw/src/plugins/install.ts:145`, `/Users/kevinlin/code/openclaw/src/plugins/install.ts:170`, `/Users/kevinlin/code/openclaw/src/plugins/install.ts:1560`).
- Mauvaises qualités :
  - La gouvernance de surface entière est toujours fragmentée entre l'inventaire des points d'entrée, les exports de package, le catalogue de documentation, la ligne de base API, et les rapports de limite au lieu d'un manifeste unique faisant autorité sur le statut de support, ce qui est la préoccupation ouverte centrale dans `#80219`.
  - La gestion de la compatibilité est toujours assez fragile pour générer des régressions bêta ouvertes et des PR de correctif actifs autour de sous-chemins supprimés ou obsolètes, en particulier dans les flux liés à Codex.
  - La catégorie publique est toujours grande et lourde de classification, avec des coutures d'assistant réservées, des surfaces possédées par le plugin, des sous-chemins publics dépréciés, et des barils de réexport avec caractères génériques nécessitant tous une curation continue (`/Users/kevinlin/code/openclaw/scripts/plugin-sdk-surface-report.mjs:23`, `/Users/kevinlin/code/openclaw/scripts/plugin-sdk-surface-report.mjs:177`, `/Users/kevinlin/code/openclaw/scripts/plugin-sdk-surface-report.mjs:207`).
  - L'utilisation de contrat hérité ou invalide peut toujours se dégrader en débogage d'opérateur confus plutôt qu'une remédiation nette, et la dérive de contrat post-mise à niveau est toujours en cours de formalisation dans le travail de compatibilité de plugin ouvert.
  - L'exécution locale fraîche des commandes de validation détenues par la taxonomie a été bloquée dans cette exécution, donc je n'ai pas de sortie de commande actuelle prouvant que la synchronisation des exports, la dérive de ligne de base, les budgets de surface, ou les portes de rapport de limite sont tous verts aujourd'hui.
- Exclus de la qualité :
  - Je n'ai pas augmenté ou diminué la Qualité en raison de la couverture des tests unitaires, d'intégration, e2e, en direct, ou d'exécution.
  - Je n'ai pas traité l'échec de dépendance locale/authentification sur la configuration de la commande de validation comme preuve de qualité du produit.

Étiquettes de qualité :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, en direct, ou d'exécution réelle comme entrée de notation.

## Lacunes Connues

- La catégorie manque toujours d'un manifeste unique faisant autorité sur le statut de support qui pilote les exports, la documentation, les lignes de base, la politique de compatibilité, et la classification des propriétaires à partir d'une source unique de vérité.
- Il n'y a pas de preuve d'installation compactée fraîche dans cette exécution que chaque sous-chemin SDK public se résout correctement à partir de la surface de package expédiée.
- Les preuves d'archive ouvertes montrent toujours des bugs de compatibilité sensibles à la mise à niveau autour de sous-chemins SDK obsolètes ou supprimés.
- Les migrations de contrat de plugin hérité et la dérive de manifeste post-mise à niveau peuvent toujours produire des diagnostics d'opérateur confus.
- ClawHub et npm partagent le même contrat de métadonnées de package, mais la preuve de bout en bout récurrente est plus forte sur les chemins npm et de version compactée que sur un chemin de publication/installation/mise à niveau ClawHub complet.
- Les commandes de validation détenues par la taxonomie pour cette surface ont été bloquées localement par des échecs d'authentification du registre de dépendances, donc une passe de validation exécutée par un mainteneur est toujours nécessaire pour la confirmation au niveau de la commande actuelle.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-overview.md:26` documente la convention d'importation de sous-chemin étroit et décourage l'utilisation large du SDK racine pour le code nouveau ordinaire.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-overview.md:75` lie la catégorie publique directement à `plugin-sdk-entrypoints.json`, la liste de filtrage locale uniquement, et `pnpm plugin-sdk:surface`.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-subpaths.md:9` explique que la catégorie publique est le sous-ensemble public généré de l'inventaire des points d'entrée et appelle les coutures d'aide groupées réservées plus les aides de test locales uniquement.
- `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:28` exige que chaque plugin natif expédie `openclaw.plugin.json`, et `/Users/kevinlin/code/openclaw/docs/plugins/manifest.md:39` indique qu'OpenClaw lit le manifeste avant de charger le code du plugin.
- `/Users/kevinlin/code/openclaw/docs/plugins/building-plugins.md:61` affiche les métadonnées de package externe avec `openclaw.compat.pluginApi`, la compatibilité de passerelle, et les champs `openclaw.build.*`.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference.md:11` indique que la référence de plugin générée est dérivée des métadonnées `package.json` et `openclaw.plugin.json` d'extension.

## Source

- `/Users/kevinlin/code/openclaw/scripts/lib/plugin-sdk-entries.mjs:20` construit l'ensemble de point d'entrée public et d'exportation de package en soustrayant les sous-chemins locaux uniquement de l'inventaire des points d'entrée.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/entrypoints.ts:36` classe les coutures groupées réservées, les façades groupées supportées, et les surfaces appartenant au plugin public dans un miroir TypeScript de l'inventaire.
- `/Users/kevinlin/code/openclaw/package.json:146` déclare les exportations `./plugin-sdk` et `./plugin-sdk/<subpath>` expédiées, tandis que `/Users/kevinlin/code/openclaw/package.json:1560` expose les scripts de gouvernance pour les vérifications d'API, d'exportation, de surface et de limite.
- `/Users/kevinlin/code/openclaw/src/plugins/sdk-alias.ts:62` et `/Users/kevinlin/code/openclaw/src/plugins/sdk-alias.ts:752` montrent comment le chargeur dérive les sous-chemins exportés des racines de package de confiance et des chemins privés contrôlés par propriétaire.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/index.ts:1` maintient la surface racine intentionnellement étroite au lieu d'agir comme un baril public large.
- `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:20` définit les chemins de champs de package externe requis, tandis que `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:46` normalise les métadonnées de compatibilité.
- `/Users/kevinlin/code/openclaw/src/plugins/install.ts:145` valide la compatibilité de l'API du plugin de package, `/Users/kevinlin/code/openclaw/src/plugins/install.ts:170` valide `openclaw.install.minHostVersion`, et `/Users/kevinlin/code/openclaw/src/plugins/install.ts:1560` rejette les packages manquant un `openclaw.plugin.json` valide.
- `/Users/kevinlin/code/openclaw/scripts/lib/plugin-npm-package-manifest.mjs:408` augmente le `package.json` du plugin emballé avec les métadonnées d'exécution, et `/Users/kevinlin/code/openclaw/scripts/lib/plugin-npm-package-manifest.mjs:564` augmente les manifestes emballés avec les métadonnées de configuration de canal générées.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/release-check.ts:563` crée le projet consommateur TypeScript emballé pour les importations SDK publiques représentatives.
- `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1045` valide les exportations `dist/plugin-sdk` construites et `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1120` exécute le test de fumée d'importation de package installé critique.
- `/Users/kevinlin/code/openclaw/scripts/openclaw-cross-os-release-checks.ts:2778` ajoute une sonde d'exécution de package installé Windows pour `openclaw/plugin-sdk/plugin-runtime`.
- `/Users/kevinlin/code/openclaw/src/plugins/install.npm-spec.e2e.test.ts:305` installe le package stable compatible le plus récent lorsque le registre `latest` nécessite une API de plugin plus récente.
- `/Users/kevinlin/code/openclaw/test/plugin-npm-package-manifest.test.ts:177` superpose les métadonnées de configuration de canal générées dans `openclaw.plugin.json` lors de l'emballage, et `/Users/kevinlin/code/openclaw/test/plugin-npm-package-manifest.test.ts:523` refuse d'emballer les plugins publiables avant que les fichiers d'exécution locaux au package existent.
- `/Users/kevinlin/code/openclaw/test/release-check.test.ts:635` exige les manifestes groupés, les métadonnées de package groupées, les catalogues générés, et les artefacts du SDK de plugin dans le package emballé.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-sdk-subpaths.test.ts:17` importe les sous-chemins SDK publics de la surface du package et `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-sdk-subpaths.test.ts:844` vérifie que les shims dépréciés restent isolés derrière les coutures de compatibilité.
- `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-sdk-package-contract-guardrails.test.ts:24` ancre les fichiers de docs et de référence de contrat, et `/Users/kevinlin/code/openclaw/src/plugins/contracts/plugin-sdk-package-contract-guardrails.test.ts:849` assure que les sous-chemins publics référencés existent à la fois dans l'inventaire des points d'entrée et les exportations `package.json`.
- `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.test.ts:10` vérifie la normalisation de compatibilité, et `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.test.ts:53` vérifie les diagnostiques de chemin de champ requis stables.
- `/Users/kevinlin/code/openclaw/src/plugins/install.test.ts:744` rejette les archives zip de plugin natif sans `openclaw.plugin.json`, tandis que `/Users/kevinlin/code/openclaw/src/plugins/install.test.ts:3621` et `/Users/kevinlin/code/openclaw/src/plugins/install.test.ts:3644` rejettent les métadonnées de compatibilité de package incompatibles ou mal formées.

## Commandes de validation de surface

- `pnpm plugin-sdk:check-exports`: `bloqué` - vérifierait que les exportations SDK publiques générées correspondent toujours à l'inventaire des points d'entrée enregistré; tenté depuis `/Users/kevinlin/code/openclaw`, mais l'installation des dépendances a d'abord échoué avec des erreurs d'authentification de registre 403 pour `@microsoft/teams.cards` et `@microsoft/teams.api` plus `No authorization header was set for the request`.
- `pnpm plugin-sdk:api:check`: `bloqué` - détecterait la dérive d'API publique dans la surface SDK emballée; bloqué par le même échec de dépendance/authentification locale avant que la validation réelle ne s'exécute.
- `pnpm plugin-sdk:surface:check`: `bloqué` - appliquerait les budgets de taille de surface publique et d'exportation dépréciée pour cette catégorie; bloqué par le même échec de dépendance/authentification locale avant que la validation réelle ne s'exécute.
- `pnpm plugins:boundary-report:ci`: `bloqué` - échouerait sur les importations réservées entre propriétaires, les sous-chemins réservés inutilisés, et en raison de la dette de compatibilité pour cette catégorie; bloqué par le même échec de dépendance/authentification locale avant que la validation réelle ne s'exécute.
- `pnpm release:plugins:npm:check`: `bloqué` - validerait les métadonnées npm du plugin publiable et la préparation à la publication autour de cette catégorie; bloqué par le même échec de dépendance/authentification locale avant que la validation réelle ne s'exécute.
- `pnpm release:plugins:clawhub:check`: `bloqué` - validerait les métadonnées ClawHub du plugin publiable et la préparation à la publication autour de cette catégorie; bloqué par le même échec de dépendance/authentification locale avant que la validation réelle ne s'exécute.

## Requêtes Gitcrawl

Requête:

- `gitcrawl threads openclaw/openclaw --numbers 80219 --include-closed --json`

Résultats:

- Le problème ouvert `#80219` est un audit d'architecture de surface entière qui appelle explicitement la dérive de publication par liste, l'expansion d'exportation, et l'absence d'un modèle de support public unique et autoritaire pour la catégorie SDK.

Requête:

- `gitcrawl threads openclaw/openclaw --numbers 86087,81213 --include-closed --json`

Résultats:

- Le problème ouvert `#86087` documente une régression bêta Windows visible par l'utilisateur où `@openclaw/codex` importe toujours `openclaw/plugin-sdk/codex-native-task-runtime` et rencontre `ERR_PACKAGE_PATH_NOT_EXPORTED`.
- Le problème ouvert `#81213` montre que la même couture de compatibilité reste confuse même lorsque le chemin du chargeur s'améliore: l'exécution réelle ne plante plus immédiatement, mais le sondage simple d'exportation de package n'expose toujours pas le sous-chemin.

Requête:

- `gitcrawl threads openclaw/openclaw --numbers 86130,87119 --include-closed --json`

Résultats:

- La PR ouverte `#86130` propose de restaurer le sous-chemin d'exécution de tâche Codex comme exportation de compatibilité uniquement pour les installations obsolètes.
- La PR ouverte `#87119` propose de corriger la résolution d'alias de sous-chemin étendu afin que les cartes d'exportation obsolètes ne tombent pas dans `root-alias.cjs/<subpath>`.

Requête:

- `gitcrawl search openclaw/openclaw --query "openclaw.compat.pluginApi openclaw.install.minHostVersion" --json`

Résultats:

- A retourné la PR ouverte `#87477`, `fix(plugins): reject incompatible package plugin API installs`.
- L'extrait lie le travail actuel directement à `openclaw.compat.pluginApi` comme contrat de compatibilité d'installation et à `openclaw.install.minHostVersion` comme vérification de plancher d'hôte séparée.

Requête:

- `gitcrawl search openclaw/openclaw --query "silent failures legacy invalid plugin contracts" --json`

Résultats:

- A retourné le problème ouvert `#78301`, `Plugin loader: silent failures on legacy/invalid plugin contracts cost hours of debugging`.

Requête:

- `gitcrawl search openclaw/openclaw --query "post-upgrade plugin compat manifest drift" --json`

Résultats:

- A retourné la PR ouverte `#79260`, `feat(doctor): add --post-upgrade --json mode for plugin-compat findings`.

Requête:

- `gitcrawl search openclaw/openclaw --query "plugin sdk export sprawl lifecycle semantics" --json`

Résultats:

- A retourné le problème ouvert `#80219`, `[plugin sdk] Consolidate author surface, lifecycle semantics, and export sprawl`.

## Requêtes Discrawl

Requête:

- `discrawl --json search "plugin sdk subpath" --limit 10`

Résultats:

- La requête a retourné les accès de canal de mainteneur et d'archive GitHub en miroir montrant une pression de catégorie récurrente: la PR `#80967` a été appelée pour l'utilisation d'aide publique dépréciée, la PR `#77205` pour un crochet de chargeur de test uniquement fuyant dans le SDK public, et le problème `#68279` pour les aides manquantes sur l'importation SDK racine nu attendue par les plugins externes.

Requête:

- `discrawl --json search "ClawHub publish openclaw.compat.pluginApi" --limit 5`

Résultats:

- A retourné les messages d'archive Discord liés au projet sur le problème `#56903`, le problème ClawHub `#1796`, et la PR ClawHub `#1802`.
- L'enregistrement d'archive montre une lacune réelle dans les docs autour des métadonnées de package requises, puis un message de fermeture ultérieur disant que `main` actuel rend maintenant le contrat de plugin de code externe explicite. J'ai traité cela comme une preuve positive que l'inadéquation docs/source a été réparée.

Requête:

- `discrawl --json search "contracts.tools openclaw.plugin.json" --limit 5`

Résultats:

- A retourné la discussion d'opérateur montrant un plugin installé enregistrant toujours des outils sans déclarer `contracts.tools`, produisant l'avertissement d'exécution `plugin must declare contracts.tools before registering agent tools`.
- J'ai traité cela comme une preuve réelle de confusion persistante de migration de contrat/opérateur, pas comme un signal de couverture.
