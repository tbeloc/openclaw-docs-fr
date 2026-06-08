---
title: "Rapport de maturité de l'application compagnon Linux"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité de l'application compagnon Linux

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Expérimental (5%)`
- Qualité : `Expérimental (27%)`
- Complétude : `Expérimental (5%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `linux-companion-app` de `/Users/kevinlin/tmp/maturity/linux-companion-app` dans le contrat d'inventaire actuel de la version 3 du processus.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe au rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                            | LTS | Couverture           | Qualité              | Complétude           | Fonctionnalités à évaluer                                                                                                                                                                              |
| ------------------------------------------------------------------- | --- | -------------------- | -------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Distribution d'application](packaging-install-update-desktop-integration.md) | ❌  | `Expérimental (0%)`  | `Expérimental (18%)` | `Expérimental (0%)`  | Package d'application native, cibles de package de distribution, métadonnées de version officielle                                                                                                      |
| [Connectivité de passerelle](gateway-connection-pairing-local-remote.md)  | ❌  | `Expérimental (8%)`  | `Expérimental (35%)` | `Expérimental (8%)`  | Attachement et statut de passerelle locale, appairage et authentification de passerelle, mode distant, limites de ressources locales et distantes                                                       |
| [Chat et sessions](native-chat-session-controls.md)                | ❌  | `Expérimental (10%)` | `Expérimental (36%)` | `Expérimental (10%)` | Fenêtre de chat Linux native, transcription, transport de chat de passerelle                                                                                                                            |
| [Capacités de bureau](desktop-permissions-secrets-sandbox.md)      | ❌  | `Expérimental (0%)`  | `Expérimental (20%)` | `Expérimental (0%)`  | Permissions de bureau Linux, stockage de secrets, posture de bac à sable/package, identité de nœud native Linux, exécution de commandes hôte, outils de bureau, Talk native Linux, capture de microphone, permissions de médias natives |
| [Statut et diagnostics](diagnostics-health-operator-repair.md)     | ❌  | `Expérimental (5%)`  | `Expérimental (25%)` | `Expérimental (5%)`  | Disponibilité de l'application Linux native, affichage de l'état/santé de la passerelle, ouverture de journaux/transcriptions, affordances de réparation/docteur, élément de barre d'état/plateau Linux, ligne d'état d'exécution, intégration d'environnement de bureau |

## Rubrique de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, en direct ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture
  uniquement ; elles ne relèvent ni n'abaissent la qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
  spécifique à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `qualité > 80 et couverture > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Adorable = 95-100`, `Stable = 80-95`, `Bêta = 70-80`,
  `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité supérieur.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Distribution d'application

Ancres de recherche : les applications compagnon Linux natives sont prévues, application Linux, installation du service de passerelle.

Note de catégorie : [Distribution d'application](packaging-install-update-desktop-integration.md)

Décisions de notation :

- Couverture : `Expérimental (0%)`
- Qualité : `Expérimental (18%)`
- Complétude : `Expérimental (0%)`
- LTS : ❌

Fonctionnalités :

- Package d'application native : disponibilité et chemin d'installation du package d'application compagnon Linux native.
- Cibles de package de distribution : cibles de package de distribution, fichiers de bureau, icônes, démarrage automatique et métadonnées de mise à jour
- Métadonnées de version officielle : métadonnées de version officielle pour les consoles en aval

Documentation principale :

- `docs/platforms/linux.md`
- `docs/platforms/index.md`
- `docs/install/index.md`

### 2. Connectivité de passerelle

Ancres de recherche : application Linux, installation du service de passerelle, passerelle distante, appairage.

Note de catégorie : [Connectivité de passerelle](gateway-connection-pairing-local-remote.md)

Décisions de notation :

- Couverture : `Expérimental (8%)`
- Qualité : `Expérimental (35%)`
- Complétude : `Expérimental (8%)`
- LTS : ❌

Fonctionnalités :

- Attachement et statut de passerelle locale : comportement d'attachement, de démarrage et de statut de passerelle locale à partir d'une application Linux.
- Appairage et authentification de passerelle : authentification de passerelle et appairage d'appareil à partir d'un client Linux native.
- Mode distant : mode distant via URL directe, tunnel SSH ou Tailscale
- Limites de ressources locales et distantes : limites de ressources locales et distantes pour un client compagnon Linux.

Documentation principale :

- `docs/platforms/linux.md`
- `docs/gateway/index.md`
- `docs/gateway/pairing.md`
- `docs/gateway/remote.md`

### 3. Chat et sessions

Ancres de recherche : WebChat, WebSocket de passerelle, historique de chat.

Note de catégorie : [Chat et sessions](native-chat-session-controls.md)

Décisions de notation :

- Couverture : `Expérimental (10%)`
- Qualité : `Expérimental (36%)`
- Complétude : `Expérimental (10%)`
- LTS : ❌

Fonctionnalités :

- Fenêtre de chat Linux native : comportement, statut et vérification visible par l'opérateur de la fenêtre de chat Linux native.
- Transcription : transcription, compositeur, sélecteur de session, sélecteur de modèle, contrôles d'envoi/abandon/suivi
- Transport de chat de passerelle : transport de chat WebSocket de passerelle à partir d'un client de bureau Linux.

Documentation principale :

- `docs/platforms/linux.md`
- `docs/gateway/protocol.md`
- `docs/web/webchat.md`

### 4. Capacités de bureau

Ancres de recherche : les applications compagnon Linux natives sont prévues, application Linux, approbations Exec, hôte de nœud sans interface, system.run, mode Talk, capture de microphone, caméra.

Note de catégorie : [Capacités de bureau](desktop-permissions-secrets-sandbox.md)

Décisions de notation :

- Couverture : `Expérimental (0%)`
- Qualité : `Expérimental (20%)`
- Complétude : `Expérimental (0%)`
- LTS : ❌

Fonctionnalités :

- Permissions de bureau Linux : permissions de bureau Linux pour les notifications, le microphone, l'écran, la caméra, l'accessibilité, les portails et les API d'environnement de bureau
- Stockage de secrets : stockage de secrets pour le jeton de passerelle, l'identité d'appareil, le jeton de socket d'approbation et les paramètres d'application
- Posture de bac à sable/package : posture de bac à sable/package pour les packages Flatpak/Snap/AppImage ou système
- Identité de nœud native Linux : identité de nœud native Linux et publicité de capacité
- Exécution de commandes hôte : exécution de commandes hôte via system.run et outils de bureau associés.
- Outils de bureau : outils de bureau tels que l'écran, la caméra, les notifications, Canvas et l'exécution de commandes locales
- Talk native Linux : Talk native Linux, push-to-talk, activation vocale et transcription
- Capture de microphone : capture de microphone, capture d'écran/caméra, détection de contexte de bureau et flux d'attachement de médias locaux
- Permissions de médias natives : permissions de médias natives et comportement de premier plan/arrière-plan

Documentation principale :

- `docs/platforms/linux.md`
- `docs/tools/exec-approvals.md`
- `docs/gateway/secrets.md`
- `docs/nodes/index.md`
- `docs/tools/exec.md`
- `docs/nodes/talk.md`
- `docs/nodes/camera.md`

### 5. Statut et diagnostics

Ancres de recherche : installation du service de passerelle, statut openclaw, interface de contrôle, application Linux, statut, notifications de bureau.

Note de catégorie : [Statut et diagnostics](diagnostics-health-operator-repair.md)

Décisions de notation :

- Couverture : `Expérimental (5%)`
- Qualité : `Expérimental (25%)`
- Complétude : `Expérimental (5%)`
- LTS : ❌

Fonctionnalités :

- Disponibilité de l'application Linux native : états de disponibilité de l'application Linux native
- Affichage de l'état/santé de la passerelle : comportement, statut et vérification visible par l'opérateur de l'affichage de l'état/santé de la passerelle.
- Ouverture de journaux/transcriptions : ouverture de journaux/transcriptions et gestion des ressources consciente de la localité
- Affordances de réparation/docteur : affordances de réparation/docteur et diagnostics du cycle de vie systemd
- Élément de barre d'état/plateau Linux : comportement, statut et vérification visible par l'opérateur de l'élément de barre d'état/plateau Linux.
- Ligne d'état d'exécution : ligne d'état d'exécution et notifications natives
- Intégration d'environnement de bureau : intégration d'environnement de bureau pour le comportement de plateau GNOME/KDE/Wayland/X11

Documentation principale :

- `docs/platforms/linux.md`
- `docs/start/openclaw.md`
- `docs/gateway/doctor.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/linux-companion-app/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/linux-companion-app`.
