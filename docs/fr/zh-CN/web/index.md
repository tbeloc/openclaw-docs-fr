---
read_when:
  - 你想通过 Tailscale 访问 Gateway 网关
  - 你想使用浏览器 Control UI 和配置编辑
summary: Gateway 网关 Web 界面：Control UI、绑定模式和安全
title: Web
x-i18n:
  generated_at: "2026-02-03T10:13:29Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 4da8bc9831018c482ac918a759b9739f75ca130f70993f81911818bc60a685d1
  source_path: web/index.md
  workflow: 15
---

# Web (Passerelle Gateway)

La passerelle Gateway fournit une petite **interface Control UI de navigateur** (Vite + Lit) sur le même port que la WebSocket de la passerelle Gateway :

- Par défaut : `http://<host>:18789/`
- Préfixe optionnel : définissez `gateway.controlUi.basePath` (par exemple `/openclaw`)

Pour plus de détails sur les fonctionnalités, consultez [Control UI](/web/control-ui).
Cette page met l'accent sur les modes de liaison, la sécurité et les interfaces orientées Web.

## Webhooks

Lorsque `hooks.enabled=true`, la passerelle Gateway expose également un petit point de terminaison webhook sur le même serveur HTTP.
Consultez [Configuration de la passerelle Gateway](/gateway/configuration) → `hooks` pour l'authentification + la charge utile.

## Configuration (activée par défaut)

Lorsque la ressource existe (`dist/control-ui`), Control UI est **activée par défaut**.
Vous pouvez la contrôler via la configuration :

```json5
{
  gateway: {
    controlUi: { enabled: true, basePath: "/openclaw" }, // basePath optionnel
  },
}
```

## Accès Tailscale

### Intégration Serve (recommandée)

Gardez la passerelle Gateway sur la boucle locale et laissez Tailscale Serve la servir en proxy :

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

Ensuite, démarrez la passerelle Gateway :

```bash
openclaw gateway
```

Ouvrez :

- `https://<magicdns>/` (ou votre `gateway.controlUi.basePath` configuré)

### Liaison Tailnet + Jeton

```json5
{
  gateway: {
    bind: "tailnet",
    controlUi: { enabled: true },
    auth: { mode: "token", token: "your-token" },
  },
}
```

Ensuite, démarrez la passerelle Gateway (les liaisons non-loopback nécessitent un jeton) :

```bash
openclaw gateway
```

Ouvrez :

- `http://<tailscale-ip>:18789/` (ou votre `gateway.controlUi.basePath` configuré)

### Internet public (Funnel)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password" }, // ou OPENCLAW_GATEWAY_PASSWORD
  },
}
```

## Considérations de sécurité

- L'authentification de la passerelle Gateway est requise par défaut (jeton/mot de passe ou en-tête d'identité Tailscale).
- Les liaisons non-loopback **nécessitent toujours** un jeton/mot de passe partagé (`gateway.auth` ou variable d'environnement).
- L'assistant génère par défaut un jeton de passerelle Gateway (même sur la boucle locale).
- L'interface utilisateur envoie `connect.params.auth.token` ou `connect.params.auth.password`.
- Lors de l'utilisation de Serve, l'en-tête d'identité Tailscale peut satisfaire l'authentification lorsque `gateway.auth.allowTailscale` est `true` (sans jeton/mot de passe). Définissez `gateway.auth.allowTailscale: false` pour exiger des identifiants explicites. Consultez [Tailscale](/gateway/tailscale) et [Sécurité](/gateway/security).
- `gateway.tailscale.mode: "funnel"` nécessite `gateway.auth.mode: "password"` (mot de passe partagé).

## Construire l'interface utilisateur

La passerelle Gateway fournit des fichiers statiques à partir de `dist/control-ui`. Construisez-les avec :

```bash
pnpm ui:build # Installe automatiquement les dépendances de l'interface utilisateur à la première exécution
```
