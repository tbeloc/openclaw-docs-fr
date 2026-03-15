---
summary: "Surfaces web de la passerelle : Interface utilisateur de contrôle, modes de liaison et sécurité"
read_when:
  - You want to access the Gateway over Tailscale
  - You want the browser Control UI and config editing
title: "Web"
---

# Web (Gateway)

La passerelle sert une petite **interface utilisateur de contrôle navigateur** (Vite + Lit) depuis le même port que la WebSocket de la passerelle :

- par défaut : `http://<host>:18789/`
- préfixe optionnel : définir `gateway.controlUi.basePath` (par exemple `/openclaw`)

Les capacités se trouvent dans [Control UI](/fr/web/control-ui).
Cette page se concentre sur les modes de liaison, la sécurité et les surfaces exposées au web.

## Webhooks

Quand `hooks.enabled=true`, la passerelle expose également un petit point de terminaison webhook sur le même serveur HTTP.
Voir [Configuration de la passerelle](/fr/gateway/configuration) → `hooks` pour l'authentification + les charges utiles.

## Config (activée par défaut)

L'interface utilisateur de contrôle est **activée par défaut** quand les ressources sont présentes (`dist/control-ui`).
Vous pouvez la contrôler via la configuration :

```json5
{
  gateway: {
    controlUi: { enabled: true, basePath: "/openclaw" }, // basePath optionnel
  },
}
```

## Accès Tailscale

### Serve intégré (recommandé)

Gardez la passerelle sur loopback et laissez Tailscale Serve la proxifier :

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

Ensuite, démarrez la passerelle :

```bash
openclaw gateway
```

Ouvrez :

- `https://<magicdns>/` (ou votre `gateway.controlUi.basePath` configuré)

### Liaison tailnet + token

```json5
{
  gateway: {
    bind: "tailnet",
    controlUi: { enabled: true },
    auth: { mode: "token", token: "your-token" },
  },
}
```

Ensuite, démarrez la passerelle (token requis pour les liaisons non-loopback) :

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

## Notes de sécurité

- L'authentification de la passerelle est requise par défaut (token/mot de passe ou en-têtes d'identité Tailscale).
- Les liaisons non-loopback **nécessitent toujours** un token/mot de passe partagé (`gateway.auth` ou env).
- L'assistant génère un token de passerelle par défaut (même sur loopback).
- L'interface utilisateur envoie `connect.params.auth.token` ou `connect.params.auth.password`.
- Pour les déploiements d'interface utilisateur de contrôle non-loopback, définissez `gateway.controlUi.allowedOrigins`
  explicitement (origines complètes). Sans cela, le démarrage de la passerelle est refusé par défaut.
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` active
  le mode de secours d'origine basé sur l'en-tête Host, mais c'est une dégradation de sécurité dangereuse.
- Avec Serve, les en-têtes d'identité Tailscale peuvent satisfaire l'authentification de l'interface utilisateur de contrôle/WebSocket
  quand `gateway.auth.allowTailscale` est `true` (aucun token/mot de passe requis).
  Les points de terminaison de l'API HTTP nécessitent toujours un token/mot de passe. Définissez
  `gateway.auth.allowTailscale: false` pour exiger des identifiants explicites. Voir
  [Tailscale](/fr/gateway/tailscale) et [Sécurité](/fr/gateway/security). Ce
  flux sans token suppose que l'hôte de la passerelle est de confiance.
- `gateway.tailscale.mode: "funnel"` nécessite `gateway.auth.mode: "password"` (mot de passe partagé).

## Construire l'interface utilisateur

La passerelle sert des fichiers statiques depuis `dist/control-ui`. Construisez-les avec :

```bash
pnpm ui:build # installe automatiquement les dépendances de l'interface utilisateur à la première exécution
```
