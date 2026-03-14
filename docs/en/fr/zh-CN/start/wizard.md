---
read_when:
  - Exécution ou configuration de l'assistant de configuration
  - Configuration d'une nouvelle machine
summary: Assistant de configuration CLI : configuration guidée de Gateway, espaces de travail, canaux et Skills
title: Assistant de configuration
x-i18n:
  generated_at: "2026-02-03T09:20:27Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: 45e10d31048d927ee6546e35b050914f0e6e21a4dee298b3b277eebe7c133732
  source_path: start/wizard.md
  workflow: 15
---

# Assistant de configuration (CLI)

L'assistant de configuration est la méthode **recommandée** pour configurer OpenClaw sur macOS, Linux ou Windows (via WSL2 ; fortement recommandé).
Il peut configurer une connexion Gateway locale ou distante, ainsi que les valeurs par défaut des canaux, Skills et espaces de travail dans un processus guidé.

Point d'entrée principal :

```bash
openclaw onboard
```

Le moyen le plus rapide de commencer à discuter : ouvrez le tableau de bord (aucune configuration de canal requise). Exécutez `openclaw dashboard` et discutez dans le navigateur. Documentation : [Tableau de bord](/web/dashboard).

Reconfiguration ultérieure :

```bash
openclaw configure
```

Recommandé : configurez la clé API Brave Search pour que les agents puissent utiliser `web_search` (`web_fetch` ne nécessite pas de clé). Le moyen le plus simple : `openclaw configure --section web`, qui stockera `tools.web.search.apiKey`. Documentation : [Outils Web](/tools/web).

## Démarrage rapide vs Avancé

L'assistant commence par **Démarrage rapide** (valeurs par défaut) vs **Avancé** (contrôle total).

**Démarrage rapide** conserve les valeurs par défaut :

- Gateway locale (loopback)
- Espace de travail par défaut (ou espace de travail existant)
- Port Gateway **18789**
- Authentification Gateway **Token** (généré automatiquement, même sur loopback)
- Exposition Tailscale **désactivée**
- Telegram + WhatsApp messages privés utilisent par défaut une **liste d'autorisation** (le système vous demandera d'entrer un numéro de téléphone)

**Avancé** expose chaque étape (mode, espace de travail, Gateway, canaux, démon, Skills).

## Ce que fait l'assistant

**Mode local (par défaut)** vous guide à travers :

- Modèle/authentification (OAuth d'abonnement OpenAI Code (Codex), clé API Anthropic (recommandée) ou setup-token (coller), ainsi que les options MiniMax/GLM/Moonshot/AI Gateway)
- Emplacement de l'espace de travail + fichiers d'amorçage
- Paramètres Gateway (port/liaison/authentification/tailscale)
- Fournisseurs (Telegram, WhatsApp, Discord, Google Chat, Mattermost (plugin), Signal)
- Installation du démon (LaunchAgent / unité utilisateur systemd)
- Vérification de santé
- Skills (recommandé)

**Mode distant** configure uniquement la connexion du client local à une Gateway située ailleurs.
Il **ne** installe ni ne modifie rien sur l'hôte distant.

Pour ajouter d'autres agents isolés (espace de travail indépendant + sessions + authentification), utilisez :

```bash
openclaw agents add <name>
```

Conseil : `--json` **ne** signifie pas le mode non-interactif. Pour les scripts, utilisez `--non-interactive` (et `--workspace`).

## Détails du processus (local)

1. **Détection de la configuration existante**
   - Si `~/.openclaw/openclaw.json` existe, choisissez **Conserver / Modifier / Réinitialiser**.
   - Réexécuter l'assistant **ne** efface rien, sauf si vous choisissez explicitement **Réinitialiser** (ou passez `--reset`).
   - Si la configuration est invalide ou contient des noms de clés hérités, l'assistant s'arrête et vous demande d'exécuter `openclaw doctor` avant de continuer.
   - La réinitialisation utilise `trash` (jamais `rm`) et offre des options de portée :
     - Configuration uniquement
     - Configuration + identifiants + sessions
     - Réinitialisation complète (supprime également l'espace de travail)

2. **Modèle/authentification**
   - **Clé API Anthropic (recommandée)** : utilise `ANTHROPIC_API_KEY` s'il existe, sinon vous demande la clé, puis la sauvegarde pour le démon.
   - **OAuth Anthropic (Claude Code CLI)** : sur macOS, l'assistant vérifie l'élément du trousseau "Claude Code-credentials" (sélectionnez "Toujours autoriser" pour que le lancement par launchd ne soit pas bloqué) ; sur Linux/Windows, réutilise `~/.claude/.credentials.json` s'il existe.
   - **Token Anthropic (coller setup-token)** : exécutez `claude setup-token` sur n'importe quelle machine, puis collez le token (vous pouvez le nommer ; vide = par défaut).
   - **Abonnement OpenAI Code (Codex) (CLI Codex)** : si `~/.codex/auth.json` existe, l'assistant peut le réutiliser.
   - **Abonnement OpenAI Code (Codex) (OAuth)** : flux de navigateur ; collez `code#state`.
     - Lorsque le modèle n'est pas défini ou est `openai/*`, définissez `agents.defaults.model` sur `openai-codex/gpt-5.2`.
   - **Clé API OpenAI** : utilise `OPENAI_API_KEY` s'il existe, sinon vous demande la clé, puis la sauvegarde dans `~/.openclaw/.env` pour que launchd puisse la lire.
   - **OpenCode Zen (agent multi-modèles)** : vous demande `OPENCODE_API_KEY` (ou `OPENCODE_ZEN_API_KEY`, obtenu sur https://opencode.ai/auth).
   - **Clé API** : stocke la clé pour vous.
   - **Vercel AI Gateway (agent multi-modèles)** : vous demande `AI_GATEWAY_API_KEY`.
   - Plus de détails : [Vercel AI Gateway](/providers/vercel-ai-gateway)
   - **MiniMax M2.1** : écrit automatiquement la configuration.
   - Plus de détails : [MiniMax](/providers/minimax)
   - **Synthetic (compatible Anthropic)** : vous demande `SYNTHETIC_API_KEY`.
   - Plus de détails : [Synthetic](/providers/synthetic)
   - **Moonshot (Kimi K2)** : écrit automatiquement la configuration.
   - **Kimi Coding** : écrit automatiquement la configuration.
   - Plus de détails : [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)
   - **Ignorer** : authentification pas encore configurée.
   - Sélectionnez le modèle par défaut parmi les options détectées (ou entrez manuellement le fournisseur/modèle).
   - L'assistant exécute une vérification du modèle et avertit si le modèle configuré est inconnu ou si l'authentification est manquante.

- Les identifiants OAuth sont stockés dans `~/.openclaw/credentials/oauth.json` ; les fichiers de configuration d'authentification sont stockés dans `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (clés API + OAuth).
- Plus de détails : [/concepts/oauth](/concepts/oauth)

3. **Espace de travail**
   - Par défaut `~/.openclaw/workspace` (configurable).
   - Amorce les fichiers d'espace de travail nécessaires pour la cérémonie d'orientation de l'agent.
   - Disposition complète de l'espace de travail + guide de sauvegarde : [Espace de travail de l'agent](/concepts/agent-workspace)

4. **Gateway**
   - Port, liaison, mode d'authentification, exposition tailscale.
   - Recommandation d'authentification : conservez **Token** même pour loopback, afin que les clients WS locaux doivent s'authentifier.
   - Désactivez l'authentification uniquement si vous faites entièrement confiance à chaque processus local.
   - Les liaisons non-loopback nécessitent toujours l'authentification.

5. **Canaux**
   - [WhatsApp](/channels/whatsapp) : connexion par code QR optionnelle.
   - [Telegram](/channels/telegram) : token de bot.
   - [Discord](/channels/discord) : token de bot.
   - [Google Chat](/channels/googlechat) : JSON de compte de service + audience webhook.
   - [Mattermost](/channels/mattermost) (plugin) : token de bot + URL de base.
   - [Signal](/channels/signal) : installation optionnelle de `signal-cli` + configuration de compte.
   - [iMessage](/channels/imessage) : chemin CLI `imsg` local + accès à la base de données.
   - Sécurité des messages privés : par défaut appairage. Le premier message privé envoie un code de vérification ; approuvez via `openclaw pairing approve <channel> <code>` ou utilisez une liste d'autorisation.

6. **Installation du démon**
   - macOS : LaunchAgent
     - Nécessite une session utilisateur connectée ; pour les environnements sans interface graphique, utilisez un LaunchDaemon personnalisé (non fourni).
   - Linux (et Windows via WSL2) : unité utilisateur systemd
     - L'assistant tente d'activer lingering via `loginctl enable-linger <user>` pour que Gateway reste en cours d'exécution après la déconnexion.
     - Peut demander sudo (écrire dans `/var/lib/systemd/linger`) ; essaie d'abord sans sudo.
   - **Choix du runtime :** Node (recommandé ; requis pour WhatsApp/Telegram). **Non recommandé** Bun.

7. **Vérification de santé**
   - Lance Gateway (si nécessaire) et exécute `openclaw health`.
   - Conseil : `openclaw status --deep` ajoute des sondes de santé Gateway à la sortie d'état (nécessite une Gateway accessible).

8. **Skills (recommandé)**
   - Lit les Skills disponibles et vérifie les exigences.
   - Vous permet de choisir le gestionnaire de nœuds : **npm / pnpm** (bun non recommandé).
   - Installe les dépendances optionnelles (certaines utilisent Homebrew sur macOS).

9. **Achèvement**
   - Résumé + étapes suivantes, y compris les applications iOS/Android/macOS pour des fonctionnalités supplémentaires.

- Si aucune interface graphique n'est détectée, l'assistant imprime les instructions de redirection de port SSH pour le tableau de bord au lieu d'ouvrir le navigateur.
- Si les ressources du tableau de bord sont manquantes, l'assistant tente de les construire ; le plan de secours est `pnpm ui:build` (installe automatiquement les dépendances de l'interface utilisateur).

## Mode distant

Le mode distant configure la connexion du client local à une Gateway située ailleurs.

Ce que vous allez configurer :

- URL Gateway distante (`ws://...`)
- Token si la Gateway distante nécessite une authentification (recommandé)

Points à noter :

- N'effectue pas d'installation distante ou de modifications de démon.
- Si Gateway est limité à loopback, utilisez un tunnel SSH ou tailnet.
- Conseils de découverte :
  - macOS : Bonjour (`dns-sd`)
  - Linux : Avahi (`avahi-browse`)

## Ajouter un autre agent

Utilisez `openclaw agents add <name>` pour créer un agent séparé avec un espace de travail indépendant, des sessions et un profil de configuration d'authentification. L'exécution sans `--workspace` lance l'assistant.

Ce qu'il configure :

- `agents.list[].name`
- `agents.list[].workspace`
- `agents.list[].agentDir`

Points à noter :

- L'espace de travail par défaut suit `~/.openclaw/workspace-<agentId>`.
- Ajoutez `bindings` pour acheminer les messages entrants (l'assistant peut le faire).
- Drapeaux non-interactifs : `--model`, `--agent-dir`, `--bind`, `--non-interactive`.

## Mode non-interactif

Utilisez `--non-interactive` pour automatiser ou scripter l'assistant :

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

Ajoutez `--json` pour un résumé lisible par machine.

Exemple Gemini :

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemple Z.AI :

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice zai-api-key \
  --zai-api-key "$ZAI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemple Vercel AI Gateway :

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemple Moonshot :

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice moonshot-api-key \
  --moonshot-api-key "$MOONSHOT_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemple Synthetic :

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice synthetic-api-key \
  --synthetic-api-key "$SYNTHETIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemple OpenCode Zen :

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice opencode-zen \
  --opencode-zen-api-key "$OPENCODE_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemple d'ajout d'agent (non-interactif)
