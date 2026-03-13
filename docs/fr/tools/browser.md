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
- Le profil `openclaw` ne touche **pas** à votre profil de navigateur personnel.
- L'agent peut **ouvrir des onglets, lire des pages, cliquer et taper** dans une voie sécurisée.
- Le profil `chrome` par défaut utilise le **navigateur Chromium par défaut du système** via le relais d'extension ; basculez vers `openclaw` pour le navigateur géré isolé.

## Ce que vous obtenez

- Un profil de navigateur séparé nommé **openclaw** (accent orange par défaut).
- Contrôle d'onglet déterministe (liste/ouverture/focus/fermeture).
- Actions d'agent (clic/saisie/glisser/sélectionner), snapshots, captures d'écran, PDF.
- Support multi-profil optionnel (`openclaw`, `work`, `remote`, ...).

Ce navigateur n'est **pas** votre navigateur quotidien. C'est une surface sécurisée et isolée pour l'automatisation et la vérification par agent.

## Démarrage rapide

```bash
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

Si vous obtenez « Browser disabled », activez-le dans la configuration (voir ci-dessous) et redémarrez la Gateway.

## Profils : `openclaw` vs `chrome`

- `openclaw` : navigateur géré, isolé (aucune extension requise).
- `chrome` : relais d'extension vers votre **navigateur système** (nécessite que l'extension OpenClaw soit attachée à un onglet).

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
    defaultProfile: "chrome",
    color: "#FF4500",
    headless: false,
    noSandbox: false,
    attachOnly: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
  },
}
```

Notes :

- Le service de contrôle du navigateur se lie à loopback sur un port dérivé de `gateway.port`
  (par défaut : `18791`, qui est gateway + 2). Le relais utilise le port suivant (`18792`).
- Si vous remplacez le port de la Gateway (`gateway.port` ou `OPENCLAW_GATEWAY_PORT`),
  les ports du navigateur dérivés se décalent pour rester dans la même « famille ».
- `cdpUrl` par défaut au port relais quand non défini.
- `remoteCdpTimeoutMs` s'applique aux vérifications de disponibilité CDP distantes (non-loopback).
- `remoteCdpHandshakeTimeoutMs` s'applique aux vérifications de disponibilité WebSocket CDP distantes.
- La navigation du navigateur/ouverture d'onglet est protégée par SSRF avant la navigation et revérifiée au mieux sur l'URL `http(s)` finale après la navigation.
- `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` par défaut à `true` (modèle de réseau de confiance). Définissez-le à `false` pour une navigation strictement publique uniquement.
- `browser.ssrfPolicy.allowPrivateNetwork` reste supporté comme alias hérité pour la compatibilité.
- `attachOnly: true` signifie « ne jamais lancer un navigateur local ; attachez-vous uniquement s'il est déjà en cours d'exécution ».
- `color` + `color` par profil teignent l'interface du navigateur pour que vous puissiez voir quel profil est actif.
- Le profil par défaut est `openclaw` (navigateur autonome géré par OpenClaw). Utilisez `defaultProfile: "chrome"` pour opter pour le relais d'extension Chrome.
- Ordre de détection automatique : navigateur par défaut du système s'il est basé sur Chromium ; sinon Chrome → Brave → Edge → Chromium → Chrome Canary.
- Les profils `openclaw` locaux attribuent automatiquement `cdpPort`/`cdpUrl` — définissez-les uniquement pour CDP distant.

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

- Jetons de requête (par exemple, `https://provider.example?token=<token>`)
- Authentification HTTP Basic (par exemple, `https://user:pass@provider.example`)

OpenClaw préserve l'authentification lors de l'appel des points de terminaison `/json/*` et lors de la connexion
au WebSocket CDP. Préférez les variables d'environnement ou les gestionnaires de secrets pour
les jetons au lieu de les valider dans les fichiers de configuration.

## Proxy de navigateur de nœud (zéro-config par défaut)

Si vous exécutez un **hôte de nœud** sur la machine qui a votre navigateur, OpenClaw peut
acheminer automatiquement les appels d'outil de navigateur vers ce nœud sans configuration de navigateur supplémentaire.
C'est le chemin par défaut pour les gateways distantes.

Notes :

- L'hôte de nœud expose son serveur de contrôle de navigateur local via une **commande proxy**.
- Les profils proviennent de la configuration `browser.profiles` du nœud lui-même (identique au local).
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

- Remplacez `<BROWSERLESS_API_KEY>` par votre vrai jeton Browserless.
- Choisissez le point de terminaison de région qui correspond à votre compte Browserless (voir leur documentation).

## Fournisseurs CDP WebSocket directs

Certains services de navigateur hébergés exposent un **point de terminaison WebSocket direct** plutôt que
le découverte CDP standard basée sur HTTP (`/json/version`). OpenClaw supporte les deux :

- **Points de terminaison HTTP(S)** (par exemple Browserless) — OpenClaw appelle `/json/version` pour
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
- Remplacez `<BROWSERBASE_API_KEY>` par votre vraie clé API Browserbase.
- Browserbase crée automatiquement une session de navigateur lors de la connexion WebSocket, donc aucune
  étape de création de session manuelle n'est nécessaire.
- Le niveau gratuit permet une session simultanée et une heure de navigateur par mois.
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

Valeurs par défaut :

- Le profil `openclaw` est créé automatiquement s'il manque.
- Le profil `chrome` est intégré pour le relais d'extension Chrome (pointe vers `http://127.0.0.1:18792` par défaut).
- Les ports CDP locaux s'attribuent à partir de **18800–18899** par défaut.
- La suppression d'un profil déplace son répertoire de données local à la Corbeille.

Tous les points de terminaison de contrôle acceptent `?profile=<name>` ; la CLI utilise `--browser-profile`.

## Relais d'extension Chrome (utilisez votre Chrome existant)

OpenClaw peut également piloter **vos onglets Chrome existants** (aucune instance Chrome « openclaw » séparée) via un relais CDP local + une extension Chrome.

Guide complet : [Chrome extension](/tools/chrome-extension)

Flux :

- La Gateway s'exécute localement (même machine) ou un hôte de nœud s'exécute sur la machine du navigateur.
- Un **serveur relais** local écoute sur un `cdpUrl` loopback (par défaut : `http://127.0.0.1:18792`).
- Vous cliquez sur l'icône de l'extension **OpenClaw Browser Relay** sur un onglet pour l'attacher (elle ne s'attache pas automatiquement).
- L'agent contrôle cet onglet via l'outil `browser` normal, en sélectionnant le bon profil.

Si la Gateway s'exécute ailleurs, exécutez un hôte de nœ
