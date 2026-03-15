---
summary: "Service de contrôle de navigateur intégré + commandes d'action"
read_when:
  - Adding agent-controlled browser automation
  - Debugging why openclaw is interfering with your own Chrome
  - Implementing browser settings + lifecycle in the macOS app
title: "Browser (OpenClaw-managed)"
---

# Browser (openclaw-managed)

OpenClaw peut exécuter un **profil Chrome/Brave/Edge/Chromium dédié** que l'agent contrôle.
Il est isolé de votre navigateur personnel et est géré via un petit service de contrôle local à l'intérieur de la Gateway (loopback uniquement).

Vue pour débutants :

- Pensez-y comme un **navigateur séparé, réservé à l'agent**.
- Le profil `openclaw` ne **touche pas** à votre profil de navigateur personnel.
- L'agent peut **ouvrir des onglets, lire des pages, cliquer et taper** dans une voie sécurisée.
- Le profil `user` intégré s'attache à votre véritable session Chrome connectée ;
  `chrome-relay` est le profil de relais d'extension explicite.

## Ce que vous obtenez

- Un profil de navigateur séparé nommé **openclaw** (accent orange par défaut).
- Contrôle d'onglet déterministe (liste/ouverture/focus/fermeture).
- Actions d'agent (clic/saisie/glisser/sélectionner), snapshots, captures d'écran, PDF.
- Support multi-profil optionnel (`openclaw`, `work`, `remote`, ...).

Ce navigateur n'est **pas** votre navigateur quotidien. C'est une surface isolée et sécurisée pour
l'automatisation et la vérification par agent.

## Démarrage rapide

```bash
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

Si vous obtenez « Browser disabled », activez-le dans la configuration (voir ci-dessous) et redémarrez la
Gateway.

## Profils : `openclaw` vs `user` vs `chrome-relay`

- `openclaw` : navigateur géré et isolé (aucune extension requise).
- `user` : profil d'attachement MCP Chrome intégré pour votre **véritable session Chrome connectée**
  .
- `chrome-relay` : relais d'extension vers votre **navigateur système** (nécessite que l'extension
  OpenClaw soit attachée à un onglet).

Pour les appels d'outil de navigateur d'agent :

- Par défaut : utilisez le navigateur `openclaw` isolé.
- Préférez `profile="user"` quand les sessions connectées existantes sont importantes et que l'utilisateur
  est à l'ordinateur pour cliquer/approuver une invite d'attachement.
- Utilisez `profile="chrome-relay"` uniquement quand l'utilisateur veut explicitement le flux
  d'attachement de l'extension Chrome / bouton de barre d'outils.
- `profile` est le remplacement explicite quand vous voulez un mode de navigateur spécifique.

Définissez `browser.defaultProfile: "openclaw"` si vous voulez le mode géré par défaut.

## Configuration

Les paramètres du navigateur se trouvent dans `~/.openclaw/openclaw.json`.

```json5
{
  browser: {
    enabled: true, // default: true
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: true, // default trusted-network mode
      // allowPrivateNetwork: true, // legacy alias
      // hostnameAllowlist: ["*.example.com", "example.com"],
      // allowedHostnames: ["localhost"],
    },
    // cdpUrl: "http://127.0.0.1:18792", // legacy single-profile override
    remoteCdpTimeoutMs: 1500, // remote CDP HTTP timeout (ms)
    remoteCdpHandshakeTimeoutMs: 3000, // remote CDP WebSocket handshake timeout (ms)
    defaultProfile: "openclaw",
    color: "#FF4500",
    headless: false,
    noSandbox: false,
    attachOnly: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      user: {
        driver: "existing-session",
        attachOnly: true,
        color: "#00AA00",
      },
      "chrome-relay": {
        driver: "extension",
        cdpUrl: "http://127.0.0.1:18792",
        color: "#00AA00",
      },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
  },
}
```

Notes :

- Le service de contrôle du navigateur se lie à loopback sur un port dérivé de `gateway.port`
  (par défaut : `18791`, qui est gateway + 2). Le relais utilise le port suivant (`18792`).
- Si vous remplacez le port de la Gateway (`gateway.port` ou `OPENCLAW_GATEWAY_PORT`),
  les ports de navigateur dérivés se décalent pour rester dans la même « famille ».
- `cdpUrl` par défaut au port de relais quand non défini.
- `remoteCdpTimeoutMs` s'applique aux vérifications de disponibilité CDP distantes (non-loopback).
- `remoteCdpHandshakeTimeoutMs` s'applique aux vérifications de disponibilité WebSocket CDP distantes.
- La navigation du navigateur/ouverture d'onglet est gardée par SSRF avant la navigation et revérifiée au mieux sur l'URL `http(s)` finale après la navigation.
- `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` par défaut à `true` (modèle de réseau de confiance). Définissez-le à `false` pour une navigation strictement publique uniquement.
- `browser.ssrfPolicy.allowPrivateNetwork` reste supporté comme alias hérité pour la compatibilité.
- `attachOnly: true` signifie « ne jamais lancer un navigateur local ; attachez-vous uniquement s'il est déjà en cours d'exécution ».
- `color` + `color` par profil tinte l'interface du navigateur pour que vous puissiez voir quel profil est actif.
- Le profil par défaut est `openclaw` (navigateur autonome géré par OpenClaw). Utilisez `defaultProfile: "user"` pour opter pour le navigateur utilisateur connecté, ou `defaultProfile: "chrome-relay"` pour le relais d'extension.
- Ordre de détection automatique : navigateur par défaut du système s'il est basé sur Chromium ; sinon Chrome → Brave → Edge → Chromium → Chrome Canary.
- Les profils `openclaw` locaux attribuent automatiquement `cdpPort`/`cdpUrl` — définissez-les uniquement pour CDP distant.
- `driver: "existing-session"` utilise Chrome DevTools MCP au lieu de CDP brut. Ne
  définissez pas `cdpUrl` pour ce pilote.

## Utiliser Brave (ou un autre navigateur basé sur Chromium)

Si votre **navigateur par défaut du système** est basé sur Chromium (Chrome/Brave/Edge/etc),
OpenClaw l'utilise automatiquement. Définissez `browser.executablePath` pour remplacer
la détection automatique :

Exemple CLI :

```bash
openclaw config set browser.executablePath "/usr/bin/google-chrome"
```

```json5
// macOS
{
  browser: {
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
  }
}

// Windows
{
  browser: {
    executablePath: "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
  }
}

// Linux
{
  browser: {
    executablePath: "/usr/bin/brave-browser"
  }
}
```

## Contrôle local vs distant

- **Contrôle local (par défaut) :** la Gateway démarre le service de contrôle loopback et peut lancer un navigateur local.
- **Contrôle distant (hôte de nœud) :** exécutez un hôte de nœud sur la machine qui a le navigateur ; la Gateway proxifie les actions du navigateur vers celui-ci.
- **CDP distant :** définissez `browser.profiles.<name>.cdpUrl` (ou `browser.cdpUrl`) pour
  vous attacher à un navigateur basé sur Chromium distant. Dans ce cas, OpenClaw ne lancera pas de navigateur local.

Les URL CDP distantes peuvent inclure l'authentification :

- Jetons de requête (par ex. `https://provider.example?token=<token>`)
- Authentification HTTP Basic (par ex. `https://user:pass@provider.example`)

OpenClaw préserve l'authentification lors de l'appel des points de terminaison `/json/*` et lors de la connexion
au WebSocket CDP. Préférez les variables d'environnement ou les gestionnaires de secrets pour
les jetons au lieu de les valider dans les fichiers de configuration.

## Proxy de navigateur de nœud (par défaut zéro-config)

Si vous exécutez un **hôte de nœud** sur la machine qui a votre navigateur, OpenClaw peut
acheminer automatiquement les appels d'outil de navigateur vers ce nœud sans configuration de navigateur supplémentaire.
C'est le chemin par défaut pour les gateways distantes.

Notes :

- L'hôte de nœud expose son serveur de contrôle de navigateur local via une **commande de proxy**.
- Les profils proviennent de la propre configuration `browser.profiles` du nœud (identique à local).
- Désactivez si vous ne le voulez pas :
  - Sur le nœud : `nodeHost.browserProxy.enabled=false`
  - Sur la gateway : `gateway.nodes.browser.mode="off"`

## Browserless (CDP distant hébergé)

[Browserless](https://browserless.io) est un service Chromium hébergé qui expose
les points de terminaison CDP sur HTTPS. Vous pouvez pointer un profil de navigateur OpenClaw vers un
point de terminaison de région Browserless et vous authentifier avec votre clé API.

Exemple :

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "browserless",
    remoteCdpTimeoutMs: 2000,
    remoteCdpHandshakeTimeoutMs: 4000,
    profiles: {
      browserless: {
        cdpUrl: "https://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
        color: "#00AA00",
      },
    },
  },
}
```

Notes :

- Remplacez `<BROWSERLESS_API_KEY>` par votre véritable jeton Browserless.
- Choisissez le point de terminaison de région qui correspond à votre compte Browserless (voir leur documentation).

## Fournisseurs CDP WebSocket directs

Certains services de navigateur hébergés exposent un **point de terminaison WebSocket direct** plutôt que
le découverte CDP standard basée sur HTTP (`/json/version`). OpenClaw supporte les deux :

- **Points de terminaison HTTP(S)** (par ex. Browserless) — OpenClaw appelle `/json/version` pour
  découvrir l'URL du débogueur WebSocket, puis se connecte.
- **Points de terminaison WebSocket** (`ws://` / `wss://`) — OpenClaw se connecte directement,
  en ignorant `/json/version`. Utilisez ceci pour les services comme
  [Browserbase](https://www.browserbase.com) ou tout fournisseur qui vous donne une
  URL WebSocket.

### Browserbase

[Browserbase](https://www.browserbase.com) est une plateforme cloud pour exécuter
des navigateurs headless avec résolution CAPTCHA intégrée, mode furtif et proxies résidentiels.

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "browserbase",
    remoteCdpTimeoutMs: 3000,
    remoteCdpHandshakeTimeoutMs: 5000,
    profiles: {
      browserbase: {
        cdpUrl: "wss://connect.browserbase.com?apiKey=<BROWSERBASE_API_KEY>",
        color: "#F97316",
      },
    },
  },
}
```

Notes :

- [Inscrivez-vous](https://www.browserbase.com/sign-up) et copiez votre **Clé API**
  depuis le [tableau de bord Vue d'ensemble](https://www.browserbase.com/overview).
- Remplacez `<BROWSERBASE_API_KEY>` par votre véritable clé API Browserbase.
- Browserbase crée automatiquement une session de navigateur lors de la connexion WebSocket, donc aucune
  étape de création de session manuelle n'est nécessaire.
- Le niveau gratuit permet une session concurrente et une heure de navigateur par mois.
  Voir [tarification](https://www.browserbase.com/pricing) pour les limites des plans payants.
- Voir la [documentation Browserbase](https://docs.browserbase.com) pour la référence API complète,
  les guides SDK et les exemples d'intégration.

## Sécurité

Idées clés :

- Le contrôle du navigateur est loopback uniquement ; l'accès s'écoule via l'authentification de la Gateway ou l'appairage de nœud.
- Si le contrôle du navigateur est activé et qu'aucune authentification n'est configurée, OpenClaw génère automatiquement `gateway.auth.token` au démarrage et le persiste dans la configuration.
- Gardez la Gateway et tous les hôtes de nœud sur un réseau privé (Tailscale) ; évitez l'exposition publique.
- Traitez les URL/jetons CDP distants comme des secrets ; préférez les variables d'environnement ou un gestionnaire de secrets.

Conseils CDP distants :

- Préférez les points de terminaison chiffrés (HTTPS ou WSS) et les jetons de courte durée si possible.
- Évitez d'intégrer les jetons de longue durée directement dans les fichiers de configuration.

## Profils (multi-navigateur)

OpenClaw supporte plusieurs profils nommés (configurations de routage). Les profils peuvent être :

- **openclaw-managed** : une instance de navigateur Chromium dédiée avec son propre répertoire de données utilisateur + port CDP
- **remote** : une URL CDP explicite (navigateur basé sur Chromium exécuté ailleurs)
- **extension relay** : vos onglets Chrome existants via le relais local + extension Chrome
- **existing session** : votre profil Chrome existant via auto-connexion Chrome DevTools MCP

Valeurs par défaut :

- Le profil `openclaw` est créé automatiquement s'il manque.
- Le profil `chrome-relay` est intégré pour le relais d'extension Chrome (pointe vers `http://127.0.0.1:18792` par défaut).
- Les profils de session existante sont opt-in ; créez-les avec `--driver existing-session`.
- Les ports CDP locaux s'allouent à partir de **18800–18899** par défaut.
- La suppression d'un profil déplace son répertoire de données local à la Corbeille.

Tous les points de terminaison de contrôle acceptent `?profile=<name>` ; la CLI utilise `--browser-profile`.

## Relais d'extension Chrome (utilisez votre Chrome existant)

OpenClaw peut également piloter **vos onglets Chrome existants** (pas d'instance Chrome "openclaw" séparée) via un relais CDP local + une extension Chrome.

Guide complet : [Extension Chrome](/fr/tools/chrome-extension)

Flux :

- La Gateway s'exécute localement (même machine) ou un nœud s'exécute sur la machine du navigateur.
- Un **serveur relais** local écoute sur une adresse de loopback `cdpUrl` (par défaut : `http://127.0.0.1:18792`).
- Vous cliquez sur l'icône de l'extension **OpenClaw Browser Relay** sur un onglet pour l'attacher (elle ne s'attache pas automatiquement).
- L'agent contrôle cet onglet via l'outil `browser` normal, en sélectionnant le bon profil.

Si la Gateway s'exécute ailleurs, exécutez un nœud hôte sur la machine du navigateur pour que la Gateway puisse relayer les actions du navigateur.

### Sessions en sandbox

Si la session de l'agent est en sandbox, l'outil `browser` peut par défaut utiliser `target="sandbox"` (navigateur sandbox).
La prise de contrôle du relais d'extension Chrome nécessite le contrôle du navigateur hôte, donc soit :

- exécutez la session sans sandbox, soit
- définissez `agents.defaults.sandbox.browser.allowHostControl: true` et utilisez `target="host"` lors de l'appel de l'outil.

### Configuration

1. Chargez l'extension (dev/unpacked) :

```bash
openclaw browser extension install
```

- Chrome → `chrome://extensions` → activez le "Mode développeur"
- "Charger l'extension non empaquetée" → sélectionnez le répertoire affiché par `openclaw browser extension path`
- Épinglez l'extension, puis cliquez dessus sur l'onglet que vous souhaitez contrôler (le badge affiche `ON`).

2. Utilisez-la :

- CLI : `openclaw browser --browser-profile chrome-relay tabs`
- Outil Agent : `browser` avec `profile="chrome-relay"`

Optionnel : si vous souhaitez un nom ou un port relais différent, créez votre propre profil :

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

Notes :

- Ce mode s'appuie sur Playwright-on-CDP pour la plupart des opérations (captures d'écran/snapshots/actions).
- Détachez-vous en cliquant à nouveau sur l'icône de l'extension.
- Utilisation par l'agent : préférez `profile="user"` pour les sites connectés. Utilisez `profile="chrome-relay"`
  uniquement lorsque vous souhaitez spécifiquement le flux d'extension. L'utilisateur doit être présent
  pour cliquer sur l'extension et attacher l'onglet.

## Session Chrome existante via MCP

OpenClaw peut également se connecter à un profil Chrome en cours d'exécution via le serveur MCP officiel
Chrome DevTools. Cela réutilise les onglets et l'état de connexion déjà ouverts dans
ce profil Chrome.

Références officielles de contexte et de configuration :

- [Chrome for Developers: Use Chrome DevTools MCP with your browser session](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session)
- [Chrome DevTools MCP README](https://github.com/ChromeDevTools/chrome-devtools-mcp)

Profil intégré :

- `user`

Optionnel : créez votre propre profil de session existante personnalisé si vous souhaitez un
nom ou une couleur différente.

Ensuite dans Chrome :

1. Ouvrez `chrome://inspect/#remote-debugging`
2. Activez le débogage à distance
3. Gardez Chrome en cours d'exécution et approuvez l'invite de connexion lorsque OpenClaw se connecte

Test de fumée d'attachement en direct :

```bash
openclaw browser --browser-profile user start
openclaw browser --browser-profile user status
openclaw browser --browser-profile user tabs
openclaw browser --browser-profile user snapshot --format ai
```

À quoi ressemble le succès :

- `status` affiche `driver: existing-session`
- `status` affiche `transport: chrome-mcp`
- `status` affiche `running: true`
- `tabs` répertorie vos onglets Chrome déjà ouverts
- `snapshot` retourne des références de l'onglet en direct sélectionné

Quoi vérifier si l'attachement ne fonctionne pas :

- Chrome est version `144+`
- le débogage à distance est activé sur `chrome://inspect/#remote-debugging`
- Chrome a affiché et vous avez accepté l'invite de consentement d'attachement

Utilisation par l'agent :

- Utilisez `profile="user"` lorsque vous avez besoin de l'état du navigateur connecté de l'utilisateur.
- Si vous utilisez un profil de session existante personnalisé, transmettez ce nom de profil explicite.
- Préférez `profile="user"` à `profile="chrome-relay"` sauf si l'utilisateur
  souhaite explicitement le flux d'extension / d'attachement d'onglet.
- Choisissez ce mode uniquement lorsque l'utilisateur est à l'ordinateur pour approuver l'invite d'attachement.
- la Gateway ou le nœud hôte peut générer `npx chrome-devtools-mcp@latest --autoConnect`

Notes :

- Ce chemin est plus risqué que le profil `openclaw` isolé car il peut
  agir dans votre session de navigateur connectée.
- OpenClaw ne lance pas Chrome pour ce pilote ; il se connecte uniquement à une session existante.
- OpenClaw utilise ici le flux officiel Chrome DevTools MCP `--autoConnect`, pas
  le flux de port de débogage à distance du profil par défaut hérité.
- Les captures d'écran de session existante supportent les captures de page et les captures d'éléments `--ref`
  à partir de snapshots, mais pas les sélecteurs CSS `--element`.
- La session existante `wait --url` supporte les modèles exacts, substring et glob
  comme les autres pilotes de navigateur. `wait --load networkidle` n'est pas encore supporté.
- Certaines fonctionnalités nécessitent toujours le relais d'extension ou le chemin du navigateur géré, comme
  l'export PDF et l'interception de téléchargement.
- Laissez le relais loopback uniquement par défaut. Si le relais doit être accessible à partir d'un espace de noms réseau différent (par exemple Gateway dans WSL2, Chrome sur Windows), définissez `browser.relayBindHost` sur une adresse de liaison explicite telle que `0.0.0.0` tout en gardant le réseau environnant privé et authentifié.

Exemple WSL2 / cross-namespace :

```json5
{
  browser: {
    enabled: true,
    relayBindHost: "0.0.0.0",
    defaultProfile: "chrome-relay",
  },
}
```

## Garanties d'isolation

- **Répertoire de données utilisateur dédié** : ne touche jamais votre profil de navigateur personnel.
- **Ports dédiés** : évite `9222` pour prévenir les collisions avec les flux de développement.
- **Contrôle d'onglet déterministe** : ciblez les onglets par `targetId`, pas "dernier onglet".

## Sélection du navigateur

Lors du lancement local, OpenClaw choisit le premier disponible :

1. Chrome
2. Brave
3. Edge
4. Chromium
5. Chrome Canary

Vous pouvez remplacer avec `browser.executablePath`.

Plateformes :

- macOS : vérifie `/Applications` et `~/Applications`.
- Linux : recherche `google-chrome`, `brave`, `microsoft-edge`, `chromium`, etc.
- Windows : vérifie les emplacements d'installation courants.

## API de contrôle (optionnel)

Pour les intégrations locales uniquement, la Gateway expose une petite API HTTP loopback :

- Statut/démarrage/arrêt : `GET /`, `POST /start`, `POST /stop`
- Onglets : `GET /tabs`, `POST /tabs/open`, `POST /tabs/focus`, `DELETE /tabs/:targetId`
- Snapshot/capture d'écran : `GET /snapshot`, `POST /screenshot`
- Actions : `POST /navigate`, `POST /act`
- Hooks : `POST /hooks/file-chooser`, `POST /hooks/dialog`
- Téléchargements : `POST /download`, `POST /wait/download`
- Débogage : `GET /console`, `POST /pdf`
- Débogage : `GET /errors`, `GET /requests`, `POST /trace/start`, `POST /trace/stop`, `POST /highlight`
- Réseau : `POST /response/body`
- État : `GET /cookies`, `POST /cookies/set`, `POST /cookies/clear`
- État : `GET /storage/:kind`, `POST /storage/:kind/set`, `POST /storage/:kind/clear`
- Paramètres : `POST /set/offline`, `POST /set/headers`, `POST /set/credentials`, `POST /set/geolocation`, `POST /set/media`, `POST /set/timezone`, `POST /set/locale`, `POST /set/device`

Tous les points de terminaison acceptent `?profile=<name>`.

Si l'authentification de la gateway est configurée, les routes HTTP du navigateur nécessitent également l'authentification :

- `Authorization: Bearer <gateway token>`
- `x-openclaw-password: <gateway password>` ou authentification HTTP Basic avec ce mot de passe

### Exigence Playwright

Certaines fonctionnalités (navigate/act/snapshot IA/snapshot de rôle, captures d'écran d'éléments, PDF) nécessitent
Playwright. Si Playwright n'est pas installé, ces points de terminaison retournent une erreur 501 claire.
Les snapshots ARIA et les captures d'écran de base fonctionnent toujours pour le Chrome géré par openclaw.
Pour le pilote relais d'extension Chrome, les snapshots ARIA et les captures d'écran nécessitent Playwright.

Si vous voyez `Playwright is not available in this gateway build`, installez le package
Playwright complet (pas `playwright-core`) et redémarrez la gateway, ou réinstallez
OpenClaw avec le support du navigateur.

#### Installation Docker Playwright

Si votre Gateway s'exécute dans Docker, évitez `npx playwright` (conflits de remplacement npm).
Utilisez plutôt la CLI groupée :

```bash
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

Pour persister les téléchargements du navigateur, définissez `PLAYWRIGHT_BROWSERS_PATH` (par exemple,
`/home/node/.cache/ms-playwright`) et assurez-vous que `/home/node` est persisté via
`OPENCLAW_HOME_VOLUME` ou un montage de liaison. Voir [Docker](/fr/install/docker).

## Comment ça marche (interne)

Flux de haut niveau :

- Un petit **serveur de contrôle** accepte les requêtes HTTP.
- Il se connecte aux navigateurs basés sur Chromium (Chrome/Brave/Edge/Chromium) via **CDP**.
- Pour les actions avancées (clic/saisie/snapshot/PDF), il utilise **Playwright** sur
  CDP.
- Lorsque Playwright est manquant, seules les opérations non-Playwright sont disponibles.

Cette conception maintient l'agent sur une interface stable et déterministe tout en vous permettant
d'échanger des navigateurs locaux/distants et des profils.

## Référence rapide de la CLI

Toutes les commandes acceptent `--browser-profile <name>` pour cibler un profil spécifique.
Toutes les commandes acceptent également `--json` pour une sortie lisible par machine (charges utiles stables).

Bases :

- `openclaw browser status`
- `openclaw browser start`
- `openclaw browser stop`
- `openclaw browser tabs`
- `openclaw browser tab`
- `openclaw browser tab new`
- `openclaw browser tab select 2`
- `openclaw browser tab close 2`
- `openclaw browser open https://example.com`
- `openclaw browser focus abcd1234`
- `openclaw browser close abcd1234`

Inspection :

- `openclaw browser screenshot`
- `openclaw browser screenshot --full-page`
- `openclaw browser screenshot --ref 12`
- `openclaw browser screenshot --ref e12`
- `openclaw browser snapshot`
- `openclaw browser snapshot --format aria --limit 200`
- `openclaw browser snapshot --interactive --compact --depth 6`
- `openclaw browser snapshot --efficient`
- `openclaw browser snapshot --labels`
- `openclaw browser snapshot --selector "#main" --interactive`
- `openclaw browser snapshot --frame "iframe#main" --interactive`
- `openclaw browser console --level error`
- `openclaw browser errors --clear`
- `openclaw browser requests --filter api --clear`
- `openclaw browser pdf`
- `openclaw browser responsebody "**/api" --max-chars 5000`

Actions :

- `openclaw browser navigate https://example.com`
- `openclaw browser resize 1280 720`
- `openclaw browser click 12 --double`
- `openclaw browser click e12 --double`
- `openclaw browser type 23 "hello" --submit`
- `openclaw browser press Enter`
- `openclaw browser hover 44`
- `openclaw browser scrollintoview e12`
- `openclaw browser drag 10 11`
- `openclaw browser select 9 OptionA OptionB`
- `openclaw browser download e12 report.pdf`
- `openclaw browser waitfordownload report.pdf`
- `openclaw browser upload /tmp/openclaw/uploads/file.pdf`
- `openclaw browser fill --fields '[{"ref":"1","type":"text","value":"Ada"}]'`
- `openclaw browser dialog --accept`
- `openclaw browser wait --text "Done"`
- `openclaw browser wait "#main" --url "**/dash" --load networkidle --fn "window.ready===true"`
- `openclaw browser evaluate --fn '(el) => el.textContent' --ref 7`
- `openclaw browser highlight e12`
- `openclaw browser trace start`
- `openclaw browser trace stop`

État :

- `openclaw browser cookies`
- `openclaw browser cookies set session abc123 --url "https://example.com"`
- `openclaw browser cookies clear`
- `openclaw browser storage local get`
- `openclaw browser storage local set theme dark`
- `openclaw browser storage session clear`
- `openclaw browser set offline on`
- `openclaw browser set headers --headers-json '{"X-Debug":"1"}'`
- `openclaw browser set credentials user pass`
- `openclaw browser set credentials --clear`
- `openclaw browser set geo 37.7749 -122.4194 --origin "https://example.com"`
- `openclaw browser set geo --clear`
- `openclaw browser set media dark`
- `openclaw browser set timezone America/New_York`
- `openclaw browser set locale en-US`
- `openclaw browser set device "iPhone 14"`

Notes :

- `upload` et `dialog` sont des appels **d'armement** ; exécutez-les avant le click/press
  qui déclenche le sélecteur de fichier/dialogue.
- Les chemins de sortie des téléchargements et des traces sont limités aux racines temporaires d'OpenClaw :
  - traces : `/tmp/openclaw` (secours : `${os.tmpdir()}/openclaw`)
  - téléchargements : `/tmp/openclaw/downloads` (secours : `${os.tmpdir()}/openclaw/downloads`)
- Les chemins de téléchargement sont limités à une racine temporaire de téléchargements d'OpenClaw :
  - téléchargements : `/tmp/openclaw/uploads` (secours : `${os.tmpdir()}/openclaw/uploads`)
- `upload` peut également définir directement les entrées de fichier via `--input-ref` ou `--element`.
- `snapshot` :
  - `--format ai` (par défaut quand Playwright est installé) : retourne un snapshot IA avec des refs numériques (`aria-ref="<n>"`).
  - `--format aria` : retourne l'arbre d'accessibilité (pas de refs ; inspection uniquement).
  - `--efficient` (ou `--mode efficient`) : préréglage de snapshot de rôle compact (interactif + compact + profondeur + maxChars inférieur).
  - Défaut de configuration (outil/CLI uniquement) : définissez `browser.snapshotDefaults.mode: "efficient"` pour utiliser des snapshots efficaces quand l'appelant ne passe pas de mode (voir [Configuration de la passerelle](/fr/gateway/configuration#browser-openclaw-managed-browser)).
  - Options de snapshot de rôle (`--interactive`, `--compact`, `--depth`, `--selector`) forcent un snapshot basé sur les rôles avec des refs comme `ref=e12`.
  - `--frame "<iframe selector>"` limite les snapshots de rôle à une iframe (s'associe avec des refs de rôle comme `e12`).
  - `--interactive` affiche une liste plate et facile à sélectionner d'éléments interactifs (meilleur pour piloter les actions).
  - `--labels` ajoute une capture d'écran de la fenêtre d'affichage uniquement avec des étiquettes de ref superposées (imprime `MEDIA:<path>`).
- `click`/`type`/etc nécessitent une `ref` de `snapshot` (soit numérique `12` soit ref de rôle `e12`).
  Les sélecteurs CSS ne sont intentionnellement pas supportés pour les actions.

## Snapshots et refs

OpenClaw supporte deux styles de « snapshot » :

- **Snapshot IA (refs numériques)** : `openclaw browser snapshot` (par défaut ; `--format ai`)
  - Sortie : un snapshot texte qui inclut des refs numériques.
  - Actions : `openclaw browser click 12`, `openclaw browser type 23 "hello"`.
  - En interne, la ref est résolue via `aria-ref` de Playwright.

- **Snapshot de rôle (refs de rôle comme `e12`)** : `openclaw browser snapshot --interactive` (ou `--compact`, `--depth`, `--selector`, `--frame`)
  - Sortie : une liste/arbre basée sur les rôles avec `[ref=e12]` (et optionnellement `[nth=1]`).
  - Actions : `openclaw browser click e12`, `openclaw browser highlight e12`.
  - En interne, la ref est résolue via `getByRole(...)` (plus `nth()` pour les doublons).
  - Ajoutez `--labels` pour inclure une capture d'écran de la fenêtre d'affichage avec des étiquettes `e12` superposées.

Comportement des refs :

- Les refs ne sont **pas stables lors des navigations** ; si quelque chose échoue, réexécutez `snapshot` et utilisez une ref fraîche.
- Si le snapshot de rôle a été pris avec `--frame`, les refs de rôle sont limitées à cette iframe jusqu'au prochain snapshot de rôle.

## Améliorations d'attente

Vous pouvez attendre plus que juste le temps/texte :

- Attendre une URL (globs supportés par Playwright) :
  - `openclaw browser wait --url "**/dash"`
- Attendre un état de chargement :
  - `openclaw browser wait --load networkidle`
- Attendre un prédicat JS :
  - `openclaw browser wait --fn "window.ready===true"`
- Attendre qu'un sélecteur devienne visible :
  - `openclaw browser wait "#main"`

Ceux-ci peuvent être combinés :

```bash
openclaw browser wait "#main" \
  --url "**/dash" \
  --load networkidle \
  --fn "window.ready===true" \
  --timeout-ms 15000
```

## Déboguer les flux de travail

Quand une action échoue (par ex. « non visible », « violation du mode strict », « couvert ») :

1. `openclaw browser snapshot --interactive`
2. Utilisez `click <ref>` / `type <ref>` (préférez les refs de rôle en mode interactif)
3. Si cela échoue toujours : `openclaw browser highlight <ref>` pour voir ce que Playwright cible
4. Si la page se comporte bizarrement :
   - `openclaw browser errors --clear`
   - `openclaw browser requests --filter api --clear`
5. Pour un débogage approfondi : enregistrez une trace :
   - `openclaw browser trace start`
   - reproduisez le problème
   - `openclaw browser trace stop` (imprime `TRACE:<path>`)

## Sortie JSON

`--json` est pour les scripts et les outils structurés.

Exemples :

```bash
openclaw browser status --json
openclaw browser snapshot --interactive --json
openclaw browser requests --filter api --json
openclaw browser cookies --json
```

Les snapshots de rôle en JSON incluent `refs` plus un petit bloc `stats` (lignes/caractères/refs/interactif) afin que les outils puissent raisonner sur la taille et la densité de la charge utile.

## Boutons d'état et d'environnement

Ceux-ci sont utiles pour les flux de travail « faire en sorte que le site se comporte comme X » :

- Cookies : `cookies`, `cookies set`, `cookies clear`
- Stockage : `storage local|session get|set|clear`
- Hors ligne : `set offline on|off`
- En-têtes : `set headers --headers-json '{"X-Debug":"1"}'` (l'ancien `set headers --json '{"X-Debug":"1"}'` reste supporté)
- Authentification HTTP basique : `set credentials user pass` (ou `--clear`)
- Géolocalisation : `set geo <lat> <lon> --origin "https://example.com"` (ou `--clear`)
- Média : `set media dark|light|no-preference|none`
- Fuseau horaire / locale : `set timezone ...`, `set locale ...`
- Appareil / fenêtre d'affichage :
  - `set device "iPhone 14"` (préréglages d'appareil Playwright)
  - `set viewport 1280 720`

## Sécurité et confidentialité

- Le profil du navigateur openclaw peut contenir des sessions connectées ; traitez-le comme sensible.
- `browser act kind=evaluate` / `openclaw browser evaluate` et `wait --fn`
  exécutent du JavaScript arbitraire dans le contexte de la page. L'injection d'invite peut le diriger.
  Désactivez-le avec `browser.evaluateEnabled=false` si vous n'en avez pas besoin.
- Pour les connexions et les notes anti-bot (X/Twitter, etc.), voir [Connexion au navigateur + publication X/Twitter](/fr/tools/browser-login).
- Gardez la passerelle/l'hôte nœud privé (loopback ou tailnet uniquement).
- Les points de terminaison CDP distants sont puissants ; tunnelisez et protégez-les.

Exemple de mode strict (bloquer les destinations privées/internes par défaut) :

```json5
{
  browser: {
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: false,
      hostnameAllowlist: ["*.example.com", "example.com"],
      allowedHostnames: ["localhost"], // optional exact allow
    },
  },
}
```

## Dépannage

Pour les problèmes spécifiques à Linux (en particulier snap Chromium), voir
[Dépannage du navigateur](/fr/tools/browser-linux-troubleshooting).

Pour les configurations WSL2 Gateway + Windows Chrome split-host, voir
[Dépannage WSL2 + Windows + CDP Chrome distant](/fr/tools/browser-wsl2-windows-remote-cdp-troubleshooting).

## Outils d'agent + fonctionnement du contrôle

L'agent obtient **un outil** pour l'automatisation du navigateur :

- `browser` — status/start/stop/tabs/open/focus/close/snapshot/screenshot/navigate/act

Comment cela s'associe :

- `browser snapshot` retourne un arbre UI stable (IA ou ARIA).
- `browser act` utilise les IDs de ref du snapshot pour cliquer/taper/glisser/sélectionner.
- `browser screenshot` capture les pixels (page complète ou élément).
- `browser` accepte :
  - `profile` pour choisir un profil de navigateur nommé (openclaw, chrome, ou CDP distant).
  - `target` (`sandbox` | `host` | `node`) pour sélectionner où le navigateur réside.
  - Dans les sessions en sandbox, `target: "host"` nécessite `agents.defaults.sandbox.browser.allowHostControl=true`.
  - Si `target` est omis : les sessions en sandbox par défaut à `sandbox`, les sessions non-sandbox par défaut à `host`.
  - Si un nœud capable de navigateur est connecté, l'outil peut s'acheminer automatiquement vers lui sauf si vous épinglez `target="host"` ou `target="node"`.

Cela garde l'agent déterministe et évite les sélecteurs fragiles.
