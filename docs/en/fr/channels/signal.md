---
summary: "Support Signal via signal-cli (JSON-RPC + SSE), chemins de configuration et modèle de numéro"
read_when:
  - Configuration du support Signal
  - Débogage de l'envoi/réception Signal
title: "Signal"
---

# Signal (signal-cli)

Statut : intégration CLI externe. La passerelle communique avec `signal-cli` via HTTP JSON-RPC + SSE.

## Prérequis

- OpenClaw installé sur votre serveur (flux Linux testé sur Ubuntu 24).
- `signal-cli` disponible sur l'hôte où s'exécute la passerelle.
- Un numéro de téléphone pouvant recevoir un SMS de vérification (pour le chemin d'enregistrement par SMS).
- Accès navigateur pour le captcha Signal (`signalcaptchas.org`) lors de l'enregistrement.

## Configuration rapide (débutant)

1. Utilisez un **numéro Signal distinct** pour le bot (recommandé).
2. Installez `signal-cli` (Java requis si vous utilisez la version JVM).
3. Choisissez un chemin de configuration :
   - **Chemin A (lien QR) :** `signal-cli link -n "OpenClaw"` et scannez avec Signal.
   - **Chemin B (enregistrement SMS) :** enregistrez un numéro dédié avec captcha + vérification SMS.
4. Configurez OpenClaw et redémarrez la passerelle.
5. Envoyez un premier DM et approuvez l'appairage (`openclaw pairing approve signal <CODE>`).

Configuration minimale :

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

Référence des champs :

| Champ       | Description                                       |
| ----------- | ------------------------------------------------- |
| `account`   | Numéro de téléphone du bot au format E.164 (`+15551234567`) |
| `cliPath`   | Chemin vers `signal-cli` (`signal-cli` si sur `PATH`)  |
| `dmPolicy`  | Politique d'accès DM (`pairing` recommandé)          |
| `allowFrom` | Numéros de téléphone ou valeurs `uuid:<id>` autorisés à envoyer des DM |

## Qu'est-ce que c'est

- Canal Signal via `signal-cli` (pas de libsignal intégré).
- Routage déterministe : les réponses reviennent toujours à Signal.
- Les DM partagent la session principale de l'agent ; les groupes sont isolés (`agent:<agentId>:signal:group:<groupId>`).

## Écritures de configuration

Par défaut, Signal est autorisé à écrire les mises à jour de configuration déclenchées par `/config set|unset` (nécessite `commands.config: true`).

Désactivez avec :

```json5
{
  channels: { signal: { configWrites: false } },
}
```

## Le modèle de numéro (important)

- La passerelle se connecte à un **appareil Signal** (le compte `signal-cli`).
- Si vous exécutez le bot sur **votre compte Signal personnel**, il ignorera vos propres messages (protection contre les boucles).
- Pour « je texte le bot et il répond », utilisez un **numéro de bot distinct**.

## Chemin de configuration A : lier un compte Signal existant (QR)

1. Installez `signal-cli` (version JVM ou native).
2. Liez un compte bot :
   - `signal-cli link -n "OpenClaw"` puis scannez le QR dans Signal.
3. Configurez Signal et démarrez la passerelle.

Exemple :

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

Support multi-compte : utilisez `channels.signal.accounts` avec configuration par compte et `name` optionnel. Voir [`gateway/configuration`](/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts) pour le modèle partagé.

## Chemin de configuration B : enregistrer un numéro de bot dédié (SMS, Linux)

Utilisez ceci quand vous voulez un numéro de bot dédié au lieu de lier un compte Signal app existant.

1. Obtenez un numéro pouvant recevoir des SMS (ou vérification vocale pour les lignes fixes).
   - Utilisez un numéro de bot dédié pour éviter les conflits de compte/session.
2. Installez `signal-cli` sur l'hôte de la passerelle :

```bash
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/AsamK/signal-cli/releases/latest | sed -e 's/^.*\/v//')
curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}-Linux-native.tar.gz"
sudo tar xf "signal-cli-${VERSION}-Linux-native.tar.gz" -C /opt
sudo ln -sf /opt/signal-cli /usr/local/bin/
signal-cli --version
```

Si vous utilisez la version JVM (`signal-cli-${VERSION}.tar.gz`), installez d'abord JRE 25+.
Maintenez `signal-cli` à jour ; les versions anciennes peuvent se casser à mesure que les API du serveur Signal changent.

3. Enregistrez et vérifiez le numéro :

```bash
signal-cli -a +<BOT_PHONE_NUMBER> register
```

Si un captcha est requis :

1. Ouvrez `https://signalcaptchas.org/registration/generate.html`.
2. Complétez le captcha, copiez la cible du lien `signalcaptcha://...` depuis « Open Signal ».
3. Exécutez depuis la même adresse IP externe que la session du navigateur si possible.
4. Exécutez l'enregistrement à nouveau immédiatement (les jetons captcha expirent rapidement) :

```bash
signal-cli -a +<BOT_PHONE_NUMBER> register --captcha '<SIGNALCAPTCHA_URL>'
signal-cli -a +<BOT_PHONE_NUMBER> verify <VERIFICATION_CODE>
```

4. Configurez OpenClaw, redémarrez la passerelle, vérifiez le canal :

```bash
# Si vous exécutez la passerelle en tant que service systemd utilisateur :
systemctl --user restart openclaw-gateway

# Puis vérifiez :
openclaw doctor
openclaw channels status --probe
```

5. Appairez votre expéditeur DM :
   - Envoyez n'importe quel message au numéro du bot.
   - Approuvez le code sur le serveur : `openclaw pairing approve signal <PAIRING_CODE>`.
   - Enregistrez le numéro du bot en tant que contact sur votre téléphone pour éviter « Contact inconnu ».

Important : enregistrer un compte de numéro de téléphone avec `signal-cli` peut désauthentifier la session Signal app principale pour ce numéro. Préférez un numéro de bot dédié, ou utilisez le mode lien QR si vous devez conserver votre configuration d'app téléphone existante.

Références en amont :

- `signal-cli` README : `https://github.com/AsamK/signal-cli`
- Flux captcha : `https://github.com/AsamK/signal-cli/wiki/Registration-with-captcha`
- Flux de liaison : `https://github.com/AsamK/signal-cli/wiki/Linking-other-devices-(Provisioning)`

## Mode daemon externe (httpUrl)

Si vous voulez gérer `signal-cli` vous-même (démarrages JVM lents à froid, initialisation de conteneur, ou CPUs partagés), exécutez le daemon séparément et pointez OpenClaw vers lui :

```json5
{
  channels: {
    signal: {
      httpUrl: "http://127.0.0.1:8080",
      autoStart: false,
    },
  },
}
```

Cela ignore l'auto-spawn et l'attente de démarrage dans OpenClaw. Pour les démarrages lents lors de l'auto-spawn, définissez `channels.signal.startupTimeoutMs`.

## Contrôle d'accès (DMs + groupes)

DMs :

- Par défaut : `channels.signal.dmPolicy = "pairing"`.
- Les expéditeurs inconnus reçoivent un code d'appairage ; les messages sont ignorés jusqu'à approbation (les codes expirent après 1 heure).
- Approuvez via :
  - `openclaw pairing list signal`
  - `openclaw pairing approve signal <CODE>`
- L'appairage est l'échange de jetons par défaut pour les DM Signal. Détails : [Pairing](/channels/pairing)
- Les expéditeurs UUID uniquement (de `sourceUuid`) sont stockés comme `uuid:<id>` dans `channels.signal.allowFrom`.

Groupes :

- `channels.signal.groupPolicy = open | allowlist | disabled`.
- `channels.signal.groupAllowFrom` contrôle qui peut déclencher dans les groupes quand `allowlist` est défini.
- `channels.signal.groups["<group-id>" | "*"]` peut remplacer le comportement du groupe avec `requireMention`, `tools`, et `toolsBySender`.
- Utilisez `channels.signal.accounts.<id>.groups` pour les remplacements par compte dans les configurations multi-compte.
- Note d'exécution : si `channels.signal` est complètement absent, l'exécution revient à `groupPolicy="allowlist"` pour les vérifications de groupe (même si `channels.defaults.groupPolicy` est défini).

## Comment ça marche (comportement)

- `signal-cli` s'exécute en tant que daemon ; la passerelle lit les événements via SSE.
- Les messages entrants sont normalisés dans l'enveloppe de canal partagée.
- Les réponses reviennent toujours au même numéro ou groupe.

## Médias + limites

- Le texte sortant est divisé en chunks selon `channels.signal.textChunkLimit` (par défaut 4000).
- Chunking optionnel par nouvelle ligne : définissez `channels.signal.chunkMode="newline"` pour diviser sur les lignes vides (limites de paragraphes) avant le chunking par longueur.
- Pièces jointes supportées (base64 récupérées de `signal-cli`).
- Limite média par défaut : `channels.signal.mediaMaxMb` (par défaut 8).
- Utilisez `channels.signal.ignoreAttachments` pour ignorer le téléchargement de médias.
- Le contexte d'historique de groupe utilise `channels.signal.historyLimit` (ou `channels.signal.accounts.*.historyLimit`), revenant à `messages.groupChat.historyLimit`. Définissez `0` pour désactiver (par défaut 50).

## Indicateurs de saisie + accusés de réception

- **Indicateurs de saisie** : OpenClaw envoie des signaux de saisie via `signal-cli sendTyping` et les actualise pendant qu'une réponse s'exécute.
- **Accusés de réception** : quand `channels.signal.sendReadReceipts` est true, OpenClaw transfère les accusés de réception pour les DM autorisés.
- Signal-cli n'expose pas les accusés de réception pour les groupes.

## Réactions (outil de message)

- Utilisez `message action=react` avec `channel=signal`.
- Cibles : E.164 de l'expéditeur ou UUID (utilisez `uuid:<id>` de la sortie d'appairage ; l'UUID nu fonctionne aussi).
- `messageId` est l'horodatage Signal du message auquel vous réagissez.
- Les réactions de groupe nécessitent `targetAuthor` ou `targetAuthorUuid`.

Exemples :

```
message action=react channel=signal target=uuid:123e4567-e89b-12d3-a456-426614174000 messageId=1737630212345 emoji=🔥
message action=react channel=signal target=+15551234567 messageId=1737630212345 emoji=🔥 remove=true
message action=react channel=signal target=signal:group:<groupId> targetAuthor=uuid:<sender-uuid> messageId=1737630212345 emoji=✅
```

Configuration :

- `channels.signal.actions.reactions` : activer/désactiver les actions de réaction (par défaut true).
- `channels.signal.reactionLevel` : `off | ack | minimal | extensive`.
  - `off`/`ack` désactive les réactions de l'agent (l'outil de message `react` génèrera une erreur).
  - `minimal`/`extensive` active les réactions de l'agent et définit le niveau de guidance.
- Remplacements par compte : `channels.signal.accounts.<id>.actions.reactions`, `channels.signal.accounts.<id>.reactionLevel`.

## Cibles de livraison (CLI/cron)

- DMs : `signal:+15551234567` (ou E.164 simple).
- DMs UUID : `uuid:<id>` (ou UUID nu).
- Groupes : `signal:group:<groupId>`.
- Noms d'utilisateur : `username:<name>` (si supporté par votre compte Signal).

## Dépannage

Exécutez d'abord cette échelle :

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Puis confirmez l'état d'appairage DM si nécessaire :

```bash
openclaw pairing list signal
```

Défaillances courantes :

- Daemon accessible mais pas de réponses : vérifiez les paramètres de compte/daemon (`httpUrl`, `account`) et le mode de réception.
- DMs ignorés : l'expéditeur est en attente d'approbation d'appairage.
- Messages de groupe ignorés : le gating d'expéditeur/mention de groupe bloque la livraison.
- Erreurs de validation de configuration après éditions : exécutez `openclaw doctor --fix`.
- Signal manquant des diagnostics : confirmez `channels.signal.enabled: true`.

Vérifications supplémentaires :

```bash
openclaw pairing list signal
pgrep -af signal-cli
grep -i "signal" "/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log" | tail -20
```

Pour le flux de triage : [/channels/troubleshooting](/channels/troubleshooting).

## Notes de sécurité

- `signal-cli` stocke les clés de compte localement (généralement `~/.local/share/signal-cli/data/`).
- Sauvegardez l'état du compte Signal avant la migration du serveur ou la reconstruction.
