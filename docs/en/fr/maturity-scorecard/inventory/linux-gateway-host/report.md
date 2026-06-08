---
title: "Rapport de maturité de l'hôte Linux Gateway"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité de l'hôte Linux Gateway

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Stable (80%)`
- Qualité : `Beta (76%)`
- Complétude : `Stable (80%)`
- Fonctionnalités LTS : `4/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `linux-gateway-host` de `/Users/kevinlin/tmp/maturity/linux-gateway-host` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité de catégorie proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                                 | LTS | Couverture     | Qualité      | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                   |
| ---------------------------------------------------------------------------------------- | --- | -------------- | ------------ | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration de l'hôte et mises à jour](linux-cli-install-and-update-path.md)           | ✅  | `Stable (82%)` | `Beta (78%)` | `Stable (82%)` | Installation de Linux CLI, prérequis du runtime Node, politique du gestionnaire de paquets, chemin de mise à jour                                                                                           |
| [Runtime Gateway et contrôle des services](foreground-gateway-runtime-and-process-control.md) | ✅  | `Stable (83%)` | `Beta (78%)` | `Stable (83%)` | Runtime Gateway au premier plan, contrôle des processus, configuration du cycle de vie du service utilisateur Systemd, opération du cycle de vie du service utilisateur Systemd, statut du cycle de vie du service utilisateur Systemd, récupération du cycle de vie du service utilisateur Systemd |
| [Accès à distance et sécurité](remote-network-exposure-tls-and-tailscale.md)               | ✅  | `Beta (78%)`   | `Beta (74%)` | `Beta (78%)`   | Exposition du réseau distant, TLS, Tailscale, protections d'exposition Gateway, modes d'authentification Gateway, gestion des secrets                                                                         |
| [Diagnostics et réparation](diagnostics-logs-doctor-and-repair.md)                          | ✅  | `Stable (82%)` | `Beta (78%)` | `Stable (82%)` | Rapports de diagnostic Gateway, suivi des journaux Gateway, vérifications Doctor, conseils de réparation pour l'opérateur                                                                                    |
| [Cibles de déploiement](vps-container-and-cloud-deployment-guidance.md)                     | ❌  | `Beta (76%)`   | `Beta (72%)` | `Beta (76%)`   | VPS, conteneur, conseils de déploiement cloud                                                                                                                                                                |

## Barème de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture uniquement ; ils
  ne font pas augmenter ou diminuer la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la complétude avec laquelle la catégorie fournit l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration de l'hôte et mises à jour

Ancres de recherche : installation Linux, prérequis du runtime Node, politique du gestionnaire de paquets, mise à jour d'OpenClaw.

Note de catégorie : [Configuration de l'hôte et mises à jour](linux-cli-install-and-update-path.md)

Décisions de notation :

- Couverture : `Stable (82%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Installation de Linux CLI : chemins d'installation de Linux CLI et vérification de l'opérateur après l'installation.
- Prérequis du runtime Node : exigences de version du runtime Node et vérifications des prérequis de l'hôte pour le fonctionnement de Linux Gateway.
- Politique du gestionnaire de paquets : politique du gestionnaire de paquets et de la plateforme prise en charge pour les chemins d'installation et de mise à jour de Linux.
- Chemin de mise à jour : flux de mise à jour Linux, remise de paquets ou git, et vérification post-mise à jour.

Documentation principale :

- `docs/install/index.md`
- `docs/install/updating.md`
- `docs/platforms/linux.md`
- `docs/platforms/index.md`

### 2. Runtime Gateway et contrôle des services

Ancres de recherche : Runtime Gateway au premier plan, contrôle des processus, runtime gateway au premier plan et contrôle des processus de l'hôte linux gateway, runtime gateway au premier plan et contrôle des processus, configuration du cycle de vie du service utilisateur Systemd, opération du cycle de vie du service utilisateur Systemd, statut du cycle de vie du service utilisateur Systemd, récupération du cycle de vie du service utilisateur Systemd, cycle de vie du service utilisateur systemd de l'hôte linux gateway, cycle de vie du service utilisateur systemd.

Note de catégorie : [Runtime Gateway et contrôle des services](foreground-gateway-runtime-and-process-control.md)

Décisions de notation :

- Couverture : `Stable (83%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (83%)`
- LTS : ✅

Fonctionnalités :

- Runtime Gateway au premier plan : couvre les contrôles visibles par l'utilisateur du runtime Gateway au premier plan, l'affichage de l'état, la navigation et le comportement de rendu pour le runtime Gateway au premier plan et le contrôle des processus.
- Contrôle des processus : couvre les contrôles visibles par l'utilisateur du contrôle des processus, l'affichage de l'état, la navigation et le comportement de rendu pour le runtime Gateway au premier plan et le contrôle des processus.
- Configuration du cycle de vie du service utilisateur Systemd : définit la configuration du cycle de vie du service utilisateur Systemd, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le cycle de vie du service utilisateur Systemd.
- Opération du cycle de vie du service utilisateur Systemd : définit l'opération du cycle de vie du service utilisateur Systemd, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le cycle de vie du service utilisateur Systemd.
- Statut du cycle de vie du service utilisateur Systemd : définit le statut du cycle de vie du service utilisateur Systemd, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le cycle de vie du service utilisateur Systemd.
- Récupération du cycle de vie du service utilisateur Systemd : définit la récupération du cycle de vie du service utilisateur Systemd, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le cycle de vie du service utilisateur Systemd.

Documentation principale :

- `docs/gateway/index.md`
- `docs/cli/gateway.md`
- `docs/platforms/linux.md`
- `docs/vps.md`

### 3. Accès à distance et sécurité

Ancres de recherche : exposition du réseau distant, TLS, Tailscale, exposition du réseau distant, tls et tailscale de l'hôte linux gateway, exposition du réseau distant, tls et tailscale, exposure-runbook, authentification Gateway, gestion des secrets, sécurité, authentification et gestion des secrets de l'hôte linux gateway, sécurité, authentification et gestion des secrets.

Note de catégorie : [Accès à distance et sécurité](remote-network-exposure-tls-and-tailscale.md)

Décisions de notation :

- Couverture : `Beta (78%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (78%)`
- LTS : ✅

Fonctionnalités :

- Exposition du réseau distant : définit l'autorisation d'exposition du réseau distant, la confiance, les limites de sécurité et les contrôles de l'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- TLS : définit l'autorisation TLS, la confiance, les limites de sécurité et les contrôles de l'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- Tailscale : définit l'autorisation Tailscale, la confiance, les limites de sécurité et les contrôles de l'opérateur pour l'exposition du réseau distant, TLS et Tailscale.
- Protections d'exposition Gateway : définit les vérifications d'exposition, les avertissements de réseau non sécurisé et les contrôles de l'opérateur pour les limites de sécurité de Linux Gateway.
- Modes d'authentification Gateway : définit l'authentification par jeton/mot de passe, la résolution de secret partagé et la vérification de l'opérateur pour l'authentification de Linux Gateway.
- Gestion des secrets : définit la configuration de la gestion des secrets, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la sécurité, l'authentification et la gestion des secrets.

Documentation principale :

- `docs/gateway/remote.md`
- `docs/gateway/tailscale.md`
- `docs/gateway/security/exposure-runbook.md`
- `docs/gateway/authentication.md`
- `docs/gateway/secrets.md`

### 4. Diagnostics et réparation

Ancres de recherche : statut openclaw, diagnostics gateway, journaux openclaw, openclaw doctor, conseils de réparation, diagnostics, journaux, doctor et réparation de l'hôte linux gateway, diagnostics, journaux, doctor et réparation.

Note de catégorie : [Diagnostics et réparation](diagnostics-logs-doctor-and-repair.md)

Décisions de notation :

- Couverture : `Stable (82%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (82%)`
- LTS : ✅

Fonctionnalités :

- Rapports de diagnostic Gateway : couvre le statut Gateway, la sortie de diagnostic, la gestion des défaillances et la réparation de l'opérateur pour les flux de travail de diagnostics, journaux, doctor et réparation.
- Suivi des journaux Gateway : couvre l'affichage des journaux, le suivi des journaux, le comportement de secours local et le statut des journaux Gateway visible par l'opérateur.
- Vérifications Doctor : couvre les vérifications `openclaw doctor`, les sondes de santé Gateway et les diagnostics de l'opérateur pour les déploiements de Linux Gateway.
- Conseils de réparation pour l'opérateur : couvre la gestion des défaillances, les conseils de réparation et les étapes de récupération pour les diagnostics de Linux Gateway et les résultats de doctor.

Documentation principale :

- `docs/cli/status.md`
- `docs/cli/logs.md`
- `docs/cli/doctor.md`
- `docs/gateway/diagnostics.md`
- `docs/gateway/index.md`

### 5. Cibles de déploiement

Ancres de recherche : VPS, conteneur, conseils de déploiement cloud, VPS, conteneur et conseils de déploiement cloud de l'hôte linux gateway, VPS, conteneur et conseils de déploiement cloud.

Note de catégorie : [Cibles de déploiement](vps-container-and-cloud-deployment-guidance.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- VPS : définit la configuration VPS, les identifiants, la configuration et le comportement de vérification de l'opérateur pour VPS, conteneur et conseils de déploiement cloud.
- Conteneur : définit la configuration du conteneur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour VPS, conteneur et conseils de déploiement cloud.
- Conseils de déploiement cloud : définit la configuration des conseils de déploiement cloud, les identifiants, la configuration et le comportement de vérification de l'opérateur pour VPS, conteneur et conseils de déploiement cloud.

Documentation principale :

- `docs/vps.md`
- `docs/install/docker.md`
- `docs/install/hetzner.md`
- `docs/install/digitalocean.md`
- `docs/install/kubernetes.md`
- `docs/install/podman.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les documents et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/linux-gateway-host/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/linux-gateway-host`.
