---
summary: "Référence CLI pour `openclaw browser` (profils, onglets, actions, relais d'extension)"
read_when:
  - You use `openclaw browser` and want examples for common tasks
  - You want to control a browser running on another machine via a node host
  - You want to use the Chrome extension relay (attach/detach via toolbar button)
title: "browser"
---

# `openclaw browser`

Gérez le serveur de contrôle de navigateur d'OpenClaw et exécutez des actions de navigateur (onglets, snapshots, captures d'écran, navigation, clics, saisie).

Connexes :

- Outil navigateur + API : [Outil navigateur](/tools/browser)
- Relais d'extension Chrome : [Extension Chrome](/tools/chrome-extension)

## Drapeaux courants

- `--url <gatewayWsUrl>` : URL WebSocket de la passerelle (par défaut depuis la config).
- `--token <token>` : Jeton de passerelle (si requis).
- `--timeout <ms>` : délai d'expiration de la requête (ms).
- `--browser-profile <name>` : choisir un profil de navigateur (par défaut depuis la config).
- `--json` : sortie lisible par machine (où supporté).

## Démarrage rapide (local)

```bash
openclaw browser profiles
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

## Profils

Les profils sont des configurations de routage de navigateur nommées. En pratique :

- `openclaw` : lance/s'attache à une instance Chrome dédiée gérée par OpenClaw (répertoire de données utilisateur isolé).
- `user` : contrôle votre session Chrome existante signée via Chrome DevTools MCP.
- `chrome-relay` : contrôle vos onglet(s) Chrome existant(s) via le relais d'extension Chrome.

```bash
openclaw browser profiles
openclaw browser create-profile --name work --color "#FF5A36"
openclaw browser delete-profile --name work
```

Utiliser un profil spécifique :

```bash
openclaw browser --browser-profile work tabs
```

## Onglets

```bash
openclaw browser tabs
openclaw browser open https://docs.openclaw.ai
openclaw browser focus <targetId>
openclaw browser close <targetId>
```

## Snapshot / capture d'écran / actions

Snapshot :

```bash
openclaw browser snapshot
```

Capture d'écran :

```bash
openclaw browser screenshot
```

Navigation/clic/saisie (automatisation UI basée sur les références) :

```bash
openclaw browser navigate https://example.com
openclaw browser click <ref>
openclaw browser type <ref> "hello"
```

## Relais d'extension Chrome (attacher via le bouton de la barre d'outils)

Ce mode permet à l'agent de contrôler un onglet Chrome existant que vous attachez manuellement (il ne s'attache pas automatiquement).

Installez l'extension décompressée dans un chemin stable :

```bash
openclaw browser extension install
openclaw browser extension path
```

Ensuite Chrome → `chrome://extensions` → activez le « Mode développeur » → « Charger l'extension non empaquetée » → sélectionnez le dossier affiché.

Guide complet : [Extension Chrome](/tools/chrome-extension)

## Contrôle de navigateur distant (proxy d'hôte nœud)

Si la passerelle s'exécute sur une machine différente de celle du navigateur, exécutez un **hôte nœud** sur la machine qui a Chrome/Brave/Edge/Chromium. La passerelle proxiera les actions du navigateur vers ce nœud (aucun serveur de contrôle de navigateur séparé requis).

Utilisez `gateway.nodes.browser.mode` pour contrôler le routage automatique et `gateway.nodes.browser.node` pour épingler un nœud spécifique si plusieurs sont connectés.

Sécurité + configuration distante : [Outil navigateur](/tools/browser), [Accès distant](/gateway/remote), [Tailscale](/gateway/tailscale), [Sécurité](/gateway/security)
