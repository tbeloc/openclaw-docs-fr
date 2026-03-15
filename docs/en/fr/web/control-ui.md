---
summary: "Interface de contrôle basée sur navigateur pour la Gateway (chat, nœuds, config)"
read_when:
  - You want to operate the Gateway from a browser
  - You want Tailnet access without SSH tunnels
title: "Control UI"
---

# Control UI (navigateur)

Control UI est une petite application monopage **Vite + Lit** servie par la Gateway :

- par défaut : `http://<host>:18789/`
- préfixe optionnel : définir `gateway.controlUi.basePath` (par ex. `/openclaw`)

Elle communique **directement avec le WebSocket de la Gateway** sur le même port.

## Ouverture rapide (local)

Si la Gateway s'exécute sur le même ordinateur, ouvrez :

- [http://127.0.0.1:18789/](http://127.0.0.1:18789/) (ou [http://localhost:18789/](http://localhost:18789/))

Si la page ne se charge pas, démarrez d'abord la Gateway : `openclaw gateway`.

L'authentification est fournie lors de la poignée de main WebSocket via :

- `connect.params.auth.token`
- `connect.params.auth.password`
  Le panneau des paramètres du tableau de bord conserve un jeton pour la session actuelle de l'onglet du navigateur et l'URL de la gateway sélectionnée ; les mots de passe ne sont pas conservés.
  L'assistant d'intégration génère un jeton de gateway par défaut, collez-le ici lors de la première connexion.

## Appairage d'appareil (première connexion)

Lorsque vous vous connectez à Control UI depuis un nouveau navigateur ou appareil, la Gateway
nécessite une **approbation d'appairage unique** — même si vous êtes sur le même Tailnet
avec `gateway.auth.allowTailscale: true`. C'est une mesure de sécurité pour prévenir
l'accès non autorisé.

**Ce que vous verrez :** « disconnected (1008): pairing required »

**Pour approuver l'appareil :**

```bash
# Lister les demandes en attente
openclaw devices list

# Approuver par ID de demande
openclaw devices approve <requestId>
```

Une fois approuvé, l'appareil est mémorisé et ne nécessitera pas de réapprobation sauf si
vous le révoquez avec `openclaw devices revoke --device <id> --role <role>`. Voir
[Devices CLI](/cli/devices) pour la rotation et la révocation des jetons.

**Notes :**

- Les connexions locales (`127.0.0.1`) sont auto-approuvées.
- Les connexions distantes (LAN, Tailnet, etc.) nécessitent une approbation explicite.
- Chaque profil de navigateur génère un ID d'appareil unique, donc changer de navigateur ou
  effacer les données du navigateur nécessitera un réappairage.

## Support des langues

Control UI peut se localiser automatiquement au premier chargement en fonction de la locale de votre navigateur, et vous pouvez la remplacer ultérieurement à partir du sélecteur de langue dans la carte Access.

- Locales supportées : `en`, `zh-CN`, `zh-TW`, `pt-BR`, `de`, `es`
- Les traductions non-anglaises sont chargées en différé dans le navigateur.
- La locale sélectionnée est enregistrée dans le stockage du navigateur et réutilisée lors des visites futures.
- Les clés de traduction manquantes reviennent à l'anglais.

## Ce qu'il peut faire (aujourd'hui)

- Discuter avec le modèle via Gateway WS (`chat.history`, `chat.send`, `chat.abort`, `chat.inject`)
- Appels d'outils en flux + cartes de sortie d'outils en direct dans Chat (événements d'agent)
- Canaux : statut WhatsApp/Telegram/Discord/Slack + canaux de plugin (Mattermost, etc.) + connexion QR + config par canal (`channels.status`, `web.login.*`, `config.patch`)
- Instances : liste de présence + actualisation (`system-presence`)
- Sessions : liste + remplacements par session de réflexion/rapide/verbeux/raisonnement (`sessions.list`, `sessions.patch`)
- Tâches Cron : liste/ajouter/éditer/exécuter/activer/désactiver + historique d'exécution (`cron.*`)
- Compétences : statut, activer/désactiver, installer, mises à jour de clé API (`skills.*`)
- Nœuds : liste + capacités (`node.list`)
- Approbations Exec : éditer les listes blanches de gateway ou de nœud + demander la politique pour `exec host=gateway/node` (`exec.approvals.*`)
- Config : afficher/éditer `~/.openclaw/openclaw.json` (`config.get`, `config.set`)
- Config : appliquer + redémarrer avec validation (`config.apply`) et réveiller la dernière session active
- Les écritures de config incluent une protection de hash de base pour éviter de écraser les éditions concurrentes
- Schéma de config + rendu de formulaire (`config.schema`, incluant les schémas de plugin + canal) ; l'éditeur JSON brut reste disponible
- Debug : snapshots de statut/santé/modèles + journal d'événements + appels RPC manuels (`status`, `health`, `models.list`)
- Logs : suivi en direct des logs de fichier de gateway avec filtre/export (`logs.tail`)
- Update : exécuter une mise à jour de package/git + redémarrer (`update.run`) avec un rapport de redémarrage

Notes du panneau des tâches Cron :

- Pour les tâches isolées, la livraison par défaut est un résumé d'annonce. Vous pouvez basculer sur aucun si vous voulez des exécutions internes uniquement.
- Les champs de canal/cible apparaissent lorsque l'annonce est sélectionnée.
- Le mode webhook utilise `delivery.mode = "webhook"` avec `delivery.to` défini sur une URL webhook HTTP(S) valide.
- Pour les tâches de session principale, les modes de livraison webhook et aucun sont disponibles.
- Les contrôles d'édition avancés incluent la suppression après exécution, l'effacement du remplacement d'agent, les options cron exact/stagger,
  les remplacements de modèle/réflexion d'agent, et les bascules de livraison au mieux.
- La validation du formulaire est en ligne avec des erreurs au niveau du champ ; les valeurs invalides désactivent le bouton d'enregistrement jusqu'à correction.
- Définir `cron.webhookToken` pour envoyer un jeton porteur dédié, s'il est omis le webhook est envoyé sans en-tête d'authentification.
- Fallback déprécié : les tâches héritées stockées avec `notify: true` peuvent toujours utiliser `cron.webhook` jusqu'à migration.

## Comportement du chat

- `chat.send` est **non-bloquant** : il accuse réception immédiatement avec `{ runId, status: "started" }` et la réponse s'écoule via les événements `chat`.
- Le renvoi avec la même `idempotencyKey` retourne `{ status: "in_flight" }` pendant l'exécution, et `{ status: "ok" }` après completion.
- Les réponses `chat.history` sont limitées en taille pour la sécurité de l'UI. Lorsque les entrées de transcription sont trop grandes, la Gateway peut tronquer les champs de texte longs, omettre les blocs de métadonnées lourds, et remplacer les messages surdimensionnés par un placeholder (`[chat.history omitted: message too large]`).
- `chat.inject` ajoute une note d'assistant à la transcription de session et diffuse un événement `chat` pour les mises à jour UI uniquement (pas d'exécution d'agent, pas de livraison de canal).
- Arrêt :
  - Cliquez sur **Stop** (appelle `chat.abort`)
  - Tapez `/stop` (ou des phrases d'arrêt autonomes comme `stop`, `stop action`, `stop run`, `stop openclaw`, `please stop`) pour avorter hors bande
  - `chat.abort` supporte `{ sessionKey }` (pas de `runId`) pour avorter toutes les exécutions actives pour cette session
- Rétention d'avortement partiel :
  - Lorsqu'une exécution est avortée, le texte d'assistant partiel peut toujours être affiché dans l'UI
  - La Gateway persiste le texte d'assistant partiel avorté dans l'historique de transcription lorsqu'il existe une sortie en buffer
  - Les entrées persistées incluent les métadonnées d'avortement afin que les consommateurs de transcription puissent distinguer les partiels d'avortement de la sortie de completion normale

## Accès Tailnet (recommandé)

### Tailscale Serve intégré (préféré)

Gardez la Gateway sur loopback et laissez Tailscale Serve la proxifier avec HTTPS :

```bash
openclaw gateway --tailscale serve
```

Ouvrez :

- `https://<magicdns>/` (ou votre `gateway.controlUi.basePath` configuré)

Par défaut, les demandes Control UI/WebSocket Serve peuvent s'authentifier via les en-têtes d'identité Tailscale
(`tailscale-user-login`) lorsque `gateway.auth.allowTailscale` est `true`. OpenClaw
vérifie l'identité en résolvant l'adresse `x-forwarded-for` avec
`tailscale whois` et en la faisant correspondre à l'en-tête, et n'accepte ces demandes que lorsque la
demande atteint loopback avec les en-têtes `x-forwarded-*` de Tailscale. Définir
`gateway.auth.allowTailscale: false` (ou forcer `gateway.auth.mode: "password"`)
si vous voulez exiger un jeton/mot de passe même pour le trafic Serve.
L'authentification Serve sans jeton suppose que l'hôte de la gateway est de confiance. Si du code local non fiable peut s'exécuter sur cet hôte, exigez une authentification par jeton/mot de passe.

### Lier à tailnet + jeton

```bash
openclaw gateway --bind tailnet --token "$(openssl rand -hex 32)"
```

Puis ouvrez :

- `http://<tailscale-ip>:18789/` (ou votre `gateway.controlUi.basePath` configuré)

Collez le jeton dans les paramètres de l'UI (envoyé comme `connect.params.auth.token`).

## HTTP non sécurisé

Si vous ouvrez le tableau de bord sur HTTP brut (`http://<lan-ip>` ou `http://<tailscale-ip>`),
le navigateur s'exécute dans un **contexte non sécurisé** et bloque WebCrypto. Par défaut,
OpenClaw **bloque** les connexions Control UI sans identité d'appareil.

**Correction recommandée :** utilisez HTTPS (Tailscale Serve) ou ouvrez l'UI localement :

- `https://<magicdns>/` (Serve)
- `http://127.0.0.1:18789/` (sur l'hôte de la gateway)

**Comportement du basculement d'authentification non sécurisée :**

```json5
{
  gateway: {
    controlUi: { allowInsecureAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

`allowInsecureAuth` est un basculement de compatibilité local uniquement :

- Il permet aux sessions Control UI localhost de procéder sans identité d'appareil dans
  les contextes HTTP non sécurisés.
- Il ne contourne pas les vérifications d'appairage.
- Il ne relâche pas les exigences d'identité d'appareil distantes (non-localhost).

**Verre de secours uniquement :**

```json5
{
  gateway: {
    controlUi: { dangerouslyDisableDeviceAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

`dangerouslyDisableDeviceAuth` désactive les vérifications d'identité d'appareil Control UI et est une
dégradation de sécurité grave. Revenez rapidement après utilisation d'urgence.

Voir [Tailscale](/gateway/tailscale) pour les conseils de configuration HTTPS.

## Construction de l'UI

La Gateway sert les fichiers statiques depuis `dist/control-ui`. Construisez-les avec :

```bash
pnpm ui:build # auto-installe les dépendances UI à la première exécution
```

Base absolue optionnelle (lorsque vous voulez des URL d'actifs fixes) :

```bash
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

Pour le développement local (serveur de développement séparé) :

```bash
pnpm ui:dev # auto-installe les dépendances UI à la première exécution
```

Puis pointez l'UI vers votre URL Gateway WS (par ex. `ws://127.0.0.1:18789`).

## Débogage/test : serveur de développement + Gateway distante

Control UI est des fichiers statiques ; la cible WebSocket est configurable et peut être
différente de l'origine HTTP. C'est pratique lorsque vous voulez le serveur Vite localement mais la Gateway s'exécute ailleurs.

1. Démarrez le serveur de développement UI : `pnpm ui:dev`
2. Ouvrez une URL comme :

```text
http://localhost:5173/?gatewayUrl=ws://<gateway-host>:18789
```

Authentification optionnelle unique (si nécessaire) :

```text
http://localhost:5173/?gatewayUrl=wss://<gateway-host>:18789#token=<gateway-token>
```

Notes :

- `gatewayUrl` est stocké dans localStorage après le chargement et supprimé de l'URL.
- `token` est importé du fragment d'URL, stocké dans sessionStorage pour la session actuelle de l'onglet du navigateur et l'URL de gateway sélectionnée, et supprimé de l'URL ; il n'est pas stocké dans localStorage.
- `password` est conservé en mémoire uniquement.
- Lorsque `gatewayUrl` est défini, l'UI ne revient pas aux identifiants de config ou d'environnement.
  Fournissez `token` (ou `password`) explicitement. Les identifiants explicites manquants sont une erreur.
- Utilisez `wss://` lorsque la Gateway est derrière TLS (Tailscale Serve, proxy HTTPS, etc.).
- `gatewayUrl` n'est accepté que dans une fenêtre de niveau supérieur (non intégrée) pour prévenir le clickjacking.
- Les déploiements Control UI non-loopback doivent définir `gateway.controlUi.allowedOrigins`
  explicitement (origines complètes). Cela inclut les configurations de développement distantes.
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` active
  le mode fallback d'origine d'en-tête Host, mais c'est un mode de sécurité dangereux.

Exemple :

```json5
{
  gateway: {
    controlUi: {
      allowedOrigins: ["http://localhost:5173"],
    },
  },
}
```

Détails de configuration d'accès distant : [Accès distant](/gateway/remote).
