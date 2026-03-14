```markdown
---
summary: "Référence complète pour l'assistant d'intégration CLI : chaque étape, drapeau et champ de configuration"
read_when:
  - Looking up a specific wizard step or flag
  - Automating onboarding with non-interactive mode
  - Debugging wizard behavior
title: "Référence de l'assistant d'intégration"
sidebarTitle: "Référence de l'assistant"
---

# Référence de l'assistant d'intégration

Ceci est la référence complète pour l'assistant CLI `openclaw onboard`.
Pour un aperçu de haut niveau, voir [Assistant d'intégration](/start/wizard).

## Détails du flux (mode local)

<Steps>
  <Step title="Détection de la configuration existante">
    - Si `~/.openclaw/openclaw.json` existe, choisissez **Conserver / Modifier / Réinitialiser**.
    - Réexécuter l'assistant ne supprime rien à moins que vous ne choisissiez explicitement **Réinitialiser**
      (ou que vous passiez `--reset`).
    - Le CLI `--reset` par défaut est `config+creds+sessions` ; utilisez `--reset-scope full`
      pour supprimer également l'espace de travail.
    - Si la configuration est invalide ou contient des clés héritées, l'assistant s'arrête et vous demande
      d'exécuter `openclaw doctor` avant de continuer.
    - La réinitialisation utilise `trash` (jamais `rm`) et offre des portées :
      - Configuration uniquement
      - Configuration + identifiants + sessions
      - Réinitialisation complète (supprime également l'espace de travail)
  </Step>
  <Step title="Modèle/Authentification">
    - **Clé API Anthropic** : utilise `ANTHROPIC_API_KEY` si présente ou demande une clé, puis l'enregistre pour l'utilisation du daemon.
    - **OAuth Anthropic (Claude Code CLI)** : sur macOS, l'assistant vérifie l'élément Keychain « Claude Code-credentials » (choisissez « Toujours autoriser » pour que les démarrages launchd ne se bloquent pas) ; sur Linux/Windows, il réutilise `~/.claude/.credentials.json` s'il est présent.
    - **Jeton Anthropic (coller setup-token)** : exécutez `claude setup-token` sur n'importe quelle machine, puis collez le jeton (vous pouvez le nommer ; vide = par défaut).
    - **Abonnement OpenAI Code (Codex) (CLI Codex)** : si `~/.codex/auth.json` existe, l'assistant peut le réutiliser.
    - **Abonnement OpenAI Code (Codex) (OAuth)** : flux de navigateur ; collez le `code#state`.
      - Définit `agents.defaults.model` sur `openai-codex/gpt-5.2` lorsque le modèle n'est pas défini ou est `openai/*`.
    - **Clé API OpenAI** : utilise `OPENAI_API_KEY` si présente ou demande une clé, puis la stocke dans les profils d'authentification.
    - **Clé API xAI (Grok)** : demande `XAI_API_KEY` et configure xAI comme fournisseur de modèle.
    - **OpenCode** : demande `OPENCODE_API_KEY` (ou `OPENCODE_ZEN_API_KEY`, obtenez-la sur https://opencode.ai/auth) et vous permet de choisir le catalogue Zen ou Go.
    - **Ollama** : demande l'URL de base Ollama, offre le mode **Cloud + Local** ou **Local**, découvre les modèles disponibles et tire automatiquement le modèle local sélectionné si nécessaire.
    - Plus de détails : [Ollama](/providers/ollama)
    - **Clé API** : stocke la clé pour vous.
    - **Vercel AI Gateway (proxy multi-modèle)** : demande `AI_GATEWAY_API_KEY`.
    - Plus de détails : [Vercel AI Gateway](/providers/vercel-ai-gateway)
    - **Cloudflare AI Gateway** : demande l'ID de compte, l'ID de passerelle et `CLOUDFLARE_AI_GATEWAY_API_KEY`.
    - Plus de détails : [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)
    - **MiniMax M2.5** : la configuration est écrite automatiquement.
    - Plus de détails : [MiniMax](/providers/minimax)
    - **Synthetic (compatible Anthropic)** : demande `SYNTHETIC_API_KEY`.
    - Plus de détails : [Synthetic](/providers/synthetic)
    - **Moonshot (Kimi K2)** : la configuration est écrite automatiquement.
    - **Kimi Coding** : la configuration est écrite automatiquement.
    - Plus de détails : [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)
    - **Ignorer** : aucune authentification configurée pour le moment.
    - Choisissez un modèle par défaut parmi les options détectées (ou entrez le fournisseur/modèle manuellement). Pour la meilleure qualité et un risque d'injection de prompt plus faible, choisissez le modèle de dernière génération le plus puissant disponible dans votre pile de fournisseurs.
    - L'assistant exécute une vérification de modèle et avertit si le modèle configuré est inconnu ou manque d'authentification.
    - Le mode de stockage des clés API par défaut est les valeurs de profil d'authentification en texte brut. Utilisez `--secret-input-mode ref` pour stocker des références soutenues par env à la place (par exemple `keyRef: { source: "env", provider: "default", id: "OPENAI_API_KEY" }`).
    - Les identifiants OAuth se trouvent dans `~/.openclaw/credentials/oauth.json` ; les profils d'authentification se trouvent dans `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (clés API + OAuth).
    - Plus de détails : [/concepts/oauth](/concepts/oauth)
    <Note>
    Conseil sans tête/serveur : complétez OAuth sur une machine avec un navigateur, puis copiez
    `~/.openclaw/credentials/oauth.json` (ou `$OPENCLAW_STATE_DIR/credentials/oauth.json`) vers l'hôte
    de la passerelle.
    </Note>
  </Step>
  <Step title="Espace de travail">
    - Par défaut `~/.openclaw/workspace` (configurable).
    - Amorce les fichiers d'espace de travail nécessaires pour le rituel d'amorçage de l'agent.
    - Disposition complète de l'espace de travail + guide de sauvegarde : [Espace de travail de l'agent](/concepts/agent-workspace)
  </Step>
  <Step title="Passerelle">
    - Port, liaison, mode d'authentification, exposition tailscale.
    - Recommandation d'authentification : conservez **Jeton** même pour la boucle locale afin que les clients WS locaux doivent s'authentifier.
    - En mode jeton, l'intégration interactive offre :
      - **Générer/stocker le jeton en texte brut** (par défaut)
      - **Utiliser SecretRef** (opt-in)
      - Quickstart réutilise les SecretRefs `gateway.auth.token` existants dans les fournisseurs `env`, `file` et `exec` pour l'amorçage de la sonde d'intégration/tableau de bord.
      - Si ce SecretRef est configuré mais ne peut pas être résolu, l'intégration échoue tôt avec un message de correction clair au lieu de se dégrader silencieusement à l'authentification d'exécution.
    - En mode mot de passe, l'intégration interactive supporte également le stockage en texte brut ou SecretRef.
    - Chemin SecretRef de jeton non-interactif : `--gateway-token-ref-env <ENV_VAR>`.
      - Nécessite une variable env non vide dans l'environnement du processus d'intégration.
      - Ne peut pas être combiné avec `--gateway-token`.
    - Désactivez l'authentification uniquement si vous faites entièrement confiance à chaque processus local.
    - Les liaisons non-loopback nécessitent toujours l'authentification.
  </Step>
  <Step title="Canaux">
    - [WhatsApp](/channels/whatsapp) : connexion QR optionnelle.
    - [Telegram](/channels/telegram) : jeton de bot.
    - [Discord](/channels/discord) : jeton de bot.
    - [Google Chat](/channels/googlechat) : JSON de compte de service + audience de webhook.
    - [Mattermost](/channels/mattermost) (plugin) : jeton de bot + URL de base.
    - [Signal](/channels/signal) : installation optionnelle de `signal-cli` + configuration de compte.
    - [BlueBubbles](/channels/bluebubbles) : **recommandé pour iMessage** ; URL du serveur + mot de passe + webhook.
    - [iMessage](/channels/imessage) : chemin CLI `imsg` hérité + accès à la base de données.
    - Sécurité des DM : par défaut l'appairage. Le premier DM envoie un code ; approuvez via `openclaw pairing approve <channel> <code>` ou utilisez des listes d'autorisation.
  </Step>
  <Step title="Recherche web">
    - Choisissez un fournisseur : Perplexity, Brave, Gemini, Grok ou Kimi (ou ignorer).
    - Collez votre clé API (QuickStart détecte automatiquement les clés des variables env ou de la configuration existante).
    - Ignorer avec `--skip-search`.
    - Configurer plus tard : `openclaw configure --section web`.
  </Step>
  <Step title="Installation du daemon">
    - macOS : LaunchAgent
      - Nécessite une session utilisateur connectée ; pour sans tête, utilisez un LaunchDaemon personnalisé (non fourni).
    - Linux (et Windows via WSL2) : unité utilisateur systemd
      - L'assistant tente d'activer la persistance via `loginctl enable-linger <user>` pour que la passerelle reste active après la déconnexion.
      - Peut demander sudo (écrit `/var/lib/systemd/linger`) ; il essaie d'abord sans sudo.
    - **Sélection d'exécution :** Node (recommandé ; requis pour WhatsApp/Telegram). Bun n'est **pas recommandé**.
    - Si l'authentification par jeton nécessite un jeton et que `gateway.auth.token` est géré par SecretRef, l'installation du daemon le valide mais ne persiste pas les valeurs de jeton en texte brut résolues dans les métadonnées d'environnement du service superviseur.
    - Si l'authentification par jeton nécessite un jeton et que le SecretRef de jeton configuré n'est pas résolu, l'installation du daemon est bloquée avec des conseils exploitables.
    - Si `gateway.auth.token` et `gateway.auth.password` sont tous deux configurés et que `gateway.auth.mode` n'est pas défini, l'installation du daemon est bloquée jusqu'à ce que le mode soit défini explicitement.
  </Step>
  <Step title="Vérification de santé">
    - Démarre la passerelle (si nécessaire) et exécute `openclaw health`.
    - Conseil : `openclaw status --deep` ajoute les sondes de santé de la passerelle à la sortie d'état (nécessite une passerelle accessible).
  </Step>
  <Step title="Compétences (recommandé)">
    - Lit les compétences disponibles et vérifie les exigences.
    - Vous permet de choisir un gestionnaire de nœuds : **npm / pnpm** (bun non recommandé).
    - Installe les dépendances optionnelles (certaines utilisent Homebrew sur macOS).
  </Step>
  <Step title="Terminer">
    - Résumé + étapes suivantes, y compris les applications iOS/Android/macOS pour des fonctionnalités supplémentaires.
  </Step>
</Steps>

<Note>
Si aucune interface graphique n'est détectée, l'assistant imprime les instructions de redirection de port SSH pour l'interface utilisateur de contrôle au lieu d'ouvrir un navigateur.
Si les ressources de l'interface utilisateur de contrôle sont manquantes, l'assistant tente de les construire ; le recours est `pnpm ui:build` (installe automatiquement les dépendances de l'interface utilisateur).
</Note>

## Mode non-interactif

Utilisez `--non-interactive` pour automatiser ou scripter l'intégration :

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

SecretRef de jeton de passerelle en mode non-interactif :

```bash
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN
```

`--gateway-token` et `--gateway-token-ref-env` s'excluent mutuellement.

<Note>
`--json` n'implique **pas** le mode non-interactif. Utilisez `--non-interactive` (et `--workspace`) pour les scripts.
</Note>

Les exemples de commandes spécifiques au fournisseur se trouvent dans [Automatisation CLI](/start/wizard-cli-automation#provider-specific-examples).
Utilisez cette page de référence pour la sémantique des drapeaux et l'ordre des étapes.

### Ajouter un agent (non-interactif)

```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.2 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

## RPC de l'assistant de passerelle

La passerelle expose le flux de l'assistant sur RPC (`wizard.start`, `wizard.next`, `wizard.cancel`, `wizard.status`).
Les clients (application macOS, interface utilisateur de contrôle) peuvent afficher les étapes sans réimplémenter la logique d'intégration.

## Configuration de Signal (signal-cli)

L'assistant peut installer `signal-cli` à partir des versions GitHub :

- Télécharge l'actif de version approprié.
- Le stocke sous `~/.openclaw/tools/signal-cli/<version>/`.
- Écrit `channels.signal.cliPath` dans votre configuration.

Remarques :

- Les builds JVM nécessitent **Java 21**.
- Les builds natifs sont utilisés lorsqu'ils sont disponibles.
- Windows utilise WSL2 ; l'installation de signal-cli suit le flux Linux à l'intérieur de WSL.

## Ce que l'assistant écrit

Champs typiques dans `~/.openclaw/openclaw.json` :

- `agents.defaults.workspace`
- `agents.defaults.model` / `models.providers` (si MiniMax est choisi)
- `tools.profile` (l'intégration locale par défaut est `"coding"` lorsqu'il n'est pas défini ; les valeurs explicites existantes sont préservées)
- `gateway.*` (mode, liaison, authentification, tailscale)
- `session.dmScope` (détails du comportement : [Référence d'intégration CLI](/start/wizard-cli-reference#outputs-and-internals))
- `channels.telegram.botToken`, `channels.discord.token`, `channels.signal.*`, `channels.imessage.*`
- Listes d'autorisation de canaux (Slack/Discord/Matrix/Microsoft Teams) lorsque vous optez pour cela lors des invites (les noms se résolvent en ID si possible).
- `skills.install.nodeManager`
- `wizard.lastRunAt`
- `wizard.lastRunVersion`
- `wizard.lastRunCommit`
- `wizard.lastRunCommand`
- `wizard.lastRunMode`

`openclaw agents add` écrit `agents.list[]` et `bindings` optionnel.

Les identifiants WhatsApp vont sous `~/.openclaw/credentials/whatsapp/<accountId>/`.
Les sessions sont stockées sous `~/.openclaw/agents/<agentId>/sessions/`.

Certains canaux sont livrés en tant que plugins. Lorsque vous en choisissez un lors de l'intégration, l'assistant
vous demandera de l'installer (npm ou un chemin local) avant qu'il puisse être configuré.
```

## Docs connexes

- Aperçu de l'assistant : [Assistant d'intégration](/start/wizard)
- Intégration de l'application macOS : [Intégration](/start/onboarding)
- Référence de configuration : [Configuration de la passerelle](/gateway/configuration)
- Fournisseurs : [WhatsApp](/channels/whatsapp), [Telegram](/channels/telegram), [Discord](/channels/discord), [Google Chat](/channels/googlechat), [Signal](/channels/signal), [BlueBubbles](/channels/bluebubbles) (iMessage), [iMessage](/channels/imessage) (hérité)
- Compétences : [Compétences](/tools/skills), [Configuration des compétences](/tools/skills-config)
