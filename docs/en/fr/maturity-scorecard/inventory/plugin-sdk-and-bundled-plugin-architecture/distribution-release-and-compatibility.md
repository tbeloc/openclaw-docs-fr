---
title: Plugins - Publishing Plugins Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Plugins - Publishing Plugins Maturity Note

## Résumé

OpenClaw dispose d'une véritable distribution, d'une version et d'une catégorie de compatibilité pour les plugins groupés et externes. La documentation distingue les plugins groupés, externes officiels et source-checkout-only ; explique la sélection de source déterministe sur ClawHub, npm, git, les chemins locaux, les archives et les places de marché ; et documente le comportement de secours de compatibilité pour les versions npm incompatibles. Le code source soutient cela avec des contrats de métadonnées de packages externes partagés, des vérificateurs/planificateurs de version npm et ClawHub explicites, des portes de compatibilité d'installation de packages et ClawHub, et une validation de pack de version qui exerce les installations empaquetées, l'activation groupée et la consommation du SDK Plugin public.

La catégorie n'est pas Lovable car la preuve de flux d'exécution la plus forte est toujours Docker local et fumée de version empaquetée plutôt qu'une boucle actuelle de publication/installation/mise à jour/restauration pour npm et ClawHub. Les preuves d'archive montrent également une pression écosystémique continue autour de l'alignement des métadonnées propriétaire/registre et un piégeage de compatibilité de plugin externe plus large.

## Portée de la catégorie

Cette catégorie couvre le comportement de distribution, de version et de compatibilité pour la surface Plugins :

- Distribution de plugin groupé par rapport à externe officiel par rapport à source-checkout-only.
- Sémantique d'installation/mise à jour ClawHub, npm, git, chemin local, archive et place de marché pour les plugins.
- Métadonnées de compatibilité de plugin externe, contrats de packages et portage d'API hôte/plugin au moment de l'installation.
- Planification de version et vérifications préalables pour la publication de plugin npm et ClawHub.
- Validation de version empaquetée qui protège les exports du SDK Plugin, l'activation de plugin groupé et les artefacts d'exécution/installation empaquetés.

Hors de portée : qualité de fonctionnalité d'exécution de plugin individuel après installation, comportement de canal/fournisseur et distribution de compétences non-plugin.

## Fonctionnalités

- Sources d'installation : Les sources d'installation de plugin prises en charge sont explicites et validées.
- Publication ClawHub : Les métadonnées et flux de travail des plugins prennent en charge la publication sur ClawHub.
- Publication npm : Les métadonnées et flux de travail des plugins prennent en charge la publication sur npm le cas échéant.
- Signalisation de compatibilité : Les données du registre de compatibilité mappent les plugins aux versions ou canaux d'exécution pris en charge.
- Attentes de mise à jour et de restauration : La sémantique de mise à jour des plugins définit ce qui peut être mis à niveau sur place et ce qui nécessite une intervention de l'opérateur.
- Règles de publication par tiers : Les règles d'acceptation de packages externes contrôlent l'empaquetage et la publication de plugins tiers.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec
  `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`,
  `open_thread_count=11181`,
  `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`.
- discrawl : `discrawl status --json` a réussi avec
  `generated_at=2026-05-30T00:38:20Z`, `state=current`,
  `summary=1487536 messages across 25831 channels`, et
  `last_sync_at=2026-05-29T19:27:40Z`.

## Score de couverture

- Score : `Beta (79%)`
- Signaux positifs :
  - Le scénario Docker de la matrice de cycle de vie installe un plugin npm de fixture, inspecte l'enregistrement d'exécution, le désactive et le réactive, met à niveau, rétrograde et force-désinstalle après suppression du code de plugin
    (`/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:41`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:45`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:53`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:57`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:68`).
  - Le scénario de place de marché de version couvre la liste de place de marché, l'installation, l'exécution CLI propriétaire du plugin, la mise à jour d'essai, la mise à jour, la réexécution, la désinstallation et l'absence post-désinstallation
    (`/Users/kevinlin/code/openclaw/scripts/e2e/lib/release-plugin-marketplace/scenario.sh:76`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/release-plugin-marketplace/scenario.sh:79`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/release-plugin-marketplace/scenario.sh:91`,
    `/Users/kevinlin/code/openclaw/scripts/e2e/lib/release-plugin-marketplace/scenario.sh:96`).
  - `release-check` vérifie l'intégrité du package installé empaqueté, la postinstallation groupée, la fumée d'activation groupée, la consommation TypeScript du SDK Plugin empaqueté, les exports/imports SDK critiques, la fumée d'entrée de canal groupée et la validation de surface empaquetée finale
    (`/Users/kevinlin/code/openclaw/scripts/release-check.ts:499`,
    `/Users/kevinlin/code/openclaw/scripts/release-check.ts:609`,
    `/Users/kevinlin/code/openclaw/scripts/release-check.ts:680`,
    `/Users/kevinlin/code/openclaw/scripts/release-check.ts:781`,
    `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1084`,
    `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1120`,
    `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1211`).
  - Le repo câble les points d'entrée de validation de version et de cycle de vie de plugin dédiés dans les scripts de package, de sorte que ces flux sont des vérifications de version de première classe plutôt que des scripts locaux ad hoc
    (`/Users/kevinlin/code/openclaw/package.json:1609`,
    `/Users/kevinlin/code/openclaw/package.json:1614`,
    `/Users/kevinlin/code/openclaw/package.json:1616`,
    `/Users/kevinlin/code/openclaw/package.json:1697`,
    `/Users/kevinlin/code/openclaw/package.json:1703`).
- Signaux négatifs :
  - La preuve de flux d'exécution localisée est toujours fixture/locale : un registre npm factice, une fixture de place de marché Claude locale et une installation de tarball empaquetée. C'est une bonne couverture de version, mais ce n'est pas une preuve actuelle de publication npm en direct, de mutation de dist-tag, de publication ClawHub ou d'installation/mise à jour/restauration de registre de production.
  - Aucun des flux d'exécution localisés n'exerce directement une installation ClawHub réelle suivie d'une mise à jour/rétrogradation/restauration par rapport au registre distant.
  - Les preuves de PR Gitcrawl incluent toujours des notes explicites selon lesquelles les flux d'installation/mise à jour/désinstallation et de publication npm/ClawHub en direct n'ont pas été vérifiés dans les travaux adjacents de gestion des plugins et de chaîne d'approvisionnement.
  - Les commandes de validation détenues par la taxonomie ont été tentées à partir de
    `/Users/kevinlin/code/openclaw` mais bloquées avant la validation réelle par des échecs d'installation de dépendances locales (`403` erreurs d'authentification pour
    `@microsoft/teams.cards` / `@microsoft/teams.api` et `No authorization
header was set for the request`). C'est un bloqueur de validation local, pas un signal de qualité de produit, mais cela signifie également que ces commandes n'ont pas ajouté de preuve d'exécution fraîche pour cette réévaluation.
- Lacunes d'intégration :
  - Ajouter une voie de publication de staging ou jetable qui publie réellement les packages de plugin candidats sur npm et ClawHub, puis les installe, les met à jour, les rétrograde et les désinstalle à partir de ces registres réels.
  - Ajouter une voie de flux d'exécution ClawHub explicite qui exerce l'acceptation/rejet de compatibilité API de plugin et d'hôte minimum via le chemin d'installation distant, pas seulement la validation source/package-locale.
  - Publier les identifiants CI/build ou les artefacts de version qui connectent `release:check` et les plans de version de plugin aux exécutions de publication réelles que les opérateurs peuvent auditer.

## Score de Qualité

- Score : `Stable (82%)`
- Rapports Gitcrawl :
  - `gitcrawl search openclaw/openclaw --query "plugin compatibility ClawHub npm release" --json`
    a retourné trois demandes de tirage ouvertes pertinentes : `#87477` sur le rejet
    des installations de plugins d'API incompatibles, `#81957` sur le durcissement
    de la chaîne d'approvisionnement des versions, et `#75186` sur les RPC de gestion
    des plugins. `#81957` et `#75186` notent explicitement que la preuve du cycle de vie
    de publication ou d'installation npm/ClawHub en direct n'a pas été effectuée. `#87477`
    montre que ce chemin de compatibilité a été sous une pression de durcissement active
    très récemment.
  - `gitcrawl search openclaw/openclaw --query "plugin lifecycle install update rollback compatibility" --json`
    a retourné la PR ouverte `#73767`, dont l'extrait référence les alias de compatibilité,
    le support du cycle de vie groupé, et les vérifications de propriété. C'est plus de
    changements que d'échecs, mais c'est toujours une preuve que cette surface de compatibilité
    est active et pas encore stabilisée.
- Rapports Discrawl :
  - `discrawl --json search "ClawHub plugin compatibility" --limit 5` a retourné
    une discussion des responsables de `#maintainers` du 2026-05-27 arguant que le
    piège de compatibilité actuel (`crabpot`) devrait s'étendre au-delà des vérifications
    de couture API vers des évaluations de plugins réels basées sur les catégories. Cela
    indique que le signal de compatibilité actuel est utile mais incomplet pour la détection
    des régressions de l'écosystème.
  - La même requête a retourné une discussion des 2026-05-06 et 2026-05-07 décrivant
    des incompatibilités généralisées de propriétaires de plugins à portée sur ClawHub
    et proposant une migration de vérité de registre au lieu de faire confiance à la portée
    npm seule. C'est une véritable préoccupation concernant la correction de la distribution
    et la qualité de la migration des métadonnées.
- Bonnes qualités :
  - La documentation explique clairement la sélection de source et le comportement de
    secours : ClawHub comme découverte primaire, préfixes de source explicites déterministes,
    précédence des plugins groupés, et secours de compatibilité vers les versions npm stables
    plus anciennes lorsque la dernière version nécessite une API de plugin plus récente ou
    une version d'hôte minimale plus récente
    (`/Users/kevinlin/code/openclaw/docs/tools/plugin.md:42`,
    `/Users/kevinlin/code/openclaw/docs/tools/plugin.md:120`,
    `/Users/kevinlin/code/openclaw/docs/tools/plugin.md:139`,
    `/Users/kevinlin/code/openclaw/docs/cli/plugins.md:125`,
    `/Users/kevinlin/code/openclaw/docs/cli/plugins.md:228`).
  - La documentation d'inventaire et de publication rend explicites les catégories de
    distribution et les limites de propriété, ce qui réduit l'ambiguïté entre les plugins
    groupés, externes officiels et source uniquement, et entre la portée du package et la
    propriété de l'éditeur
    (`/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:21`,
    `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:31`,
    `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:141`,
    `/Users/kevinlin/code/openclaw/docs/clawhub/publishing.md:11`,
    `/Users/kevinlin/code/openclaw/docs/clawhub/publishing.md:42`,
    `/Users/kevinlin/code/openclaw/docs/clawhub/publishing.md:56`).
  - Le contrat de package partagé nécessite `openclaw.compat.pluginApi` et
    `openclaw.build.openclawVersion`, normalise les métadonnées de compatibilité, et est
    réutilisé par les outils de version npm et ClawHub
    (`/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:20`,
    `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:46`,
    `/Users/kevinlin/code/openclaw/scripts/lib/plugin-npm-release.ts:225`,
    `/Users/kevinlin/code/openclaw/scripts/lib/plugin-clawhub-release.ts:101`).
  - Les installations de packages directs et les installations source/package-dir exécutent
    désormais une validation de compatibilité d'hôte minimum et d'API de plugin partagée,
    tandis que les installations ClawHub appliquent les mêmes dimensions de compatibilité
    avant le téléchargement. Cela réduit un écart de qualité plus ancien entre les installations
    directes et gérées par ClawHub
    (`/Users/kevinlin/code/openclaw/src/plugins/install.ts:145`,
    `/Users/kevinlin/code/openclaw/src/plugins/install.ts:170`,
    `/Users/kevinlin/code/openclaw/src/plugins/install.ts:1422`,
    `/Users/kevinlin/code/openclaw/src/plugins/install.ts:1600`,
    `/Users/kevinlin/code/openclaw/src/plugins/clawhub.ts:963`).
  - Les outils de version appliquent les métadonnées publiables, la sélection de packages,
    les portes de bump de version, les vérifications de propriétaire ClawHub, et le comportement
    de secours officiel lors des mises à jour ; `release-check` protège également les exports
    SDK empaquetés, le contenu des packages, et l'activation groupée
    (`/Users/kevinlin/code/openclaw/scripts/lib/plugin-npm-release.ts:239`,
    `/Users/kevinlin/code/openclaw/scripts/lib/plugin-npm-release.ts:492`,
    `/Users/kevinlin/code/openclaw/scripts/lib/plugin-clawhub-release.ts:282`,
    `/Users/kevinlin/code/openclaw/scripts/lib/plugin-clawhub-release.ts:353`,
    `/Users/kevinlin/code/openclaw/src/plugins/update.ts:1368`,
    `/Users/kevinlin/code/openclaw/src/plugins/update.ts:1641`,
    `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1162`).
- Mauvaises qualités :
  - `docs/plugins/compatibility.md` encadre toujours l'inspecteur de plugins externe comme
    un package séparé futur plutôt qu'un outil livré, donc l'une des garde-fous de compatibilité
    prévus est toujours aspirationnelle
    (`/Users/kevinlin/code/openclaw/docs/plugins/compatibility.md:46`).
  - La documentation décrit toujours un état de transition de lancement où ClawHub est la
    surface de découverte primaire mais les spécifications de packages nus ordinaires se
    résolvent fréquemment via npm. C'est acceptable, mais cela augmente l'ambiguïté de
    l'opérateur concernant la source de vérité et la provenance
    (`/Users/kevinlin/code/openclaw/docs/tools/plugin.md:42`,
    `/Users/kevinlin/code/openclaw/docs/cli/plugins.md:125`).
  - Il n'existe toujours pas de fiche de score de compatibilité unique publiée face à
    l'opérateur ou de matrice de support qui lie les versions d'hôte, les plages d'API de
    plugin, les packages npm, et la disponibilité ClawHub ensemble à la même révision.
  - Les preuves d'archive montrent une pression continue autour de la vérité du propriétaire
    du registre et le besoin d'un piégeage de compatibilité de plugins réels plus large, ce
    qui signifie que cette catégorie dépend toujours de la vigilance active des responsables
    plutôt que d'un processus stabilisé et ennuyeux.
- Exclu de la qualité :
  - Couverture des tests unitaires, d'intégration, e2e, en direct et de flux d'exécution.
  - Manque de couverture de test.

## Lacunes Connues

- Ajouter des preuves réelles de publication/installation/mise à jour/restauration pour npm
  et ClawHub, pas seulement des preuves de fixture et de version empaquetée.
- Livrer ou remplacer clairement le flux de travail d'inspecteur de plugins externe prévu
  afin que les conseils de compatibilité ne soient pas partiellement aspirationnels.
- Réduire l'ambiguïté de l'opérateur entre la découverte primaire ClawHub et les installations
  de packages nus par défaut npm pendant le comportement de transition actuel.
- Publier une matrice de compatibilité/support canonique pour les auteurs de plugins externes
  et les opérateurs qui lie les versions d'hôte, les plages d'API de plugin, et la disponibilité
  du registre ensemble.
- Résoudre l'histoire de migration d'incompatibilité de propriétaire de registre afin que les
  noms de packages à portée ne restent pas un risque récurrent de correction de distribution.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/tools/plugin.md:42` documente ClawHub comme
  découverte primaire tout en expliquant le comportement de secours des paquets groupés et npm pendant la transition actuelle.
- `/Users/kevinlin/code/openclaw/docs/tools/plugin.md:120` à `:145`
  définit les règles de sélection de source et le secours de compatibilité stable antérieure pour les installations npm.
- `/Users/kevinlin/code/openclaw/docs/cli/plugins.md:104` à `:118`
  énumère les points d'entrée d'installation pour ClawHub, npm, `npm-pack`, git, chemin local,
  et sources de marketplace.
- `/Users/kevinlin/code/openclaw/docs/cli/plugins.md:125` à `:140`
  décrit les installations npm par défaut sans arguments pendant la transition et ClawHub comme distribution/découverte primaire.
- `/Users/kevinlin/code/openclaw/docs/cli/plugins.md:228` à `:229`
  documente les vérifications d'API de plugin/hôte minimum, la vérification ClawPack, et les métadonnées d'installation enregistrées pour les installations ClawHub.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:21` à
  `:23` définit les catégories de paquets groupés, officiels externes, et checkout-source uniquement.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:31` à
  `:47` explique comment les opérateurs choisissent les chemins d'installation à partir de l'inventaire de distribution.
- `/Users/kevinlin/code/openclaw/docs/plugins/plugin-inventory.md:141` à
  `:176` liste les paquets externes officiels distribués via npm et/ou ClawHub.
- `/Users/kevinlin/code/openclaw/docs/plugins/compatibility.md:17` à `:32`
  définit le contrat du registre de compatibilité et les attentes de maintenance.
- `/Users/kevinlin/code/openclaw/docs/plugins/compatibility.md:46` à `:86`
  documente l'inspecteur de plugin externe planifié et la voie d'acceptation.
- `/Users/kevinlin/code/openclaw/docs/plugins/compatibility.md:90` à `:105`
  définit la politique de dépréciation et la séquence de migration.
- `/Users/kevinlin/code/openclaw/docs/clawhub/publishing.md:11` à `:18`
  définit la publication avec portée propriétaire.
- `/Users/kevinlin/code/openclaw/docs/clawhub/publishing.md:42` à `:65`
  définit la correspondance portée-paquet/propriétaire et le flux de validation de version ClawHub.

## Source

- `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:20`
  à `:23` définit les champs de compatibilité de plugin externe requis.
- `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:46`
  à `:74` normalise les métadonnées de compatibilité d'API de plugin, de passerelle minimum, et de version de build.
- `/Users/kevinlin/code/openclaw/packages/plugin-package-contract/src/index.ts:77`
  à `:99` valide les champs de plugin externe requis manquants.
- `/Users/kevinlin/code/openclaw/src/plugins/install.ts:145` à `:206`
  implémente les vérifications de compatibilité d'hôte minimum et d'API de plugin partagées pour les installations de paquet.
- `/Users/kevinlin/code/openclaw/src/plugins/install.ts:1422` à `:1429`
  applique cette validation aux installations de bundle/source avec métadonnées de paquet.
- `/Users/kevinlin/code/openclaw/src/plugins/install.ts:1600` à `:1607`
  applique cette validation aux installations de répertoire de paquet.
- `/Users/kevinlin/code/openclaw/src/plugins/clawhub.ts:963` à `:1015`
  rejette les familles de paquets ClawHub incompatibles, les modes de confidentialité, les plages d'API de plugin, et les versions de passerelle minimum.
- `/Users/kevinlin/code/openclaw/src/plugins/clawhub.ts:1115` à `:1253`
  vérifie l'intégrité ClawPack/archive et enregistre les métadonnées d'artefact pour les mises à jour ultérieures.
- `/Users/kevinlin/code/openclaw/src/plugins/update.ts:1368` à `:1423`
  supporte le secours du canal bêta et npm officiel pendant les mises à jour d'essai.
- `/Users/kevinlin/code/openclaw/src/plugins/update.ts:1611` à `:1655`
  supporte le même comportement de secours pendant les mises à jour réelles.
- `/Users/kevinlin/code/openclaw/scripts/lib/plugin-npm-release.ts:225` à
  `:337` valide les métadonnées de plugin npm publiables et collecte les candidats.
- `/Users/kevinlin/code/openclaw/scripts/lib/plugin-npm-release.ts:492` à
  `:536` résout les plans de version npm et ignore les versions déjà publiées.
- `/Users/kevinlin/code/openclaw/scripts/lib/plugin-clawhub-release.ts:101`
  à `:179` valide les métadonnées de plugin ClawHub publiables.
- `/Users/kevinlin/code/openclaw/scripts/lib/plugin-clawhub-release.ts:282`
  à `:318` applique les portes de bump de version pour les plugins publiables modifiés.
- `/Users/kevinlin/code/openclaw/scripts/lib/plugin-clawhub-release.ts:353`
  à `:404` vérifie que les paquets `@openclaw/*` appartiennent déjà au propriétaire OpenClaw sur ClawHub.
- `/Users/kevinlin/code/openclaw/scripts/lib/plugin-clawhub-release.ts:406`
  à `:455` construit les plans de version ClawHub et filtre les versions déjà publiées.
- `/Users/kevinlin/code/openclaw/scripts/release-check.ts:499` à `:560`
  vérifie le contenu du paquet installé emballé et la version binaire.
- `/Users/kevinlin/code/openclaw/scripts/release-check.ts:609` à `:635`
  exécute un test de fumée du consommateur TypeScript du SDK de plugin emballé.
- `/Users/kevinlin/code/openclaw/scripts/release-check.ts:680` à `:707`
  exécute le test de fumée d'activation du plugin groupé sur une installation emballée.
- `/Users/kevinlin/code/openclaw/scripts/release-check.ts:781` à `:821`
  exécute le flux de test de fumée d'entrée du canal groupé emballé.
- `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1084` à `:1155`
  vérifie les exportations critiques du SDK de plugin public et l'importabilité.
- `/Users/kevinlin/code/openclaw/scripts/release-check.ts:1162` à `:1213`
  valide le contenu du paquet et les invariants finaux de surface emballée.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/scripts/e2e/plugin-lifecycle-matrix-docker.sh:1`
  définit le point d'entrée de la matrice de cycle de vie Docker.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:41`
  à `:69` couvre l'installation npm, l'inspection à l'exécution, la désactivation/activation, la mise à niveau,
  la rétrogradation, et la désinstallation de code manquant.
- `/Users/kevinlin/code/openclaw/scripts/e2e/release-plugin-marketplace-docker.sh:1`
  définit le point d'entrée du scénario de version marketplace.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/release-plugin-marketplace/scenario.sh:76`
  à `:103` couvre le comportement de liste/installation/mise à jour/désinstallation de marketplace et la vérification CLI.
- `/Users/kevinlin/code/openclaw/package.json:1697` câble
  `test:docker:release-plugin-marketplace`.
- `/Users/kevinlin/code/openclaw/package.json:1703` câble
  `test:docker:plugin-lifecycle-matrix`.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/test/plugin-clawhub-release.test.ts:58`
  à `:65` exige le contrat de compatibilité de plugin externe pour les candidats de version ClawHub.
- `/Users/kevinlin/code/openclaw/test/plugin-clawhub-release.test.ts:120`
  à `:159` maintient les plugins de diagnostics publiés en double sélectionnables via
  les chemins de version npm et ClawHub.
- `/Users/kevinlin/code/openclaw/test/plugin-clawhub-release.test.ts:164`
  à `:193` applique les bumps de version pour les plugins ClawHub publiables modifiés.
- `/Users/kevinlin/code/openclaw/test/plugin-clawhub-release.test.ts:373`
  à `:398` applique la correction du propriétaire ClawHub pour les paquets `@openclaw/*`.
- `/Users/kevinlin/code/openclaw/test/plugin-npm-release.test.ts:158` à
  `:233` applique les exigences d'URL de provenance npm, de métadonnées d'installation, et de contrat de compatibilité.
- `/Users/kevinlin/code/openclaw/test/plugin-npm-release.test.ts:238` à
  `:257` maintient les arbres dist de plugin publiables exclus du paquet npm principal.
- `/Users/kevinlin/code/openclaw/test/plugin-npm-release.test.ts:372` à
  `:404` mappe les versions de préversion aux balises npm de publication correctes.
- `/Users/kevinlin/code/openclaw/test/plugin-npm-package-manifest.test.ts:231`
  à `:309` prépare les métadonnées d'exécution correctement lors de l'emballage des plugins publiables.
- `/Users/kevinlin/code/openclaw/test/plugin-npm-package-manifest.test.ts:311`
  à `:380` groupe et nettoie les dépendances d'exécution locales au paquet.
- `/Users/kevinlin/code/openclaw/test/plugin-npm-package-manifest.test.ts:523`
  à `:560` échoue fermé lorsque les fichiers d'exécution annoncés sont manquants ou exclus des paquets.
- `/Users/kevinlin/code/openclaw/test/release-check.test.ts:287` à `:316`
  valide les métadonnées d'installation groupées et le formatage de version d'hôte minimum.
- `/Users/kevinlin/code/openclaw/test/release-check.test.ts:701` à `:750`
  vérifie l'intégrité du paquet post-emballage et les vérifications de sécurité d'alias racine.
- `/Users/kevinlin/code/openclaw/test/release-check.test.ts:792` à `:826`
  vérifie l'accessoire de test de fumée TypeScript du SDK de plugin emballé.
- `/Users/kevinlin/code/openclaw/test/release-check.test.ts:859` à `:876`
  applique les budgets de taille de point d'entrée SDK de plugin public critique.

## Commandes de validation de surface

- `pnpm plugin-sdk:check-exports`: `bloqué` - vérifierait la synchronisation de l'inventaire d'exportation SDK public généré; tenté depuis `/Users/kevinlin/code/openclaw`, mais l'environnement local a échoué avant la validation réelle car l'installation des dépendances a rencontré des erreurs d'authentification `403` pour `@microsoft/teams.cards` /
  `@microsoft/teams.api` et `No authorization header was set for the request`.
- `pnpm plugin-sdk:api:check`: `bloqué` - détecterait la dérive de l'API du SDK de plugin public emballé; bloqué par le même échec d'authentification des dépendances locales, donc neutre pour ce score de catégorie.
- `pnpm plugin-sdk:surface:check`: `bloqué` - appliquerait les budgets de taille de surface SDK et les limites d'exportation dépréciée; bloqué par le même
  échec d'authentification des dépendances locales, donc neutre pour ce score de catégorie.
- `pnpm plugins:boundary-report:ci`: `bloqué` - validerait les limites d'importation réservées, les sous-chemins réservés non classifiés, et la dette de compatibilité; bloqué par le même échec d'authentification des dépendances locales, donc neutre pour ce score de catégorie.
- `pnpm release:plugins:npm:check`: `bloqué` - validerait les métadonnées de plugin npm publiables et la préparation de version depuis la racine du dépôt; bloqué par le même échec d'authentification des dépendances locales, donc neutre pour ce score de catégorie.
- `pnpm release:plugins:clawhub:check`: `bloqué` - validerait les métadonnées de plugin ClawHub publiables et la préparation de version; bloqué par le même échec d'authentification des dépendances locales, donc neutre pour ce score de catégorie.

## Requêtes Gitcrawl

Requête:

`gitcrawl search openclaw/openclaw --query "plugin compatibility ClawHub npm release" --json`

Résultats:

- La PR ouverte `#87477` (`fix(plugins): reject incompatible package plugin API installs`) indique que la compatibilité d'installation de paquet direct était en cours d'alignement avec les vérifications d'API de plugin ClawHub.
- La PR ouverte `#81957` (`ci: harden GitHub Actions supply-chain boundaries`) indique qu'aucune publication npm en direct, mutation de dist-tag, publication ClawHub, publication de version, ou exécution de passerelle de production n'a été effectuée dans ce travail de durcissement.
- La PR ouverte `#75186` (`[Feat] Add plugin management RPCs`) indique que l'installation/mise à jour/désinstallation npm/ClawHub en direct n'a pas été vérifiée.

Requête:

`gitcrawl search openclaw/openclaw --query "plugin lifecycle install update rollback compatibility" --json`

Résultats:

- La PR ouverte `#73767` (`[codex] Finalize RuntimePlan embedded-runner cleanup stack`)
  mentionne les alias de compatibilité, le support de cycle de vie groupé natif, et
  les surfaces de plugin vérifiées par propriété.

Requête:

`gitcrawl search openclaw/openclaw --query "reject incompatible package plugin API installs" --json`

Résultats:

- La PR ouverte `#87477` renforce que le rejet de compatibilité d'installation de paquet
  a été un travail de durcissement récent sur cette surface.

## Requêtes Discrawl

Requête:

`discrawl --json search "ClawHub plugin compatibility" --limit 5`

Résultats:

- Un message `#maintainers` du 2026-05-27 propose d'étendre le piège de compatibilité `crabpot`
  au-delà des vérifications de couture d'API vers les évaluations de plugin réel basées sur les catégories, impliquant que la capture de régression de plugin externe actuelle est encore étroite.
- Un message `#maintainers` du 2026-05-06 décrit approximativement `61.8%` de décalage de propriétaire de plugin à portée et plaide pour résoudre l'organisation d'installation à partir des métadonnées du registre ClawHub plutôt que de la portée npm.
- Une discussion du 2026-05-07 appelle également le décalage de propriété ClawHub/plugin comme un problème majeur de migration et le lie à la correction de distribution.
