---
title: Plugins - Installing and Running Plugins Maturity Note
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Plugins - Installing and Running Plugins Maturity Note

## Summary

Le chargement du runtime et le cycle de vie restent une catégorie Stable. OpenClaw dispose d'un modèle de chargement manifest-first clair, de portes de sécurité pré-exécution, de limites explicites entre cache runtime et métadonnées, de dossiers d'installation durables, de commutation de registre active, de staging de runtime groupé, et de preuves solides de bout en bout pour le cycle de vie des plugins npm gérés, smoke tests d'installation/désinstallation groupés, et tolérance aux mises à jour de plugins corrompus. Les principaux risques restants sont les preuves de runtime inégales sur chaque source d'installation, le modèle de confiance intentionnellement in-process pour les plugins natifs, et la dérive réelle des installations groupées autour de l'état mixte du cache Homebrew Node/runtime/plugin.

## Scope de la catégorie

Cette catégorie couvre le chargement des plugins manifest-first, les portes de sécurité des candidats, les décisions d'activation et de chargement scoped, les modes `setupEntry` et d'activation runtime complet, le remplacement et la réutilisation du registre actif, le staging du runtime groupé, la transmission des dossiers d'installation au chargement runtime, les limites de réparation des dépendances, et les effets d'installation/mise à jour/désinstallation sur l'état du runtime.

Hors scope : le comportement des fonctionnalités par plugin après l'enregistrement, l'ergonomie de la création de plugins, le classement/UX de confiance de la marketplace, et la surface API/subpath SDK publique plus large.

## Fonctionnalités

- Configuration du plugin : Les opérateurs peuvent exécuter les flux de configuration des plugins sans activer complètement le comportement du runtime.
- Activation du runtime : Les plugins activés s'activent et enregistrent le comportement du runtime après la validation réussie du manifest.
- Activation et désactivation : Les opérateurs peuvent activer ou désactiver les plugins installés sans perdre l'état d'installation.
- Chargements sûrs échoués : Les chargements de plugins non sûrs ou non supportés sont bloqués avec des défaillances diagnostiquables avant l'exécution du runtime.
- Réparation des dépendances : Le runtime peut détecter et réparer les dépendances de plugins manquantes ou obsolètes.
- Installation, mise à jour et désinstallation : Le comportement du cycle de vie d'installation, de mise à jour et de désinstallation est défini et testé.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `last_sync_at=2026-05-28T19:09:52.784704Z`, `thread_count=29810`, `open_thread_count=11181`, et `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`.
- discrawl : `discrawl status --json` a réussi avec `generated_at=2026-05-30T00:38:20Z`, `state=current`, résumé `1487536 messages across 25831 channels`, et `last_sync_at=2026-05-29T19:27:40Z`.

## Score de couverture

- Score : `Stable (86%)`
- Signaux positifs :
  - Les docs et la source s'accordent sur une division manifest-first où la validation des métadonnées et la planification du démarrage se produisent avant l'activation runtime complète de `register(api)`.
  - `test:docker:plugin-lifecycle-matrix` exerce le flux de cycle de vie npm réel géré : installation, inspection runtime, désactivation, activation, mise à niveau, rétrogradation, et désinstallation de code manquant.
  - `test:docker:bundled-plugin-install-uninstall` lance une Gateway réelle, attend `/readyz`, effectue des appels RPC runtime, et rejette le travail de dépendance post-ready pour le smoke test du runtime des plugins groupés.
  - `test:docker:update-corrupt-plugin` prouve la tolérance au moment de la mise à jour quand un plugin géré perd `package.json`, y compris les résultats d'avertissement ou de désactivation après défaillance au lieu d'abandonner la mise à jour du cœur.
- Signaux négatifs :
  - La preuve de flux runtime la plus forte concerne les installations npm gérées et les plugins groupés, pas une seule voie détenue par la catégorie couvrant les installations git, ClawHub, marketplace, chemin local, et source liée avec les mêmes assertions de cycle de vie.
  - Le smoke test du runtime groupé ignore intentionnellement les plugins qui nécessitent une configuration, donc les branches de démarrage configuré et `setupEntry` ne sont pas uniformément exercées par des preuves spécifiques à la catégorie en direct.
  - La preuve démontre l'enregistrement du runtime et les effets du cycle de vie CLI, mais pas chaque chemin de redémarrage automatique de l'hôte géré sur les gestionnaires de services.
- Lacunes d'intégration :
  - Ajouter une matrice de cycle de vie qui répète les assertions d'inspection/smoke du runtime sur les sources npm, ClawHub, git, chemin local, source liée, marketplace, et groupées.
  - Ajouter une couverture de smoke du runtime de plugin configuré et `setupEntry` avec des canaux/fournisseurs de fixture sûrs.
  - Ajouter une vérification explicite de redémarrage de Gateway gérée autour de l'installation, la mise à jour, et la désinstallation au lieu de s'appuyer sur les attentes des docs et du chemin de release.

Étiquettes de couverture :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La couverture mesure l'intégration, e2e, en direct, ou les preuves de flux runtime réel sur
la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une fonctionnalité couverte par
eux-mêmes.

## Score de qualité

- Score : `Stable (84%)`
- Rapports Gitcrawl :
  - `gitcrawl search openclaw/openclaw --query "plugin runtime lifecycle install uninstall update corrupt" --json` n'a retourné aucun problème direct ou hit PR pour les régressions de cycle de vie répétées.
  - `gitcrawl search openclaw/openclaw --query "plugin dependency runtime deps repair" --json` a retourné le problème ouvert `#75250`, "Bug: OpenClaw breaks after Homebrew updates due to mixed Homebrew Node/runtime/plugin cache drift", qui est directement pertinent pour la durabilité du chargement runtime pour les installations groupées.
- Rapports Discrawl :
  - `discrawl --json search "plugin runtime lifecycle" --limit 5` a retourné une discussion des mainteneurs et de la communauté sur la performance du rechargement/réutilisation du registre de plugins et les limites de confinement du runtime, mais pas une vague de rapports d'opérateurs selon lesquels le cycle de vie d'installation/désinstallation/mise à jour est largement cassé.
  - `discrawl --json search "plugin install restart runtime" --limit 5` a retourné des discussions de release/aide qui mettent l'accent sur la vérification du redémarrage et la réparation du doctor d'installation/mise à jour des plugins, ce qui renforce que les conseils de redémarrage et de réparation des opérateurs restent une partie importante de l'histoire du cycle de vie.
- Bonnes qualités :
  - Les docs et la source s'alignent sur la division plan de contrôle versus plan de données : les métadonnées de manifest/schéma restent lisibles sur le chemin froid, tandis que le comportement runtime ne provient que des chemins `register(api)` ou `setupEntry`.
  - Les portes de sécurité se produisent avant l'exécution du runtime, et les candidats bloqués restent diagnostiquables par id de plugin au lieu de disparaître silencieusement de la validation de configuration.
  - La gestion de l'état du runtime est explicite : les chargements scoped vides restent vides, le remplacement du registre actif synchronise les surfaces suivies, et les erreurs de chargement peuvent être levées comme des défaillances `PluginLoadFailureError` structurées.
  - Le staging du runtime groupé garde l'alias `openclaw/plugin-sdk` limité aux exports publics générés et exclut intentionnellement `node_modules` du plugin de la superposition du runtime.
- Mauvaises qualités :
  - Les plugins natifs s'exécutent toujours in-process et sans sandbox, donc la correction du cycle de vie ne réduit pas le rayon d'explosion d'un plugin bogué ou malveillant.
  - Les opérateurs doivent toujours distinguer l'inventaire froid (`plugins list`) de l'état d'importation runtime en direct et comprendre quand un redémarrage de Gateway est requis.
  - Le problème `#75250` montre que la dérive des installations groupées reste un risque opérationnel réel quand Node, les fichiers runtime, et les dépendances de plugins en cache divergent.
- Exclu de la qualité :
  - La profondeur unitaire, d'intégration, et Docker e2e ne sont pas utilisées comme entrées de qualité pour cette catégorie.
  - Les commandes de validation de surface bloquée ci-dessous sont traitées comme des bloqueurs de validation locaux, pas comme des preuves de qualité du produit.

Étiquettes de qualité :

- `Lovable`: 95-100
- `Stable`: 80-95
- `Beta`: 70-80
- `Alpha`: 50-70
- `Experimental`: 0-50

Aux limites partagées, choisissez l'étiquette de maturité plus élevée.

La qualité ne doit pas utiliser la couverture de test unitaire, d'intégration, e2e, en direct, ou runtime réel
comme entrée de notation.

## Lacunes connues

- La preuve de flux runtime détenue par la catégorie est toujours la plus forte pour les plugins npm gérés et groupés plutôt que pour toutes les sources d'installation annoncées.
- Les plugins nécessitant une configuration et les chemins de démarrage lourds en `setupEntry` ont toujours besoin de plus de validation en direct dans les voies spécifiques à la catégorie.
- La clarté des opérateurs dépend toujours des conseils de redémarrage et de réparation car la découverte des métadonnées froides et l'activation du runtime en direct sont intentionnellement séparées.
- Le modèle de confiance in-process et le problème ouvert de dérive des installations groupées maintiennent cette catégorie en dessous de Lovable.

# Preuve

## Docs

- `/Users/kevinlin/code/openclaw/docs/plugins/architecture.md:142`-`170` : définit la limite manifest-first, le contenu de l'instantané des métadonnées, les règles de remplacement d'instantané et la division du cache runtime par rapport aux métadonnées.
- `/Users/kevinlin/code/openclaw/docs/plugins/architecture.md:446`-`459` : indique que les plugins natifs s'exécutent en processus, ne sont pas sandboxés, et que la confiance des plugins groupés provient de l'instantané source plutôt que des métadonnées d'installation.
- `/Users/kevinlin/code/openclaw/docs/plugins/architecture-internals.md:20`-`41` : documente l'ordre de chargement, les portes de sécurité pré-exécution et le comportement du cycle de vie `register`/`activate`.
- `/Users/kevinlin/code/openclaw/docs/plugins/architecture-internals.md:45`-`59` : documente le comportement du plan de contrôle manifest-first et maintient les métadonnées `activation` / `setup` séparées de l'enregistrement runtime.
- `/Users/kevinlin/code/openclaw/docs/plugins/architecture-internals.md:99`-`130` : définit la limite du cache des plugins et limite la mise en cache persistante aux artefacts chargés au runtime.
- `/Users/kevinlin/code/openclaw/docs/plugins/architecture-internals.md:869`-`888` : documente la politique de dépendance au moment de l'installation et le comportement de démarrage du canal configuré `setupEntry` / différé.
- `/Users/kevinlin/code/openclaw/docs/plugins/architecture-internals.md:1017`-`1020` : fait de `plugins/installs.json` la source de vérité d'installation durable même lorsque les manifestes sont manquants ou invalides.
- `/Users/kevinlin/code/openclaw/docs/plugins/dependency-resolution.md:11`-`31` : indique que le chargement runtime n'exécute jamais les gestionnaires de paquets et limite la propriété OpenClaw aux opérations explicites du cycle de vie des plugins.
- `/Users/kevinlin/code/openclaw/docs/plugins/dependency-resolution.md:120`-`124` : indique que le démarrage et le rechargement de la configuration lisent les enregistrements d'installation et échouent avec des erreurs de réparation exploitables au lieu de réparer sur place.
- `/Users/kevinlin/code/openclaw/docs/plugins/manage-plugins.md:16`-`21` : définit le flux d'installation comme installation, redémarrage si nécessaire, puis vérification des enregistrements runtime.
- `/Users/kevinlin/code/openclaw/docs/plugins/manage-plugins.md:40`-`44` : indique que `plugins list` est une vérification d'inventaire à froid et ne prouve pas qu'une Gateway en cours d'exécution a importé le runtime du plugin.

## Source

- `/Users/kevinlin/code/openclaw/src/plugins/loader.ts:1536`-`1545` : lève `PluginLoadFailureError` lorsque des erreurs de chargement de plugin sont présentes et que les appelants demandent de lever.
- `/Users/kevinlin/code/openclaw/src/plugins/loader.ts:1548`-`1560` : active le registre et préserve ou réinitialise le coureur de hook global selon le mode runtime.
- `/Users/kevinlin/code/openclaw/src/plugins/loader.ts:1564`-`1576` : préserve les portées de plugin explicites vides au lieu de s'élargir à tous les plugins découverts.
- `/Users/kevinlin/code/openclaw/src/plugins/loader.ts:2494`-`2505` : émet des diagnostics explicites pour les exports `register`/`activate` manquants avant la création de l'API runtime.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime.ts:182`-`198` : remplace le registre actif, synchronise les surfaces HTTP/canal suivies et avance la versioning de l'état runtime.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime/runtime-plugin-boundary.ts:132`-`145` : exige que les modules runtime groupés se chargent nativement en tant que JavaScript construit plutôt que via le secours source.
- `/Users/kevinlin/code/openclaw/scripts/stage-bundled-plugin-runtime.mjs:191`-`205` : génère l'alias runtime `openclaw/plugin-sdk` à partir des exports dist publics uniquement.
- `/Users/kevinlin/code/openclaw/scripts/stage-bundled-plugin-runtime.mjs:278`-`318` : prépare les superpositions runtime tout en ignorant le `node_modules` du plugin, en enveloppant les fichiers JS runtime et en copiant uniquement les fichiers runtime sélectionnés.
- `/Users/kevinlin/code/openclaw/scripts/stage-bundled-plugin-runtime.mjs:322`-`345` : reconstruit `dist-runtime/extensions` à partir de `dist/extensions` et supprime les racines runtime obsolètes avant la préparation.

## Tests d'intégration

- `/Users/kevinlin/code/openclaw/package.json:1642` : câble `test:docker:bundled-plugin-install-uninstall`.
- `/Users/kevinlin/code/openclaw/package.json:1703` : câble `test:docker:plugin-lifecycle-matrix`.
- `/Users/kevinlin/code/openclaw/package.json:1714` : câble `test:docker:update-corrupt-plugin`.
- `/Users/kevinlin/code/openclaw/docs/help/testing.md:791`-`793` : documente le cycle de vie runtime et les voies Docker d'installation/mise à jour de plugin qui soutiennent cette catégorie.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/sweep.sh:41`-`66` : couvre l'installation npm gérée, l'inspection runtime, la désactivation/activation, la mise à niveau/rétrogradation et la désinstallation du code manquant.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-lifecycle-matrix/probe.mjs:38`-`71` : affirme la version installée et la disposition du projet npm root pour les installations de plugins gérés.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/sweep.sh:40`-`57` : installe les plugins groupés, exécute le smoke runtime, puis les désinstalle de force.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:376`-`430` : démarre un vrai processus Gateway et attend la disponibilité.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:500`-`538` : vérifie `/readyz` et effectue des appels RPC Gateway sur WebSocket avec authentification par jeton.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/bundled-plugin-install-uninstall/runtime-smoke.mjs:817`-`819` : échoue le smoke runtime si le travail d'installation de dépendance post-ready apparaît dans les journaux.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-update/corrupt-update-scenario.sh:37`-`69` : installe un plugin externe géré, supprime `package.json` et met à jour OpenClaw avec un état de plugin corrompu présent.
- `/Users/kevinlin/code/openclaw/scripts/e2e/lib/plugin-update/probe.mjs:115`-`188` : exige des résultats tolérés ou avertis et valide le comportement désactivé après défaillance pour les plugins corrompus.

## Tests unitaires

- `/Users/kevinlin/code/openclaw/src/plugins/runtime/load-context.test.ts:145` : vérifie que les métadonnées dérivées deviennent un instantané runtime réutilisable.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime/load-context.test.ts:188` : vérifie que les enregistrements d'installation s'enfilent à partir de l'instantané des métadonnées dans les options de chargement runtime.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime/runtime-registry-loader.test.ts:173` : vérifie que les chargements de canal configuré réutilisent le contexte de chargement runtime partagé.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime/runtime-registry-loader.test.ts:378` : vérifie que les chargements de portée all vides sont préservés au lieu de s'élargir.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime/runtime-registry-loader.test.ts:389` : vérifie que les registres actifs vides peuvent être réutilisés en toute sécurité.
- `/Users/kevinlin/code/openclaw/src/plugins/runtime/runtime-registry-loader.test.ts:429` : vérifie que les registres actifs non vides ne sont pas incorrectement réutilisés pour les chargements de portée vide.
- `/Users/kevinlin/code/openclaw/src/plugins/stage-bundled-plugin-runtime.test.ts:97` : vérifie que les enveloppes runtime sont préparées sans lier le `node_modules` du plugin.
- `/Users/kevinlin/code/openclaw/src/plugins/stage-bundled-plugin-runtime.test.ts:546` : vérifie que les répertoires de plugins runtime obsolètes sont supprimés lorsqu'ils ne sont plus présents dans `dist`.

## Commandes de validation de surface

- `pnpm plugin-sdk:check-exports` : `blocked` - vérifierait que l'inventaire d'export SDK public généré correspond toujours à l'alias runtime enregistré/surface de préparation, mais la validation locale n'a jamais atteint la sémantique de commande car l'installation de dépendance a échoué avec des erreurs d'authentification de registre 403 pour `@microsoft/teams.cards` / `@microsoft/teams.api` et `No authorization header was set for the request`.
- `pnpm plugin-sdk:api:check` : `blocked` - détecterait la dérive de l'API SDK Plugin public qui peut affecter la compatibilité du chargement/préparation runtime, mais le même échec d'authentification de dépendance locale a bloqué la validation réelle.
- `pnpm plugin-sdk:surface:check` : `blocked` - appliquerait les limites de taille de surface SDK publique et d'export obsolète qui alimentent la préparation runtime groupée, mais le même échec d'authentification de dépendance locale a bloqué la validation réelle.
- `pnpm plugins:boundary-report:ci` : `blocked` - validerait les contrats de limite de plugin d'importation réservée et de propriétaire croisé pertinents aux coutures de chargement runtime, mais le même échec d'authentification de dépendance locale a bloqué la validation réelle.
- `pnpm release:plugins:npm:check` : `blocked` - validerait les métadonnées/disponibilité de version npm pour les flux de cycle de vie de plugin emballés, mais le même échec d'authentification de dépendance locale a bloqué la validation réelle.
- `pnpm release:plugins:clawhub:check` : `blocked` - validerait les métadonnées/disponibilité de version ClawHub pour les chemins de distribution de plugin adjacents à cette catégorie, mais le même échec d'authentification de dépendance locale a bloqué la validation réelle.

## Requêtes Gitcrawl

Requête :

`gitcrawl search openclaw/openclaw --query "plugin runtime lifecycle install uninstall update corrupt" --json`

Résultats :

- `{"hits":[],"mode":"keyword","query":"plugin runtime lifecycle install uninstall update corrupt","repository":"openclaw/openclaw"}`

Requête :

`gitcrawl search openclaw/openclaw --query "plugin dependency runtime deps repair" --json`

Résultats :

- Un problème ouvert : `#75250` "Bug: OpenClaw breaks after Homebrew updates due to mixed Homebrew Node/runtime/plugin cache drift" (`https://github.com/openclaw/openclaw/issues/75250`). L'extrait mentionne la dérive de version de l'hôte gateway et les dépendances runtime du plugin en cache référençant des fichiers SDK manquants.

## Requêtes Discrawl

Requête :

`discrawl --json search "plugin runtime lifecycle" --limit 5`

Résultats :

- A retourné une discussion mainteneur/communauté plutôt que des rapports de défaillance répétés, y compris une mise à jour du mainteneur sur le travail de rechargement/réutilisation du registre de plugins et une discussion de conception sur le confinement runtime pour l'automatisation basée sur les compétences.

Requête :

`discrawl --json search "plugin install restart runtime" --limit 5`

Résultats :

- A retourné des messages de version/aide qui mettent l'accent sur la réparation d'installation/mise à jour/docteur de plugin et la vérification du redémarrage de Gateway, y compris les notes bêta de mai 2026 et les conseils d'aide utilisateur pour réinstaller un plugin et redémarrer la Gateway.
