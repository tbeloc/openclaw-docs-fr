---
summary: "Tests en direct (touchant le réseau) : matrice de modèles, backends CLI, ACP, fournisseurs de médias, identifiants"
read_when:
  - Exécution de tests de fumée de matrice de modèles / backend CLI / ACP / fournisseur de médias en direct
  - Débogage de la résolution des identifiants de test en direct
  - Ajout d'un nouveau test en direct spécifique au fournisseur
title: "Tests : suites en direct"
sidebarTitle: "Tests en direct"
---

Pour un démarrage rapide, les exécuteurs QA, les suites unitaires/intégration et les flux Docker, voir
[Tests](/fr/help/testing). Cette page couvre les suites de tests **en direct** (touchant le réseau) : matrice de modèles, backends CLI, ACP et tests en direct des fournisseurs de médias, plus la gestion des identifiants.

## En direct : balayage des capacités des nœuds Android

- Test : `src/gateway/android-node.capabilities.live.test.ts`
- Script : `pnpm android:test:integration`
- Objectif : invoquer **chaque commande actuellement annoncée** par un nœud Android connecté et affirmer le comportement du contrat de commande.
- Portée :
  - Configuration précondionnée/manuelle (la suite n'installe/n'exécute/n'apparie pas l'application).
  - Validation de la passerelle `node.invoke` commande par commande pour le nœud Android sélectionné.
- Configuration préalable requise :
  - Application Android déjà connectée + appairée à la passerelle.
  - Application maintenue au premier plan.
  - Autorisations/consentement de capture accordés pour les capacités que vous vous attendez à réussir.
- Remplacements de cible optionnels :
  - `OPENCLAW_ANDROID_NODE_ID` ou `OPENCLAW_ANDROID_NODE_NAME`.
  - `OPENCLAW_ANDROID_GATEWAY_URL` / `OPENCLAW_ANDROID_GATEWAY_TOKEN` / `OPENCLAW_ANDROID_GATEWAY_PASSWORD`.
- Détails complets de la configuration Android : [Application Android](/fr/platforms/android)

## En direct : fumée de modèle (clés de profil)

Les tests en direct sont divisés en deux couches pour pouvoir isoler les défaillances :

- « Modèle direct » nous indique si le fournisseur/modèle peut répondre avec la clé donnée.
- « Fumée de passerelle » nous indique si le pipeline complet passerelle+agent fonctionne pour ce modèle (sessions, historique, outils, politique de bac à sable, etc.).

### Couche 1 : Complétion de modèle direct (sans passerelle)

- Test : `src/agents/models.profiles.live.test.ts`
- Objectif :
  - Énumérer les modèles découverts
  - Utiliser `getApiKeyForModel` pour sélectionner les modèles pour lesquels vous avez des identifiants
  - Exécuter une petite complétion par modèle (et des régressions ciblées si nécessaire)
- Comment activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
- Définissez `OPENCLAW_LIVE_MODELS=modern` (ou `all`, alias pour modern) pour exécuter réellement cette suite ; sinon elle est ignorée pour garder `pnpm test:live` concentré sur la fumée de passerelle
- Comment sélectionner les modèles :
  - `OPENCLAW_LIVE_MODELS=modern` pour exécuter la liste d'autorisation moderne (Opus/Sonnet 4.6+, GPT-5.2 + Codex, Gemini 3, GLM 4.7, MiniMax M2.7, Grok 4)
  - `OPENCLAW_LIVE_MODELS=all` est un alias pour la liste d'autorisation moderne
  - ou `OPENCLAW_LIVE_MODELS="openai/gpt-5.2,openai-codex/gpt-5.2,anthropic/claude-opus-4-6,..."` (liste d'autorisation séparée par des virgules)
  - Les balayages modernes/all utilisent par défaut un plafond curé à haut signal ; définissez `OPENCLAW_LIVE_MAX_MODELS=0` pour un balayage moderne exhaustif ou un nombre positif pour un plafond plus petit.
  - Les balayages exhaustifs utilisent `OPENCLAW_LIVE_TEST_TIMEOUT_MS` pour le délai d'expiration du test de modèle direct complet. Par défaut : 60 minutes.
  - Les sondes de modèle direct s'exécutent avec un parallélisme de 20 par défaut ; définissez `OPENCLAW_LIVE_MODEL_CONCURRENCY` pour remplacer.
- Comment sélectionner les fournisseurs :
  - `OPENCLAW_LIVE_PROVIDERS="google,google-antigravity,google-gemini-cli"` (liste d'autorisation séparée par des virgules)
- D'où viennent les clés :
  - Par défaut : magasin de profils et replis env
  - Définissez `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` pour appliquer **magasin de profils** uniquement
- Pourquoi cela existe :
  - Sépare « l'API du fournisseur est cassée / la clé est invalide » de « le pipeline de l'agent de passerelle est cassé »
  - Contient de petites régressions isolées (exemple : OpenAI Responses/Codex Responses relecture du raisonnement + flux d'appels d'outils)

### Couche 2 : Fumée de passerelle + agent dev (ce que « @openclaw » fait réellement)

- Test : `src/gateway/gateway-models.profiles.live.test.ts`
- Objectif :
  - Démarrer une passerelle en processus
  - Créer/corriger une session `agent:dev:*` (remplacement de modèle par exécution)
  - Itérer les modèles-avec-clés et affirmer :
    - réponse « significative » (pas d'outils)
    - une invocation d'outil réelle fonctionne (sonde de lecture)
    - sondes d'outils supplémentaires optionnelles (sonde exec+lecture)
    - les chemins de régression OpenAI (appel d'outil uniquement → suivi) continuent de fonctionner
- Détails de la sonde (pour que vous puissiez expliquer rapidement les défaillances) :
  - sonde `read` : le test écrit un fichier nonce dans l'espace de travail et demande à l'agent de le `read` et d'echo le nonce en retour.
  - sonde `exec+read` : le test demande à l'agent d'`exec`-écrire un nonce dans un fichier temporaire, puis de le `read` en retour.
  - sonde d'image : le test joint un PNG généré (chat + code aléatoire) et s'attend à ce que le modèle retourne `cat <CODE>`.
  - Référence d'implémentation : `src/gateway/gateway-models.profiles.live.test.ts` et `src/gateway/live-image-probe.ts`.
- Comment activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
- Comment sélectionner les modèles :
  - Par défaut : liste d'autorisation moderne (Opus/Sonnet 4.6+, GPT-5.2 + Codex, Gemini 3, GLM 4.7, MiniMax M2.7, Grok 4)
  - `OPENCLAW_LIVE_GATEWAY_MODELS=all` est un alias pour la liste d'autorisation moderne
  - Ou définissez `OPENCLAW_LIVE_GATEWAY_MODELS="provider/model"` (ou liste séparée par des virgules) pour affiner
  - Les balayages modernes/all de passerelle utilisent par défaut un plafond curé à haut signal ; définissez `OPENCLAW_LIVE_GATEWAY_MAX_MODELS=0` pour un balayage moderne exhaustif ou un nombre positif pour un plafond plus petit.
- Comment sélectionner les fournisseurs (éviter « OpenRouter tout ») :
  - `OPENCLAW_LIVE_GATEWAY_PROVIDERS="google,google-antigravity,google-gemini-cli,openai,anthropic,zai,minimax"` (liste d'autorisation séparée par des virgules)
- Les sondes d'outils + d'images sont toujours activées dans ce test en direct :
  - sonde `read` + sonde `exec+read` (stress des outils)
  - la sonde d'image s'exécute quand le modèle annonce le support d'entrée d'image
  - Flux (haut niveau) :
    - Le test génère un petit PNG avec « CAT » + code aléatoire (`src/gateway/live-image-probe.ts`)
    - L'envoie via `agent` `attachments: [{ mimeType: "image/png", content: "<base64>" }]`
    - La passerelle analyse les pièces jointes en `images[]` (`src/gateway/server-methods/agent.ts` + `src/gateway/chat-attachments.ts`)
    - L'agent intégré transmet un message utilisateur multimodal au modèle
    - Assertion : la réponse contient `cat` + le code (tolérance OCR : les petites erreurs sont autorisées)

Conseil : pour voir ce que vous pouvez tester sur votre machine (et les identifiants exacts `provider/model`), exécutez :

```bash
openclaw models list
openclaw models list --json
```

## En direct : fumée de backend CLI (Claude, Codex, Gemini ou autres CLI locaux)

- Test : `src/gateway/gateway-cli-backend.live.test.ts`
- Objectif : valider le pipeline Passerelle + agent en utilisant un backend CLI local, sans toucher à votre configuration par défaut.
- Les valeurs par défaut de fumée spécifiques au backend vivent avec la définition `cli-backend.ts` de l'extension propriétaire.
- Activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
  - `OPENCLAW_LIVE_CLI_BACKEND=1`
- Valeurs par défaut :
  - Fournisseur/modèle par défaut : `claude-cli/claude-sonnet-4-6`
  - Le comportement de la commande/args/image provient des métadonnées du plugin backend CLI propriétaire.
- Remplacements (optionnels) :
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="codex-cli/gpt-5.2"`
  - `OPENCLAW_LIVE_CLI_BACKEND_COMMAND="/full/path/to/codex"`
  - `OPENCLAW_LIVE_CLI_BACKEND_ARGS='["exec","--json","--color","never","--sandbox","read-only","--skip-git-repo-check"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_PROBE=1` pour envoyer une véritable pièce jointe d'image (les chemins sont injectés dans l'invite).
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_ARG="--image"` pour passer les chemins de fichiers image en tant qu'arguments CLI au lieu d'injection d'invite.
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_MODE="repeat"` (ou `"list"`) pour contrôler comment les arguments d'image sont passés quand `IMAGE_ARG` est défini.
  - `OPENCLAW_LIVE_CLI_BACKEND_RESUME_PROBE=1` pour envoyer un deuxième tour et valider le flux de reprise.
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL_SWITCH_PROBE=0` pour désactiver la sonde de continuité de session identique Claude Sonnet -> Opus par défaut (définissez à `1` pour la forcer quand le modèle sélectionné supporte une cible de commutation).

Exemple :

```bash
OPENCLAW_LIVE_CLI_BACKEND=1 \
  OPENCLAW_LIVE_CLI_BACKEND_MODEL="codex-cli/gpt-5.2" \
  pnpm test:live src/gateway/gateway-cli-backend.live.test.ts
```

Recette Docker :

```bash
pnpm test:docker:live-cli-backend
```

Recettes Docker pour un seul fournisseur :

```bash
pnpm test:docker:live-cli-backend:claude
pnpm test:docker:live-cli-backend:claude-subscription
pnpm test:docker:live-cli-backend:codex
pnpm test:docker:live-cli-backend:gemini
```

Notes :

- Le coureur Docker se trouve à `scripts/test-live-cli-backend-docker.sh`.
- Il exécute la fumée CLI-backend en direct à l'intérieur de l'image Docker du repo en tant qu'utilisateur non-root `node`.
- Il résout les métadonnées de fumée CLI à partir de l'extension propriétaire, puis installe le package CLI Linux correspondant (`@anthropic-ai/claude-code`, `@openai/codex`, ou `@google/gemini-cli`) dans un préfixe inscriptible mis en cache à `OPENCLAW_DOCKER_CLI_TOOLS_DIR` (par défaut : `~/.cache/openclaw/docker-cli-tools`).
- `pnpm test:docker:live-cli-backend:claude-subscription` nécessite une authentification OAuth portable Claude Code via soit `~/.claude/.credentials.json` avec `claudeAiOauth.subscriptionType` soit `CLAUDE_CODE_OAUTH_TOKEN` de `claude setup-token`. Il prouve d'abord directement `claude -p` dans Docker, puis exécute deux tours de backend CLI de passerelle sans préserver les variables env de clé API Anthropic. Cette voie d'abonnement désactive les sondes Claude MCP/outil et image par défaut car Claude achemine actuellement l'utilisation par des applications tierces via une facturation d'utilisation supplémentaire au lieu des limites du plan d'abonnement normal.
- La fumée CLI-backend en direct exerce maintenant le même flux de bout en bout pour Claude, Codex et Gemini : tour de texte, tour de classification d'image, puis appel d'outil MCP `cron` vérifié via la CLI de passerelle.
- La fumée par défaut de Claude corrige également la session de Sonnet à Opus et vérifie que la session reprise se souvient toujours d'une note antérieure.

## Live : ACP bind smoke (`/acp spawn ... --bind here`)

- Test : `src/gateway/gateway-acp-bind.live.test.ts`
- Objectif : valider le flux réel de liaison de conversation ACP avec un agent ACP en direct :
  - envoyer `/acp spawn <agent> --bind here`
  - lier une conversation de canal de message synthétique en place
  - envoyer un suivi normal sur cette même conversation
  - vérifier que le suivi arrive dans la transcription de la session ACP liée
- Activation :
  - `pnpm test:live src/gateway/gateway-acp-bind.live.test.ts`
  - `OPENCLAW_LIVE_ACP_BIND=1`
- Valeurs par défaut :
  - Agents ACP dans Docker : `claude,codex,gemini`
  - Agent ACP pour `pnpm test:live ...` direct : `claude`
  - Canal synthétique : contexte de conversation de style Slack DM
  - Backend ACP : `acpx`
- Remplacements :
  - `OPENCLAW_LIVE_ACP_BIND_AGENT=claude`
  - `OPENCLAW_LIVE_ACP_BIND_AGENT=codex`
  - `OPENCLAW_LIVE_ACP_BIND_AGENT=gemini`
  - `OPENCLAW_LIVE_ACP_BIND_AGENTS=claude,codex,gemini`
  - `OPENCLAW_LIVE_ACP_BIND_AGENT_COMMAND='npx -y @agentclientprotocol/claude-agent-acp@<version>'`
  - `OPENCLAW_LIVE_ACP_BIND_CODEX_MODEL=gpt-5.2`
  - `OPENCLAW_LIVE_ACP_BIND_PARENT_MODEL=openai/gpt-5.2`
- Notes :
  - Cette voie utilise la surface `chat.send` de la passerelle avec des champs de route d'origine synthétique réservés aux administrateurs afin que les tests puissent joindre le contexte du canal de message sans prétendre livrer en externe.
  - Quand `OPENCLAW_LIVE_ACP_BIND_AGENT_COMMAND` n'est pas défini, le test utilise le registre d'agent intégré du plugin `acpx` embarqué pour l'agent de harnais ACP sélectionné.

Exemple :

```bash
OPENCLAW_LIVE_ACP_BIND=1 \
  OPENCLAW_LIVE_ACP_BIND_AGENT=claude \
  pnpm test:live src/gateway/gateway-acp-bind.live.test.ts
```

Recette Docker :

```bash
pnpm test:docker:live-acp-bind
```

Recettes Docker pour un seul agent :

```bash
pnpm test:docker:live-acp-bind:claude
pnpm test:docker:live-acp-bind:codex
pnpm test:docker:live-acp-bind:gemini
```

Notes Docker :

- Le runner Docker se trouve à `scripts/test-live-acp-bind-docker.sh`.
- Par défaut, il exécute le test de fumée de liaison ACP par rapport à tous les agents CLI en direct pris en charge en séquence : `claude`, `codex`, puis `gemini`.
- Utilisez `OPENCLAW_LIVE_ACP_BIND_AGENTS=claude`, `OPENCLAW_LIVE_ACP_BIND_AGENTS=codex`, ou `OPENCLAW_LIVE_ACP_BIND_AGENTS=gemini` pour réduire la matrice.
- Il source `~/.profile`, prépare le matériel d'authentification CLI correspondant dans le conteneur, installe `acpx` dans un préfixe npm inscriptible, puis installe le CLI en direct demandé (`@anthropic-ai/claude-code`, `@openai/codex`, ou `@google/gemini-cli`) s'il est manquant.
- À l'intérieur de Docker, le runner définit `OPENCLAW_LIVE_ACP_BIND_ACPX_COMMAND=$HOME/.npm-global/bin/acpx` afin que acpx conserve les variables d'environnement du fournisseur du profil sourcé disponibles pour le CLI de harnais enfant.

## Live : test de fumée du harnais du serveur d'application Codex

- Objectif : valider le harnais Codex détenu par le plugin via la méthode `agent` normale de la passerelle :
  - charger le plugin `codex` fourni
  - sélectionner `OPENCLAW_AGENT_RUNTIME=codex`
  - envoyer un premier tour d'agent de passerelle à `openai/gpt-5.2` avec le harnais Codex forcé
  - envoyer un deuxième tour à la même session OpenClaw et vérifier que le thread du serveur d'application peut reprendre
  - exécuter `/codex status` et `/codex models` via le même chemin de commande de passerelle
  - exécuter optionnellement deux sondes shell escaladées examinées par Guardian : une commande bénigne qui devrait être approuvée et un faux téléchargement de secret qui devrait être refusé afin que l'agent demande à nouveau
- Test : `src/gateway/gateway-codex-harness.live.test.ts`
- Activation : `OPENCLAW_LIVE_CODEX_HARNESS=1`
- Modèle par défaut : `openai/gpt-5.2`
- Sonde d'image optionnelle : `OPENCLAW_LIVE_CODEX_HARNESS_IMAGE_PROBE=1`
- Sonde MCP/outil optionnelle : `OPENCLAW_LIVE_CODEX_HARNESS_MCP_PROBE=1`
- Sonde Guardian optionnelle : `OPENCLAW_LIVE_CODEX_HARNESS_GUARDIAN_PROBE=1`
- Le test de fumée définit `OPENCLAW_AGENT_HARNESS_FALLBACK=none` afin qu'un harnais Codex cassé ne puisse pas passer en se repliant silencieusement sur PI.
- Authentification : authentification du serveur d'application Codex à partir de la connexion d'abonnement Codex locale. Les tests de fumée Docker peuvent également fournir `OPENAI_API_KEY` pour les sondes non-Codex le cas échéant, plus `~/.codex/auth.json` et `~/.codex/config.toml` copiés optionnellement.

Recette locale :

```bash
source ~/.profile
OPENCLAW_LIVE_CODEX_HARNESS=1 \
  OPENCLAW_LIVE_CODEX_HARNESS_IMAGE_PROBE=1 \
  OPENCLAW_LIVE_CODEX_HARNESS_MCP_PROBE=1 \
  OPENCLAW_LIVE_CODEX_HARNESS_GUARDIAN_PROBE=1 \
  OPENCLAW_LIVE_CODEX_HARNESS_MODEL=openai/gpt-5.2 \
  pnpm test:live -- src/gateway/gateway-codex-harness.live.test.ts
```

Recette Docker :

```bash
source ~/.profile
pnpm test:docker:live-codex-harness
```

Notes Docker :

- Le runner Docker se trouve à `scripts/test-live-codex-harness-docker.sh`.
- Il source le `~/.profile` monté, transmet `OPENAI_API_KEY`, copie les fichiers d'authentification CLI Codex le cas échéant, installe `@openai/codex` dans un préfixe npm monté inscriptible, prépare l'arborescence source, puis exécute uniquement le test en direct du harnais Codex.
- Docker active les sondes d'image, MCP/outil et Guardian par défaut. Définissez `OPENCLAW_LIVE_CODEX_HARNESS_IMAGE_PROBE=0` ou `OPENCLAW_LIVE_CODEX_HARNESS_MCP_PROBE=0` ou `OPENCLAW_LIVE_CODEX_HARNESS_GUARDIAN_PROBE=0` quand vous avez besoin d'une exécution de débogage plus étroite.
- Docker exporte également `OPENCLAW_AGENT_HARNESS_FALLBACK=none`, correspondant à la configuration du test en direct afin que les alias hérités ou le repli PI ne puissent pas masquer une régression du harnais Codex.

### Recettes en direct recommandées

Les listes d'autorisation étroites et explicites sont les plus rapides et les moins instables :

- Modèle unique, direct (pas de passerelle) :
  - `OPENCLAW_LIVE_MODELS="openai/gpt-5.2" pnpm test:live src/agents/models.profiles.live.test.ts`

- Modèle unique, test de fumée de passerelle :
  - `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

- Appel d'outil sur plusieurs fournisseurs :
  - `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,openai-codex/gpt-5.2,anthropic/claude-opus-4-6,google/gemini-3-flash-preview,zai/glm-4.7,minimax/MiniMax-M2.7" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

- Focus Google (clé API Gemini + Antigravity) :
  - Gemini (clé API) : `OPENCLAW_LIVE_GATEWAY_MODELS="google/gemini-3-flash-preview" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`
  - Antigravity (OAuth) : `OPENCLAW_LIVE_GATEWAY_MODELS="google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-pro-high" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

Notes :

- `google/...` utilise l'API Gemini (clé API).
- `google-antigravity/...` utilise le pont OAuth Antigravity (point de terminaison d'agent de style Cloud Code Assist).
- `google-gemini-cli/...` utilise le CLI Gemini local sur votre machine (authentification séparée + particularités des outils).
- API Gemini vs CLI Gemini :
  - API : OpenClaw appelle l'API Gemini hébergée de Google via HTTP (authentification par clé API / profil) ; c'est ce que la plupart des utilisateurs entendent par « Gemini ».
  - CLI : OpenClaw exécute un binaire `gemini` local ; il a sa propre authentification et peut se comporter différemment (streaming/support des outils/décalage de version).

## Live : matrice de modèles (ce que nous couvrons)

Il n'y a pas de liste « CI model » fixe (live est opt-in), mais ce sont les modèles **recommandés** à couvrir régulièrement sur une machine de développement avec des clés.

### Ensemble de test de fumée moderne (appel d'outil + image)

C'est l'exécution des « modèles courants » que nous nous attendons à maintenir en fonctionnement :

- OpenAI (non-Codex) : `openai/gpt-5.2`
- OpenAI Codex OAuth : `openai-codex/gpt-5.2`
- Anthropic : `anthropic/claude-opus-4-6` (ou `anthropic/claude-sonnet-4-6`)
- Google (API Gemini) : `google/gemini-3.1-pro-preview` et `google/gemini-3-flash-preview` (éviter les anciens modèles Gemini 2.x)
- Google (Antigravity) : `google-antigravity/claude-opus-4-6-thinking` et `google-antigravity/gemini-3-flash`
- Z.AI (GLM) : `zai/glm-4.7`
- MiniMax : `minimax/MiniMax-M2.7`

Exécuter le test de fumée de passerelle avec outils + image :
`OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,openai-codex/gpt-5.2,anthropic/claude-opus-4-6,google/gemini-3.1-pro-preview,google/gemini-3-flash-preview,google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-flash,zai/glm-4.7,minimax/MiniMax-M2.7" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

### Ligne de base : appel d'outil (Lecture + Exécution optionnelle)

Choisissez au moins un par famille de fournisseur :

- OpenAI : `openai/gpt-5.2`
- Anthropic : `anthropic/claude-opus-4-6` (ou `anthropic/claude-sonnet-4-6`)
- Google : `google/gemini-3-flash-preview` (ou `google/gemini-3.1-pro-preview`)
- Z.AI (GLM) : `zai/glm-4.7`
- MiniMax : `minimax/MiniMax-M2.7`

Couverture supplémentaire optionnelle (agréable à avoir) :

- xAI : `xai/grok-4` (ou la dernière disponible)
- Mistral : `mistral/`… (choisissez un modèle capable « d'outils » que vous avez activé)
- Cerebras : `cerebras/`… (si vous avez accès)
- LM Studio : `lmstudio/`… (local ; l'appel d'outil dépend du mode API)

### Vision : envoi d'image (pièce jointe → message multimodal)

Incluez au moins un modèle capable d'images dans `OPENCLAW_LIVE_GATEWAY_MODELS` (variantes Claude/Gemini/OpenAI compatibles avec la vision, etc.) pour exercer la sonde d'image.

### Agrégateurs / passerelles alternatives

Si vous avez des clés activées, nous supportons également les tests via :

- OpenRouter : `openrouter/...` (des centaines de modèles ; utilisez `openclaw models scan` pour trouver des candidats capables d'outils+images)
- OpenCode : `opencode/...` pour Zen et `opencode-go/...` pour Go (authentification via `OPENCODE_API_KEY` / `OPENCODE_ZEN_API_KEY`)

Plus de fournisseurs que vous pouvez inclure dans la matrice en direct (si vous avez des identifiants/config) :

- Intégré : `openai`, `openai-codex`, `anthropic`, `google`, `google-vertex`, `google-antigravity`, `google-gemini-cli`, `zai`, `openrouter`, `opencode`, `opencode-go`, `xai`, `groq`, `cerebras`, `mistral`, `github-copilot`
- Via `models.providers` (points de terminaison personnalisés) : `minimax` (cloud/API), plus tout proxy compatible OpenAI/Anthropic (LM Studio, vLLM, LiteLLM, etc.)

Conseil : ne tentez pas de coder en dur « tous les modèles » dans la documentation. La liste faisant autorité est ce que `discoverModels(...)` retourne sur votre machine + les clés disponibles.

## Identifiants (ne jamais valider)

Les tests en direct découvrent les identifiants de la même manière que le CLI. Implications pratiques :

- Si le CLI fonctionne, les tests en direct devraient trouver les mêmes clés.
- Si un test en direct dit « pas d'identifiants », déboguez de la même manière que vous débogueriez `openclaw models list` / sélection de modèle.

- Profils d'authentification par agent : `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (c'est ce que « clés de profil » signifie dans les tests en direct)
- Config : `~/.openclaw/openclaw.json` (ou `OPENCLAW_CONFIG_PATH`)
- Répertoire d'état hérité : `~/.openclaw/credentials/` (copié dans le répertoire d'accueil en direct préparé quand présent, mais pas le magasin de clés de profil principal)
- Les exécutions locales en direct copient la config active, les fichiers `auth-profiles.json` par agent, le `credentials/` hérité, et les répertoires d'authentification CLI externes pris en charge dans un répertoire d'accueil de test temporaire par défaut ; les répertoires d'accueil en direct préparés ignorent `workspace/` et `sandboxes/`, et les remplacements de chemin `agents.*.workspace` / `agentDir` sont supprimés afin que les sondes restent en dehors de votre vrai espace de travail hôte.

Si vous voulez compter sur les clés env (par exemple exportées dans votre `~/.profile`), exécutez les tests locaux après `source ~/.profile`, ou utilisez les runners Docker ci-dessous (ils peuvent monter `~/.profile` dans le conteneur).

## Deepgram en direct (transcription audio)

- Test : `extensions/deepgram/audio.live.test.ts`
- Activation : `DEEPGRAM_API_KEY=... DEEPGRAM_LIVE_TEST=1 pnpm test:live extensions/deepgram/audio.live.test.ts`

## Plan de codage BytePlus en direct

- Test : `extensions/byteplus/live.test.ts`
- Activation : `BYTEPLUS_API_KEY=... BYTEPLUS_LIVE_TEST=1 pnpm test:live extensions/byteplus/live.test.ts`
- Remplacement de modèle optionnel : `BYTEPLUS_CODING_MODEL=ark-code-latest`

## Média de flux de travail ComfyUI en direct

- Test : `extensions/comfy/comfy.live.test.ts`
- Activation : `OPENCLAW_LIVE_TEST=1 COMFY_LIVE_TEST=1 pnpm test:live -- extensions/comfy/comfy.live.test.ts`
- Portée :
  - Exerce les chemins d'image, vidéo et `music_generate` comfy fournis
  - Ignore chaque capacité sauf si `models.providers.comfy.<capability>` est configuré
  - Utile après modification de la soumission de flux de travail comfy, de l'interrogation, des téléchargements ou de l'enregistrement du plugin

## Génération d'images en direct

- Test : `test/image-generation.runtime.live.test.ts`
- Commande : `pnpm test:live test/image-generation.runtime.live.test.ts`
- Harnais : `pnpm test:live:media image`
- Portée :
  - Énumère tous les plugins de fournisseur de génération d'images enregistrés
  - Charge les variables d'environnement manquantes du fournisseur à partir de votre shell de connexion (`~/.profile`) avant de sonder
  - Utilise les clés API en direct/env avant les profils d'authentification stockés par défaut, de sorte que les clés de test obsolètes dans `auth-profiles.json` ne masquent pas les véritables identifiants shell
  - Ignore les fournisseurs sans authentification/profil/modèle utilisable
  - Exécute les variantes de génération d'images standard via la capacité d'exécution partagée :
    - `google:flash-generate`
    - `google:pro-generate`
    - `google:pro-edit`
    - `openai:default-generate`
- Fournisseurs groupés actuellement couverts :
  - `fal`
  - `google`
  - `minimax`
  - `openai`
  - `openrouter`
  - `vydra`
  - `xai`
- Réduction optionnelle :
  - `OPENCLAW_LIVE_IMAGE_GENERATION_PROVIDERS="openai,google,openrouter,xai"`
  - `OPENCLAW_LIVE_IMAGE_GENERATION_MODELS="openai/gpt-image-2,google/gemini-3.1-flash-image-preview,openrouter/google/gemini-3.1-flash-image-preview,xai/grok-imagine-image"`
  - `OPENCLAW_LIVE_IMAGE_GENERATION_CASES="google:flash-generate,google:pro-edit,openrouter:generate,xai:default-generate,xai:default-edit"`
- Comportement d'authentification optionnel :
  - `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` pour forcer l'authentification du magasin de profils et ignorer les remplacements env uniquement

## Génération de musique en direct

- Test : `extensions/music-generation-providers.live.test.ts`
- Activer : `OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/music-generation-providers.live.test.ts`
- Harnais : `pnpm test:live:media music`
- Portée :
  - Exerce le chemin du fournisseur de génération de musique groupé partagé
  - Couvre actuellement Google et MiniMax
  - Charge les variables d'environnement du fournisseur à partir de votre shell de connexion (`~/.profile`) avant de sonder
  - Utilise les clés API en direct/env avant les profils d'authentification stockés par défaut, de sorte que les clés de test obsolètes dans `auth-profiles.json` ne masquent pas les véritables identifiants shell
  - Ignore les fournisseurs sans authentification/profil/modèle utilisable
  - Exécute les deux modes d'exécution déclarés lorsqu'ils sont disponibles :
    - `generate` avec entrée d'invite uniquement
    - `edit` lorsque le fournisseur déclare `capabilities.edit.enabled`
  - Couverture de voie partagée actuelle :
    - `google` : `generate`, `edit`
    - `minimax` : `generate`
    - `comfy` : fichier Comfy en direct séparé, pas ce balayage partagé
- Réduction optionnelle :
  - `OPENCLAW_LIVE_MUSIC_GENERATION_PROVIDERS="google,minimax"`
  - `OPENCLAW_LIVE_MUSIC_GENERATION_MODELS="google/lyria-3-clip-preview,minimax/music-2.5+"`
- Comportement d'authentification optionnel :
  - `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` pour forcer l'authentification du magasin de profils et ignorer les remplacements env uniquement

## Génération de vidéo en direct

- Test : `extensions/video-generation-providers.live.test.ts`
- Activer : `OPENCLAW_LIVE_TEST=1 pnpm test:live -- extensions/video-generation-providers.live.test.ts`
- Harnais : `pnpm test:live:media video`
- Portée :
  - Exerce le chemin du fournisseur de génération de vidéo groupé partagé
  - Par défaut, le chemin de fumée sûr pour la version : fournisseurs non-FAL, une demande texte-vers-vidéo par fournisseur, une invite de homard d'une seconde, et un plafond d'opération par fournisseur de `OPENCLAW_LIVE_VIDEO_GENERATION_TIMEOUT_MS` (`180000` par défaut)
  - Ignore FAL par défaut car la latence de la file d'attente côté fournisseur peut dominer le temps de version ; passez `--video-providers fal` ou `OPENCLAW_LIVE_VIDEO_GENERATION_PROVIDERS="fal"` pour l'exécuter explicitement
  - Charge les variables d'environnement du fournisseur à partir de votre shell de connexion (`~/.profile`) avant de sonder
  - Utilise les clés API en direct/env avant les profils d'authentification stockés par défaut, de sorte que les clés de test obsolètes dans `auth-profiles.json` ne masquent pas les véritables identifiants shell
  - Ignore les fournisseurs sans authentification/profil/modèle utilisable
  - Exécute uniquement `generate` par défaut
  - Définissez `OPENCLAW_LIVE_VIDEO_GENERATION_FULL_MODES=1` pour également exécuter les modes de transformation déclarés lorsqu'ils sont disponibles :
    - `imageToVideo` lorsque le fournisseur déclare `capabilities.imageToVideo.enabled` et que le fournisseur/modèle sélectionné accepte l'entrée d'image locale soutenue par un tampon dans le balayage partagé
    - `videoToVideo` lorsque le fournisseur déclare `capabilities.videoToVideo.enabled` et que le fournisseur/modèle sélectionné accepte l'entrée vidéo locale soutenue par un tampon dans le balayage partagé
  - Fournisseurs `imageToVideo` déclarés mais ignorés actuellement dans le balayage partagé :
    - `vydra` car `veo3` groupé est texte uniquement et `kling` groupé nécessite une URL d'image distante
  - Couverture Vydra spécifique au fournisseur :
    - `OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_VYDRA_VIDEO=1 pnpm test:live -- extensions/vydra/vydra.live.test.ts`
    - ce fichier exécute `veo3` texte-vers-vidéo plus une voie `kling` qui utilise une fixture d'URL d'image distante par défaut
  - Couverture en direct `videoToVideo` actuelle :
    - `runway` uniquement lorsque le modèle sélectionné est `runway/gen4_aleph`
  - Fournisseurs `videoToVideo` déclarés mais ignorés actuellement dans le balayage partagé :
    - `alibaba`, `qwen`, `xai` car ces chemins nécessitent actuellement des URL de référence `http(s)` / MP4 distantes
    - `google` car la voie Gemini/Veo partagée actuelle utilise l'entrée locale soutenue par un tampon et ce chemin n'est pas accepté dans le balayage partagé
    - `openai` car la voie partagée actuelle manque de garanties d'accès à la retouche/remix vidéo spécifiques à l'organisation
- Réduction optionnelle :
  - `OPENCLAW_LIVE_VIDEO_GENERATION_PROVIDERS="google,openai,runway"`
  - `OPENCLAW_LIVE_VIDEO_GENERATION_MODELS="google/veo-3.1-fast-generate-preview,openai/sora-2,runway/gen4_aleph"`
  - `OPENCLAW_LIVE_VIDEO_GENERATION_SKIP_PROVIDERS=""` pour inclure tous les fournisseurs dans le balayage par défaut, y compris FAL
  - `OPENCLAW_LIVE_VIDEO_GENERATION_TIMEOUT_MS=60000` pour réduire le plafond d'opération de chaque fournisseur pour un balayage de fumée agressif
- Comportement d'authentification optionnel :
  - `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` pour forcer l'authentification du magasin de profils et ignorer les remplacements env uniquement

## Harnais média en direct

- Commande : `pnpm test:live:media`
- Objectif :
  - Exécute les suites en direct d'image, de musique et de vidéo partagées via un point d'entrée natif du référentiel
  - Charge automatiquement les variables d'environnement manquantes du fournisseur à partir de `~/.profile`
  - Réduit automatiquement chaque suite aux fournisseurs qui ont actuellement une authentification utilisable par défaut
  - Réutilise `scripts/test-live.mjs`, de sorte que le comportement du battement cardiaque et du mode silencieux reste cohérent
- Exemples :
  - `pnpm test:live:media`
  - `pnpm test:live:media image video --providers openai,google,minimax`
  - `pnpm test:live:media video --video-providers openai,runway --all-providers`
  - `pnpm test:live:media music --quiet`

## Connexes

- [Testing](/fr/help/testing) — suites unitaires, d'intégration, d'assurance qualité et Docker
