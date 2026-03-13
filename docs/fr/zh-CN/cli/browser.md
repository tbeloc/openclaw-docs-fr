---
read_when:
  - 你使用 `openclaw browser` 并想要常见任务的示例
  - 你想通过 node host 控制在另一台机器上运行的浏览器
  - 你想使用 Chrome 扩展中继（通过工具栏按钮附加/分离）
summary: "`openclaw browser` 的 CLI 参考（配置文件、标签页、操作、扩展中继）"
title: browser
x-i18n:
  generated_at: "2026-02-03T07:44:49Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: af35adfd68726fd519c704d046451effd330458c2b8305e713137fb07b2571fd
  source_path: cli/browser.md
  workflow: 15
---

# `openclaw browser`

Gérez le serveur de contrôle de navigateur d'OpenClaw et exécutez des opérations de navigateur (onglets, snapshots, captures d'écran, navigation, clics, saisie).

Connexes :

- Outils de navigateur + API : [Outils de navigateur](/tools/browser)
- Relais d'extension Chrome : [Extension Chrome](/tools/chrome-extension)

## Drapeaux généraux

- `--url <gatewayWsUrl>` : URL WebSocket de la passerelle Gateway (par défaut depuis la configuration).
- `--token <token>` : Jeton de la passerelle Gateway (si nécessaire).
- `--timeout <ms>` : Délai d'expiration de la requête (millisecondes).
- `--browser-profile <name>` : Sélectionnez un profil de navigateur (par défaut depuis la configuration).
- `--json` : Sortie lisible par machine (où supporté).

## Démarrage rapide (local)

```bash
openclaw browser --browser-profile chrome tabs
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

## Profils de configuration

Les profils de configuration sont des configurations de routage de navigateur nommées. En pratique :

- `openclaw` : Démarrer/attacher à une instance Chrome dédiée gérée par OpenClaw (répertoire de données utilisateur isolé).
- `chrome` : Contrôlez vos onglets Chrome existants via le relais d'extension Chrome.

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

## Snapshots / Captures d'écran / Opérations

Snapshot :

```bash
openclaw browser snapshot
```

Capture d'écran :

```bash
openclaw browser screenshot
```

Navigation/clics/saisie (automatisation d'interface utilisateur basée sur ref) :

```bash
openclaw browser navigate https://example.com
openclaw browser click <ref>
openclaw browser type <ref> "hello"
```

## Relais d'extension Chrome (attachement via bouton de barre d'outils)

Ce mode permet à l'agent de contrôler les onglets Chrome existants que vous attachez manuellement (pas d'attachement automatique).

Installez l'extension non empaquetée dans un chemin stable :

```bash
openclaw browser extension install
openclaw browser extension path
```

Ensuite Chrome → `chrome://extensions` → Activez le "Mode développeur" → "Charger l'extension non empaquetée" → Sélectionnez le dossier imprimé.

Guide complet : [Extension Chrome](/tools/chrome-extension)

## Contrôle de navigateur distant (proxy node host)

Si la passerelle Gateway et le navigateur s'exécutent sur des machines différentes, exécutez **node host** sur la machine avec Chrome/Brave/Edge/Chromium. La passerelle Gateway proxiera les opérations de navigateur vers ce nœud (pas besoin de serveur de contrôle de navigateur séparé).

Utilisez `gateway.nodes.browser.mode` pour contrôler le routage automatique, et `gateway.nodes.browser.node` pour épingler un nœud spécifique lors de la connexion de plusieurs nœuds.

Configuration sécurisée + distante : [Outils de navigateur](/tools/browser), [Accès distant](/gateway/remote), [Tailscale](/gateway/tailscale), [Sécurité](/gateway/security)
