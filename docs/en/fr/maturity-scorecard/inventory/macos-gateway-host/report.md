---
title: "Rapport de maturité de l'hôte macOS Gateway"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité de l'hôte macOS Gateway

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (75%)`
- Qualité : `Beta (79%)`
- Complétude : `Beta (75%)`
- Fonctionnalités LTS : `0/7`

## Résumé

Ce rapport promeut les preuves de maturité archivées `macos-gateway-host` de `/Users/kevinlin/tmp/maturity/macos-gateway-host` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                             | LTS | Couverture     | Qualité        | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------- | --- | -------------- | -------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration CLI](cli-install-runtime-prerequisites.md)                             | ❌  | `Stable (82%)` | `Beta (76%)`   | `Stable (82%)` | Programme d'installation hébergé, recommandation Node 24, Installation CLI déclenchée par l'application, Dérive PATH du shell et gestionnaire de versions                                                                                                                                       |
| [Intégration Gateway locale](local-gateway-mode-host-configuration.md)                | ❌  | `Beta (76%)`   | `Stable (82%)` | `Beta (76%)`   | Mode de connexion Gateway local/distant de l'application, Installation/redémarrage/désinstallation de LaunchAgent Gateway gérée par l'application, Détection d'installation CLI, Compatibilité Gateway existant, Point de terminaison Gateway, Configuration gateway.mode=local, Liaison de bouclage, Résolution de point de terminaison d'application locale, Découverte Bonjour |
| [Mode Gateway distant](remote-gateway-mode-transport.md)                              | ❌  | `Beta (72%)`   | `Stable (82%)` | `Beta (72%)`   | Application macOS « Gateway distant sur SSH », Configuration du tunnel SSH, Tailscale MagicDNS, Jeton/mot de passe/empreinte TLS du point de terminaison distant, Démarrage du nœud hôte local                                                                                                |
| [Cycle de vie du service Gateway](launchagent-service-lifecycle.md)                   | ❌  | `Stable (82%)` | `Beta (76%)`   | `Stable (82%)` | Installation de LaunchAgent Gateway par utilisateur, amorçage launchctl, Étiquettes LaunchAgent, Gestion des jetons/env Gateway, Transfert de LaunchAgent géré par l'application, Transfert de paquet openclaw update/git, Actualisation du service géré, Détection de tâche launchd de mise à jour obsolète, Désinstallation openclaw, Récupération de service orphelin |
| [Diagnostics et observabilité](diagnostics-logs-operator-observability.md)            | ❌  | `Stable (80%)` | `Stable (83%)` | `Stable (80%)` | Chemins de journal LaunchAgent, openclaw gateway status --deep, Gateway cesse silencieusement de répondre, Tâches de mise à jour obsolètes                                                                                                                                                    |
| [Permissions et capacités natives](macos-permissions-native-node-capabilities.md)     | ❌  | `Alpha (62%)`  | `Beta (73%)`   | `Alpha (62%)`  | Invites de permission TCC macOS/statut, Exposition de capacité de nœud native, Politique system.run, Support piloté par les permissions                                                                                                                                                       |
| [Profils et isolation](profiles-multi-gateway-isolation.md)                           | ❌  | `Beta (74%)`   | `Stable (82%)` | `Beta (74%)`   | Étiquettes LaunchAgent spécifiques au profil, Racines d'état/config/espace de travail spécifiques au profil, Ports dérivés, Configuration du bot de secours, Détection de processus Gateway supplémentaire                                                                                     |

## Barème de notation

- Couverture :
  notation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les
  preuves de flux de serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais une
  fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture uniquement ; elles ne
  augmentent ni ne diminuent la qualité.
- Complétude :
  notation de l'étiquette de maturité pour la façon dont la catégorie fournit complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette
  surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité
  supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration CLI

Ancres de recherche : macos gateway host macos cli install and runtime prerequisites, macos cli install and runtime prerequisites.

Note de catégorie : [Configuration CLI](cli-install-runtime-prerequisites.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (76%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Programme d'installation hébergé : Programme d'installation hébergé et chemins d'installation avec préfixe local sur macOS
- Recommandation Node 24 : Recommandation Node 24 et compatibilité plancher Node 22.19+
- Installation CLI déclenchée par l'application : Installation CLI déclenchée par l'application et découverte du runtime
- Dérive du PATH shell et du gestionnaire de versions : Dérive du PATH shell, du gestionnaire de paquets et du gestionnaire de versions qui affectent la passerelle hôte.

Documentation principale :

- `docs/platforms/macos.md`
- `docs/platforms/mac/bundled-gateway.md`
- `docs/install/installer.md`
- `docs/install/node.md`

### 2. Intégration de la passerelle locale

Ancres de recherche : macos gateway host companion app gateway integration, companion app gateway integration, macos gateway host local gateway mode and host configuration, local gateway mode and host configuration.

Note de catégorie : [Intégration de la passerelle locale](local-gateway-mode-host-configuration.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Stable (82%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Mode de connexion local/distant de l'application : Coordination du mode de connexion local/distant de l'application
- Installation/redémarrage/désinstallation de LaunchAgent géré par l'application : Installation/redémarrage/désinstallation de LaunchAgent géré par l'application via la CLI
- Détection d'installation CLI : Détection d'installation CLI et invite d'installation d'application
- Compatibilité d'attachement à une passerelle locale existante : Vérifications de compatibilité d'attachement à une passerelle locale existante
- Résolution du point de terminaison de la passerelle : Résolution du point de terminaison, des identifiants et du canal de contrôle de la passerelle
- Configuration gateway.mode=local : Configuration gateway.mode=local et définition par défaut lors de l'installation du service
- Liaison de boucle locale : Liaison de boucle locale, remplacements explicites d'hôte/liaison, exigences d'authentification et précédence des ports
- Résolution du point de terminaison local de l'application : Résolution du point de terminaison local de l'application, canal de contrôle local et comportement d'attachement à une passerelle existante
- Découverte Bonjour : Découverte Bonjour et surfaces de statut/sonde/santé locales

Documentation principale :

- `docs/platforms/macos.md`
- `docs/platforms/mac/bundled-gateway.md`
- `docs/platforms/mac/remote.md`
- `docs/gateway/index.md`
- `docs/cli/gateway.md`
- `docs/gateway/bonjour.md`

### 3. Mode passerelle distante

Ancres de recherche : macos gateway host remote gateway mode and transport, remote gateway mode and transport.

Note de catégorie : [Mode passerelle distante](remote-gateway-mode-transport.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Stable (82%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Application macOS « Distant via SSH » : Modes de passerelle distante « Distant via SSH » et direct de l'application macOS
- Configuration du tunnel SSH : Configuration du tunnel SSH, propriété de transfert local stable et redémarrage/backoff du tunnel
- Tailscale MagicDNS : Tailscale MagicDNS, Serve et Funnel pour l'accès distant
- Résolution du jeton/mot de passe/empreinte TLS du point de terminaison distant : Résolution du jeton, du mot de passe et de l'empreinte TLS du point de terminaison distant
- Démarrage du nœud hôte local : Démarrage du nœud hôte local et suppression de la passerelle locale pendant que l'application est distante

Documentation principale :

- `docs/platforms/mac/remote.md`
- `docs/gateway/remote.md`
- `docs/gateway/tailscale.md`

### 4. Cycle de vie du service de passerelle

Ancres de recherche : macos gateway host launchagent service lifecycle, launchagent service lifecycle, macos gateway host update, uninstall, and recovery, update, uninstall, and recovery.

Note de catégorie : [Cycle de vie du service de passerelle](launchagent-service-lifecycle.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (76%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Installation de LaunchAgent par utilisateur : Installation, mise en scène, désinstallation, démarrage, arrêt, redémarrage et statut de LaunchAgent par utilisateur
- launchctl bootstrap : launchctl bootstrap, bootout, enable, disable, kickstart, analyse du runtime, réparation des installations non chargées et sémantique --disable
- Étiquettes LaunchAgent : Étiquettes LaunchAgent, étiquettes de profil, nettoyage hérité, métadonnées de service, génération plist, KeepAlive, RunAtLoad, journaux, répertoire de travail et gestion du répertoire temporaire
- Gestion des jetons/env de passerelle : Gestion des jetons/env de passerelle, fichiers/wrappers env réservés au propriétaire, clés env de service gérées et sortie d'audit/statut de configuration
- Remise de LaunchAgent gérée par l'application : Intégration d'application macOS qui gère le LaunchAgent de passerelle en mode local et l'évite en modes distant ou d'attachement uniquement.
- Remise de paquet/git de mise à jour openclaw : Remise de paquet/git de mise à jour openclaw sur macOS
- Actualisation du service géré : Actualisation du service géré et réamorçage de LaunchAgent après les mises à jour
- Détection de tâche launchd de mise à jour obsolète : Détection et nettoyage de tâche launchd de mise à jour obsolète
- Désinstallation openclaw : Désinstallation openclaw, désinstallation du service, nettoyage d'état et suppression manuelle de launchd
- Récupération du service bloqué : Récupération après des services de passerelle macOS partiellement mis à jour ou bloqués.

Documentation principale :

- `docs/platforms/macos.md`
- `docs/platforms/mac/bundled-gateway.md`
- `docs/cli/gateway.md`
- `docs/gateway/index.md`
- `docs/cli/update.md`
- `docs/install/updating.md`
- `docs/install/uninstall.md`
- `docs/gateway/troubleshooting.md`

### 5. Diagnostics et observabilité

Ancres de recherche : macos gateway host diagnostics, logs, and operator observability, diagnostics, logs, and operator observability.

Note de catégorie : [Diagnostics et observabilité](diagnostics-logs-operator-observability.md)

Décisions de score :

- Couverture : `Stable (80%)`
- Qualité : `Stable (83%)`
- Complétude : `Stable (80%)`
- LTS : ❌

Fonctionnalités :

- Chemins de journaux LaunchAgent : Chemins de journaux LaunchAgent et chemins de journaux de diagnostic d'application
- openclaw gateway status --deep : openclaw gateway status --deep, sonde de passerelle, commandes doctor, health et logs
- La passerelle cesse silencieusement de répondre : La passerelle cesse silencieusement de répondre, défaillance ENETDOWN veille/réveil, conflits de ports, configuration invalide et runbooks de pression mémoire
- Tâches de mise à jour obsolètes : Tâches de mise à jour obsolètes, dérive de configuration de service et diagnostics d'environnement LaunchAgent

Documentation principale :

- `docs/platforms/mac/bundled-gateway.md`
- `docs/platforms/macos.md`
- `docs/cli/gateway.md`
- `docs/gateway/doctor.md`
- `docs/gateway/troubleshooting.md`

### 6. Permissions et capacités natives

Ancres de recherche : macos gateway host macos permissions and native node capabilities, macos permissions and native node capabilities.

Note de catégorie : [Permissions et capacités natives](macos-permissions-native-node-capabilities.md)

Décisions de score :

- Couverture : `Alpha (62%)`
- Qualité : `Beta (73%)`
- Complétude : `Alpha (62%)`
- LTS : ❌

Fonctionnalités :

- Invites/statut de permission TCC macOS : Invites et statut de permission TCC macOS pour Accessibilité, AppleScript, Enregistrement d'écran, Microphone, Reconnaissance vocale, Caméra, Localisation, Notifications et Activation vocale
- Exposition des capacités de nœud natif : Exposition des capacités de nœud natif pour les opérations d'écran/canevas/navigateur/système
- Politique system.run : Politique system.run et attentes d'exécution de nœud local/distant
- Support piloté par les permissions : Support piloté par les permissions et diagnostics d'opérateur

Documentation principale :

- `docs/platforms/macos.md`
- `docs/platforms/mac/remote.md`

### 7. Profils et isolation

Ancres de recherche : macos gateway host profiles and multi-gateway isolation, profiles and multi-gateway isolation.

Note de catégorie : [Profils et isolation](profiles-multi-gateway-isolation.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Stable (82%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Étiquettes LaunchAgent spécifiques au profil : Étiquettes LaunchAgent spécifiques au profil et chemins plist
- Racines d'état/config/espace de travail spécifiques au profil : Racines d'état, de configuration et d'espace de travail spécifiques au profil pour les passerelles locales isolées.
- Ports dérivés : Ports dérivés et évitement de conflits multi-passerelle
- Configuration du bot de secours : Configuration du bot de secours et vérifications d'opérateur
- Détection de processus de passerelle supplémentaire : Détection de statut profond pour les services de type passerelle supplémentaires et les processus locaux en double.

Documentation principale :

- `docs/gateway/multiple-gateways.md`
- `docs/gateway/index.md`
- `docs/cli/gateway.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/macos-gateway-host/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuve archivée :
  `/Users/kevinlin/tmp/maturity/macos-gateway-host`.
