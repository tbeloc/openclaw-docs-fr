---
title: "Rapport de Maturité Google Chat"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité Google Chat

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Alpha (57%)`
- Qualité : `Alpha (53%)`
- Complétude : `Alpha (57%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `google-chat` de `/Users/kevinlin/tmp/maturity/google-chat` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                             | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration et Opérations des Canaux](setup-auth-and-workspace-app.md)              | ❌  | `Alpha (64%)` | `Alpha (62%)` | `Alpha (64%)` | Configuration du projet Google Cloud, Configuration de l'application Chat, Configuration du compte de service, Audience et chemin du webhook, Visibilité de l'espace de travail et statut de l'application, Configuration guidée des canaux, Résolution de compte, SecretRefs du compte de service, Fichier env et identifiants en ligne, Statut du canal et sondes, Diagnostics de répertoire et d'ID mutable, Installation NPM et ClawHub, Documentation des plugins et routage du catalogue, Alias et étiquettes de canal, Interface utilisateur du statut de l'opérateur, Métadonnées d'installation/mise à jour |
| [Accès et Identité](dm-pairing-and-sender-authorization.md)                          | ❌  | `Alpha (58%)` | `Alpha (55%)` | `Alpha (58%)` | Approbation d'appairage DM, Listes blanches d'expéditeurs, Correspondance d'identité Google Chat, Routage de session directe, Diagnostics d'appairage, Listes blanches d'espaces, Gating de mention, Groupes d'accès des expéditeurs, Isolation de session de groupe, Protection contre les boucles de bot, Diagnostics d'espace                                                                                                                          |
| [Routage et Livraison des Conversations](space-routing-mentions-and-session-isolation.md) | ❌  | `Alpha (55%)` | `Alpha (50%)` | `Alpha (55%)` | Routage et Livraison des Conversations                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Médias et Contenu Enrichi](media-attachments-and-file-transfer.md)                   | ❌  | `Alpha (55%)` | `Alpha (50%)` | `Alpha (55%)` | Médias et Contenu Enrichi                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [Contrôles Natifs et Approbations](message-actions-reactions-and-approval-auth.md)    | ❌  | `Alpha (55%)` | `Alpha (50%)` | `Alpha (55%)` | Pièces jointes entrantes, Réponses médias sortantes, Action de téléchargement de message, Contrôles de source et de taille des médias, Reçus médias et placement dans les fils, Action d'envoi de texte, Action de téléchargement de fichier, Actions de réaction, Portes de capacité d'action, Correspondance d'expéditeur d'approbation, Réponses conscientes des fils, Réponses en streaming et par chunks, Cycle de vie du placeholder de saisie, Réponses de source actuelle de l'outil de message, Nettoyage NO_REPLY, Rendu Markdown/texte                                |

## Barème de notation

- Couverture :
  notation de label de maturité pour l'intégration, e2e, live, ou les preuves
  de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent fournir un contexte de soutien mais ne rendent jamais
  une fonctionnalité couverte par eux-mêmes.
- Qualité :
  notation de label de maturité pour la robustesse de l'implémentation et opérationnelle. La couverture des tests unitaires,
  d'intégration, e2e, live et de flux runtime réel sont des entrées de couverture uniquement ; elles
  ne relèvent ni n'abaissent la qualité.
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
  texte de preuve uniquement, suivi dans l'inventaire détaillé des fonctionnalités plutôt que comme une
  dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et opérations des canaux

Ancres de recherche : Configuration du projet Google Cloud, Configuration de l'application Chat, Configuration du compte de service, Audience et chemin du webhook, Visibilité de l'espace de travail et statut de l'application, Configuration guidée des canaux, Appairage DM, dm.policy, Résolution de compte, SecretRefs du compte de service, Fichier env et identifiants en ligne, Statut du canal et sondes, Diagnostics du répertoire et mutable-id, allowFrom, Installation NPM et ClawHub, Documentation des plugins et routage du catalogue, Alias et étiquettes des canaux, Interface utilisateur du statut de l'opérateur, Métadonnées d'installation/mise à jour.

Note de catégorie : [Configuration et opérations des canaux](setup-auth-and-workspace-app.md)

Décisions de score :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (62%)`
- Complétude : `Alpha (64%)`
- LTS : ❌

Fonctionnalités :

- Configuration du projet Google Cloud : Couvre la configuration du projet Google Cloud dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement connexe de configuration de l'authentification et de l'application de l'espace de travail.
- Configuration de l'application Chat : Couvre la configuration de l'application Chat dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement connexe de configuration de l'authentification et de l'application de l'espace de travail.
- Configuration du compte de service : Couvre la configuration du compte de service dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement connexe de configuration de l'authentification et de l'application de l'espace de travail.
- Audience et chemin du webhook : Couvre l'audience et le chemin du webhook dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement connexe de configuration de l'authentification et de l'application de l'espace de travail.
- Visibilité de l'espace de travail et statut de l'application : Couvre la visibilité de l'espace de travail et le statut de l'application dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement connexe de configuration de l'authentification et de l'application de l'espace de travail.
- Configuration guidée des canaux : Couvre la configuration guidée des canaux dans l'installation du plugin Google Chat, la configuration du projet Google Cloud et de l'API Chat, la sélection des identifiants du compte de service JSON/fichier/env, `audienceType`, et le comportement connexe de configuration de l'authentification et de l'application de l'espace de travail.
- Résolution de compte : Couvre la résolution de compte dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement connexe du statut des secrets multi-comptes et des diagnostics.
- SecretRefs du compte de service : Couvre les SecretRefs du compte de service dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement connexe du statut des secrets multi-comptes et des diagnostics.
- Fichier env et identifiants en ligne : Couvre le fichier env et les identifiants en ligne dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement connexe du statut des secrets multi-comptes et des diagnostics.
- Statut du canal et sondes : Couvre le statut du canal et les sondes dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement connexe du statut des secrets multi-comptes et des diagnostics.
- Diagnostics du répertoire et mutable-id : Couvre les diagnostics du répertoire et mutable-id dans `accounts`, `defaultAccount`, héritage des identifiants au niveau supérieur et au niveau du compte, SecretRefs du compte de service, et le comportement connexe du statut des secrets multi-comptes et des diagnostics.
- Installation NPM et ClawHub : Couvre l'installation NPM et ClawHub dans les métadonnées du plugin npm/ClawHub, la navigation de la documentation, les références des plugins, le catalogue officiel des plugins externes, et le comportement connexe de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.
- Documentation des plugins et routage du catalogue : Couvre la documentation des plugins et le routage du catalogue dans les métadonnées du plugin npm/ClawHub, la navigation de la documentation, les références des plugins, le catalogue officiel des plugins externes, et le comportement connexe de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.
- Alias et étiquettes des canaux : Couvre les alias et étiquettes des canaux dans les métadonnées du plugin npm/ClawHub, la navigation de la documentation, les références des plugins, le catalogue officiel des plugins externes, et le comportement connexe de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.
- Interface utilisateur du statut de l'opérateur : Couvre l'interface utilisateur du statut de l'opérateur dans les métadonnées du plugin npm/ClawHub, la navigation de la documentation, les références des plugins, le catalogue officiel des plugins externes, et le comportement connexe de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.
- Métadonnées d'installation/mise à jour : Couvre les métadonnées d'installation/mise à jour dans les métadonnées du plugin npm/ClawHub, la navigation de la documentation, les références des plugins, le catalogue officiel des plugins externes, et le comportement connexe de l'interface utilisateur de l'opérateur de distribution des plugins et de la documentation.

Documentation principale :

- `docs/channels/googlechat.md`
- `docs/plugins/reference/googlechat.md`
- `docs/gateway/config-channels.md`
- `docs/start/wizard-cli-reference.md`
- `docs/gateway/secrets.md`
- `docs/reference/secretref-credential-surface.md`
- `docs/gateway/health.md`
- `docs/plugins/plugin-inventory.md`
- `docs/channels/index.md`
- `docs/docs.json`

### 2. Accès et identité

Ancres de recherche : Approbation de l'appairage DM, Listes blanches d'expéditeurs, Correspondance d'identité Google Chat, Routage de session directe, Diagnostics d'appairage, Appairage DM, dm.policy, allowFrom, Listes blanches d'espaces, Mention gating, Groupes d'accès des expéditeurs, Isolation de session de groupe, Protection contre les boucles de bot, Diagnostics d'espace.

Note de catégorie : [Accès et identité](dm-pairing-and-sender-authorization.md)

Décisions de score :

- Couverture : `Alpha (58%)`
- Qualité : `Alpha (55%)`
- Complétude : `Alpha (58%)`
- LTS : ❌

Fonctionnalités :

- Approbation de l'appairage DM : Couvre l'approbation de l'appairage DM dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, défis d'appairage, et le comportement connexe de l'appairage DM et de l'autorisation de l'expéditeur.
- Listes blanches d'expéditeurs : Couvre les listes blanches d'expéditeurs dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, défis d'appairage, et le comportement connexe de l'appairage DM et de l'autorisation de l'expéditeur.
- Correspondance d'identité Google Chat : Couvre la correspondance d'identité Google Chat dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, défis d'appairage, et le comportement connexe de l'appairage DM et de l'autorisation de l'expéditeur.
- Routage de session directe : Couvre le routage de session directe dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, défis d'appairage, et le comportement connexe de l'appairage DM et de l'autorisation de l'expéditeur.
- Diagnostics d'appairage : Couvre les diagnostics d'appairage dans les DM Google Chat, `dm.policy`, `dm.allowFrom`, défis d'appairage, et le comportement connexe de l'appairage DM et de l'autorisation de l'expéditeur.
- Listes blanches d'espaces : Couvre les listes blanches d'espaces dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, groupes génériques, et le comportement connexe du routage d'espace, des mentions et de l'isolation de session.
- Mention gating : Couvre la mention gating dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, groupes génériques, et le comportement connexe du routage d'espace, des mentions et de l'isolation de session.
- Groupes d'accès des expéditeurs : Couvre les groupes d'accès des expéditeurs dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, groupes génériques, et le comportement connexe du routage d'espace, des mentions et de l'isolation de session.
- Isolation de session de groupe : Couvre l'isolation de session de groupe dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, groupes génériques, et le comportement connexe du routage d'espace, des mentions et de l'isolation de session.
- Protection contre les boucles de bot : Couvre la protection contre les boucles de bot dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, groupes génériques, et le comportement connexe du routage d'espace, des mentions et de l'isolation de session.
- Diagnostics d'espace : Couvre les diagnostics d'espace dans les espaces Google Chat et les messages de groupe, `groupPolicy`, `groups`, groupes génériques, et le comportement connexe du routage d'espace, des mentions et de l'isolation de session.

Documentation principale :

- `docs/channels/googlechat.md`
- `docs/channels/pairing.md`
- `docs/channels/access-groups.md`
- `docs/gateway/config-channels.md`
- `docs/channels/bot-loop-protection.md`
- `docs/channels/channel-routing.md`

### 3. Routage et livraison des conversations

Ancres de recherche : routage et livraison des conversations google chat, routage et livraison des conversations.

Note de catégorie : [Routage et livraison des conversations](space-routing-mentions-and-session-isolation.md)

Décisions de score :

- Couverture : `Alpha (55%)`
- Qualité : `Alpha (50%)`
- Complétude : `Alpha (55%)`
- LTS : ❌

Fonctionnalités :

- Routage et livraison des conversations : Portée des preuves pour le routage et la livraison des conversations.

Documentation principale :

- `docs/channels/googlechat.md`
- `docs/channels/bot-loop-protection.md`
- `docs/channels/access-groups.md`
- `docs/channels/channel-routing.md`

### 4. Médias et contenu enrichi

Ancres de recherche : médias et contenu enrichi google chat, médias et contenu enrichi.

Note de catégorie : [Médias et contenu enrichi](media-attachments-and-file-transfer.md)

Décisions de score :

- Couverture : `Alpha (55%)`
- Qualité : `Alpha (50%)`
- Complétude : `Alpha (55%)`
- LTS : ❌

Fonctionnalités :

- Médias et contenu enrichi : Portée des preuves pour les médias et le contenu enrichi.

Documentation principale :

- `docs/channels/googlechat.md`
- `docs/cli/message.md`
- `docs/nodes/media-understanding.md`
- `docs/reference/secretref-credential-surface.md`

### 5. Contrôles natifs et approbations

Ancres de recherche : Pièces jointes entrantes, Réponses médias sortantes, Action de téléchargement de message, Contrôles de source et de taille des médias, Reçus médias et placement dans les fils, Appairage DM, dm.policy, allowFrom, Action d'envoi de texte, Action de téléchargement de fichier, Actions de réaction, Portes de capacité d'action, Correspondance d'expéditeur d'approbation, Réponses conscientes des fils, Réponses en streaming et par chunks, Cycle de vie du placeholder de saisie, Réponses de source actuelle de l'outil de message, Nettoyage NO_REPLY, Rendu Markdown/texte.

Note de catégorie : [Contrôles natifs et approbations](message-actions-reactions-and-approval-auth.md)

Décisions de score :

- Couverture : `Alpha (55%)`
- Qualité : `Alpha (50%)`
- Complétude : `Alpha (55%)`
- LTS : ❌

Fonctionnalités :

- Pièces jointes entrantes : Couvre les pièces jointes entrantes dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file`, et le comportement connexe des pièces jointes médias et du transfert de fichiers.
- Réponses médias sortantes : Couvre les réponses médias sortantes dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file`, et le comportement connexe des pièces jointes médias et du transfert de fichiers.
- Action de téléchargement de message : Couvre l'action de téléchargement de message dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file`, et le comportement connexe des pièces jointes médias et du transfert de fichiers.
- Contrôles de source et de taille des médias : Couvre les contrôles de source et de taille des médias dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file`, et le comportement connexe des pièces jointes médias et du transfert de fichiers.
- Reçus médias et placement dans les fils : Couvre les reçus médias et le placement dans les fils dans le téléchargement de pièces jointes Google Chat, la remise du magasin de médias, la livraison des réponses médias sortantes, `upload-file`, et le comportement connexe des pièces jointes médias et du transfert de fichiers.
- Action d'envoi de texte : Couvre l'action d'envoi de texte dans la découverte d'action de l'outil de message Google Chat, `send`, `upload-file`, `react`, et le comportement connexe des actions de message, des réactions et de l'authentification d'approbation.
- Action de téléchargement de fichier : Couvre l'action de téléchargement de fichier dans la découverte d'action de l'outil de message Google Chat, `send`, `upload-file`, `react`, et le comportement connexe des actions de message, des réactions et de l'authentification d'approbation.
- Actions de réaction : Couvre les actions de réaction dans la découverte d'action de l'outil de message Google Chat, `send`, `upload-file`, `react`, et le comportement connexe des actions de message, des réactions et de l'authentification d'approbation.
- Portes de capacité d'action : Couvre les portes de capacité d'action dans la découverte d'action de l'outil de message Google Chat, `send`, `upload-file`, `react`, et le comportement connexe des actions de message, des réactions et de l'authentification d'approbation.
- Correspondance d'expéditeur d'approbation : Couvre la correspondance d'expéditeur d'approbation dans la découverte d'action de l'outil de message Google Chat, `send`, `upload-file`, `react`, et le comportement connexe des actions de message, des réactions et de l'authentification d'approbation.
- Réponses conscientes des fils : Couvre les réponses conscientes des fils dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte, et le comportement connexe des réponses en fil, du streaming et du cycle de vie de la saisie.
- Réponses en streaming et par chunks : Couvre les réponses en streaming et par chunks dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte, et le comportement connexe des réponses en fil, du streaming et du cycle de vie de la saisie.
- Cycle de vie du placeholder de saisie : Couvre le cycle de vie du placeholder de saisie dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte, et le comportement connexe des réponses en fil, du streaming et du cycle de vie de la saisie.
- Réponses de source actuelle de l'outil de message : Couvre les réponses de source actuelle de l'outil de message dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte, et le comportement connexe des réponses en fil, du streaming et du cycle de vie de la saisie.
- Nettoyage NO_REPLY : Couvre le nettoyage NO_REPLY dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte, et le comportement connexe des réponses en fil, du streaming et du cycle de vie de la saisie.
- Rendu Markdown/texte : Couvre le rendu Markdown/texte dans la propagation des ressources de fil entrant, `replyToMode`, Google Chat `messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`, chunking de texte, et le comportement connexe des réponses en fil, du streaming et du cycle de vie de la saisie.

Documentation principale :

- `docs/channels/googlechat.md`
- `docs/cli/message.md`
- `docs/nodes/media-understanding.md`
- `docs/reference/secretref-credential-surface.md`
- `docs/tools/reactions.md`
- `docs/tools/slash-commands.md`
- `docs/gateway/config-agents.md`
- `docs/concepts/message-lifecycle-refactor.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application de cette surface

- Redéfinition des limites de catégories de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance de l'audit

- Source du score :
  `docs/kevinslin/maturity-scorecard/inventory/google-chat/scores.yaml`.
- Source des métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source des preuves archivées :
  `/Users/kevinlin/tmp/maturity/google-chat`.
