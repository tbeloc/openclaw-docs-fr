---
summary: "Plugin Google Meet : rejoindre des URL Meet explicites via Chrome ou Twilio avec les paramètres par défaut de voix en temps réel"
read_when:
  - You want an OpenClaw agent to join a Google Meet call
  - You are configuring Chrome, Chrome node, or Twilio as a Google Meet transport
title: "Plugin Google Meet"
---

# Google Meet (plugin)

Support des participants Google Meet pour OpenClaw.

Le plugin est explicite par conception :

- Il ne rejoint que des URL `https://meet.google.com/...` explicites.
- La voix `realtime` est le mode par défaut.
- La voix en temps réel peut rappeler l'agent OpenClaw complet quand un raisonnement ou des outils plus approfondis sont nécessaires.
- L'authentification commence par OAuth Google personnel ou un profil Chrome déjà connecté.
- Il n'y a pas d'annonce de consentement automatique.
- Le backend audio Chrome par défaut est `BlackHole 2ch`.
- Chrome peut s'exécuter localement ou sur un hôte de nœud appairé.
- Twilio accepte un numéro d'accès par téléphone plus un PIN ou une séquence DTMF optionnels.
- La commande CLI est `googlemeet` ; `meet` est réservé aux flux de téléconférence d'agent plus larges.

## Démarrage rapide

Installez les dépendances audio locales et assurez-vous que le fournisseur en temps réel peut utiliser OpenAI :

```bash
brew install blackhole-2ch sox
export OPENAI_API_KEY=sk-...
```

`blackhole-2ch` installe le périphérique audio virtuel `BlackHole 2ch`. L'installateur Homebrew nécessite un redémarrage avant que macOS expose le périphérique :

```bash
sudo reboot
```

Après le redémarrage, vérifiez les deux éléments :

```bash
system_profiler SPAudioDataType | grep -i BlackHole
command -v rec play
```

Activez le plugin :

```json5
{
  plugins: {
    entries: {
      "google-meet": {
        enabled: true,
        config: {},
      },
    },
  },
}
```

Vérifiez la configuration :

```bash
openclaw googlemeet setup
```

Rejoignez une réunion :

```bash
openclaw googlemeet join https://meet.google.com/abc-defg-hij
```

Ou laissez un agent rejoindre via l'outil `google_meet` :

```json
{
  "action": "join",
  "url": "https://meet.google.com/abc-defg-hij"
}
```

Chrome se connecte en tant que profil Chrome connecté. Dans Meet, choisissez `BlackHole 2ch` pour le chemin du microphone/haut-parleur utilisé par OpenClaw. Pour un audio duplex propre, utilisez des périphériques virtuels séparés ou un graphique de style Loopback ; un seul périphérique BlackHole suffit pour un premier test de fumée mais peut créer des échos.

### Passerelle locale + Chrome Parallels

Vous n'avez **pas** besoin d'une passerelle OpenClaw complète ou d'une clé API de modèle à l'intérieur d'une VM macOS juste pour que la VM possède Chrome. Exécutez la passerelle et l'agent localement, puis exécutez un hôte de nœud dans la VM. Activez le plugin fourni sur la VM une fois pour que le nœud annonce la commande Chrome :

Ce qui s'exécute où :

- Hôte de passerelle : passerelle OpenClaw, espace de travail d'agent, clés de modèle/API, fournisseur en temps réel et configuration du plugin Google Meet.
- VM macOS Parallels : CLI OpenClaw/hôte de nœud, Google Chrome, SoX, BlackHole 2ch et un profil Chrome connecté à Google.
- Non nécessaire dans la VM : service de passerelle, configuration d'agent, clé OpenAI/GPT ou configuration du fournisseur de modèle.

Installez les dépendances de la VM :

```bash
brew install blackhole-2ch sox
```

Redémarrez la VM après l'installation de BlackHole pour que macOS expose `BlackHole 2ch` :

```bash
sudo reboot
```

Après le redémarrage, vérifiez que la VM peut voir le périphérique audio et les commandes SoX :

```bash
system_profiler SPAudioDataType | grep -i BlackHole
command -v rec play
```

Installez ou mettez à jour OpenClaw dans la VM, puis activez le plugin fourni :

```bash
openclaw plugins enable google-meet
```

Démarrez l'hôte de nœud dans la VM :

```bash
openclaw node run --host <gateway-host> --port 18789 --display-name parallels-macos
```

Si `<gateway-host>` est une IP LAN et que vous n'utilisez pas TLS, le nœud refuse le WebSocket en texte brut à moins que vous n'optiez pour ce réseau privé de confiance :

```bash
OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1 \
  openclaw node run --host <gateway-lan-ip> --port 18789 --display-name parallels-macos
```

Utilisez la même variable d'environnement lors de l'installation du nœud en tant que LaunchAgent :

```bash
OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1 \
  openclaw node install --host <gateway-lan-ip> --port 18789 --display-name parallels-macos --force
openclaw node restart
```

`OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` est un environnement de processus, pas un paramètre `openclaw.json`. `openclaw node install` le stocke dans l'environnement LaunchAgent quand il est présent sur la commande d'installation.

Approuvez le nœud depuis l'hôte de passerelle :

```bash
openclaw devices list
openclaw devices approve <requestId>
```

Confirmez que la passerelle voit le nœud et qu'il annonce `googlemeet.chrome` :

```bash
openclaw nodes status
```

Routez Meet via ce nœud sur l'hôte de passerelle :

```json5
{
  gateway: {
    nodes: {
      allowCommands: ["googlemeet.chrome"],
    },
  },
  plugins: {
    entries: {
      "google-meet": {
        enabled: true,
        config: {
          defaultTransport: "chrome-node",
          chromeNode: {
            node: "parallels-macos",
          },
        },
      },
    },
  },
}
```

Rejoignez maintenant normalement depuis l'hôte de passerelle :

```bash
openclaw googlemeet join https://meet.google.com/abc-defg-hij
```

ou demandez à l'agent d'utiliser l'outil `google_meet` avec `transport: "chrome-node"`.

Si `chromeNode.node` est omis, OpenClaw sélectionne automatiquement uniquement quand exactement un nœud connecté annonce `googlemeet.chrome`. Si plusieurs nœuds capables sont connectés, définissez `chromeNode.node` sur l'ID du nœud, le nom d'affichage ou l'IP distante.

Vérifications d'échec courant :

- `No connected Google Meet-capable node` : démarrez `openclaw node run` dans la VM, approuvez l'appairage et assurez-vous que `openclaw plugins enable google-meet` a été exécuté dans la VM. Confirmez également que l'hôte de passerelle autorise la commande du nœud avec `gateway.nodes.allowCommands: ["googlemeet.chrome"]`.
- `BlackHole 2ch audio device not found on the node` : installez `blackhole-2ch` dans la VM et redémarrez la VM.
- Chrome s'ouvre mais ne peut pas rejoindre : connectez-vous à Chrome dans la VM et confirmez que ce profil peut rejoindre l'URL Meet manuellement.
- Pas d'audio : dans Meet, routez le microphone/haut-parleur via le chemin du périphérique audio virtuel utilisé par OpenClaw ; utilisez des périphériques virtuels séparés ou un routage de style Loopback pour un audio duplex propre.

## Notes d'installation

La valeur par défaut en temps réel de Chrome utilise deux outils externes :

- `sox` : utilitaire audio en ligne de commande. Le plugin utilise ses commandes `rec` et `play` pour le pont audio mu-law G.711 8 kHz par défaut.
- `blackhole-2ch` : pilote audio virtuel macOS. Il crée le périphérique audio `BlackHole 2ch` que Chrome/Meet peut router.

OpenClaw ne regroupe ni ne redistribue aucun des deux packages. La documentation demande aux utilisateurs de les installer en tant que dépendances d'hôte via Homebrew. SoX est sous licence `LGPL-2.0-only AND GPL-2.0-only` ; BlackHole est GPL-3.0. Si vous créez un installateur ou une appliance qui regroupe BlackHole avec OpenClaw, examinez les conditions de licence en amont de BlackHole ou obtenez une licence séparée auprès d'Existential Audio.

## Transports

### Chrome

Le transport Chrome ouvre l'URL Meet dans Google Chrome et se connecte en tant que profil Chrome connecté. Sur macOS, le plugin vérifie `BlackHole 2ch` avant le lancement. S'il est configuré, il exécute également une commande de vérification de santé du pont audio et une commande de démarrage avant d'ouvrir Chrome. Utilisez `chrome` quand Chrome/audio vivent sur l'hôte de passerelle ; utilisez `chrome-node` quand Chrome/audio vivent sur un nœud appairé tel qu'une VM macOS Parallels.

```bash
openclaw googlemeet join https://meet.google.com/abc-defg-hij --transport chrome
openclaw googlemeet join https://meet.google.com/abc-defg-hij --transport chrome-node
```

Routez l'audio du microphone et du haut-parleur Chrome via le pont audio OpenClaw local. Si `BlackHole 2ch` n'est pas installé, la connexion échoue avec une erreur de configuration au lieu de se connecter silencieusement sans chemin audio.

### Twilio

Le transport Twilio est un plan de numérotation strict délégué au plugin Voice Call. Il n'analyse pas les pages Meet pour les numéros de téléphone.

```bash
openclaw googlemeet join https://meet.google.com/abc-defg-hij \
  --transport twilio \
  --dial-in-number +15551234567 \
  --pin 123456
```

Utilisez `--dtmf-sequence` quand la réunion a besoin d'une séquence personnalisée :

```bash
openclaw googlemeet join https://meet.google.com/abc-defg-hij \
  --transport twilio \
  --dial-in-number +15551234567 \
  --dtmf-sequence ww123456#
```

## OAuth et préflight

L'accès à l'API Google Meet Media utilise d'abord un client OAuth personnel. Configurez `oauth.clientId` et optionnellement `oauth.clientSecret`, puis exécutez :

```bash
openclaw googlemeet auth login --json
```

La commande imprime un bloc de configuration `oauth` avec un jeton d'actualisation. Elle utilise PKCE, le rappel localhost sur `http://localhost:8085/oauth2callback` et un flux de copie/collage manuel avec `--manual`.

Ces variables d'environnement sont acceptées comme solutions de secours :

- `OPENCLAW_GOOGLE_MEET_CLIENT_ID` ou `GOOGLE_MEET_CLIENT_ID`
- `OPENCLAW_GOOGLE_MEET_CLIENT_SECRET` ou `GOOGLE_MEET_CLIENT_SECRET`
- `OPENCLAW_GOOGLE_MEET_REFRESH_TOKEN` ou `GOOGLE_MEET_REFRESH_TOKEN`
- `OPENCLAW_GOOGLE_MEET_ACCESS_TOKEN` ou `GOOGLE_MEET_ACCESS_TOKEN`
- `OPENCLAW_GOOGLE_MEET_ACCESS_TOKEN_EXPIRES_AT` ou
  `GOOGLE_MEET_ACCESS_TOKEN_EXPIRES_AT`
- `OPENCLAW_GOOGLE_MEET_DEFAULT_MEETING` ou `GOOGLE_MEET_DEFAULT_MEETING`
- `OPENCLAW_GOOGLE_MEET_PREVIEW_ACK` ou `GOOGLE_MEET_PREVIEW_ACK`

Résolvez une URL Meet, un code ou `spaces/{id}` via `spaces.get` :

```bash
openclaw googlemeet resolve-space --meeting https://meet.google.com/abc-defg-hij
```

Exécutez le préflight avant le travail multimédia :

```bash
openclaw googlemeet preflight --meeting https://meet.google.com/abc-defg-hij
```

Définissez `preview.enrollmentAcknowledged: true` uniquement après avoir confirmé que votre projet Cloud, votre principal OAuth et les participants à la réunion sont inscrits au programme Google Workspace Developer Preview pour les API Meet media.

## Configuration

Le chemin en temps réel Chrome courant ne nécessite que le plugin activé, BlackHole, SoX et une clé OpenAI :

```bash
brew install blackhole-2ch sox
export OPENAI_API_KEY=sk-...
```

Définissez la configuration du plugin sous `plugins.entries.google-meet.config` :

```json5
{
  plugins: {
    entries: {
      "google-meet": {
        enabled: true,
        config: {},
      },
    },
  },
}
```

Valeurs par défaut :

- `defaultTransport: "chrome"`
- `defaultMode: "realtime"`
- `chromeNode.node` : ID/nom/IP du nœud optionnel pour `chrome-node`
- `chrome.audioBackend: "blackhole-2ch"`
- `chrome.audioInputCommand` : commande SoX `rec` écrivant l'audio mu-law G.711 8 kHz sur stdout
- `chrome.audioOutputCommand` : commande SoX `play` lisant l'audio mu-law G.711 8 kHz depuis stdin
- `realtime.provider: "openai"`
- `realtime.toolPolicy: "safe-read-only"`
- `realtime.instructions` : réponses parlées brèves, avec `openclaw_agent_consult` pour les réponses plus approfondies

Remplacements optionnels :

```json5
{
  defaults: {
    meeting: "https://meet.google.com/abc-defg-hij",
  },
  chrome: {
    browserProfile: "Default",
  },
  chromeNode: {
    node: "parallels-macos",
  },
  realtime: {
    toolPolicy: "owner",
  },
}
```

Configuration Twilio uniquement :

```json5
{
  defaultTransport: "twilio",
  twilio: {
    defaultDialInNumber: "+15551234567",
    defaultPin: "123456",
  },
  voiceCall: {
    gatewayUrl: "ws://127.0.0.1:18789",
  },
}
```

## Outil

Les agents peuvent utiliser l'outil `google_meet` :

```json
{
  "action": "join",
  "url": "https://meet.google.com/abc-defg-hij",
  "transport": "chrome-node",
  "mode": "realtime"
}
```

Utilisez `transport: "chrome"` quand Chrome s'exécute sur l'hôte de passerelle. Utilisez `transport: "chrome-node"` quand Chrome s'exécute sur un nœud appairé tel qu'une VM Parallels. Dans les deux cas, le modèle en temps réel et `openclaw_agent_consult` s'exécutent sur l'hôte de passerelle, les identifiants de modèle restent donc là.

Utilisez `action: "status"` pour lister les sessions actives ou inspecter un ID de session. Utilisez `action: "leave"` pour marquer une session comme terminée.

## Consultation d'agent en temps réel

Le mode temps réel de Chrome est optimisé pour une boucle vocale en direct. Le fournisseur de voix temps réel entend l'audio de la réunion et parle via le pont audio configuré. Lorsque le modèle temps réel a besoin d'un raisonnement plus approfondi, d'informations actuelles ou des outils OpenClaw normaux, il peut appeler `openclaw_agent_consult`.

L'outil de consultation exécute l'agent OpenClaw régulier en arrière-plan avec le contexte de la transcription récente de la réunion et retourne une réponse parlée concise à la session vocale temps réel. Le modèle vocal peut alors prononcer cette réponse dans la réunion.

`realtime.toolPolicy` contrôle l'exécution de la consultation :

- `safe-read-only` : expose l'outil de consultation et limite l'agent régulier à `read`, `web_search`, `web_fetch`, `x_search`, `memory_search` et `memory_get`.
- `owner` : expose l'outil de consultation et permet à l'agent régulier d'utiliser la politique d'outils d'agent normale.
- `none` : n'expose pas l'outil de consultation au modèle vocal temps réel.

La clé de session de consultation est limitée par session Meet, donc les appels de consultation ultérieurs peuvent réutiliser le contexte de consultation antérieur pendant la même réunion.

## Remarques

L'API média officielle de Google Meet est orientée vers la réception, donc parler dans un appel Meet nécessite toujours un chemin de participant. Ce plugin maintient cette limite visible : Chrome gère la participation au navigateur et le routage audio local ; Twilio gère la participation par appel téléphonique.

Le mode temps réel de Chrome nécessite soit :

- `chrome.audioInputCommand` plus `chrome.audioOutputCommand` : OpenClaw possède le pont du modèle temps réel et canalise l'audio mu-law G.711 8 kHz entre ces commandes et le fournisseur de voix temps réel sélectionné.
- `chrome.audioBridgeCommand` : une commande de pont externe possède tout le chemin audio local et doit se terminer après le démarrage ou la validation de son démon.

Pour un audio duplex propre, routez la sortie Meet et le microphone Meet via des appareils virtuels séparés ou un graphique d'appareils virtuels de style Loopback. Un seul appareil BlackHole partagé peut renvoyer les autres participants dans l'appel.

`googlemeet leave` arrête la paire de commandes du pont audio temps réel pour les sessions Chrome. Pour les sessions Twilio déléguées via le plugin Voice Call, il raccroche également l'appel vocal sous-jacent.

## Connexes

- [Plugin d'appel vocal](/fr/plugins/voice-call)
- [Mode Talk](/fr/nodes/talk)
- [Création de plugins](/fr/plugins/building-plugins)
