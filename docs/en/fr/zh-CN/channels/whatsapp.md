---
read_when:
  - Lors du traitement du comportement des canaux WhatsApp/Web ou du routage des boîtes de réception
summary: Intégration WhatsApp (canal Web) : connexion, boîte de réception, réponses, médias et opérations
title: WhatsApp
x-i18n:
  generated_at: "2026-02-03T07:46:24Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 44fd88f8e269284999e5a5a52b230edae6e6f978528dd298d6a5603d03c0c38d
  source_path: channels/whatsapp.md
  workflow: 15
---

# WhatsApp (canal Web)

Statut : Support uniquement de WhatsApp Web via Baileys. La passerelle possède la session.

## Configuration rapide (débutants)

1. Si possible, utilisez un **numéro de téléphone distinct** (recommandé).
2. Configurez WhatsApp dans `~/.openclaw/openclaw.json`.
3. Exécutez `openclaw channels login` pour scanner le code QR (appairage d'appareil).
4. Démarrez la passerelle.

Configuration minimale :

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}
```

## Objectifs

- Supporter plusieurs comptes WhatsApp dans un seul processus de passerelle (multi-comptes).
- Routage déterministe : les réponses reviennent à WhatsApp, sans routage par modèle.
- Le modèle voit suffisamment de contexte pour comprendre les réponses citées.

## Écritures de configuration

Par défaut, WhatsApp autorise les mises à jour de configuration déclenchées par `/config set|unset` (nécessite `commands.config: true`).

Pour désactiver :

```json5
{
  channels: { whatsapp: { configWrites: false } },
}
```

## Architecture (qui possède quoi)

- **La passerelle** possède le socket Baileys et la boucle de boîte de réception.
- **CLI / application macOS** communique avec la passerelle ; n'utilise pas directement Baileys.
- L'envoi de messages sortants nécessite un **écouteur actif** ; sinon l'envoi échoue rapidement.

## Obtenir un numéro de téléphone (deux modes)

WhatsApp nécessite un vrai numéro de téléphone pour la vérification. Les numéros VoIP et virtuels sont généralement bloqués. Il y a deux façons supportées d'exécuter OpenClaw sur WhatsApp :

### Numéro dédié (recommandé)

Utilisez un **numéro de téléphone distinct** pour OpenClaw. Meilleure expérience utilisateur, routage clair, pas de problèmes d'auto-chat. Configuration idéale : **téléphone Android ancien/de secours + eSIM**. Gardez le Wi-Fi et l'alimentation connectés, appairez via code QR.

**WhatsApp Business :** Vous pouvez utiliser WhatsApp Business avec un numéro différent sur le même appareil. Parfait pour séparer WhatsApp personnel — installez WhatsApp Business et enregistrez le numéro OpenClaw là-bas.

**Exemple de configuration (numéro dédié, liste d'autorisation mono-utilisateur) :**

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}
```

**Mode d'appairage (optionnel) :**
Si vous souhaitez utiliser l'appairage au lieu d'une liste d'autorisation, définissez `channels.whatsapp.dmPolicy` sur `pairing`. Les expéditeurs inconnus recevront un code d'appairage ; approuvez avec :
`openclaw pairing approve whatsapp <code>`

### Numéro personnel (alternative)

Alternative rapide : exécutez OpenClaw sur **votre propre numéro**. Envoyez-vous des messages (WhatsApp "Envoyer un message à soi-même") pour tester, sans déranger les contacts. Nécessite de lire les codes de vérification sur le téléphone principal pendant la configuration et l'expérimentation. **Vous devez activer le mode auto-chat.**
Lorsque l'assistant vous demande votre numéro WhatsApp personnel, entrez le téléphone que vous utiliserez pour envoyer des messages (propriétaire/expéditeur), pas le numéro de l'assistant.

**Exemple de configuration (numéro personnel, auto-chat) :**

```json
{
  "whatsapp": {
    "selfChatMode": true,
    "dmPolicy": "allowlist",
    "allowFrom": ["+15551234567"]
  }
}
```

Lorsque `identity.name` est défini, les réponses d'auto-chat sont par défaut `[{identity.name}]` (sinon `[openclaw]`),
à condition que `messages.responsePrefix` ne soit pas défini. Le définir explicitement permet de personnaliser ou désactiver
le préfixe (utilisez `""` pour le supprimer).

### Conseils pour obtenir un numéro

- **eSIM local** auprès d'un opérateur mobile de votre pays (plus fiable)
  - Autriche : [hot.at](https://www.hot.at)
  - Royaume-Uni : [giffgaff](https://www.giffgaff.com) — Carte SIM gratuite, sans contrat
- **Carte SIM prépayée** — Bon marché, il suffit de recevoir un SMS de vérification

**À éviter :** TextNow, Google Voice, la plupart des services "SMS gratuits" — WhatsApp les bloque activement.

**Conseil :** Ce numéro ne doit recevoir qu'un seul SMS de vérification. Après cela, la session WhatsApp Web persiste via `creds.json`.

## Pourquoi pas Twilio ?

- Les versions antérieures d'OpenClaw supportaient l'intégration WhatsApp Business de Twilio.
- Les numéros WhatsApp Business ne conviennent pas aux assistants personnels.
- Meta applique une fenêtre de réponse de 24 heures ; les numéros commerciaux ne peuvent pas initier de nouveaux messages si vous n'avez pas répondu au cours des 24 dernières heures.
- L'utilisation fréquente ou "intensive" déclenche des blocages agressifs, car les comptes commerciaux ne sont pas conçus pour envoyer de nombreux messages d'assistant personnel.
- Résultat : livraison peu fiable et blocages fréquents, donc ce support a été supprimé.

## Connexion + Identifiants

- Commande de connexion : `openclaw channels login` (scanner le code QR via appairage d'appareil).
- Connexion multi-comptes : `openclaw channels login --account <id>` (`<id>` = `accountId`).
- Compte par défaut (lorsque `--account` est omis) : `default` s'il existe, sinon le premier `accountId` configuré (trié).
- Les identifiants sont stockés dans `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`.
- Copie de sauvegarde dans `creds.json.bak` (restauration en cas de corruption).
- Compatibilité héritée : les installations plus anciennes stockent les fichiers Baileys directement dans `~/.openclaw/credentials/`.
- Déconnexion : `openclaw channels logout` (ou `--account <id>`) supprime l'état d'authentification WhatsApp (mais conserve `oauth.json` partagé).
- Socket déconnecté => message d'erreur pour réappairer.

## Flux entrant (messages directs + groupes)

- Les événements WhatsApp proviennent de `messages.upsert` (Baileys).
- Les écouteurs de boîte de réception se détachent à la fermeture pour éviter d'accumuler les gestionnaires d'événements lors des tests/redémarrages.
- Les chats de statut/diffusion sont ignorés.
- Les chats directs utilisent E.164 ; les groupes utilisent le JID du groupe.
- **Politique de messages directs** : `channels.whatsapp.dmPolicy` contrôle l'accès aux chats directs (par défaut : `pairing`).
  - Appairage : les expéditeurs inconnus reçoivent un code d'appairage (approuvé via `openclaw pairing approve whatsapp <code>` ; le code expire après 1 heure).
  - Ouvert : nécessite que `channels.whatsapp.allowFrom` contienne `"*"`.
  - Le numéro WhatsApp que vous avez appairé est implicitement approuvé, donc les messages de vous-même contournent les vérifications `channels.whatsapp.dmPolicy` et `channels.whatsapp.allowFrom`.

### Mode numéro personnel (alternative)

Si vous exécutez OpenClaw sur **votre numéro WhatsApp personnel**, activez `channels.whatsapp.selfChatMode` (voir l'exemple ci-dessus).

Comportement :

- Les messages directs sortants ne déclenchent jamais de réponse d'appairage (pour ne pas déranger les contacts).
- Les expéditeurs inconnus entrants respectent toujours `channels.whatsapp.dmPolicy`.
- Le mode auto-chat (allowFrom contient votre numéro) évite les accusés de lecture automatiques et ignore les JID mentionnés.
- Les messages directs non-auto-chat envoient des accusés de lecture.

## Accusés de lecture

Par défaut, la passerelle marque les messages WhatsApp entrants comme lus (coches bleues) après les avoir acceptés.

Désactiver globalement :

```json5
{
  channels: { whatsapp: { sendReadReceipts: false } },
}
```

Désactiver par compte :

```json5
{
  channels: {
    whatsapp: {
      accounts: {
        personal: { sendReadReceipts: false },
      },
    },
  },
}
```

Remarques :

- Le mode auto-chat ignore toujours les accusés de lecture.

## FAQ WhatsApp : envoi de messages + appairage

**Lorsque j'appaire WhatsApp, OpenClaw envoie-t-il des messages à des contacts aléatoires ?**
Non. La politique de messages directs par défaut est **appairage**, donc les expéditeurs inconnus ne reçoivent qu'un code d'appairage, et leurs messages **ne sont pas traités**. OpenClaw répond uniquement aux chats qu'il reçoit, ou aux envois que vous déclenchez explicitement (agent/CLI).

**Comment fonctionne l'appairage sur WhatsApp ?**
L'appairage est un contrôle d'accès aux messages directs pour les expéditeurs inconnus :

- Le premier message direct d'un nouvel expéditeur retourne un code court (le message n'est pas traité).
- Approuvez avec : `openclaw pairing approve whatsapp <code>` (listez avec `openclaw pairing list whatsapp`).
- Le code expire après 1 heure ; limite de 3 demandes en attente par canal.

**Plusieurs personnes peuvent-elles utiliser différentes instances OpenClaw sur un seul numéro WhatsApp ?**
Oui, via `bindings` pour router chaque expéditeur vers un agent différent (peer `kind: "dm"`, expéditeur E.164 comme `+15551234567`). Les réponses proviennent toujours du **même compte WhatsApp**, les chats directs s'effondrent dans la session principale de chaque agent, donc **utilisez un agent par personne**. Le contrôle d'accès aux messages directs (`dmPolicy`/`allowFrom`) est global par compte WhatsApp. Voir [Routage multi-agent](/concepts/multi-agent).

**Pourquoi l'assistant me demande-t-il mon numéro de téléphone ?**
L'assistant l'utilise pour configurer votre **liste d'autorisation/propriétaire**, afin d'autoriser vos propres messages directs. Il n'est pas utilisé pour l'envoi automatique. Si vous exécutez sur votre numéro WhatsApp personnel, utilisez le même numéro et activez `channels.whatsapp.selfChatMode`.

## Normalisation des messages (ce que voit le modèle)

- `Body` est le corps du message actuel avec enveloppe.
- Le contexte des réponses citées est **toujours ajouté** :
  ```
  [Replying to +1555 id:ABC123]
  <quoted text or <media:...>>
  [/Replying]
  ```
- Les métadonnées de réponse sont également définies :
  - `ReplyToId` = stanzaId
  - `ReplyToBody` = corps cité ou placeholder média
  - `ReplyToSender` = E.164 si connu
- Les messages entrants purement médias utilisent des placeholders :
  - `<media:image|video|audio|document|sticker>`

## Groupes

- Les groupes sont mappés aux sessions `agent:<agentId>:whatsapp:group:<jid>`.
- Politique de groupes : `channels.whatsapp.groupPolicy = open|disabled|allowlist` (par défaut `allowlist`).
- Mode d'activation :
  - `mention` (par défaut) : nécessite une @mention ou une correspondance regex.
  - `always` : déclenche toujours.
- `/activation mention|always` réservé au propriétaire, doit être envoyé comme message indépendant.
- Propriétaire = `channels.whatsapp.allowFrom` (sinon E.164 de vous-même).
- **Injection d'historique** (en attente uniquement) :
  - Les messages non traités les plus récents (50 par défaut) sont insérés dans :
    `[Chat messages since your last reply - for context]` (les messages déjà dans la session ne sont pas réinjectés)
  - Le message actuel dans :
    `[Current message - respond to this]`
  - Suffixe d'expéditeur ajouté : `[from: Name (+E164)]`
- Cache des métadonnées de groupe 5 minutes (sujet + participants).

## Livraison des réponses (threads)

- WhatsApp Web envoie des messages standard (la passerelle actuelle n'a pas de threads de réponse citée).
- Ce canal ignore les étiquettes de réponse.

## Réactions de confirmation (réponse automatique à la réception)

WhatsApp peut envoyer automatiquement une réaction emoji immédiatement à la réception d'un message entrant, avant que le bot ne génère une réponse. Cela fournit un retour instantané à l'utilisateur indiquant que son message a été reçu.

**Configuration :**

```json
{
  "whatsapp": {
    "ackReaction": {
      "emoji": "👀",
      "direct": true,
      "group": "mentions"
    }
  }
}
```

**
