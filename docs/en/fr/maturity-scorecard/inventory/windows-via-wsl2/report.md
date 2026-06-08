---
title: "Windows via WSL2 Maturity Report"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité Windows via WSL2

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (72%)`
- Qualité : `Alpha (69%)`
- Complétude : `Beta (72%)`
- Fonctionnalités LTS : `5/6`

## Résumé

Ce rapport promeut les preuves de maturité archivées `windows-via-wsl2` de `/Users/kevinlin/tmp/maturity/windows-via-wsl2` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                               | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration WSL](wsl2-install-and-runtime-prerequisites.md)          | ✅  | `Beta (76%)`  | `Beta (70%)`  | `Beta (76%)`  | Installation WSL2 + Ubuntu, runtime Node, flux d'installation Linux dans WSL2, limite d'exécution WSL2, exigences de famille réseau WSL2, installation source et compilation dans WSL2                                                                                                                              |
| [CLI](wsl2-cli.md)                                                     | ✅  | `Beta (76%)`  | `Beta (70%)`  | `Beta (76%)`  | Points d'entrée CLI WSL2, intégration openclaw, statut et journaux du docteur openclaw, mise à jour openclaw, racine de paquet npm/pnpm/git, redémarrage de passerelle systemd géré, actualisation des métadonnées de service, avertissements du gestionnaire de paquets                                                                                                              |
| [Cycle de vie du service Gateway](systemd-gateway-service-lifecycle.md) | ✅  | `Alpha (64%)` | `Alpha (66%)` | `Alpha (64%)` | Installation systemd intégrée, installation du service Gateway, rendu d'unité utilisateur systemd, conseils d'indisponibilité systemd conscients de WSL, réparation du service docteur, linger du service utilisateur WSL, disponibilité de systemd après démarrage Windows, tâche de démarrage Windows pour WSL, vérification avant connexion Windows, attentes claires autour de l'alimentation du PC |
| [Accès et exposition de la passerelle](auth-secrets-and-exposure-posture.md) | ✅  | `Beta (70%)`  | `Alpha (65%)` | `Beta (70%)`  | Authentification par jeton/mot de passe Gateway, identifiants du fournisseur, SecretRefs d'authentification Gateway, précédence des identifiants d'URL distante, réseau virtuel WSL, configuration portproxy Windows, règles Pare-feu Windows, URL Gateway accessibles, exposition loopback et LAN, réseau IPv4 WSL2, accès distant Tailscale                                 |
| [Diagnostics et réparation](diagnostics-doctor-logs-and-repair.md)     | ✅  | `Beta (74%)`  | `Beta (72%)`  | `Beta (74%)`  | docteur openclaw, statut openclaw, journaux openclaw, SecretRef, conseils d'indisponibilité WSL/systemd, conseils de réparation de l'opérateur après service WSL2                                                                                                                                                    |
| [Navigateur et interface de contrôle](split-host-browser-and-control-ui-interop.md) | ❌  | `Beta (72%)`  | `Beta (70%)`  | `Beta (72%)`  | Passerelle WSL2 avec navigateur Windows, URL de l'interface de contrôle Windows, CDP distant brut vers Chrome Windows, MCP Chrome local hôte, cdpUrl du profil navigateur, diagnostics en couches                                                                                                                      |

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
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité
  supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration WSL

Ancres de recherche : WSL2 (recommandé), Ubuntu, Node 24, installation à partir des sources.

Note de catégorie : [Configuration WSL](wsl2-install-and-runtime-prerequisites.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ✅

Fonctionnalités :

- Installation WSL2 + Ubuntu : Exigences d'installation de WSL2 et Ubuntu.
- Runtime Node : Exigences de runtime Node 24 et Node 22.19+ à l'intérieur de WSL2.
- Flux d'installation Linux à l'intérieur de WSL2 : Flux d'installation Linux et de démarrage exécutés à l'intérieur de WSL2.
- Limite de runtime WSL2 : Limite de runtime WSL2 et sa distinction par rapport aux installations Windows natives.
- Exigences de famille réseau WSL2 : Exigences de famille réseau spécifiques à WSL2 qui affectent le démarrage de la passerelle.
- Installation à partir des sources et compilation à l'intérieur de WSL2 : Flux de travail d'installation à partir des sources et de compilation à l'intérieur de la distribution WSL2.

Docs principaux :

- `docs/platforms/windows.md`
- `docs/start/getting-started.md`

### 2. CLI

Ancres de recherche : windows via wsl2 cli, points d'entrée CLI WSL2, openclaw onboard, openclaw doctor, openclaw status, openclaw logs, openclaw update, gestionnaire de paquets.

Note de catégorie : [CLI](wsl2-cli.md)

Décisions de score :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ✅

Fonctionnalités :

- Points d'entrée CLI WSL2 : Les commandes openclaw CLI install, version, onboard, doctor, status et update s'exécutent à l'intérieur de l'environnement Linux WSL2.
- openclaw onboard : openclaw onboard et intégration non-interactive s'exécutent à l'intérieur de l'environnement Linux WSL2.
- openclaw doctor status et logs : openclaw doctor, status et logs fournissent des retours de diagnostic et de réparation spécifiques à WSL2.
- openclaw update : openclaw update, changement de canal, diagnostics dry-run/status
- npm/pnpm/git package-root : npm/pnpm/git package-root et changement de mode d'installation
- Redémarrage de passerelle systemd géré : Redémarrage de passerelle systemd géré et transfert de mise à jour
- Actualisation des métadonnées de service : Actualisation des métadonnées de service après les mises à jour de la passerelle WSL2.
- Avertissements du gestionnaire de paquets : Avertissements du gestionnaire de paquets observés à partir des installations de source et de paquets WSL2.

Docs principaux :

- `docs/platforms/windows.md`
- `docs/start/getting-started.md`
- `docs/install/updating.md`
- `docs/cli/onboard.md`
- `docs/cli/doctor.md`
- `docs/cli/status.md`
- `docs/cli/logs.md`

### 3. Cycle de vie du service de passerelle

Ancres de recherche : Installation du service de passerelle (CLI), service utilisateur systemd, systemd compatible WSL, démarrage automatique de la passerelle avant la connexion Windows, linger du service utilisateur WSL, tâche planifiée de démarrage Windows.

Note de catégorie : [Cycle de vie du service de passerelle](systemd-gateway-service-lifecycle.md)

Décisions de score :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (66%)`
- Complétude : `Alpha (64%)`
- LTS : ✅

Fonctionnalités :

- Installation systemd intégrée : Installation du daemon openclaw onboard à l'intérieur de WSL2.
- Installation du service de passerelle : Comportement d'installation de la passerelle openclaw sous systemd WSL2.
- Rendu de l'unité utilisateur systemd : Rendu de l'unité utilisateur systemd et métadonnées de cycle de vie.
- Indices de systemd non disponible compatible WSL : Indices d'opérateur lorsque systemd n'est pas disponible dans la distribution WSL.
- Réparation du service Doctor : Comportement de réparation de Doctor pour les services de passerelle WSL2.
- Linger du service utilisateur WSL : Comportement, statut et vérification visible par l'opérateur du linger du service utilisateur WSL.
- Disponibilité de Systemd après le démarrage de Windows : Disponibilité de systemd après le démarrage de Windows et le démarrage de la distribution WSL.
- Tâche de démarrage Windows pour WSL : Comportement de la tâche de démarrage Windows pour lancer WSL avant la connexion.
- Vérification avant la connexion Windows : Comportement, statut et vérification visible par l'opérateur avant la connexion Windows.
- Attentes claires autour de l'alimentation du PC : Attentes claires autour de l'alimentation du PC, mise en veille, démarrage de Windows, démarrage de WSL et disponibilité de la passerelle

Docs principaux :

- `docs/platforms/windows.md`
- `docs/gateway/index.md`
- `docs/gateway/doctor.md`

### 4. Accès et exposition de la passerelle

Ancres de recherche : Authentification de la passerelle, SecretRef, Précédence des identifiants d'URL distante, Avancé : exposer les services WSL sur le LAN (portproxy), portproxy, IPv4 WSL2.

Note de catégorie : [Accès et exposition de la passerelle](auth-secrets-and-exposure-posture.md)

Décisions de score :

- Couverture : `Beta (70%)`
- Qualité : `Alpha (65%)`
- Complétude : `Beta (70%)`
- LTS : ✅

Fonctionnalités :

- Authentification par jeton/mot de passe de la passerelle : Authentification par jeton et mot de passe de la passerelle pour les clients s'exécutant via WSL2.
- Identifiants du fournisseur : Stockage et recherche des identifiants du fournisseur à partir de l'environnement WSL2.
- SecretRefs d'authentification de la passerelle : Gestion des SecretRef d'authentification de la passerelle pour les processus de passerelle hébergés sur WSL2.
- Précédence des identifiants d'URL distante : Précédence des identifiants d'URL distante lorsque les clients WSL2 se connectent à des passerelles locales ou distantes.
- Réseau virtuel WSL : Comportement du réseau virtuel WSL et adressage hôte/invité.
- Configuration Windows portproxy : Configuration Windows netsh interface portproxy pour exposer les services WSL.
- Règles du pare-feu Windows : Règles du pare-feu Windows pour l'accès à la passerelle WSL.
- URLs de passerelle accessibles : URLs de passerelle qui doivent être accessibles à partir de Windows, WSL2 et des clients LAN.
- Exposition en boucle locale et LAN : Comportement d'écoute en boucle locale par rapport au LAN pour l'exposition de la passerelle WSL2.
- Réseau IPv4 spécifique à WSL2 : Comportement de la famille réseau IPv4 spécifique à WSL2.
- Accès distant Tailscale : Comportement de Tailscale et d'accès distant où il intersecte la mise en réseau WSL2.

Docs principaux :

- `docs/gateway/authentication.md`
- `docs/gateway/secrets.md`
- `docs/gateway/remote.md`
- `docs/gateway/security/exposure-runbook.md`
- `docs/platforms/windows.md`

### 5. Diagnostics et réparation

Ancres de recherche : windows via wsl2 diagnostics, doctor, logs et repair, diagnostics, doctor, logs et repair.

Note de catégorie : [Diagnostics et réparation](diagnostics-doctor-logs-and-repair.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- openclaw doctor : openclaw doctor et réparation/migration pour la passerelle WSL2
- openclaw status : openclaw status, status --all et résumé du service/runtime de la passerelle
- openclaw logs : openclaw logs et secours du journal systemd Linux
- SecretRef : SecretRef et diagnostics d'authentification visibles à partir de status/doctor
- Indices WSL/systemd non disponible : Indices WSL/systemd non disponible et vérifications de linger
- Conseils de réparation d'opérateur après le service WSL2 : Conseils de réparation d'opérateur après le service WSL2, la configuration ou les défaillances de la passerelle

Docs principaux :

- `docs/platforms/windows.md`
- `docs/cli/status.md`
- `docs/cli/logs.md`
- `docs/cli/doctor.md`
- `docs/gateway/doctor.md`

### 6. Navigateur et interface de contrôle

Ancres de recherche : CDP distant brut de WSL2 vers Windows, URL de l'interface de contrôle Windows, MCP Chrome local sur l'hôte.

Note de catégorie : [Navigateur et interface de contrôle](split-host-browser-and-control-ui-interop.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Passerelle WSL2 avec navigateur Windows : Passerelle WSL2 avec navigateur Windows et Chrome Windows
- URL de l'interface de contrôle Windows : URL de l'interface de contrôle Windows et conseils d'origine
- Accès CDP distant brut vers Chrome Windows : Accès CDP distant brut à partir de WSL2 vers une instance Chrome Windows.
- MCP Chrome local sur l'hôte : MCP Chrome local sur l'hôte et limite de session existante
- cdpUrl du profil de navigateur : cdpUrl du profil de navigateur et configuration attachOnly
- Diagnostics en couches : Diagnostics en couches pour les défaillances d'authentification/origine/CDP

Docs principaux :

- `docs/tools/browser-wsl2-windows-remote-cdp-troubleshooting.md`
- `docs/tools/browser.md`
- `docs/web/control-ui.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, les docs et les ancres de recherche.

## Provenance de l'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/windows-via-wsl2/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/windows-via-wsl2`.
