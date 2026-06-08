---
title: "Windows via WSL2 - CLI Maturity Note"
version: 3
last_refreshed: 2026-06-04
last_refreshed_by: codex
---

# Windows via WSL2 - CLI Maturity Note

## Résumé

Le chemin CLI WSL2 est le chemin opérateur Windows recommandé : les utilisateurs installent et
exécutent la CLI OpenClaw dans l'environnement Linux WSL2, puis utilisent les commandes Linux normales pour l'intégration, le statut, le diagnostic, les journaux, les mises à jour et la réparation du flux de travail package/source. La couverture est `Beta` car la documentation et les preuves de plateforme WSL2 existantes décrivent le cycle de vie CLI complet, tandis que la qualité reste limitée par le démarrage WSL, systemd, le gestionnaire de paquets et le comportement des limites Windows/WSL.

## Portée de la catégorie

- Cette catégorie couvre les points d'entrée CLI OpenClaw et les commandes du cycle de vie lorsque la
  CLI s'exécute dans WSL2.
- Cette catégorie couvre l'intégration, le diagnostic/statut/journaux, les mises à jour, le comportement de la racine des paquets,
  le changement de mode d'installation et la transmission de mise à jour en tant que flux de travail opérateur orienté CLI.
- Hors de portée : les prérequis génériques d'installation WSL2/Ubuntu, le cycle de vie du service Gateway, l'authentification/exposition Gateway et le comportement du navigateur partagé entre hôtes.

## Fonctionnalités

- Points d'entrée CLI WSL2 : les commandes openclaw CLI install, version, onboard, doctor, status et update s'exécutent dans l'environnement Linux WSL2.
- openclaw onboard : openclaw onboard et l'intégration non-interactive s'exécutent dans l'environnement Linux WSL2.
- openclaw doctor status et logs : openclaw doctor, status et logs fournissent des retours de diagnostic et de réparation spécifiques à WSL2.
- openclaw update : openclaw update, changement de canal, diagnostics de dry-run/statut
- npm/pnpm/git package-root : npm/pnpm/git package-root et changement de mode d'installation
- Redémarrage Gateway systemd géré : Redémarrage Gateway systemd géré et transmission de mise à jour
- Actualisation des métadonnées de service : Actualisation des métadonnées de service après les mises à jour Gateway WSL2.
- Avertissements du gestionnaire de paquets : Avertissements du gestionnaire de paquets observés à partir des installations de source et de paquets WSL2.

## Score de couverture

- Score : `Beta (76%)`
- Signaux positifs :
  - `docs/platforms/windows.md` décrit WSL2 comme le chemin Windows recommandé
    et oriente les opérateurs à travers la configuration CLI de style Linux.
  - `docs/start/getting-started.md`, `docs/cli/onboard.md`,
    `docs/cli/doctor.md`, `docs/cli/status.md` et `docs/cli/logs.md` couvrent
    les points d'entrée CLI normaux et les commandes de réparation.
  - `docs/install/updating.md` couvre la mise à jour, le mode d'installation, le gestionnaire de paquets
    et le comportement de redémarrage du service qui s'applique à l'utilisation de la CLI WSL2.
- Signaux négatifs :
  - La preuve la plus solide est la documentation et la notation de plateforme WSL2 adjacente, pas une
    fiche d'évaluation CLI WSL2 de bout en bout dédiée et récente.
- Lacunes d'intégration :
  - Ajouter un test de fumée de version CLI WSL2 reproductible qui provisionne une distribution, installe
    la CLI, exécute l'intégration, le statut, le diagnostic, les journaux, le dry-run de mise à jour et vérifie
    les métadonnées de service après la mise à jour.

## Score de qualité

- Score : `Beta (70%)`
- Bonnes qualités :
  - WSL2 maintient la CLI sur le chemin Linux au lieu de s'appuyer sur des shims de commande Windows natifs.
  - La documentation opérateur rend la limite native-vs-WSL explicite et maintient WSL2 comme le
    chemin d'expérience complète recommandé.
- Mauvaises qualités :
  - Le succès de la CLI dépend toujours de l'état de démarrage WSL, de la disponibilité de systemd, du comportement du gestionnaire de paquets et des limites de réseau et de système de fichiers Windows/WSL.
- Exclus de la qualité :
  - L'étendue de la documentation et la présence de tests augmentent uniquement la couverture.

## Score de complétude

- Score : `Beta (76%)`
- Signaux positifs : la documentation archivée, la source, les tests, les preuves Gitcrawl et Discrawl couvrent la portée de la taxonomie pour les points d'entrée CLI WSL2, openclaw onboard, openclaw doctor status et logs, openclaw update, npm/pnpm/git package-root, redémarrage Gateway systemd géré, actualisation des métadonnées de service, avertissements du gestionnaire de paquets.
  diagnostics, journaux, mise à jour, package-root et transmission de métadonnées de service.
- Signaux négatifs : La catégorie manque toujours d'un artefact d'acceptation CLI WSL2 en direct dédié.
