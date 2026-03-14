---
read_when:
  - Ajouter l'automatisation de navigateur contrôlée par agent
  - Déboguer les problèmes d'openclaw qui interfèrent avec votre propre Chrome
  - Implémenter la gestion des paramètres et du cycle de vie du navigateur dans les applications macOS
summary: Intégrer le service de contrôle du navigateur + commandes d'action
title: Navigateur (OpenClaw géré)
x-i18n:
  generated_at: "2026-02-03T09:26:06Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a868d040183436a1fb355130995e79782cb817b5ea298beaf1e1d2cb82e21c4c
  source_path: tools/browser.md
  workflow: 15
---

# Navigateur (openclaw géré)

OpenClaw peut exécuter un **profil Chrome/Brave/Edge/Chromium dédié contrôlé par agent**.
Il est isolé de votre navigateur personnel et géré via un petit service de contrôle local à l'intérieur de la passerelle Gateway (loopback uniquement).

Perspective débutant :

- Pensez-y comme un **navigateur indépendant, réservé aux agents**.
- Le profil `openclaw` **ne touchera pas** à votre profil de navigateur personnel.
- Les agents peuvent **ouvrir des onglets, lire des pages, cliquer et taper** dans un canal sécurisé.
- Le profil `chrome` par défaut utilise le **navigateur Chromium par défaut du système** via un relais d'extension ; basculer vers `openclaw` utilise le navigateur géré isolé.

## Aperçu des fonctionnalités

- Un profil de navigateur indépendant nommé **openclaw** (thème orange par défaut).
- Contrôle d'onglets déterministe (lister/ouvrir/mettre au point/fermer).
- Actions d'agent (cliquer/taper/glisser/sélectionner), snapshots, captures d'écran, PDF.
- Support multi-profils optionnel (`openclaw`, `work`, `remote`, etc.).

Ce navigateur **n'est pas** votre navigateur quotidien. C'est une interface sécurisée et isolée pour l'automatisation et la vérification par agent.

## Démarrage rapide

```bash
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

Si vous voyez "Browser disabled", activez-le dans la configuration (voir ci-dessous) et redémarrez la passerelle Gateway.

## Profils : `openclaw` vs `chrome`

- `openclaw` : navigateur géré isolé (pas d'extension requise).
- `chrome` : relais d'extension vers votre **navigateur système** (nécessite d'attacher l'extension OpenClaw aux onglets).

Si vous souhaitez utiliser le mode géré par défaut, définissez `browser.defaultProfile: "openclaw"`.

## Configuration

Les paramètres du navigateur se trouvent dans `~/.openclaw/openclaw.json`.

```json5
{
  browser: {
    enabled: true, // default: true
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

- Le service de contrôle du navigateur se lie à un port sur loopback, dérivé de `gateway.port` (par défaut : `18791`, soit gateway + 2). Le relais utilise le port suivant (`18792`).
- Si vous remplacez le port de la passerelle Gateway (`gateway.port` ou `OPENCLAW_GATEWAY_PORT`), les ports de navigateur dérivés s'ajustent en conséquence pour rester dans la même « famille ».
- `cdpUrl` par défaut au port relais quand non défini.
- `remoteCdpTimeoutMs` s'applique aux vérifications de disponibilité CDP distantes (non-loopback).
- `remoteCdpHandshakeTimeoutMs` s'applique aux vérifications de disponibilité WebSocket CDP distantes.
- `attachOnly: true` signifie « ne jamais lancer le navigateur local ; attacher uniquement si le navigateur est déjà en cours d'exécution ».
- `color` + `color` par profil colore l'interface utilisateur du navigateur pour que vous puissiez voir quel profil est actif.
- Le profil par défaut est `chrome` (relais d'extension). Utilisez `defaultProfile: "openclaw"` pour utiliser le navigateur géré.
- Ordre de détection automatique : si le navigateur par défaut du système est basé sur Chromium, l'utiliser ; sinon Chrome → Brave → Edge → Chromium → Chrome Canary.
- Le profil `openclaw` local se voit automatiquement attribuer `cdpPort`/`cdpUrl` — définissez-les uniquement pour CDP distant.

## Utiliser Brave (ou un autre navigateur basé sur Chromium)

Si votre navigateur **par défaut du système** est basé sur Chromium (Chrome/Brave/Edge, etc.), OpenClaw l'utilisera automatiquement. Définissez `browser.executablePath` pour remplacer la détection automatique :

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

## Contrôle local vs contrôle distant

- **Contrôle local (par défaut) :** la passerelle Gateway lance un service de contrôle loopback et peut lancer un navigateur local.
- **Contrôle distant (hôte nœud) :** exécutez l'hôte nœud sur la machine avec le navigateur ; la passerelle Gateway proxy les opérations de navigateur vers ce nœud.
- **CDP distant :** définissez `browser.profiles.<name>.cdpUrl` (ou `browser.cdpUrl`) pour vous attacher à un navigateur basé sur Chromium distant. Dans ce cas, OpenClaw ne lancera pas de navigateur local.

Les URL CDP distantes peuvent contenir des informations d'authentification :

- Jeton de requête (par exemple `https://provider.example?token=<token>`)
- Authentification HTTP Basic (par exemple `https://user:pass@provider.example`)

OpenClaw préserve les informations d'authentification lors de l'appel des points de terminaison `/json/*` et de la connexion au WebSocket CDP. Il est recommandé d'utiliser des variables d'environnement ou un gestionnaire de secrets pour stocker les jetons plutôt que de les valider dans la configuration.

## Proxy de navigateur de nœud (zéro configuration par défaut)

Si vous exécutez un **hôte nœud** sur une machine avec un navigateur, OpenClaw peut automatiquement router les appels d'outils de navigateur vers ce nœud, sans configuration de navigateur supplémentaire. C'est le chemin par défaut pour une passerelle Gateway distante.

Notes :

- L'hôte nœud expose son serveur de contrôle de navigateur local via des **commandes proxy**.
- Les profils proviennent de la propre configuration `browser.profiles` du nœud (identique au local).
- Peut être désactivé si non nécessaire :
  - Sur le nœud : `nodeHost.browserProxy.enabled=false`
  - Sur la passerelle Gateway : `gateway.nodes.browser.mode="off"`

## Browserless (CDP distant géré)

[Browserless](https://browserless.io) est un service Chromium géré qui expose les points de terminaison CDP via HTTPS. Vous pouvez pointer un profil de navigateur OpenClaw vers un point de terminaison de région Browserless et vous authentifier avec votre clé API.

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
- Choisissez le point de terminaison de région qui correspond à votre compte Browserless (voir sa documentation).

## Sécurité

Idée centrale :

- Le contrôle du navigateur est limité à loopback ; l'accès est via l'authentification de la passerelle Gateway ou l'appairage de nœud.
- Gardez la passerelle Gateway et tout hôte nœud sur un réseau privé (Tailscale) ; évitez d'exposer publiquement.
- Traitez les URL/jetons CDP distants comme des secrets ; préférez les variables d'environnement ou les gestionnaires de secrets.

Conseils CDP distant :

- Utilisez des points de terminaison HTTPS et des jetons de courte durée autant que possible.
- Évitez d'intégrer directement les jetons de longue durée dans la configuration.

## Profils (navigateur multiple)

OpenClaw prend en charge plusieurs profils nommés (configurations de routage). Les profils peuvent être :

- **openclaw géré** : instance de navigateur basée sur Chromium dédiée avec répertoire de données utilisateur indépendant et port CDP
- **distant** : URL CDP explicite (navigateur basé sur Chromium exécuté ailleurs)
- **relais d'extension** : accès à vos onglets Chrome existants via relais local + extension Chrome

Valeurs par défaut :

- Si le profil `openclaw` est manquant, il est créé automatiquement.
- Le profil `chrome` est intégré pour le relais d'extension Chrome (pointe par défaut vers `http://127.0.0.1:18792`).
- Les ports CDP locaux sont attribués par défaut à partir de **18800–18899**.
- La suppression d'un profil déplace son répertoire de données local vers la corbeille.

Tous les points de terminaison de contrôle acceptent `?profile=<name>` ; la CLI utilise `--browser-profile`.

## Relais d'extension Chrome (utiliser votre Chrome existant)

OpenClaw peut également piloter **vos onglets Chrome existants** via un relais CDP local + extension Chrome (sans instance Chrome « openclaw » séparée).

Guide complet : [Extension Chrome](/tools/chrome-extension)

Flux :

- La passerelle Gateway s'exécute localement (même machine) ou l'hôte nœud s'exécute sur la machine avec le navigateur.
- Un **serveur relais** local écoute sur `cdpUrl` sur loopback (par défaut : `http://127.0.0.1:18792`).
- Vous cliquez sur l'icône de l'extension **OpenClaw Browser Relay** sur un onglet pour l'attacher (elle ne s'attache pas automatiquement).
- Les agents contrôlent cet onglet en utilisant l'outil `browser` normal en sélectionnant le bon profil.

Si la passerelle Gateway s'exécute ailleurs, exécutez l'hôte nœud sur la machine avec le navigateur pour que la passerelle Gateway puisse proxy les opérations de navigateur.

### Sessions en bac à sable

Si la session d'agent est isolée en bac à sable, l'outil `browser` peut par défaut utiliser `target="sandbox"` (navigateur en bac à sable).
Le relais d'extension Chrome nécessite le contrôle du navigateur hôte, donc soit :

- Exécutez la session en mode non-bac à sable, ou
- Définissez `agents.defaults.sandbox.browser.allowHostControl: true` et utilisez `target="host"` lors de l'appel de l'outil.

### Configuration

1. Chargez l'extension (développement/non emballée) :

```bash
openclaw browser extension install
```

- Chrome → `chrome://extensions` → Activez le « Mode développeur »
- « Charger l'extension non emballée » → Sélectionnez le répertoire imprimé par `openclaw browser extension path`
- Épinglez l'extension, puis cliquez dessus sur l'onglet que vous souhaitez contrôler (le badge affiche `ON`).

2. Utilisez-la :

- CLI : `openclaw browser --browser-profile chrome tabs`
- Outil d'agent : `browser` avec `profile="chrome"`

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
- Cliquez à nouveau sur l'icône de l'extension pour détacher.

## Garanties d'isolation

- **Répertoire de données utilisateur dédié** : ne touche jamais à votre profil de navigateur personnel.
- **Port dédié** : évite d'utiliser `9222` pour éviter les conflits avec les flux de travail de développement.
- **Contrôle d'onglets déterministe** : localise les onglets par `targetId`, pas « le dernier onglet ».

## Sélection du navigateur

Au lancement local, OpenClaw choisit le premier disponible :

1. Chrome
2. Brave
3. Edge
4. Chromium
5. Chrome Canary

Vous pouvez remplacer avec `browser.executablePath`.

Plates-formes :

- macOS : vérifie `/Applications` et `~/Applications`.
- Linux : recherche `google-chrome`, `brave`, `microsoft-edge`, `chromium`, etc.
- Windows : vérif
