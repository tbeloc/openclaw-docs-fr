---
summary: "Configuration et configuration du bot de chat Twitch"
read_when:
  - Setting up Twitch chat integration for OpenClaw
title: "Twitch"
---

# Twitch (plugin)

Support du chat Twitch via connexion IRC. OpenClaw se connecte en tant qu'utilisateur Twitch (compte bot) pour recevoir et envoyer des messages dans les canaux.

## Plugin requis

Twitch est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

Installez via CLI (registre npm) :

```bash
openclaw plugins install @openclaw/twitch
```

Checkout local (lors de l'exécution à partir d'un dépôt git) :

```bash
openclaw plugins install ./extensions/twitch
```

Détails : [Plugins](/tools/plugin)

## Configuration rapide (débutant)

1. Créez un compte Twitch dédié pour le bot (ou utilisez un compte existant).
2. Générez les identifiants : [Générateur de jetons Twitch](https://twitchtokengenerator.com/)
   - Sélectionnez **Bot Token**
   - Vérifiez que les portées `chat:read` et `chat:write` sont sélectionnées
   - Copiez l'**ID client** et le **jeton d'accès**
3. Trouvez votre ID utilisateur Twitch : [https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/](https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/)
4. Configurez le jeton :
   - Env : `OPENCLAW_TWITCH_ACCESS_TOKEN=...` (compte par défaut uniquement)
   - Ou config : `channels.twitch.accessToken`
   - Si les deux sont définis, la config a la priorité (le fallback env est le compte par défaut uniquement).
5. Démarrez la passerelle.

**⚠️ Important :** Ajoutez le contrôle d'accès (`allowFrom` ou `allowedRoles`) pour empêcher les utilisateurs non autorisés de déclencher le bot. `requireMention` est par défaut `true`.

Configuration minimale :

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw", // Compte Twitch du bot
      accessToken: "oauth:abc123...", // Jeton d'accès OAuth (ou utilisez la variable d'env OPENCLAW_TWITCH_ACCESS_TOKEN)
      clientId: "xyz789...", // ID client du générateur de jetons
      channel: "vevisk", // Canal de chat Twitch à rejoindre (requis)
      allowFrom: ["123456789"], // (recommandé) Votre ID utilisateur Twitch uniquement - obtenez-le sur https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
    },
  },
}
```

## Qu'est-ce que c'est

- Un canal Twitch appartenant à la passerelle.
- Routage déterministe : les réponses reviennent toujours à Twitch.
- Chaque compte correspond à une clé de session isolée `agent:<agentId>:twitch:<accountName>`.
- `username` est le compte du bot (qui s'authentifie), `channel` est le salon de chat à rejoindre.

## Configuration (détaillée)

### Générer les identifiants

Utilisez [Générateur de jetons Twitch](https://twitchtokengenerator.com/) :

- Sélectionnez **Bot Token**
- Vérifiez que les portées `chat:read` et `chat:write` sont sélectionnées
- Copiez l'**ID client** et le **jeton d'accès**

Aucune inscription d'application manuelle requise. Les jetons expirent après plusieurs heures.

### Configurer le bot

**Variable d'env (compte par défaut uniquement) :**

```bash
OPENCLAW_TWITCH_ACCESS_TOKEN=oauth:abc123...
```

**Ou config :**

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

Si l'env et la config sont tous deux définis, la config a la priorité.

### Contrôle d'accès (recommandé)

```json5
{
  channels: {
    twitch: {
      allowFrom: ["123456789"], // (recommandé) Votre ID utilisateur Twitch uniquement
    },
  },
}
```

Préférez `allowFrom` pour une liste blanche stricte. Utilisez `allowedRoles` à la place si vous souhaitez un accès basé sur les rôles.

**Rôles disponibles :** `"moderator"`, `"owner"`, `"vip"`, `"subscriber"`, `"all"`.

**Pourquoi les ID utilisateur ?** Les noms d'utilisateur peuvent changer, permettant l'usurpation d'identité. Les ID utilisateur sont permanents.

Trouvez votre ID utilisateur Twitch : [https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/](https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/) (Convertissez votre nom d'utilisateur Twitch en ID)

## Actualisation du jeton (optionnel)

Les jetons du [Générateur de jetons Twitch](https://twitchtokengenerator.com/) ne peuvent pas être actualisés automatiquement - régénérez-les à l'expiration.

Pour l'actualisation automatique des jetons, créez votre propre application Twitch sur [Console développeur Twitch](https://dev.twitch.tv/console) et ajoutez à la config :

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

Le bot actualise automatiquement les jetons avant l'expiration et enregistre les événements d'actualisation.

## Support multi-compte

Utilisez `channels.twitch.accounts` avec des jetons par compte. Voir [`gateway/configuration`](/gateway/configuration) pour le modèle partagé.

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

### Liste blanche par ID utilisateur (plus sécurisé)

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

`allowFrom` est une liste blanche stricte. Lorsqu'elle est définie, seuls ces ID utilisateur sont autorisés.
Si vous souhaitez un accès basé sur les rôles, laissez `allowFrom` non défini et configurez `allowedRoles` à la place :

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

Tout d'abord, exécutez les commandes de diagnostic :

```bash
openclaw doctor
openclaw channels status --probe
```

### Le bot ne répond pas aux messages

**Vérifiez le contrôle d'accès :** Assurez-vous que votre ID utilisateur est dans `allowFrom`, ou supprimez temporairement
`allowFrom` et définissez `allowedRoles: ["all"]` pour tester.

**Vérifiez que le bot est dans le canal :** Le bot doit rejoindre le canal spécifié dans `channel`.

### Problèmes de jeton

**"Échec de la connexion" ou erreurs d'authentification :**

- Vérifiez que `accessToken` est la valeur du jeton d'accès OAuth (commence généralement par le préfixe `oauth:`)
- Vérifiez que le jeton a les portées `chat:read` et `chat:write`
- Si vous utilisez l'actualisation du jeton, vérifiez que `clientSecret` et `refreshToken` sont définis

### L'actualisation du jeton ne fonctionne pas

**Vérifiez les journaux pour les événements d'actualisation :**

```
Using env token source for mybot
Access token refreshed for user 123456 (expires in 14400s)
```

Si vous voyez "token refresh disabled (no refresh token)" :

- Assurez-vous que `clientSecret` est fourni
- Assurez-vous que `refreshToken` est fourni

## Config

**Configuration du compte :**

- `username` - Nom d'utilisateur du bot
- `accessToken` - Jeton d'accès OAuth avec `chat:read` et `chat:write`
- `clientId` - ID client Twitch (du générateur de jetons ou de votre application)
- `channel` - Canal à rejoindre (requis)
- `enabled` - Activer ce compte (par défaut : `true`)
- `clientSecret` - Optionnel : Pour l'actualisation automatique du jeton
- `refreshToken` - Optionnel : Pour l'actualisation automatique du jeton
- `expiresIn` - Expiration du jeton en secondes
- `obtainmentTimestamp` - Horodatage d'obtention du jeton
- `allowFrom` - Liste blanche des ID utilisateur
- `allowedRoles` - Contrôle d'accès basé sur les rôles (`"moderator" | "owner" | "vip" | "subscriber" | "all"`)
- `requireMention` - Exiger @mention (par défaut : `true`)

**Options du fournisseur :**

- `channels.twitch.enabled` - Activer/désactiver le démarrage du canal
- `channels.twitch.username` - Nom d'utilisateur du bot (configuration simplifiée à compte unique)
- `channels.twitch.accessToken` - Jeton d'accès OAuth (configuration simplifiée à compte unique)
- `channels.twitch.clientId` - ID client Twitch (configuration simplifiée à compte unique)
- `channels.twitch.channel` - Canal à rejoindre (configuration simplifiée à compte unique)
- `channels.twitch.accounts.<accountName>` - Configuration multi-compte (tous les champs de compte ci-dessus)

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

L'agent peut appeler `twitch` avec l'action :

- `send` - Envoyer un message à un canal

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

## Sécurité et opérations

- **Traitez les jetons comme des mots de passe** - Ne validez jamais les jetons dans git
- **Utilisez l'actualisation automatique des jetons** pour les bots de longue durée
- **Utilisez des listes blanches d'ID utilisateur** au lieu de noms d'utilisateur pour le contrôle d'accès
- **Surveillez les journaux** pour les événements d'actualisation des jetons et l'état de la connexion
- **Limitez les portées des jetons** - Demandez uniquement `chat:read` et `chat:write`
- **Si vous êtes bloqué** : Redémarrez la passerelle après avoir confirmé qu'aucun autre processus ne possède la session

## Limites

- **500 caractères** par message (auto-fragmenté aux limites des mots)
- Markdown est supprimé avant la fragmentation
- Pas de limitation de débit (utilise les limites de débit intégrées de Twitch)
