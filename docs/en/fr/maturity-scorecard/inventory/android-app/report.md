---
title: "Rapport de maturité de l'application Android"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité de l'application Android

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Alpha (65%)`
- Qualité : `Alpha (62%)`
- Complétude : `Alpha (65%)`
- Fonctionnalités LTS : `0/7`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `android-app` de `/Users/kevinlin/tmp/maturity/android-app` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                       | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                   |
| ----------------------------------------------- | --- | ------------- | ------------- | ------------- | ------------------------------------------------------------------------------------------- |
| [Capture multimédia](camera-media-capture.md)   | ❌  | `Alpha (66%)` | `Alpha (62%)` | `Alpha (66%)` | Capture de caméra et de médias                                                              |
| [Chat mobile](chat-sessions-ui.md)              | ❌  | `Beta (70%)`  | `Alpha (66%)` | `Beta (70%)`  | Onglet Chat                                                                                 |
| [Configuration de connexion](gateway-pairing-security.md) | ❌  | `Alpha (68%)` | `Alpha (64%)` | `Alpha (68%)` | Découverte de passerelle                                                                    |
| [Distribution](install-release-distribution.md) | ❌  | `Alpha (60%)` | `Alpha (62%)` | `Alpha (60%)` | Chemin d'installation Google Play public, Chemin d'installation manuel, Performance de démarrage et smoke test de version |
| [Paramètres](settings-permissions-diagnostics.md) | ❌  | `Alpha (64%)` | `Alpha (66%)` | `Alpha (64%)` | Feuille de paramètres                                                                       |
| [Voix](voice-talk-wake.md)                      | ❌  | `Alpha (66%)` | `Alpha (60%)` | `Alpha (66%)` | Onglet Voix                                                                                 |
| [Runtime de l'appareil](node-device-capabilities.md) | ❌  | `Alpha (62%)` | `Alpha (55%)` | `Alpha (62%)` | Reconnexion en arrière-plan et présence, Disponibilité des commandes d'appareil              |

## Barème de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais une
  fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture uniquement ; ils
  ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie fournit complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `qualité > 80 et couverture > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Capture multimédia

Ancres de recherche : camera.list, camera.capture, screen capture.

Note de catégorie : [Capture multimédia](camera-media-capture.md)

Décisions de notation :

- Couverture : `Alpha (66%)`
- Qualité : `Alpha (62%)`
- Complétude : `Alpha (66%)`
- LTS : ❌

Fonctionnalités :

- Capture de caméra et de médias : Énumération de caméra, capture, photo, écran et comportement de capture multimédia.

Documentation principale :

- `docs/platforms/android.md`
- `docs/nodes/camera.md`

### 2. Chat mobile

Ancres de recherche : Chat tab, chat.history, mobile UI.

Note de catégorie : [Chat mobile](chat-sessions-ui.md)

Décisions de notation :

- Couverture : `Beta (70%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Onglet Chat : Onglet Chat, liste/filtrage de sessions, compositeur, pièces jointes d'images, analyse/rendu de messages, statut du modèle/fournisseur adjacent au chat et intégration RPC chat de passerelle

Documentation principale :

- `docs/platforms/android.md`

### 3. Configuration de connexion

Ancres de recherche : Setup Code, Manual, Bonjour.

Note de catégorie : [Configuration de connexion](gateway-pairing-security.md)

Décisions de notation :

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (64%)`
- Complétude : `Alpha (68%)`
- LTS : ❌

Fonctionnalités :

- Découverte de passerelle : Découverte de passerelle, analyse de code de configuration et de point de terminaison manuel, configuration de connexion WS/WSS, décisions de confiance TLS, identité d'appareil, jetons d'appareil stockés, authentification nœud/opérateur et gestion des erreurs de connexion

Documentation principale :

- `docs/platforms/android.md`
- `docs/gateway/bonjour.md`
- `docs/gateway/pairing.md`

### 4. Distribution

Ancres de recherche : Google Play, Manual, Startup macrobenchmark.

Note de catégorie : [Distribution](install-release-distribution.md)

Décisions de notation :

- Couverture : `Alpha (60%)`
- Qualité : `Alpha (62%)`
- Complétude : `Alpha (60%)`
- LTS : ❌

Fonctionnalités :

- Chemin d'installation Google Play public : Chemin d'installation Google Play public et points d'entrée de construction/exécution source
- Chemin d'installation manuel : Chemin d'installation manuel et comportement de distribution Google Play.
- Performance de démarrage et smoke test de version : Vérifications de smoke test et de performance de démarrage pour la distribution d'applications Android.

Documentation principale :

- `docs/platforms/android.md`

### 5. Paramètres

Ancres de recherche : Settings sheet, Notification forwarding, diagnostics.

Note de catégorie : [Paramètres](settings-permissions-diagnostics.md)

Décisions de notation :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (66%)`
- Complétude : `Alpha (64%)`
- LTS : ❌

Fonctionnalités :

- Feuille de paramètres : Feuille de paramètres et écrans de détails des paramètres, UX de demande de permission, contrôles de transfert de notifications, statut des nœuds et appareils, diagnostics du fournisseur/modèle, préférences sécurisées et rapport de diagnostic de passerelle copiable

Documentation principale :

- `docs/platforms/android.md`

### 6. Voix

Ancres de recherche : Talk Mode, Voice tab, wake.

Note de catégorie : [Voix](voice-talk-wake.md)

Décisions de notation :

- Couverture : `Alpha (66%)`
- Qualité : `Alpha (60%)`
- Complétude : `Alpha (66%)`
- LTS : ❌

Fonctionnalités :

- Onglet Voix : Onglet Voix, capture manuelle du microphone, boucle d'écoute/réflexion/parole du mode Talk, configuration Talk de passerelle, talk.speak, mode relais en temps réel, type de service de capture vocale et récepteur/script e2e vocal

Documentation principale :

- `docs/platforms/android.md`
- `docs/nodes/talk.md`

### 7. Runtime de l'appareil

Ancres de recherche : foreground service, node.presence.alive, background reconnect, Additional Android command families, node capabilities, command handling.

Note de catégorie : [Runtime de l'appareil](node-device-capabilities.md)

Décisions de notation :

- Couverture : `Alpha (62%)`
- Qualité : `Alpha (55%)`
- Complétude : `Alpha (62%)`
- LTS : ❌

Fonctionnalités :

- Reconnexion en arrière-plan et présence : Présence de service de premier plan, reconnexion et comportement de présence de nœud.
- Disponibilité des commandes d'appareil : Disponibilité des commandes d'appareil Android et annonce de capacité.

Documentation principale :

- `docs/platforms/android.md`
- `docs/nodes/troubleshooting.md`
- `docs/gateway/protocol.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec la recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/android-app/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/android-app`.
