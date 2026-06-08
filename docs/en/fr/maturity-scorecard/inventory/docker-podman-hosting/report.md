---
title: "Rapport de maturité Docker / Podman hosting"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité Docker / Podman hosting

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (77%)`
- Qualité : `Beta (73%)`
- Complétude : `Beta (77%)`
- Fonctionnalités LTS : `0/4`

## Résumé

Ce rapport promeut les preuves de maturité archivées `docker-podman-hosting` de `/Users/kevinlin/tmp/maturity/docker-podman-hosting` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité de la catégorie proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                          | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Configuration des conteneurs](docker-install-compose-and-first-run-setup.md)      | ❌  | `Beta (74%)`   | `Beta (76%)`  | `Beta (74%)`   | Script de configuration d'image locale, passerelle Docker Compose, Intégration au premier démarrage, Notes spécifiques à Docker au premier démarrage, Scripts de configuration Podman et modèle Quadlet, Configuration d'image Podman sans privilèges                                                                        |
| [Opérations des conteneurs](runtime-configuration-state-volumes-and-secrets.md)   | ❌  | `Beta (76%)`   | `Beta (70%)`  | `Beta (76%)`   | Routage CLI hôte vers Docker/Podman en cours d'exécution, Ciblage des conteneurs, Conseils de mise à jour/reconstruction/redémarrage des conteneurs pour Docker, Docker Compose, Génération de jetons de passerelle, Propriété, Docker Compose, Points de terminaison de santé des conteneurs, Documentation Docker d'hébergement VPS/fournisseur, Conseils de persistance/mise à jour Docker VM, Mise à jour côté opérateur |
| [Publication et validation d'images](image-build-release-packaging-and-attestations.md) | ❌  | `Stable (84%)` | `Beta (78%)`  | `Stable (84%)` | Étapes de construction Dockerfile racine, Flux de travail de publication Docker, Génération d'artefacts de package E2E Docker, Scripts de plan/planificateur E2E Docker, Installation du chemin de publication                                                                                                           |
| [Sandbox et outils d'agent](containerized-agents-sandbox-and-tooling-support.md)  | ❌  | `Beta (75%)`   | `Alpha (68%)` | `Beta (75%)`   | Configuration de la passerelle Docker, Support du sandbox d'agent soutenu par Docker, Cuisson des dépendances d'image de conteneur                                                                                                                                                                                       |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie fournit complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette
  de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration des conteneurs

Ancres de recherche : docker / podman hosting docker install, compose, and first-run setup, docker install, compose, and first-run setup, docker / podman hosting podman rootless, quadlet, and host cli, podman rootless, quadlet, and host cli.

Note de catégorie : [Configuration des conteneurs](docker-install-compose-and-first-run-setup.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Beta (76%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Script de configuration d'image locale : Couvre le script de configuration d'image locale dans `./scripts/docker/setup.sh` configuration d'image locale et GHCR. Forme de passerelle Docker Compose et CLI sidecar. Intégration au premier démarrage, gestion des jetons, valeurs par défaut de liaison/origine et commandes de configuration de canal après démarrage. Notes spécifiques à Docker au premier démarrage et comportement connexe d'installation, composition et configuration du premier démarrage de docker.
- Passerelle Docker Compose : Passerelle Docker Compose et forme CLI sidecar
- Intégration au premier démarrage : Intégration au premier démarrage, gestion des jetons, valeurs par défaut de liaison/origine et commandes de configuration de canal après démarrage
- Notes spécifiques à Docker au premier démarrage : Notes spécifiques à Docker au premier démarrage, excluant la configuration sans privilèges de Podman et les protocoles internes généraux de la passerelle
- Scripts de configuration Podman et modèle Quadlet : Documentation de configuration Podman, scripts/podman/setup.sh, scripts/run-openclaw-podman.sh et scripts/podman/openclaw.container.in
- Configuration d'image Podman sans privilèges : Configuration d'image Podman sans privilèges, lancement, configuration/intégration, routage CLI hôte, démarrage automatique Quadlet et vérifications de propriétaire/permissions

Docs principaux :

- `docs/install/docker.md`
- `docs/install/podman.md`

### 2. Opérations des conteneurs

Ancres de recherche : docker / podman hosting host cli container targeting and update lifecycle, host cli container targeting and update lifecycle, docker / podman hosting runtime configuration, state persistence, volumes, and secrets, runtime configuration, state persistence, volumes, and secrets, docker / podman hosting networking, control ui, health, and observability, networking, control ui, health, and observability, docker / podman hosting provider-hosted vps and operator runbooks, provider-hosted vps and operator runbooks.

Note de catégorie : [Opérations des conteneurs](runtime-configuration-state-volumes-and-secrets.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ❌

Fonctionnalités :

- Routage CLI hôte vers Docker/Podman en cours d'exécution : Routage CLI hôte vers les conteneurs Docker/Podman en cours d'exécution
- Ciblage des conteneurs : Couvre le ciblage des conteneurs dans le routage CLI hôte vers les conteneurs Docker/Podman en cours d'exécution. Comportement `--container` et `OPENCLAW_CONTAINER`, gestion env, détection runtime ambiguë, garde de proxy loopback et comportement connexe de ciblage et cycle de vie de mise à jour du conteneur hôte cli.
- Conseils de mise à jour/reconstruction/redémarrage des conteneurs pour Docker : Conseils de mise à jour/reconstruction/redémarrage des conteneurs pour les hôtes Docker et Podman
- Docker Compose : Docker Compose et montages secrets de configuration/espace de travail/profil d'authentification Podman
- Génération de jetons de passerelle : Génération de jetons de passerelle, réutilisation, persistance .env et origines autorisées de l'interface utilisateur de contrôle
- Propriété : Propriété, permissions, comportement de montage SELinux et survie d'état lors du remplacement de conteneur
- Docker Compose : Docker Compose et publication de ports Podman, mode de liaison, accès au fournisseur local hôte, Bonjour, Tailscale et origines de l'interface utilisateur de contrôle
- Points de terminaison de santé des conteneurs : Points de terminaison de santé des conteneurs, vérifications de santé Dockerfile/Compose, santé openclaw, journaux et documentation des métriques/OTel
- Documentation Docker d'hébergement VPS/fournisseur : Documentation Docker d'hébergement VPS/fournisseur et runbooks opérationnels
- Conseils de persistance/mise à jour Docker VM : Conseils de persistance/mise à jour Docker VM, adjacence Hetzner/Hostinger/DigitalOcean, avertissements Kubernetes/conteneur et exposition sécurisée
- Mise à jour côté opérateur : Mise à jour côté opérateur, sauvegarde, persistance, faible mémoire et conseils de dépannage

Docs principaux :

- `docs/install/podman.md`
- `docs/install/docker-vm-runtime.md`
- `docs/install/docker.md`
- `docs/install/hetzner.md`
- `docs/install/hostinger.md`

### 3. Publication et validation d'images

Ancres de recherche : docker / podman hosting image build, release packaging, and attestations, image build, release packaging, and attestations, docker / podman hosting docker e2e release smoke and scheduler, docker e2e release smoke and scheduler.

Note de catégorie : [Publication et validation d'images](image-build-release-packaging-and-attestations.md)

Décisions de notation :

- Couverture : `Stable (84%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (84%)`
- LTS : ❌

Fonctionnalités :

- Étapes de construction Dockerfile racine : Étapes de construction Dockerfile racine, contenu d'image runtime, arguments de construction optionnels du navigateur et CLI Docker
- Flux de travail de publication Docker : Flux de travail de publication Docker pour la publication GHCR, balises multi-arch, manifestes et vérification d'attestation
- Génération d'artefacts de package E2E Docker : Génération d'artefacts de package E2E Docker et assistants de construction partagés
- Scripts de plan/planificateur E2E Docker : Scripts de plan/planificateur E2E Docker, métadonnées de voie, regroupement ciblé, génération d'artefacts de package et action d'hydratation GitHub
- Installation du chemin de publication : Installation du chemin de publication, mise à jour, survivant de mise à niveau, fournisseur en direct, plugin, Open WebUI et planification de scénario de nettoyage

Docs principaux :

- `docs/install/docker.md`
- `docs/install/docker-vm-runtime.md`
- `docs/reference/full-release-validation.md`

### 4. Sandbox et outils d'agent

Ancres de recherche : docker / podman hosting containerized agents, sandbox, and tooling support, containerized agents, sandbox, and tooling support.

Note de catégorie : [Sandbox et outils d'agent](containerized-agents-sandbox-and-tooling-support.md)

Décisions de notation :

- Couverture : `Beta (75%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (75%)`
- LTS : ❌

Fonctionnalités :

- Configuration de la passerelle Docker : Configuration de la passerelle Docker avec OPENCLAW_SANDBOX, argument de construction CLI Docker, montage de socket, écritures de configuration sandbox et comportement de restauration
- Support du sandbox d'agent soutenu par Docker : Documentation du sandbox d'agent soutenu par Docker, comportement source et tests qui affectent les opérateurs de passerelle hébergés dans des conteneurs.
- Cuisson des dépendances d'image de conteneur : Cuisson des dépendances d'image de conteneur pour les compétences/plugins/outils

Docs principaux :

- `docs/install/docker.md`
- `docs/install/docker-vm-runtime.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les documents, et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/docker-podman-hosting/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/docker-podman-hosting`.
