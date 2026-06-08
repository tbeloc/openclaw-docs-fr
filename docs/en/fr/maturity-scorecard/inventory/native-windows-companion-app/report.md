---
title: "Rapport de maturité de l'application compagnon Windows native"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité de l'application compagnon Windows native

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Expérimental (5%)`
- Qualité : `Expérimental (30%)`
- Complétude : `Expérimental (5%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `native-windows-companion-app` depuis `/Users/kevinlin/tmp/maturity/native-windows-companion-app` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score soutenues par les preuves archivées. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe au barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                    | LTS | Couverture          | Qualité              | Complétude          | Fonctionnalités à évaluer                                                                                                                                                                                           |
| --------------------------------------------------------------------------- | --- | ------------------- | -------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Installation et mises à jour](packaging-install-update-desktop-integration.md) | ❌  | `Expérimental (5%)` | `Expérimental (25%)` | `Expérimental (5%)` | Téléchargement officiel de l'application, empaquetage MSI/MSIX/App Installer/winget, gestion de l'architecture Windows pour x64, canal de version de l'application                                                    |
| [Connexion à la passerelle](gateway-connection-pairing-local-remote.md)            | ❌  | `Expérimental (8%)` | `Expérimental (35%)` | `Expérimental (8%)` | Attachement/démarrage de la passerelle locale géré par l'application, modes de connexion à la passerelle distante, appairage des appareils/nœuds                                                                    |
| [Sessions de chat](native-chat-session-controls.md)                            | ❌  | `Expérimental (0%)` | `Expérimental (25%)` | `Expérimental (0%)` | Fenêtre de chat Windows native, transport de chat de passerelle                                                                                                                                                      |
| [État et réparation](diagnostics-health-operator-repair.md)                  | ❌  | `Expérimental (5%)` | `Expérimental (35%)` | `Expérimental (5%)` | États de santé de l'application, réparation spécifique à l'application, application de barre d'état système Windows, indicateurs d'état, permission de notification spécifique à l'application                        |
| [Outils de bureau et permissions](node-host-capabilities-exec-approvals.md)   | ❌  | `Expérimental (5%)` | `Expérimental (28%)` | `Expérimental (5%)` | Identité du nœud Windows, exécution de commandes hôte, politique de commande de bureau, invites d'approbation d'application, capture d'écran et de médias, comportement de l'hôte Canvas, intégrations shell Windows, secrets d'application, ACL Windows, approbation de commande |

## Barème de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les
  preuves de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent
  fournir un contexte de soutien mais ne rendent jamais une fonctionnalité couverte
  par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et
  opérationnelle. La couverture des tests unitaires, d'intégration, e2e, en direct
  et de flux runtime réel sont des entrées de couverture uniquement ; ils ne
  relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre
  complètement l'ensemble de capacités spécifiques à la surface prévue. Utilisez
  les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez
  l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées
  plutôt que comme une dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Installation et mises à jour

Ancres de recherche : Les applications compagnon Windows natives sont planifiées, application compagnon Windows, App Installer, winget.

Note de catégorie : [Installation et mises à jour](packaging-install-update-desktop-integration.md)

Décisions de notation :

- Couverture : `Expérimental (5%)`
- Qualité : `Expérimental (25%)`
- Complétude : `Expérimental (5%)`
- LTS : ❌

Fonctionnalités :

- Téléchargement officiel de l'application : Chemin de téléchargement ou d'installation officiel de l'application pour l'application compagnon Windows native.
- Empaquetage MSI/MSIX/App Installer/winget : Empaquetage MSI/MSIX/App Installer/winget, signature, mise à jour, restauration, désinstallation et entrées de bureau
- Gestion de l'architecture Windows pour x64 : Gestion de l'architecture Windows pour x64 et ARM64
- Canal de version de l'application : Canal de version de l'application, gestion de l'architecture et disponibilité des mises à jour.

Documentation principale :

- `docs/platforms/windows.md`
- `docs/install/index.md`

### 2. Connexion à la passerelle

Ancres de recherche : Application compagnon Windows, passerelle locale, passerelle distante, appairage.

Note de catégorie : [Connexion à la passerelle](gateway-connection-pairing-local-remote.md)

Décisions de notation :

- Couverture : `Expérimental (8%)`
- Qualité : `Expérimental (35%)`
- Complétude : `Expérimental (8%)`
- LTS : ❌

Fonctionnalités :

- Attachement/démarrage de la passerelle locale géré par l'application : Attachement/démarrage de la passerelle locale géré par l'application et état
- Modes de connexion à la passerelle distante : Modes de connexion à la passerelle distante, gestion des jetons/TLS et reconnexion
- Appairage des appareils/nœuds : Appairage des appareils/nœuds, UX d'approbation en attente et récupération d'appairage

Documentation principale :

- `docs/platforms/windows.md`
- `docs/gateway/index.md`
- `docs/gateway/pairing.md`
- `docs/gateway/remote.md`

### 3. Sessions de chat

Ancres de recherche : WebChat, Gateway WebSocket, application compagnon Windows.

Note de catégorie : [Sessions de chat](native-chat-session-controls.md)

Décisions de notation :

- Couverture : `Expérimental (0%)`
- Qualité : `Expérimental (25%)`
- Complétude : `Expérimental (0%)`
- LTS : ❌

Fonctionnalités :

- Fenêtre de chat Windows native : Fenêtre de chat Windows native, transcription, compositeur, sélecteur de session, contrôles de modèle/réflexion, actions d'abandon/suivi, gestion de la reconnexion et rendu des outils
- Transport de chat de passerelle : Transport de chat de passerelle et contrôle de session depuis l'application compagnon Windows native.

Documentation principale :

- `docs/platforms/windows.md`
- `docs/gateway/protocol.md`

### 4. État et réparation

Ancres de recherche : Application compagnon Windows, état de la passerelle, réparation du docteur, barre d'état système, notifications natives.

Note de catégorie : [État et réparation](diagnostics-health-operator-repair.md)

Décisions de notation :

- Couverture : `Expérimental (5%)`
- Qualité : `Expérimental (35%)`
- Complétude : `Expérimental (5%)`
- LTS : ❌

Fonctionnalités :

- États de santé de l'application : États de santé de l'application, disponibilité de la passerelle/nœud, panneaux de diagnostic, ouverture de journaux, état de mise à jour, actions de réparation et comportement du bundle de support
- Réparation spécifique à l'application : Réparation spécifique à l'application pour l'appairage, les permissions, le cycle de vie du service, les versions obsolètes et l'incompatibilité de protocole
- Application de barre d'état système Windows : Application de barre d'état système Windows, icône d'état, menu d'état, notifications natives et contrôles de lancement/fermeture d'application
- Indicateurs d'état : Indicateurs d'état pour la passerelle, l'appairage des nœuds, l'activité de travail et les mises à jour
- Permission de notification spécifique à l'application : Permission de notification spécifique à l'application et gestion des défaillances

Documentation principale :

- `docs/platforms/windows.md`
- `docs/gateway/doctor.md`
- `docs/gateway/index.md`

### 5. Outils de bureau et permissions

Ancres de recherche : nœud hôte, system.run, approbations Exec, capture d'écran, ACL Windows, secrets d'application.

Note de catégorie : [Outils de bureau et permissions](node-host-capabilities-exec-approvals.md)

Décisions de notation :

- Couverture : `Expérimental (5%)`
- Qualité : `Expérimental (28%)`
- Complétude : `Expérimental (5%)`
- LTS : ❌

Fonctionnalités :

- Identité du nœud Windows : Identité du nœud Windows et publicité de capacité.
- Exécution de commandes hôte : Exécution de commandes hôte via system.run et outils de bureau connexes.
- Politique de commande de bureau : Politique d'autorisation/refus de commande pour les outils Windows natifs.
- Invites d'approbation d'application : Invites d'interface utilisateur d'application pour les commandes de bureau sensibles à l'approbation.
- Capture d'écran et de médias : Capture d'écran, enregistrement et affordances de capture de médias natifs.
- Comportement de l'hôte Canvas : Comportement de l'hôte Canvas et A2UI dans une application compagnon Windows native.
- Intégrations shell Windows : Intégrations shell Windows et intégrations de bureau de style PowerToys.
- Secrets d'application : Secrets d'application, persistance des jetons, IPC local sécurisé, identité de signature d'application, posture d'autorisation AppContainer ou de bureau
- ACL Windows : ACL Windows et hygiène du système de fichiers pour l'état détenu par l'application
- Approbation de commande : Approbation de commande et gating de capacité dangereuse tel que présenté aux utilisateurs

Documentation principale :

- `docs/platforms/windows.md`
- `docs/nodes/index.md`
- `docs/tools/exec.md`
- `docs/tools/exec-approvals.md`
- `docs/gateway/security/index.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/native-windows-companion-app/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/native-windows-companion-app`.
