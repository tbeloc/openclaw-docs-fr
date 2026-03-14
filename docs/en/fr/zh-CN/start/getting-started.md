---
read_when:
  - 从零开始首次设置
  - 你想要从安装 → 新手引导 → 第一条消息的最快路径
summary: 新手指南：从零到第一条消息（向导、认证、渠道、配对）
title: 入门指南
x-i18n:
  generated_at: "2026-02-03T07:54:14Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 78cfa02eb2e4ea1a83e18edd99d142dbae707ec063e8d74c9a54f94581aa067f
  source_path: start/getting-started.md
  workflow: 15
---

# Guide de démarrage

Objectif : passer rapidement de **zéro** à **votre premier chat fonctionnel** (avec des paramètres par défaut raisonnables).

Chat le plus rapide : ouvrez l'interface de contrôle (sans configuration de canal). Exécutez `openclaw dashboard` et chattez dans votre navigateur, ou ouvrez `http://127.0.0.1:18789/` sur l'hôte Gateway. Documentation : [Dashboard](/web/dashboard) et [Control UI](/web/control-ui).

Chemin recommandé : utilisez l'**assistant d'intégration CLI** (`openclaw onboard`). Il configure :

- Modèle/authentification (OAuth recommandé)
- Configuration de Gateway
- Canaux (WhatsApp/Telegram/Discord/Mattermost (plugin)/...)
- Valeurs par défaut d'appairage (messages privés sécurisés)
- Initialisation de l'espace de travail + Skills
- Services en arrière-plan optionnels

Si vous souhaitez des pages de référence plus approfondies, consultez : [Assistant](/start/wizard), [Configuration](/start/setup), [Appairage](/channels/pairing), [Sécurité](/gateway/security).

Note sur le bac à sable : `agents.defaults.sandbox.mode: "non-main"` utilise `session.mainKey` (par défaut `"main"`), donc les sessions de groupe/canal sont isolées dans le bac à sable. Si vous souhaitez que l'agent principal s'exécute toujours sur l'hôte principal, définissez un remplacement explicite par agent :

```json
{
  "routing": {
    "agents": {
      "main": {
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    }
  }
}
```

## 0) Prérequis

- Node `>=22`
- `pnpm` (optionnel ; recommandé si vous construisez à partir du code source)
- **Recommandé :** clé API Brave Search pour la recherche web. Le moyen le plus simple : `openclaw configure --section web` (stocke `tools.web.search.apiKey`). Voir [Outils Web](/tools/web).

macOS : si vous prévoyez de construire l'application, installez Xcode / CLT. Pour CLI + Gateway uniquement, Node suffit.
Windows : utilisez **WSL2** (Ubuntu recommandé). WSL2 est fortement recommandé ; Windows natif n'a pas été testé, a plus de problèmes et une compatibilité d'outils moins bonne. Installez d'abord WSL2, puis exécutez les étapes Linux dans WSL. Voir [Windows (WSL2)](/platforms/windows).

## 1) Installer la CLI (recommandé)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Options du programme d'installation (méthode d'installation, non-interactif, depuis GitHub) : [Installation](/install).

Windows (PowerShell) :

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Alternative (installation globale) :

```bash
npm install -g openclaw@latest
```

```bash
pnpm add -g openclaw@latest
```

## 2) Exécuter l'assistant d'intégration (et installer le service)

```bash
openclaw onboard --install-daemon
```

Vous allez choisir :

- **Gateway local vs distant**
- **Authentification** : abonnement OpenAI Code (Codex) (OAuth) ou clé API. Pour Anthropic, nous recommandons la clé API ; `claude setup-token` est également supporté.
- **Fournisseurs** : connexion QR WhatsApp, jetons de bot Telegram/Discord, jetons de plugin Mattermost, etc.
- **Démon** : installation en arrière-plan (launchd/systemd ; WSL2 utilise systemd)
  - **Runtime** : Node (recommandé ; requis pour WhatsApp/Telegram). **Non recommandé** Bun.
- **Jeton Gateway** : l'assistant génère par défaut un jeton (même sur loopback) et le stocke dans `gateway.auth.token`.

Documentation de l'assistant : [Assistant](/start/wizard)

### Identifiants : emplacement de stockage (important)

- **Chemin Anthropic recommandé :** définissez la clé API (l'assistant peut la stocker pour le service). Si vous souhaitez réutiliser les identifiants Claude Code, `claude setup-token` est également supporté.

- Identifiants OAuth (importation héritée) : `~/.openclaw/credentials/oauth.json`
- Fichier de configuration d'authentification (OAuth + clé API) : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

Conseil sans interface/serveur : complétez d'abord OAuth sur une machine ordinaire, puis copiez `oauth.json` sur l'hôte Gateway.

## 3) Démarrer Gateway

Si vous avez installé le service pendant l'intégration, Gateway devrait déjà être en cours d'exécution :

```bash
openclaw gateway status
```

Exécution manuelle (premier plan) :

```bash
openclaw gateway --port 18789 --verbose
```

Dashboard (loopback local) : `http://127.0.0.1:18789/`
Si un jeton est configuré, collez-le dans les paramètres de l'interface de contrôle (stocké comme `connect.params.auth.token`).

⚠️ **Avertissement Bun (WhatsApp + Telegram) :** Bun a des problèmes connus avec ces canaux. Si vous utilisez WhatsApp ou Telegram, exécutez Gateway avec **Node**.

## 3.5) Vérification rapide (2 minutes)

```bash
openclaw status
openclaw health
openclaw security audit --deep
```

## 4) Appairage + connexion de votre première interface de chat

### WhatsApp (connexion QR)

```bash
openclaw channels login
```

Scannez via WhatsApp → Paramètres → Appareils liés.

Documentation WhatsApp : [WhatsApp](/channels/whatsapp)

### Telegram / Discord / Autres

L'assistant peut écrire les jetons/configurations pour vous. Si vous préférez la configuration manuelle, commencez ici :

- Telegram : [Telegram](/channels/telegram)
- Discord : [Discord](/channels/discord)
- Mattermost (plugin) : [Mattermost](/channels/mattermost)

**Conseil messages privés Telegram :** votre premier message privé retournera un code d'appairage. Approuvez-le (voir l'étape suivante), sinon le bot ne répondra pas.

## 5) Sécurité des messages privés (approbation d'appairage)

Posture par défaut : les messages privés inconnus reçoivent un code court, et les messages ne sont pas traités avant approbation. Si votre premier message privé n'a pas reçu de réponse, approuvez l'appairage :

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <code>
```

Documentation d'appairage : [Appairage](/channels/pairing)

## À partir du code source (développement)

Si vous développez OpenClaw lui-même, exécutez à partir du code source :

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # Installe automatiquement les dépendances UI à la première exécution
pnpm build
openclaw onboard --install-daemon
```

Si vous n'avez pas installé globalement, exécutez les étapes d'intégration depuis le dépôt via `pnpm openclaw ...`. `pnpm build` empaquette également les ressources A2UI ; si vous avez seulement besoin d'exécuter cette étape, utilisez `pnpm canvas:a2ui:bundle`.

Gateway (depuis ce dépôt) :

```bash
node openclaw.mjs gateway --port 18789 --verbose
```

## 7) Vérification de bout en bout

Dans un nouveau terminal, envoyez un message de test :

```bash
openclaw message send --target +15555550123 --message "Hello from OpenClaw"
```

Si `openclaw health` affiche "authentification non configurée", retournez à l'assistant pour configurer l'authentification OAuth/clé — sans cela, l'agent ne pourra pas répondre.

Conseil : `openclaw status --all` est le meilleur rapport de débogage collable et en lecture seule.
Sonde de santé : `openclaw health` (ou `openclaw status --deep`) demande un snapshot de santé au Gateway en cours d'exécution.

## Étapes suivantes (optionnel, mais excellent)

- Application barre de menu macOS + activation vocale : [Application macOS](/platforms/macos)
- Nœuds iOS/Android (Canvas/caméra/voix) : [Nœuds](/nodes)
- Accès distant (tunnel SSH / Tailscale Serve) : [Accès distant](/gateway/remote) et [Tailscale](/gateway/tailscale)
- Configuration toujours actif / VPN : [Accès distant](/gateway/remote), [exe.dev](/install/exe-dev), [Hetzner](/install/hetzner), [macOS distant](/platforms/mac/remote)
