---
summary: "Configuration de bot Mattermost et config OpenClaw"
read_when:
  - Setting up Mattermost
  - Debugging Mattermost routing
title: "Mattermost"
---

# Mattermost (plugin)

Statut : supporté via plugin (jeton de bot + événements WebSocket). Les canaux, groupes et DMs sont supportés.
Mattermost est une plateforme de messagerie d'équipe auto-hébergeable ; consultez le site officiel sur
[mattermost.com](https://mattermost.com) pour les détails du produit et les téléchargements.

## Plugin requis

Mattermost est fourni en tant que plugin et n'est pas inclus dans l'installation principale.

Installez via CLI (registre npm) :

```bash
openclaw plugins install @openclaw/mattermost
```

Checkout local (lors de l'exécution à partir d'un dépôt git) :

```bash
openclaw plugins install ./extensions/mattermost
```

Si vous choisissez Mattermost lors de la configuration/intégration et qu'un checkout git est détecté,
OpenClaw proposera automatiquement le chemin d'installation local.

Détails : [Plugins](/tools/plugin)

## Configuration rapide

1. Installez le plugin Mattermost.
2. Créez un compte de bot Mattermost et copiez le **jeton de bot**.
3. Copiez l'**URL de base** de Mattermost (par exemple, `https://chat.example.com`).
4. Configurez OpenClaw et démarrez la passerelle.

Configuration minimale :

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
    },
  },
}
```

## Commandes slash natives

Les commandes slash natives sont optionnelles. Lorsqu'elles sont activées, OpenClaw enregistre les commandes slash `oc_*` via
l'API Mattermost et reçoit les POSTs de rappel sur le serveur HTTP de la passerelle.

```json5
{
  channels: {
    mattermost: {
      commands: {
        native: true,
        nativeSkills: true,
        callbackPath: "/api/channels/mattermost/command",
        // À utiliser lorsque Mattermost ne peut pas atteindre la passerelle directement (proxy inverse/URL publique).
        callbackUrl: "https://gateway.example.com/api/channels/mattermost/command",
      },
    },
  },
}
```

Notes :

- `native: "auto"` est désactivé par défaut pour Mattermost. Définissez `native: true` pour activer.
- Si `callbackUrl` est omis, OpenClaw en dérive un à partir de l'hôte/port de la passerelle + `callbackPath`.
- Pour les configurations multi-comptes, `commands` peut être défini au niveau supérieur ou sous
  `channels.mattermost.accounts.<id>.commands` (les valeurs du compte remplacent les champs de niveau supérieur).
- Les rappels de commande sont validés avec des jetons par commande et échouent fermés lorsque les vérifications de jetons échouent.
- Exigence de disponibilité : le point de terminaison de rappel doit être accessible depuis le serveur Mattermost.
  - Ne définissez pas `callbackUrl` sur `localhost` sauf si Mattermost s'exécute sur le même hôte/espace de noms réseau qu'OpenClaw.
  - Ne définissez pas `callbackUrl` sur votre URL de base Mattermost sauf si cette URL fait un proxy inverse de `/api/channels/mattermost/command` vers OpenClaw.
  - Une vérification rapide est `curl https://<gateway-host>/api/channels/mattermost/command` ; un GET devrait retourner `405 Method Not Allowed` d'OpenClaw, pas `404`.
- Exigence de liste blanche de sortie Mattermost :
  - Si votre rappel cible des adresses privées/tailnet/internes, définissez Mattermost
    `ServiceSettings.AllowedUntrustedInternalConnections` pour inclure l'hôte/domaine de rappel.
  - Utilisez les entrées hôte/domaine, pas les URL complètes.
    - Bon : `gateway.tailnet-name.ts.net`
    - Mauvais : `https://gateway.tailnet-name.ts.net`

## Variables d'environnement (compte par défaut)

Définissez-les sur l'hôte de la passerelle si vous préférez les variables d'environnement :

- `MATTERMOST_BOT_TOKEN=...`
- `MATTERMOST_URL=https://chat.example.com`

Les variables d'environnement s'appliquent uniquement au compte **par défaut** (`default`). Les autres comptes doivent utiliser les valeurs de configuration.

## Modes de chat

Mattermost répond automatiquement aux DMs. Le comportement du canal est contrôlé par `chatmode` :

- `oncall` (par défaut) : répondre uniquement lorsque @mentionné dans les canaux.
- `onmessage` : répondre à chaque message du canal.
- `onchar` : répondre lorsqu'un message commence par un préfixe de déclenchement.

Exemple de configuration :

```json5
{
  channels: {
    mattermost: {
      chatmode: "onchar",
      oncharPrefixes: [">", "!"],
    },
  },
}
```

Notes :

- `onchar` répond toujours aux @mentions explicites.
- `channels.mattermost.requireMention` est honoré pour les configurations héritées mais `chatmode` est préféré.

## Threading et sessions

Utilisez `channels.mattermost.replyToMode` pour contrôler si les réponses de canal et de groupe restent dans le
canal principal ou démarrent un thread sous le message déclencheur.

- `off` (par défaut) : répondre uniquement dans un thread lorsque le message entrant est déjà dans un.
- `first` : pour les messages de canal/groupe de niveau supérieur, démarrer un thread sous ce message et router la
  conversation vers une session limitée au thread.
- `all` : même comportement que `first` pour Mattermost aujourd'hui.
- Les messages directs ignorent ce paramètre et restent non-threadés.

Exemple de configuration :

```json5
{
  channels: {
    mattermost: {
      replyToMode: "all",
    },
  },
}
```

Notes :

- Les sessions limitées au thread utilisent l'ID du message déclencheur comme racine du thread.
- `first` et `all` sont actuellement équivalents car une fois que Mattermost a une racine de thread,
  les chunks suivants et les médias continuent dans le même thread.

## Contrôle d'accès (DMs)

- Par défaut : `channels.mattermost.dmPolicy = "pairing"` (les expéditeurs inconnus reçoivent un code d'appairage).
- Approuver via :
  - `openclaw pairing list mattermost`
  - `openclaw pairing approve mattermost <CODE>`
- DMs publics : `channels.mattermost.dmPolicy="open"` plus `channels.mattermost.allowFrom=["*"]`.

## Canaux (groupes)

- Par défaut : `channels.mattermost.groupPolicy = "allowlist"` (mention-gated).
- Ajouter les expéditeurs à la liste blanche avec `channels.mattermost.groupAllowFrom` (IDs utilisateur recommandés).
- La correspondance `@username` est mutable et activée uniquement lorsque `channels.mattermost.dangerouslyAllowNameMatching: true`.
- Canaux ouverts : `channels.mattermost.groupPolicy="open"` (mention-gated).
- Note d'exécution : si `channels.mattermost` est complètement absent, l'exécution revient à `groupPolicy="allowlist"` pour les vérifications de groupe (même si `channels.defaults.groupPolicy` est défini).

## Cibles pour la livraison sortante

Utilisez ces formats de cible avec `openclaw message send` ou cron/webhooks :

- `channel:<id>` pour un canal
- `user:<id>` pour un DM
- `@username` pour un DM (résolu via l'API Mattermost)

Les IDs opaques nus (comme `64ifufp...`) sont **ambigus** dans Mattermost (ID utilisateur vs ID canal).

OpenClaw les résout **en priorité utilisateur** :

- Si l'ID existe en tant qu'utilisateur (`GET /api/v4/users/<id>` réussit), OpenClaw envoie un **DM** en résolvant le canal direct via `/api/v4/channels/direct`.
- Sinon, l'ID est traité comme un **ID de canal**.

Si vous avez besoin d'un comportement déterministe, utilisez toujours les préfixes explicites (`user:<id>` / `channel:<id>`).

## Réactions (outil de message)

- Utilisez `message action=react` avec `channel=mattermost`.
- `messageId` est l'ID du message Mattermost.
- `emoji` accepte les noms comme `thumbsup` ou `:+1:` (les deux-points sont optionnels).
- Définissez `remove=true` (booléen) pour supprimer une réaction.
- Les événements d'ajout/suppression de réaction sont transmis en tant qu'événements système à la session d'agent routée.

Exemples :

```
message action=react channel=mattermost target=channel:<channelId> messageId=<postId> emoji=thumbsup
message action=react channel=mattermost target=channel:<channelId> messageId=<postId> emoji=thumbsup remove=true
```

Configuration :

- `channels.mattermost.actions.reactions` : activer/désactiver les actions de réaction (par défaut true).
- Remplacement par compte : `channels.mattermost.accounts.<id>.actions.reactions`.

## Boutons interactifs (outil de message)

Envoyez des messages avec des boutons cliquables. Lorsqu'un utilisateur clique sur un bouton, l'agent reçoit la
sélection et peut répondre.

Activez les boutons en ajoutant `inlineButtons` aux capacités du canal :

```json5
{
  channels: {
    mattermost: {
      capabilities: ["inlineButtons"],
    },
  },
}
```

Utilisez `message action=send` avec un paramètre `buttons`. Les boutons sont un tableau 2D (lignes de boutons) :

```
message action=send channel=mattermost target=channel:<channelId> buttons=[[{"text":"Yes","callback_data":"yes"},{"text":"No","callback_data":"no"}]]
```

Champs de bouton :

- `text` (requis) : étiquette d'affichage.
- `callback_data` (requis) : valeur renvoyée au clic (utilisée comme ID d'action).
- `style` (optionnel) : `"default"`, `"primary"`, ou `"danger"`.

Lorsqu'un utilisateur clique sur un bouton :

1. Tous les boutons sont remplacés par une ligne de confirmation (par exemple, "✓ **Yes** sélectionné par @user").
2. L'agent reçoit la sélection en tant que message entrant et répond.

Notes :

- Les rappels de bouton utilisent la vérification HMAC-SHA256 (automatique, aucune configuration nécessaire).
- Mattermost supprime les données de rappel de ses réponses API (fonctionnalité de sécurité), donc tous les boutons
  sont supprimés au clic — la suppression partielle n'est pas possible.
- Les IDs d'action contenant des tirets ou des traits de soulignement sont automatiquement assainis
  (limitation du routage Mattermost).

Configuration :

- `channels.mattermost.capabilities` : tableau de chaînes de capacité. Ajoutez `"inlineButtons"` pour
  activer la description de l'outil de boutons dans l'invite système de l'agent.
- `channels.mattermost.interactions.callbackBaseUrl` : URL de base externe optionnelle pour les
  rappels de bouton (par exemple `https://gateway.example.com`). Utilisez ceci lorsque Mattermost ne peut pas
  atteindre la passerelle à son hôte de liaison directement.
- Dans les configurations multi-comptes, vous pouvez également définir le même champ sous
  `channels.mattermost.accounts.<id>.interactions.callbackBaseUrl`.
- Si `interactions.callbackBaseUrl` est omis, OpenClaw dérive l'URL de rappel de
  `gateway.customBindHost` + `gateway.port`, puis revient à `http://localhost:<port>`.
- Règle de disponibilité : l'URL de rappel de bouton doit être accessible depuis le serveur Mattermost.
  `localhost` ne fonctionne que lorsque Mattermost et OpenClaw s'exécutent sur le même hôte/espace de noms réseau.
- Si votre cible de rappel est privée/tailnet/interne, ajoutez son hôte/domaine à Mattermost
  `ServiceSettings.AllowedUntrustedInternalConnections`.

### Intégration API directe (scripts externes)

Les scripts externes et webhooks peuvent poster des boutons directement via l'API REST Mattermost
au lieu de passer par l'outil `message` de l'agent. Utilisez `buildButtonAttachments()` de
l'extension si possible ; si vous postez du JSON brut, suivez ces règles :

**Structure de la charge utile :**

```json5
{
  channel_id: "<channelId>",
  message: "Choose an option:",
  props: {
    attachments: [
      {
        actions: [
          {
            id: "mybutton01", // alphanumeric only — see below
            type: "button", // required, or clicks are silently ignored
            name: "Approve", // display label
            style: "primary", // optional: "default", "primary", "danger"
            integration: {
              url: "https://gateway.example.com/mattermost/interactions/default",
              context: {
                action_id: "mybutton01", // must match button id (for name lookup)
                action: "approve",
                // ... any custom fields ...
                _token: "<hmac>", // see HMAC section below
              },
            },
          },
        ],
      },
    ],
  },
}
```

**Règles critiques :**

1. Les pièces jointes vont dans `props.attachments`, pas au niveau supérieur `attachments` (ignorées silencieusement).
2. Chaque action a besoin de `type: "button"` — sans cela, les clics sont avalés silencieusement.
3. Chaque action a besoin d'un champ `id` — Mattermost ignore les actions sans IDs.
4. L'`id` d'action doit être **alphanumérique uniquement** (`[a-zA-Z0-9]`). Les tirets et traits
