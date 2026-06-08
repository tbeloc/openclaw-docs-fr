---
title: "Rapport de maturité de l'application compagnon macOS"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de maturité de l'application compagnon macOS

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont
arrondis au nombre entier le plus proche.

- Couverture : `Beta (71%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (71%)`
- Fonctionnalités LTS : `0/8`

## Résumé

Ce rapport promeut les preuves de maturité archivées de `macos-companion-app` depuis `/Users/kevinlin/tmp/maturity/macos-companion-app` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                     | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                          |
| ------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Canvas](canvas-a2ui.md)                                      | ❌  | `Beta (74%)`  | `Alpha (66%)` | `Beta (74%)`  | Ouverture/masquage/navigation/évaluation/snapshot du panneau Canvas, Schéma d'URL personnalisé local, Navigation automatique de l'hôte A2UI, Paramètre d'activation/désactivation de Canvas                                         |
| [Configuration locale](onboarding-cli-workspace.md)           | ❌  | `Beta (72%)`  | `Alpha (65%)` | `Beta (72%)`  | Attachement/démarrage/arrêt de la passerelle en mode local, Installation/mise à jour/redémarrage/désinstallation de LaunchAgent, Détection d'écouteur existant, Flux d'intégration natif de première exécution, Découverte CLI, Sélection d'espace de travail local, Séparation de session WebChat d'intégration |
| [État et paramètres](settings-health-diagnostics.md)          | ❌  | `Beta (70%)`  | `Beta (72%)`  | `Beta (70%)`  | État de la barre de menu, Ingestion de l'état d'activité, Navigation des paramètres, Interrogation de santé, Paramètres des canaux                                                                                                  |
| [Capacités natives](node-mode-system-run-exec-host.md)        | ❌  | `Alpha (64%)` | `Alpha (60%)` | `Alpha (64%)` | Connexion de session de nœud Mac, system.run, Politique d'approbation Exec, Demandes de permission, Persistance TCC                                                                                                                |
| [Connexions distantes](remote-mode-discovery-tunnels.md)      | ❌  | `Beta (72%)`  | `Alpha (68%)` | `Beta (72%)`  | Sélection du mode de connexion distante, Tunnel SSH, Découverte de passerelle                                                                                                                                                      |
| [Voix et conversation](voice-wake-talk.md)                    | ❌  | `Beta (70%)`  | `Alpha (63%)` | `Beta (70%)`  | Runtime Voice Wake, Appui pour parler, Plan de lecture du fournisseur de conversation                                                                                                                                               |
| [WebChat](webchat-sessions.md)                                | ❌  | `Beta (72%)`  | `Alpha (62%)` | `Beta (72%)`  | Fenêtre WebChat SwiftUI native, Transport de chat de passerelle, Réutilisation du plan de données local et distant                                                                                                                 |
| [WebChat distant](native-webchat-and-remote-client-bridges.md) | ❌  | `Beta (74%)`  | `Beta (76%)`  | `Beta (74%)`  | Transport WebChat macOS, Plan de données de tunnel SSH, Mode distant ws/wss direct, Continuité de session, Dépannage à distance                                                                                                    |

## Barème de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture uniquement ; ils ne
  n'augmentent ni ne diminuent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie fournit complètement l'ensemble de
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

### 1. Canvas

Ancres de recherche : macos companion app canvas and a2ui, canvas and a2ui.

Note de catégorie : [Canvas](canvas-a2ui.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Canvas panel open/hide/navigate/eval/snapshot : Comportement, statut et vérification visible par l'opérateur du panneau Canvas open/hide/navigate/eval/snapshot.
- Local custom URL scheme : Local custom URL scheme et service de fichiers à la racine de la session
- A2UI host auto-navigation : A2UI host auto-navigation, push/reset, et action bridge
- Canvas enable/disable setting : Paramètre Canvas enable/disable et comportement de la commande node

Docs principales :

- `docs/platforms/mac/canvas.md`
- `docs/platforms/macos.md`
- `docs/web/webchat.md`

### 2. Configuration locale

Ancres de recherche : macos companion app local gateway and launchagent, local gateway and launchagent, macos companion app onboarding, cli install, and workspace setup, onboarding, cli install, and workspace setup.

Note de catégorie : [Configuration locale](onboarding-cli-workspace.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (65%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Local mode Gateway attach/start/stop : Comportement, statut et vérification visible par l'opérateur de Local mode Gateway attach/start/stop.
- LaunchAgent install/update/restart/uninstall : LaunchAgent install/update/restart/uninstall via appels CLI gérés par l'application
- Existing-listener detection : Détection des écouteurs existants, protection des ports et chemin du journal launchd
- Native first-run onboarding flow : Flux d'intégration natif au premier lancement et marqueur d'achèvement
- CLI discovery : Découverte CLI et invite/chemin d'installation « Install CLI »
- Local workspace selection : Sélection de l'espace de travail local et démarrage de l'assistant Gateway
- Onboarding WebChat session separation : Comportement, statut et vérification visible par l'opérateur de la séparation des sessions WebChat d'intégration.

Docs principales :

- `docs/platforms/mac/bundled-gateway.md`
- `docs/platforms/macos.md`
- `docs/platforms/mac/child-process.md`
- `docs/platforms/mac/dev-setup.md`

### 3. Statut et paramètres

Ancres de recherche : macos companion app menu status and dashboard, menu status and dashboard, macos companion app settings, health, channels, and diagnostics, settings, health, channels, and diagnostics.

Note de catégorie : [Statut et paramètres](settings-health-diagnostics.md)

Décisions de score :

- Couverture : `Beta (70%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Menu-bar status : Statut de la barre de menu, menu d'action, état de l'icône de statut, menu du dock, raccourcis dashboard/chat/canvas/talk
- Activity state ingestion : Ingestion de l'état d'activité et comportement de la ligne de statut
- Settings navigation : Navigation des paramètres et onglets
- Health polling : Interrogation de la santé, statut du canal, journaux, actions de débogage, visibilité config/session/instance
- Channels settings : Paramètres des canaux et statut QR/login/probe exposés via l'application

Docs principales :

- `docs/platforms/mac/menu-bar.md`
- `docs/platforms/mac/icon.md`
- `docs/platforms/macos.md`
- `docs/platforms/mac/health.md`
- `docs/platforms/mac/logging.md`
- `docs/platforms/mac/remote.md`

### 4. Capacités natives

Ancres de recherche : macos companion app node mode, system.run, and exec host, node mode, system.run, and exec host, macos companion app permissions, privacy, and tcc, permissions, privacy, and tcc.

Note de catégorie : [Capacités natives](node-mode-system-run-exec-host.md)

Décisions de score :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (60%)`
- Complétude : `Alpha (64%)`
- LTS : ❌

Fonctionnalités :

- Mac node session connection : Connexion de session Mac node, annonce de capacité et de commande
- system.run : system.run, system.which, system.notify, approbations exec get/set
- Exec approval policy : Politique d'approbation exec, app exec host, socket local et émission d'événements
- Permission requests : Demandes de permission, interrogation de statut, interface utilisateur des paramètres et annonce de permission node
- TCC persistence : Persistance TCC, exigences de signature et conseils de permission sécurisée pour les applications propriétaires

Docs principales :

- `docs/platforms/macos.md`
- `docs/platforms/mac/xpc.md`
- `docs/platforms/mac/permissions.md`
- `docs/platforms/mac/signing.md`
- `docs/platforms/mac/peekaboo.md`

### 5. Connexions distantes

Ancres de recherche : macos companion app remote mode, discovery, and tunnels, remote mode, discovery, and tunnels.

Note de catégorie : [Connexions distantes](remote-mode-discovery-tunnels.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Remote connection mode selection : Sélection et configuration du mode de connexion distante
- SSH tunnel : Tunnel SSH et transport Gateway ws/wss direct
- Gateway discovery : Découverte Gateway, réparation de l'épingle TLS et démarrage du service node distant

Docs principales :

- `docs/platforms/mac/remote.md`
- `docs/platforms/macos.md`
- `docs/gateway/remote.md`

### 6. Voix et Talk

Ancres de recherche : macos companion app voice wake, push-to-talk, and talk mode, voice wake, push-to-talk, and talk mode.

Note de catégorie : [Voix et Talk](voice-wake-talk.md)

Décisions de score :

- Couverture : `Beta (70%)`
- Qualité : `Alpha (63%)`
- Complétude : `Beta (70%)`
- LTS : ❌

Fonctionnalités :

- Voice Wake runtime : Runtime Voice Wake, détection de déclenchement, permissions, superposition, carillons et transfert
- Push-to-talk : Push-to-talk et cycle de vie Talk Mode capture/listen/think/speak
- Talk provider playback plan : Plan de lecture du fournisseur Talk et statut talk Gateway

Docs principales :

- `docs/platforms/mac/voicewake.md`
- `docs/platforms/mac/voice-overlay.md`
- `docs/nodes/talk.md`
- `docs/platforms/macos.md`

### 7. WebChat

Ancres de recherche : macos companion app webchat and session ui, webchat and session ui.

Note de catégorie : [WebChat](webchat-sessions.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Alpha (62%)`
- Complétude : `Beta (72%)`
- LTS : ❌

Fonctionnalités :

- Native SwiftUI WebChat window : Fenêtre WebChat SwiftUI native et panneau de menu
- Gateway chat transport : Transport de chat Gateway, contrôles session/model/thinking, mappage d'événements et santé
- Local and remote data-plane reuse : Réutilisation du plan de données local et distant entre les sessions WebChat natives.

Docs principales :

- `docs/platforms/mac/webchat.md`
- `docs/platforms/macos.md`
- `docs/web/webchat.md`

### 8. WebChat distant

Ancres de recherche : macOS WebChat transport, SSH tunnel data plane, Direct ws/wss remote mode, Session continuity, Remote troubleshooting, What it can do (today), Chat behavior.

Note de catégorie : [WebChat distant](native-webchat-and-remote-client-bridges.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (76%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- macOS WebChat transport : Couvre le transport WebChat macOS sur WebChat macOS natif, réutilisation de connexion Gateway, mappage de transport de chat natif, présentation de fenêtre/panneau et comportement des ponts clients WebChat distants associés.
- SSH tunnel data plane : Couvre le plan de données du tunnel SSH sur WebChat macOS natif, réutilisation de connexion Gateway, mappage de transport de chat natif, présentation de fenêtre/panneau et comportement des ponts clients WebChat distants associés.
- Direct ws/wss remote mode : Couvre le mode distant ws/wss direct sur WebChat macOS natif, réutilisation de connexion Gateway, mappage de transport de chat natif, présentation de fenêtre/panneau et comportement des ponts clients WebChat distants associés.
- Session continuity : Couvre la continuité de session sur WebChat macOS natif, réutilisation de connexion Gateway, mappage de transport de chat natif, présentation de fenêtre/panneau et comportement des ponts clients WebChat distants associés.
- Remote troubleshooting : Couvre le dépannage distant sur WebChat macOS natif, réutilisation de connexion Gateway, mappage de transport de chat natif, présentation de fenêtre/panneau et comportement des ponts clients WebChat distants associés.

Docs principales :

- `docs/platforms/mac/webchat.md`
- `docs/gateway/remote.md`
- `docs/platforms/mac/remote.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites de la catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de la catégorie, les fonctionnalités, les docs et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/macos-companion-app/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/macos-companion-app`.
