---
summary: "Configuration du canal SMS Twilio, contrôles d'accès et configuration des webhooks"
read_when:
  - You want to connect OpenClaw to SMS through Twilio
  - You need SMS webhook or allowlist setup
title: "SMS"
---

OpenClaw peut recevoir et envoyer des SMS via un numéro de téléphone Twilio ou un service de messagerie. La Gateway enregistre une route de webhook entrant, valide les signatures de requête Twilio par défaut et renvoie les réponses via l'API Messages de Twilio.

<CardGroup cols={3}>
  <Card title="Pairing" icon="link" href="/fr/channels/pairing">
    La politique DM par défaut pour SMS est l'appairage.
  </Card>
  <Card title="Gateway security" icon="shield" href="/fr/gateway/security">
    Examinez l'exposition des webhooks et les contrôles d'accès des expéditeurs.
  </Card>
  <Card title="Channel troubleshooting" icon="wrench" href="/fr/channels/troubleshooting">
    Diagnostics multi-canaux et playbooks de réparation.
  </Card>
</CardGroup>

## Avant de commencer

Vous avez besoin de :

- Un compte Twilio avec un numéro de téléphone compatible SMS ou un service de messagerie Twilio.
- L'identifiant de compte Twilio et le jeton d'authentification.
- Une URL HTTPS publique qui atteint votre Gateway OpenClaw.
- Un choix de politique d'expéditeur : `pairing` pour un usage privé, `allowlist` pour les numéros de téléphone préapprouvés, ou `open` uniquement pour un accès SMS intentionnellement public.

Utilisez un numéro Twilio pour SMS et appels vocaux si le numéro a les deux capacités. Configurez le webhook SMS et le webhook d'appel vocal séparément dans Twilio ; cette page couvre uniquement le webhook SMS.

## Configuration rapide

<Steps>
  <Step title="Créer ou choisir un expéditeur Twilio">
    Dans Twilio, ouvrez **Phone Numbers > Manage > Active numbers** et choisissez un numéro compatible SMS. Enregistrez :

    - Account SID, par exemple `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
    - Auth Token
    - Numéro de téléphone de l'expéditeur, par exemple `+15551234567`

    Si vous utilisez un service de messagerie au lieu d'un numéro d'expéditeur fixe, enregistrez le SID du service de messagerie, par exemple `MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.

  </Step>

  <Step title="Configurer le canal SMS">

Enregistrez ceci sous `sms.patch.json5` et modifiez les espaces réservés :

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: "twilio-auth-token",
      fromNumber: "+15551234567",
      publicWebhookUrl: "https://gateway.example.com/webhooks/sms",
      dmPolicy: "pairing",
    },
  },
}
```

Appliquez-le :

```bash
openclaw config patch --file ./sms.patch.json5 --dry-run
openclaw config patch --file ./sms.patch.json5
```

  </Step>

  <Step title="Pointer Twilio vers le webhook de la Gateway">
    Dans les paramètres du numéro de téléphone Twilio, ouvrez **Messaging** et définissez **A message comes in** sur :

```text
https://gateway.example.com/webhooks/sms
```

    Utilisez HTTP `POST`. Le chemin local par défaut est `/webhooks/sms` ; modifiez `channels.sms.webhookPath` si vous avez besoin d'une route différente.

  </Step>

  <Step title="Exposer le chemin exact du webhook SMS">
    Votre URL publique doit router le chemin SMS vers le processus Gateway. Si vous utilisez Tailscale Funnel pour les tests locaux, exposez `/webhooks/sms` explicitement :

```bash
tailscale funnel --bg --set-path /webhooks/sms http://127.0.0.1:<gateway-port>/webhooks/sms
tailscale funnel status
```

    Les appels vocaux et SMS utilisent des chemins de webhook séparés. Si le même numéro Twilio gère les deux, gardez les deux routes configurées dans Twilio et dans votre tunnel.

  </Step>

  <Step title="Démarrer la Gateway et approuver le premier expéditeur">

```bash
openclaw gateway
```

Envoyez un message texte au numéro Twilio. Le premier message crée une demande d'appairage. Approuvez-la :

```bash
openclaw pairing list sms
openclaw pairing approve sms <CODE>
```

    Les codes d'appairage expirent après 1 heure.

  </Step>
</Steps>

## Exemples de configuration

### Fichier de configuration

Utilisez la configuration par fichier quand vous voulez que la définition du canal voyage avec la configuration de la Gateway :

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: "twilio-auth-token",
      fromNumber: "+15551234567",
      publicWebhookUrl: "https://gateway.example.com/webhooks/sms",
      dmPolicy: "pairing",
    },
  },
}
```

### Variables d'environnement

Utilisez la configuration env pour les déploiements à compte unique où les secrets proviennent de l'environnement hôte :

```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="<twilio-auth-token>"
export TWILIO_PHONE_NUMBER="+15551234567"
export SMS_PUBLIC_WEBHOOK_URL="https://gateway.example.com/webhooks/sms"
```

Ensuite, activez le canal dans la configuration :

```json5
{
  channels: {
    sms: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

`TWILIO_SMS_FROM` est accepté comme alias pour `TWILIO_PHONE_NUMBER`. Utilisez `TWILIO_MESSAGING_SERVICE_SID` au lieu d'un expéditeur de numéro de téléphone quand Twilio doit choisir l'expéditeur dans un service de messagerie.

### Authentification SecretRef

`authToken` peut être une SecretRef. Utilisez ceci quand la Gateway doit résoudre le jeton d'authentification Twilio à partir du runtime des secrets OpenClaw au lieu de stocker la configuration en texte brut :

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: { source: "env", provider: "default", id: "TWILIO_AUTH_TOKEN" },
      fromNumber: "+15551234567",
      publicWebhookUrl: "https://gateway.example.com/webhooks/sms",
      dmPolicy: "pairing",
    },
  },
}
```

La variable d'environnement ou le fournisseur de secrets référencé doit être visible pour le runtime de la Gateway. Redémarrez les processus Gateway gérés après avoir modifié les variables d'environnement de l'hôte.

### Numéro privé avec liste d'autorisation uniquement

Utilisez `allowlist` quand seuls les numéros de téléphone connus doivent pouvoir communiquer avec l'agent :

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: "twilio-auth-token",
      fromNumber: "+15551234567",
      publicWebhookUrl: "https://gateway.example.com/webhooks/sms",
      dmPolicy: "allowlist",
      allowFrom: ["+15557654321"],
    },
  },
}
```

### Expéditeur du service de messagerie

Utilisez `messagingServiceSid` au lieu de `fromNumber` quand Twilio doit choisir l'expéditeur via un service de messagerie :

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: "twilio-auth-token",
      messagingServiceSid: "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      publicWebhookUrl: "https://gateway.example.com/webhooks/sms",
      dmPolicy: "pairing",
    },
  },
}
```

Si `fromNumber` et `messagingServiceSid` sont tous deux présents après la résolution de la configuration et de l'env, `fromNumber` est utilisé.

### Cible sortante par défaut

Définissez `defaultTo` quand l'automatisation ou la livraison initiée par l'agent doit avoir une destination par défaut si un flux d'envoi omet une cible explicite :

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: "twilio-auth-token",
      fromNumber: "+15551234567",
      defaultTo: "+15557654321",
      publicWebhookUrl: "https://gateway.example.com/webhooks/sms",
    },
  },
}
```

## Contrôle d'accès

`channels.sms.dmPolicy` contrôle l'accès SMS direct :

- `pairing` (par défaut)
- `allowlist` (nécessite au moins un expéditeur dans `allowFrom`)
- `open` (nécessite que `allowFrom` inclue `"*"`)
- `disabled`

Les entrées `allowFrom` doivent être des numéros de téléphone E.164 tels que `+15551234567`. Les préfixes `sms:` sont acceptés et normalisés. Pour un assistant privé, préférez `dmPolicy: "allowlist"` avec des numéros de téléphone explicites.

## Envoi de SMS

Les cibles SMS sortantes utilisent le préfixe de service `sms:` avec le canal SMS sélectionné :

```bash
openclaw message send --channel sms --target sms:+15551234567 --message "hello"
```

Quand la sélection du canal est implicite, `twilio-sms:+15551234567` sélectionne ce canal sans reprendre le préfixe de service `sms:` existant appartenant au canal utilisé par iMessage.

```bash
openclaw message send --target twilio-sms:+15551234567 --message "hello"
```

La CLI nécessite une `--target` explicite. `defaultTo` est pour les chemins d'automatisation et de livraison initiée par l'agent où la cible peut être résolue à partir de la configuration du canal.

Les réponses de l'agent à partir des conversations SMS entrantes reviennent automatiquement à l'expéditeur via l'expéditeur Twilio configuré.

La sortie SMS est du texte brut. OpenClaw supprime le markdown, aplatit les blocs de code clôturés, préserve les liens lisibles et divise les réponses longues avant de les envoyer via Twilio.

## Vérifier la configuration

Après le démarrage de la Gateway :

1. Confirmez que le journal de la Gateway affiche la route du webhook SMS.
2. Exécutez une sonde côté Twilio :

```bash
openclaw channels capabilities --channel sms
openclaw channels status --channel sms --probe --json
```

3. Envoyez un SMS au numéro Twilio depuis votre téléphone.
4. Exécutez `openclaw pairing list sms`.
5. Approuvez le code d'appairage avec `openclaw pairing approve sms <CODE>`.
6. Envoyez un autre SMS et confirmez que l'agent répond.

Pour les tests sortants uniquement, utilisez :

```bash
openclaw message send --channel sms --target sms:+15557654321 --message "OpenClaw SMS test"
```

### Test de bout en bout depuis macOS iMessage/SMS

Sur un Mac qui peut envoyer des SMS opérateur via Messages, vous pouvez utiliser `imsg` pour piloter le côté expéditeur sans toucher votre téléphone :

```bash
imsg send --to "+15551234567" --service sms --text "OpenClaw SMS E2E $(date -u +%Y%m%dT%H%M%SZ)" --json
openclaw pairing list sms
openclaw pairing approve sms <CODE>
imsg send --to "+15551234567" --service sms --text "reply exactly SMS pong" --json
```

Le premier message doit créer une demande d'appairage. Le deuxième message doit recevoir la réponse de l'agent via Twilio.

## Sécurité des webhooks

Par défaut, OpenClaw valide `X-Twilio-Signature` en utilisant `publicWebhookUrl` et `authToken`. Gardez `publicWebhookUrl` aligné octet par octet avec l'URL configurée dans Twilio, y compris le schéma, l'hôte, le chemin et la chaîne de requête.

Pour les tests de tunnel locaux uniquement, vous pouvez définir :

```json5
{
  channels: {
    sms: {
      dangerouslyDisableSignatureValidation: true,
    },
  },
}
```

N'utilisez pas la validation de signature désactivée sur une Gateway publique.

## Configuration multi-compte

Utilisez `accounts` quand vous exploitez plus d'un numéro Twilio :

```json5
{
  channels: {
    sms: {
      accounts: {
        support: {
          enabled: true,
          accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          authToken: "twilio-auth-token",
          fromNumber: "+15551234567",
          publicWebhookUrl: "https://gateway.example.com/webhooks/sms/support",
          webhookPath: "/webhooks/sms/support",
          dmPolicy: "allowlist",
          allowFrom: ["+15557654321"],
        },
      },
    },
  },
}
```

Chaque compte doit utiliser un `webhookPath` distinct.

## Dépannage

### Twilio retourne 403 ou OpenClaw rejette le webhook

Vérifiez que `publicWebhookUrl` correspond exactement à l'URL configurée dans Twilio, y compris le schéma, l'hôte, le chemin et la chaîne de requête. Twilio signe la chaîne d'URL publique, donc les réécritures de proxy et les noms d'hôte alternatifs peuvent casser la validation de signature.

### Aucune demande d'appairage n'apparaît

Vérifiez l'URL du webhook **Messaging** du numéro Twilio et la méthode. Elle doit pointer vers l'URL du webhook SMS et utiliser `POST`. Confirmez également que la passerelle est accessible depuis l'Internet public ou via votre tunnel.

Si le journal des messages Twilio affiche l'erreur `11200`, Twilio a accepté le SMS entrant mais n'a pas pu atteindre votre webhook. Vérifiez :

- **Messaging > A message comes in** de Twilio pointe vers `publicWebhookUrl`.
- La méthode est `POST`.
- Le tunnel ou le proxy inverse expose exactement `webhookPath` ; pour Tailscale Funnel, exécutez `tailscale funnel status` et confirmez que `/webhooks/sms` est listé.
- `publicWebhookUrl` utilise le même schéma, hôte, chemin et chaîne de requête que Twilio envoie, afin que la validation de signature puisse reproduire l'URL signée.

### Les envois sortants échouent

Confirmez que `accountSid`, `authToken` et soit `fromNumber` soit `messagingServiceSid` sont résolus. Si vous utilisez un compte Twilio d'essai, le numéro de destination devra peut-être être vérifié dans Twilio avant que les SMS sortants ne soient envoyés.

### Les messages arrivent mais l'agent ne répond pas

Vérifiez `dmPolicy` et `allowFrom`. Avec la politique `pairing` par défaut, l'expéditeur doit être approuvé avant que les tours d'agent normaux ne soient traités.
