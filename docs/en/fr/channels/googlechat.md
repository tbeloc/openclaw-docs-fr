---
summary: "Statut de support de l'application Google Chat, capacités et configuration"
read_when:
  - Working on Google Chat channel features
title: "Google Chat"
---

# Google Chat (Chat API)

Statut : prêt pour les DM + espaces via les webhooks de l'API Google Chat (HTTP uniquement).

## Configuration rapide (débutant)

1. Créez un projet Google Cloud et activez l'**API Google Chat**.
   - Allez à : [Identifiants de l'API Google Chat](https://console.cloud.google.com/apis/api/chat.googleapis.com/credentials)
   - Activez l'API si elle n'est pas déjà activée.
2. Créez un **Compte de service** :
   - Appuyez sur **Créer des identifiants** > **Compte de service**.
   - Nommez-le comme vous le souhaitez (par exemple, `openclaw-chat`).
   - Laissez les permissions vides (appuyez sur **Continuer**).
   - Laissez les principaux ayant accès vides (appuyez sur **Terminé**).
3. Créez et téléchargez la **Clé JSON** :
   - Dans la liste des comptes de service, cliquez sur celui que vous venez de créer.
   - Allez à l'onglet **Clés**.
   - Cliquez sur **Ajouter une clé** > **Créer une nouvelle clé**.
   - Sélectionnez **JSON** et appuyez sur **Créer**.
4. Stockez le fichier JSON téléchargé sur votre hôte de passerelle (par exemple, `~/.openclaw/googlechat-service-account.json`).
5. Créez une application Google Chat dans la [Configuration Google Chat de la console Google Cloud](https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat) :
   - Remplissez les **Informations sur l'application** :
     - **Nom de l'application** : (par exemple `OpenClaw`)
     - **URL de l'avatar** : (par exemple `https://openclaw.ai/logo.png`)
     - **Description** : (par exemple `Assistant IA personnel`)
   - Activez les **Fonctionnalités interactives**.
   - Sous **Fonctionnalité**, cochez **Rejoindre des espaces et des conversations de groupe**.
   - Sous **Paramètres de connexion**, sélectionnez **URL du point de terminaison HTTP**.
   - Sous **Déclencheurs**, sélectionnez **Utiliser une URL de point de terminaison HTTP commune pour tous les déclencheurs** et définissez-la sur l'URL publique de votre passerelle suivie de `/googlechat`.
     - _Conseil : Exécutez `openclaw status` pour trouver l'URL publique de votre passerelle._
   - Sous **Visibilité**, cochez **Rendre cette application Google Chat disponible pour des personnes et des groupes spécifiques dans &lt;Votre domaine&gt;**.
   - Entrez votre adresse e-mail (par exemple `user@example.com`) dans la zone de texte.
   - Cliquez sur **Enregistrer** en bas.
6. **Activez le statut de l'application** :
   - Après l'enregistrement, **actualisez la page**.
   - Recherchez la section **Statut de l'application** (généralement près du haut ou du bas après l'enregistrement).
   - Changez le statut en **En direct - disponible pour les utilisateurs**.
   - Cliquez à nouveau sur **Enregistrer**.
7. Configurez OpenClaw avec le chemin du compte de service + l'audience du webhook :
   - Env : `GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/path/to/service-account.json`
   - Ou config : `channels.googlechat.serviceAccountFile: "/path/to/service-account.json"`.
8. Définissez le type d'audience du webhook + la valeur (correspond à votre configuration d'application Chat).
9. Démarrez la passerelle. Google Chat enverra des POST à votre chemin de webhook.

## Ajouter à Google Chat

Une fois la passerelle en cours d'exécution et votre e-mail ajouté à la liste de visibilité :

1. Allez à [Google Chat](https://chat.google.com/).
2. Cliquez sur l'icône **+** (plus) à côté de **Messages directs**.
3. Dans la barre de recherche (où vous ajoutez généralement des personnes), tapez le **Nom de l'application** que vous avez configuré dans la console Google Cloud.
   - **Remarque** : Le bot n'apparaîtra _pas_ dans la liste de navigation "Marketplace" car c'est une application privée. Vous devez la rechercher par nom.
4. Sélectionnez votre bot dans les résultats.
5. Cliquez sur **Ajouter** ou **Discuter** pour démarrer une conversation 1:1.
6. Envoyez "Bonjour" pour déclencher l'assistant !

## URL publique (Webhook uniquement)

Les webhooks Google Chat nécessitent un point de terminaison HTTPS public. Pour la sécurité, **exposez uniquement le chemin `/googlechat`** à Internet. Gardez le tableau de bord OpenClaw et les autres points de terminaison sensibles sur votre réseau privé.

### Option A : Tailscale Funnel (Recommandé)

Utilisez Tailscale Serve pour le tableau de bord privé et Funnel pour le chemin du webhook public. Cela garde `/` privé tout en exposant uniquement `/googlechat`.

1. **Vérifiez à quelle adresse votre passerelle est liée :**

   ```bash
   ss -tlnp | grep 18789
   ```

   Notez l'adresse IP (par exemple, `127.0.0.1`, `0.0.0.0`, ou votre IP Tailscale comme `100.x.x.x`).

2. **Exposez le tableau de bord au tailnet uniquement (port 8443) :**

   ```bash
   # Si lié à localhost (127.0.0.1 ou 0.0.0.0) :
   tailscale serve --bg --https 8443 http://127.0.0.1:18789

   # Si lié à l'IP Tailscale uniquement (par exemple, 100.106.161.80) :
   tailscale serve --bg --https 8443 http://100.106.161.80:18789
   ```

3. **Exposez uniquement le chemin du webhook publiquement :**

   ```bash
   # Si lié à localhost (127.0.0.1 ou 0.0.0.0) :
   tailscale funnel --bg --set-path /googlechat http://127.0.0.1:18789/googlechat

   # Si lié à l'IP Tailscale uniquement (par exemple, 100.106.161.80) :
   tailscale funnel --bg --set-path /googlechat http://100.106.161.80:18789/googlechat
   ```

4. **Autorisez le nœud pour l'accès Funnel :**
   Si vous y êtes invité, visitez l'URL d'autorisation affichée dans la sortie pour activer Funnel pour ce nœud dans votre politique tailnet.

5. **Vérifiez la configuration :**

   ```bash
   tailscale serve status
   tailscale funnel status
   ```

Votre URL de webhook public sera :
`https://<node-name>.<tailnet>.ts.net/googlechat`

Votre tableau de bord privé reste réservé au tailnet :
`https://<node-name>.<tailnet>.ts.net:8443/`

Utilisez l'URL publique (sans `:8443`) dans la configuration de l'application Google Chat.

> Remarque : Cette configuration persiste après les redémarrages. Pour la supprimer ultérieurement, exécutez `tailscale funnel reset` et `tailscale serve reset`.

### Option B : Proxy inverse (Caddy)

Si vous utilisez un proxy inverse comme Caddy, ne proxifiez que le chemin spécifique :

```caddy
your-domain.com {
    reverse_proxy /googlechat* localhost:18789
}
```

Avec cette configuration, toute demande à `your-domain.com/` sera ignorée ou retournera 404, tandis que `your-domain.com/googlechat` est correctement acheminée vers OpenClaw.

### Option C : Tunnel Cloudflare

Configurez les règles d'entrée de votre tunnel pour n'acheminer que le chemin du webhook :

- **Chemin** : `/googlechat` -> `http://localhost:18789/googlechat`
- **Règle par défaut** : HTTP 404 (Non trouvé)

## Fonctionnement

1. Google Chat envoie des POST de webhook à la passerelle. Chaque demande inclut un en-tête `Authorization: Bearer <token>`.
   - OpenClaw vérifie l'authentification du porteur avant de lire/analyser les corps complets du webhook lorsque l'en-tête est présent.
   - Les demandes de complément Google Workspace qui portent `authorizationEventObject.systemIdToken` dans le corps sont prises en charge via un budget de pré-authentification du corps plus strict.
2. OpenClaw vérifie le jeton par rapport au `audienceType` + `audience` configuré :
   - `audienceType: "app-url"` → l'audience est votre URL de webhook HTTPS.
   - `audienceType: "project-number"` → l'audience est le numéro du projet Cloud.
3. Les messages sont acheminés par espace :
   - Les DM utilisent la clé de session `agent:<agentId>:googlechat:direct:<spaceId>`.
   - Les espaces utilisent la clé de session `agent:<agentId>:googlechat:group:<spaceId>`.
4. L'accès aux DM est l'appairage par défaut. Les expéditeurs inconnus reçoivent un code d'appairage ; approuvez avec :
   - `openclaw pairing approve googlechat <code>`
5. Les espaces de groupe nécessitent une @-mention par défaut. Utilisez `botUser` si la détection de mention a besoin du nom d'utilisateur de l'application.

## Cibles

Utilisez ces identifiants pour la livraison et les listes d'autorisation :

- Messages directs : `users/<userId>` (recommandé).
- L'e-mail brut `name@example.com` est mutable et n'est utilisé que pour la correspondance directe de la liste d'autorisation lorsque `channels.googlechat.dangerouslyAllowNameMatching: true`.
- Déprécié : `users/<email>` est traité comme un ID utilisateur, pas une liste d'autorisation d'e-mail.
- Espaces : `spaces/<spaceId>`.

## Points clés de la configuration

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      // ou serviceAccountRef: { source: "file", provider: "filemain", id: "/channels/googlechat/serviceAccount" }
      audienceType: "app-url",
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optionnel ; aide à la détection de mention
      dm: {
        policy: "pairing",
        allowFrom: ["users/1234567890"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": {
          allow: true,
          requireMention: true,
          users: ["users/1234567890"],
          systemPrompt: "Réponses courtes uniquement.",
        },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

Remarques :

- Les identifiants du compte de service peuvent également être transmis en ligne avec `serviceAccount` (chaîne JSON).
- `serviceAccountRef` est également pris en charge (SecretRef env/file), y compris les références par compte sous `channels.googlechat.accounts.<id>.serviceAccountRef`.
- Le chemin du webhook par défaut est `/googlechat` si `webhookPath` n'est pas défini.
- `dangerouslyAllowNameMatching` réactive la correspondance du principal d'e-mail mutable pour les listes d'autorisation (mode de compatibilité de secours).
- Les réactions sont disponibles via l'outil `reactions` et `channels action` lorsque `actions.reactions` est activé.
- `typingIndicator` prend en charge `none`, `message` (par défaut) et `reaction` (la réaction nécessite OAuth utilisateur).
- Les pièces jointes sont téléchargées via l'API Chat et stockées dans le pipeline multimédia (taille limitée par `mediaMaxMb`).

Détails de la référence des secrets : [Gestion des secrets](/gateway/secrets).

## Dépannage

### 405 Method Not Allowed

Si Google Cloud Logs Explorer affiche des erreurs comme :

```
status code: 405, reason phrase: HTTP error response: HTTP/1.1 405 Method Not Allowed
```

Cela signifie que le gestionnaire de webhook n'est pas enregistré. Les causes courantes sont :

1. **Canal non configuré** : La section `channels.googlechat` manque de votre configuration. Vérifiez avec :

   ```bash
   openclaw config get channels.googlechat
   ```

   Si elle retourne "Config path not found", ajoutez la configuration (voir [Points clés de la configuration](#points-clés-de-la-configuration)).

2. **Plugin non activé** : Vérifiez le statut du plugin :

   ```bash
   openclaw plugins list | grep googlechat
   ```

   S'il affiche "disabled", ajoutez `plugins.entries.googlechat.enabled: true` à votre configuration.

3. **Passerelle non redémarrée** : Après l'ajout de la configuration, redémarrez la passerelle :

   ```bash
   openclaw gateway restart
   ```

Vérifiez que le canal est en cours d'exécution :

```bash
openclaw channels status
# Devrait afficher : Google Chat default: enabled, configured, ...
```

### Autres problèmes

- Vérifiez `openclaw channels status --probe` pour les erreurs d'authentification ou la configuration d'audience manquante.
- Si aucun message n'arrive, confirmez l'URL du webhook de l'application Chat + les abonnements aux événements.
- Si la mention gating bloque les réponses, définissez `botUser` sur le nom de ressource utilisateur de l'application et vérifiez `requireMention`.
- Utilisez `openclaw logs --follow` tout en envoyant un message de test pour voir si les demandes atteignent la passerelle.

Documents connexes :

- [Configuration de la passerelle](/gateway/configuration)
- [Sécurité](/gateway/security)
- [Réactions](/tools/reactions)
