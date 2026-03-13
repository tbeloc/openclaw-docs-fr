---
read_when:
  - 为 OpenClaw 设置 Twitch 聊天集成
summary: Twitch 聊天机器人配置和设置
title: Twitch
x-i18n:
  generated_at: "2026-02-03T07:44:41Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 0dd1c05bef570470d8b82c1f6dee5337e8b76b57269c5cad6aee2e711483f8ba
  source_path: channels/twitch.md
  workflow: 15
---

# Twitch (Plugin)

Support pour le chat Twitch via connexion IRC. OpenClaw se connecte en tant qu'utilisateur Twitch (compte bot), recevant et envoyant des messages dans les canaux.

## Plugin requis

Twitch est distribué en tant que plugin et n'est pas inclus dans l'installation principale.

Installation via CLI (registre npm) :

```bash
openclaw plugins install @openclaw/twitch
```

Checkout local (lors de l'exécution depuis un dépôt git) :

```bash
openclaw plugins install ./extensions/twitch
```

Détails : [Plugins](/tools/plugin)

## Configuration rapide (débutants)

1. Créez un compte Twitch dédié pour le bot (ou utilisez un compte existant).
2. Générez les identifiants : [Twitch Token Generator](https://twitchtokengenerator.com/)
   - Sélectionnez **Bot Token**
   - Confirmez que les portées de permission `chat:read` et `chat:write` sont sélectionnées
   - Copiez l'**ID Client** et le **Jeton d'accès**
3. Trouvez votre ID utilisateur Twitch : https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
4. Configurez les jetons :
   - Variable d'environnement : `OPENCLAW_TWITCH_ACCESS_TOKEN=...` (compte par défaut uniquement)
   - Ou configuration : `channels.twitch.accessToken`
   - Si les deux sont définis, la configuration a priorité (la variable d'environnement est utilisée en secours pour le compte par défaut uniquement).
5. Démarrez la passerelle Gateway.

**⚠️ Important :** Ajoutez un contrôle d'accès (`allowFrom` ou `allowedRoles`) pour empêcher les utilisateurs non autorisés de déclencher le bot. `requireMention` est `true` par défaut.

Configuration minimale :

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw", // Compte Twitch du bot
      accessToken: "oauth:abc123...", // Jeton d'accès OAuth (ou utilisez la variable d'environnement OPENCLAW_TWITCH_ACCESS_TOKEN)
      clientId: "xyz789...", // ID Client du Token Generator
      channel: "vevisk", // Chat du canal Twitch à rejoindre (obligatoire)
      allowFrom: ["123456789"], // (Recommandé) Votre ID utilisateur Twitch uniquement - obtenu depuis https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
    },
  },
}
```

## Qu'est-ce que c'est

- Un canal Twitch détenu par la passerelle Gateway.
- Routage déterministe : les réponses reviennent toujours à Twitch.
- Chaque compte est mappé à une clé de session isolée `agent:<agentId>:twitch:<accountName>`.
- `username` est le compte bot (le compte qui s'authentifie), `channel` est le salon de chat à rejoindre.

## Configuration (détaillée)

### Générer les identifiants

Utilisez [Twitch Token Generator](https://twitchtokengenerator.com/) :

- Sélectionnez **Bot Token**
- Confirmez que les portées de permission `chat:read` et `chat:write` sont sélectionnées
- Copiez l'**ID Client** et le **Jeton d'accès**

Aucune inscription d'application manuelle requise. Les jetons expirent après quelques heures.

### Configurer le bot

**Variables d'environnement (compte par défaut uniquement) :**

```bash
OPENCLAW_TWITCH_ACCESS_TOKEN=oauth:abc123...
```

**Ou configuration :**

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
    },
  },
}
```

Si la variable d'environnement et la configuration sont toutes deux définies, la configuration a priorité.

### Contrôle d'accès (recommandé)

```json5
{
  channels: {
    twitch: {
      allowFrom: ["123456789"], // (Recommandé) Votre ID utilisateur Twitch uniquement
    },
  },
}
```

Préférez `allowFrom` comme liste d'autorisation stricte. Si vous souhaitez un contrôle d'accès basé sur les rôles, utilisez plutôt `allowedRoles`.

**Rôles disponibles :** `"moderator"`, `"owner"`, `"vip"`, `"subscriber"`, `"all"`.

**Pourquoi les ID utilisateur ?** Les noms d'utilisateur peuvent être modifiés, ce qui permet l'usurpation d'identité. Les ID utilisateur sont permanents.

Trouvez votre ID utilisateur Twitch : https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/ (convertissez votre nom d'utilisateur Twitch en ID)

## Actualisation des jetons (optionnel)

Les jetons de [Twitch Token Generator](https://twitchtokengenerator.com/) ne peuvent pas être actualisés automatiquement - ils doivent être régénérés à l'expiration.

Pour implémenter l'actualisation automatique des jetons, créez votre propre application Twitch dans la [Console Twitch Developer](https://dev.twitch.tv/console) et ajoutez-la à la configuration :

```json5
{
  channels: {
    twitch: {
      clientSecret: "your_client_secret",
      refreshToken: "your_refresh_token",
    },
  },
}
```

Le bot actualisera automatiquement le jeton avant son expiration et enregistrera les événements d'actualisation.

## Support multi-comptes

Utilisez la configuration `channels.twitch.accounts` pour configurer les jetons par compte. Consultez [`gateway/configuration`](/gateway/configuration) pour le mode partagé.

Exemple (un compte bot dans deux canaux) :

```json5
{
  channels: {
    twitch: {
      accounts: {
        channel1: {
          username: "openclaw",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "vevisk",
        },
        channel2: {
          username: "openclaw",
          accessToken: "oauth:def456...",
          clientId: "uvw012...",
          channel: "secondchannel",
        },
      },
    },
  },
}
```

**Remarque :** Chaque compte a besoin de son propre jeton (un jeton par canal).

## Contrôle d'accès

### Restrictions basées sur les rôles

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowedRoles: ["moderator", "vip"],
        },
      },
    },
  },
}
```

### Liste d'autorisation par ID utilisateur (plus sûr)

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowFrom: ["123456789", "987654321"],
        },
      },
    },
  },
}
```

### Accès basé sur les rôles (alternative)

`allowFrom` est une liste d'autorisation stricte. Une fois défini, seuls ces ID utilisateur sont autorisés.
Si vous souhaitez un accès basé sur les rôles, ne définissez pas `allowFrom`, configurez plutôt `allowedRoles` :

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowedRoles: ["moderator"],
        },
      },
    },
  },
}
```

### Désactiver l'exigence de @mention

Par défaut, `requireMention` est `true`. Pour désactiver et répondre à tous les messages :

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          requireMention: false,
        },
      },
    },
  },
}
```

## Dépannage

Commencez par exécuter les commandes de diagnostic :

```bash
openclaw doctor
openclaw channels status --probe
```

### Le bot ne répond pas aux messages

**Vérifiez le contrôle d'accès :** Assurez-vous que votre ID utilisateur est dans `allowFrom`, ou supprimez temporairement `allowFrom` et définissez `allowedRoles: ["all"]` pour tester.

**Vérifiez que le bot est dans le canal :** Le bot doit rejoindre le canal spécifié dans `channel`.

### Problèmes de jeton

**"Failed to connect" ou erreurs d'authentification :**

- Vérifiez que `accessToken` est une valeur de jeton d'accès OAuth (généralement préfixée par `oauth:`)
- Vérifiez que le jeton a les portées de permission `chat:read` et `chat:write`
- Si vous utilisez l'actualisation des jetons, vérifiez que `clientSecret` et `refreshToken` sont définis

### L'actualisation des jetons ne fonctionne pas

**Vérifiez les événements d'actualisation dans les journaux :**

```
Using env token source for mybot
Access token refreshed for user 123456 (expires in 14400s)
```

Si vous voyez "token refresh disabled (no refresh token)" :

- Assurez-vous que `clientSecret` est fourni
- Assurez-vous que `refreshToken` est fourni

## Configuration

**Configuration du compte :**

- `username` - Nom d'utilisateur du bot
- `accessToken` - Jeton d'accès OAuth avec permissions `chat:read` et `chat:write`
- `clientId` - ID Client Twitch (du Token Generator ou de votre application)
- `channel` - Canal à rejoindre (obligatoire)
- `enabled` - Activer ce compte (par défaut : `true`)
- `clientSecret` - Optionnel : pour l'actualisation automatique des jetons
- `refreshToken` - Optionnel : pour l'actualisation automatique des jetons
- `expiresIn` - Expiration du jeton (secondes)
- `obtainmentTimestamp` - Horodatage d'obtention du jeton
- `allowFrom` - Liste d'autorisation des ID utilisateur
- `allowedRoles` - Contrôle d'accès basé sur les rôles (`"moderator" | "owner" | "vip" | "subscriber" | "all"`)
- `requireMention` - Exiger une @mention (par défaut : `true`)

**Options du fournisseur :**

- `channels.twitch.enabled` - Activer/désactiver le démarrage du canal
- `channels.twitch.username` - Nom d'utilisateur du bot (configuration simplifiée à compte unique)
- `channels.twitch.accessToken` - Jeton d'accès OAuth (configuration simplifiée à compte unique)
- `channels.twitch.clientId` - ID Client Twitch (configuration simplifiée à compte unique)
- `channels.twitch.channel` - Canal à rejoindre (configuration simplifiée à compte unique)
- `channels.twitch.accounts.<accountName>` - Configuration multi-comptes (tous les champs de compte ci-dessus)

Exemple complet :

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
      clientSecret: "secret123...",
      refreshToken: "refresh456...",
      allowFrom: ["123456789"],
      allowedRoles: ["moderator", "vip"],
      accounts: {
        default: {
          username: "mybot",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "your_channel",
          enabled: true,
          clientSecret: "secret123...",
          refreshToken: "refresh456...",
          expiresIn: 14400,
          obtainmentTimestamp: 1706092800000,
          allowFrom: ["123456789", "987654321"],
          allowedRoles: ["moderator"],
        },
      },
    },
  },
}
```

## Actions des outils

Les agents peuvent appeler `twitch` pour effectuer les actions suivantes :

- `send` - Envoyer un message au canal

Exemple :

```json5
{
  action: "twitch",
  params: {
    message: "Hello Twitch!",
    to: "#mychannel",
  },
}
```

## Sécurité et exploitation

- **Traitez les jetons comme des mots de passe** - Ne commitez jamais les jetons dans git
- **Utilisez l'actualisation automatique des jetons** pour les bots de longue durée
- **Utilisez les listes d'autorisation des ID utilisateur** plutôt que les noms d'utilisateur pour le contrôle d'accès
- **Surveillez les journaux** pour les événements d'actualisation des jetons et l'état de la connexion
- **Minimisez les portées de permission des jetons** - Demandez uniquement `chat:read` et `chat:write`
- **Si vous êtes bloqué** : Redémarrez la passerelle Gateway après avoir confirmé qu'aucun autre processus ne possède la session

## Limitations

- **500 caractères par message** (fragmenté automatiquement aux limites de mots)
- Markdown supprimé avant la fragmentation
- Pas de limite de débit (utilise la limite de débit intégrée de Twitch)
