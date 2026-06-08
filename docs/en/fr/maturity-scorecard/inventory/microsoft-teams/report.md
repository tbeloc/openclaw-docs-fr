---
title: "Rapport de Maturité Microsoft Teams"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Rapport de Maturité Microsoft Teams

## Scores de haut niveau

Ces agrégations sont des moyennes arithmétiques simples sur les scores
numériques des catégories dans `scores.yaml`. Les pourcentages sont arrondis
au nombre entier le plus proche.

- Couverture : `Alpha (62%)`
- Qualité : `Alpha (63%)`
- Complétude : `Alpha (62%)`
- Fonctionnalités LTS : `0/5`

## Résumé

Ce rapport promeut les preuves de maturité archivées `microsoft-teams` de `/Users/kevinlin/tmp/maturity/microsoft-teams` dans le contrat d'inventaire actuel de la version de processus 3.

Les scores de couverture et de qualité des catégories proviennent des lignes de score archivées soutenues par des preuves. La complétude est initialisée à partir de la même étendue des preuves archivées et du registre des lacunes connues, puis jointe avec le barème de complétude spécifique à la surface référencé par la taxonomie.

## Matrice

| Catégorie                                                                                           | LTS | Couverture    | Qualité       | Complétude    | Fonctionnalités à évaluer                                                                                                                                                                                                                     |
| -------------------------------------------------------------------------------------------------- | --- | ------------- | ------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Configuration et Opérations des Canaux](setup-app-registration-credentials-admin-install.md)                | ❌  | `Alpha (58%)` | `Alpha (64%)` | `Alpha (58%)` | Création d'application Teams CLI, Enregistrement de bot et téléchargement de manifeste, Configuration des identifiants, Vérification de l'installation de l'application Teams, État de la configuration, Rapports de sonde et d'étendue, Médecin d'application Teams, Diagnostics de webhook et de santé, Chemins de réparation des opérateurs |
| [Accès et Identité](dm-pairing-sender-authorization-config-writes.md)                            | ❌  | `Alpha (60%)` | `Alpha (62%)` | `Alpha (60%)` | Appairage DM, Identité d'expéditeur stable, Listes blanches et groupes d'accès, Autorisation d'invocation et de commande, Écritures de configuration d'origine Teams, Invocations SSO Bot Framework, Stockage de jetons délégués, Recherche dans le répertoire Graph, Recherche de profil de membre    |
| [Routage et Livraison des Conversations](team-channel-routing-mention-gates-sessions-thread-context.md) | ❌  | `Alpha (68%)` | `Alpha (66%)` | `Alpha (68%)` | Listes blanches d'équipes et de canaux, Réponses de canal déterministes, Accès aux groupes avec mention, Routage de session, Contexte de réponse et de thread                                                                                                        |
| [Médias et Contenu Enrichi](media-attachments-file-consent-graph-file-flows.md)                       | ❌  | `Alpha (62%)` | `Alpha (58%)` | `Alpha (62%)` | Pièces jointes entrantes, Médias hébergés sur Graph, Consentement de fichier, Partage SharePoint et OneDrive, Sécurité de la récupération de médias                                                                                                                               |
| [Contrôles Natifs et Approbations](actions-reactions-polls-approvals-group-management.md)             | ❌  | `Alpha (64%)` | `Alpha (66%)` | `Alpha (64%)` | Découverte d'actions de message, Sondages et réactions, Lecture, édition, suppression et épinglage, Cartes d'approbation natives, Actions de rétroaction et de groupe                                                                                                            |

## Barème de notation

- Couverture :
  évaluation du libellé de maturité pour l'intégration, e2e, en direct ou les
  preuves de flux serveur/runtime dans la catégorie. Les tests unitaires peuvent
  fournir un contexte de soutien mais ne rendent jamais une fonctionnalité
  couverte par eux-mêmes.
- Qualité :
  évaluation du libellé de maturité pour la robustesse de la mise en œuvre et
  opérationnelle. La couverture des tests unitaires, d'intégration, e2e, en
  direct et de flux runtime réel sont des entrées de couverture uniquement ; ils
  ne relèvent ni n'abaissent la qualité.
- Complétude :
  évaluation du libellé de maturité pour la façon dont la catégorie livre
  complètement l'ensemble de capacités spécifiques à la surface prévue.
  Utilisez les instructions de complétude liées à la taxonomie pour cette
  surface.
- LTS :
  calculé comme `quality > 80 and coverage > 90`, ou lorsque la catégorie de
  taxonomie correspondante définit `human_lts_override`.
- Bandes de score partagées :
  `Lovable = 95-100`, `Stable = 80-95`, `Beta = 70-80`,
  `Alpha = 50-70`, et `Experimental = 0-50`. Aux limites partagées, choisissez
  le libellé de maturité plus élevé.
- Lacunes majeures de qualité/complétude :
  texte de preuve uniquement, suivi dans l'inventaire des fonctionnalités
  détaillées plutôt que comme une dimension notée séparée.

## Inventaire détaillé des fonctionnalités

### 1. Configuration et opérations des canaux

Ancres de recherche : Configuration rapide, création d'application teams, enregistrement d'application, enregistrement de bot, manifeste d'application Teams, permissions RSC, génération de credentials, Configurer OpenClaw, MSTEAMS_APP_ID, channels.msteams, Installer l'application dans Teams, teams app doctor, Statut de configuration, Rapports de sonde et de portée, Teams app doctor, Diagnostics de webhook et de santé, Chemins de réparation d'opérateur.

Note de catégorie : [Configuration et opérations des canaux](setup-app-registration-credentials-admin-install.md)

Décisions de score :

- Couverture : `Alpha (58%)`
- Qualité : `Alpha (64%)`
- Complétude : `Alpha (58%)`
- LTS : ❌

Fonctionnalités :

- Création d'application Teams CLI : Couvre l'installation du canal Microsoft Teams via `teams app create`, l'enregistrement de bot, la création de manifeste, la génération de credentials et la vérification de configuration.
- Enregistrement de bot et téléchargement de manifeste : Couvre l'enregistrement d'application Entra ID, la configuration d'Azure Bot, les permissions de manifeste/RSC d'application Teams et le téléchargement de package d'application Teams.
- Configuration des credentials : Couvre CLIENT_ID, CLIENT_SECRET, TENANT_ID, variables d'environnement `MSTEAMS_*`, et la configuration des credentials `channels.msteams` d'OpenClaw.
- Vérification d'installation d'application Teams : Couvre les liens d'installation Teams, l'installation d'application dans Teams et la vérification `teams app doctor` après la configuration.
- Statut de configuration : Couvre le statut de configuration dans l'assistant de configuration, les invites de credentials, la détection de credentials d'environnement, la documentation de configuration et les diagnostics et comportements de réparation associés.
- Rapports de sonde et de portée : Couvre les rapports de sonde et de portée dans l'assistant de configuration, les invites de credentials, la détection de credentials d'environnement, la documentation de configuration et les diagnostics et comportements de réparation associés.
- Teams app doctor : Couvre Teams app doctor dans l'assistant de configuration, les invites de credentials, la détection de credentials d'environnement, la documentation de configuration et les diagnostics et comportements de réparation associés.
- Diagnostics de webhook et de santé : Couvre les diagnostics de webhook et de santé dans l'assistant de configuration, les invites de credentials, la détection de credentials d'environnement, la documentation de configuration et les diagnostics et comportements de réparation associés.
- Chemins de réparation d'opérateur : Couvre les chemins de réparation d'opérateur dans l'assistant de configuration, les invites de credentials, la détection de credentials d'environnement, la documentation de configuration et les diagnostics et comportements de réparation associés.

Documentation principale :

- `docs/channels/msteams.md`
- `docs/plugins/reference/msteams.md`
- `docs/gateway/config-channels.md`
- `docs/gateway/health.md`

### 2. Accès et identité

Ancres de recherche : Appairage DM, Identité d'expéditeur stable, Listes blanches et groupes d'accès, Autorisation d'invocation et de commande, Écritures de configuration originaires de Teams, Invocations SSO Bot Framework, Échange de token OAuth, Stockage de token délégué, Résolution de token d'application Graph, Informations de membre.

Note de catégorie : [Accès et identité](dm-pairing-sender-authorization-config-writes.md)

Décisions de score :

- Couverture : `Alpha (60%)`
- Qualité : `Alpha (62%)`
- Complétude : `Alpha (60%)`
- LTS : ❌

Fonctionnalités :

- Appairage DM : Couvre l'appairage DM dans l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et le comportement d'appairage DM et d'accès d'expéditeur associé.
- Identité d'expéditeur stable : Couvre l'identité d'expéditeur stable dans l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et le comportement d'appairage DM et d'accès d'expéditeur associé.
- Listes blanches et groupes d'accès : Couvre les listes blanches et groupes d'accès dans l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et le comportement d'appairage DM et d'accès d'expéditeur associé.
- Autorisation d'invocation et de commande : Couvre l'autorisation d'invocation et de commande dans l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et le comportement d'appairage DM et d'accès d'expéditeur associé.
- Écritures de configuration originaires de Teams : Couvre les écritures de configuration originaires de Teams dans l'appairage DM, `dmPolicy`, `allowFrom`, correspondance d'ID AAD et le comportement d'appairage DM et d'accès d'expéditeur associé.
- Invocations SSO Bot Framework : Couvre la gestion des invocations SSO Bot Framework et l'échange de token OAuth pour les utilisateurs Microsoft Teams.
- Stockage de token délégué : Couvre le stockage de token délégué, l'actualisation de token et la récupération pour l'authentification d'utilisateur Microsoft Teams.
- Recherche dans le répertoire Graph : Couvre la résolution de token d'application Graph et le comportement de recherche dans le répertoire pour le routage Teams et les métadonnées d'utilisateur.
- Recherche de profil de membre : Couvre la recherche d'informations de membre et la récupération de métadonnées d'utilisateur pour les conversations Microsoft Teams.

Documentation principale :

- `docs/channels/msteams.md`
- `docs/channels/pairing.md`
- `docs/channels/access-groups.md`

### 3. Routage et livraison de conversations

Ancres de recherche : Liste blanche Teams + canal, routage déterministe, les réponses reviennent toujours au canal, mention-gated, Formes de clé de session, groupPolicy, groupAllowFrom, requireMention, routage de canal, Contexte de réponse.

Note de catégorie : [Routage et livraison de conversations](team-channel-routing-mention-gates-sessions-thread-context.md)

Décisions de score :

- Couverture : `Alpha (68%)`
- Qualité : `Alpha (66%)`
- Complétude : `Alpha (68%)`
- LTS : ❌

Fonctionnalités :

- Listes blanches d'équipe et de canal : Couvre les listes blanches Teams/canal, les ID de conversation stables, `channels.msteams.teams`, le routage avec caractères génériques et la résolution de noms d'équipe/canal.
- Réponses de canal déterministes : Couvre le routage de réponse déterministe vers le canal Teams où un message est arrivé et les protections de routage avec caractères génériques.
- Accès à groupe avec mention-gated : Couvre `groupPolicy`, `groupAllowFrom`, `requireMention` et les réponses de groupe ou canal avec mention-gated.
- Routage de session : Couvre le routage de réponse déterministe, les clés de session, les liaisons de canal et l'isolation de conversation pour les salles et canaux Microsoft Teams.
- Contexte de réponse et de thread : Couvre le contexte de réponse, les messages source cités, le routage conscient des threads et le contexte de salle pour les conversations Teams.

Documentation principale :

- `docs/channels/msteams.md`
- `docs/channels/groups.md`
- `docs/channels/channel-routing.md`

### 4. Médias et contenu enrichi

Ancres de recherche : Pièces jointes entrantes, Médias hébergés par Graph, Consentement de fichier, Partage SharePoint et OneDrive, Sécurité de récupération de médias.

Note de catégorie : [Médias et contenu enrichi](media-attachments-file-consent-graph-file-flows.md)

Décisions de score :

- Couverture : `Alpha (62%)`
- Qualité : `Alpha (58%)`
- Complétude : `Alpha (62%)`
- LTS : ❌

Fonctionnalités :

- Pièces jointes entrantes : Couvre les pièces jointes entrantes dans les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph et le comportement de partage de médias et de fichiers associé.
- Médias hébergés par Graph : Couvre les médias hébergés par Graph dans les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph et le comportement de partage de médias et de fichiers associé.
- Consentement de fichier : Couvre le consentement de fichier dans les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph et le comportement de partage de médias et de fichiers associé.
- Partage SharePoint et OneDrive : Couvre le partage SharePoint et OneDrive dans les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph et le comportement de partage de médias et de fichiers associé.
- Sécurité de récupération de médias : Couvre la sécurité de récupération de médias dans les pièces jointes entrantes, les images en ligne, les espaces réservés `msteams://media`, le contenu hébergé par Graph et le comportement de partage de médias et de fichiers associé.

Documentation principale :

- `docs/channels/msteams.md`

### 5. Contrôles natifs et approbations

Ancres de recherche : Découverte d'action de message, Sondages et réactions, Lire, modifier, supprimer et épingler, Cartes d'approbation natives, Retours et actions de groupe.

Note de catégorie : [Contrôles natifs et approbations](actions-reactions-polls-approvals-group-management.md)

Décisions de score :

- Couverture : `Alpha (64%)`
- Qualité : `Alpha (66%)`
- Complétude : `Alpha (64%)`
- LTS : ❌

Fonctionnalités :

- Découverte d'action de message : Couvre la découverte d'action de message dans la découverte d'outil de message, téléchargement de fichier, sondage, lecture/recherche et le comportement d'actions et d'approbations associé.
- Sondages et réactions : Couvre les sondages et réactions dans la découverte d'outil de message, téléchargement de fichier, sondage, lecture/recherche et le comportement d'actions et d'approbations associé.
- Lire, modifier, supprimer et épingler : Couvre la lecture, la modification, la suppression et l'épinglage dans la découverte d'outil de message, téléchargement de fichier, sondage, lecture/recherche et le comportement d'actions et d'approbations associé.
- Cartes d'approbation natives : Couvre les cartes d'approbation natives dans la découverte d'outil de message, téléchargement de fichier, sondage, lecture/recherche et le comportement d'actions et d'approbations associé.
- Retours et actions de groupe : Couvre les retours et actions de groupe dans la découverte d'outil de message, téléchargement de fichier, sondage, lecture/recherche et le comportement d'actions et d'approbations associé.

Documentation principale :

- `docs/channels/msteams.md`
- `docs/tools/exec-approvals-advanced.md`

## Interprétation recommandée de la fiche d'évaluation

Utilisez ce score migré comme base d'inventaire actuelle. Actualisez les catégories individuelles avec une recherche d'agent de catégorie en direct avant de traiter un score élevé comme une porte de promotion LTS.

## Hors du champ d'application pour cette surface

- Redéfinition des limites de catégorie de taxonomie ; la taxonomie reste la source de vérité pour l'identité de catégorie, les fonctionnalités, la documentation et les ancres de recherche.

## Provenance d'audit

- Source de score :
  `docs/kevinslin/maturity-scorecard/inventory/microsoft-teams/scores.yaml`.
- Source de métadonnées de taxonomie :
  `.agents/skills/claw-score/taxonomy.yaml`.
- Source de preuve archivée :
  `/Users/kevinlin/tmp/maturity/microsoft-teams`.
