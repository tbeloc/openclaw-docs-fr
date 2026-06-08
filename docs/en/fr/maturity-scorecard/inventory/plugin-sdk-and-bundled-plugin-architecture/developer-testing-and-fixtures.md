---
title: Plugins - Testing Plugins Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Plugins - Testing Plugins Maturity Note

## Summary

Cette catégorie est solide pour les auteurs de plugins regroupés dans le dépôt. OpenClaw documente
les sous-chemins d'aide au test ciblés, maintient la source d'aide organisée par rôle de test,
et exécute les flux réels du cycle de vie des plugins, installation, mise à jour, désinstallation
et flux de plugins en direct sur une infrastructure de fixtures partagée. La couverture est donc
Stable : le dépôt dispose de preuves réelles de flux d'exécution montrant que la fixture et les
outils de test pour développeurs supportent l'architecture de plugins qu'ils sont censés exercer.

La principale limite de maturité est la clarté du contrat à la limite du package. La documentation
indique que ces aides sont locales au dépôt et non des exports de packages tiers, le package
`openclaw` racine exclut les fichiers dist d'aide, mais le package workspace privé
`@openclaw/plugin-sdk` exporte toujours le barrel `./testing` déprécié. Cette histoire mixte,
plus le problème ouvert d'expansion de surface SDK, maintient la Qualité à un niveau Stable bas
plutôt qu'Adorable.

## Category Scope

Cette catégorie couvre les utilitaires de test orientés développeur, les constructeurs de fixtures,
la configuration de test scoped, et la preuve de flux d'exécution réel pour les workflows de test
et de fixture de plugins dans la surface Plugins. Elle inclut `docs/plugins/sdk-testing.md`,
`docs/plugins/sdk-subpaths.md`, `src/plugin-sdk/test-fixtures.ts`, `src/plugin-sdk/test-env.ts`,
`src/plugin-sdk/plugin-test-runtime.ts`, `src/plugin-sdk/channel-test-helpers.ts`, le barrel
de compatibilité déprécié `src/plugin-sdk/testing.ts`, l'export workspace privé
`packages/plugin-sdk/src/testing.ts`, les aides de fixture sous `test/helpers`, la configuration
Vitest scoped sous `test/vitest`, et les flux E2E Docker de cycle de vie et de fixtures sous
`scripts/e2e`.

Elle exclut l'évaluation du comportement métier des plugins regroupés individuels sauf lorsque
ces plugins sont utilisés comme sujets de fixture pour les flux d'installation, de cycle de vie
ou de smoke d'exécution. Elle exclut également le support de packages publics tiers pour les
sous-chemins d'aide ciblés car `docs/plugins/sdk-testing.md` les marque explicitement comme
des points d'entrée source locaux au dépôt et le package `openclaw` racine exclut leurs artefacts dist.

## Features

- Test fixtures : Les fixtures fournissent des métadonnées de plugins réutilisables et des entrées de test d'exécution.
- Environnement de test local : Les auteurs de plugins peuvent configurer l'environnement de test local et la configuration d'aide scoped pour les tests de plugins.
- Plugin runtime harness : Les harnais de test de plugins couvrent les chemins d'intégration d'authoring et d'exécution.
- Scaffolds unitaires et d'intégration : Les aides de test scoped et la configuration supportent les tests unitaires et d'intégration pour les surfaces de plugins.
- Suites de cycle de vie Docker : Les scripts de bout en bout basés sur Docker valident les flux de cycle de vie des plugins packagés.
- Tests de smoke : Les tests de smoke locaux et packagés détectent les installations cassées avant la release.

## Archive Freshness

- gitcrawl : snapshot d'archive de surface de plugin partagée depuis `gitcrawl doctor --json`
  réussi avec `last_sync_at` `2026-05-28T19:09:52.784704Z`,
  `thread_count` `29810`, `open_thread_count` `11181`, et `db_path`
  `/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`.
- discrawl : snapshot d'archive de surface de plugin partagée depuis `discrawl status --json`
  réussi avec `generated_at` `2026-05-30T00:38:20Z`, `state` `current`,
  `summary` `1487536 messages across 25831 channels`, et `last_sync_at`
  `2026-05-29T19:27:40Z`.

## Coverage Score

- Score : `Stable (84%)`
- Signaux positifs :
  - `scripts/e2e/plugins-docker.sh` et `scripts/e2e/lib/plugins/sweep.sh` exécutent
    les flux réels d'installation, inspection, mise à jour et désinstallation de plugins
    sur les cas de fixture tgz, répertoire local, `file:`, registre npm, git, marketplace,
    et ClawHub.
  - `scripts/e2e/lib/plugins/fixtures.sh` centralise la création de plugins de fixture,
    l'empaquetage de tarball, la configuration de registre temporaire, l'enregistrement de confiance
    et le nettoyage, de sorte que les E2Es majeurs du cycle de vie des plugins partagent un substrat
    de fixture maintenu.
  - `scripts/e2e/bundled-plugin-install-uninstall-docker.sh` et
    `scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh` installent les plugins regroupés,
    exécutent optionnellement les vérifications de smoke d'exécution, les désinstallent et affirment
    la suppression.
  - `scripts/e2e/plugin-lifecycle-matrix-docker.sh` et
    `scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh` couvrent les phases d'installation, inspection,
    désactivation, activation, mise à niveau, rétrogradation et désinstallation de code manquant
    avec les points d'entrée OpenClaw packagés.
  - `scripts/e2e/codex-npm-plugin-live-docker.sh` exécute un flux en direct OpenClaw + Codex plugin
    packagé qui installe et active le plugin, vérifie l'état du plugin, effectue un tour d'agent
    et valide le comportement de désinstallation.
- Signaux négatifs :
  - La preuve d'exécution la plus forte est le comportement E2E du cycle de vie complet du plugin
    et piloté par fixtures, pas une preuve dédiée à la limite du package pour chaque famille d'aide
    de test ciblée.
  - `docs/plugins/sdk-testing.md` dit explicitement que les sous-chemins d'aide de test ciblés
    sont des points d'entrée source locaux au dépôt pour les tests de plugins regroupés plutôt que
    des exports de packages tiers, donc cette catégorie ne montre pas encore de preuve large de
    consommateurs externes.
  - Le package `openclaw` racine exclut `dist/plugin-sdk/test-env.js`,
    `dist/plugin-sdk/test-fixtures.js`, `dist/plugin-sdk/plugin-test-runtime.js`,
    `dist/plugin-sdk/channel-test-helpers.js`, et `dist/plugin-sdk/testing.js`,
    ce qui signifie que la couverture de la catégorie est intentionnellement concentrée sur les
    flux de développeur dans le dépôt.
- Lacunes d'intégration :
  - Ajouter un smoke récurrent qui exerce les familles d'aide ciblées représentatives
    via les points d'entrée locaux au dépôt prévus de sorte que la dérive de la table d'aide
    soit détectée par la preuve d'exécution, pas seulement par les tests unitaires et les E2Es
    de plugins volumineux.
  - Ajouter une validation générée ou un smoke d'exemple pour `docs/plugins/sdk-testing.md`
    de sorte que les imports d'aide documentés et les snippets d'exemple ne puissent pas dériver
    silencieusement de la source.
  - Décider si l'export privé déprécié `@openclaw/plugin-sdk/testing` doit rester existant
    comme une couture de compatibilité supportée ou être complètement clôturé de la nouvelle
    utilisation de test pour développeurs.

Étiquettes de couverture :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, live, ou la preuve de flux d'exécution réel dans
la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
une fonctionnalité couverte par eux-mêmes.

## Quality Score

- Score : `Stable (81%)`
- Rapports Gitcrawl :
  - La requête `gitcrawl search openclaw/openclaw --query "plugin sdk testing harness fixture" --json`
    a retourné 4 résultats de mots-clés. Le signal de catégorie pertinent était le problème ouvert
    `#80219`, `[plugin sdk] Consolidate author surface, lifecycle semantics, and export sprawl`,
    dont le corps compte explicitement `23` familles de test-ish et de contrat ou mock et recommande
    de geler ou de désemphasiser les surfaces de compatibilité larges telles que `testing`.
  - La requête `gitcrawl search openclaw/openclaw --query "plugin sdk e2e docker fixture" --json`
    a retourné 1 résultat de mot-clé : PR ouvert `#87141`,
    `fix(plugin): harden schema and metadata fuzz boundaries`. C'est un signal de durcissement
    pour le comportement de test et de fixture adjacent au plugin-SDK, pas une preuve d'instabilité
    large de test pour développeurs.
  - La requête `gitcrawl threads openclaw/openclaw --numbers 80219,87141 --include-closed --json`
    a confirmé que `#80219` est toujours ouvert comme un élément de dette d'architecture de surface
    entière et `#87141` est un changement de durcissement actif avec couverture de test adjacent
    au plugin-SDK ajoutée.
- Rapports Discrawl :
  - La requête `discrawl --json search "plugin sdk testing harness fixture" --limit 5`
    a retourné `null`.
  - La requête `discrawl --json search "plugin sdk testing" --limit 5` a retourné 5
    résultats larges. Le seul résultat légèrement pertinent était un message de statut de mainteneur
    du 2026-05-16 mentionnant le travail de test RTT plus les problèmes ou PRs continus du plugin SDK,
    de la mise à niveau et de npm ; il ne décrivait pas un défaut direct dans la surface d'aide ou
    de fixture. Je traite donc la preuve Discrawl actuelle comme neutre.
- Bonnes qualités :
  - `docs/plugins/sdk-testing.md` est explicite sur l'utilisation prévue : imports d'aide ciblés
    pour les nouveaux tests de plugins regroupés, statut local au dépôt uniquement pour ces aides,
    et dépréciation du barrel large `plugin-sdk/testing`.
  - La source d'aide est organisée par rôle plutôt que comme un sac d'utilitaire opaque :
    `test-fixtures`, `test-env`, `plugin-test-runtime`, et `channel-test-helpers` ont chacun
    des responsabilités claires.
  - `test/vitest/vitest.plugin-sdk.config.ts` et `test/vitest/vitest.plugin-sdk-light.config.ts`
    donnent à la catégorie des voies scoped explicites pour le travail complet et léger du Plugin SDK.
  - L'inventaire du package racine et les règles d'exclusion rendent le contrat local au dépôt
    explicite en excluant les fichiers dist d'aide au test de l'inventaire du package `openclaw` principal.
- Mauvaises qualités :
  - `src/plugin-sdk/testing.ts` reste un barrel de compatibilité déprécié très large qui
    réexporte de nombreuses aides non liées, coutures d'exécution et utilitaires de test internes.
  - Le package workspace privé `@openclaw/plugin-sdk` exporte toujours `./testing`, et
    `packages/plugin-sdk/src/testing.ts` réexporte simplement le barrel de compatibilité large.
    Cela maintient le risque de dépendance accidentelle vivant même si la documentation éloigne
    le nouveau code de celui-ci.
  - Le package `openclaw` racine et le package workspace privé racontent des histoires différentes
    sur la disponibilité des aides de test, ce qui rend les attentes de limite de package plus
    difficiles à raisonner.
  - Le problème d'architecture de surface entière ouvert `#80219` renforce que cette catégorie
    se situe toujours à l'intérieur d'un effort plus large d'expansion SDK et de nettoyage de
    dette de compatibilité.
- Exclu de la qualité :
  - Je n'ai pas augmenté ou diminué la Qualité en raison de la couverture de test unitaire,
    d'intégration, e2e, live ou d'exécution réel.
  - Les commandes de validation de surface bloquées ci-dessous sont traitées comme un bloqueur
    d'environnement local, pas comme une preuve de qualité de catégorie.

Étiquettes de qualité :

- `Adorable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Expérimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture de test unitaire, d'intégration, e2e, live ou
d'exécution réel comme entrée de notation.

## Known Gaps

- Aligner l'histoire de limite de package pour les aides de test : soit retirer l'export privé
  `@openclaw/plugin-sdk/testing`, soit documenter exactement qui devrait s'y fier et sous quelles
  garanties de compatibilité.
- Ajouter une validation générée de doc-à-source ou un smoke d'exemple pour `docs/plugins/sdk-testing.md`
  et `docs/plugins/sdk-subpaths.md` de sorte que les conseils d'import d'aide restent synchronisés
  avec la source et les règles de package.
- Ajouter un smoke récurrent étroit local au dépôt pour les familles d'aide de test représentatives
  plutôt que de s'appuyer principalement sur les E2Es de cycle de vie volumineux plus le signal
  de support au niveau unitaire.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-testing.md` documente les
  importations d'aide ciblées, les marque comme locales au dépôt pour les tests
  de plugins groupés, et déprécie le large baril `openclaw/plugin-sdk/testing`
  pour les nouvelles utilisations.
- `/Users/kevinlin/code/openclaw/docs/plugins/sdk-subpaths.md` catalogue les
  sous-chemins d'aide de test et étiquette `plugin-sdk/testing` comme un baril
  de compatibilité déprécié local au dépôt.
- `/Users/kevinlin/code/openclaw/docs/help/testing.md` énumère le cycle de vie
  du plugin Docker pertinent et les voies de test d'installation/mise à jour de
  plugin qui exercent l'infrastructure de fixture partagée.

### Source

- `/Users/kevinlin/code/openclaw/src/plugin-sdk/test-fixtures.ts` regroupe les
  fixtures génériques de capture de runtime CLI, sandbox, chemin de plugin
  groupé, transcription, terminal et cas typés.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/test-env.ts` regroupe
  l'environnement, fetch, serveur HTTP, temp-home, temp-dir, time, et les
  aides d'utilisation de fournisseur.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/plugin-test-runtime.ts` regroupe
  le runtime de plugin, registre, assistant de configuration, et les aides
  d'enregistrement de fournisseur.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/channel-test-helpers.ts` regroupe
  le cycle de vie du canal, répertoire, statut, livraison sortante, et les
  aides de mock runtime.
- `/Users/kevinlin/code/openclaw/src/plugin-sdk/testing.ts` est le large baril
  de compatibilité déprécié qui réexporte toujours de nombreuses coutures
  d'aide non liées.
- `/Users/kevinlin/code/openclaw/packages/plugin-sdk/src/testing.ts` réexporte
  le baril de compatibilité déprécié, et
  `/Users/kevinlin/code/openclaw/packages/plugin-sdk/package.json` exporte
  toujours `./testing`.
- `/Users/kevinlin/code/openclaw/package.json` et
  `/Users/kevinlin/code/openclaw/src/infra/package-dist-inventory.ts` excluent
  les fichiers dist d'aide de test locaux au dépôt de l'inventaire du package
  principal `openclaw`.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/plugins-docker.sh` et
  `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugins/sweep.sh` exercent
  l'installation, l'inspection, la mise à jour, la désinstallation et les
  vérifications de runtime de plugin pilotées par fixture sur plusieurs formes
  de source de plugin.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugins/fixtures.sh`
  centralise l'écriture de fixture, l'empaquetage de tarball, la configuration
  du registre npm factice, l'enregistrement de confiance, et le nettoyage
  utilisés par les flux E2E de plugin.
- `/Users/kevinlin/code/openclaw/scripts/e2e/bundled-plugin-install-uninstall-docker.sh`
  et
  `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh`
  valident l'installation et la désinstallation de plugin groupé plus le smoke
  runtime optionnel.
- `/Users/kevinlin/code/openclaw/scripts/e2e/plugin-lifecycle-matrix-docker.sh`
  et
  `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh`
  valident l'installation, l'inspection, la désactivation, l'activation, la
  mise à niveau, la rétrogradation, et la désinstallation de code manquant pour
  les flux de plugin empaquetés.
- `/Users/kevinlin/code/openclaw/scripts/e2e/codex-npm-plugin-live-docker.sh`
  valide une installation en direct OpenClaw + Codex empaquetée et un flux de
  tour d'agent.
- `/Users/kevinlin/code/openclaw/packages/sdk/src/package.e2e.test.ts` et
  `/Users/kevinlin/code/openclaw/packages/sdk/src/index.e2e.test.ts` fournissent
  une preuve de consommateur empaquetée adjacente pour la surface SDK plus large,
  même si les sous-chemins d'aide de test eux-mêmes sont locaux au dépôt.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/test/vitest/vitest.plugin-sdk.config.ts`
  définit la voie `plugin-sdk` délimitée pour `src/plugin-sdk/**/*.test.ts`.
- `/Users/kevinlin/code/openclaw/test/vitest/vitest.plugin-sdk-light.config.ts`
  définit la voie `plugin-sdk-light` plus légère sans configuration complète du
  runtime OpenClaw.
- `/Users/kevinlin/code/openclaw/test/vitest-scoped-config.test.ts` et
  `/Users/kevinlin/code/openclaw/test/vitest-light-paths.test.ts` valident le
  câblage de la voie Plugin SDK délimitée et le routage des chemins légers.
- `/Users/kevinlin/code/openclaw/test/openclaw-npm-postpublish-verify.test.ts`
  et `/Users/kevinlin/code/openclaw/src/infra/package-dist-inventory.ts`
  valident l'exclusion et les règles d'empaquetage pour les artefacts d'aide de
  test locaux au dépôt.

### Commandes de validation de surface

- `pnpm plugin-sdk:check-exports`: `bloqué` - pertinent car il vérifierait
  l'inventaire d'exportation Plugin SDK enregistré, y compris les coutures de
  compatibilité dépréciées, mais la validation locale n'a jamais atteint les
  vérifications spécifiques aux commandes car l'installation des dépendances a
  échoué avec des erreurs d'authentification de registre 403 pour
  `@microsoft/teams.cards` et `@microsoft/teams.api`, y compris
  `No authorization header was set for the request`.
- `pnpm plugin-sdk:api:check`: `bloqué` - pertinent car il détecterait la
  dérive dans la surface Plugin SDK actuellement exportée, y compris les coutures
  de test héritées, mais la même défaillance d'authentification de dépendance
  locale a bloqué l'exécution avant la validation réelle.
- `pnpm plugin-sdk:surface:check`: `bloqué` - pertinent car il mesurerait la
  croissance de la surface SDK publique et dépréciée, y compris les barils de
  compatibilité, mais la même défaillance d'authentification de dépendance
  locale a bloqué l'exécution avant la validation réelle.
- `pnpm plugins:boundary-report:ci`: `bloqué` - pertinent car il échouerait sur
  les importations réservées entre propriétaires et en raison de la dette de
  compatibilité, ce qui importe pour les larges barils d'aide de test, mais la
  même défaillance d'authentification de dépendance locale a bloqué l'exécution
  avant la validation réelle.
- `pnpm release:plugins:npm:check`: `bloqué` - pertinent car il validerait la
  préparation à la publication npm du plugin et les hypothèses d'empaquetage
  adjacentes aux flux de cycle de vie de plugin pilotés par fixture, mais la
  même défaillance d'authentification de dépendance locale a bloqué l'exécution
  avant la validation réelle.
- `pnpm release:plugins:clawhub:check`: `bloqué` - pertinent car il validerait
  la préparation à la publication ClawHub du plugin pour les flux exercés par
  les tests d'installation et de cycle de vie de plugin basés sur fixture, mais
  la même défaillance d'authentification de dépendance locale a bloqué
  l'exécution avant la validation réelle.

### Requêtes Gitcrawl

Requête: `gitcrawl search openclaw/openclaw --query "plugin sdk testing harness fixture" --json`

Résultats:

- 4 correspondances de mots-clés.
- La correspondance pertinente était le problème ouvert `#80219`, qui appelle
  explicitement la surface de test-ish, contrat, mock, et compatibilité dans le
  Plugin SDK.
- Les autres correspondances étaient des PRs de harnais ou de passerelle/runtime
  adjacentes plutôt que des défauts directs dans cette catégorie.

Requête: `gitcrawl search openclaw/openclaw --query "plugin sdk e2e docker fixture" --json`

Résultats:

- 1 correspondance de mots-clés.
- La correspondance était la PR ouverte `#87141`, un changement de durcissement
  actif pour la gestion des limites de schéma et métadonnées de plugin malformés
  avec des tests adjacents au Plugin SDK.

Requête: `gitcrawl threads openclaw/openclaw --numbers 80219,87141 --include-closed --json`

Résultats:

- `#80219` reste ouvert et recommande de geler ou de dé-emphasiser les surfaces
  de compatibilité larges telles que `testing`.
- `#87141` reste ouvert et documente le durcissement ciblé plus les tests ajoutés
  plutôt qu'une régression de surface de fixture systémique.

### Requêtes Discrawl

Requête: `discrawl --json search "plugin sdk testing harness fixture" --limit 5`

Résultats:

- `null`.
- Avec la fraîcheur actuelle de l'archive enregistrée ci-dessus, je traite cela
  comme neutre plutôt que positif.

Requête: `discrawl --json search "plugin sdk testing" --limit 5`

Résultats:

- 5 correspondances larges.
- La seule correspondance légèrement pertinente était une note de statut du
  responsable du 2026-05-16 disant que l'accent actuel incluait le travail de
  test RTT plus le Plugin SDK, la mise à niveau, et les problèmes ou PRs npm.
- Je n'ai pas trouvé de rapport d'archive direct du responsable ou de
  l'utilisateur décrivant un sous-chemin d'aide cassé ou un flux de travail de
  fixture dans cette catégorie.
