---
summary: "Exécutez OpenClaw dans un bac à sable cloud Daytona avec accès SSH et URLs d'aperçu signées"
read_when:
  - Running OpenClaw in a Daytona sandbox
  - You want a cloud sandbox for OpenClaw without managing a VPS
title: "Daytona"
---

Exécutez une passerelle OpenClaw persistante dans un bac à sable cloud [Daytona](https://www.daytona.io) : un environnement Linux isolé avec accès SSH et URLs d'aperçu intégrées, sans gestion de VPS requise. OpenClaw est préinstallé dans le snapshot `daytona-medium`, donc la configuration commence immédiatement après SSH.

Gardez la passerelle sur loopback et accédez au tableau de bord via les URLs d'aperçu signées de Daytona. N'exposez pas le port de la passerelle directement à l'internet public.

## Ce dont vous avez besoin

- [Compte Daytona](https://app.daytona.io) (niveau gratuit disponible)
- Clé API Daytona depuis le [tableau de bord Daytona](https://app.daytona.io/dashboard/keys)
- Clé API pour votre fournisseur de modèle (Anthropic, OpenAI, etc.)

## Installez la CLI Daytona

<Tabs>
  <Tab title="macOS / Linux">
    ```bash
    brew install daytonaio/cli/daytona
    ```
  </Tab>
  <Tab title="Windows">
    ```powershell
    powershell -Command "irm https://get.daytona.io/windows | iex"
    ```
  </Tab>
</Tabs>

Vérifiez l'installation :

```bash
daytona --version
```

Les versions plus anciennes de la CLI manquent les commandes de bac à sable plus récentes ; maintenez-la à jour (par exemple `brew upgrade daytonaio/cli/daytona`).

## Authentifiez-vous

```bash
daytona login --api-key=YOUR_API_KEY
```

## Créez un bac à sable

```bash
daytona sandbox create --name openclaw --snapshot daytona-medium --auto-stop 0
```

| Drapeau                     | Raison                                                           |
| --------------------------- | ---------------------------------------------------------------- |
| `--snapshot daytona-medium` | Fournit suffisamment d'espace mémoire pour exécuter la passerelle |
| `--auto-stop 0`             | Garde le bac à sable en cours d'exécution jusqu'à l'arrêt manuel   |

## Connectez-vous via SSH

```bash
daytona ssh openclaw
```

## Exécutez l'intégration

À l'intérieur du bac à sable, configurez OpenClaw en une seule commande :

```bash
openclaw onboard --non-interactive --accept-risk \
  --anthropic-api-key YOUR_ANTHROPIC_KEY \
  --skip-daemon --skip-channels --skip-skills --skip-hooks --skip-health
```

`--skip-daemon` est important : les bacs à sable Daytona n'exécutent pas de gestionnaire de service, vous démarrez donc la passerelle manuellement ci-dessous. Échangez le drapeau de clé pour votre fournisseur (`--openai-api-key`, `--openrouter-api-key`, etc.) ; `openclaw onboard --help` les liste tous. Les canaux, les compétences et les hooks sont ignorés ici et configurés ultérieurement.

L'exécution de `openclaw onboard` sans drapeaux démarre un assistant de configuration conversationnel à la place et nécessite un terminal interactif ; `openclaw onboard --classic` exécute l'ancien assistant étape par étape.

L'intégration configure un jeton d'authentification de passerelle. Imprimez-le à tout moment depuis le bac à sable :

```bash
node -p "require(process.env.HOME + '/.openclaw/openclaw.json').gateway.auth.token"
```

`openclaw config get gateway.auth.token` retourne `__OPENCLAW_REDACTED__` plutôt que la valeur, car la CLI masque les secrets dans sa sortie.

## Autorisez l'origine de l'URL d'aperçu

La passerelle n'accepte les connexions du navigateur que depuis les origines autorisées, et le proxy d'aperçu de Daytona se trouve devant. Configurez les deux avant de démarrer la passerelle.

Depuis votre **terminal local** (pas la session SSH du bac à sable), générez une URL d'aperçu signée pour le port de la passerelle :

```bash
daytona preview-url openclaw --port 18789
```

Copiez l'URL qu'il affiche. De retour dans la session SSH du bac à sable, autorisez cette origine et faites confiance au proxy d'aperçu dans le bac à sable, en remplaçant l'URL d'exemple par la vôtre :

```bash
openclaw config set gateway.controlUi.allowedOrigins '["PASTE_YOUR_PREVIEW_URL"]'
openclaw config set gateway.trustedProxies '["127.0.0.1"]'
```

Collez l'URL exactement comme imprimée : schéma et hôte uniquement, sans barre oblique finale et sans chemin. La passerelle compare l'origine du navigateur littéralement, et les navigateurs envoient `https://host` sans barre oblique finale, donc `https://host/` échoue à correspondre et la connexion est rejetée. Les barres d'adresse du navigateur affichent souvent cette barre oblique finale, donc copiez depuis le terminal à la place.

## Démarrez la passerelle

```bash
nohup openclaw gateway run > /tmp/gateway.log 2>&1 &
```

La passerelle s'exécute en arrière-plan et survit aux déconnexions SSH. Vérifiez qu'elle est active :

```bash
openclaw gateway health
```

La commande rapporte l'état de la passerelle, donc `OK` signifie que vous êtes bon pour continuer.

Pour redémarrer la passerelle ultérieurement (après des modifications de configuration ou des mises à jour) :

```bash
pkill -f "openclaw gateway" || true
nohup openclaw gateway run > /tmp/gateway.log 2>&1 &
```

## Ouvrez le tableau de bord

Ouvrez l'URL d'aperçu que vous avez générée précédemment dans votre navigateur. L'interface de contrôle demande le jeton de passerelle à la première connexion ; collez la valeur que vous avez imprimée après l'intégration.

### Approuvez votre appareil

La première connexion du navigateur met en file d'attente une demande d'appairage d'appareil. De retour dans votre session SSH du bac à sable :

```bash
# Listez les demandes en attente et copiez l'ID de demande
openclaw devices list

# Approuvez-la
openclaw devices approve REQUEST_ID
```

## Sécurité

L'accès à la passerelle est protégé en trois couches :

| Couche          | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| URL d'aperçu    | URL signée limitée dans le temps (expire après 1 heure)      |
| Jeton de passerelle | Requis pour se connecter via l'interface de contrôle         |
| Approbation d'appareil | Chaque nouveau navigateur ou client doit être explicitement approuvé |

Gardez votre jeton de passerelle et vos URLs d'aperçu privés. La passerelle reste liée à loopback ; le proxy d'aperçu de Daytona gère l'accès externe.

## Configuration des canaux

Les expéditeurs inconnus nécessitent une approbation d'appairage par défaut ; voir [Appairage](/fr/channels/pairing).

### Telegram

Créez un bot avec [@BotFather](https://t.me/botfather) (`/newbot`), copiez le jeton, puis configurez OpenClaw depuis la session SSH du bac à sable :

```bash
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken YOUR_BOT_TOKEN
```

Redémarrez la passerelle (voir ci-dessus), envoyez un DM à votre bot, puis approuvez le code d'appairage qu'il rapporte :

```bash
openclaw pairing list telegram
openclaw pairing approve telegram PAIRING_CODE
```

Les codes d'appairage expirent après 1 heure. Référence complète : [Telegram](/fr/channels/telegram).

### WhatsApp

WhatsApp est fourni en tant que plugin séparé, donc installez et activez-le d'abord :

```bash
openclaw plugins install clawhub:@openclaw/whatsapp --acknowledge-clawhub-risk
openclaw plugins enable whatsapp
```

L'installation n'active pas un plugin, donc l'étape `enable` est requise ; sinon la passerelle rapporte le canal comme configuré mais non approuvé. L'exécution de la commande de connexion ci-dessous sans installation d'abord vous invite à télécharger le plugin depuis ClawHub ou npm à la place.

Ensuite, liez le compte en scannant un code QR depuis la session SSH du bac à sable :

```bash
openclaw channels login --channel whatsapp
```

Sur votre téléphone : **Paramètres → Appareils liés → Lier un appareil**, puis scannez le code QR affiché dans le terminal. Redémarrez la passerelle après la liaison, puis envoyez-vous un message sur WhatsApp et OpenClaw répond dans ce chat.

Aucune approbation d'appairage n'est nécessaire : sans liste d'autorisation configurée, le numéro du compte lié est autorisé par défaut. L'appairage s'applique aux expéditeurs inconnus, c'est pourquoi Telegram en a besoin et l'auto-chat non. Listes d'autorisation, mode numéro personnel et détails d'auto-chat : [WhatsApp](/fr/channels/whatsapp).

## Mise à jour

L'arborescence npm globale du snapshot est détenue par root, donc `openclaw update` simple ne peut pas y écrire. Mettez à jour depuis la session SSH du bac à sable avec :

```bash
sudo env "PATH=$PATH" npm install --global openclaw@latest
openclaw doctor
```

`openclaw doctor` migre toute configuration plus ancienne après la mise à jour. Redémarrez la passerelle après (voir ci-dessus).

## Arrêtez et reprenez le bac à sable

```bash
# Arrêtez
daytona sandbox stop openclaw

# Reprenez
daytona sandbox start openclaw
```

L'état du bac à sable persiste entre les cycles d'arrêt/démarrage, mais le processus de passerelle ne démarre pas automatiquement. Après une reprise, reconnectez-vous et redémarrez-le :

```bash
daytona ssh openclaw
nohup openclaw gateway run > /tmp/gateway.log 2>&1 &
```

## Dépannage

### La passerelle ne s'exécute pas après le redémarrage du bac à sable

Le processus de passerelle ne survit pas à un redémarrage du bac à sable. Reconnectez-vous avec `daytona ssh openclaw` et redémarrez-le avec la commande nohup ci-dessus.

### URL d'aperçu expirée

Les URLs d'aperçu sont limitées dans le temps (3600 secondes par défaut). Régénérez depuis votre terminal local, éventuellement avec une expiration plus longue :

```bash
daytona preview-url openclaw --port 18789 --expires 86400
```

Chaque URL générée a un hôte différent, c'est donc une nouvelle origine. Après régénération, mettez à jour `gateway.controlUi.allowedOrigins` avec la nouvelle URL et redémarrez la passerelle, sinon l'interface de contrôle est rejetée avec `origin not allowed`.

### Bac à sable arrêté automatiquement

Si le bac à sable a été créé sans `--auto-stop 0`, il s'arrête automatiquement en cas d'inactivité. Reprenez-le avec `daytona sandbox start openclaw`.

### Port de passerelle non accessible

Confirmez que la passerelle s'exécute et écoute :

```bash
openclaw gateway health
tail -20 /tmp/gateway.log
```

Si vous avez modifié le port de la passerelle, passez le même port à `daytona preview-url`.

## Notes

- Pour l'approvisionnement programmatique du bac à sable, voir le [guide du SDK OpenClaw Daytona](https://www.daytona.io/docs/en/guides/openclaw/openclaw-sdk-sandbox/)

## Connexes

- [Accès distant à la passerelle](/fr/gateway/remote)
- [Sécurité de la passerelle](/fr/gateway/security)
- [Mise à jour d'OpenClaw](/fr/install/updating)
