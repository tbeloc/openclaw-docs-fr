# Microsoft Teams (plugin)

> « Abandonnez tout espoir, vous qui entrez ici. »

Mis à jour : 2026-01-21

Statut : texte + pièces jointes DM sont supportés ; l'envoi de fichiers dans les canaux/groupes nécessite `sharePointSiteId` + permissions Graph (voir [Envoi de fichiers dans les chats de groupe](#envoi-de-fichiers-dans-les-chats-de-groupe)). Les sondages sont envoyés via des cartes adaptatives.

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

Détails : [Plugins](/tools/plugin)

## Configuration rapide (débutant)

1. Installez le plugin Microsoft Teams.
2. Créez un **bot Azure** (ID d'application + secret client + ID de locataire).
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

- Communiquer avec OpenClaw via Teams DMs, chats de groupe ou canaux.
- Maintenir un routage déterministe : les réponses reviennent toujours au canal d'où elles proviennent.
- Adopter un comportement de canal sûr par défaut (mentions requises sauf configuration contraire).

## Écritures de configuration

Par défaut, Microsoft Teams est autorisé à écrire les mises à jour de configuration déclenchées par `/config set|unset` (nécessite `commands.config: true`).

Désactivez avec :

```json5
{
  channels: { msteams: { configWrites: false } },
}
```

## Contrôle d'accès (DMs + groupes)

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

**Liste d'autorisation Teams + canal**

- Limitez les réponses de groupe/canal en listant les équipes et canaux sous `channels.msteams.teams`.
- Les clés doivent utiliser des ID d'équipe stables et des ID de conversation de canal.
- Quand `groupPolicy="allowlist"` et qu'une liste d'autorisation d'équipes est présente, seules les équipes/canaux listés sont acceptés (mention obligatoire).
- L'assistant de configuration accepte les entrées `Team/Channel` et les stocke pour vous.
- Au démarrage, OpenClaw résout les noms de liste d'autorisation d'équipe/canal et d'utilisateur en ID (quand les permissions Graph le permettent)
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
2. Créez un **bot Azure** (ID d'application + secret + ID de locataire).
3. Créez un **package d'application Teams** qui référence le bot et inclut les permissions RSC ci-dessous.
4. Téléchargez/installez l'application Teams dans une équipe (ou portée personnelle pour les DMs).
5. Configurez `msteams` dans `~/.openclaw/openclaw.json` (ou variables d'environnement) et démarrez la passerelle.
6. La passerelle écoute le trafic webhook Bot Framework sur `/api/messages` par défaut.

## Configuration du bot Azure (Prérequis)

Avant de configurer OpenClaw, vous devez créer une ressource bot Azure.

### Étape 1 : Créer un bot Azure

1. Allez à [Créer un bot Azure](https://portal.azure.com/#create/Microsoft.AzureBot)
2. Remplissez l'onglet **Bases** :

   | Champ              | Valeur                                                    |
   | ------------------ | -------------------------------------------------------- |
   | **Identifiant du bot**     | Nom de votre bot, par ex. `openclaw-msteams` (doit être unique) |
   | **Abonnement**   | Sélectionnez votre abonnement Azure                           |
   | **Groupe de ressources** | Créer nouveau ou utiliser existant                               |
   | **Niveau tarifaire**   | **Gratuit** pour le développement/test                                 |
   | **Type d'application**    | **Locataire unique** (recommandé - voir remarque ci-dessous)         |
   | **Type de création**  | **Créer un nouvel ID d'application Microsoft**                          |

> **Avis de dépréciation :** La création de nouveaux bots multi-locataires a été dépréciée après 2025-07-31. Utilisez **Locataire unique** pour les nouveaux bots.

3. Cliquez sur **Vérifier + créer** → **Créer** (attendez ~1-2 minutes)

### Étape 2 : Obtenir les identifiants

1. Allez à votre ressource bot Azure → **Configuration**
2. Copiez **ID d'application Microsoft** → c'est votre `appId`
3. Cliquez sur **Gérer le mot de passe** → allez à l'enregistrement d'application
4. Sous **Certificats et secrets** → **Nouveau secret client** → copiez la **Valeur** → c'est votre `appPassword`
5. Allez à **Aperçu** → copiez **ID de répertoire (locataire)** → c'est votre `tenantId`

### Étape 3 : Configurer le point de terminaison de messagerie

1. Dans bot Azure → **Configuration**
2. Définissez **Point de terminaison de messagerie** sur votre URL webhook :
   - Production : `https://your-domain.com/api/messages`
   - Développement local : Utilisez un tunnel (voir [Développement local](#développement-local-tunneling) ci-dessous)

### Étape 4 : Activer le canal Teams

1. Dans bot Azure → **Canaux**
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
4. Sélectionnez **Entrer un ID de bot manuellement** et collez votre ID d'application bot Azure
5. Vérifiez les portées : **Personnel**, **Équipe**, **Chat de groupe**
6. Cliquez sur **Distribuer** → **Télécharger le package d'application**
7. Dans Teams : **Applications** → **Gérer vos applications** → **Télécharger une application personnalisée** → sélectionnez le ZIP

C'est souvent plus facile que de modifier manuellement les manifestes JSON.

## Test du bot

**Option A : Web Chat Azure (vérifier d'abord le webhook)**

1. Dans le portail Azure → votre ressource bot Azure → **Tester dans Web Chat**
2. Envoyez un message - vous devriez voir une réponse
3. Cela confirme que votre point de terminaison webhook fonctionne avant la configuration Teams

**Option B : Teams (après installation de l'application)**

1. Installez l'application Teams (sideload ou catalogue organisationnel)
2. Trouvez le bot dans Teams et envoyez un DM
3. Vérifiez les journaux de la passerelle pour l'activité entrante

## Configuration (texte minimal uniquement)

1. **Installez le plugin Microsoft Teams**
   - Depuis npm : `openclaw plugins install @openclaw/msteams`
   - Depuis un checkout local : `openclaw plugins install ./extensions/msteams`

2. **Enregistrement du bot**
   - Créez un bot Azure (voir ci-dessus) et notez :
     - ID d'application
     - Secret client (mot de passe d'application)
     - ID de locataire (locataire unique)

3. **Manifeste d'application Teams**
   - Incluez une entrée `bot` avec `botId = <App ID>`.
   - Portées : `personal`, `team`, `groupChat`.
   - `supportsFiles: true` (requis pour la gestion des fichiers dans la portée personnelle).
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
   - Définissez le point de terminaison de messagerie du bot Azure sur :
     - `https://<host>:3978/api/messages` (ou votre chemin/port choisi).

6. **Exécutez la passerelle**
   - Le canal Teams démarre automatiquement quand le plugin est installé et que la configuration `msteams` existe avec les identifiants.

## Contexte d'historique

- `channels.msteams.historyLimit` contrôle combien de messages récents de canal/groupe sont enveloppés dans l'invite.
- Revient à `messages.groupChat.historyLimit`. Définissez `0` pour désactiver (par défaut 50).
- L'historique DM peut être limité avec `channels.msteams.dmHistoryLimit` (tours utilisateur). Remplacements par utilisateur : `channels.msteams.dms["<user_id>"].historyLimit`.

## Permissions RSC Teams actuelles (Manifeste)

Ce sont les **permissions spécifiques aux ressources existantes** dans notre manifeste d'application Teams. Elles s'appliquent uniquement dans l'équipe/chat où l'application est installée.

**Pour les canaux (portée équipe) :**

- `ChannelMessage.Read.Group` (Application) - recevoir tous les messages de canal sans @mention
- `ChannelMessage.Send.Group` (Application)
- `Member.Read.Group` (Application)
- `Owner.Read.Group` (Application)
- `ChannelSettings.Read.Group` (Application)
- `TeamMember.Read.Group` (Application)
- `TeamSettings.Read.Group` (Application)

**Pour les chats de groupe :**

- `ChatMessage.Read.Chat` (Application) - recevoir tous les messages de chat de groupe sans @mention

## Exemple de manifeste Teams (édité)

Exemple minimal et valide avec les champs requis. Remplacez les ID
