---
read_when:
  - 你想从浏览器操作 Gateway 网关
  - 你想要无需 SSH 隧道的 Tailnet 访问
summary: Gateway 网关的浏览器控制 UI（聊天、节点、配置）
title: 控制 UI
x-i18n:
  generated_at: "2026-02-03T10:13:20Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: bef105a376fc1a1df44e3e4fb625db1cbcafe2f41e718181c36877b8cbc08816
  source_path: web/control-ui.md
  workflow: 15
---

# Interface de contrôle (navigateur)

L'interface de contrôle est une petite application monopage **Vite + Lit** servie par la passerelle Gateway :

- Par défaut : `http://<host>:18789/`
- Préfixe optionnel : définissez `gateway.controlUi.basePath` (par exemple `/openclaw`)

Elle **communique directement avec le WebSocket de la passerelle Gateway sur le même port**.

## Ouverture rapide (local)

Si la passerelle Gateway s'exécute sur le même ordinateur, ouvrez :

- http://127.0.0.1:18789/ (ou http://localhost:18789/)

Si la page ne se charge pas, démarrez d'abord la passerelle Gateway : `openclaw gateway`.

L'authentification est fournie lors de la poignée de main WebSocket via :

- `connect.params.auth.token`
- `connect.params.auth.password`
  Le panneau des paramètres du tableau de bord vous permet de stocker le token ; le mot de passe n'est pas persisté.
  L'assistant de configuration génère par défaut un token de passerelle Gateway, collez-le donc ici lors de la première connexion.

## Appairage d'appareil (première connexion)

Lorsque vous vous connectez à l'interface de contrôle depuis un nouveau navigateur ou appareil, la passerelle Gateway nécessite une **approbation d'appairage unique** — même si vous êtes sur le même Tailnet et que `gateway.auth.allowTailscale: true`. C'est une mesure de sécurité pour prévenir l'accès non autorisé.

**Vous verrez :** « disconnected (1008): pairing required »

**Approuver un appareil :**

```bash
# Lister les demandes en attente
openclaw devices list

# Approuver par ID de demande
openclaw devices approve <requestId>
```

Une fois approuvé, l'appareil est mémorisé et ne nécessite pas de réappairage à moins que vous le révoquiez avec `openclaw devices revoke --device <id> --role <role>`. Consultez [Devices CLI](/cli/devices) pour la rotation des tokens et la révocation.

**Remarques :**

- Les connexions locales (`127.0.0.1`) sont automatiquement approuvées.
- Les connexions distantes (LAN, Tailnet, etc.) nécessitent une approbation explicite.
- Chaque profil de navigateur génère un ID d'appareil unique, donc changer de navigateur ou effacer les données du navigateur nécessitera un réappairage.

## Ce que vous pouvez faire actuellement

- Discuter avec les modèles via la passerelle Gateway WS (`chat.history`, `chat.send`, `chat.abort`, `chat.inject`)
- Diffuser les appels d'outils + cartes de sortie d'outils en temps réel dans le chat (événements d'agent)
- Canaux : statut WhatsApp/Telegram/Discord/Slack + canaux de plugin (Mattermost, etc.) + connexion QR + configuration par canal (`channels.status`, `web.login.*`, `config.patch`)
- Instances : liste en ligne + actualisation (`system-presence`)
- Sessions : liste + couverture de réflexion/détails par session (`sessions.list`, `sessions.patch`)
- Tâches planifiées : lister/ajouter/exécuter/activer/désactiver + historique d'exécution (`cron.*`)
- Compétences : statut, activer/désactiver, installer, mise à jour des clés API (`skills.*`)
- Nœuds : liste + capacités (`node.list`)
- Approbations d'exécution : éditer les listes d'autorisation de la passerelle Gateway ou du nœud + politique de demande pour `exec host=gateway/node` (`exec.approvals.*`)
- Configuration : afficher/éditer `~/.openclaw/openclaw.json` (`config.get`, `config.set`)
- Configuration : appliquer + redémarrer avec validation (`config.apply`) et réveiller la dernière session active
- Les écritures de configuration incluent une protection par hash de base pour éviter les écrasements d'éditions concurrentes
- Schéma de configuration + rendu de formulaire (`config.schema`, incluant les schémas de plugin + canal) ; l'éditeur JSON brut reste disponible
- Débogage : statut/santé/snapshot de modèles + journal des événements + appels RPC manuels (`status`, `health`, `models.list`)
- Journaux : suivi en temps réel de la fin des journaux de fichiers de la passerelle Gateway, avec filtrage/export (`logs.tail`)
- Mises à jour : exécuter les mises à jour de paquet/git + redémarrer (`update.run`) et afficher le rapport de redémarrage

## Comportement du chat

- `chat.send` est **non-bloquant** : il confirme immédiatement avec `{ runId, status: "started" }`, la réponse est diffusée via le flux d'événements `chat`.
- Renvoyer avec la même `idempotencyKey` retourne `{ status: "in_flight" }` pendant l'exécution, puis `{ status: "ok" }` une fois terminé.
- `chat.inject` ajoute une note d'assistant à la transcription de session et diffuse un événement `chat` pour les mises à jour UI uniquement (pas d'exécution d'agent, pas de livraison de canal).
- Arrêt :
  - Cliquez sur **Arrêter** (appelle `chat.abort`)
  - Entrez `/stop` (ou `stop|esc|abort|wait|exit|interrupt`) pour un arrêt hors bande
  - `chat.abort` supporte `{ sessionKey }` (sans `runId`) pour arrêter toutes les exécutions actives de cette session

## Accès Tailnet (recommandé)

### Intégration Tailscale Serve (préféré)

Gardez la passerelle Gateway sur la boucle locale et laissez Tailscale Serve la proxifier avec HTTPS :

```bash
openclaw gateway --tailscale serve
```

Ouvrez :

- `https://<magicdns>/` (ou votre `gateway.controlUi.basePath` configuré)

Par défaut, lorsque `gateway.auth.allowTailscale` est `true`, les demandes Serve peuvent être authentifiées via l'en-tête d'identité Tailscale (`tailscale-user-login`). OpenClaw valide l'identité en utilisant `tailscale whois` pour résoudre l'adresse `x-forwarded-for` et la comparer avec l'en-tête, et n'accepte ces en-têtes que si la demande arrive à la boucle locale via les en-têtes `x-forwarded-*` de Tailscale. Si vous souhaitez exiger un token/mot de passe même pour le trafic Serve, définissez `gateway.auth.allowTailscale: false` (ou forcez `gateway.auth.mode: "password"`).

### Liaison à tailnet + token

```bash
openclaw gateway --bind tailnet --token "$(openssl rand -hex 32)"
```

Puis ouvrez :

- `http://<tailscale-ip>:18789/` (ou votre `gateway.controlUi.basePath` configuré)

Collez le token dans les paramètres de l'UI (envoyé comme `connect.params.auth.token`).

## HTTP non sécurisé

Si vous ouvrez le tableau de bord via HTTP simple (`http://<lan-ip>` ou `http://<tailscale-ip>`), le navigateur s'exécute dans un **contexte non sécurisé** et bloque WebCrypto. Par défaut, OpenClaw **bloque** les connexions de l'interface de contrôle sans identité d'appareil.

**Correction recommandée :** Utilisez HTTPS (Tailscale Serve) ou ouvrez l'UI localement :

- `https://<magicdns>/` (Serve)
- `http://127.0.0.1:18789/` (sur l'hôte de la passerelle Gateway)

**Exemple de dégradation (utiliser le token via HTTP uniquement) :**

```json5
{
  gateway: {
    controlUi: { allowInsecureAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

Cela désactive l'identité d'appareil + l'appairage pour l'interface de contrôle (même sur HTTPS). À utiliser uniquement si vous faites confiance au réseau.

Consultez [Tailscale](/gateway/tailscale) pour un guide de configuration HTTPS.

## Construire l'UI

La passerelle Gateway sert les fichiers statiques depuis `dist/control-ui`. Construisez avec :

```bash
pnpm ui:build # Installe automatiquement les dépendances UI à la première exécution
```

Chemin de base absolu optionnel (lorsque vous voulez des URL de ressources fixes) :

```bash
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

Pour le développement local (serveur de développement séparé) :

```bash
pnpm ui:dev # Installe automatiquement les dépendances UI à la première exécution
```

Puis pointez l'UI vers votre URL WS de passerelle Gateway (par exemple `ws://127.0.0.1:18789`).

## Débogage/Test : serveur de développement + passerelle Gateway distante

L'interface de contrôle est des fichiers statiques ; la cible WebSocket est configurable et peut différer de la source HTTP. C'est pratique lorsque vous voulez utiliser le serveur de développement Vite localement mais que la passerelle Gateway s'exécute ailleurs.

1. Démarrez le serveur de développement UI : `pnpm ui:dev`
2. Ouvrez une URL comme :

```text
http://localhost:5173/?gatewayUrl=ws://<gateway-host>:18789
```

Authentification unique optionnelle (si nécessaire) :

```text
http://localhost:5173/?gatewayUrl=wss://<gateway-host>:18789&token=<gateway-token>
```

Remarques :

- `gatewayUrl` est stocké dans localStorage après le chargement et supprimé de l'URL.
- `token` est stocké dans localStorage ; `password` est conservé uniquement en mémoire.
- Utilisez `wss://` lorsque la passerelle Gateway est derrière TLS (Tailscale Serve, proxy HTTPS, etc.).

Détails de configuration d'accès distant : [Accès distant](/gateway/remote).
