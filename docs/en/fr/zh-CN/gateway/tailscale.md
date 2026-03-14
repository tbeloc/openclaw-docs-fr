```markdown
---
read_when:
  - Exposer l'interface de contrôle Gateway en dehors de localhost
  - Automatiser l'accès au tailnet ou au tableau de bord public
summary: Intégrer Tailscale Serve/Funnel pour le tableau de bord Gateway
title: Tailscale
x-i18n:
  generated_at: "2026-02-03T07:49:04Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: c900c70a9301f2909a3a29a6fb0e6edfc8c18dba443f2e71b9cfadbc58167911
  source_path: gateway/tailscale.md
  workflow: 15
---

# Tailscale (Tableau de bord Gateway)

OpenClaw peut configurer automatiquement Tailscale **Serve** (tailnet) ou **Funnel** (public) pour le tableau de bord Gateway et le port WebSocket. Cela permet à Gateway de rester lié à loopback, tandis que Tailscale fournit HTTPS, le routage et (pour Serve) les en-têtes d'identité.

## Modes

- `serve` : Serve réservé au Tailnet, via `tailscale serve`. Gateway reste sur `127.0.0.1`.
- `funnel` : HTTPS public via `tailscale funnel`. OpenClaw nécessite un mot de passe partagé.
- `off` : Par défaut (pas d'automatisation Tailscale).

## Authentification

Définissez `gateway.auth.mode` pour contrôler la négociation :

- `token` (par défaut quand `OPENCLAW_GATEWAY_TOKEN` est défini)
- `password` (via `OPENCLAW_GATEWAY_PASSWORD` ou clé partagée configurée)

Quand `tailscale.mode = "serve"` et `gateway.auth.allowTailscale` est `true`,
les requêtes Serve valides peuvent être authentifiées via l'en-tête d'identité Tailscale (`tailscale-user-login`) sans fournir de jeton/mot de passe. OpenClaw vérifie l'identité en analysant l'adresse `x-forwarded-for` via le démon Tailscale local (`tailscale whois`) et en la faisant correspondre à l'en-tête, avant de l'accepter.
OpenClaw ne considère une requête comme une requête Serve que si elle arrive depuis loopback avec les en-têtes `x-forwarded-for`, `x-forwarded-proto` et `x-forwarded-host` de Tailscale.
Pour exiger des identifiants explicites, définissez `gateway.auth.allowTailscale: false` ou forcez `gateway.auth.mode: "password"`.

## Exemples de configuration

### Tailnet uniquement (Serve)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

Accédez à : `https://<magicdns>/` (ou votre `gateway.controlUi.basePath` configuré)

### Tailnet uniquement (lié à l'IP Tailnet)

Utilisez ceci quand vous voulez que Gateway écoute directement l'IP Tailnet (sans Serve/Funnel).

```json5
{
  gateway: {
    bind: "tailnet",
    auth: { mode: "token", token: "your-token" },
  },
}
```

Connectez-vous depuis un autre appareil Tailnet :

- Interface de contrôle : `http://<tailscale-ip>:18789/`
- WebSocket : `ws://<tailscale-ip>:18789`

Remarque : Dans ce mode, loopback (`http://127.0.0.1:18789`) ne fonctionnera **pas**.

### Internet public (Funnel + mot de passe partagé)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password", password: "replace-me" },
  },
}
```

Préférez `OPENCLAW_GATEWAY_PASSWORD` plutôt que de valider le mot de passe sur le disque.

## Exemples CLI

```bash
openclaw gateway --tailscale serve
openclaw gateway --tailscale funnel --auth password
```

## Remarques

- Tailscale Serve/Funnel nécessite l'installation et la connexion à la CLI `tailscale`.
- `tailscale.mode: "funnel"` refuse de démarrer sauf si le mode d'authentification est `password`, pour éviter une exposition publique.
- Si vous souhaitez qu'OpenClaw révoque la configuration `tailscale serve` ou `tailscale funnel` à l'arrêt, définissez `gateway.tailscale.resetOnExit`.
- `gateway.bind: "tailnet"` est une liaison Tailnet directe (pas HTTPS, pas Serve/Funnel).
- `gateway.bind: "auto"` privilégie loopback ; si vous voulez Tailnet uniquement, utilisez `tailnet`.
- Serve/Funnel expose uniquement **l'interface de contrôle Gateway + WS**. Les nœuds se connectent via le même point de terminaison Gateway WS, donc Serve peut être utilisé pour l'accès aux nœuds.

## Contrôle du navigateur (Gateway distant + navigateur local)

Si vous exécutez Gateway sur une machine mais souhaitez piloter le navigateur sur une autre,
exécutez un **hôte de nœud** sur la machine du navigateur et gardez les deux sur le même tailnet.
Gateway proxiera les opérations du navigateur vers le nœud ; aucun serveur de contrôle séparé ou URL Serve n'est nécessaire.

Évitez d'utiliser Funnel pour le contrôle du navigateur ; considérez l'appairage des nœuds comme un accès opérateur.

## Prérequis et limitations Tailscale

- Serve nécessite HTTPS activé pour votre tailnet ; si absent, la CLI vous le signalera.
- Serve injecte les en-têtes d'identité Tailscale ; Funnel ne le fait pas.
- Funnel nécessite Tailscale v1.38.3+, MagicDNS, HTTPS activé et propriété de nœud funnel.
- Funnel ne supporte que les ports `443`, `8443` et `10000` via TLS.
- Funnel sur macOS nécessite la variante d'application Tailscale open source.

## En savoir plus

- Aperçu de Tailscale Serve : https://tailscale.com/kb/1312/serve
- Commande `tailscale serve` : https://tailscale.com/kb/1242/tailscale-serve
- Aperçu de Tailscale Funnel : https://tailscale.com/kb/1223/tailscale-funnel
- Commande `tailscale funnel` : https://tailscale.com/kb/1311/tailscale-funnel
```
