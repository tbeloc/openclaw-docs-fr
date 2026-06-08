---
title: Plugins - Bundled Plugins Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Plugins - Bundled Plugins Maturity Note

## Summary

Cette catégorie reste `Stable` en termes de couverture et de qualité. OpenClaw dispose d'un modèle de découverte clair pour les plugins groupés empaquetés, les superpositions de sources montées en bind, les entrées de checkout de workspace/source uniquement, et la documentation d'inventaire/référence de plugins générée. La preuve de couverture la plus solide reste le balayage d'installation/désinstallation de plugins groupés Docker plus les tests d'intégration Gateway et CLI ciblés qui exercent les chemins de chargement groupés réels.

Les principales raisons pour lesquelles cette catégorie reste en dessous de `Lovable` sont inchangées : le chemin d'inventaire des docs est soutenu par un générateur et des vérifications de dérive plutôt que par une E2E de chemin de publication, et les lignes externes officielles de l'inventaire sont bien modélisées mais pas toutes prouvées par des flux d'installation/runtime récurrents en direct dans cette catégorie.

## Portée de la catégorie

- Cette catégorie couvre la découverte à l'exécution des plugins groupés, l'inventaire `extensions/*` dans les buckets core/external/source-only, la copie des métadonnées de plugins groupés dans les artefacts construits, et l'exposition de l'identité et des métadonnées de manifeste des plugins groupés aux appelants runtime en aval.
- Cette catégorie couvre également les superpositions de sources groupées, les racines groupées empaquetées, les entrées source-checkout-only qui restent visibles en développement local, et la documentation d'inventaire/référence de plugins générée qui décrit ce qui est livré en core par rapport à ce qui s'installe séparément.
- Hors de portée : la maturité des fonctionnalités de tout plugin groupé individuel, le comportement de distribution ClawHub ou npm après qu'un utilisateur choisisse un plugin, et la surface API du Plugin SDK public plus large.

## Fonctionnalités

- Listing des plugins groupés : Les opérateurs et mainteneurs peuvent inspecter l'ensemble des plugins groupés et ses métadonnées publiées.
- Superpositions de sources groupées : Les superpositions de sources fonctionnent pour le développement local et les tests pilotés par repo.
- Plugins groupés empaquetés : Les distributions construites découvrent les plugins groupés à partir de racines empaquetées.
- Inventaire de plugins généré : L'inventaire de plugins généré et la documentation de référence décrivent ce qui est livré en core par rapport à ce qui s'installe séparément.
- IDs de canaux groupés : Les IDs de canaux groupés sont découverts et normalisés à partir des métadonnées de plugins.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `last_sync_at`
  `2026-05-28T19:09:52.784704Z`, `thread_count` `29810`,
  `open_thread_count` `11181`, `db_path`
  `/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`.
- discrawl : `discrawl status --json` a réussi avec `generated_at`
  `2026-05-30T00:38:20Z`, `state` `current`, résumé
  `1487536 messages across 25831 channels`, et `last_sync_at`
  `2026-05-29T19:27:40Z`.

## Score de couverture

- Score : `Stable (86%)`
- Signaux positifs :
  - Le balayage de plugins groupés Docker sélectionne les plugins groupés empaquetés installables à partir de `openclaw plugins list --json`, les installe par ID groupé, affirme l'état d'installation/configuration persistant, exécute optionnellement un smoke runtime, puis désinstalle et vérifie le nettoyage
    (`/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/probe.mjs:54`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/probe.mjs:98`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/probe.mjs:164`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh:21`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh:40`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh:56`).
  - Le smoke runtime prouve que le plugin groupé installé peut survivre au démarrage réel de Gateway et répondre aux sondes runtime de base telles que `/healthz`, `/readyz`,
    `health`, `channels.status`, et `commands.list`
    (`/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:376`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:423`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:612`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:672`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:678`).
  - Le démarrage de Gateway et le chargement CLI ont tous deux des tests d'intégration bundled-browser qui exercent `OPENCLAW_BUNDLED_PLUGINS_DIR` avec un fixture réel et vérifient l'enregistrement groupé à l'exécution
    (`/Users/kevinlin/code/openclaw/src/gateway/server-plugin-bootstrap.browser-plugin.integration.test.ts:22`,
    `/Users/kevinlin/code/openclaw/src/gateway/server-plugin-bootstrap.browser-plugin.integration.test.ts:38`,
    `/Users/kevinlin/code/openclaw/src/plugins/cli.browser-plugin.integration.test.ts:13`,
    `/Users/kevinlin/code/openclaw/src/plugins/cli.browser-plugin.integration.test.ts:29`,
    `/Users/kevinlin/code/openclaw/src/plugins/cli.browser-plugin.integration.test.ts:48`).
  - La génération d'inventaire a un chemin de vérification de dérive/release récurrent via
    `plugins:inventory:check`, `plugins:inventory:gen`, et
    `release-preflight`
    (`/Users/kevinlin/code/openclaw/package.json:1573`,
    `/Users/kevinlin/code/openclaw/package.json:1574`,
    `/Users/kevinlin/code/openclaw/scripts/release-preflight.mjs:22`,
    `/Users/kevinlin/code/openclaw/scripts/release-preflight.mjs:25`,
    `/Users/kevinlin/code/openclaw/scripts/release-preflight.mjs:42`).
- Signaux négatifs :
  - L'inventaire généré et la documentation de référence sont protégés par des vérifications de générateur et de fichiers obsolètes, mais je n'ai pas trouvé d'E2E de publication de docs ou de navigation de docs qui prouve que ces pages générées sont accessibles après la release.
  - Les lignes de packages externes officielles sont présentes dans l'inventaire généré et les preuves du catalogue de canaux, mais la preuve de flux runtime la plus solide dans cette catégorie provient toujours des tests de cycle de vie de plugins groupés empaquetés plutôt que de scénarios d'installation/runtime externes récurrents pour chaque ligne d'inventaire externe officielle.
  - Les commandes de validation de surface détenues par la taxonomie ont toutes été bloquées localement par un échec d'authentification d'installation de dépendance avant la validation réelle, donc elles n'ajoutent pas de nouvelles preuves de couverture pour ce rescore.
- Lacunes d'intégration :
  - Ajouter une E2E de chemin de release qui vérifie les pages d'inventaire/référence générées dans un artefact de docs construit plutôt que seulement la dérive de génération de fichiers.
  - Ajouter un scénario récurrent qui sélectionne une ligne d'inventaire externe officielle, l'installe via la source annoncée, et vérifie que les métadonnées runtime/inventaire s'alignent avec le bucket de distribution revendiqué.
  - Persister un artefact lisible par machine à partir du balayage de plugins groupés afin que les examinateurs de release puissent voir quels IDs groupés ont été sélectionnés, ignorés pour la configuration requise, runtime-smoked, et nettoyés.

Étiquettes de couverture :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, l'e2e, le live, ou les preuves de flux runtime réel dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.

## Score de Qualité

- Score : `Stable (84%)`
- Rapports Gitcrawl :
  - La requête `bundled plugin discovery inventory` a retourné 4 résultats de mots-clés : PR ouverte #84997 ajoutant des entrées d'inventaire NEAR AI Cloud, problème ouvert #72991 concernant les niveaux de découverte de hook adjacents, PR ouverte #83292 ajoutant un plugin de fournisseur groupé, et PR ouverte #87141 renforçant le schéma de plugin et les limites de fuzzing des métadonnées.
  - La requête `plugin inventory bundled ids` a retourné 1 résultat de mot-clé : PR ouverte #87141, qui est une preuve directe que le renforcement des limites de métadonnées et d'inventaire est toujours un travail actif dans cette catégorie.
- Rapports Discrawl :
  - La requête `discrawl --json search "bundled plugin inventory" --limit 5` a été bloquée localement avec `open sync lock: open /Users/kevinlin/Library/Application Support/discrawl/.discrawl-sync.lock: operation not permitted`.
  - J'ai traité cela comme un bloqueur de requête local, pas comme une preuve de produit. La qualité a été évaluée à partir de l'alignement actuel source/docs plus les preuves gitcrawl, tandis que l'instantané de fraîcheur `discrawl status --json` fourni confirme que l'archive est à jour.
- Bonnes qualités :
  - L'implémentation de découverte porte des métadonnées groupées explicites sur chaque candidat, y compris l'origine, les métadonnées du package, l'identité du manifeste, le chemin du manifeste, et les dépendances de plugin groupé requises au lieu de s'appuyer sur une inférence de chemin vague
    (`/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:66`,
    `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:82`).
  - Les portes de sécurité de découverte rejettent ou réparent les états dangereux du système de fichiers, et les superpositions groupées sont surfacées comme des diagnostics au lieu d'un masquage silencieux
    (`/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:149`,
    `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:176`,
    `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:197`,
    `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:1504`,
    `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:1520`).
  - La génération de métadonnées groupées réécrit les entrées source en chemins construits, porte les artefacts de configuration/exécution/surface publique, et maintient la résolution à l'intérieur des racines de plugin groupé
    (`/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.ts:95`,
    `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.ts:112`,
    `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.ts:120`,
    `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.ts:136`).
  - Les scripts de construction copient les manifestes groupés et les métadonnées du package dans dist, fusionnent les configurations de canal générées, et relocalisent/copient les ressources de compétences déclarées afin que les métadonnées expédiées correspondent à la disposition d'exécution
    (`/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:125`,
    `/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:179`,
    `/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:246`,
    `/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:290`,
    `/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:326`).
  - La génération d'inventaire est déterministe à partir des manifestes vérifiés et des exclusions de package racine, et elle échoue fortement sur les ID de plugin manquants, supplémentaires ou dupliqués avant de mettre à jour les docs générées
    (`/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:445`,
    `/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:452`,
    `/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:469`,
    `/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:515`,
    `/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:603`).
  - Les docs destinées aux utilisateurs distinguent clairement les états d'inventaire groupé/core, externe officiel et source-checkout-only, et les docs de canal indiquent systématiquement aux opérateurs quand un canal est expédié en tant que plugin groupé
    (`/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:12`,
    `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:21`,
    `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:35`,
    `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:145`,
    `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:178`,
    `/Users/kevinlin/code/openclaw/docs/channels/index.md:31`,
    `/Users/kevinlin/code/openclaw/docs/channels/msteams.md:10`,
    `/Users/kevinlin/code/openclaw/docs/channels/nostr.md:13`).
- Mauvaises qualités :
  - Cette catégorie dépend toujours de plusieurs surfaces de vérité synchronisées : `extensions/*`, docs d'inventaire/référence générées, copies de métadonnées dist, instantanés de métadonnées d'exécution, et enregistrements d'installation persistants doivent tous rester alignés.
  - La PR ouverte #87141 montre que les limites de fuzzing de schéma et de métadonnées sont toujours activement resserrées, ce qui est un vrai frein à la qualité même si la direction est corrective.
  - La catégorie documente bien les lignes d'inventaire externe officiel, mais elle s'appuie toujours sur les surfaces de distribution/version adjacentes pour une confiance complète de bout en bout dans ces lignes.
- Exclu de la qualité :
  - L'étendue des tests unitaires, d'intégration, Docker E2E et smoke d'exécution n'a pas été utilisée pour augmenter ou diminuer la Qualité.
  - Les commandes de validation locale bloquées ont été traitées comme un échec de condition préalable d'environnement, pas comme un signal de qualité de produit.

Étiquettes de qualité :

- `Lovable` : 95-100
- `Stable` : 80-95
- `Beta` : 70-80
- `Alpha` : 50-70
- `Experimental` : 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture des tests unitaires, d'intégration, e2e, live ou d'exécution réelle comme entrée de notation.

## Lacunes Connues

- Aucune validation de chemin de publication n'a été trouvée qui prouve que la page d'inventaire générée et les pages de référence de plugin générées sont accessibles dans les docs publiées.
- Les lignes d'inventaire externe officiel sont représentées dans les docs et les tests de catalogue, mais cette catégorie manque toujours de preuve d'installation/exécution en direct récurrente sur tout ce bucket.
- Les commandes de validation de surface pour cette réévaluation ont été bloquées localement par des échecs d'authentification de registre avant qu'elles ne puissent valider quoi que ce soit de spécifique à la catégorie.
- La recherche Discrawl pour cette catégorie a été bloquée localement par un problème de permission de verrou de synchronisation, il n'y a donc pas de résultat de requête Discord frais au-delà de l'instantané de fraîcheur d'archive fourni.

## Preuve

### Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:12` à
  `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:47` définissent
  l'inventaire généré source-de-vérité et la sémantique d'installation pour les
  plugins groupés par rapport aux plugins externes.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:145` à
  `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:176` montrent
  le bucket officiel de packages externes, incluant les plugins du canal groupé
  comme `msteams`, `nextcloud-talk`, `nostr`, `qqbot`, `twitch`, `zalo`, et
  `zalouser`.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:178` à
  `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:184` montrent
  le bucket source-checkout-only.
- `/Users/kevinlin/code/openclaw/docs/plugins/reference.md:11` à
  `/Users/kevinlin/code/openclaw/docs/plugins/reference.md:20` montrent le
  contrat d'index de référence généré.
- `/Users/kevinlin/code/openclaw/docs/channels/index.md:31` à
  `/Users/kevinlin/code/openclaw/docs/channels/index.md:54` présentent le
  statut du plugin groupé directement dans le catalogue des canaux.
- `/Users/kevinlin/code/openclaw/docs/channels/msteams.md:10` à
  `/Users/kevinlin/code/openclaw/docs/channels/msteams.md:20`,
  `/Users/kevinlin/code/openclaw/docs/channels/nostr.md:13` à
  `/Users/kevinlin/code/openclaw/docs/channels/nostr.md:22`, et
  `/Users/kevinlin/code/openclaw/docs/channels/nextcloud-talk.md:10` à
  `/Users/kevinlin/code/openclaw/docs/channels/nextcloud-talk.md:22` montrent
  le modèle de guidance d'installation du plugin groupé dans la documentation
  actuelle des canaux.

### Source

- `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:66` à
  `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:88` définissent les
  métadonnées portées sur les candidats de plugins découverts.
- `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:149` à
  `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:223` appliquent les
  vérifications de sécurité des chemins et des permissions pour les candidats
  de découverte.
- `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:1500` à
  `/Users/kevinlin/code/openclaw/src/plugins/discovery.ts:1545` chargent les
  overlays de source groupés, émettent des diagnostics explicites, puis
  scannent les racines groupées empaquetées.
- `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.ts:95`
  à `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.ts:168`
  dérivent les entrées de métadonnées groupées à partir des manifestes, des
  réécritures d'entrées construites, des artefacts de surface publique générés,
  et des configurations de canaux.
- `/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:125`
  à `/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:143`
  et `/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:179`
  à `/Users/kevinlin/code/openclaw/scripts/copy-bundled-plugin-metadata.mjs:326`
  copient les manifestes/métadonnées de packages groupés dans dist et réécrivent
  les chemins de compétences copiés.
- `/Users/kevinlin/code/openclaw/scripts/bundled-plugin-assets.mjs:39` à
  `/Users/kevinlin/code/openclaw/scripts/bundled-plugin-assets.mjs:130`
  résolvent les alias de manifeste/package et exécutent les hooks d'actifs
  appartenant aux plugins.
- `/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:430`
  à `/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:490`
  collectent les entrées de source et rejettent les IDs manquants/supplémentaires/
  dupliqués, tandis que `/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:515`
  à `/Users/kevinlin/code/openclaw/scripts/generate-plugin-inventory-doc.mjs:616`
  rendent et vérifient la dérive des docs d'inventaire/référence générés.
- `/Users/kevinlin/code/openclaw/package.json:1571` à
  `/Users/kevinlin/code/openclaw/package.json:1574`,
  `/Users/kevinlin/code/openclaw/package.json:1611` à
  `/Users/kevinlin/code/openclaw/package.json:1619`, et
  `/Users/kevinlin/code/openclaw/package.json:1642` câblent les commandes de
  cycle de vie des actifs, d'inventaire, de pré-vol de release, et Docker de
  la catégorie.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/src/gateway/server-plugin-bootstrap.browser-plugin.integration.test.ts:22`
  à `/Users/kevinlin/code/openclaw/src/gateway/server-plugin-bootstrap.browser-plugin.integration.test.ts:59`
  chargent une fixture de navigateur groupée dans le démarrage de Gateway et
  vérifient l'enregistrement des méthodes/services.
- `/Users/kevinlin/code/openclaw/src/plugins/cli.browser-plugin.integration.test.ts:13`
  à `/Users/kevinlin/code/openclaw/src/plugins/cli.browser-plugin.integration.test.ts:70`
  vérifient l'enregistrement CLI et l'omission des plugins désactivés pour une
  fixture groupée.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/probe.mjs:54`
  à `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/probe.mjs:118`
  sélectionnent les plugins groupés empaquetés à partir de `plugins list --json`.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/probe.mjs:164`
  à `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/probe.mjs:239`
  affirment l'état installé et désinstallé pour les enregistrements de plugins
  groupés, la configuration, et les répertoires gérés.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:376`
  à `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:446`
  démarrent la Gateway et attendent la disponibilité, tandis que
  `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:612`
  à `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:705`
  sondent la visibilité du canal et des commandes à l'exécution.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh:21`
  à `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh:67`
  exécutent le balayage d'installation/exécution/désinstallation groupé.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:741` à
  `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:805` couvrent
  le comportement d'ombrage des chemins de chargement groupés empaquetés et
  hérités.
- `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:808` à
  `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:898` couvrent
  les overlays de source groupés par rapport aux bundles dist empaquetés.
- `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:1175` à
  `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:1225` vérifient
  qu'un plugin groupé valide surpasse un package géré source-only.
- `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:1713` à
  `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:1768` vérifient
  que les plugins groupés source-checkout-only restent découvrables aux côtés
  des plugins construits.
- `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:2277` à
  `/Users/kevinlin/code/openclaw/src/plugins/discovery.test.ts:2301` vérifient
  que les répertoires groupés accessibles en écriture par tous sont réparés
  avant le chargement.
- `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.test.ts:326`
  à `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.test.ts:345`
  vérifient que les métadonnées du repo correspondent à l'instantané d'exécution,
  tandis que `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.test.ts:526`
  à `/Users/kevinlin/code/openclaw/src/plugins/bundled-plugin-metadata.test.ts:550`
  exigent des schémas de configuration et une activation de démarrage explicite
  sur les manifestes groupés.
- `/Users/kevinlin/code/openclaw/test/official-channel-catalog.test.ts:71`
  à `/Users/kevinlin/code/openclaw/test/official-channel-catalog.test.ts:205`
  vérifient les plugins de canaux officiels publiables et les entrées externes,
  et `/Users/kevinlin/code/openclaw/test/official-channel-catalog.test.ts:277`
  à `/Users/kevinlin/code/openclaw/test/official-channel-catalog.test.ts:341`
  vérifient que le catalogue généré sous dist reste unique et inclut les
  métadonnées d'installation attendues.
- `/Users/kevinlin/code/openclaw/test/scripts/bundled-plugin-assets.test.ts:40`
  à `/Users/kevinlin/code/openclaw/test/scripts/bundled-plugin-assets.test.ts:76`
  vérifient la découverte des hooks d'actifs et l'analyse des arguments par les
  alias de manifeste/package.

### Commandes de validation de surface

- `pnpm plugin-sdk:check-exports`: `bloqué` - tenté à partir de
  `/Users/kevinlin/code/openclaw`, mais l'installation des dépendances locales
  a échoué avec des erreurs d'authentification du registre 403 pour
  `@microsoft/teams.cards` / `@microsoft/teams.api` et `No authorization header
  was set for the request`; pour cette catégorie, il validerait que les exports
  SDK générés s'alignent toujours avec l'inventaire de points d'entrée enregistré
  utilisé par les surfaces groupées/d'exécution.
- `pnpm plugin-sdk:api:check`: `bloqué` - même blocker de dépendance/authentification
  locale; pour cette catégorie, il validerait que la dérive de l'API SDK
  empaquetée n'a pas cassé les helpers exportés adjacents à la découverte/
  inventaire.
- `pnpm plugin-sdk:surface:check`: `bloqué` - même blocker de dépendance/
  authentification locale; pour cette catégorie, il validerait la dérive du
  budget de surface sur les helpers publics dont le code de découverte et
  d'inventaire groupé dépend.
- `pnpm plugins:boundary-report:ci`: `bloqué` - même blocker de dépendance/
  authentification locale; pour cette catégorie, il validerait les limites
  d'importation réservées et la dette de compatibilité entre propriétaires
  affectant l'empaquetage/la disposition des plugins groupés.
- `pnpm release:plugins:npm:check`: `bloqué` - même blocker de dépendance/
  authentification locale; pour cette catégorie, il validerait les métadonnées
  de release npm pour les lignes d'inventaire externe officiel.
- `pnpm release:plugins:clawhub:check`: `bloqué` - même blocker de dépendance/
  authentification locale; pour cette catégorie, il validerait les métadonnées
  de release ClawHub pour les lignes d'inventaire externe officiel.

### Requêtes Gitcrawl

Requête:

```bash
gitcrawl search openclaw/openclaw --query "bundled plugin discovery inventory" --json
```

Résultats:

- 4 résultats, mode `keyword`.
- PR ouverte #84997, `[AI-assisted] Add NEAR AI Cloud provider`, mentionne les
  entrées d'inventaire de plugins générées.
- Problème ouvert #72991, `[Feature]: Expose machine-wide hook policies`,
  discute des niveaux de découverte groupés/plugins adjacents.
- PR ouverte #83292, `feat(gigachat): add provider integration`, ajoute un
  plugin de fournisseur groupé.
- PR ouverte #87141, `fix(plugin): harden schema and metadata fuzz boundaries`,
  est le travail de durcissement actuel touchant directement la sécurité des
  métadonnées/inventaire des plugins.

Requête:

```bash
gitcrawl search openclaw/openclaw --query "plugin inventory bundled ids" --json
```

Résultats:

- 1 résultat, mode `keyword`.
- PR ouverte #87141, `fix(plugin): harden schema and metadata fuzz boundaries`.

### Requêtes Discrawl

Requête:

```bash
discrawl --json search "bundled plugin inventory" --limit 5
```

Résultats:

- Bloqué localement avec `open sync lock: open /Users/kevinlin/Library/Application Support/discrawl/.discrawl-sync.lock: operation not permitted`.
- Traité comme un blocker de requête local, pas comme une preuve de produit
  positive ou négative.
- La fraîcheur des archives pour la preuve Discord provient toujours de
  l'instantané `discrawl status --json` réussi enregistré ci-dessus.
