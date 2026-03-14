---
read_when:
  - Appairage ou reconnexion d'un nœud iOS
  - Exécution de l'application iOS à partir des sources
  - Débogage de la découverte Gateway ou des commandes canvas
summary: Application iOS nœud : connexion à Gateway, appairage, canvas et dépannage
title: Application iOS
x-i18n:
  generated_at: "2026-02-03T07:52:17Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 692eebdc82e4bb8dc221bcbabf6a344a861a839fc377f1aeeb6eecaa4917a232
  source_path: platforms/ios.md
  workflow: 15
---

# Application iOS (Nœud)

Disponibilité : aperçu interne. L'application iOS n'est pas encore distribuée publiquement.

## Fonctionnalités

- Connexion à Gateway via WebSocket (LAN ou tailnet).
- Exposition des capacités du nœud : Canvas, capture d'écran, capture caméra, localisation, mode conversation, activation vocale.
- Réception des commandes `node.invoke` et signalement des événements d'état du nœud.

## Exigences

- Gateway s'exécute sur un autre appareil (macOS, Linux ou Windows via WSL2).
- Chemins réseau :
  - Même LAN via Bonjour, **ou**
  - Tailnet via DNS-SD unicast (domaine exemple : `openclaw.internal.`), **ou**
  - Hôte/port manuel (alternative).

## Démarrage rapide (appairage + connexion)

1. Démarrez Gateway :

```bash
openclaw gateway --port 18789
```

2. Dans l'application iOS, ouvrez les paramètres et sélectionnez une Gateway découverte (ou activez l'hôte manuel et entrez l'hôte/port).

3. Sur l'hôte Gateway, approuvez la demande d'appairage :

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

4. Vérifiez la connexion :

```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

## Chemins de découverte

### Bonjour (LAN)

Gateway diffuse `_openclaw-gw._tcp` sur `local.`. L'application iOS les énumère automatiquement.

### Tailnet (inter-réseaux)

Si mDNS est bloqué, utilisez une zone DNS-SD unicast (choisissez un domaine ; exemple : `openclaw.internal.`) et le DNS fractionné Tailscale.
Voir [Bonjour](/gateway/bonjour) pour un exemple CoreDNS.

### Hôte/port manuel

Dans les paramètres, activez **Hôte manuel** et entrez l'hôte Gateway + port (par défaut `18789`).

## Canvas + A2UI

Le nœud iOS rend un canvas WKWebView. Utilisez `node.invoke` pour le piloter :

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18793/__openclaw__/canvas/"}'
```

Remarques :

- Gateway sert le canvas sur `/__openclaw__/canvas/` et `/__openclaw__/a2ui/`.
- Quand l'URL du canvas est diffusée, le nœud iOS navigue automatiquement vers A2UI à la connexion.
- Utilisez `canvas.navigate` avec `{"url":""}` pour revenir à l'échafaudage intégré.

### Canvas eval / snapshot

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"(() => { const {ctx} = window.__openclaw; ctx.clearRect(0,0,innerWidth,innerHeight); ctx.lineWidth=6; ctx.strokeStyle=\"#ff2d55\"; ctx.beginPath(); ctx.moveTo(40,40); ctx.lineTo(innerWidth-40, innerHeight-40); ctx.stroke(); return \"ok\"; })()"}'
```

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'
```

## Activation vocale + mode conversation

- L'activation vocale et le mode conversation sont disponibles dans les paramètres.
- iOS peut suspendre l'audio en arrière-plan ; considérez les fonctionnalités vocales comme au mieux quand l'application n'est pas active.

## Erreurs courantes

- `NODE_BACKGROUND_UNAVAILABLE` : mettez l'application iOS au premier plan (les commandes canvas/caméra/écran l'exigent).
- `A2UI_HOST_NOT_CONFIGURED` : Gateway ne diffuse pas l'URL du canvas ; vérifiez `canvasHost` dans la [configuration Gateway](/gateway/configuration).
- L'invite d'appairage n'apparaît jamais : exécutez `openclaw nodes pending` et approuvez manuellement.
- La reconnexion échoue après réinstallation : le jeton d'appairage du trousseau a été effacé ; réappairiez le nœud.

## Documentation connexe

- [Appairage](/gateway/pairing)
- [Découverte d'appareils](/gateway/discovery)
- [Bonjour](/gateway/bonjour)
