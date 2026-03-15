---
summary: "Référence complète pour le flux d'intégration CLI, configuration auth/modèle, sorties et éléments internes"
read_when:
  - You need detailed behavior for openclaw onboard
  - You are debugging onboarding results or integrating onboarding clients
title: "Référence d'intégration CLI"
sidebarTitle: "Référence CLI"
---

# Référence d'intégration CLI

Cette page est la référence complète pour `openclaw onboard`.
Pour le guide court, voir [Assistant d'intégration (CLI)](/start/wizard).

## Ce que fait l'assistant

Le mode local (par défaut) vous guide à travers :

- Configuration du modèle et de l'authentification (abonnement OpenAI Code OAuth, clé API Anthropic ou jeton de configuration, plus options MiniMax, GLM, Ollama, Moonshot et AI Gateway)
- Localisation de l'espace de travail et fichiers d'amorçage
- Paramètres de passerelle (port, liaison, authentification, tailscale)
- Canaux et fournisseurs (Telegram, WhatsApp, Discord, Google Chat, plugin Mattermost, Signal)
- Installation du démon (LaunchAgent ou unité utilisateur systemd)
- Vérification de santé
- Configuration des compétences

Le mode distant configure cette machine pour se connecter à une passerelle ailleurs.
Il n'installe ni ne modifie rien sur l'hôte distant.

## Détails du flux local

<Steps>
  <Step title="Détection de configuration existante">
    - Si `~/.openclaw/openclaw.json` existe, choisissez Conserver, Modifier ou Réinitialiser.
    - Réexécuter l'assistant n'efface rien sauf si vous choisissez explicitement Réinitialiser (ou passez `--reset`).
    - CLI `--reset` par défaut à `config+creds+sessions` ; utilisez `--reset-scope full` pour supprimer également l'espace de travail.
    - Si la configuration est invalide ou contient des clés héritées, l'assistant s'arrête et vous demande d'exécuter `openclaw doctor` avant de continuer.
    - La réinitialisation utilise `trash` et offre des portées :
      - Configuration uniquement
      - Configuration + identifiants + sessions
      - Réinitialisation complète (supprime également l'espace de travail)
  </Step>
  <Step title="Modèle et authentification">
    - La matrice complète des options se trouve dans [Options d'authentification et de modèle](#options-dauthentification-et-de-modèle).
  </Step>
  <Step title="Espace de travail">
    - Par défaut `~/.openclaw/workspace` (configurable).
    - Amorce les fichiers d'espace de travail nécessaires pour le rituel d'amorçage du premier lancement.
    - Disposition de l'espace de travail : [Espace de travail agent](/concepts/agent-workspace).
  </Step>
  <Step title="Passerelle">
    - Demande le port, la liaison, le mode d'authentification et l'exposition tailscale.
    - Recommandé : gardez l'authentification par jeton activée même pour la boucle locale afin que les clients WS locaux doivent s'authentifier.
    - En mode jeton, l'intégration interactive offre :
      - **Générer/stocker le jeton en texte brut** (par défaut)
      - **Utiliser SecretRef** (opt-in)
    - En mode mot de passe, l'intégration interactive supporte également le stockage en texte brut ou SecretRef.
    - Chemin SecretRef jeton non-interactif : `--gateway-token-ref-env <ENV_VAR>`.
      - Nécessite une variable d'environnement non vide dans l'environnement du processus d'intégration.
      - Ne peut pas être combiné avec `--gateway-token`.
    - Désactivez l'authentification uniquement si vous faites entièrement confiance à chaque processus local.
    - Les liaisons non-boucle nécessitent toujours l'authentification.
  </Step>
  <Step title="Canaux">
    - [WhatsApp](/channels/whatsapp): connexion QR optionnelle
    - [Telegram](/channels/telegram): jeton bot
    - [Discord](/channels/discord): jeton bot
    - [Google Chat](/channels/googlechat): JSON de compte de service + audience webhook
    - [Plugin Mattermost](/channels/mattermost) : jeton bot + URL de base
    - [Signal](/channels/signal): installation `signal-cli` optionnelle + configuration de compte
    - [BlueBubbles](/channels/bluebubbles): recommandé pour iMessage ; URL du serveur + mot de passe + webhook
    - [iMessage](/channels/imessage): chemin CLI `imsg` hérité + accès à la base de données
    - Sécurité DM : par défaut l'appairage. Le premier DM envoie un code ; approuvez via
      `openclaw pairing approve <channel> <code>` ou utilisez des listes d'autorisation.
  </Step>
  <Step title="Installation du démon">
    - macOS : LaunchAgent
      - Nécessite une session utilisateur connectée ; pour sans interface, utilisez un LaunchDaemon personnalisé (non fourni).
    - Linux et Windows via WSL2 : unité utilisateur systemd
      - L'assistant tente `loginctl enable-linger <user>` afin que la passerelle reste active après la déconnexion.
      - Peut demander sudo (écrit `/var/lib/systemd/linger`) ; il essaie d'abord sans sudo.
    - Sélection du runtime : Node (recommandé ; requis pour WhatsApp et Telegram). Bun n'est pas recommandé.
  </Step>
  <Step title="Vérification de santé">
    - Démarre la passerelle (si nécessaire) et exécute `openclaw health`.
    - `openclaw status --deep` ajoute des sondes de santé de passerelle à la sortie de statut.
  </Step>
  <Step title="Compétences">
    - Lit les compétences disponibles et vérifie les exigences.
    - Vous permet de choisir le gestionnaire de nœuds : npm ou pnpm (bun non recommandé).
    - Installe les dépendances optionnelles (certaines utilisent Homebrew sur macOS).
  </Step>
  <Step title="Fin">
    - Résumé et prochaines étapes, y compris les options d'application iOS, Android et macOS.
  </Step>
</Steps>

<Note>
Si aucune interface graphique n'est détectée, l'assistant imprime les instructions de redirection de port SSH pour l'interface de contrôle au lieu d'ouvrir un navigateur.
Si les ressources de l'interface de contrôle sont manquantes, l'assistant tente de les construire ; le repli est `pnpm ui:build` (installe automatiquement les dépendances UI).
</Note>

## Détails du mode distant

Le mode distant configure cette machine pour se connecter à une passerelle ailleurs.

<Info>
Le mode distant n'installe ni ne modifie rien sur l'hôte distant.
</Info>

Ce que vous définissez :

- URL de la passerelle distante (`ws://...`)
- Jeton si l'authentification de la passerelle distante est requise (recommandé)

<Note>
- Si la passerelle est boucle uniquement, utilisez le tunneling SSH ou un tailnet.
- Indices de découverte :
  - macOS : Bonjour (`dns-sd`)
  - Linux : Avahi (`avahi-browse`)
</Note>

## Options d'authentification et de modèle

<AccordionGroup>
  <Accordion title="Clé API Anthropic">
    Utilise `ANTHROPIC_API_KEY` s'il est présent ou demande une clé, puis l'enregistre pour utilisation par le démon.
  </Accordion>
  <Accordion title="OAuth Anthropic (Claude Code CLI)">
    - macOS : vérifie l'élément Keychain "Claude Code-credentials"
    - Linux et Windows : réutilise `~/.claude/.credentials.json` s'il est présent

    Sur macOS, choisissez "Toujours autoriser" afin que les démarrages launchd ne se bloquent pas.

  </Accordion>
  <Accordion title="Jeton Anthropic (collage de jeton de configuration)">
    Exécutez `claude setup-token` sur n'importe quelle machine, puis collez le jeton.
    Vous pouvez le nommer ; vide utilise la valeur par défaut.
  </Accordion>
  <Accordion title="Abonnement OpenAI Code (réutilisation Codex CLI)">
    Si `~/.codex/auth.json` existe, l'assistant peut le réutiliser.
  </Accordion>
  <Accordion title="Abonnement OpenAI Code (OAuth)">
    Flux navigateur ; collez `code#state`.

    Définit `agents.defaults.model` à `openai-codex/gpt-5.4` lorsque le modèle n'est pas défini ou `openai/*`.

  </Accordion>
  <Accordion title="Clé API OpenAI">
    Utilise `OPENAI_API_KEY` s'il est présent ou demande une clé, puis stocke l'identifiant dans les profils d'authentification.

    Définit `agents.defaults.model` à `openai/gpt-5.1-codex` lorsque le modèle n'est pas défini, `openai/*`, ou `openai-codex/*`.

  </Accordion>
  <Accordion title="Clé API xAI (Grok)">
    Demande `XAI_API_KEY` et configure xAI comme fournisseur de modèle.
  </Accordion>
  <Accordion title="OpenCode">
    Demande `OPENCODE_API_KEY` (ou `OPENCODE_ZEN_API_KEY`) et vous permet de choisir le catalogue Zen ou Go.
    URL de configuration : [opencode.ai/auth](https://opencode.ai/auth).
  </Accordion>
  <Accordion title="Clé API (générique)">
    Stocke la clé pour vous.
  </Accordion>
  <Accordion title="Passerelle AI Vercel">
    Demande `AI_GATEWAY_API_KEY`.
    Plus de détails : [Passerelle AI Vercel](/providers/vercel-ai-gateway).
  </Accordion>
  <Accordion title="Passerelle AI Cloudflare">
    Demande l'ID de compte, l'ID de passerelle et `CLOUDFLARE_AI_GATEWAY_API_KEY`.
    Plus de détails : [Passerelle AI Cloudflare](/providers/cloudflare-ai-gateway).
  </Accordion>
  <Accordion title="MiniMax M2.5">
    La configuration est écrite automatiquement.
    Plus de détails : [MiniMax](/providers/minimax).
  </Accordion>
  <Accordion title="Synthétique (compatible Anthropic)">
    Demande `SYNTHETIC_API_KEY`.
    Plus de détails : [Synthétique](/providers/synthetic).
  </Accordion>
  <Accordion title="Ollama (Modèles ouverts Cloud et locaux)">
    Demande l'URL de base (par défaut `http://127.0.0.1:11434`), puis offre le mode Cloud + Local ou Local uniquement.
    Découvre les modèles disponibles et suggère les valeurs par défaut.
    Plus de détails : [Ollama](/providers/ollama).
  </Accordion>
  <Accordion title="Moonshot et Kimi Coding">
    Les configurations Moonshot (Kimi K2) et Kimi Coding sont écrites automatiquement.
    Plus de détails : [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot).
  </Accordion>
  <Accordion title="Fournisseur personnalisé">
    Fonctionne avec les points de terminaison compatibles OpenAI et Anthropic.

    L'intégration interactive supporte les mêmes choix de stockage de clé API que les autres flux de clé API de fournisseur :
    - **Coller la clé API maintenant** (texte brut)
    - **Utiliser une référence secrète** (référence env ou référence fournisseur configurée, avec validation préalable)

    Drapeaux non-interactifs :
    - `--auth-choice custom-api-key`
    - `--custom-base-url`
    - `--custom-model-id`
    - `--custom-api-key` (optionnel ; repli à `CUSTOM_API_KEY`)
    - `--custom-provider-id` (optionnel)
    - `--custom-compatibility <openai|anthropic>` (optionnel ; par défaut `openai`)

  </Accordion>
  <Accordion title="Ignorer">
    Laisse l'authentification non configurée.
  </Accordion>
</AccordionGroup>

Comportement du modèle :

- Choisissez le modèle par défaut parmi les options détectées, ou entrez le fournisseur et le modèle manuellement.
- L'assistant exécute une vérification de modèle et avertit si le modèle configuré est inconnu ou manque d'authentification.

Chemins des identifiants et profils :

- Identifiants OAuth : `~/.openclaw/credentials/oauth.json`
- Profils d'authentification (clés API + OAuth) : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

Mode de stockage des identifiants :

- Le comportement d'intégration par défaut persiste les clés API comme valeurs en texte brut dans les profils d'authentification.
- `--secret-input-mode ref` active le mode référence au lieu du stockage de clé en texte brut.
  Dans l'intégration interactive, vous pouvez choisir l'un ou l'autre :
  - référence de variable d'environnement (par exemple `keyRef: { source: "env", provider: "default", id: "OPENAI_API_KEY" }`)
  - référence fournisseur configurée (`file` ou `exec`) avec alias fournisseur + id
- Le mode référence interactif exécute une validation préalable rapide avant d'enregistrer.
  - Références env : valide le nom de variable + valeur non vide dans l'environnement d'intégration actuel.
  - Références fournisseur : valide la configuration du fournisseur et résout l'id demandé.
  - Si la validation préalable échoue, l'intégration affiche l'erreur et vous permet de réessayer.
- En mode non-interactif, `--secret-input-mode ref` est soutenu par env uniquement.
  - Définissez la variable d'environnement du fournisseur dans l'environnement du processus d'intégration.
  - Les drapeaux de clé en ligne (par exemple `--openai-api-key`) nécessitent que cette variable d'environnement soit définie ; sinon l'intégration échoue rapidement.
  - Pour les fournisseurs personnalisés, le mode `ref` non-interactif stocke `models.providers.<id>.apiKey` comme `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`.
  - Dans ce cas de fournisseur personnalisé, `--custom-api-key` nécessite que `CUSTOM_API_KEY` soit défini ; sinon l'intégration échoue rapidement.
- Les identifiants d'authentification de passerelle supportent les choix texte brut et SecretRef dans l'intégration interactive :
  - Mode jeton : **Générer/stocker le jeton en texte brut** (par défaut) ou **Utiliser SecretRef**.
  - Mode mot de passe : texte brut ou SecretRef.
- Chemin SecretRef jeton non-interactif : `--gateway-token-ref-env <ENV_VAR>`.
- Les configurations en texte brut existantes continuent de fonctionner sans modification.

<Note>
Conseil sans interface et serveur : complétez OAuth sur une machine avec un navigateur, puis copiez
`~/.openclaw/credentials/oauth.json` (ou `$OPENCLAW_STATE_DIR/credentials/oauth.json`)
vers l'hôte de la passerelle.
</Note>

## Sorties et éléments internes

Champs typiques dans `~/.openclaw/openclaw.json` :

- `agents.defaults.workspace`
- `agents.defaults.model` / `models.providers` (si Minimax est choisi)
- `tools.profile` (l'intégration locale par défaut est `"coding"` quand non défini ; les valeurs explicites existantes sont conservées)
- `gateway.*` (mode, bind, auth, tailscale)
- `session.dmScope` (l'intégration locale par défaut est `per-channel-peer` quand non défini ; les valeurs explicites existantes sont conservées)
- `channels.telegram.botToken`, `channels.discord.token`, `channels.signal.*`, `channels.imessage.*`
- Listes blanches de canaux (Slack, Discord, Matrix, Microsoft Teams) quand vous acceptez lors des invites (les noms sont résolus en IDs si possible)
- `skills.install.nodeManager`
- `wizard.lastRunAt`
- `wizard.lastRunVersion`
- `wizard.lastRunCommit`
- `wizard.lastRunCommand`
- `wizard.lastRunMode`

`openclaw agents add` écrit `agents.list[]` et `bindings` optionnel.

Les identifiants WhatsApp se trouvent sous `~/.openclaw/credentials/whatsapp/<accountId>/`.
Les sessions sont stockées sous `~/.openclaw/agents/<agentId>/sessions/`.

<Note>
Certains canaux sont fournis en tant que plugins. Quand sélectionnés lors de l'intégration, l'assistant
vous invite à installer le plugin (npm ou chemin local) avant la configuration du canal.
</Note>

RPC de l'assistant de passerelle :

- `wizard.start`
- `wizard.next`
- `wizard.cancel`
- `wizard.status`

Les clients (application macOS et Control UI) peuvent afficher les étapes sans réimplémenter la logique d'intégration.

Comportement de configuration Signal :

- Télécharge l'actif de version approprié
- Le stocke sous `~/.openclaw/tools/signal-cli/<version>/`
- Écrit `channels.signal.cliPath` dans la configuration
- Les builds JVM nécessitent Java 21
- Les builds natifs sont utilisés quand disponibles
- Windows utilise WSL2 et suit le flux signal-cli Linux à l'intérieur de WSL

## Documentation connexe

- Hub d'intégration : [Assistant d'intégration (CLI)](/start/wizard)
- Automatisation et scripts : [Automatisation CLI](/start/wizard-cli-automation)
- Référence des commandes : [`openclaw onboard`](/cli/onboard)
