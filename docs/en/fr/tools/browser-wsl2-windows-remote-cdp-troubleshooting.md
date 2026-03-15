---
summary: "Dépannage des configurations WSL2 Gateway + Chrome distant CDP et extension-relay de Windows en couches"
read_when:
  - Exécution d'OpenClaw Gateway dans WSL2 tandis que Chrome se trouve sur Windows
  - Observation d'erreurs chevauchantes du navigateur/control-ui sur WSL2 et Windows
  - Décision entre le CDP distant brut et le relais d'extension Chrome dans les configurations multi-hôtes
title: "Dépannage WSL2 + Windows + Chrome CDP distant"
---

# Dépannage WSL2 + Windows + Chrome CDP distant

Ce guide couvre la configuration multi-hôte courante où :

- OpenClaw Gateway s'exécute dans WSL2
- Chrome s'exécute sur Windows
- le contrôle du navigateur doit traverser la limite WSL2/Windows

Il couvre également le modèle de défaillance en couches du [problème #39369](https://github.com/openclaw/openclaw/issues/39369) : plusieurs problèmes indépendants peuvent apparaître simultanément, ce qui fait que la mauvaise couche semble cassée en premier.

## Choisir d'abord le bon mode navigateur

Vous avez deux modèles valides :

### Option 1 : CDP distant brut

Utilisez un profil de navigateur distant qui pointe de WSL2 vers un point de terminaison CDP Chrome Windows.

Choisissez ceci quand :

- vous avez besoin uniquement du contrôle du navigateur
- vous êtes à l'aise d'exposer le débogage distant de Chrome à WSL2
- vous n'avez pas besoin du relais d'extension Chrome

### Option 2 : Relais d'extension Chrome

Utilisez le profil `chrome-relay` intégré plus l'extension OpenClaw Chrome.

Choisissez ceci quand :

- vous voulez vous attacher à un onglet Chrome Windows existant avec le bouton de la barre d'outils
- vous préférez le contrôle basé sur l'extension plutôt que le `--remote-debugging-port` brut
- le relais lui-même doit être accessible à travers la limite WSL2/Windows

Si vous utilisez le relais d'extension sur les espaces de noms, `browser.relayBindHost` est le paramètre important introduit dans [Browser](/tools/browser) et [Extension Chrome](/tools/chrome-extension).

## Architecture fonctionnelle

Forme de référence :

- WSL2 exécute la Gateway sur `127.0.0.1:18789`
- Windows ouvre l'interface de contrôle dans un navigateur normal à `http://127.0.0.1:18789/`
- Windows Chrome expose un point de terminaison CDP sur le port `9222`
- WSL2 peut atteindre ce point de terminaison CDP Windows
- OpenClaw pointe un profil de navigateur vers l'adresse accessible depuis WSL2

## Pourquoi cette configuration est confuse

Plusieurs défaillances peuvent se chevaucher :

- WSL2 ne peut pas atteindre le point de terminaison CDP Windows
- l'interface de contrôle est ouverte à partir d'une origine non sécurisée
- `gateway.controlUi.allowedOrigins` ne correspond pas à l'origine de la page
- le jeton ou l'appairage est manquant
- le profil du navigateur pointe vers la mauvaise adresse
- le relais d'extension est toujours en loopback uniquement alors que vous avez réellement besoin d'un accès multi-espaces de noms

Pour cette raison, corriger une couche peut laisser une erreur différente visible.

## Règle critique pour l'interface de contrôle

Quand l'interface est ouverte depuis Windows, utilisez localhost Windows sauf si vous avez une configuration HTTPS délibérée.

Utilisez :

`http://127.0.0.1:18789/`

Ne passez pas par défaut à une adresse IP LAN pour l'interface de contrôle. Le HTTP brut sur une adresse LAN ou tailnet peut déclencher un comportement d'authentification d'appareil/origine non sécurisée sans rapport avec le CDP lui-même. Voir [Interface de contrôle](/web/control-ui).

## Valider par couches

Travaillez de haut en bas. Ne sautez pas d'étapes.

### Couche 1 : Vérifier que Chrome sert CDP sur Windows

Démarrez Chrome sur Windows avec le débogage distant activé :

```powershell
chrome.exe --remote-debugging-port=9222
```

Depuis Windows, vérifiez d'abord Chrome lui-même :

```powershell
curl http://127.0.0.1:9222/json/version
curl http://127.0.0.1:9222/json/list
```

Si cela échoue sur Windows, OpenClaw n'est pas encore le problème.

### Couche 2 : Vérifier que WSL2 peut atteindre ce point de terminaison Windows

Depuis WSL2, testez l'adresse exacte que vous prévoyez d'utiliser dans `cdpUrl` :

```bash
curl http://WINDOWS_HOST_OR_IP:9222/json/version
curl http://WINDOWS_HOST_OR_IP:9222/json/list
```

Bon résultat :

- `/json/version` retourne JSON avec les métadonnées Browser / Protocol-Version
- `/json/list` retourne JSON (un tableau vide est correct si aucune page n'est ouverte)

Si cela échoue :

- Windows n'expose pas encore le port à WSL2
- l'adresse est incorrecte pour le côté WSL2
- le pare-feu / la redirection de port / le proxy local est toujours manquant

Corrigez cela avant de toucher à la configuration OpenClaw.

### Couche 3 : Configurer le profil de navigateur correct

Pour le CDP distant brut, pointez OpenClaw vers l'adresse accessible depuis WSL2 :

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "remote",
    profiles: {
      remote: {
        cdpUrl: "http://WINDOWS_HOST_OR_IP:9222",
        attachOnly: true,
        color: "#00AA00",
      },
    },
  },
}
```

Notes :

- utilisez l'adresse accessible depuis WSL2, pas celle qui ne fonctionne que sur Windows
- gardez `attachOnly: true` pour les navigateurs gérés en externe
- testez la même URL avec `curl` avant de vous attendre à ce qu'OpenClaw réussisse

### Couche 4 : Si vous utilisez le relais d'extension Chrome à la place

Si la machine du navigateur et la Gateway sont séparées par une limite d'espace de noms, le relais peut avoir besoin d'une adresse de liaison non-loopback.

Exemple :

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "chrome-relay",
    relayBindHost: "0.0.0.0",
  },
}
```

Utilisez ceci uniquement si nécessaire :

- le comportement par défaut est plus sûr car le relais reste en loopback uniquement
- `0.0.0.0` élargit la surface d'exposition
- gardez l'authentification Gateway, l'appairage des nœuds et le réseau environnant privés

Si vous n'avez pas besoin du relais d'extension, préférez le profil CDP distant brut ci-dessus.

### Couche 5 : Vérifier la couche interface de contrôle séparément

Ouvrez l'interface depuis Windows :

`http://127.0.0.1:18789/`

Puis vérifiez :

- l'origine de la page correspond à ce que `gateway.controlUi.allowedOrigins` attend
- l'authentification par jeton ou l'appairage est configuré correctement
- vous ne déboguez pas un problème d'authentification de l'interface de contrôle comme s'il s'agissait d'un problème de navigateur

Page utile :

- [Interface de contrôle](/web/control-ui)

### Couche 6 : Vérifier le contrôle du navigateur de bout en bout

Depuis WSL2 :

```bash
openclaw browser open https://example.com --browser-profile remote
openclaw browser tabs --browser-profile remote
```

Pour le relais d'extension :

```bash
openclaw browser tabs --browser-profile chrome-relay
```

Bon résultat :

- l'onglet s'ouvre dans Windows Chrome
- `openclaw browser tabs` retourne la cible
- les actions ultérieures (`snapshot`, `screenshot`, `navigate`) fonctionnent à partir du même profil

## Erreurs courantes trompeuses

Traitez chaque message comme un indice spécifique à une couche :

- `control-ui-insecure-auth`
  - Problème d'origine UI / contexte sécurisé, pas un problème de transport CDP
- `token_missing`
  - Problème de configuration d'authentification
- `pairing required`
  - Problème d'approbation d'appareil
- `Remote CDP for profile "remote" is not reachable`
  - WSL2 ne peut pas atteindre le `cdpUrl` configuré
- `gateway timeout after 1500ms`
  - Souvent toujours un problème de réachabilité CDP ou un point de terminaison distant lent/inaccessible
- `Chrome extension relay is running, but no tab is connected`
  - Profil de relais d'extension sélectionné, mais aucun onglet attaché n'existe encore

## Liste de contrôle de triage rapide

1. Windows : `curl http://127.0.0.1:9222/json/version` fonctionne-t-il ?
2. WSL2 : `curl http://WINDOWS_HOST_OR_IP:9222/json/version` fonctionne-t-il ?
3. Configuration OpenClaw : `browser.profiles.<name>.cdpUrl` utilise-t-il cette adresse exacte accessible depuis WSL2 ?
4. Interface de contrôle : ouvrez-vous `http://127.0.0.1:18789/` au lieu d'une adresse IP LAN ?
5. Relais d'extension uniquement : avez-vous réellement besoin de `browser.relayBindHost`, et si oui est-il défini explicitement ?

## Conclusion pratique

La configuration est généralement viable. La partie difficile est que le transport du navigateur, la sécurité de l'origine de l'interface de contrôle, le jeton/appairage et la topologie du relais d'extension peuvent chacun échouer indépendamment tout en semblant similaires du côté utilisateur.

En cas de doute :

- vérifiez d'abord le point de terminaison Chrome Windows localement
- vérifiez le même point de terminaison depuis WSL2 en second
- ne déboguez la configuration OpenClaw ou l'authentification de l'interface de contrôle qu'après
