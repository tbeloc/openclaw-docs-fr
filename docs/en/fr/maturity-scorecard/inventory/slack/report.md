---
title: "Slack Maturity Report"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité Slack

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores numériques des notes de catégorie dans `scores.yaml`. Les pourcentages sont arrondis au nombre entier le plus proche.

- Couverture : `Beta (70%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (70%)`
- Fonctionnalités LTS : `5/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `slack` de `/Users/kevinlin/tmp/maturity/slack` dans le contrat d'inventaire actuel de la version-3 du processus.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec la rubrique de complétude spécifique à la surface référencée par la taxonomie.

## Matrice

| Catégorie                                                                             | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                          |
| ------------------------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Configuration et Opérations des Canaux](app-install-auth-manifest-and-scopes.md)     | ✅  | `Beta (74%)`  | `Alpha (68%)` | `Beta (74%)`  | Installation d'App, Identifiants d'app Slack, Manifest, Scopes, Diagnostics d'état des canaux, État du compte Slack, Réparation Opérateur, Socket, Transport HTTP, Cycle de vie du Runtime |
| [Accès et Identité](dm-pairing-and-sender-authorization.md)                          | ✅  | `Beta (74%)`  | `Beta (70%)`  | `Beta (74%)`  | Accès et Identité                                                                                                                                                  |
| [Routage et Livraison des Conversations](channel-thread-routing-and-session-isolation.md) | ✅  | `Alpha (64%)` | `Alpha (66%)` | `Alpha (64%)` | Listes blanches de canaux, Routage des threads, Isolation de session, Appairage DM, Autorisation de l'expéditeur                                                  |
| [Médias et Contenu Enrichi](media-attachments-files-and-vision.md)                    | ✅  | `Alpha (64%)` | `Alpha (66%)` | `Alpha (64%)` | Médias et Contenu Enrichi                                                                                                                                         |
| [Contrôles Natifs et Approbations](slash-commands-and-native-command-routing.md)      | ✅  | `Beta (72%)`  | `Beta (70%)`  | `Beta (72%)`  | Commandes Slash, Routage des Commandes Natives, Réponses Interactives, Accueil de l'App, Événements Assistant, Approbations Natives, Actions, Opérations Sensibles à la Sécurité |

## Rubrique de notation

- Couverture :
  évaluation de l'étiquette de maturité pour l'intégration, e2e, live, ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais une
  fonctionnalité couverte par eux-mêmes.
- Qualité :
  évaluation de l'étiquette de maturité pour la robustesse de l'implémentation et opérationnelle. Les tests unitaires,
  d'intégration, e2e, live et de flux runtime réel sont des entrées de couverture uniquement ; ils ne
  augmentent ni ne diminuent la qualité.
- Complétude :
  évaluation de l'étiquette de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
  spécifique à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez l'étiquette de maturité supérieure.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et opérations des canaux

Ancres de recherche : App Install, bot token, signing secret, Manifest, Scopes, recommended manifest, minimal manifest, openclaw channels status --probe, capability and scope diagnostics, account snapshots, Operator Repair, slack diagnostics, status, and operator repair, diagnostics, status, and operator repair, Socket, HTTP Request URL, Runtime Lifecycle, slack socket/http transport and runtime lifecycle, socket/http transport and runtime lifecycle.

Note de catégorie : [Channel Setup and Operations](app-install-auth-manifest-and-scopes.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- App Install : Couvre App Install sur l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/user/signing-secret, et le comportement associé à l'installation, l'authentification, le manifest et les scopes.
- Identifiants d'application Slack : Couvre les tokens bot/app/user, la gestion du signing-secret, et la configuration des identifiants Slack pour l'authentification de l'application.
- Manifest : Couvre Manifest sur l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/user/signing-secret, et le comportement associé à l'installation, l'authentification, le manifest et les scopes.
- Scopes : Couvre Scopes sur l'installation de `@openclaw/slack`, la création de l'application Slack, le choix des manifestes recommandés/minimaux, la gestion des identifiants bot/app/user/signing-secret, et le comportement associé à l'installation, l'authentification, le manifest et les scopes.
- Diagnostics de statut du canal : Couvre `openclaw channels status --probe`, les snapshots de compte, les champs source/statut du token, les diagnostics de capacité et de scope, et les conseils de réparation Slack.
- Statut du compte Slack : Couvre les snapshots de compte, les champs source/statut du token, les résumés de capacité, et la sortie de statut Slack.
- Operator Repair : Couvre Operator Repair sur `openclaw channels status --probe`, les snapshots de compte, les champs source/statut du token, les diagnostics de capacité et de scope, et le comportement associé aux diagnostics, au statut et à la réparation de l'opérateur.
- Socket : Couvre Socket sur le démarrage/reconnexion/backoff du Socket Mode, l'enregistrement de l'URL de requête HTTP et la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, le statut/liveness, et le comportement de démarrage/skip du runtime.
- Transport HTTP : Couvre l'enregistrement de l'URL de requête HTTP, la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, le statut/liveness, et le comportement de démarrage/skip du runtime HTTP Slack.
- Runtime Lifecycle : Couvre Runtime Lifecycle sur le démarrage/reconnexion/backoff du Socket Mode, l'enregistrement de l'URL de requête HTTP et la vérification du signing-secret, la sélection du mode de transport, le cycle de vie multi-compte, le statut/liveness, et le comportement de démarrage/skip du runtime.

Docs principaux :

- `docs/channels/slack.md`
- `docs/plugins/reference/slack.md`
- `docs/gateway/secrets.md`
- `docs/concepts/qa-e2e-automation.md`
- `docs/channels/troubleshooting.md`

### 2. Accès et identité

Ancres de recherche : slack access and identity, access and identity.

Note de catégorie : [Access and Identity](dm-pairing-and-sender-authorization.md)

Décisions de score :

- Couverture : `Beta (74%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Access and Identity : Portée des preuves pour Access and Identity.

Docs principaux :

- `docs/channels/slack.md`
- `docs/channels/pairing.md`

### 3. Routage et livraison des conversations

Ancres de recherche : channel allowlists, Thread routing, Session Isolation, groupPolicy, subteam mention, DM Pairing, Sender Authorization, slack dm pairing and sender authorization, dm pairing and sender authorization.

Note de catégorie : [Conversation Routing and Delivery](channel-thread-routing-and-session-isolation.md)

Décisions de score :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (66%)`
- Complétude : `Alpha (64%)`
- LTS : ✅

Fonctionnalités :

- Channel allowlists : Couvre les listes blanches de canaux, `groupPolicy`, les portes de canal/utilisateur, les portes de mention, et le comportement de mention de sous-équipe.
- Thread routing : Couvre le routage des threads Slack, le ciblage des réponses conscientes des threads, et la liaison de session pour les threads de canal.
- Session Isolation : Couvre Session Isolation sur les listes blanches de canaux, `groupPolicy`, les portes de canal/utilisateur, le comportement de mention et de mention de sous-équipe, et le comportement associé au routage de canal/thread et à l'isolation de session.
- DM Pairing : Couvre DM Pairing sur le routage des DM Slack, `dmPolicy`, `allowFrom`, les approbations d'appairage, les DM de groupe/MPIM, l'héritage de la liste blanche au niveau du compte, l'autorisation des commandes dans les DM, et la normalisation de l'identité de l'expéditeur.
- Sender Authorization : Couvre Sender Authorization sur le routage des DM Slack, `dmPolicy`, `allowFrom`, les approbations d'appairage, les DM de groupe/MPIM, l'héritage de la liste blanche au niveau du compte, l'autorisation des commandes dans les DM, et la normalisation de l'identité de l'expéditeur.

Docs principaux :

- `docs/channels/slack.md`
- `docs/channels/bot-loop-protection.md`
- `docs/channels/pairing.md`

### 4. Médias et contenu enrichi

Ancres de recherche : slack media and rich content, media and rich content.

Note de catégorie : [Media and Rich Content](media-attachments-files-and-vision.md)

Décisions de score :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (66%)`
- Complétude : `Alpha (64%)`
- LTS : ✅

Fonctionnalités :

- Media and Rich Content : Portée des preuves pour Media and Rich Content.

Docs principaux :

- `docs/channels/slack.md`
- `docs/concepts/qa-e2e-automation.md`

### 5. Contrôles natifs et approbations

Ancres de recherche : Slash Commands, Native Command Routing, slack slash commands and native command routing, slash commands and native command routing, Interactive Replies, App Home, Assistant Events, slack interactive replies, app home, and assistant events, interactive replies, app home, and assistant events, Native Approvals, Actions, Security-sensitive Ops, slack native approvals, actions, and security-sensitive ops, native approvals, actions, and security-sensitive ops.

Note de catégorie : [Native Controls and Approvals](slash-commands-and-native-command-routing.md)

Décisions de score :

- Couverture : `Beta (72%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (72%)`
- LTS : ✅

Fonctionnalités :

- Slash Commands : Couvre Slash Commands sur le mode de commande slash configuré, les commandes slash natives, les attentes d'enregistrement des commandes, les clés de session, et le comportement associé aux commandes slash et au routage des commandes natives.
- Native Command Routing : Couvre Native Command Routing sur le mode de commande slash configuré, les commandes slash natives, les attentes d'enregistrement des commandes, les clés de session, et le comportement associé aux commandes slash et au routage des commandes natives.
- Interactive Replies : Couvre Interactive Replies sur le comportement de publication/ouverture d'App Home, les événements de thread d'assistant Slack démarrés/contexte modifié, les actions de bloc, les soumissions de modal, et le comportement associé aux réponses interactives, à l'accueil de l'application et aux événements d'assistant.
- App Home : Couvre App Home sur le comportement de publication/ouverture d'App Home, les événements de thread d'assistant Slack démarrés/contexte modifié, les actions de bloc, les soumissions de modal, et le comportement associé aux réponses interactives, à l'accueil de l'application et aux événements d'assistant.
- Assistant Events : Couvre Assistant Events sur le comportement de publication/ouverture d'App Home, les événements de thread d'assistant Slack démarrés/contexte modifié, les actions de bloc, les soumissions de modal, et le comportement associé aux réponses interactives, à l'accueil de l'application et aux événements d'assistant.
- Native Approvals : Couvre Native Approvals sur les approbations exec et plugin natives Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé aux approbations natives, aux actions et aux opérations sensibles à la sécurité.
- Actions : Couvre Actions sur les approbations exec et plugin natives Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé aux approbations natives, aux actions et aux opérations sensibles à la sécurité.
- Security-sensitive Ops : Couvre Security-sensitive Ops sur les approbations exec et plugin natives Slack, les invites d'approbation Block Kit, l'authentification d'approbation, le routage d'approbation, et le comportement associé aux approbations natives, aux actions et aux opérations sensibles à la sécurité.

Docs principaux :

- `docs/channels/slack.md`
- `docs/tools/slash-commands.md`
- `docs/tools/exec-approvals.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base de référence de l'inventaire actuel. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinir les limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, les docs et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/slack/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/slack`.
