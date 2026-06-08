---
title: Rapport de Maturité CLI
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité CLI

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Stable (83%)`
- Qualité : `Beta (72%)`
- Complétude : `Stable (80%)`
- Fonctionnalités LTS : `6/7`

## Résumé

Ce rapport développe la surface de scorecard nommée « CLI » en capacités
concrètes orientées opérateur qui font fonctionner en pratique la configuration,
la réparation et la gestion du cycle de vie d'OpenClaw.

La surface CLI dispose d'une documentation complète et d'une large empreinte
d'implémentation/test. La couverture est généralement forte dans les flux
d'installation, d'intégration, de diagnostic et de mise à jour. Le principal
frein à la qualité provient des chemins de gestion de service et de mise à jour,
où le comportement de redémarrage, les superviseurs spécifiques à la plateforme
et les secours de service produisent toujours des problèmes récurrents pour les
opérateurs.

## Matrice

| Catégorie                                                                  | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                  |
| -------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Configuration CLI](package-install-and-cli-entrypoints.md)                | ✅  | `Beta (78%)`   | `Beta (75%)`  | `Stable (84%)` | Scripts d'installation, Installation avec préfixe local, Installations via gestionnaire de paquets, Runtime Node supporté, Installation à partir du code source, Point d'entrée CLI                                                         |
| [Intégration et Configuration Auth](first-run-onboarding-and-auth-selection.md)   | ✅  | `Stable (86%)` | `Beta (78%)`  | `Stable (80%)` | Intégration guidée, Reconfiguration ciblée, Choix d'authentification, Stockage d'authentification Gateway, Intégration à distance                                                                                                           |
| [Configuration Plugin et Canal](plugin-and-channel-setup-during-onboarding.md) | ❌  | `Stable (82%)` | `Beta (72%)`  | `Beta (76%)`   | Sélecteur de canal, Sources d'installation de plugin, Configuration de compte de canal, Sondes post-configuration, Caveat de passerelle distante                                                                                            |
| [Gestion du Service Gateway](gateway-service-install-and-lifecycle.md)    | ✅  | `Stable (88%)` | `Alpha (66%)` | `Stable (84%)` | Exécutions de gateway au premier plan, Installation et contrôle du service, Câblage d'authentification du service, Récupération de dérive et réinstallation, Vérifications de santé du service                                             |
| [Observabilité CLI](status-health-logs-and-diagnostics-support-path.md)   | ✅  | `Stable (84%)` | `Beta (74%)`  | `Stable (84%)` | Snapshots d'état, Snapshots de santé, Suivi des journaux à distance, Export de diagnostics, Rédaction sûre pour le support                                                                                                                |
| [Doctor](doctor-config-auth-plugin-and-lint.md)                           | ✅  | `Stable (80%)` | `Alpha (68%)` | `Beta (77%)`   | Réparation interactive, Migration de configuration, Vérifications d'authentification et SecretRef, Validation et réparation de plugin, Résultats Lint et JSON, Découverte de gateway supplémentaire, Réparation de dérive de superviseur, Diagnostic de port et de démarrage, Vérifications de chemin d'exécution, Conseils de redémarrage |
| [Mises à Jour et Upgrades](update-channel-and-core-upgrade-flow.md)           | ✅  | `Stable (82%)` | `Alpha (68%)` | `Beta (78%)`   | Canaux de mise à jour, Changement de type d'installation, Redémarrage de gateway géré, État de mise à jour et RPC, Convergence de plugin                                                                                                   |

## Rubrique de notation

- Couverture :
  notation maturity-label pour l'intégration, e2e, live ou les preuves de flux
  serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un
  contexte de support mais ne rendent jamais une fonctionnalité couverte par
  eux-mêmes.
- Qualité :
  notation maturity-label pour la robustesse de l'implémentation et
  opérationnelle. La couverture des tests unitaires, d'intégration, e2e, live
  et de flux runtime réel sont des entrées de Couverture uniquement ; elles ne
  relèvent ni n'abaissent la Qualité.
- Complétude :
  notation maturity-label pour la complétude avec laquelle la catégorie
  fournit l'ensemble de capacités spécifiques à la surface prévu. Utilisez les
  instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez
  le libellé de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités
  détaillées plutôt que comme dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration CLI

Ancres de recherche : cli install, update, onboard, doctor cli installation and launch, cli installation and launch, cli install, update, onboard, doctor runtime prerequisites, runtime prerequisites.

Note de catégorie : [Configuration CLI](package-install-and-cli-entrypoints.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (75%)`
- Complétude : `Stable (84%)`
- LTS : ✅

Fonctionnalités :

- Scripts d'installation : Les scripts d'installation hébergés configurent Node, installent OpenClaw et démarrent optionnellement l'intégration.
- Installation avec préfixe local : L'installateur avec préfixe local conserve Node et OpenClaw dans un répertoire OpenClaw dédié au lieu de dépendre d'un runtime système.
- Installations via gestionnaire de paquets : Les installations globales npm, pnpm et bun sont prises en charge lorsque l'opérateur gère Node directement, y compris les attentes de câblage PATH.
- Runtime Node pris en charge : OpenClaw documente les versions Node prises en charge et le runtime recommandé avant que les flux de travail CLI normaux ne se poursuivent.
- Installation à partir d'une extraction source : Les opérateurs peuvent exécuter OpenClaw à partir d'une extraction source pour les flux de travail de développement ou de récupération, et les flux de mise à jour distinguent ce chemin des installations de paquets.
- Point d'entrée CLI : Le lanceur openclaw empaqueté, openclaw --help, openclaw --version, la vérification préalable du runtime et les attentes de récupération de base sont documentés.

Documentation principale :

- `docs/install/index.md`
- `docs/install/installer.md`
- `docs/install/node.md`
- `docs/install/updating.md`

Lacunes majeures en qualité/complétude :

- Les scripts d'installation hébergés manquent encore de preuve e2e locale au référentiel.

### 2. Intégration et configuration d'authentification

Ancres de recherche : cli install, update, onboard, doctor onboarding and auth setup, onboarding and auth setup.

Note de catégorie : [Intégration et configuration d'authentification](first-run-onboarding-and-auth-selection.md)

Décisions de score :

- Couverture : `Stable (86%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (80%)`
- LTS : ✅

Fonctionnalités :

- Intégration guidée : openclaw onboard guide l'opérateur à travers l'espace de travail, la passerelle, l'authentification du modèle, les canaux, les compétences et la configuration de la santé.
- Reconfiguration ciblée : openclaw configure permet aux opérateurs de revisiter uniquement les sections qu'ils souhaitent modifier après la configuration initiale.
- Choix d'authentification : L'intégration et la configuration prennent en charge les choix d'authentification par clé API, OAuth et autres spécifiques au fournisseur.
- Stockage d'authentification de passerelle : La configuration du jeton de passerelle et du mot de passe sont documentées, y compris le comportement de stockage géré par SecretRef.
- Intégration à distance : L'intégration de passerelle à distance documente ce qui est configuré localement par rapport à ce qui doit déjà exister sur l'hôte distant.

Documentation principale :

- `docs/cli/onboard.md`
- `docs/cli/configure.md`
- `docs/start/onboarding-overview.md`

### 3. Configuration des plugins et des canaux

Ancres de recherche : cli install, update, onboard, doctor plugin and channel setup, plugin and channel setup.

Note de catégorie : [Configuration des plugins et des canaux](plugin-and-channel-setup-during-onboarding.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Sélecteur de canaux : L'intégration peut guider l'opérateur dans le choix des canaux à configurer.
- Sources d'installation de plugins : La configuration des plugins prend en charge les sources d'installation groupées, npm, ClawHub, marketplace, git et locales.
- Configuration de compte de canal : Les commandes de canal prennent en charge la configuration de compte interactive et basée sur des drapeaux pour les transports de chat pris en charge.
- Sondes post-configuration : Les opérateurs peuvent sonder l'état et les capacités du canal après la configuration pour vérifier que le compte configuré fonctionne.
- Avertissement de passerelle à distance : L'intégration à distance documente que l'installation de plugins ne se produit pas localement lorsque la passerelle s'exécute ailleurs.

Documentation principale :

- `docs/cli/onboard.md`
- `docs/cli/plugins.md`
- `docs/cli/channels.md`

### 4. Gestion du service de passerelle

Ancres de recherche : cli install, update, onboard, doctor gateway service management, gateway service management.

Note de catégorie : [Gestion du service de passerelle](gateway-service-install-and-lifecycle.md)

Décisions de score :

- Couverture : `Stable (88%)`
- Qualité : `Alpha (66%)`
- Complétude : `Stable (84%)`
- LTS : ✅

Fonctionnalités :

- Exécutions de passerelle au premier plan : Les opérateurs peuvent exécuter la passerelle directement à partir de la CLI pour le développement local ou la récupération ad hoc.
- Installation et contrôle du service : La CLI documente les flux d'installation, de statut, de démarrage, d'arrêt, de redémarrage et d'exécution pour les services de passerelle gérés.
- Câblage d'authentification du service : L'installation du service de passerelle documente comment les jetons d'authentification et autres valeurs sensibles sont gérés.
- Récupération de dérive et de réinstallation : Les opérateurs reçoivent des conseils explicites pour réparer ou réinstaller un service de passerelle géré cassé.
- Vérifications de santé du service : Les flux de service de passerelle pointent les opérateurs vers les vérifications de santé et de dépannage du runtime après l'installation ou le redémarrage.

Documentation principale :

- `docs/cli/gateway.md`
- `docs/install/updating.md`
- `docs/gateway/troubleshooting.md`

### 5. Observabilité CLI

Ancres de recherche : cli install, update, onboard, doctor status health logs and diagnostics, status health logs and diagnostics.

Note de catégorie : [Observabilité CLI](status-health-logs-and-diagnostics-support-path.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Beta (74%)`
- Complétude : `Stable (84%)`
- LTS : ✅

Fonctionnalités :

- Instantanés de statut : openclaw status et les drapeaux associés résument l'état du runtime, la santé de la configuration et le contexte de mise à jour.
- Instantanés de santé : openclaw health donne une lecture rapide de la santé de la passerelle et prend en charge la sortie détaillée ou JSON.
- Suivi des journaux à distance : openclaw logs suit les journaux de passerelle sur RPC, y compris le mode de suivi et la sortie JSON.
- Export de diagnostics : Les bundles de diagnostics de passerelle peuvent être exportés localement pour les rapports de bogues et les flux de travail de support.
- Rédaction sûre pour le support : Les chemins de diagnostics et de statut documentent les attentes de confidentialité et de rédaction avant de partager les résultats.

Documentation principale :

- `docs/cli/status.md`
- `docs/cli/health.md`
- `docs/cli/logs.md`
- `docs/gateway/diagnostics.md`

### 6. Docteur

Ancres de recherche : cli install, update, onboard, doctor doctor config and policy repair, doctor config and policy repair, cli install, update, onboard, doctor doctor platform and service repair, doctor platform and service repair.

Note de catégorie : [Docteur](doctor-config-auth-plugin-and-lint.md)

Décisions de score :

- Couverture : `Stable (80%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (77%)`
- LTS : ✅

Fonctionnalités :

- Réparation interactive : openclaw doctor prend en charge les postures d'inspection, de réparation, non-interactive et de réparation forcée.
- Migration de configuration : Doctor réécrit la configuration héritée ou endommagée et l'état dans les formats actuels pris en charge.
- Vérifications d'authentification et de SecretRef : Doctor audite la forme d'authentification, la génération de jetons et les chemins de configuration pris en charge par SecretRef.
- Validation et réparation de plugins : Doctor met en surface les problèmes de configuration de plugins et la dérive de schéma d'extension qui bloquent le fonctionnement normal du runtime.
- Résultats Lint et JSON : openclaw doctor --lint --json fournit des résultats stables lisibles par machine pour l'automatisation.
- Découverte de passerelle supplémentaire : Doctor peut analyser les services de passerelle inattendus et les installations conflictuelles.
- Réparation de dérive du superviseur : Doctor vérifie les définitions de service gérées et peut réparer la dérive launchd, systemd ou Scheduled Task.
- Diagnostic de port et de démarrage : Doctor pointe les opérateurs vers les conflits de port, les échecs de redémarrage et les erreurs récentes de passerelle.
- Vérifications du chemin d'exécution : Doctor vérifie les meilleures pratiques du chemin d'exécution et les erreurs de configuration de chemin courantes.
- Conseils de redémarrage : Doctor explique quand un problème de santé nécessite un redémarrage ou un chemin de réparation de service plus profond.

Documentation principale :

- `docs/cli/doctor.md`
- `docs/gateway/doctor.md`
- `docs/gateway/secrets.md`
- `docs/gateway/troubleshooting.md`

### 7. Mises à jour et mises à niveau

Ancres de recherche : cli install, update, onboard, doctor updates and upgrades, updates and upgrades.

Note de catégorie : [Mises à jour et mises à niveau](update-channel-and-core-upgrade-flow.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Canaux de mise à jour : openclaw update prend en charge la sélection de canal stable, bêta et dev.
- Changement de type d'installation : Les flux de mise à jour peuvent basculer entre les installations de paquets et les installations git/source lorsqu'elles sont prises en charge.
- Redémarrage de passerelle géré : Les flux de mise à jour documentent quand la passerelle gérée est arrêtée, redémarrée ou intentionnellement laissée seule.
- Statut de mise à jour et RPC : Les opérateurs peuvent inspecter l'état de mise à jour et l'état du plan de contrôle de passerelle associé.
- Convergence des plugins : Les mises à jour principales documentent comment les versions de plugins et les avertissements de réparation de plugins sont gérés par la suite.

Documentation principale :

- `docs/install/updating.md`
- `docs/cli/update.md`
- `docs/gateway/troubleshooting.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez la ligne CLI comme signal de préparation de l'opérateur pondéré plutôt que de supposer que chaque sous-chemin est également solide. L'installation locale, l'intégration et les diagnostics orientés vers la lecture sont en meilleure forme que la réparation de service multiplateforme et les chemins de redémarrage gérés par mise à jour.

## Hors du champ d'application de cette surface

- Sémantique du protocole d'exécution de passerelle au-delà des crochets CLI orientés vers l'opérateur.
- Création du SDK de plugin et détails d'architecture de plugin en dehors des flux de configuration et de réparation CLI.
- Comportement du runtime de canal après la réussite de la configuration.

## Provenance de l'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/cli-install-update-onboard-doctor/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
