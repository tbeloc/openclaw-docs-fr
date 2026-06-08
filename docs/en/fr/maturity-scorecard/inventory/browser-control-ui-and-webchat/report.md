---
title: "Gateway Web App Maturity Report"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité de l'Application Web Gateway

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Beta (79%)`
- Qualité : `Beta (71%)`
- Complétude : `Beta (79%)`
- Fonctionnalités LTS : `0/6`

## Résumé

Ce rapport promeut les preuves de maturité archivées `browser-control-ui-and-webchat` de `/Users/kevinlin/tmp/maturity/browser-control-ui-and-webchat` dans le contrat d'inventaire actuel process-version-3.

Les scores de catégorie Couverture et Qualité proviennent des lignes de score soutenues par les preuves archivées. La Complétude est initialisée à partir de la même largeur de preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                          | LTS | Couverture     | Qualité       | Complétude     | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------- | --- | -------------- | ------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Browser Realtime Talk](browser-realtime-talk-controls-and-voice-transports.md)   | ❌  | `Beta (78%)`   | `Beta (70%)`  | `Beta (78%)`   | Démarrage/arrêt Browser Talk, Sélection de session Provider, Relais audio Gateway, Consultations d'appels d'outils, Direction et annulation                                                                                                                                                                                                   |
| [Browser Access and Trust](gateway-connection-auth-device-pairing-and-origins.md) | ❌  | `Stable (84%)` | `Alpha (68%)` | `Stable (84%)` | Appairage d'appareil, Authentification par jeton/mot de passe, Authentification Tailscale Serve, Authentification proxy de confiance, Origines autorisées/gatewayUrl                                                                                                                                                                          |
| [Configuration](config-schema-editing-and-safe-writes.md)                         | ❌  | `Stable (82%)` | `Beta (78%)`  | `Stable (82%)` | Snapshots de configuration, Édition de formulaire de schéma, Édition JSON brute, Écritures protégées par hash de base, Application et redémarrage                                                                                                                                                                                             |
| [Browser UI](control-ui-static-shell-routing-and-pwa.md)                          | ❌  | `Beta (74%)`   | `Beta (72%)`  | `Beta (74%)`   | Interface utilisateur hébergée par Gateway, Ouverture du tableau de bord/amorçage d'authentification, Routage de chemin de base, Récupération d'actifs statiques, Cible gatewayUrl de développement, Métadonnées d'installation PWA, Mises à jour de service worker, Clés VAPID, S'abonner/se désabonner, Notifications de test                |
| [WebChat Conversations](chat-composer-session-model-controls-and-rendering.md)    | ❌  | `Beta (78%)`   | `Alpha (66%)` | `Beta (78%)`   | Envoi et abandon, Sélecteur de session et d'agent, Contrôles de modèle/réflexion, Pièces jointes, Rendu Markdown/outil/média, Projection chat.history, Cycle de vie chat.send, Rétention d'abandon/partielle, Notes d'assistant injectées, Continuité de reconnexion, Intégrations hébergées, Contrôle d'intégration externe, Tickets média d'assistant, Avatars authentifiés, Politique d'image CSP |
| [Operator Console](diagnostics-logs-update-and-activity.md)                       | ❌  | `Beta (78%)`   | `Beta (74%)`  | `Beta (78%)`   | Santé/statut/modèles, Queue de journal en direct, Exécution/statut de mise à jour, Résumés d'activité, Télémétrie de synchronisation RPC, Canaux/connexion, Gestionnaire de session et historique, Cron, Compétences/nœuds, Approbations d'exécution/agents                                                                                    |

## Barème de notation

- Couverture :
  Évaluation de l'étiquette de maturité pour l'intégration, e2e, en direct ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de support mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  Évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de Couverture uniquement ; ils
  ne relèvent ni n'abaissent la Qualité.
- Complétude :
  Évaluation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de
  capacités spécifiques à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme
  une dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Browser Realtime Talk

Ancres de recherche : Démarrage/arrêt Browser Talk, Sélection de session fournisseur, Relais audio Gateway, Consultations d'appels d'outils, Direction et annulation, Ce qu'il peut faire (aujourd'hui), Comportement du chat, Installation PWA et notifications web push.

Note de catégorie : [Browser Realtime Talk](browser-realtime-talk-controls-and-voice-transports.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Démarrage/arrêt Browser Talk : Couvre le démarrage/arrêt Browser Talk dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/fournisseur WebSocket, et le comportement du navigateur realtime talk associé.
- Sélection de session fournisseur : Couvre la sélection de session fournisseur dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/fournisseur WebSocket, et le comportement du navigateur realtime talk associé.
- Relais audio Gateway : Couvre le relais audio Gateway dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/fournisseur WebSocket, et le comportement du navigateur realtime talk associé.
- Consultations d'appels d'outils : Couvre les consultations d'appels d'outils dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/fournisseur WebSocket, et le comportement du navigateur realtime talk associé.
- Direction et annulation : Couvre la direction et l'annulation dans les contrôles Browser Talk, les options Talk, OpenAI browser WebRTC, Google Live/fournisseur WebSocket, et le comportement du navigateur realtime talk associé.

Documentation principale :

- `docs/web/control-ui.md`
- `docs/gateway/protocol.md`
- `docs/nodes/talk.md`

### 2. Browser Access and Trust

Ancres de recherche : Appairage d'appareil, Authentification par jeton/mot de passe, Authentification Tailscale Serve, Authentification proxy de confiance, Origines autorisées/gatewayUrl, Ce qu'il peut faire (aujourd'hui), Comportement du chat, Installation PWA et notifications web push.

Note de catégorie : [Browser Access and Trust](gateway-connection-auth-device-pairing-and-origins.md)

Décisions de score :

- Couverture : `Stable (84%)`
- Qualité : `Alpha (68%)`
- Complétude : `Stable (84%)`
- LTS : ❌

Fonctionnalités :

- Appairage d'appareil : Couvre l'appairage d'appareil dans la configuration de connexion Control UI/WebChat Gateway, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification proxy de confiance et Tailscale Serve, et le comportement associé de connexion gateway, authentification, appairage d'appareil et origines distantes.
- Authentification par jeton/mot de passe : Couvre l'authentification par jeton/mot de passe dans la configuration de connexion Control UI/WebChat Gateway, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification proxy de confiance et Tailscale Serve, et le comportement associé de connexion gateway, authentification, appairage d'appareil et origines distantes.
- Authentification Tailscale Serve : Couvre l'authentification Tailscale Serve dans la configuration de connexion Control UI/WebChat Gateway, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification proxy de confiance et Tailscale Serve, et le comportement associé de connexion gateway, authentification, appairage d'appareil et origines distantes.
- Authentification proxy de confiance : Couvre l'authentification proxy de confiance dans la configuration de connexion Control UI/WebChat Gateway, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification proxy de confiance et Tailscale Serve, et le comportement associé de connexion gateway, authentification, appairage d'appareil et origines distantes.
- Origines autorisées/gatewayUrl : Couvre les origines autorisées/gatewayUrl dans la configuration de connexion Control UI/WebChat Gateway, les vérifications d'origine du navigateur, l'authentification par jeton/mot de passe, l'authentification proxy de confiance et Tailscale Serve, et le comportement associé de connexion gateway, authentification, appairage d'appareil et origines distantes.

Documentation principale :

- `docs/web/control-ui.md`
- `docs/web/dashboard.md`
- `docs/gateway/tailscale.md`
- `docs/gateway/remote.md`

### 3. Configuration

Ancres de recherche : Snapshots de configuration, Édition de formulaire de schéma, Édition JSON brute, Écritures protégées par hash de base, Appliquer et redémarrer, Ce qu'il peut faire (aujourd'hui), Comportement du chat, Installation PWA et notifications web push.

Note de catégorie : [Configuration](config-schema-editing-and-safe-writes.md)

Décisions de score :

- Couverture : `Stable (82%)`
- Qualité : `Beta (78%)`
- Complétude : `Stable (82%)`
- LTS : ❌

Fonctionnalités :

- Snapshots de configuration : Couvre les snapshots de configuration dans `config.get`, `config.set`, `config.apply`, `config.patch`, et le comportement associé d'édition de schéma de configuration et d'écritures sécurisées.
- Édition de formulaire de schéma : Couvre l'édition de formulaire de schéma dans `config.get`, `config.set`, `config.apply`, `config.patch`, et le comportement associé d'édition de schéma de configuration et d'écritures sécurisées.
- Édition JSON brute : Couvre l'édition JSON brute dans `config.get`, `config.set`, `config.apply`, `config.patch`, et le comportement associé d'édition de schéma de configuration et d'écritures sécurisées.
- Écritures protégées par hash de base : Couvre les écritures protégées par hash de base dans `config.get`, `config.set`, `config.apply`, `config.patch`, et le comportement associé d'édition de schéma de configuration et d'écritures sécurisées.
- Appliquer et redémarrer : Couvre l'application et le redémarrage dans `config.get`, `config.set`, `config.apply`, `config.patch`, et le comportement associé d'édition de schéma de configuration et d'écritures sécurisées.

Documentation principale :

- `docs/web/control-ui.md`
- `docs/gateway/configuration.md`

### 4. Browser UI

Ancres de recherche : Interface utilisateur hébergée par Gateway, Ouverture du tableau de bord/amorçage d'authentification, Routage de chemin de base, Récupération d'actifs statiques, Cible gatewayUrl de développement, Ce qu'il peut faire (aujourd'hui), Comportement du chat, Installation PWA et notifications web push, Métadonnées d'installation PWA, Mises à jour du service worker, Clés VAPID, S'abonner/se désabonner, Notifications de test.

Note de catégorie : [Browser UI](control-ui-static-shell-routing-and-pwa.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ❌

Fonctionnalités :

- Interface utilisateur hébergée par Gateway : Couvre l'interface utilisateur hébergée par Gateway dans la fourniture du bundle Control UI depuis la Gateway, le routage racine et chemin de base, le comportement MIME/cache des actifs statiques, les actifs PWA publics, et le comportement associé du shell et du routage de l'interface de contrôle.
- Ouverture du tableau de bord/amorçage d'authentification : Couvre l'ouverture du tableau de bord/amorçage d'authentification dans la fourniture du bundle Control UI depuis la Gateway, le routage racine et chemin de base, le comportement MIME/cache des actifs statiques, les actifs PWA publics, et le comportement associé du shell et du routage de l'interface de contrôle.
- Routage de chemin de base : Couvre le routage de chemin de base dans la fourniture du bundle Control UI depuis la Gateway, le routage racine et chemin de base, le comportement MIME/cache des actifs statiques, les actifs PWA publics, et le comportement associé du shell et du routage de l'interface de contrôle.
- Récupération d'actifs statiques : Couvre la récupération d'actifs statiques dans la fourniture du bundle Control UI depuis la Gateway, le routage racine et chemin de base, le comportement MIME/cache des actifs statiques, les actifs PWA publics, et le comportement associé du shell et du routage de l'interface de contrôle.
- Cible gatewayUrl de développement : Couvre la cible gatewayUrl de développement dans la fourniture du bundle Control UI depuis la Gateway, le routage racine et chemin de base, le comportement MIME/cache des actifs statiques, les actifs PWA publics, et le comportement associé du shell et du routage de l'interface de contrôle.
- Métadonnées d'installation PWA : Couvre les métadonnées d'installation PWA dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement associé d'installation PWA et de notifications web push.
- Mises à jour du service worker : Couvre les mises à jour du service worker dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement associé d'installation PWA et de notifications web push.
- Clés VAPID : Couvre les clés VAPID dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement associé d'installation PWA et de notifications web push.
- S'abonner/se désabonner : Couvre l'abonnement/désabonnement dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement associé d'installation PWA et de notifications web push.
- Notifications de test : Couvre les notifications de test dans les métadonnées d'installation PWA du navigateur, l'enregistrement du service worker de production, la gestion des événements push, le comportement de clic de notification, et le comportement associé d'installation PWA et de notifications web push.

Documentation principale :

- `docs/web/control-ui.md`
- `docs/web/index.md`
- `docs/web/dashboard.md`
- `docs/gateway/protocol.md`

### 5. WebChat Conversations

Ancres de recherche : Envoyer et abandonner, Sélecteur de session et d'agent, Contrôles de modèle/réflexion, Pièces jointes, Rendu Markdown/outil/média, Ce qu'il peut faire (aujourd'hui), Comportement du chat, Installation PWA et notifications web push, Projection chat.history, Cycle de vie chat.send, Rétention d'abandon/partielle, Notes d'assistant injectées, Continuité de reconnexion, Intégrations hébergées, Contrôle d'intégration externe, Tickets de média d'assistant, Avatars authentifiés, Politique d'image CSP.

Note de catégorie : [WebChat Conversations](chat-composer-session-model-controls-and-rendering.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Alpha (66%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Envoyer et abandonner : Couvre l'envoi et l'abandon dans l'expérience utilisateur de composition et d'affichage du chat du navigateur après l'existence d'une connexion Gateway authentifiée : contrôles du compositeur, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion, et comportement associé du compositeur de chat et du rendu de message.
- Sélecteur de session et d'agent : Couvre le sélecteur de session et d'agent dans l'expérience utilisateur de composition et d'affichage du chat du navigateur après l'existence d'une connexion Gateway authentifiée : contrôles du compositeur, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion, et comportement associé du compositeur de chat et du rendu de message.
- Contrôles de modèle/réflexion : Couvre les contrôles de modèle/réflexion dans l'expérience utilisateur de composition et d'affichage du chat du navigateur après l'existence d'une connexion Gateway authentifiée : contrôles du compositeur, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion, et comportement associé du compositeur de chat et du rendu de message.
- Pièces jointes : Couvre les pièces jointes dans l'expérience utilisateur de composition et d'affichage du chat du navigateur après l'existence d'une connexion Gateway authentifiée : contrôles du compositeur, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion, et comportement associé du compositeur de chat et du rendu de message.
- Rendu Markdown/outil/média : Couvre le rendu Markdown/outil/média dans l'expérience utilisateur de composition et d'affichage du chat du navigateur après l'existence d'une connexion Gateway authentifiée : contrôles du compositeur, commandes slash, filtrage de session et d'agent, remplacements de modèle/réflexion, et comportement associé du compositeur de chat et du rendu de message.
- Projection chat.history : Couvre la projection chat.history dans le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement associé du runtime webchat et de la continuité de session.
- Cycle de vie chat.send : Couvre le cycle de vie chat.send dans le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement associé du runtime webchat et de la continuité de session.
- Rétention d'abandon/partielle : Couvre la rétention d'abandon/partielle dans le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement associé du runtime webchat et de la continuité de session.
- Notes d'assistant injectées : Couvre les notes d'assistant injectées dans le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement associé du runtime webchat et de la continuité de session.
- Continuité de reconnexion : Couvre la continuité de reconnexion dans le contrat RPC/runtime WebChat Gateway, la projection de transcription durable, le cycle de vie d'exécution actif, l'abandon et la rétention partielle, et le comportement associé du runtime webchat et de la continuité de session.
- Intégrations hébergées : Couvre les intégrations hébergées dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'URL d'intégration externe, CSP et refus de cadre, et le comportement associé des médias hébergés et de la sécurité des intégrations.
- Contrôle d'intégration externe : Couvre le contrôle d'intégration externe dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'URL d'intégration externe, CSP et refus de cadre, et le comportement associé des médias hébergés et de la sécurité des intégrations.
- Tickets de média d'assistant : Couvre les tickets de média d'assistant dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'URL d'intégration externe, CSP et refus de cadre, et le comportement associé des médias hébergés et de la sécurité des intégrations.
- Avatars authentifiés : Couvre les avatars authentifiés dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'URL d'intégration externe, CSP et refus de cadre, et le comportement associé des médias hébergés et de la sécurité des intégrations.
- Politique d'image CSP : Couvre la politique d'image CSP dans la politique de rendu `[embed ...]`, `gateway.controlUi.embedSandbox`, le contrôle d'URL d'intégration externe, CSP et refus de cadre, et le comportement associé des médias hébergés et de la sécurité des intégrations.

Documentation principale :

- `docs/web/control-ui.md`
- `docs/web/webchat.md`
- `docs/start/getting-started.md`
- `docs/channels/channel-routing.md`
- `docs/gateway/security/secure-file-operations.md`

### 6. Operator Console

Ancres de recherche : Santé/statut/modèles, Queue de journal en direct, Exécution/statut de mise à jour, Résumés d'activité, Télémétrie de synchronisation RPC, Ce qu'il peut faire (aujourd'hui), Comportement du chat, Installation PWA et notifications web push, Canaux/connexion, gestionnaire de session, historique de session, Cron, Compétences/nœuds, Approbations d'exécution/agents.

Note de catégorie : [Operator Console](diagnostics-logs-update-and-activity.md)

Décisions de score :

- Couverture : `Beta (78%)`
- Qualité : `Beta (74%)`
- Complétude : `Beta (78%)`
- LTS : ❌

Fonctionnalités :

- Santé/statut/modèles : Couvre la santé/statut/modèles dans Debug, Logs, Update, Activity, et le comportement associé des diagnostics, journaux, mise à jour et activité.
- Queue de journal en direct : Couvre la queue de journal en direct dans Debug, Logs, Update, Activity, et le comportement associé des diagnostics, journaux, mise à jour et activité.
- Exécution/statut de mise à jour : Couvre l'exécution/statut de mise à jour dans Debug, Logs, Update, Activity, et le comportement associé des diagnostics, journaux, mise à jour et activité.
- Résumés d'activité : Couvre les résumés d'activité dans Debug, Logs, Update, Activity, et le comportement associé des diagnostics, journaux, mise à jour et activité.
- Télémétrie de synchronisation RPC : Couvre la télémétrie de synchronisation RPC dans Debug, Logs, Update, Activity, et le comportement associé des diagnostics, journaux, mise à jour et activité.
- Canaux/connexion : Couvre les canaux/connexion dans les panneaux d'opérateur non-config de l'interface de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves, et la navigation du tableau de bord qui les affiche.
- Gestionnaire de session et historique : Couvre le gestionnaire de session de l'interface de contrôle du navigateur, l'historique de session, la présence d'instance, les approbations, les diagnostics, et les onglets de journal.
- Cron : Couvre Cron dans les panneaux d'opérateur non-config de l'interface de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves, et la navigation du tableau de bord qui les affiche.
- Compétences/nœuds : Couvre les compétences/nœuds dans les panneaux d'opérateur non-config de l'interface de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves, et la navigation du tableau de bord qui les affiche.
- Approbations d'exécution/agents : Couvre les approbations d'exécution/agents dans les panneaux d'opérateur non-config de l'interface de contrôle du navigateur : canaux et connexion, instances/présence, sessions, tâches cron, compétences, nœuds, approbations d'exécution, agents, utilisation, rêves, et la navigation du tableau de bord qui les affiche.

Documentation principale :

- `docs/web/control-ui.md`
- `docs/gateway/health.md`
- `docs/gateway/protocol.md`
- `docs/web/dashboard.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/browser-control-ui-and-webchat/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/browser-control-ui-and-webchat`.
