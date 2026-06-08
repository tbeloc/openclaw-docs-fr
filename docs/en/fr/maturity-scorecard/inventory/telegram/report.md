---
title: "Rapport de Maturité Telegram"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité Telegram

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Beta (75%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (75%)`
- Fonctionnalités LTS : `5/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `telegram` de `/Users/kevinlin/tmp/maturity/telegram` dans le contrat d'inventaire actuel de la version-3 du processus.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                      | LTS | Couverture   | Qualité       | Complétude   | Fonctionnalités à évaluer                                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------- | --- | ------------ | ------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration et Opérations des Canaux](bot-setup-and-account-configuration.md)        | ✅  | `Beta (76%)` | `Beta (70%)`  | `Beta (76%)` | Création de jeton BotFather, TELEGRAM_BOT_TOKEN, Capture des identifiants de l'assistant de configuration, Démarrage getMe, Surfaçage Doctor/status, Configuration de compte nommé, Cibles CLI/message-tool, Adaptateurs de répertoire, Statut du canal, Sortie délimitée par compte      |
| [Accès et Identité](dm-pairing-and-sender-authorization.md)                 | ✅  | `Beta (76%)` | `Alpha (68%)` | `Beta (76%)` | Modes dmPolicy, Approbation du code d'appairage, Normalisation de l'ID utilisateur Telegram numérique avec telegram, allowFrom, DM non autorisé, Listes blanches de groupe, ID de chat négatifs de supergroupe, Clés de session de sujet de forum, Routage de sujet ACP, Construction de clé de session |
| [Routage et Livraison des Conversations](group-forum-topic-and-session-routing.md) | ✅  | `Beta (74%)` | `Alpha (68%)` | `Beta (74%)` | Routage et Livraison des Conversations                                                                                                                                                                                                         |
| [Médias et Contenu Enrichi](media-location-polls-and-rich-inputs.md)             | ✅  | `Beta (74%)` | `Beta (72%)`  | `Beta (74%)` | Médias et Contenu Enrichi                                                                                                                                                                                                                      |
| [Contrôles Natifs et Approbations](inline-buttons-approvals-and-actions.md)      | ✅  | `Beta (74%)` | `Beta (72%)`  | `Beta (74%)` | Rendu du clavier en ligne, Approbations Exec dans les DM, Actions de message, Découverte de capacité d'action, Synchronisation setMyCommands native au démarrage, Normalisation du nom/description de commande, Commandes intégrées, Autorisation de commande dans les DM, Boutons de modèle      |

## Barème de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, en direct, ou les preuves de flux serveur/runtime
  dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. Les couvertures de test unitaires,
  d'intégration, e2e, en direct et de flux runtime réel sont des entrées de couverture
  uniquement ; elles ne relèvent ni n'abaissent la qualité.
- Complétude :
  notation de label de maturité pour la façon dont la catégorie livre complètement l'ensemble de capacités
  spécifique à la surface prévue. Utilisez les instructions de complétude liées à la taxonomie pour cette surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez le
  label de maturité plus élevé.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités détaillées plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et Opérations des Canaux

Ancres de recherche : configuration et opérations des canaux telegram bot, configuration et opérations des canaux bot, cibles cli multi-compte telegram et statut, cibles cli multi-compte et statut.

Note de catégorie : [Configuration et Opérations des Canaux](bot-setup-and-account-configuration.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Beta (70%)`
- Complétude : `Beta (76%)`
- LTS : ✅

Fonctionnalités :

- Création de jeton BotFather : Création de jeton BotFather et premier démarrage de passerelle
- TELEGRAM_BOT_TOKEN : TELEGRAM_BOT_TOKEN, botToken, tokenFile, et jeton délimité par compte
- Capture des identifiants de l'assistant de configuration : Capture des identifiants de l'assistant de configuration, invites de liste blanche, et valeurs par défaut de politique DM
- Démarrage getMe : Démarrage getMe, cache d'informations bot, limitation de compte, et défaut multi-compte
- Surfaçage Doctor/status : Surfaçage Doctor/status pour jetons invalides, valeurs par défaut manquantes, et lecture seule
- Configuration de compte nommé : Configuration de compte nommé, sélection de compte par défaut, groupe local au compte
- Cibles CLI/message-tool : ID de chat numériques, noms d'utilisateur, sujet de forum
- Adaptateurs de répertoire : Adaptateurs de répertoire et pairs/groupes configurés pour les listes de cibles visibles par l'utilisateur
- Statut du canal : Statut du canal, statut des canaux --probe, résumés de source de jeton, vivacité
- Sortie délimitée par compte : Sortie délimitée par compte, sondage, média, et résolution de cible d'approbation

Docs principales :

- `docs/channels/telegram.md`
- `docs/gateway/config-channels.md`
- `docs/cli/channels.md`

### 2. Accès et Identité

Ancres de recherche : appairage dm telegram et autorisation de l'expéditeur, appairage dm et autorisation de l'expéditeur, routage de sujet de forum de groupe telegram, routage de sujet de forum de groupe.

Note de catégorie : [Accès et Identité](dm-pairing-and-sender-authorization.md)

Décisions de notation :

- Couverture : `Beta (76%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (76%)`
- LTS : ✅

Fonctionnalités :

- Modes dmPolicy : appairage, liste blanche, ouvert, et désactivé
- Approbation du code d'appairage : Approbation du code d'appairage, amorçage du premier propriétaire, et commands.ownerAllowFrom
- Normalisation de l'ID utilisateur Telegram numérique avec les préfixes telegram et tg :
- allowFrom : allowFrom, groupAllowFrom, groupes d'accès, et limites DM-versus-groupe
- DM non autorisé : Gestion non autorisée des DM, groupe, commande, rappel, et réaction
- Listes blanches de groupe : Listes blanches de groupe, groupPolicy, groupAllowFrom, et portillonnage de mention
- ID de chat négatifs de supergroupe : ID de chat négatifs de supergroupe et héritage de configuration de groupe/sujet
- Clés de session de sujet de forum : Clés de session de sujet de forum, message_thread_id, Comportement du sujet général, et routage de sujet.
- Routage de sujet ACP : Liaison de sujet ACP et /acp spawn --thread
- Construction de clé de session : Construction de clé de session, correspondance de route de conversation, et cible de réponse

Docs principales :

- `docs/channels/telegram.md`
- `docs/channels/pairing.md`
- `docs/channels/access-groups.md`
- `docs/channels/groups.md`
- `docs/concepts/multi-agent.md`

### 3. Routage et Livraison des Conversations

Ancres de recherche : routage et livraison des conversations telegram, routage et livraison des conversations.

Note de catégorie : [Routage et Livraison des Conversations](group-forum-topic-and-session-routing.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Alpha (68%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Routage et Livraison des Conversations : Portée des preuves pour le Routage et la Livraison des Conversations.

Docs principales :

- `docs/channels/telegram.md`
- `docs/channels/groups.md`
- `docs/concepts/multi-agent.md`

### 4. Médias et Contenu Enrichi

Ancres de recherche : médias et contenu enrichi telegram, médias et contenu enrichi.

Note de catégorie : [Médias et Contenu Enrichi](media-location-polls-and-rich-inputs.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Médias et Contenu Enrichi : Portée des preuves pour les Médias et le Contenu Enrichi.

Docs principales :

- `docs/channels/telegram.md`
- `docs/channels/location.md`

### 5. Contrôles Natifs et Approbations

Ancres de recherche : boutons en ligne telegram approbations et actions, boutons en ligne approbations et actions, commandes natives telegram et interface utilisateur de commande, commandes natives et interface utilisateur de commande.

Note de catégorie : [Contrôles Natifs et Approbations](inline-buttons-approvals-and-actions.md)

Décisions de notation :

- Couverture : `Beta (74%)`
- Qualité : `Beta (72%)`
- Complétude : `Beta (74%)`
- LTS : ✅

Fonctionnalités :

- Rendu du clavier en ligne : Rendu du clavier en ligne, gestion des requêtes de rappel, Boutons URL Mini App, et rappels d'approbation.
- Approbations Exec dans les DM : Approbations Exec dans les DM, canaux, sujets, ou les deux ; résolution de l'approbateur ; plugin
- Actions de message : envoi, sondage, réaction, suppression, édition, autocollant, et actions de recherche d'autocollant.
- Découverte de capacité d'action : Découverte de capacité d'action, configuration de portillonnage, portes d'action délimitées par compte, et vérifications de confiance du demandeur.
- Synchronisation setMyCommands native au démarrage : Synchronisation setMyCommands native au démarrage, commandes personnalisées, alias natifs, plugin
- Normalisation du nom/description de commande : Normalisation du nom/description de commande, écrêtage du budget de menu, doublon
- Commandes intégrées : Commandes intégrées telles que /help, /commands, /whoami, /status, et interface utilisateur de commande associée.
- Autorisation de commande dans les DM : Autorisation de commande dans les DM, groupes, et commandes adressées à d'autres bots
- Boutons de modèle : Boutons de modèle et assistants d'interface utilisateur de commande

Docs principales :

- `docs/channels/telegram.md`
- `docs/tools/exec-approvals.md`
- `docs/tools/reactions.md`

## Interprétation recommandée de la fiche de notation

Utilisez ce score migré comme ligne de base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites des catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité des catégories, les fonctionnalités, les docs, et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/telegram/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuves archivées :
  `/Users/kevinlin/tmp/maturity/telegram`.
