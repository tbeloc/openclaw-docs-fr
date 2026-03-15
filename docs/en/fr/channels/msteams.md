---
summary: "État du support des bots Microsoft Teams, capacités et configuration"
read_when:
  - Working on MS Teams channel features
title: "Microsoft Teams"
---

# Microsoft Teams (plugin)

> "Abandon all hope, ye who enter here."

Mis à jour : 2026-01-21

État : texte + pièces jointes DM sont supportés ; l'envoi de fichiers dans les chats de groupe/canal nécessite `sharePointSiteId` + permissions Graph (voir [Envoi de fichiers dans les chats de groupe](#sending-files-in-group-chats)). Les sondages sont envoyés via Adaptive Cards.

## Plugin requis

Microsoft Teams est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

**Changement majeur (2026.1.15) :** MS Teams a été retiré du noyau. Si vous l'utilisez, vous devez installer le plugin.

Justification : cela maintient les installations principales plus légères et permet aux dépendances de MS Teams de se mettre à jour indépendamment.

Installez via CLI (registre npm) :

```bash
openclaw plugins install @openclaw/msteams
```

Checkout local (lors de l'exécution à partir d'un dépôt git) :

```bash
openclaw plugins install ./extensions/msteams
```

Si vous choisissez Teams lors de la configuration/intégration et qu'un checkout git est détecté,
OpenClaw proposera automatiquement le chemin d'installation local.

Détails : [Plugins](/fr/tools/plugin)

## Configuration rapide (débutant)

1. Installez le plugin Microsoft Teams.
2. Créez un **Azure Bot** (ID d'application + secret client + ID de locataire).
3. Configurez OpenClaw avec ces identifiants.
4. Exposez `/api/messages` (port 3978 par défaut) via une URL publique ou un tunnel.
5. Installez le package d'application Teams et démarrez la passerelle.

Configuration minimale :

```json5
{
  channels: {
    msteams: {
      enabled: true,
      appId: "<APP_ID>",
      appPassword: "<APP_PASSWORD>",
      tenantId: "<TENANT_ID>",
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

Remarque : les chats de groupe sont bloqués par défaut (`channels.msteams.groupPolicy: "allowlist"`). Pour autoriser les réponses de groupe, définissez `channels.msteams.groupAllowFrom` (ou utilisez `groupPolicy: "open"` pour autoriser tout membre, avec mention obligatoire).

## Objectifs

- Communiquer avec OpenClaw via les DM Teams, les chats de groupe ou les canaux.
- Maintenir le routage déterministe : les réponses reviennent toujours au canal d'où elles proviennent.
- Adopter par défaut un comportement de canal sûr (mentions requises sauf configuration contraire).

## Écritures de configuration

Par défaut, Microsoft Teams est autorisé à écrire les mises à jour de configuration déclenchées par `/config set|unset` (nécessite `commands.config: true`).

Désactivez avec :

```json5
{
  channels: { msteams: { configWrites: false } },
}
```

## Contrôle d'accès (DM + groupes)

**Accès DM**

- Par défaut : `channels.msteams.dmPolicy = "pairing"`. Les expéditeurs inconnus sont ignorés jusqu'à approbation.
- `channels.msteams.allowFrom` doit utiliser des ID d'objet AAD stables.
- Les UPN/noms d'affichage sont mutables ; la correspondance directe est désactivée par défaut et n'est activée qu'avec `channels.msteams.dangerouslyAllowNameMatching: true`.
- L'assistant peut résoudre les noms en ID via Microsoft Graph lorsque les identifiants le permettent.

**Accès groupe**

- Par défaut : `channels.msteams.groupPolicy = "allowlist"` (bloqué sauf si vous ajoutez `groupAllowFrom`). Utilisez `channels.defaults.groupPolicy` pour remplacer la valeur par défaut si elle n'est pas définie.
- `channels.msteams.groupAllowFrom` contrôle quels expéditeurs peuvent déclencher dans les chats/canaux de groupe (revient à `channels.msteams.allowFrom`).
- Définissez `groupPolicy: "open"` pour autoriser tout membre (mention obligatoire par défaut).
- Pour autoriser **aucun canal**, définissez `channels.msteams.groupPolicy: "disabled"`.

Exemple :

```json5
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
    },
  },
}
```

**Liste blanche Teams + canal**

- Limitez les réponses de groupe/canal en listant les équipes et canaux sous `channels.msteams.teams`.
- Les clés doivent utiliser des ID d'équipe stables et des ID de conversation de canal.
- Lorsque `groupPolicy="allowlist"` et qu'une liste blanche d'équipes est présente, seules les équipes/canaux listés sont acceptés (mention obligatoire).
- L'assistant de configuration accepte les entrées `Team/Channel` et les stocke pour vous.
- Au démarrage, OpenClaw résout les noms de liste blanche d'équipe/canal et d'utilisateur en ID (lorsque les permissions Graph le permettent)
  et enregistre le mappage ; les noms d'équipe/canal non résolus sont conservés tels que saisis mais ignorés pour le routage par défaut sauf si `channels.msteams.dangerouslyAllowNameMatching: true` est activé.

Exemple :

```json5
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      teams: {
        "My Team": {
          channels: {
            General: { requireMention: true },
          },
        },
      },
    },
  },
}
```

## Fonctionnement

1. Installez le plugin Microsoft Teams.
2. Créez un **Azure Bot** (ID d'application + secret + ID de locataire).
3. Créez un **package d'application Teams** qui référence le bot et inclut les permissions RSC ci-dessous.
4. Téléchargez/installez l'application Teams dans une équipe (ou portée personnelle pour les DM).
5. Configurez `msteams` dans `~/.openclaw/openclaw.json` (ou variables d'environnement) et démarrez la passerelle.
6. La passerelle écoute le trafic webhook Bot Framework sur `/api/messages` par défaut.

## Configuration Azure Bot (Prérequis)

Avant de configurer OpenClaw, vous devez créer une ressource Azure Bot.

### Étape 1 : Créer Azure Bot

1. Allez à [Créer Azure Bot](https://portal.azure.com/#create/Microsoft.AzureBot)
2. Remplissez l'onglet **Bases** :

   | Champ              | Valeur                                                    |
   | ------------------ | -------------------------------------------------------- |
   | **Identifiant du bot**     | Nom de votre bot, par ex. `openclaw-msteams` (doit être unique) |
   | **Abonnement**   | Sélectionnez votre abonnement Azure                           |
   | **Groupe de ressources** | Créer nouveau ou utiliser existant                               |
   | **Niveau tarifaire**   | **Gratuit** pour dev/test                                 |
   | **Type d'application**    | **Locataire unique** (recommandé - voir remarque ci-dessous)         |
   | **Type de création**  | **Créer un nouvel ID d'application Microsoft**                          |

> **Avis de dépréciation :** La création de nouveaux bots multi-locataires a été dépréciée après 2025-07-31. Utilisez **Locataire unique** pour les nouveaux bots.

3. Cliquez sur **Vérifier + créer** → **Créer** (attendez ~1-2 minutes)

### Étape 2 : Obtenir les identifiants

1. Allez à votre ressource Azure Bot → **Configuration**
2. Copiez **ID d'application Microsoft** → c'est votre `appId`
3. Cliquez sur **Gérer le mot de passe** → allez à l'enregistrement d'application
4. Sous **Certificats et secrets** → **Nouveau secret client** → copiez la **Valeur** → c'est votre `appPassword`
5. Allez à **Aperçu** → copiez **ID du répertoire (locataire)** → c'est votre `tenantId`

### Étape 3 : Configurer le point de terminaison de messagerie

1. Dans Azure Bot → **Configuration**
2. Définissez **Point de terminaison de messagerie** sur votre URL webhook :
   - Production : `https://your-domain.com/api/messages`
   - Dev local : Utilisez un tunnel (voir [Développement local](#local-development-tunneling) ci-dessous)

### Étape 4 : Activer le canal Teams

1. Dans Azure Bot → **Canaux**
2. Cliquez sur **Microsoft Teams** → Configurer → Enregistrer
3. Acceptez les conditions d'utilisation

## Développement local (Tunneling)

Teams ne peut pas atteindre `localhost`. Utilisez un tunnel pour le développement local :

**Option A : ngrok**

```bash
ngrok http 3978
# Copiez l'URL https, par ex. https://abc123.ngrok.io
# Définissez le point de terminaison de messagerie sur : https://abc123.ngrok.io/api/messages
```

**Option B : Tailscale Funnel**

```bash
tailscale funnel 3978
# Utilisez votre URL Tailscale funnel comme point de terminaison de messagerie
```

## Portail des développeurs Teams (Alternative)

Au lieu de créer manuellement un ZIP de manifeste, vous pouvez utiliser le [Portail des développeurs Teams](https://dev.teams.microsoft.com/apps) :

1. Cliquez sur **+ Nouvelle application**
2. Remplissez les informations de base (nom, description, informations développeur)
3. Allez à **Fonctionnalités d'application** → **Bot**
4. Sélectionnez **Entrer un ID de bot manuellement** et collez votre ID d'application Azure Bot
5. Vérifiez les portées : **Personnel**, **Équipe**, **Chat de groupe**
6. Cliquez sur **Distribuer** → **Télécharger le package d'application**
7. Dans Teams : **Applications** → **Gérer vos applications** → **Télécharger une application personnalisée** → sélectionnez le ZIP

C'est souvent plus facile que de modifier manuellement les manifestes JSON.

## Test du bot

**Option A : Web Chat Azure (vérifier d'abord le webhook)**

1. Dans le portail Azure → votre ressource Azure Bot → **Tester dans Web Chat**
2. Envoyez un message - vous devriez voir une réponse
3. Cela confirme que votre point de terminaison webhook fonctionne avant la configuration Teams

**Option B : Teams (après installation de l'application)**

1. Installez l'application Teams (chargement indépendant ou catalogue organisationnel)
2. Trouvez le bot dans Teams et envoyez un DM
3. Vérifiez les journaux de la passerelle pour l'activité entrante

## Configuration (texte minimal uniquement)

1. **Installez le plugin Microsoft Teams**
   - Depuis npm : `openclaw plugins install @openclaw/msteams`
   - Depuis un checkout local : `openclaw plugins install ./extensions/msteams`

2. **Enregistrement du bot**
   - Créez un Azure Bot (voir ci-dessus) et notez :
     - ID d'application
     - Secret client (mot de passe d'application)
     - ID de locataire (locataire unique)

3. **Manifeste d'application Teams**
   - Incluez une entrée `bot` avec `botId = <App ID>`.
   - Portées : `personal`, `team`, `groupChat`.
   - `supportsFiles: true` (requis pour la gestion des fichiers en portée personnelle).
   - Ajoutez les permissions RSC (ci-dessous).
   - Créez des icônes : `outline.png` (32x32) et `color.png` (192x192).
   - Zippez les trois fichiers ensemble : `manifest.json`, `outline.png`, `color.png`.

4. **Configurez OpenClaw**

   ```json
   {
     "msteams": {
       "enabled": true,
       "appId": "<APP_ID>",
       "appPassword": "<APP_PASSWORD>",
       "tenantId": "<TENANT_ID>",
       "webhook": { "port": 3978, "path": "/api/messages" }
     }
   }
   ```

   Vous pouvez également utiliser des variables d'environnement au lieu de clés de configuration :
   - `MSTEAMS_APP_ID`
   - `MSTEAMS_APP_PASSWORD`
   - `MSTEAMS_TENANT_ID`

5. **Point de terminaison du bot**
   - Définissez le point de terminaison de messagerie Azure Bot sur :
     - `https://<host>:3978/api/messages` (ou votre chemin/port choisi).

6. **Exécutez la passerelle**
   - Le canal Teams démarre automatiquement lorsque le plugin est installé et que la configuration `msteams` existe avec les identifiants.

## Contexte de l'historique

- `channels.msteams.historyLimit` contrôle le nombre de messages récents de canal/groupe enveloppés dans l'invite.
- Revient à `messages.groupChat.historyLimit`. Définissez `0` pour désactiver (par défaut 50).
- L'historique DM peut être limité avec `channels.msteams.dmHistoryLimit` (tours utilisateur). Remplacements par utilisateur : `channels.msteams.dms["<user_id>"].historyLimit`.

## Permissions RSC Teams actuelles (Manifeste)

Ce sont les **permissions spécifiques aux ressources** existantes dans notre manifeste d'application Teams. Elles s'appliquent uniquement dans l'équipe/chat où l'application est installée.

**Pour les canaux (portée d'équipe) :**

- `ChannelMessage.Read.Group` (Application) - recevoir tous les messages de canal sans @mention
- `ChannelMessage.Send.Group` (Application)
- `Member.Read.Group` (Application)
- `Owner.Read.Group` (Application)
- `ChannelSettings.Read.Group` (Application)
- `TeamMember.Read.Group` (Application)
- `TeamSettings.Read.Group` (Application)

**Pour les chats de groupe :**

- `ChatMessage.Read.Chat` (Application) - recevoir tous les messages de chat de groupe sans @mention

## Exemple de manifeste Teams (masqué)

Exemple minimal et valide avec les champs requis. Remplacez les IDs et les URLs.

```json
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.23/MicrosoftTeams.schema.json",
  "manifestVersion": "1.23",
  "version": "1.0.0",
  "id": "00000000-0000-0000-0000-000000000000",
  "name": { "short": "OpenClaw" },
  "developer": {
    "name": "Your Org",
    "websiteUrl": "https://example.com",
    "privacyUrl": "https://example.com/privacy",
    "termsOfUseUrl": "https://example.com/terms"
  },
  "description": { "short": "OpenClaw in Teams", "full": "OpenClaw in Teams" },
  "icons": { "outline": "outline.png", "color": "color.png" },
  "accentColor": "#5B6DEF",
  "bots": [
    {
      "botId": "11111111-1111-1111-1111-111111111111",
      "scopes": ["personal", "team", "groupChat"],
      "isNotificationOnly": false,
      "supportsCalling": false,
      "supportsVideo": false,
      "supportsFiles": true
    }
  ],
  "webApplicationInfo": {
    "id": "11111111-1111-1111-1111-111111111111"
  },
  "authorization": {
    "permissions": {
      "resourceSpecific": [
        { "name": "ChannelMessage.Read.Group", "type": "Application" },
        { "name": "ChannelMessage.Send.Group", "type": "Application" },
        { "name": "Member.Read.Group", "type": "Application" },
        { "name": "Owner.Read.Group", "type": "Application" },
        { "name": "ChannelSettings.Read.Group", "type": "Application" },
        { "name": "TeamMember.Read.Group", "type": "Application" },
        { "name": "TeamSettings.Read.Group", "type": "Application" },
        { "name": "ChatMessage.Read.Chat", "type": "Application" }
      ]
    }
  }
}
```

### Avertissements du manifeste (champs obligatoires)

- `bots[].botId` **doit** correspondre à l'ID d'application Azure Bot.
- `webApplicationInfo.id` **doit** correspondre à l'ID d'application Azure Bot.
- `bots[].scopes` doit inclure les surfaces que vous prévoyez d'utiliser (`personal`, `team`, `groupChat`).
- `bots[].supportsFiles: true` est requis pour la gestion des fichiers dans la portée personnelle.
- `authorization.permissions.resourceSpecific` doit inclure la lecture/envoi de canal si vous souhaitez le trafic de canal.

### Mise à jour d'une application existante

Pour mettre à jour une application Teams déjà installée (par exemple, pour ajouter des permissions RSC) :

1. Mettez à jour votre `manifest.json` avec les nouveaux paramètres
2. **Incrémentez le champ `version`** (par exemple, `1.0.0` → `1.1.0`)
3. **Re-zippez** le manifeste avec les icônes (`manifest.json`, `outline.png`, `color.png`)
4. Téléchargez le nouveau zip :
   - **Option A (Centre d'administration Teams) :** Centre d'administration Teams → Applications Teams → Gérer les applications → trouvez votre application → Télécharger une nouvelle version
   - **Option B (Chargement latéral) :** Dans Teams → Applications → Gérer vos applications → Télécharger une application personnalisée
5. **Pour les canaux d'équipe :** Réinstallez l'application dans chaque équipe pour que les nouvelles permissions prennent effet
6. **Quittez complètement et relancez Teams** (pas seulement fermer la fenêtre) pour effacer les métadonnées d'application en cache

## Capacités : RSC uniquement vs Graph

### Avec **Teams RSC uniquement** (application installée, sans permissions API Graph)

Fonctionne :

- Lire le contenu **texte** des messages de canal.
- Envoyer du contenu **texte** des messages de canal.
- Recevoir les pièces jointes de fichiers **personnelles (DM)**.

Ne fonctionne PAS :

- Contenu **image ou fichier** du canal/groupe (la charge utile inclut uniquement un stub HTML).
- Téléchargement des pièces jointes stockées dans SharePoint/OneDrive.
- Lecture de l'historique des messages (au-delà de l'événement webhook en direct).

### Avec **Teams RSC + permissions d'application Microsoft Graph**

Ajoute :

- Téléchargement des contenus hébergés (images collées dans les messages).
- Téléchargement des pièces jointes stockées dans SharePoint/OneDrive.
- Lecture de l'historique des messages de canal/chat via Graph.

### RSC vs API Graph

| Capacité                | Permissions RSC      | API Graph                           |
| ----------------------- | -------------------- | ----------------------------------- |
| **Messages en temps réel** | Oui (via webhook)    | Non (sondage uniquement)            |
| **Messages historiques** | Non                  | Oui (peut interroger l'historique)  |
| **Complexité de configuration** | Manifeste d'application uniquement | Nécessite le consentement administrateur + flux de jeton |
| **Fonctionne hors ligne** | Non (doit être en cours d'exécution) | Oui (interroger à tout moment)      |

**En résumé :** RSC est pour l'écoute en temps réel ; l'API Graph est pour l'accès historique. Pour rattraper les messages manqués hors ligne, vous avez besoin de l'API Graph avec `ChannelMessage.Read.All` (nécessite le consentement administrateur).

## Médias activés par Graph + historique (requis pour les canaux)

Si vous avez besoin d'images/fichiers dans les **canaux** ou si vous souhaitez récupérer l'**historique des messages**, vous devez activer les permissions Microsoft Graph et accorder le consentement administrateur.

1. Dans l'**enregistrement d'application** Entra ID (Azure AD), ajoutez les permissions d'**application** Microsoft Graph :
   - `ChannelMessage.Read.All` (pièces jointes de canal + historique)
   - `Chat.Read.All` ou `ChatMessage.Read.All` (chats de groupe)
2. **Accordez le consentement administrateur** pour le locataire.
3. Augmentez la **version du manifeste** de l'application Teams, re-téléchargez et **réinstallez l'application dans Teams**.
4. **Quittez complètement et relancez Teams** pour effacer les métadonnées d'application en cache.

**Permission supplémentaire pour les mentions d'utilisateurs :** Les mentions @utilisateurs fonctionnent directement pour les utilisateurs dans la conversation. Cependant, si vous souhaitez rechercher et mentionner dynamiquement des utilisateurs qui ne sont **pas dans la conversation actuelle**, ajoutez la permission `User.Read.All` (Application) et accordez le consentement administrateur.

## Limitations connues

### Délais d'expiration du webhook

Teams livre les messages via webhook HTTP. Si le traitement prend trop de temps (par exemple, réponses LLM lentes), vous pouvez voir :

- Délais d'expiration de la passerelle
- Teams réessayant le message (causant des doublons)
- Réponses supprimées

OpenClaw gère cela en revenant rapidement et en envoyant des réponses de manière proactive, mais les réponses très lentes peuvent toujours causer des problèmes.

### Formatage

Le markdown Teams est plus limité que Slack ou Discord :

- Le formatage de base fonctionne : **gras**, _italique_, `code`, liens
- Le markdown complexe (tableaux, listes imbriquées) peut ne pas s'afficher correctement
- Les cartes adaptatives sont prises en charge pour les sondages et les envois de cartes arbitraires (voir ci-dessous)

## Configuration

Paramètres clés (voir `/gateway/configuration` pour les modèles de canal partagé) :

- `channels.msteams.enabled` : activer/désactiver le canal.
- `channels.msteams.appId`, `channels.msteams.appPassword`, `channels.msteams.tenantId` : identifiants du bot.
- `channels.msteams.webhook.port` (par défaut `3978`)
- `channels.msteams.webhook.path` (par défaut `/api/messages`)
- `channels.msteams.dmPolicy` : `pairing | allowlist | open | disabled` (par défaut : pairing)
- `channels.msteams.allowFrom` : liste d'autorisation DM (IDs d'objet AAD recommandés). L'assistant résout les noms en IDs lors de la configuration lorsque l'accès Graph est disponible.
- `channels.msteams.dangerouslyAllowNameMatching` : basculer de secours pour réactiver la correspondance UPN/nom d'affichage mutable et le routage direct du nom d'équipe/canal.
- `channels.msteams.textChunkLimit` : taille du bloc de texte sortant.
- `channels.msteams.chunkMode` : `length` (par défaut) ou `newline` pour diviser sur les lignes vides (limites de paragraphe) avant le chunking de longueur.
- `channels.msteams.mediaAllowHosts` : liste d'autorisation pour les hôtes de pièces jointes entrantes (par défaut les domaines Microsoft/Teams).
- `channels.msteams.mediaAuthAllowHosts` : liste d'autorisation pour joindre les en-têtes d'autorisation sur les tentatives de média (par défaut les hôtes Graph + Bot Framework).
- `channels.msteams.requireMention` : exiger @mention dans les canaux/groupes (par défaut true).
- `channels.msteams.replyStyle` : `thread | top-level` (voir [Style de réponse](#reply-style-threads-vs-posts)).
- `channels.msteams.teams.<teamId>.replyStyle` : remplacement par équipe.
- `channels.msteams.teams.<teamId>.requireMention` : remplacement par équipe.
- `channels.msteams.teams.<teamId>.tools` : remplacements de politique d'outil par défaut par équipe (`allow`/`deny`/`alsoAllow`) utilisés lorsqu'un remplacement de canal est manquant.
- `channels.msteams.teams.<teamId>.toolsBySender` : remplacements de politique d'outil par défaut par équipe par expéditeur (wildcard `"*"` supporté).
- `channels.msteams.teams.<teamId>.channels.<conversationId>.replyStyle` : remplacement par canal.
- `channels.msteams.teams.<teamId>.channels.<conversationId>.requireMention` : remplacement par canal.
- `channels.msteams.teams.<teamId>.channels.<conversationId>.tools` : remplacements de politique d'outil par canal (`allow`/`deny`/`alsoAllow`).
- `channels.msteams.teams.<teamId>.channels.<conversationId>.toolsBySender` : remplacements de politique d'outil par canal par expéditeur (wildcard `"*"` supporté).
- Les clés `toolsBySender` doivent utiliser des préfixes explicites :
  `id:`, `e164:`, `username:`, `name:` (les clés non préfixées héritées mappent toujours à `id:` uniquement).
- `channels.msteams.sharePointSiteId` : ID du site SharePoint pour les téléchargements de fichiers dans les chats de groupe/canaux (voir [Envoi de fichiers dans les chats de groupe](#sending-files-in-group-chats)).

## Routage et sessions

- Les clés de session suivent le format d'agent standard (voir [/concepts/session](/fr/concepts/session)) :
  - Les messages directs partagent la session principale (`agent:<agentId>:<mainKey>`).
  - Les messages de canal/groupe utilisent l'ID de conversation :
    - `agent:<agentId>:msteams:channel:<conversationId>`
    - `agent:<agentId>:msteams:group:<conversationId>`

## Style de réponse : Threads vs Posts

Teams a récemment introduit deux styles d'interface utilisateur de canal sur le même modèle de données sous-jacent :

| Style                    | Description                                               | `replyStyle` recommandé |
| ------------------------ | --------------------------------------------------------- | ----------------------- |
| **Posts** (classique)    | Les messages apparaissent sous forme de cartes avec des réponses en thread en dessous | `thread` (par défaut)   |
| **Threads** (style Slack) | Les messages s'écoulent linéairement, plus comme Slack    | `top-level`             |

**Le problème :** L'API Teams n'expose pas quel style d'interface utilisateur un canal utilise. Si vous utilisez le mauvais `replyStyle` :

- `thread` dans un canal de style Threads → les réponses apparaissent imbriquées maladroitement
- `top-level` dans un canal de style Posts → les réponses apparaissent comme des posts de niveau supérieur séparés au lieu d'être en thread

**Solution :** Configurez `replyStyle` par canal en fonction de la façon dont le canal est configuré :

```json
{
  "msteams": {
    "replyStyle": "thread",
    "teams": {
      "19:abc...@thread.tacv2": {
        "channels": {
          "19:xyz...@thread.tacv2": {
            "replyStyle": "top-level"
          }
        }
      }
    }
  }
}
```

## Pièces jointes et images

**Limitations actuelles :**

- **DMs :** Les images et les pièces jointes fonctionnent via les API de fichiers du bot Teams.
- **Canaux/groupes :** Les pièces jointes vivent dans le stockage M365 (SharePoint/OneDrive). La charge utile du webhook inclut uniquement un stub HTML, pas les octets de fichier réels. **Les permissions API Graph sont requises** pour télécharger les pièces jointes de canal.

Sans permissions Graph, les messages de canal avec images seront reçus en texte uniquement (le contenu de l'image n'est pas accessible au bot).
Par défaut, OpenClaw télécharge uniquement les médias à partir des noms d'hôte Microsoft/Teams. Remplacez avec `channels.msteams.mediaAllowHosts` (utilisez `["*"]` pour autoriser n'importe quel hôte).
Les en-têtes d'autorisation ne sont attachés que pour les hôtes dans `channels.msteams.mediaAuthAllowHosts` (par défaut les hôtes Graph + Bot Framework). Gardez cette liste stricte (évitez les suffixes multi-locataires).

## Envoi de fichiers dans les chats de groupe

Les bots peuvent envoyer des fichiers en messages directs en utilisant le flux FileConsentCard (intégré). Cependant, **l'envoi de fichiers dans les chats de groupe/canaux** nécessite une configuration supplémentaire :

| Contexte                 | Comment les fichiers sont envoyés              | Configuration nécessaire                        |
| ------------------------ | ---------------------------------------------- | ----------------------------------------------- |
| **Messages directs**     | FileConsentCard → l'utilisateur accepte → le bot télécharge | Fonctionne directement                          |
| **Chats de groupe/canaux** | Télécharger vers SharePoint → partager le lien | Nécessite `sharePointSiteId` + permissions Graph |
| **Images (tout contexte)** | Encodées en base64 en ligne                    | Fonctionne directement                          |

### Pourquoi les chats de groupe ont besoin de SharePoint

Les bots n'ont pas de lecteur OneDrive personnel (le point de terminaison de l'API Graph `/me/drive` ne fonctionne pas pour les identités d'application). Pour envoyer des fichiers dans les chats de groupe/canaux, le bot télécharge vers un **site SharePoint** et crée un lien de partage.

### Configuration

1. **Ajouter les permissions de l'API Graph** dans Entra ID (Azure AD) → Inscription d'application :
   - `Sites.ReadWrite.All` (Application) - télécharger des fichiers vers SharePoint
   - `Chat.Read.All` (Application) - optionnel, active les liens de partage par utilisateur

2. **Accorder le consentement administrateur** pour le locataire.

3. **Obtenir votre ID de site SharePoint :**

   ```bash
   # Via Graph Explorer ou curl avec un jeton valide :
   curl -H "Authorization: Bearer $TOKEN" \
     "https://graph.microsoft.com/v1.0/sites/{hostname}:/{site-path}"

   # Exemple : pour un site à "contoso.sharepoint.com/sites/BotFiles"
   curl -H "Authorization: Bearer $TOKEN" \
     "https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/BotFiles"

   # La réponse inclut : "id": "contoso.sharepoint.com,guid1,guid2"
   ```

4. **Configurer OpenClaw :**

   ```json5
   {
     channels: {
       msteams: {
         // ... autre configuration ...
         sharePointSiteId: "contoso.sharepoint.com,guid1,guid2",
       },
     },
   }
   ```

### Comportement de partage

| Permission                              | Comportement de partage                                    |
| --------------------------------------- | ---------------------------------------------------------- |
| `Sites.ReadWrite.All` uniquement        | Lien de partage à l'échelle de l'organisation (tous les utilisateurs de l'org peuvent accéder) |
| `Sites.ReadWrite.All` + `Chat.Read.All` | Lien de partage par utilisateur (seuls les membres du chat peuvent accéder)      |

Le partage par utilisateur est plus sécurisé car seuls les participants du chat peuvent accéder au fichier. Si la permission `Chat.Read.All` est manquante, le bot revient au partage à l'échelle de l'organisation.

### Comportement de secours

| Scénario                                          | Résultat                                             |
| ------------------------------------------------- | ---------------------------------------------------- |
| Chat de groupe + fichier + `sharePointSiteId` configuré | Télécharger vers SharePoint, envoyer le lien de partage            |
| Chat de groupe + fichier + pas de `sharePointSiteId`    | Tentative de téléchargement OneDrive (peut échouer), envoyer le texte uniquement |
| Chat personnel + fichier                         | Flux FileConsentCard (fonctionne sans SharePoint)    |
| Tout contexte + image                            | Encodée en base64 en ligne (fonctionne sans SharePoint)   |

### Emplacement de stockage des fichiers

Les fichiers téléchargés sont stockés dans un dossier `/OpenClawShared/` dans la bibliothèque de documents par défaut du site SharePoint configuré.

## Sondages (Cartes adaptatives)

OpenClaw envoie les sondages Teams sous forme de cartes adaptatives (il n'y a pas d'API de sondage Teams native).

- CLI : `openclaw message poll --channel msteams --target conversation:<id> ...`
- Les votes sont enregistrés par la passerelle dans `~/.openclaw/msteams-polls.json`.
- La passerelle doit rester en ligne pour enregistrer les votes.
- Les sondages ne publient pas encore automatiquement les résumés de résultats (inspectez le fichier de stockage si nécessaire).

## Cartes adaptatives (arbitraires)

Envoyez n'importe quel JSON de carte adaptative aux utilisateurs ou conversations Teams en utilisant l'outil `message` ou la CLI.

Le paramètre `card` accepte un objet JSON de carte adaptative. Quand `card` est fourni, le texte du message est optionnel.

**Outil d'agent :**

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "user:<id>",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello!" }]
  }
}
```

**CLI :**

```bash
openclaw message send --channel msteams \
  --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello!"}]}'
```

Consultez la [documentation des cartes adaptatives](https://adaptivecards.io/) pour le schéma de carte et les exemples. Pour les détails du format cible, voir [Formats cibles](#formats-cibles) ci-dessous.

## Formats cibles

Les cibles MSTeams utilisent des préfixes pour distinguer les utilisateurs des conversations :

| Type de cible       | Format                           | Exemple                                             |
| ------------------- | -------------------------------- | --------------------------------------------------- |
| Utilisateur (par ID) | `user:<aad-object-id>`           | `user:40a1a0ed-4ff2-4164-a219-55518990c197`         |
| Utilisateur (par nom) | `user:<display-name>`            | `user:John Smith` (nécessite l'API Graph)           |
| Groupe/canal        | `conversation:<conversation-id>` | `conversation:19:abc123...@thread.tacv2`            |
| Groupe/canal (brut) | `<conversation-id>`              | `19:abc123...@thread.tacv2` (s'il contient `@thread`) |

**Exemples CLI :**

```bash
# Envoyer à un utilisateur par ID
openclaw message send --channel msteams --target "user:40a1a0ed-..." --message "Hello"

# Envoyer à un utilisateur par nom d'affichage (déclenche une recherche API Graph)
openclaw message send --channel msteams --target "user:John Smith" --message "Hello"

# Envoyer à un chat de groupe ou un canal
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" --message "Hello"

# Envoyer une carte adaptative à une conversation
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello"}]}'
```

**Exemples d'outil d'agent :**

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "user:John Smith",
  "message": "Hello!"
}
```

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "conversation:19:abc...@thread.tacv2",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello" }]
  }
}
```

Remarque : Sans le préfixe `user:`, les noms sont résolus par défaut en groupe/équipe. Utilisez toujours `user:` lors du ciblage de personnes par nom d'affichage.

## Messagerie proactive

- Les messages proactifs ne sont possibles **qu'après** qu'un utilisateur ait interagi, car nous stockons les références de conversation à ce moment.
- Voir `/gateway/configuration` pour `dmPolicy` et la mise en liste blanche.

## ID d'équipe et de canal (Piège courant)

Le paramètre de requête `groupId` dans les URL Teams **N'EST PAS** l'ID d'équipe utilisé pour la configuration. Extrayez les ID du chemin d'accès URL à la place :

**URL d'équipe :**

```
https://teams.microsoft.com/l/team/19%3ABk4j...%40thread.tacv2/conversations?groupId=...
                                    └────────────────────────────┘
                                    ID d'équipe (décodez ceci)
```

**URL de canal :**

```
https://teams.microsoft.com/l/channel/19%3A15bc...%40thread.tacv2/ChannelName?groupId=...
                                      └─────────────────────────┘
                                      ID de canal (décodez ceci)
```

**Pour la configuration :**

- ID d'équipe = segment de chemin après `/team/` (décodé en URL, par ex. `19:Bk4j...@thread.tacv2`)
- ID de canal = segment de chemin après `/channel/` (décodé en URL)
- **Ignorez** le paramètre de requête `groupId`

## Canaux privés

Les bots ont un support limité dans les canaux privés :

| Fonctionnalité                   | Canaux standard | Canaux privés          |
| -------------------------------- | --------------- | ---------------------- |
| Installation du bot              | Oui             | Limité                 |
| Messages en temps réel (webhook) | Oui             | Peut ne pas fonctionner |
| Permissions RSC                  | Oui             | Peut se comporter différemment |
| @mentions                        | Oui             | Si le bot est accessible |
| Historique de l'API Graph        | Oui             | Oui (avec permissions) |

**Solutions de contournement si les canaux privés ne fonctionnent pas :**

1. Utilisez les canaux standard pour les interactions du bot
2. Utilisez les messages directs - les utilisateurs peuvent toujours envoyer un message au bot directement
3. Utilisez l'API Graph pour l'accès historique (nécessite `ChannelMessage.Read.All`)

## Dépannage

### Problèmes courants

- **Les images ne s'affichent pas dans les canaux :** Permissions Graph ou consentement administrateur manquants. Réinstallez l'application Teams et quittez/rouvrez complètement Teams.
- **Pas de réponses dans le canal :** les mentions sont requises par défaut ; définissez `channels.msteams.requireMention=false` ou configurez par équipe/canal.
- **Incompatibilité de version (Teams affiche toujours l'ancien manifeste) :** supprimez et réajoutez l'application et quittez complètement Teams pour actualiser.
- **401 Non autorisé du webhook :** Attendu lors des tests manuels sans JWT Azure - signifie que le point de terminaison est accessible mais l'authentification a échoué. Utilisez Azure Web Chat pour tester correctement.

### Erreurs de téléchargement de manifeste

- **"Le fichier d'icône ne peut pas être vide" :** Le manifeste référence des fichiers d'icône qui font 0 octet. Créez des icônes PNG valides (32x32 pour `outline.png`, 192x192 pour `color.png`).
- **"webApplicationInfo.Id déjà utilisé" :** L'application est toujours installée dans une autre équipe/chat. Trouvez et désinstallez-la d'abord, ou attendez 5-10 minutes pour la propagation.
- **"Une erreur s'est produite" lors du téléchargement :** Téléchargez via [https://admin.teams.microsoft.com](https://admin.teams.microsoft.com) à la place, ouvrez les outils de développement du navigateur (F12) → onglet Réseau, et vérifiez le corps de la réponse pour l'erreur réelle.
- **Le chargement de version échoue :** Essayez "Télécharger une application dans le catalogue d'applications de votre organisation" au lieu de "Télécharger une application personnalisée" - cela contourne souvent les restrictions de chargement de version.

### Les permissions RSC ne fonctionnent pas

1. Vérifiez que `webApplicationInfo.id` correspond exactement à l'ID d'application de votre bot
2. Retéléchargez l'application et réinstallez-la dans l'équipe/chat
3. Vérifiez si votre administrateur d'organisation a bloqué les permissions RSC
4. Confirmez que vous utilisez la bonne portée : `ChannelMessage.Read.Group` pour les équipes, `ChatMessage.Read.Chat` pour les chats de groupe

## Références

- [Créer un bot Azure](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-registration) - Guide de configuration du bot Azure
- [Portail des développeurs Teams](https://dev.teams.microsoft.com/apps) - créer/gérer les applications Teams
- [Schéma du manifeste de l'application Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/resources/schema/manifest-schema)
- [Recevoir les messages de canal avec RSC](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/channel-messages-with-rsc)
- [Référence des permissions RSC](https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/rsc/resource-specific-consent)
- [Gestion des fichiers du bot Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/bots-filesv4) (le canal/groupe nécessite Graph)
- [Messagerie proactive](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/send-proactive-messages)
