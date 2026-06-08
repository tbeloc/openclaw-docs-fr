---
title: Matrice des fonctionnalités des plugins
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Matrice des fonctionnalités des plugins

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Stable (82%)`
- Qualité : `Stable (80%)`
- Complétude : `Stable (81%)`
- Fonctionnalités LTS : `7/9`

## Résumé

Ce rapport développe la surface de scorecard nommée « Plugins »
de la scorecard de maturité dans les principales catégories orientées vers
les auteurs, les opérateurs et les responsables de maintenance derrière cette ligne.

L'audit détaillé soutient un rollup Stable à la fois pour la Couverture et la
Qualité, mais la surface devrait toujours être interprétée comme bêta-vers-stable
plutôt que promue sans conditions. Les domaines les plus forts sont la découverte
des plugins groupés, le chargement à l'exécution, l'architecture fournisseur/outil
et les limites d'approbation/sécurité. Le principal bloqueur de promotion est
l'API SDK publique et la surface de sous-chemin : sa note de catégorie enregistre
toujours les scores les plus bas de la surface à `Beta (77%)` Couverture et
`Beta (74%)` Qualité, avec des preuves d'archive actives de réparations de
compatibilité de sous-chemin et une pression de gouvernance de surface entière.
La preuve de distribution/version reste également plus mince que les chemins
internes plus forts de manifeste, découverte, exécution et approbation.

## Matrice

| Catégorie                                                           | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                                                                                           |
| ------------------------------------------------------------------ | --- | -------------- | -------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Création et empaquetage des plugins](public-sdk-api-and-subpaths.md)  | ✅  | `Beta (77%)`   | `Beta (74%)`   | `Beta (72%)`   | Point d'entrée SDK racine, Importations SDK ciblées, Découverte de point d'entrée, Shims de migration, Manifeste de plugin, Métadonnées de package, Compatibilité à l'exécution, Retours de validation |
| [Plugins groupés](bundled-plugin-discovery-and-inventory.md)       | ✅  | `Stable (86%)` | `Stable (84%)` | `Stable (88%)` | Liste des plugins groupés, Superpositions de source groupées, Plugins groupés empaquetés, Inventaire de plugin généré, ID de canal groupés                                     |
| [Plugin Canvas](canvas-plugin.md)                                  | ❌  | `Beta (76%)`   | `Alpha (66%)`  | `Beta (74%)`   | Surfaces Canvas et A2UI hébergées, Outil canvas d'agent, Commandes Canvas de nœud, Intégrations d'interface utilisateur de contrôle, Documents Canvas, Transport A2UI et snapshots                    |
| [Installation et exécution des plugins](runtime-loading-and-lifecycle.md) | ✅  | `Stable (86%)` | `Stable (84%)` | `Stable (88%)` | Configuration du plugin, Activation à l'exécution, Activation et désactivation, Échecs de chargement sécurisés, Réparation de dépendances, Installation, mise à jour et désinstallation                                      |
| [Plugins de canal](channel-plugin-architecture.md)                  | ✅  | `Stable (82%)` | `Beta (78%)`   | `Stable (80%)` | Gestion des événements entrants, Livraison sortante, Autorisation d'entrée, Résolution de destination, Invites d'approbation natives                                              |
| [Plugins fournisseur et outil](provider-tool-plugin-architecture.md)  | ✅  | `Stable (84%)` | `Stable (82%)` | `Stable (84%)` | Plugins fournisseur, Plugins outil, Catalogues de modèles, Authentification fournisseur, Recherche et récupération web, Plugins mixtes                                                             |
| [Approbations de plugins](approval-and-security-boundaries.md)            | ✅  | `Stable (84%)` | `Stable (86%)` | `Stable (86%)` | Demandes d'approbation, Livraison d'approbation native, Secours dans le même chat, Séparation exec et plugin, Protection contre la relecture d'approbation, Assistants de sécurité                     |
| [Publication de plugins](distribution-release-and-compatibility.md)    | ✅  | `Beta (79%)`   | `Stable (82%)` | `Beta (74%)`   | Sources d'installation, Publication ClawHub, Publication npm, Signalisation de compatibilité, Attentes de mise à jour et restauration, Règles de publication par tiers                  |
| [Test des plugins](developer-testing-and-fixtures.md)               | ❌  | `Stable (84%)` | `Stable (81%)` | `Stable (82%)` | Fixtures de test, Environnement de test local, Harnais d'exécution de plugin, Échafaudages unitaires et d'intégration, Suites de cycle de vie Docker, Tests de fumée                            |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, en direct ou les preuves
  de flux serveur/exécution dans la catégorie. Les tests unitaires peuvent fournir
  un contexte de support mais ne rendent jamais une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle.
  La couverture des tests unitaires, d'intégration, e2e, en direct et du flux d'exécution
  réel sont des entrées de Couverture uniquement ; elles ne relèvent ni n'abaissent la Qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre l'ensemble
  de capacités spécifiques à la surface prévue. Utilisez les instructions de complétude
  liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez
  le label de maturité plus élevé.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées
  plutôt que comme une dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Authoring and Packaging plugins

Search anchors: plugin sdk entrypoints, plugin sdk subpaths, plugin manifest, package metadata, authoring plugins, packaging plugins.

Category note: [Authoring and Packaging plugins](public-sdk-api-and-subpaths.md)

Score decisions:

- Coverage: `Beta (77%)`
- Quality: `Beta (74%)`
- Completeness: `Beta (72%)`
- LTS: ✅

Features:

- Root SDK entrypoint: Les auteurs de plugins utilisent le point d'entrée racine du SDK de plugin pris en charge lorsque le contrat de haut niveau est suffisant.
- Focused SDK imports: Les auteurs de plugins utilisent les sous-chemins du SDK de plugin ciblés au lieu de dépendre d'un seul point d'entrée global.
- Entrypoint discovery: Les auteurs de plugins découvrent les points d'entrée publics pris en charge et leur statut de support à partir de la documentation du SDK et du catalogue des points d'entrée.
- Migration shims: Les sous-chemins dépréciés ou de compatibilité continuent à se résoudre pendant les migrations des auteurs.
- Plugin manifest: `openclaw.plugin.json` déclare l'identité du plugin, les capacités et le schéma de configuration.
- Package metadata: `package.json` porte les métadonnées `openclaw` requises pour les flux de découverte et de publication.
- Runtime compatibility: Les packages de plugins déclarent la compatibilité du runtime et de l'API de plugin pris en charge.
- Validation feedback: La validation du contrat du manifeste et du package échoue rapidement sur les métadonnées mal formées ou incohérentes.

Primary docs:

- `docs/plugins/building-plugins.md`
- `docs/plugins/sdk-overview.md`
- `docs/plugins/sdk-entrypoints.md`
- `docs/plugins/sdk-subpaths.md`
- `docs/plugins/manifest.md`
- `docs/plugins/reference.md`

Major quality/completeness gaps:

- Cette catégorie porte toujours le contrat le plus large orienté vers les auteurs dans la surface, et les preuves d'archive continuent de montrer des corrections de compatibilité de sous-chemin, une pression de consolidation de surface entière et des demandes de réduction de la dispersion orientée vers les auteurs.
- Les commandes de validation les plus fortes pour cette catégorie ont été bloquées localement par des défaillances d'authentification du registre de dépendances lors de ce rescoring, il n'y a donc toujours pas de résultat de budget de surface ou de ligne de base d'API emballée pour compenser la pression d'archive.

### 2. Bundled plugins

Search anchors: bundled plugins, plugin inventory, bundled plugin metadata.

Category note: [Bundled plugins](bundled-plugin-discovery-and-inventory.md)

Score decisions:

- Coverage: `Stable (86%)`
- Quality: `Stable (84%)`
- Completeness: `Stable (88%)`
- LTS: ✅

Features:

- Bundled plugin listing: Les opérateurs et les responsables peuvent inspecter l'ensemble des plugins groupés et ses métadonnées publiées.
- Bundled source overlays: Les superpositions de source fonctionnent pour le développement local et les tests pilotés par le référentiel.
- Packaged bundled plugins: Les distributions construites découvrent les plugins groupés à partir des racines emballées.
- Generated plugin inventory: L'inventaire des plugins généré et la documentation de référence décrivent ce qui est livré dans le noyau par rapport à ce qui s'installe séparément.
- Bundled channel IDs: Les identifiants de canal groupés sont découverts et normalisés à partir des métadonnées du plugin.

Primary docs:

- `docs/plugins/plugin-inventory.md`
- `docs/cli/plugins.md`
- `docs/plugins/architecture-internals.md`

Major quality/completeness gaps:

- La découverte et l'inventaire sont forts en interne, mais l'audit n'a pas trouvé de scénario de publication de docs en direct ou de scénario ClawHub/npm en direct qui relie l'inventaire généré au comportement d'installation externe.

### 3. Canvas plugin

Search anchors: Canvas plugin, hosted canvas documents, A2UI, canvas tool, canvas node commands.

Category note: [Canvas plugin](canvas-plugin.md)

Score decisions:

- Coverage: `Beta (76%)`
- Quality: `Alpha (66%)`
- Completeness: `Beta (74%)`
- LTS: ❌

Features:

- Hosted Canvas and A2UI surfaces: Le plugin Canvas enregistre les routes HTTP et WebSocket authentifiées de la passerelle pour les documents Canvas hébergés et les surfaces de runtime A2UI.
- Agent canvas tool: Le plugin Canvas enregistre l'outil `canvas` orienté vers l'agent pour présenter, masquer, naviguer, évaluer, capturer et contrôler A2UI.
- Node Canvas commands: Le plugin Canvas possède la politique d'invocation de nœud pour les commandes `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot` et `canvas.a2ui.*`.
- Control UI embeds: La sortie de l'assistant peut intégrer les URL des documents Canvas hébergés dans les sessions Control UI et WebChat.
- Canvas documents: Le plugin Canvas matérialise les fichiers de document hébergés et les URL `/__openclaw__/canvas/documents/...`.
- A2UI transport and snapshots: Le plugin Canvas groupe le transport A2UI push, reset et JSONL avec la capture de snapshot et l'état Canvas rendu par nœud.

Primary docs:

- `docs/plugins/reference/canvas.md`
- `docs/refactor/canvas.md`
- `docs/gateway/configuration-reference.md`

Major quality/completeness gaps:

- Canvas a une couverture source/docs pour la famille de fonctionnalités, mais pas de fumée de famille entière récurrente qui prouve que les documents hébergés, les intégrations Control UI, les commandes de nœud, les snapshots et le transport A2UI fonctionnent ensemble.
- La fonctionnalité reste expérimentale et dépend de la configuration de l'hôte de la passerelle, de la disponibilité des nœuds et de l'alignement de la disponibilité des URL d'intégration/document.

### 4. Installing and running plugins

Search anchors: installing and running plugins, plugin setup, runtime activation, plugins doctor.

Category note: [Installing and running plugins](runtime-loading-and-lifecycle.md)

Score decisions:

- Coverage: `Stable (86%)`
- Quality: `Stable (84%)`
- Completeness: `Stable (88%)`
- LTS: ✅

Features:

- Plugin setup: Les opérateurs peuvent exécuter les flux de configuration des plugins sans activer complètement le comportement du runtime.
- Runtime activation: Les plugins activés s'activent et enregistrent le comportement du runtime après la validation réussie du manifeste.
- Enable and disable: Les opérateurs peuvent activer ou désactiver les plugins installés sans perdre l'état d'installation.
- Safe load failures: Les chargements de plugins non sûrs ou non pris en charge sont bloqués avec des défaillances diagnostiquables avant l'exécution du runtime.
- Dependency repair: Le runtime peut détecter et réparer les dépendances de plugins manquantes ou obsolètes.
- Install update and uninstall: Le comportement du cycle de vie d'installation, de mise à jour et de désinstallation est défini et testé.

Primary docs:

- `docs/plugins/architecture.md`
- `docs/plugins/architecture-internals.md`
- `docs/cli/plugins.md`

Major quality/completeness gaps:

- Le comportement du runtime est bien structuré, mais les opérateurs doivent toujours comprendre les lectures de métadonnées à froid, l'inspection du runtime en direct, les redémarrages de la passerelle et la réparation des dépendances comme des flux de travail distincts.

### 5. Channel plugins

Search anchors: channel plugins, sdk channel plugins, channel inbound, channel outbound.

Category note: [Channel plugins](channel-plugin-architecture.md)

Score decisions:

- Coverage: `Stable (82%)`
- Quality: `Beta (78%)`
- Completeness: `Stable (80%)`
- LTS: ✅

Features:

- Inbound event handling: Les plugins de canal enregistrent les hooks entrants et normalisent les événements entrants.
- Outbound delivery: Les adaptateurs sortants traduisent la sortie du modèle en charges utiles spécifiques au canal.
- Ingress authorization: Le runtime d'entrée de canal applique la limite d'autorisation d'entrée partagée.
- Destination resolution: La résolution de cible mappe les utilisateurs, les threads et les conversations aux destinations du canal.
- Native approval prompts: Les actions de canal natif peuvent acheminer les demandes d'approbation et les réponses via le système d'approbation.

Primary docs:

- `docs/plugins/sdk-channel-plugins.md`
- `docs/plugins/sdk-channel-inbound.md`
- `docs/plugins/sdk-channel-outbound.md`

Major quality/completeness gaps:

- L'architecture du plugin de canal est large et activement migrée ; la documentation avertit les auteurs de s'éloigner des chemins de compatibilité dépréciés tout en en conservant beaucoup pour les canaux groupés et externes existants.
- La variance de l'API/compte externe signifie que le comportement du canal a toujours besoin d'une preuve de scénario en direct répétée par canal important.

### 6. Provider and tool plugins

Search anchors: provider and tool plugins, provider plugins, tool plugins, adding capabilities.

Category note: [Provider and tool plugins](provider-tool-plugin-architecture.md)

Score decisions:

- Coverage: `Stable (84%)`
- Quality: `Stable (82%)`
- Completeness: `Stable (84%)`
- LTS: ✅

Features:

- Provider plugins: Les plugins de fournisseur enregistrent les modèles et les capacités avec le runtime.
- Tool plugins: Les plugins d'outil enregistrent les outils découvrables et les métadonnées statiques sans propriété de runtime ambiguë.
- Model catalogs: Les catalogues de modèles de fournisseur sont découvrables et fusionnent proprement dans les listes globales.
- Provider auth: La configuration d'authentification du fournisseur et la gestion des secrets sont prises en charge.
- Web search and fetch: Les plugins de fournisseur ou d'outil peuvent exposer les capacités de recherche web et de récupération.
- Mixed plugins: Les plugins mixtes de fournisseur et d'outil sont pris en charge sans propriété ambiguë.

Primary docs:

- `docs/plugins/sdk-provider-plugins.md`
- `docs/plugins/tool-plugins.md`
- `docs/plugins/adding-capabilities.md`

Major quality/completeness gaps:

- Les preuves de Gitcrawl montrent des corrections et des migrations actives autour du routage de recherche web, de la propagation du catalogue/authentification du modèle, des refroidissements du fournisseur et de la dispersion de la surface de l'auteur du SDK.
- Les plugins mixtes fournisseur+outil nécessitent toujours une connaissance de niveau inférieur que les plugins d'outil simples.

### 7. Plugin approvals

Search anchors: plugin approvals, plugin permission requests, exec approvals.

Category note: [Plugin approvals](approval-and-security-boundaries.md)

Score decisions:

- Coverage: `Stable (84%)`
- Quality: `Stable (86%)`
- Completeness: `Stable (86%)`
- LTS: ✅

Features:

- Approval requests: Les actions initiées par le plugin peuvent demander et résoudre les approbations via le flux standard.
- Native approval delivery: Les actions de plugin privilégiées peuvent acheminer les approbations via les invites natives du canal et les réponses.
- Same-chat fallbacks: La livraison d'approbation peut revenir aux avis d'autorisation du même chat lorsque le routage natif n'est pas disponible.
- Exec and plugin separation: Les approbations Exec restent distinctes des chemins d'approbation des plugins et des relais de permission natifs.
- Approval replay protection: Les décisions d'approbation restent limitées à la demande d'origine, à la cible et à la liaison de l'appareil ou du nœud.
- Security helpers: Les exportations d'aide à la sécurité fournissent des primitives approuvées sans élargir les limites de confiance.

Primary docs:

- `docs/plugins/plugin-permission-requests.md`
- `docs/tools/exec-approvals.md`
- `docs/plugins/sdk-channel-plugins.md`

Major quality/completeness gaps:

- Le modèle de limite s'étend sur plusieurs pages de documentation et packages de runtime.
- L'audit a trouvé une preuve locale/runtime forte, mais pas de preuve de transcription de canal externe en direct pour les chemins d'approbation natifs dans l'archive Discrawl vide.

### 8. Publishing plugins

Search anchors: publishing plugins, clawhub publishing, npm publishing, plugin compatibility.

Category note: [Publishing plugins](distribution-release-and-compatibility.md)

Score decisions:

- Coverage: `Beta (79%)`
- Quality: `Stable (82%)`
- Completeness: `Beta (74%)`
- LTS: ✅

Features:

- Install sources: Les sources d'installation de plugins prises en charge sont explicites et validées.
- ClawHub publishing: Les métadonnées et les flux de travail des plugins prennent en charge la publication sur ClawHub.
- npm publishing: Les métadonnées et les flux de travail des plugins prennent en charge la publication sur npm le cas échéant.
- Compatibility signaling: Les données du registre de compatibilité mappent les plugins aux versions ou canaux de runtime pris en charge.
- Update and rollback expectations: La sémantique de mise à jour des plugins définit ce qui peut être mis à niveau sur place et ce qui nécessite une intervention de l'opérateur.
- Third-party publication rules: Les règles d'acceptation des packages externes contrôlent l'emballage et la publication des plugins tiers.

Primary docs:

- `docs/cli/plugins.md`
- `docs/plugins/compatibility.md`
- `docs/clawhub/publishing.md`

Major quality/completeness gaps:

- La couverture reste Beta car la preuve la plus forte est locale et basée sur Docker ; les cartes de pointage du cycle de vie externe pour l'installation, la confiance, la mise à jour, la restauration et la compatibilité sont toujours plus faibles que les vérifications de publication internes.

### 9. Testing plugins

Search anchors: testing plugins, sdk testing, plugin test fixtures, codex harness.

Category note: [Testing plugins](developer-testing-and-fixtures.md)

Score decisions:

- Coverage: `Stable (84%)`
- Quality: `Stable (81%)`
- Completeness: `Stable (82%)`
- LTS: ❌

Features:

- Test fixtures: Les fixtures fournissent des métadonnées de plugin réutilisables et des entrées de test de runtime.
- Local test environment: Les auteurs de plugins peuvent configurer l'environnement de test local et la configuration d'aide limitée pour les tests de plugins.
- Plugin runtime harness: Les harnais de test de plugins couvrent les chemins d'intégration de création et de runtime.
- Unit and integration scaffolds: Les aides de test limitées et la configuration prennent en charge les tests unitaires et d'intégration pour les surfaces de plugins.
- Docker lifecycle suites: Les scripts de bout en bout basés sur Docker valident les flux de cycle de vie des plugins emballés.
- Smoke tests: Les tests de fumée locaux et emballés détectent les installations cassées avant la publication.

Primary docs:

- `docs/plugins/sdk-testing.md`
- `docs/plugins/sdk-setup.md`
- `docs/plugins/codex-harness.md`

Major quality/completeness gaps:

- Les conseils du harnais de test sont utiles mais denses, et les auteurs doivent toujours mapper le chemin de preuve local, de package, Docker et en direct approprié à leur type de plugin.

## Interprétation recommandée de la fiche d'évaluation

Maintenez la ligne de fiche d'évaluation publique à `M3 Beta` jusqu'à ce que la surface de l'API/sous-chemin du SDK public soit réparée et que la preuve du cycle de vie des plugins externes soit plus régulière. Les cumuls de catégories sont suffisamment élevés pour justifier un langage « bêta vers stable », mais une surface dont la limite de l'API publique obtient toujours un score `Beta (74%)` en Qualité ne doit pas être présentée comme entièrement Stable pour les auteurs externes normaux.

Les critères de promotion suivants doivent être concrets :

- faire passer les vérifications de base de la surface/API du SDK à partir de `main` actuel ;
- publier une petite fiche d'évaluation de compatibilité pour l'installation, la mise à jour, la restauration et le comportement de l'inspecteur des plugins externes ;
- ajouter une preuve récurrente en direct ou de test de fumée de version pour au moins un plugin de canal, un plugin de fournisseur et un plugin mixte fournisseur+outil ;
- maintenir les requêtes d'archive Gitcrawl et Discrawl dans les notes de catégorie à jour avant tout changement de cumul futur.

## Hors du champ d'application de cette surface

- Scores de maturité individuels pour chaque plugin de canal, fournisseur ou outil fourni.
- La ligne de fiche d'évaluation `ClawHub` séparée, sauf
où la compatibilité d'installation/version affecte directement l'architecture du SDK Plugin.
- Maturité générale de l'authentification Gateway, de la session, de la mémoire, de l'exécution du fournisseur et du framework de canal en dehors des contrats appartenant aux plugins.

## Provenance de l'audit

- Source de la fiche d'évaluation :
`docs/kevinslin/maturity-scorecard/maturity-scorecard.md`, ligne `Plugin SDK
and bundled plugin architecture`.
- Source du score de fonctionnalité :
`docs/kevinslin/maturity-scorecard/inventory/plugin-sdk-and-bundled-plugin-architecture/scores.yaml`.
- Racine de sortie :
`docs/kevinslin/maturity-scorecard/inventory/plugin-sdk-and-bundled-plugin-architecture/`.
- Extraction de source OpenClaw :
`/Users/kevinlin/code/openclaw` à `b877fc58a5c5 refactor: centralize numeric
coercion helpers`.
- Extraction de la maintenance :
`/Users/kevinlin/code/claw/maintainers` à `2ac4ebe4d3be Enhance
claw-score documentation and validation commands for maturity scoring`.
- Fraîcheur de Gitcrawl :
`gitcrawl doctor --json` a réussi après la synchronisation ; `last_sync_at`
`2026-05-28T19:09:52.784704Z` ; `thread_count` `29810` ;
`open_thread_count` `11181` ; `db_path`
`/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db` ;
`version` `0.2.1`.
- Fraîcheur de Discrawl :
`discrawl status --json` généré à `2026-05-30T00:38:20Z`, a signalé
`state` `current`, résumé `1487536 messages across 25831 channels`, et
`last_sync_at` `2026-05-29T19:27:40Z`.
- Interprétation de l'archive :
Les recherches Gitcrawl sont traitées comme des preuves GitHub actuelles sauvegardées par archive.
Les recherches Discrawl sont des preuves Discord spécifiques aux fonctionnalités lorsque la recherche locale réussit ; lorsqu'une requête est bloquée localement, cela est enregistré comme une lacune environnementale plutôt que traité comme un signal de produit.
