---
title: "Rapport de maturité Raspberry Pi / petits appareils Linux"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité Raspberry Pi / petits appareils Linux

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (70%)`
- Qualité : `Alpha (67%)`
- Complétude : `Beta (70%)`
- Fonctionnalités LTS : `0/4`

## Résumé

Ce rapport promeut les preuves de maturité archivées `raspberry-pi-small-linux-devices` de `/Users/kevinlin/tmp/maturity/raspberry-pi-small-linux-devices` dans le contrat d'inventaire process-version-3 actuel.

Les scores de Couverture et Qualité proviennent des lignes de score archivées soutenues par des preuves. La Complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                              | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration et compatibilité](arm-linux-install-and-runtime-prerequisites.md)             | ❌  | `Alpha (55%)` | `Alpha (58%)` | `Alpha (55%)` | Exigences matérielles et système d'exploitation 64 bits, configuration du runtime Node, installation et intégration d'OpenClaw, vérification de première exécution, sélection du modèle Pi supporté, limite ARM 64 bits, conseils pour appareils non supportés, avertissements pour appareils lents, modes d'installation npm/pnpm/Bun, détection d'architecture du programme d'installation, vérifications binaires ARM optionnelles, conseils de secours/compilation |
| [Accès à distance et authentification](remote-access-tailscale-ssh-and-control-ui.md)               | ❌  | `Beta (74%)`  | `Alpha (68%)` | `Beta (74%)`  | Authentification par clé API sans interface, authentification par secret partagé de passerelle, approbations d'appairage d'appareil, gestion de SecretRef, récupération de dérive de jeton, accès au tableau de bord du tunnel SSH, Tailscale Serve/Funnel, contrôles d'exposition loopback/non-loopback, accès à l'interface utilisateur de contrôle authentifiée                                                                                     |
| [Runtime de passerelle](headless-gateway-runtime-and-model-routing.md)                      | ❌  | `Beta (78%)`  | `Beta (72%)`  | `Beta (78%)`  | Processus de passerelle toujours actif, configuration du modèle cloud, démarrage du canal, santé/statut de la passerelle, installation du service utilisateur, persistance linger/boot, drop-ins de service, réglage du redémarrage, inspection du statut/journal, sauvegarde/restauration                                                                                                                                     |
| [Performance et diagnostics](resource-tuning-diagnostics-and-low-memory-behavior.md) | ❌  | `Beta (75%)`  | `Alpha (69%)` | `Beta (75%)`  | Réglage du swap et de la RAM faible, conseils SSD USB, paramètres de cache de compilation/pas de respawn, dépannage OOM/performance, bundles de diagnostics                                                                                                                                                                                                       |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, live ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et du flux runtime réel sont des entrées de Couverture uniquement ; elles
  ne relèvent ni n'abaissent la Qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble
  de capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et compatibilité

Ancres de recherche : Exigences matérielles et système d'exploitation 64 bits, Configuration du runtime Node, Installation et intégration OpenClaw, Vérification au premier lancement, Compatibilité matérielle, Installer Node.js 24, Les clés API sont recommandées par rapport à OAuth, Accéder à l'interface de contrôle, Sélection du modèle Pi pris en charge, Limite ARM 64 bits, Conseils pour les appareils non pris en charge, Avertissements pour les appareils lents, Modes d'installation npm/pnpm/Bun, Détection de l'architecture du programme d'installation, Vérifications binaires ARM optionnelles, Conseils de secours/construction.

Note de catégorie : [Configuration et compatibilité](arm-linux-install-and-runtime-prerequisites.md)

Décisions de score :

- Couverture : `Alpha (55%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (55%)`
- LTS : ❌

Fonctionnalités :

- Exigences matérielles et système d'exploitation 64 bits : Définit la configuration des exigences matérielles et système d'exploitation 64 bits, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et les prérequis ARM Linux.
- Configuration du runtime Node : Définit la configuration du runtime Node, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et les prérequis ARM Linux.
- Installation et intégration OpenClaw : Définit l'installation et l'intégration OpenClaw, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et les prérequis ARM Linux.
- Vérification au premier lancement : Définit la vérification au premier lancement, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la configuration et les prérequis ARM Linux.
- Sélection du modèle Pi pris en charge : Définit la sélection du modèle Pi pris en charge, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Limite ARM 64 bits : Définit la limite ARM 64 bits, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Conseils pour les appareils non pris en charge : Définit les conseils pour les appareils non pris en charge, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Avertissements pour les appareils lents : Définit les avertissements pour les appareils lents, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la limite de support matériel.
- Modes d'installation npm/pnpm/Bun : Définit les modes d'installation npm/pnpm/Bun, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Détection de l'architecture du programme d'installation : Définit la détection de l'architecture du programme d'installation, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Vérifications binaires ARM optionnelles : Définit les vérifications binaires ARM optionnelles, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.
- Conseils de secours/construction : Définit les conseils de secours/construction, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la compatibilité du gestionnaire de paquets et des binaires ARM.

Documentation principale :

- `docs/install/raspberry-pi.md`
- `docs/install/index.md`
- `docs/help/faq-first-run.md`
- `docs/help/faq.md`
- `docs/platforms/linux.md`
- `docs/install/installer.md`

### 2. Accès à distance et authentification

Ancres de recherche : Authentification API-key sans interface, Authentification par secret partagé de la passerelle, Approbations d'appairage d'appareils, Gestion de SecretRef, Récupération de la dérive de jeton, Compatibilité matérielle, Installer Node.js 24, Les clés API sont recommandées par rapport à OAuth, Accès au tableau de bord via tunnel SSH, Tailscale Serve/Funnel, Contrôles d'exposition loopback/non-loopback, Accès à l'interface de contrôle authentifiée, Accéder à l'interface de contrôle.

Note de catégorie : [Accès à distance et authentification](remote-access-tailscale-ssh-and-control-ui.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Authentification API-key sans interface : Définit l'assemblage du contexte d'authentification API-key sans interface, la persistance, la gestion de la pression des jetons et le comportement de récupération pour l'authentification de la passerelle, l'appairage d'appareils et les secrets.
- Authentification par secret partagé de la passerelle : Définit l'assemblage du contexte d'authentification par secret partagé de la passerelle, la persistance, la gestion de la pression des jetons et le comportement de récupération pour l'authentification de la passerelle, l'appairage d'appareils et les secrets.
- Approbations d'appairage d'appareils : Définit l'assemblage du contexte des approbations d'appairage d'appareils, la persistance, la gestion de la pression des jetons et le comportement de récupération pour l'authentification de la passerelle, l'appairage d'appareils et les secrets.
- Gestion de SecretRef : Définit l'assemblage du contexte de gestion de SecretRef, la persistance, la gestion de la pression des jetons et le comportement de récupération pour l'authentification de la passerelle, l'appairage d'appareils et les secrets.
- Récupération de la dérive de jeton : Définit l'assemblage du contexte de récupération de la dérive de jeton, la persistance, la gestion de la pression des jetons et le comportement de récupération pour l'authentification de la passerelle, l'appairage d'appareils et les secrets.
- Accès au tableau de bord via tunnel SSH : Définit la configuration de l'accès au tableau de bord via tunnel SSH, les identifiants, la configuration et le comportement de vérification de l'opérateur pour l'accès à distance et l'interface de contrôle.
- Tailscale Serve/Funnel : Définit la configuration de Tailscale Serve/Funnel, les identifiants, la configuration et le comportement de vérification de l'opérateur pour l'accès à distance et l'interface de contrôle.
- Contrôles d'exposition loopback/non-loopback : Définit la configuration des contrôles d'exposition loopback/non-loopback, les identifiants, la configuration et le comportement de vérification de l'opérateur pour l'accès à distance et l'interface de contrôle.
- Accès à l'interface de contrôle authentifiée : Définit la configuration de l'accès à l'interface de contrôle authentifiée, les identifiants, la configuration et le comportement de vérification de l'opérateur pour l'accès à distance et l'interface de contrôle.

Documentation principale :

- `docs/install/raspberry-pi.md`
- `docs/gateway/authentication.md`
- `docs/gateway/secrets.md`
- `docs/gateway/pairing.md`
- `docs/cli/devices.md`
- `docs/gateway/remote.md`
- `docs/gateway/tailscale.md`

### 3. Runtime de la passerelle

Ancres de recherche : Processus de passerelle toujours actif, Configuration du modèle cloud, Démarrage du canal, Santé/statut de la passerelle, Compatibilité matérielle, Installer Node.js 24, Les clés API sont recommandées par rapport à OAuth, Accéder à l'interface de contrôle, Installation du service utilisateur, Persistance linger/boot, Fichiers drop-in de service, Réglage du redémarrage, Inspection du statut/journal, Sauvegarde/restauration.

Note de catégorie : [Runtime de la passerelle](headless-gateway-runtime-and-model-routing.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Processus de passerelle toujours actif : Définit la configuration du processus de passerelle toujours actif, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la passerelle sans interface et la configuration du modèle.
- Configuration du modèle cloud : Définit la configuration de la configuration du modèle cloud, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la passerelle sans interface et la configuration du modèle.
- Démarrage du canal : Définit la configuration du démarrage du canal, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la passerelle sans interface et la configuration du modèle.
- Santé/statut de la passerelle : Définit la configuration de la santé/statut de la passerelle, les identifiants, la configuration et le comportement de vérification de l'opérateur pour la passerelle sans interface et la configuration du modèle.
- Installation du service utilisateur : Définit la configuration de l'installation du service utilisateur, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le service systemd et la persistance du boot.
- Persistance linger/boot : Définit la configuration de la persistance linger/boot, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le service systemd et la persistance du boot.
- Fichiers drop-in de service : Définit la configuration des fichiers drop-in de service, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le service systemd et la persistance du boot.
- Réglage du redémarrage : Définit la configuration du réglage du redémarrage, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le service systemd et la persistance du boot.
- Inspection du statut/journal : Définit la configuration de l'inspection du statut/journal, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le service systemd et la persistance du boot.
- Sauvegarde/restauration : Définit la configuration de la sauvegarde/restauration, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le service systemd et la persistance du boot.

Documentation principale :

- `docs/gateway/index.md`
- `docs/cli/gateway.md`
- `docs/install/raspberry-pi.md`
- `docs/platforms/linux.md`
- `docs/vps.md`

### 4. Performance et diagnostics

Ancres de recherche : Réglage du swap et de la RAM faible, Conseils sur les SSD USB, Paramètres de cache de compilation/pas de respawn, Dépannage OOM/performance, Bundles de diagnostics, Compatibilité matérielle, Installer Node.js 24, Les clés API sont recommandées par rapport à OAuth.

Note de catégorie : [Performance et diagnostics](resource-tuning-diagnostics-and-low-memory-behavior.md)

Décisions de score :

- Couverture : `Beta (75%)`
- Qualité : `Alpha (69%)`
- Complétude : `Beta (75%)`
- LTS : ❌

Fonctionnalités :

- Réglage du swap et de la RAM faible : Définit la configuration du réglage du swap et de la RAM faible, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le réglage des ressources et les diagnostics.
- Conseils sur les SSD USB : Définit la configuration des conseils sur les SSD USB, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le réglage des ressources et les diagnostics.
- Paramètres de cache de compilation/pas de respawn : Définit la configuration des paramètres de cache de compilation/pas de respawn, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le réglage des ressources et les diagnostics.
- Dépannage OOM/performance : Définit la configuration du dépannage OOM/performance, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le réglage des ressources et les diagnostics.
- Bundles de diagnostics : Définit la configuration des bundles de diagnostics, les identifiants, la configuration et le comportement de vérification de l'opérateur pour le réglage des ressources et les diagnostics.

Documentation principale :

- `docs/install/raspberry-pi.md`
- `docs/platforms/linux.md`
- `docs/gateway/health.md`
- `docs/gateway/diagnostics.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/raspberry-pi-small-linux-devices/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/raspberry-pi-small-linux-devices`.
