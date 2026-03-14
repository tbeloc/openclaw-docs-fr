---
read_when:
  - 开发 Google Chat 渠道功能时
summary: Google Chat 应用支持状态、功能和配置
title: Google Chat
x-i18n:
  generated_at: "2026-02-03T07:43:39Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 3b2bb116cdd12614c3d5afddd0879e9deb05c3606e3a2385cbc07f23552b357e
  source_path: channels/googlechat.md
  workflow: 15
---

# Google Chat（Chat API）

Statut : Pris en charge via les webhooks de l'API Google Chat (HTTP uniquement) pour les messages directs et les espaces.

## Configuration rapide (débutants)

1. Créez un projet Google Cloud et activez l'**API Google Chat**.
   - Accédez à : [Google Chat API Credentials](https://console.cloud.google.com/apis/api/chat.googleapis.com/credentials)
   - Si l'API n'est pas encore activée, activez-la.
2. Créez un **compte de service** :
   - Cliquez sur **Create Credentials** > **Service Account**.
   - Nommez-le librement (par exemple `openclaw-chat`).
   - Laissez les permissions vides (cliquez sur **Continue**).
   - Laissez le compte principal avec accès vide (cliquez sur **Done**).
3. Créez et téléchargez une **clé JSON** :
   - Dans la liste des comptes de service, cliquez sur le compte que vous venez de créer.
   - Accédez à l'onglet **Keys**.
   - Cliquez sur **Add Key** > **Create new key**.
   - Sélectionnez **JSON** et cliquez sur **Create**.
4. Stockez le fichier JSON téléchargé sur l'hôte Gateway (par exemple `~/.openclaw/googlechat-service-account.json`).
5. Créez une application Google Chat dans la [Configuration Google Cloud Console Chat](https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat) :
   - Remplissez les **informations de l'application** :
     - **App name** : (par exemple `OpenClaw`)
     - **Avatar URL** : (par exemple `https://openclaw.ai/logo.png`)
     - **Description** : (par exemple `Personal AI Assistant`)
   - Activez les **fonctionnalités interactives**.
   - Sous **Functionality**, cochez **Join spaces and group conversations**.
   - Sous **Connection settings**, sélectionnez **HTTP endpoint URL**.
   - Sous **Triggers**, sélectionnez **Use a common HTTP endpoint URL for all triggers** et définissez-le sur votre URL publique Gateway suivie de `/googlechat`.
     - _Conseil : exécutez `openclaw status` pour voir votre URL publique Gateway._
   - Sous **Visibility**, cochez **Make this Chat app available to specific people and groups in &lt;Your Domain&gt;**.
   - Entrez votre adresse e-mail dans la zone de texte (par exemple `user@example.com`).
   - Cliquez sur **Save** en bas.
6. **Activez l'état de l'application** :
   - Après l'enregistrement, **actualisez la page**.
   - Trouvez la section **App status** (généralement près du haut ou du bas après l'enregistrement).
   - Changez l'état en **Live - available to users**.
   - Cliquez à nouveau sur **Save**.
7. Configurez OpenClaw avec le chemin du compte de service et l'audience du webhook :
   - Variable d'environnement : `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/path/to/service-account.json`
   - Ou configuration : `channels.googlechat.serviceAccountFile: "/path/to/service-account.json"`.
8. Définissez le type et la valeur de l'audience du webhook (correspondant à votre configuration d'application Chat).
9. Démarrez Gateway. Google Chat enverra des requêtes POST à votre chemin webhook.

## Ajouter à Google Chat

Une fois Gateway en cours d'exécution et votre e-mail ajouté à la liste de visibilité :

1. Accédez à [Google Chat](https://chat.google.com/).
2. Cliquez sur l'icône **+** (plus) à côté de **Direct Messages**.
3. Dans la barre de recherche (généralement utilisée pour ajouter des contacts), entrez le **App name** que vous avez configuré dans Google Cloud Console.
   - **Remarque** : le bot *n'apparaîtra pas* dans la liste de navigation "Marketplace" car c'est une application privée. Vous devez le rechercher par nom.
4. Sélectionnez votre bot dans les résultats.
5. Cliquez sur **Add** ou **Chat** pour démarrer une conversation individuelle.
6. Envoyez "Hello" pour déclencher l'assistant !

## URL publique (webhooks uniquement)

Les webhooks Google Chat nécessitent un point de terminaison HTTPS public. Pour des raisons de sécurité, **exposez uniquement le chemin `/googlechat` à Internet**. Gardez le tableau de bord OpenClaw et les autres points de terminaison sensibles sur votre réseau privé.

### Option A : Tailscale Funnel (recommandé)

Utilisez Tailscale Serve pour servir le tableau de bord privé et Funnel pour le chemin webhook public. Cela permet de garder `/` privé tout en exposant uniquement `/googlechat`.

1. **Vérifiez l'adresse à laquelle votre Gateway est liée :**

   ```bash
   ss -tlnp | grep 18789
   ```

   Notez l'adresse IP (par exemple `127.0.0.1`, `0.0.0.0` ou votre IP Tailscale comme `100.x.x.x`).

2. **Exposez le tableau de bord uniquement à votre tailnet (port 8443) :**

   ```bash
   # Si lié à localhost (127.0.0.1 ou 0.0.0.0) :
   tailscale serve --bg --https 8443 http://127.0.0.1:18789

   # Si lié uniquement à l'IP Tailscale (par exemple 100.106.161.80) :
   tailscale serve --bg --https 8443 http://100.106.161.80:18789
   ```

3. **Exposez publiquement uniquement le chemin webhook :**

   ```bash
   # Si lié à localhost (127.0.0.1 ou 0.0.0.0) :
   tailscale funnel --bg --set-path /googlechat http://127.0.0.1:18789/googlechat

   # Si lié uniquement à l'IP Tailscale (par exemple 100.106.161.80) :
   tailscale funnel --bg --set-path /googlechat http://100.106.161.80:18789/googlechat
   ```

4. **Autorisez le nœud à accéder à Funnel :**
   Si vous y êtes invité, visitez l'URL d'autorisation affichée dans la sortie pour activer Funnel pour ce nœud dans votre politique tailnet.

5. **Vérifiez la configuration :**
   ```bash
   tailscale serve status
   tailscale funnel status
   ```

Votre URL webhook publique sera :
`https://<node-name>.<tailnet>.ts.net/googlechat`

Votre tableau de bord privé est accessible uniquement via tailnet :
`https://<node-name>.<tailnet>.ts.net:8443/`

Utilisez l'URL publique (sans `:8443`) dans la configuration de votre application Google Chat.

> Remarque : cette configuration persiste après redémarrage. Pour la supprimer ultérieurement, exécutez `tailscale funnel reset` et `tailscale serve reset`.

### Option B : Proxy inverse (Caddy)

Si vous utilisez un proxy inverse comme Caddy, ne proxifiez que le chemin spécifique :

```caddy
your-domain.com {
    reverse_proxy /googlechat* localhost:18789
}
```

Avec cette configuration, toute requête vers `your-domain.com/` sera ignorée ou retournera 404, tandis que `your-domain.com/googlechat` sera routée en toute sécurité vers OpenClaw.

### Option C : Cloudflare Tunnel

Configurez vos règles d'entrée de tunnel pour router uniquement le chemin webhook :

- **Chemin** : `/googlechat` -> `http://localhost:18789/googlechat`
- **Règle par défaut** : HTTP 404 (non trouvé)

## Fonctionnement

1. Google Chat envoie une requête POST webhook à Gateway. Chaque requête inclut un en-tête `Authorization: Bearer <token>`.
2. OpenClaw valide le jeton selon le `audienceType` + `audience` configuré :
   - `audienceType: "app-url"` → l'audience est votre URL webhook HTTPS.
   - `audienceType: "project-number"` → l'audience est le numéro du projet Cloud.
3. Les messages sont routés par espace :
   - Les messages directs utilisent la clé de session `agent:<agentId>:googlechat:dm:<spaceId>`.
   - Les espaces utilisent la clé de session `agent:<agentId>:googlechat:group:<spaceId>`.
4. L'accès aux messages directs est par défaut en mode appairage. Les expéditeurs inconnus reçoivent un code d'appairage ; approuvez avec :
   - `openclaw pairing approve googlechat <code>`
5. Les espaces de groupe nécessitent par défaut une @mention. Si la détection de mention a besoin du nom d'utilisateur de l'application, utilisez `botUser`.

## Identifiants de destination

Utilisez ces identifiants pour la livraison de messages et les listes d'autorisation :

- Messages directs : `users/<userId>` ou `users/<email>` (accepte les adresses e-mail).
- Espaces : `spaces/<spaceId>`.

## Points clés de configuration

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url",
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // Optionnel ; aide à la détection de mention
      dm: {
        policy: "pairing",
        allowFrom: ["users/1234567890", "name@example.com"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": {
          allow: true,
          requireMention: true,
          users: ["users/1234567890"],
          systemPrompt: "Short answers only.",
        },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

Points à noter :

- Les identifiants du compte de service peuvent également être transmis en ligne via `serviceAccount` (chaîne JSON).
- Si `webhookPath` n'est pas défini, le chemin webhook par défaut est `/googlechat`.
- Lorsque `actions.reactions` est activé, les réactions d'emoji sont disponibles via l'outil `reactions` et `channels action`.
- `typingIndicator` supporte `none`, `message` (par défaut) et `reaction` (reaction nécessite OAuth utilisateur).
- Les pièces jointes sont téléchargées via l'API Chat et stockées dans le pipeline média (taille limitée par `mediaMaxMb`).

## Dépannage

### 405 Method Not Allowed

Si Google Cloud Logs Explorer affiche une erreur comme :

```
status code: 405, reason phrase: HTTP error response: HTTP/1.1 405 Method Not Allowed
```

Cela signifie que le gestionnaire webhook n'est pas enregistré. Causes courantes :

1. **Canal non configuré** : la section `channels.googlechat` manque dans la configuration. Vérifiez avec :

   ```bash
   openclaw config get channels.googlechat
   ```

   Si cela retourne "Config path not found", ajoutez la configuration (voir [Points clés de configuration](#points-clés-de-configuration)).

2. **Plugin non activé** : vérifiez l'état du plugin :

   ```bash
   openclaw plugins list | grep googlechat
   ```

   S'il affiche "disabled", ajoutez `plugins.entries.googlechat.enabled: true` à votre configuration.

3. **Gateway non redémarrée** : après avoir ajouté la configuration, redémarrez Gateway :
   ```bash
   openclaw gateway restart
   ```

Vérifiez que le canal est en cours d'exécution :

```bash
openclaw channels status
# Devrait afficher : Google Chat default: enabled, configured, ...
```

### Autres problèmes

- Vérifiez `openclaw channels status --probe` pour voir les erreurs d'authentification ou la configuration d'audience manquante.
- Si vous ne recevez pas de messages, confirmez l'URL webhook et les abonnements aux événements de l'application Chat.
- Si le contrôle de mention bloque les réponses, définissez `botUser` sur le nom de ressource utilisateur de l'application et vérifiez `requireMention`.
- Utilisez `openclaw logs --follow` lors de l'envoi de messages de test pour voir si les requêtes arrivent à Gateway.

Documentation connexe :

- [Configuration Gateway](/gateway/configuration)
- [Sécurité](/gateway/security)
- [Réactions d'emoji](/tools/reactions)
