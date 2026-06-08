---
title: "Rapport de maturité du chemin d'installation Nix"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité du chemin d'installation Nix

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Expérimental (38%)`
- Qualité : `Expérimental (45%)`
- Complétude : `Expérimental (38%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `nix-install-path` de `/Users/kevinlin/tmp/maturity/nix-install-path` dans le contrat d'inventaire actuel de la version 3 du processus.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                    | LTS | Couverture           | Qualité              | Complétude           | Fonctionnalités à évaluer                                                                                                                                                                    |
| --------------------------------------------------------------------------- | --- | -------------------- | -------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Transfert d'installation](public-nix-docs-handoff.md)                               | ❌  | `Expérimental (25%)` | `Expérimental (45%)` | `Expérimental (25%)` | Aperçu de l'installation Nix, source de vérité nix-openclaw, Découverte de l'installation, Transfert de vérification                                                                                       |
| [Cycle de vie des plugins](plugin-lifecycle-nix-store-loading.md)                   | ❌  | `Expérimental (40%)` | `Expérimental (35%)` | `Expérimental (40%)` | Refus de commande de cycle de vie, Sélection déclarative de plugins, Chargement de plugins nix-store, Sécurité des liens physiques                                                                                      |
| [Activation et UX de l'application](nix-mode-activation-runtime-detection.md)           | ❌  | `Expérimental (42%)` | `Alpha (50%)`        | `Expérimental (42%)` | Activation de l'environnement, Activation des paramètres par défaut macOS, Détection du mode Nix à l'exécution, Paramètres par défaut Nix stables, Bannière Managed-by-Nix, Contrôles de configuration en lecture seule, Saut de l'intégration                   |
| [Configuration et état](state-config-path-immutable-store.md)                    | ❌  | `Expérimental (45%)` | `Alpha (50%)`        | `Expérimental (45%)` | Garde de configuration immuable, Refus du writer de configuration, Éditions Nix en premier agent, Chemin de configuration explicite, Répertoire d'état inscriptible, Support de configuration du magasin immuable, Vérifications d'intégrité d'état            |
| [Runtime de service et gardes](gateway-service-path-nix-profile-discovery.md) | ❌  | `Expérimental (38%)` | `Expérimental (45%)` | `Expérimental (38%)` | Découverte du profil Nix PATH, Précédence du profil, Secours PATH du service, Limites binaires de confiance, Refus d'écriture de configuration, Refus de réparation du docteur, Transfert de mise à jour, Transfert du cycle de vie du service |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux de serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture
  uniquement ; ils ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie
  pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante
  définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'
  étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Install Handoff

Ancres de recherche : Aperçu de l'installation Nix, source de vérité nix-openclaw, Découvrabilité de l'installation, Remise de vérification.

Note de catégorie : [Install Handoff](public-nix-docs-handoff.md)

Décisions de score :

- Couverture : `Experimental (25%)`
- Qualité : `Experimental (45%)`
- Complétude : `Experimental (25%)`
- LTS : ❌

Fonctionnalités :

- Aperçu de l'installation Nix : Couvre l'aperçu de l'installation Nix sur la page d'installation publique Nix, la découvrabilité de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager `nix-openclaw` de première partie. Il exclut l'implémentation réelle du référentiel externe `openclaw/nix-openclaw`, ainsi que la documentation publique Nix associée et le comportement de remise nix-openclaw.
- Source de vérité nix-openclaw : Couvre la source de vérité nix-openclaw sur la page d'installation publique Nix, la découvrabilité de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager `nix-openclaw` de première partie. Il exclut l'implémentation réelle du référentiel externe `openclaw/nix-openclaw`, ainsi que la documentation publique Nix associée et le comportement de remise nix-openclaw.
- Découvrabilité de l'installation : Couvre la découvrabilité de l'installation sur la page d'installation publique Nix, la découvrabilité de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager `nix-openclaw` de première partie. Il exclut l'implémentation réelle du référentiel externe `openclaw/nix-openclaw`, ainsi que la documentation publique Nix associée et le comportement de remise nix-openclaw.
- Remise de vérification : Couvre la remise de vérification sur la page d'installation publique Nix, la découvrabilité de l'index d'installation, la navigation dans la documentation et la remise au module Home Manager `nix-openclaw` de première partie. Il exclut l'implémentation réelle du référentiel externe `openclaw/nix-openclaw`, ainsi que la documentation publique Nix associée et le comportement de remise nix-openclaw.

Documentation principale :

- `docs/install/nix.md`
- `docs/install/index.md`
- `docs/start/docs-directory.md`

### 2. Cycle de vie des plugins

Ancres de recherche : Refus de commande de cycle de vie, Sélection déclarative de plugins, Chargement de plugins nix-store, Sécurité des liens physiques.

Note de catégorie : [Plugin Lifecycle](plugin-lifecycle-nix-store-loading.md)

Décisions de score :

- Couverture : `Experimental (40%)`
- Qualité : `Experimental (35%)`
- Complétude : `Experimental (40%)`
- LTS : ❌

Fonctionnalités :

- Refus de commande de cycle de vie : Couvre le refus de commande de cycle de vie sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation de plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative de plugins.
- Sélection déclarative de plugins : Couvre la sélection déclarative de plugins sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation de plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative de plugins.
- Chargement de plugins nix-store : Couvre le chargement de plugins nix-store sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation de plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative de plugins.
- Sécurité des liens physiques : Couvre la sécurité des liens physiques sur le comportement d'installation/mise à jour/désinstallation/activation/désactivation de plugins en mode Nix, la gestion des liens physiques `/nix/store`, la sécurité du registre de manifeste et les conseils destinés aux utilisateurs pour la sélection déclarative de plugins.

Documentation principale :

- `docs/plugins/manage-plugins.md`
- `docs/tools/plugin.md`
- `docs/install/nix.md`

### 3. Activation et UX de l'application

Ancres de recherche : Activation de l'environnement, Activation des paramètres par défaut macOS, Détection du mode Nix à l'exécution, Paramètres par défaut Nix stables, Bannière Managed-by-Nix, Contrôles de configuration en lecture seule, Ignorer l'intégration.

Note de catégorie : [Activation and App UX](nix-mode-activation-runtime-detection.md)

Décisions de score :

- Couverture : `Experimental (42%)`
- Qualité : `Alpha (50%)`
- Complétude : `Experimental (42%)`
- LTS : ❌

Fonctionnalités :

- Activation de l'environnement : Couvre l'activation de l'environnement sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Activation des paramètres par défaut macOS : Couvre l'activation des paramètres par défaut macOS sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Détection du mode Nix à l'exécution : Couvre la détection du mode Nix à l'exécution sur l'activation du mode Nix, la détection des variables d'environnement, la détection des paramètres par défaut macOS et la documentation de l'opérateur qui explique comment le mode Nix est activé.
- Paramètres par défaut Nix stables : Couvre les paramètres par défaut Nix stables sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention de l'écriture de configuration locale.
- Bannière Managed-by-Nix : Couvre la bannière Managed-by-Nix sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention de l'écriture de configuration locale.
- Contrôles de configuration en lecture seule : Couvre les contrôles de configuration en lecture seule sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention de l'écriture de configuration locale.
- Ignorer l'intégration : Couvre l'ignorer de l'intégration sur la gestion des paramètres par défaut `openclaw.nixMode` de l'application macOS, l'UX de configuration en lecture seule, la bannière des paramètres, le comportement de l'intégration et la prévention de l'écriture de configuration locale.

Documentation principale :

- `docs/install/nix.md`

### 4. Configuration et état

Ancres de recherche : Garde de configuration immuable, Refus du rédacteur de configuration, Éditions Nix en priorité à l'agent, Chemin de configuration explicite, Répertoire d'état inscriptible, Support de configuration de magasin immuable, Vérifications d'intégrité d'état.

Note de catégorie : [Config and State](state-config-path-immutable-store.md)

Décisions de score :

- Couverture : `Experimental (45%)`
- Qualité : `Alpha (50%)`
- Complétude : `Experimental (45%)`
- LTS : ❌

Fonctionnalités :

- Garde de configuration immuable : Couvre la garde de configuration immuable sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du rédacteur de configuration et l'instruction de source Nix en priorité à l'agent.
- Refus du rédacteur de configuration : Couvre le refus du rédacteur de configuration sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du rédacteur de configuration et l'instruction de source Nix en priorité à l'agent.
- Éditions Nix en priorité à l'agent : Couvre les éditions Nix en priorité à l'agent sur la garde `OPENCLAW_NIX_MODE_CONFIG_IMMUTABLE`, les conseils d'édition de source, l'intégration du rédacteur de configuration et l'instruction de source Nix en priorité à l'agent.
- Chemin de configuration explicite : Couvre le chemin de configuration explicite sur les variables d'environnement de chemin de configuration/état, les attentes du magasin immuable, la résolution de chemin, les vérifications d'intégrité d'état autour de `/nix/store` et les conseils à l'exécution selon lesquels l'état doit rester inscriptible.
- Répertoire d'état inscriptible : Couvre le répertoire d'état inscriptible sur les variables d'environnement de chemin de configuration/état, les attentes du magasin immuable, la résolution de chemin, les vérifications d'intégrité d'état autour de `/nix/store` et les conseils à l'exécution selon lesquels l'état doit rester inscriptible.
- Support de configuration de magasin immuable : Couvre le support de configuration de magasin immuable sur les variables d'environnement de chemin de configuration/état, les attentes du magasin immuable, la résolution de chemin, les vérifications d'intégrité d'état autour de `/nix/store` et les conseils à l'exécution selon lesquels l'état doit rester inscriptible.
- Vérifications d'intégrité d'état : Couvre les vérifications d'intégrité d'état sur les variables d'environnement de chemin de configuration/état, les attentes du magasin immuable, la résolution de chemin, les vérifications d'intégrité d'état autour de `/nix/store` et les conseils à l'exécution selon lesquels l'état doit rester inscriptible.

Documentation principale :

- `docs/install/nix.md`
- `docs/cli/setup.md`
- `docs/help/environment.md`

### 5. Exécution du service et gardes

Ancres de recherche : Découverte du profil Nix PATH, Précédence du profil, Secours du service PATH, Limites de binaires de confiance, Refus d'écriture de configuration, Refus de réparation du docteur, Remise de mise à jour, Remise du cycle de vie du service.

Note de catégorie : [Service Runtime and Guards](gateway-service-path-nix-profile-discovery.md)

Décisions de score :

- Couverture : `Experimental (38%)`
- Qualité : `Experimental (45%)`
- Complétude : `Experimental (38%)`
- LTS : ❌

Fonctionnalités :

- Découverte du profil Nix PATH : Couvre la découverte du profil Nix PATH sur la gestion de `NIX_PROFILES`, le secours `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd et les règles adjacentes de résolution de binaires sûrs.
- Précédence du profil : Couvre la précédence du profil sur la gestion de `NIX_PROFILES`, le secours `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd et les règles adjacentes de résolution de binaires sûrs.
- Secours du service PATH : Couvre le secours du service PATH sur la gestion de `NIX_PROFILES`, le secours `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd et les règles adjacentes de résolution de binaires sûrs.
- Limites de binaires de confiance : Couvre les limites de binaires de confiance sur la gestion de `NIX_PROFILES`, le secours `~/.nix-profile/bin`, la génération du PATH du service launchd/systemd et les règles adjacentes de résolution de binaires sûrs.
- Refus d'écriture de configuration : Couvre le refus d'écriture de configuration sur `openclaw setup`, les modes de réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Refus de réparation du docteur : Couvre le refus de réparation du docteur sur `openclaw setup`, les modes de réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Remise de mise à jour : Couvre la remise de mise à jour sur `openclaw setup`, les modes de réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage et le comportement d'installation/désinstallation du service daemon en mode Nix.
- Remise du cycle de vie du service : Couvre la remise du cycle de vie du service sur `openclaw setup`, les modes de réparation/jeton `openclaw doctor`, le comportement de mise à jour automatique `openclaw update`/démarrage et le comportement d'installation/désinstallation du service daemon en mode Nix.

Documentation principale :

- `docs/install/nix.md`
- `docs/cli/setup.md`
- `docs/cli/doctor.md`
- `docs/cli/update.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites de la catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de la catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/nix-install-path/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/nix-install-path`.
