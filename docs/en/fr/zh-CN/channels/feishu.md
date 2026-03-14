```markdown
---
summary: "Support de robot Feishu, fonctionnalités et configuration"
read_when:
  - Vous souhaitez connecter un robot Feishu
  - Vous configurez le canal Feishu
title: Feishu
---

# Robot Feishu

Statut : Prêt pour la production, supporte les chats privés et les groupes de robots. Utilise le mode de connexion longue WebSocket pour recevoir les messages.

---

## Plugin intégré

La version actuelle d'OpenClaw inclut le plugin Feishu, donc une installation séparée n'est généralement pas nécessaire.

Si vous utilisez une version plus ancienne ou une installation personnalisée sans Feishu, vous pouvez l'installer manuellement :

```bash
openclaw plugins install @openclaw/feishu
```

---

## Démarrage rapide

Il y a deux façons d'ajouter un canal Feishu :

### Méthode 1 : Ajouter via l'assistant d'installation (recommandé)

Si vous venez d'installer OpenClaw, vous pouvez exécuter directement l'assistant et ajouter Feishu selon les instructions :

```bash
openclaw onboard
```

L'assistant vous guidera à travers :

1. Créer une application Feishu et obtenir les identifiants
2. Configurer les identifiants de l'application
3. Démarrer la passerelle

✅ **Après avoir terminé la configuration**, vous pouvez utiliser les commandes suivantes pour vérifier l'état de la passerelle :

- `openclaw gateway status` - Afficher l'état d'exécution de la passerelle
- `openclaw logs --follow` - Afficher les journaux en temps réel

### Méthode 2 : Ajouter via la ligne de commande

Si vous avez déjà terminé l'installation initiale, vous pouvez ajouter le canal Feishu avec la commande suivante :

```bash
openclaw channels add
```

Puis sélectionnez Feishu selon les invites interactives et entrez l'App ID et l'App Secret.

✅ **Après avoir terminé la configuration**, vous pouvez utiliser les commandes suivantes pour gérer la passerelle :

- `openclaw gateway status` - Afficher l'état d'exécution de la passerelle
- `openclaw gateway restart` - Redémarrer la passerelle pour appliquer la nouvelle configuration
- `openclaw logs --follow` - Afficher les journaux en temps réel

---

## Étape 1 : Créer une application Feishu

### 1. Ouvrir la plateforme ouverte Feishu

Visitez [Plateforme ouverte Feishu](https://open.feishu.cn/app) et connectez-vous avec votre compte Feishu.

Pour Lark (version internationale), utilisez https://open.larksuite.com/app et définissez `domain: "lark"` dans la configuration.

### 2. Créer une application

1. Cliquez sur **Créer une application d'entreprise personnalisée**
2. Remplissez le nom et la description de l'application
3. Sélectionnez l'icône de l'application

![Créer une application d'entreprise personnalisée](/images/feishu-step2-create-app.png)

### 3. Obtenir les identifiants de l'application

Sur la page **Identifiants et informations de base** de l'application, copiez :

- **App ID** (format comme `cli_xxx`)
- **App Secret**

❗ **Important** : Gardez l'App Secret en sécurité et ne le partagez pas avec d'autres.

![Obtenir les identifiants de l'application](/images/feishu-step3-credentials.png)

### 4. Configurer les permissions de l'application

Sur la page **Gestion des permissions**, cliquez sur le bouton **Importer en masse**, collez la configuration JSON suivante pour importer les permissions requises en un clic :

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "cardkit:card:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "docs:document.content:read",
      "event:ip_list",
      "im:chat",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.group_msg",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource",
      "sheets:spreadsheet",
      "wiki:wiki:readonly"
    ],
    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
  }
}
```

![Configurer les permissions de l'application](/images/feishu-step4-permissions.png)

### 5. Activer la capacité de robot

Sur la page **Capacités de l'application** > **Robot** :

1. Activez la capacité de robot
2. Configurez le nom du robot

![Activer la capacité de robot](/images/feishu-step5-bot-capability.png)

### 6. Configurer l'abonnement aux événements

⚠️ **Rappel important** : Avant de configurer l'abonnement aux événements, assurez-vous d'avoir complété les étapes suivantes :

1. Exécuté `openclaw channels add` pour ajouter le canal Feishu
2. La passerelle est en état de démarrage (vous pouvez vérifier l'état via `openclaw gateway status`)

Sur la page **Abonnement aux événements** :

1. Sélectionnez **Utiliser la connexion longue pour recevoir les événements** (mode WebSocket)
2. Ajoutez l'événement : `im.message.receive_v1` (recevoir les messages)

⚠️ **Remarque** : Si la passerelle n'est pas démarrée ou le canal n'est pas ajouté, la configuration de la connexion longue échouera.

![Configurer l'abonnement aux événements](/images/feishu-step6-event-subscription.png)

### 7. Publier l'application

1. Créez une version sur la page **Gestion des versions et publication**
2. Soumettez pour examen et publiez
3. Attendez l'approbation de l'administrateur (les applications d'entreprise personnalisées sont généralement approuvées automatiquement)

---

## Étape 2 : Configurer OpenClaw

### Configurer via l'assistant (recommandé)

Exécutez la commande suivante et collez l'App ID et l'App Secret selon les invites :

```bash
openclaw channels add
```

Sélectionnez **Feishu**, puis entrez les identifiants que vous avez obtenus à l'étape 1.

### Configurer via le fichier de configuration

Modifiez `~/.openclaw/openclaw.json` :

```json5
{
  channels: {
    feishu: {
      enabled: true,
      dmPolicy: "pairing",
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
          botName: "Mon assistant IA",
        },
      },
    },
  },
}
```

Si vous utilisez `connectionMode: "webhook"`, vous devez définir `verificationToken`. Le service Webhook Feishu est lié par défaut à `127.0.0.1` ; définissez `webhookHost` uniquement si vous avez besoin d'une adresse d'écoute différente.

#### Obtenir le Verification Token (mode Webhook uniquement)

Lors de l'utilisation du mode Webhook, vous devez définir `channels.feishu.verificationToken` dans la configuration. Pour l'obtenir :

1. Ouvrez votre application sur la plateforme ouverte Feishu
2. Allez à **Configuration de développement** → **Événements et rappels**
3. Ouvrez l'onglet **Politique de chiffrement**
4. Copiez le **Verification Token** (jeton de vérification)

![Emplacement du Verification Token](/images/feishu-verification-token.png)

### Configurer via les variables d'environnement

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

### Domaine Lark (version internationale)

Si votre locataire est sur Lark (version internationale), définissez le domaine sur `lark` (ou le domaine complet), vous pouvez configurer `channels.feishu.domain` ou `channels.feishu.accounts.<id>.domain` :

```json5
{
  channels: {
    feishu: {
      domain: "lark",
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
        },
      },
    },
  },
}
```

### Optimisation des quotas

Vous pouvez réduire les appels API Feishu avec les configurations optionnelles suivantes :

- `typingIndicator` (par défaut `true`) : définissez sur `false` pour ne pas envoyer le statut "en train de taper".
- `resolveSenderNames` (par défaut `true`) : définissez sur `false` pour ne pas récupérer le profil de l'expéditeur.

Peut être configuré au niveau du canal ou du compte :

```json5
{
  channels: {
    feishu: {
      typingIndicator: false,
      resolveSenderNames: false,
      accounts: {
        main: {
          appId: "cli_xxx",
          appSecret: "xxx",
          typingIndicator: true,
          resolveSenderNames: false,
        },
      },
    },
  },
}
```

---

## Étape 3 : Démarrer et tester

### 1. Démarrer la passerelle

```bash
openclaw gateway
```

### 2. Envoyer un message de test

Trouvez le robot que vous avez créé dans Feishu et envoyez un message.

### 3. Appairage et autorisation

Par défaut, le robot répondra avec un **code d'appairage**. Vous devez approuver ce code :

```bash
openclaw pairing approve feishu <code-appairage>
```

Après approbation, vous pouvez converser normalement.

---

## Introduction

- **Canal robot Feishu** : Robot Feishu géré par la passerelle
- **Routage déterministe** : Les réponses reviennent toujours à Feishu, le modèle ne choisit pas le canal
- **Isolation des sessions** : Les chats privés partagent la session principale ; les groupes sont isolés indépendamment
- **Connexion WebSocket** : Utilise le mode de connexion longue du SDK Feishu, pas besoin d'URL publique

---

## Contrôle d'accès

### Accès aux chats privés

- **Par défaut** : `dmPolicy: "pairing"`, les utilisateurs inconnus reçoivent un code d'appairage
- **Approuver l'appairage** :
  ```bash
  openclaw pairing list feishu      # Afficher la liste en attente d'approbation
  openclaw pairing approve feishu <CODE>  # Approuver
  ```
- **Mode liste blanche** : Configurez les Open ID des utilisateurs autorisés via `channels.feishu.allowFrom`

### Accès aux groupes

**1. Politique de groupe** (`channels.feishu.groupPolicy`) :

- `"open"` = Autoriser tous les utilisateurs du groupe (par défaut)
- `"allowlist"` = Autoriser uniquement les groupes dans `groupAllowFrom`
- `"disabled"` = Désactiver les messages de groupe

**2. Exigence de mention** (`channels.feishu.groups.<chat_id>.requireMention`) :

- `true` = Nécessite de @mentionner le robot pour répondre (par défaut)
- `false` = Répond sans @mention

---

## Exemple de configuration de groupe

### Autoriser tous les groupes, mention requise (comportement par défaut)

```json5
{
  channels: {
    feishu: {
      groupPolicy: "open",
      // Par défaut requireMention: true
    },
  },
}
```

### Autoriser tous les groupes, mention non requise

Vous devez configurer pour des groupes spécifiques :

```json5
{
  channels: {
    feishu: {
      groups: {
        oc_xxx: { requireMention: false },
      },
    },
  },
}
```

### Autoriser uniquement des groupes spécifiques

```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      // Format d'ID de groupe : oc_xxx
      groupAllowFrom: ["oc_xxx", "oc_yyy"],
    },
  },
}
```

### Autoriser uniquement des membres spécifiques à envoyer des messages dans le groupe (liste blanche des expéditeurs)

En plus de la liste blanche des groupes, **tous les messages** de ce groupe sont vérifiés par l'open_id de l'expéditeur : seuls les messages des utilisateurs listés dans `groups.<chat_id>.allowFrom` seront traités, les messages des autres membres seront ignorés (c'est une liste blanche au niveau de l'expéditeur, pas seulement pour les commandes de contrôle comme /reset, /new).

```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["oc_xxx"],
      groups: {
        oc_xxx: {
          // Format d'ID utilisateur : ou_xxx
          allowFrom: ["ou_user1", "ou_user2"],
        },
      },
    },
  },
}
```

---

## Obtenir les ID de groupe/utilisateur

### Obtenir l'ID de groupe (chat_id)

Le format d'ID de groupe est `oc_xxx`, vous pouvez l'obtenir de la manière suivante :

**Méthode 1** (recommandée) :

1. Démarrez la passerelle et @mentionnez le robot dans le groupe
2. Exécutez `openclaw logs --follow` pour voir le `chat_id` dans les journaux

**Méthode 2** :
Utilisez l'outil de débogage API Feishu pour obtenir la liste des groupes du robot.

### Obtenir l'ID utilisateur (open_id)

Le format d'ID utilisateur est `ou_xxx`, vous pouvez l'obtenir de la manière suivante :

**Méthode 1** (recommandée) :

1. Démar
