---
title: "Rapport de maturité de l'application iOS"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité de l'application iOS

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Expérimental (41%)`
- Qualité : `Expérimental (45%)`
- Complétude : `Expérimental (41%)`
- Fonctionnalités LTS : `0/8`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `ios-app` depuis `/Users/kevinlin/tmp/maturity/ios-app` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                   | LTS | Couverture           | Qualité              | Complétude           | Fonctionnalités à évaluer                                                                                                                                                    |
| -------------------------------------------------------------------------- | --- | -------------------- | -------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Médias et partage](camera-media-photos-and-share-extension.md)            | ❌  | `Expérimental (42%)` | `Expérimental (45%)` | `Expérimental (42%)` | Liste de caméra/capture/clip                                                                                                                                                 |
| [Canevas et écran](canvas-screen-and-a2ui.md)                             | ❌  | `Expérimental (44%)` | `Expérimental (47%)` | `Expérimental (44%)` | Canevas présent/masqué/naviguer/évaluer/snapshot                                                                                                                             |
| [Chat et sessions](chat-operator-ui-and-session-controls.md)              | ❌  | `Expérimental (40%)` | `Expérimental (44%)` | `Expérimental (40%)` | Sessions de chat et contrôles d'opérateur                                                                                                                                     |
| [Configuration de la passerelle et diagnostics](settings-permissions-and-diagnostics.md)   | ❌  | `Expérimental (41%)` | `Expérimental (47%)` | `Expérimental (41%)` | Bonjour/local, Hôte/port manuel, Persistance de la configuration de connexion à la passerelle, Invite d'approbation d'empreinte TLS, Approbation d'appairage, Diagnostics d'appairage/authentification pour les utilisateurs, Onglet Paramètres |
| [Distribution](install-signing-and-testflight-distribution.md)             | ❌  | `Expérimental (42%)` | `Expérimental (45%)` | `Expérimental (42%)` | Statut d'aperçu interne                                                                                                                                                      |
| [Commandes d'appareil](node-capability-routing-and-device-commands.md)          | ❌  | `Expérimental (37%)` | `Expérimental (45%)` | `Expérimental (37%)` | Modes de localisation, Gestion des commandes d'appareil                                                                                                                       |
| [Notifications et arrière-plan](relay-push-background-and-live-activity.md) | ❌  | `Expérimental (44%)` | `Expérimental (46%)` | `Expérimental (44%)` | Enregistrement APNs et livraison par relais                                                                                                                                   |
| [Voix](voice-talk-mode-and-wake.md)                                       | ❌  | `Expérimental (38%)` | `Expérimental (43%)` | `Expérimental (38%)` | Activation vocale                                                                                                                                                            |

## Rubrique de notation

- Couverture :
  notation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de l'étiquette de maturité pour la robustesse de la mise en œuvre et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture uniquement ; ils
  ne relèvent ni n'abaissent la qualité.
- Complétude :
  notation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
  spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `qualité > 80 et couverture > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Adorable = 95-100`, `Stable = 80-95`, `Bêta = 70-80`,
  `Alpha = 50-70`, et `Expérimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Médias et partage

Ancres de recherche : liste de caméra, photothèque, Extension de partage.

Note de catégorie : [Médias et partage](camera-media-photos-and-share-extension.md)

Décisions de notation :

- Couverture : `Expérimental (42%)`
- Qualité : `Expérimental (45%)`
- Complétude : `Expérimental (42%)`
- LTS : ❌

Fonctionnalités :

- Liste de caméra/capture/clip : Liste de caméra/capture/clip, charges utiles d'image la plus récente de la photothèque, enregistrement d'écran en tant que média, flux d'extension de partage brouillon/envoi, extraction de pièces jointes, paramètres de relais de passerelle pour le partage et limites de charge utile de média mobile

Docs principaux :

- `docs/platforms/ios.md`
- `docs/nodes/camera.md`

### 2. Canevas et écran

Ancres de recherche : Canevas, A2UI, WKWebView.

Note de catégorie : [Canevas et écran](canvas-screen-and-a2ui.md)

Décisions de notation :

- Couverture : `Expérimental (44%)`
- Qualité : `Expérimental (47%)`
- Complétude : `Expérimental (44%)`
- LTS : ❌

Fonctionnalités :

- Canevas présent/masqué/naviguer/évaluer/snapshot : Canevas présent/masqué/naviguer/évaluer/snapshot, réinitialisation A2UI/push/pushJSONL, chargement de l'échafaudage WKWebView, pont d'action A2UI de confiance, enregistrement d'écran, portes de commande au premier plan et gestion de l'URL d'hôte Canvas de la passerelle

Docs principaux :

- `docs/platforms/ios.md`
- `docs/plugins/reference/canvas.md`

### 3. Chat et sessions

Ancres de recherche : Onglet Chat, compositeur de chat, centre de commande, sélecteur de session.

Note de catégorie : [Chat et sessions](chat-operator-ui-and-session-controls.md)

Décisions de notation :

- Couverture : `Expérimental (40%)`
- Qualité : `Expérimental (44%)`
- Complétude : `Expérimental (40%)`
- LTS : ❌

Fonctionnalités :

- Sessions de chat et contrôles d'opérateur : Transport de session d'opérateur, onglet Chat, compositeur/historique/streaming/affichage d'outils de chat, centre de commande, permissions et contrôles de session.

Docs principaux :

- `docs/platforms/ios.md`
- `docs/web/webchat.md`
- `docs/gateway/protocol.md`

### 4. Configuration de la passerelle et diagnostics

Ancres de recherche : Démarrage rapide (appairage + connexion), Chemins de découverte, Appairage d'appareil de nœud, Découverte Bonjour / DNS-SD, Confiance d'empreinte TLS, Onglet Paramètres, bascules de permission, diagnostics.

Note de catégorie : [Configuration de la passerelle et diagnostics](settings-permissions-and-diagnostics.md)

Décisions de notation :

- Couverture : `Expérimental (41%)`
- Qualité : `Expérimental (47%)`
- Complétude : `Expérimental (41%)`
- LTS : ❌

Fonctionnalités :

- Bonjour/local : Découverte de passerelle Bonjour/local et zone large
- Hôte/port manuel : Intégration d'hôte/port manuel et QR/code de configuration
- Persistance de la configuration de connexion à la passerelle : Comportement, statut et vérification visible par l'opérateur de la persistance de la configuration de connexion à la passerelle.
- Invite d'approbation d'empreinte TLS : Invite d'approbation d'empreinte TLS et comportement d'épinglage
- Approbation d'appairage : Approbation d'appairage, stockage d'authentification/trousseau d'appareil et authentification de session nœud+opérateur
- Diagnostics d'appairage/authentification pour les utilisateurs : Diagnostics d'appairage/authentification pour les utilisateurs et opérateurs
- Onglet Paramètres : Onglet Paramètres, paramètres de passerelle, assistants de mise en réseau manuel, intégration QR/code de configuration, bascules et demandes de permission, journaux de découverte, détails des problèmes de passerelle, liste des problèmes de diagnostics, état d'autorisation de notification et actions de récupération visibles

Docs principaux :

- `docs/platforms/ios.md`
- `docs/channels/pairing.md`

### 5. Distribution

Ancres de recherche : TestFlight, déploiement manuel Xcode, signature.

Note de catégorie : [Distribution](install-signing-and-testflight-distribution.md)

Décisions de notation :

- Couverture : `Expérimental (42%)`
- Qualité : `Expérimental (45%)`
- Complétude : `Expérimental (42%)`
- LTS : ❌

Fonctionnalités :

- Statut d'aperçu interne : Statut d'aperçu interne, déploiement manuel source/Xcode, signature locale, génération de projet XcodeGen, archive/upload TestFlight Fastlane, versioning/changelog/métadonnées, artefacts de version et drapeaux de build officiels vs locaux

Docs principaux :

- `docs/platforms/ios.md`

### 6. Commandes d'appareil

Ancres de recherche : localisation, activité de mouvement, calendrier, contacts, rappels, node.invoke, commandes d'appareil, gestion des commandes au premier plan/arrière-plan.

Note de catégorie : [Commandes d'appareil](node-capability-routing-and-device-commands.md)

Décisions de notation :

- Couverture : `Expérimental (37%)`
- Qualité : `Expérimental (45%)`
- Complétude : `Expérimental (37%)`
- LTS : ❌

Fonctionnalités :

- Modes de localisation : Modes de localisation, localisation actuelle, événements de localisation significatifs, activité de mouvement et podomètre, contacts, calendrier, rappels, ponts de demande de permission et charges utiles de commande de contexte personnel
- Gestion des commandes d'appareil : Gestion des commandes d'appareil iOS, gestion au premier plan/arrière-plan, spécifications de commande et visibilité des capacités.

Docs principaux :

- `docs/platforms/ios.md`
- `docs/gateway/protocol.md`

### 7. Notifications et arrière-plan

Ancres de recherche : Enregistrement APNs, relais de push, Activité en direct, arrière-plan actif.

Note de catégorie : [Notifications et arrière-plan](relay-push-background-and-live-activity.md)

Décisions de notation :

- Couverture : `Expérimental (44%)`
- Qualité : `Expérimental (46%)`
- Complétude : `Expérimental (44%)`
- LTS : ❌

Fonctionnalités :

- Enregistrement APNs et livraison par relais : Enregistrement APNs direct et soutenu par relais, confiance du relais de push, poignées de relais stockées, fenêtres actives en arrière-plan et mises à jour d'activité en direct.

Docs principaux :

- `docs/platforms/ios.md`
- `docs/gateway/configuration.md`

### 8. Voix

Ancres de recherche : Activation vocale, Mode de conversation, push-to-talk.

Note de catégorie : [Voix](voice-talk-mode-and-wake.md)

Décisions de notation :

- Couverture : `Expérimental (38%)`
- Qualité : `Expérimental (43%)`
- Complétude : `Expérimental (38%)`
- LTS : ❌

Fonctionnalités :

- Activation vocale : Activation vocale, synchronisation des mots déclencheurs, Mode de conversation, commandes push-to-talk, relais de passerelle en temps réel, permissions de parole et de microphone, coordination de session audio, suspension en arrière-plan et paramètres vocaux

Docs principaux :

- `docs/platforms/ios.md`
- `docs/nodes/talk.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors de portée pour cette surface

- Redéfinir les limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les docs, les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/ios-app/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/ios-app`.
