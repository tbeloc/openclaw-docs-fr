---
summary: "Intégration de Tailscale Serve/Funnel pour le tableau de bord de la passerelle"
read_when:
  - Exposing the Gateway Control UI outside localhost
  - Automating tailnet or public dashboard access
title: "Tailscale"
---

# Tailscale (tableau de bord de la passerelle)

OpenClaw peut configurer automatiquement Tailscale **Serve** (tailnet) ou **Funnel** (public) pour le
tableau de bord de la passerelle et le port WebSocket. Cela maintient la passerelle liée à loopback tandis que
Tailscale fournit HTTPS, le routage et (pour Serve) les en-têtes d'identité.

## Modes

- `serve` : Serve tailnet uniquement via `tailscale serve`. La passerelle reste sur `127.0.0.1`.
- `funnel` : HTTPS public via `tailscale funnel`. OpenClaw nécessite un mot de passe partagé.
- `off` : Par défaut (pas d'automatisation Tailscale).

## Authentification

Définissez `gateway.auth.mode` pour contrôler la négociation :

- `token` (par défaut quand `OPENCLAW_GATEWAY_TOKEN` est défini)
- `password` (secret partagé via `OPENCLAW_GATEWAY_PASSWORD` ou config)

Quand `tailscale.mode = "serve"` et `gateway.auth.allowTailscale` est `true`,
l'authentification de l'interface utilisateur de contrôle/WebSocket peut utiliser les en-têtes d'identité Tailscale
(`tailscale-user-login`) sans fournir de token/mot de passe. OpenClaw vérifie
l'identité en résolvant l'adresse `x-forwarded-for` via le démon Tailscale local
(`tailscale whois`) et en la comparant à l'en-tête avant de l'accepter.
OpenClaw ne traite une requête comme Serve que si elle provient de loopback avec
les en-têtes `x-forwarded-for`, `x-forwarded-proto` et `x-forwarded-host` de Tailscale.
Les points de terminaison de l'API HTTP (par exemple `/v1/*`, `/tools/invoke` et `/api/channels/*`)
nécessitent toujours une authentification par token/mot de passe.
Ce flux sans token suppose que l'hôte de la passerelle est de confiance. Si du code local non fiable
peut s'exécuter sur le même hôte, désactivez `gateway.auth.allowTailscale` et exigez
plutôt une authentification par token/mot de passe.
Pour exiger des identifiants explicites, définissez `gateway.auth.allowTailscale: false` ou
forcez `gateway.auth.mode: "password"`.

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

Ouvrir : `https://<magicdns>/` (ou votre `gateway.controlUi.basePath` configuré)

### Tailnet uniquement (liaison à l'adresse IP Tailnet)

Utilisez ceci quand vous voulez que la passerelle écoute directement sur l'adresse IP Tailnet (pas de Serve/Funnel).

```json5
{
  gateway: {
    bind: "tailnet",
    auth: { mode: "token", token: "your-token" },
  },
}
```

Connectez-vous depuis un autre appareil Tailnet :

- Interface utilisateur de contrôle : `http://<tailscale-ip>:18789/`
- WebSocket : `ws://<tailscale-ip>:18789`

Remarque : loopback (`http://127.0.0.1:18789`) ne fonctionnera **pas** dans ce mode.

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

Préférez `OPENCLAW_GATEWAY_PASSWORD` plutôt que de valider un mot de passe sur disque.

## Exemples CLI

```bash
openclaw gateway --tailscale serve
openclaw gateway --tailscale funnel --auth password
```

## Remarques

- Tailscale Serve/Funnel nécessite que l'interface CLI `tailscale` soit installée et connectée.
- `tailscale.mode: "funnel"` refuse de démarrer à moins que le mode d'authentification soit `password` pour éviter une exposition publique.
- Définissez `gateway.tailscale.resetOnExit` si vous voulez qu'OpenClaw annule la configuration `tailscale serve`
  ou `tailscale funnel` à l'arrêt.
- `gateway.bind: "tailnet"` est une liaison Tailnet directe (pas HTTPS, pas Serve/Funnel).
- `gateway.bind: "auto"` préfère loopback ; utilisez `tailnet` si vous voulez Tailnet uniquement.
- Serve/Funnel exposent uniquement l'**interface utilisateur de contrôle de la passerelle + WS**. Les nœuds se connectent via
  le même point de terminaison WS de la passerelle, donc Serve peut fonctionner pour l'accès aux nœuds.

## Contrôle du navigateur (passerelle distante + navigateur local)

Si vous exécutez la passerelle sur une machine mais que vous voulez piloter un navigateur sur une autre machine,
exécutez un **hôte de nœud** sur la machine du navigateur et gardez les deux sur le même tailnet.
La passerelle proxiera les actions du navigateur vers le nœud ; aucun serveur de contrôle séparé ou URL Serve nécessaire.

Évitez Funnel pour le contrôle du navigateur ; traitez l'appairage des nœuds comme un accès opérateur.

## Prérequis et limites de Tailscale

- Serve nécessite HTTPS activé pour votre tailnet ; l'interface CLI vous le signale s'il manque.
- Serve injecte les en-têtes d'identité Tailscale ; Funnel ne le fait pas.
- Funnel nécessite Tailscale v1.38.3+, MagicDNS, HTTPS activé et un attribut de nœud funnel.
- Funnel ne supporte que les ports `443`, `8443` et `10000` sur TLS.
- Funnel sur macOS nécessite la variante d'application Tailscale open-source.

## En savoir plus

- Aperçu de Tailscale Serve : [https://tailscale.com/kb/1312/serve](https://tailscale.com/kb/1312/serve)
- Commande `tailscale serve` : [https://tailscale.com/kb/1242/tailscale-serve](https://tailscale.com/kb/1242/tailscale-serve)
- Aperçu de Tailscale Funnel : [https://tailscale.com/kb/1223/tailscale-funnel](https://tailscale.com/kb/1223/tailscale-funnel)
- Commande `tailscale funnel` : [https://tailscale.com/kb/1311/tailscale-funnel](https://tailscale.com/kb/1311/tailscale-funnel)
