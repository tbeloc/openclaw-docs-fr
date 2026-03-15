---
summary: "Application iOS : connexion à la Gateway, appairage, canvas et dépannage"
read_when:
  - Appairage ou reconnexion du nœud iOS
  - Exécution de l'application iOS à partir de la source
  - Débogage de la découverte de gateway ou des commandes canvas
title: "Application iOS"
---

# Application iOS (Nœud)

Disponibilité : aperçu interne. L'application iOS n'est pas encore distribuée publiquement.

## Ce qu'elle fait

- Se connecte à une Gateway via WebSocket (LAN ou tailnet).
- Expose les capacités du nœud : Canvas, Capture d'écran, Capture de caméra, Localisation, Mode conversation, Activation vocale.
- Reçoit les commandes `node.invoke` et signale les événements d'état du nœud.

## Prérequis

- Gateway en cours d'exécution sur un autre appareil (macOS, Linux ou Windows via WSL2).
- Chemin réseau :
  - Même LAN via Bonjour, **ou**
  - Tailnet via DNS-SD unicast (exemple de domaine : `openclaw.internal.`), **ou**
  - Hôte/port manuel (secours).

## Démarrage rapide (appairage + connexion)

1. Démarrez la Gateway :

```bash
openclaw gateway --port 18789
```

2. Dans l'application iOS, ouvrez Paramètres et sélectionnez une gateway découverte (ou activez Hôte manuel et entrez l'hôte/port).

3. Approuvez la demande d'appairage sur l'hôte de la gateway :

```bash
openclaw devices list
openclaw devices approve <requestId>
```

4. Vérifiez la connexion :

```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

## Push relayé pour les builds officiels

Les builds iOS officiels distribués utilisent le relais de push externe au lieu de publier le jeton APNs brut à la gateway.

Exigence côté Gateway :

```json5
{
  gateway: {
    push: {
      apns: {
        relay: {
          baseUrl: "https://relay.example.com",
        },
      },
    },
  },
}
```

Fonctionnement du flux :

- L'application iOS s'enregistre auprès du relais en utilisant App Attest et le reçu de l'application.
- Le relais retourne un handle de relais opaque plus une subvention d'envoi limitée à l'enregistrement.
- L'application iOS récupère l'identité de la gateway appairée et l'inclut dans l'enregistrement du relais, de sorte que l'enregistrement soutenu par le relais est délégué à cette gateway spécifique.
- L'application transmet cet enregistrement soutenu par le relais à la gateway appairée avec `push.apns.register`.
- La gateway utilise ce handle de relais stocké pour `push.test`, les réveils en arrière-plan et les nudges de réveil.
- L'URL de base du relais de la gateway doit correspondre à l'URL du relais intégrée dans le build iOS officiel/TestFlight.
- Si l'application se connecte ultérieurement à une gateway différente ou à un build avec une URL de base de relais différente, elle actualise l'enregistrement du relais au lieu de réutiliser l'ancienne liaison.

Ce que la gateway **n'a pas besoin** pour ce chemin :

- Pas de jeton de relais à l'échelle du déploiement.
- Pas de clé APNs directe pour les envois relayés officiels/TestFlight.

Flux opérateur attendu :

1. Installez le build iOS officiel/TestFlight.
2. Définissez `gateway.push.apns.relay.baseUrl` sur la gateway.
3. Appairez l'application à la gateway et laissez-la terminer la connexion.
4. L'application publie `push.apns.register` automatiquement après avoir un jeton APNs, la session opérateur connectée et l'enregistrement du relais réussi.
5. Après cela, `push.test`, les réveils de reconnexion et les nudges de réveil peuvent utiliser l'enregistrement soutenu par le relais stocké.

Note de compatibilité :

- `OPENCLAW_APNS_RELAY_BASE_URL` fonctionne toujours comme un remplacement d'env temporaire pour la gateway.

## Flux d'authentification et de confiance

Le relais existe pour appliquer deux contraintes que les APNs directs sur gateway ne peuvent pas fournir pour les builds iOS officiels :

- Seuls les builds iOS OpenClaw authentiques distribués via Apple peuvent utiliser le relais hébergé.
- Une gateway ne peut envoyer des pushes relayés que pour les appareils iOS qui se sont appairés avec cette gateway spécifique.

Saut par saut :

1. `Application iOS -> gateway`
   - L'application s'appaire d'abord avec la gateway via le flux d'authentification Gateway normal.
   - Cela donne à l'application une session de nœud authentifiée plus une session opérateur authentifiée.
   - La session opérateur est utilisée pour appeler `gateway.identity.get`.

2. `Application iOS -> relais`
   - L'application appelle les points de terminaison d'enregistrement du relais via HTTPS.
   - L'enregistrement inclut la preuve App Attest plus le reçu de l'application.
   - Le relais valide l'ID de bundle, la preuve App Attest et le reçu Apple, et exige le chemin de distribution officiel/production.
   - C'est ce qui empêche les builds locaux Xcode/dev d'utiliser le relais hébergé. Un build local peut être signé, mais il ne satisfait pas la preuve de distribution Apple officielle que le relais attend.

3. `Délégation d'identité de gateway`
   - Avant l'enregistrement du relais, l'application récupère l'identité de la gateway appairée à partir de `gateway.identity.get`.
   - L'application inclut cette identité de gateway dans la charge utile d'enregistrement du relais.
   - Le relais retourne un handle de relais et une subvention d'envoi limitée à l'enregistrement qui sont délégués à cette identité de gateway.

4. `Gateway -> relais`
   - La gateway stocke le handle de relais et la subvention d'envoi de `push.apns.register`.
   - Sur `push.test`, les réveils de reconnexion et les nudges de réveil, la gateway signe la demande d'envoi avec sa propre identité d'appareil.
   - Le relais vérifie à la fois la subvention d'envoi stockée et la signature de la gateway par rapport à l'identité de gateway déléguée de l'enregistrement.
   - Une autre gateway ne peut pas réutiliser cet enregistrement stocké, même si elle obtient d'une manière ou d'une autre le handle.

5. `Relais -> APNs`
   - Le relais possède les identifiants APNs de production et le jeton APNs brut pour le build officiel.
   - La gateway ne stocke jamais le jeton APNs brut pour les builds officiels relayés.
   - Le relais envoie le push final à APNs au nom de la gateway appairée.

Pourquoi cette conception a été créée :

- Pour garder les identifiants APNs de production hors des gateways utilisateur.
- Pour éviter de stocker les jetons APNs bruts de build officiel sur la gateway.
- Pour permettre l'utilisation du relais hébergé uniquement pour les builds OpenClaw officiels/TestFlight.
- Pour empêcher une gateway d'envoyer des pushes de réveil aux appareils iOS appartenant à une gateway différente.

Les builds locaux/manuels restent sur APNs direct. Si vous testez ces builds sans le relais, la gateway a toujours besoin des identifiants APNs directs :

```bash
export OPENCLAW_APNS_TEAM_ID="TEAMID"
export OPENCLAW_APNS_KEY_ID="KEYID"
export OPENCLAW_APNS_PRIVATE_KEY_P8="$(cat /path/to/AuthKey_KEYID.p8)"
```

## Chemins de découverte

### Bonjour (LAN)

La Gateway annonce `_openclaw-gw._tcp` sur `local.`. L'application iOS les liste automatiquement.

### Tailnet (inter-réseau)

Si mDNS est bloqué, utilisez une zone DNS-SD unicast (choisissez un domaine ; exemple : `openclaw.internal.`) et le DNS divisé Tailscale.
Voir [Bonjour](/fr/gateway/bonjour) pour l'exemple CoreDNS.

### Hôte/port manuel

Dans Paramètres, activez **Hôte manuel** et entrez l'hôte + port de la gateway (par défaut `18789`).

## Canvas + A2UI

Le nœud iOS rend un canvas WKWebView. Utilisez `node.invoke` pour le piloter :

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18789/__openclaw__/canvas/"}'
```

Notes :

- L'hôte canvas de la Gateway sert `/__openclaw__/canvas/` et `/__openclaw__/a2ui/`.
- Il est servi à partir du serveur HTTP Gateway (même port que `gateway.port`, par défaut `18789`).
- Le nœud iOS navigue automatiquement vers A2UI à la connexion quand une URL d'hôte canvas est annoncée.
- Retournez à l'échafaudage intégré avec `canvas.navigate` et `{"url":""}`.

### Évaluation canvas / snapshot

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"(() => { const {ctx} = window.__openclaw; ctx.clearRect(0,0,innerWidth,innerHeight); ctx.lineWidth=6; ctx.strokeStyle=\"#ff2d55\"; ctx.beginPath(); ctx.moveTo(40,40); ctx.lineTo(innerWidth-40, innerHeight-40); ctx.stroke(); return \"ok\"; })()"}'
```

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'
```

## Activation vocale + mode conversation

- L'activation vocale et le mode conversation sont disponibles dans Paramètres.
- iOS peut suspendre l'audio en arrière-plan ; traitez les fonctionnalités vocales comme étant au mieux des efforts quand l'application n'est pas active.

## Erreurs courantes

- `NODE_BACKGROUND_UNAVAILABLE` : mettez l'application iOS au premier plan (les commandes canvas/caméra/écran l'exigent).
- `A2UI_HOST_NOT_CONFIGURED` : la Gateway n'a pas annoncé d'URL d'hôte canvas ; vérifiez `canvasHost` dans [Configuration de la Gateway](/fr/gateway/configuration).
- L'invite d'appairage n'apparaît jamais : exécutez `openclaw devices list` et approuvez manuellement.
- La reconnexion échoue après la réinstallation : le jeton d'appairage Keychain a été effacé ; réappairez le nœud.

## Documentation connexe

- [Appairage](/fr/channels/pairing)
- [Découverte](/fr/gateway/discovery)
- [Bonjour](/fr/gateway/bonjour)
