---
summary: "Kit de test : suites unit/e2e/live, exécuteurs Docker, et ce que chaque test couvre"
read_when:
  - Running tests locally or in CI
  - Adding regressions for model/provider bugs
  - Debugging gateway + agent behavior
title: "Testing"
---

# Testing

OpenClaw dispose de trois suites Vitest (unit/integration, e2e, live) et d'un petit ensemble d'exécuteurs Docker.

Ce document est un guide « comment nous testons » :

- Ce que chaque suite couvre (et ce qu'elle ne couvre délibérément _pas_)
- Quelles commandes exécuter pour les workflows courants (local, pré-push, débogage)
- Comment les tests live découvrent les identifiants et sélectionnent les modèles/fournisseurs
- Comment ajouter des régressions pour les problèmes réels de modèle/fournisseur

## Démarrage rapide

La plupart du temps :

- Portail complet (attendu avant le push) : `pnpm build && pnpm check && pnpm test`

Quand vous touchez aux tests ou voulez plus de confiance :

- Portail de couverture : `pnpm test:coverage`
- Suite E2E : `pnpm test:e2e`

Lors du débogage de fournisseurs/modèles réels (nécessite des identifiants réels) :

- Suite live (modèles + sondes d'outil/image de passerelle) : `pnpm test:live`

Conseil : quand vous n'avez besoin que d'un seul cas défaillant, préférez réduire les tests live via les variables d'environnement de liste blanche décrites ci-dessous.

## Suites de test (ce qui s'exécute où)

Pensez aux suites comme « réalisme croissant » (et instabilité/coût croissants) :

### Unit / integration (par défaut)

- Commande : `pnpm test`
- Config : `scripts/test-parallel.mjs` (exécute `vitest.unit.config.ts`, `vitest.extensions.config.ts`, `vitest.gateway.config.ts`)
- Fichiers : `src/**/*.test.ts`, `extensions/**/*.test.ts`
- Portée :
  - Tests unitaires purs
  - Tests d'intégration en processus (authentification de passerelle, routage, outillage, analyse, configuration)
  - Régressions déterministes pour les bugs connus
- Attentes :
  - S'exécute en CI
  - Aucune clé réelle requise
  - Doit être rapide et stable
- Note sur le pool :
  - OpenClaw utilise Vitest `vmForks` sur Node 22, 23 et 24 pour des shards unitaires plus rapides.
  - Sur Node 25+, OpenClaw revient automatiquement à `forks` régulier jusqu'à ce que le dépôt soit revalidé là-bas.
  - Remplacez manuellement avec `OPENCLAW_TEST_VM_FORKS=0` (forcer `forks`) ou `OPENCLAW_TEST_VM_FORKS=1` (forcer `vmForks`).

### E2E (smoke de passerelle)

- Commande : `pnpm test:e2e`
- Config : `vitest.e2e.config.ts`
- Fichiers : `src/**/*.e2e.test.ts`
- Valeurs par défaut du runtime :
  - Utilise Vitest `vmForks` pour un démarrage de fichier plus rapide.
  - Utilise des workers adaptatifs (CI : 2-4, local : 4-8).
  - S'exécute en mode silencieux par défaut pour réduire la surcharge d'E/S de la console.
- Remplacements utiles :
  - `OPENCLAW_E2E_WORKERS=<n>` pour forcer le nombre de workers (limité à 16).
  - `OPENCLAW_E2E_VERBOSE=1` pour réactiver la sortie console détaillée.
- Portée :
  - Comportement end-to-end multi-instance de la passerelle
  - Surfaces WebSocket/HTTP, appairage de nœuds et réseautage plus lourd
- Attentes :
  - S'exécute en CI (quand activé dans le pipeline)
  - Aucune clé réelle requise
  - Plus de pièces mobiles que les tests unitaires (peut être plus lent)

### Live (fournisseurs réels + modèles réels)

- Commande : `pnpm test:live`
- Config : `vitest.live.config.ts`
- Fichiers : `src/**/*.live.test.ts`
- Par défaut : **activé** par `pnpm test:live` (définit `OPENCLAW_LIVE_TEST=1`)
- Portée :
  - « Ce fournisseur/modèle fonctionne-t-il réellement _aujourd'hui_ avec des identifiants réels ? »
  - Détecter les changements de format de fournisseur, les bizarreries d'appel d'outil, les problèmes d'authentification et le comportement des limites de débit
- Attentes :
  - Non stable en CI par conception (réseaux réels, politiques de fournisseur réelles, quotas, pannes)
  - Coûte de l'argent / utilise les limites de débit
  - Préférez exécuter des sous-ensembles réduits au lieu de « tout »
  - Les exécutions live sourceront `~/.profile` pour récupérer les clés API manquantes
- Rotation de clé API (spécifique au fournisseur) : définissez `*_API_KEYS` avec format virgule/point-virgule ou `*_API_KEY_1`, `*_API_KEY_2` (par exemple `OPENAI_API_KEYS`, `ANTHROPIC_API_KEYS`, `GEMINI_API_KEYS`) ou remplacez par live via `OPENCLAW_LIVE_*_KEY` ; les tests réessaient sur les réponses de limite de débit.

## Quelle suite dois-je exécuter ?

Utilisez ce tableau de décision :

- Édition de logique/tests : exécutez `pnpm test` (et `pnpm test:coverage` si vous avez beaucoup changé)
- Toucher au réseautage de passerelle / protocole WS / appairage : ajoutez `pnpm test:e2e`
- Débogage « mon bot est en panne » / défaillances spécifiques au fournisseur / appel d'outil : exécutez un `pnpm test:live` réduit

## Live : balayage de capacité du nœud Android

- Test : `src/gateway/android-node.capabilities.live.test.ts`
- Script : `pnpm android:test:integration`
- Objectif : invoquer **chaque commande actuellement annoncée** par un nœud Android connecté et affirmer le comportement du contrat de commande.
- Portée :
  - Configuration précondition/manuelle (la suite n'installe/n'exécute/n'appaire pas l'application).
  - Validation `node.invoke` de passerelle commande par commande pour le nœud Android sélectionné.
- Configuration préalable requise :
  - Application Android déjà connectée + appairée à la passerelle.
  - Application maintenue au premier plan.
  - Autorisations/consentement de capture accordés pour les capacités que vous vous attendez à réussir.
- Remplacements de cible optionnels :
  - `OPENCLAW_ANDROID_NODE_ID` ou `OPENCLAW_ANDROID_NODE_NAME`.
  - `OPENCLAW_ANDROID_GATEWAY_URL` / `OPENCLAW_ANDROID_GATEWAY_TOKEN` / `OPENCLAW_ANDROID_GATEWAY_PASSWORD`.
- Détails complets de configuration Android : [Android App](/fr/platforms/android)

## Live : smoke de modèle (clés de profil)

Les tests live sont divisés en deux couches pour que nous puissions isoler les défaillances :

- « Modèle direct » nous dit que le fournisseur/modèle peut répondre du tout avec la clé donnée.
- « Smoke de passerelle » nous dit que le pipeline complet passerelle+agent fonctionne pour ce modèle (sessions, historique, outils, politique de sandbox, etc.).

### Couche 1 : Complétion de modèle direct (pas de passerelle)

- Test : `src/agents/models.profiles.live.test.ts`
- Objectif :
  - Énumérer les modèles découverts
  - Utiliser `getApiKeyForModel` pour sélectionner les modèles pour lesquels vous avez des identifiants
  - Exécuter une petite complétion par modèle (et régressions ciblées si nécessaire)
- Comment activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
- Définissez `OPENCLAW_LIVE_MODELS=modern` (ou `all`, alias pour modern) pour exécuter réellement cette suite ; sinon elle saute pour garder `pnpm test:live` concentré sur le smoke de passerelle
- Comment sélectionner les modèles :
  - `OPENCLAW_LIVE_MODELS=modern` pour exécuter la liste blanche moderne (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.5, Grok 4)
  - `OPENCLAW_LIVE_MODELS=all` est un alias pour la liste blanche moderne
  - ou `OPENCLAW_LIVE_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,..."` (liste blanche virgule)
- Comment sélectionner les fournisseurs :
  - `OPENCLAW_LIVE_PROVIDERS="google,google-antigravity,google-gemini-cli"` (liste blanche virgule)
- D'où viennent les clés :
  - Par défaut : magasin de profil et remplacements env
  - Définissez `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` pour appliquer **magasin de profil** uniquement
- Pourquoi cela existe :
  - Sépare « l'API du fournisseur est cassée / la clé est invalide » de « le pipeline d'agent de passerelle est cassé »
  - Contient de petites régressions isolées (exemple : replay de raisonnement OpenAI Responses/Codex Responses + flux d'appel d'outil)

### Couche 2 : Smoke de passerelle + agent dev (ce que « @openclaw » fait réellement)

- Test : `src/gateway/gateway-models.profiles.live.test.ts`
- Objectif :
  - Démarrer une passerelle en processus
  - Créer/corriger une session `agent:dev:*` (modèle remplacé par exécution)
  - Itérer les modèles-avec-clés et affirmer :
    - « réponse significative » (pas d'outils)
    - une invocation d'outil réelle fonctionne (sonde de lecture)
    - sondes d'outil supplémentaires optionnelles (sonde exec+read)
    - Les chemins de régression OpenAI (tool-call-only → follow-up) continuent de fonctionner
- Détails de sonde (pour que vous puissiez expliquer rapidement les défaillances) :
  - sonde `read` : le test écrit un fichier nonce dans l'espace de travail et demande à l'agent de le `read` et d'écho le nonce.
  - sonde `exec+read` : le test demande à l'agent d'`exec`-écrire un nonce dans un fichier temporaire, puis de le `read` en arrière.
  - sonde d'image : le test joint un PNG généré (chat + code aléatoire) et s'attend à ce que le modèle retourne `cat <CODE>`.
  - Référence d'implémentation : `src/gateway/gateway-models.profiles.live.test.ts` et `src/gateway/live-image-probe.ts`.
- Comment activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
- Comment sélectionner les modèles :
  - Par défaut : liste blanche moderne (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.5, Grok 4)
  - `OPENCLAW_LIVE_GATEWAY_MODELS=all` est un alias pour la liste blanche moderne
  - Ou définissez `OPENCLAW_LIVE_GATEWAY_MODELS="provider/model"` (ou liste virgule) pour réduire
- Comment sélectionner les fournisseurs (éviter « OpenRouter tout ») :
  - `OPENCLAW_LIVE_GATEWAY_PROVIDERS="google,google-antigravity,google-gemini-cli,openai,anthropic,zai,minimax"` (liste blanche virgule)
- Les sondes d'outil + image sont toujours activées dans ce test live :
  - sonde `read` + sonde `exec+read` (stress d'outil)
  - la sonde d'image s'exécute quand le modèle annonce le support d'entrée d'image
  - Flux (haut niveau) :
    - Le test génère un petit PNG avec « CAT » + code aléatoire (`src/gateway/live-image-probe.ts`)
    - L'envoie via `agent` `attachments: [{ mimeType: "image/png", content: "<base64>" }]`
    - La passerelle analyse les pièces jointes en `images[]` (`src/gateway/server-methods/agent.ts` + `src/gateway/chat-attachments.ts`)
    - L'agent intégré transmet un message utilisateur multimodal au modèle
    - Assertion : la réponse contient `cat` + le code (tolérance OCR : les petites erreurs sont autorisées)

Conseil : pour voir ce que vous pouvez tester sur votre machine (et les identifiants `provider/model` exacts), exécutez :

```bash
openclaw models list
openclaw models list --json
```

## Live : smoke de jeton de configuration Anthropic

- Test : `src/agents/anthropic.setup-token.live.test.ts`
- Objectif : vérifier que le jeton de configuration Claude Code CLI (ou un profil de jeton de configuration collé) peut compléter une invite Anthropic.
- Activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
  - `OPENCLAW_LIVE_SETUP_TOKEN=1`
- Sources de jeton (choisissez-en une) :
  - Profil : `OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test`
  - Jeton brut : `OPENCLAW_LIVE_SETUP_TOKEN_VALUE=sk-ant-oat01-...`
- Remplacement de modèle (optionnel) :
  - `OPENCLAW_LIVE_SETUP_TOKEN_MODEL=anthropic/claude-opus-4-6`

Exemple de configuration :

```bash
openclaw models auth paste-token --provider anthropic --profile-id anthropic:setup-token-test
OPENCLAW_LIVE_SETUP_TOKEN=1 OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test pnpm test:live src/agents/anthropic.setup-token.live.test.ts
```

## Live : test de fumée du backend CLI (Claude Code CLI ou autres CLI locaux)

- Test : `src/gateway/gateway-cli-backend.live.test.ts`
- Objectif : valider le pipeline Gateway + agent en utilisant un backend CLI local, sans toucher à votre configuration par défaut.
- Activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
  - `OPENCLAW_LIVE_CLI_BACKEND=1`
- Valeurs par défaut :
  - Modèle : `claude-cli/claude-sonnet-4-6`
  - Commande : `claude`
  - Arguments : `["-p","--output-format","json","--permission-mode","bypassPermissions"]`
- Remplacements (optionnels) :
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-opus-4-6"`
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="codex-cli/gpt-5.4"`
  - `OPENCLAW_LIVE_CLI_BACKEND_COMMAND="/full/path/to/claude"`
  - `OPENCLAW_LIVE_CLI_BACKEND_ARGS='["-p","--output-format","json","--permission-mode","bypassPermissions"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_CLEAR_ENV='["ANTHROPIC_API_KEY","ANTHROPIC_API_KEY_OLD"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_PROBE=1` pour envoyer une véritable pièce jointe image (les chemins sont injectés dans l'invite).
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_ARG="--image"` pour passer les chemins de fichiers image en tant qu'arguments CLI au lieu d'injection d'invite.
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_MODE="repeat"` (ou `"list"`) pour contrôler comment les arguments image sont passés quand `IMAGE_ARG` est défini.
  - `OPENCLAW_LIVE_CLI_BACKEND_RESUME_PROBE=1` pour envoyer un deuxième tour et valider le flux de reprise.
- `OPENCLAW_LIVE_CLI_BACKEND_DISABLE_MCP_CONFIG=0` pour garder la configuration MCP de Claude Code CLI activée (par défaut désactive la configuration MCP avec un fichier vide temporaire).

Exemple :

```bash
OPENCLAW_LIVE_CLI_BACKEND=1 \
  OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-sonnet-4-6" \
  pnpm test:live src/gateway/gateway-cli-backend.live.test.ts
```

### Recettes live recommandées

Les listes d'autorisation étroites et explicites sont les plus rapides et les moins instables :

- Modèle unique, direct (pas de gateway) :
  - `OPENCLAW_LIVE_MODELS="openai/gpt-5.2" pnpm test:live src/agents/models.profiles.live.test.ts`

- Modèle unique, test de fumée gateway :
  - `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

- Appel d'outils sur plusieurs fournisseurs :
  - `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,google/gemini-3-flash-preview,zai/glm-4.7,minimax/minimax-m2.5" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

- Focus Google (clé API Gemini + Antigravity) :
  - Gemini (clé API) : `OPENCLAW_LIVE_GATEWAY_MODELS="google/gemini-3-flash-preview" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`
  - Antigravity (OAuth) : `OPENCLAW_LIVE_GATEWAY_MODELS="google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-pro-high" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

Remarques :

- `google/...` utilise l'API Gemini (clé API).
- `google-antigravity/...` utilise le pont OAuth Antigravity (point de terminaison agent de style Cloud Code Assist).
- `google-gemini-cli/...` utilise le CLI Gemini local sur votre machine (authentification séparée + particularités des outils).
- API Gemini vs CLI Gemini :
  - API : OpenClaw appelle l'API Gemini hébergée de Google via HTTP (authentification par clé API / profil) ; c'est ce que la plupart des utilisateurs entendent par « Gemini ».
  - CLI : OpenClaw exécute un binaire `gemini` local ; il a sa propre authentification et peut se comporter différemment (streaming/support des outils/décalage de version).

## Live : matrice de modèles (ce que nous couvrons)

Il n'y a pas de liste « CI model » fixe (live est opt-in), mais voici les modèles **recommandés** à couvrir régulièrement sur une machine de développement avec des clés.

### Ensemble de fumée moderne (appel d'outils + image)

C'est la exécution « modèles courants » que nous nous attendons à garder fonctionnelle :

- OpenAI (non-Codex) : `openai/gpt-5.2` (optionnel : `openai/gpt-5.1`)
- OpenAI Codex : `openai-codex/gpt-5.4`
- Anthropic : `anthropic/claude-opus-4-6` (ou `anthropic/claude-sonnet-4-5`)
- Google (API Gemini) : `google/gemini-3.1-pro-preview` et `google/gemini-3-flash-preview` (évitez les anciens modèles Gemini 2.x)
- Google (Antigravity) : `google-antigravity/claude-opus-4-6-thinking` et `google-antigravity/gemini-3-flash`
- Z.AI (GLM) : `zai/glm-4.7`
- MiniMax : `minimax/minimax-m2.5`

Exécutez le test de fumée gateway avec outils + image :
`OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.2,openai-codex/gpt-5.4,anthropic/claude-opus-4-6,google/gemini-3.1-pro-preview,google/gemini-3-flash-preview,google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-flash,zai/glm-4.7,minimax/minimax-m2.5" pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`

### Ligne de base : appel d'outils (Lecture + Exécution optionnelle)

Choisissez au moins un par famille de fournisseur :

- OpenAI : `openai/gpt-5.2` (ou `openai/gpt-5-mini`)
- Anthropic : `anthropic/claude-opus-4-6` (ou `anthropic/claude-sonnet-4-5`)
- Google : `google/gemini-3-flash-preview` (ou `google/gemini-3.1-pro-preview`)
- Z.AI (GLM) : `zai/glm-4.7`
- MiniMax : `minimax/minimax-m2.5`

Couverture supplémentaire optionnelle (agréable à avoir) :

- xAI : `xai/grok-4` (ou la dernière disponible)
- Mistral : `mistral/`… (choisissez un modèle capable « d'outils » que vous avez activé)
- Cerebras : `cerebras/`… (si vous avez accès)
- LM Studio : `lmstudio/`… (local ; l'appel d'outils dépend du mode API)

### Vision : envoi d'image (pièce jointe → message multimodal)

Incluez au moins un modèle capable d'images dans `OPENCLAW_LIVE_GATEWAY_MODELS` (variantes Claude/Gemini/OpenAI compatibles avec la vision, etc.) pour exercer la sonde d'image.

### Agrégateurs / gateways alternatifs

Si vous avez des clés activées, nous supportons également les tests via :

- OpenRouter : `openrouter/...` (des centaines de modèles ; utilisez `openclaw models scan` pour trouver des candidats capables d'outils + image)
- OpenCode : `opencode/...` pour Zen et `opencode-go/...` pour Go (authentification via `OPENCODE_API_KEY` / `OPENCODE_ZEN_API_KEY`)

Plus de fournisseurs que vous pouvez inclure dans la matrice live (si vous avez des identifiants/configuration) :

- Intégré : `openai`, `openai-codex`, `anthropic`, `google`, `google-vertex`, `google-antigravity`, `google-gemini-cli`, `zai`, `openrouter`, `opencode`, `opencode-go`, `xai`, `groq`, `cerebras`, `mistral`, `github-copilot`
- Via `models.providers` (points de terminaison personnalisés) : `minimax` (cloud/API), plus tout proxy compatible OpenAI/Anthropic (LM Studio, vLLM, LiteLLM, etc.)

Conseil : ne tentez pas de coder en dur « tous les modèles » dans la documentation. La liste faisant autorité est ce que `discoverModels(...)` retourne sur votre machine + les clés disponibles.

## Identifiants (ne jamais valider)

Les tests live découvrent les identifiants de la même manière que le CLI. Implications pratiques :

- Si le CLI fonctionne, les tests live devraient trouver les mêmes clés.
- Si un test live dit « pas d'identifiants », déboguez de la même manière que vous débogueriez `openclaw models list` / sélection de modèle.

- Magasin de profils : `~/.openclaw/credentials/` (préféré ; ce que « clés de profil » signifie dans les tests)
- Configuration : `~/.openclaw/openclaw.json` (ou `OPENCLAW_CONFIG_PATH`)

Si vous voulez vous fier aux clés env (par exemple exportées dans votre `~/.profile`), exécutez les tests locaux après `source ~/.profile`, ou utilisez les exécuteurs Docker ci-dessous (ils peuvent monter `~/.profile` dans le conteneur).

## Live Deepgram (transcription audio)

- Test : `src/media-understanding/providers/deepgram/audio.live.test.ts`
- Activer : `DEEPGRAM_API_KEY=... DEEPGRAM_LIVE_TEST=1 pnpm test:live src/media-understanding/providers/deepgram/audio.live.test.ts`

## Live plan de codage BytePlus

- Test : `src/agents/byteplus.live.test.ts`
- Activer : `BYTEPLUS_API_KEY=... BYTEPLUS_LIVE_TEST=1 pnpm test:live src/agents/byteplus.live.test.ts`
- Remplacement de modèle optionnel : `BYTEPLUS_CODING_MODEL=ark-code-latest`

## Exécuteurs Docker (vérifications optionnelles « fonctionne sous Linux »)

Ceux-ci exécutent `pnpm test:live` à l'intérieur de l'image Docker du dépôt, en montant votre répertoire de configuration local et votre espace de travail (et en sourçant `~/.profile` s'il est monté) :

- Modèles directs : `pnpm test:docker:live-models` (script : `scripts/test-live-models-docker.sh`)
- Gateway + agent de développement : `pnpm test:docker:live-gateway` (script : `scripts/test-live-gateway-models-docker.sh`)
- Assistant d'intégration (TTY, échafaudage complet) : `pnpm test:docker:onboard` (script : `scripts/e2e/onboard-docker.sh`)
- Réseau Gateway (deux conteneurs, authentification WS + santé) : `pnpm test:docker:gateway-network` (script : `scripts/e2e/gateway-network-docker.sh`)
- Plugins (chargement d'extension personnalisée + test de fumée du registre) : `pnpm test:docker:plugins` (script : `scripts/e2e/plugins-docker.sh`)

Les exécuteurs Docker de modèles live montent également le checkout actuel en lecture seule et
le mettent en scène dans un répertoire de travail temporaire à l'intérieur du conteneur. Cela garde l'image d'exécution
mince tout en exécutant Vitest contre votre source/configuration locale exacte.

Test de fumée de fil en langage naturel ACP manuel (pas CI) :

- `bun scripts/dev/discord-acp-plain-language-smoke.ts --channel <discord-channel-id> ...`
- Conservez ce script pour les flux de travail de régression/débogage. Il peut être nécessaire à nouveau pour la validation du routage des fils ACP, ne le supprimez donc pas.

Variables env utiles :

- `OPENCLAW_CONFIG_DIR=...` (par défaut : `~/.openclaw`) monté sur `/home/node/.openclaw`
- `OPENCLAW_WORKSPACE_DIR=...` (par défaut : `~/.openclaw/workspace`) monté sur `/home/node/.openclaw/workspace`
- `OPENCLAW_PROFILE_FILE=...` (par défaut : `~/.profile`) monté sur `/home/node/.profile` et sourcé avant d'exécuter les tests
- `OPENCLAW_LIVE_GATEWAY_MODELS=...` / `OPENCLAW_LIVE_MODELS=...` pour réduire l'exécution
- `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` pour s'assurer que les identifiants proviennent du magasin de profils (pas env)

## Vérification de santé des documents

Exécutez les vérifications de documents après les modifications de documents : `pnpm docs:list`.

## Régression hors ligne (sûre pour CI)

Ce sont des régressions « pipeline réel » sans vrais fournisseurs :

- Appel d'outils Gateway (OpenAI simulé, pipeline gateway + agent réel) : `src/gateway/gateway.test.ts` (cas : « exécute un appel d'outil OpenAI simulé de bout en bout via la boucle d'agent gateway »)
- Assistant Gateway (WS `wizard.start`/`wizard.next`, écrit la configuration + authentification appliquée) : `src/gateway/gateway.test.ts` (cas : « exécute l'assistant sur ws et écrit la configuration du jeton d'authentification »)

## Évaluations de fiabilité des agents (compétences)

Nous avons déjà quelques tests sûrs pour CI qui se comportent comme des « évaluations de fiabilité des agents » :

- Appel d'outils simulé via la gateway réelle + boucle d'agent (`src/gateway/gateway.test.ts`).
- Flux d'assistant de bout en bout qui valident le câblage de session et les effets de configuration (`src/gateway/gateway.test.ts`).

Ce qui manque encore pour les compétences (voir [Compétences](/fr/tools/skills)) :

- **Prise de décision :** quand les compétences sont listées dans l'invite, l'agent choisit-il la bonne compétence (ou évite-t-il les compétences non pertinentes) ?
- **Conformité :** l'agent lit-il `SKILL.md` avant utilisation et suit-il les étapes/arguments requis ?
- **Contrats de flux de travail :** scénarios multi-tours qui affirment l'ordre des outils, la conservation de l'historique de session et les limites du bac à sable.

Les futures évaluations doivent rester déterministes en premier :

- Un exécuteur de scénario utilisant des fournisseurs simulés pour affirmer les appels d'outils + ordre, les lectures de fichiers de compétences et le câblage de session.
- Une petite suite de scénarios axés sur les compétences (utilisation vs évitement, gating, injection d'invite).
- Évaluations live optionnelles (opt-in, env-gated) uniquement après que la suite sûre pour CI soit en place.

## Ajout de régressions (conseils)

Quand vous corrigez un problème de fournisseur/modèle découvert en live :

- Ajoutez une régression sûre pour CI si possible (fournisseur simulé/stub, ou capturez la transformation exacte de la forme de la requête)
- Si c'est intrinsèquement live-only (limites de débit, politiques d'authentification), gardez le test live étroit et opt-in via des variables env
- Préférez cibler la couche la plus petite qui attrape le bug :
  - bug de conversion/relecture de requête de fournisseur → test de modèles directs
  - bug de pipeline de session/historique/outils gateway → test de fumée live gateway ou test mock gateway sûr pour CI
- Garde-fou de traversée SecretRef :
  - `src/secrets/exec-secret-ref-id-parity.test.ts` dérive une cible échantillonnée par classe SecretRef à partir des métadonnées du registre (`listSecretTargetRegistryEntries()`), puis affirme que les identifiants exec des segments de traversée sont rejetés.
  - Si vous ajoutez une nouvelle famille de cibles SecretRef `includeInPlan` dans `src/secrets/target-registry-data.ts`, mettez à jour `classifyTargetClass` dans ce test. Le test échoue intentionnellement sur les identifiants de cibles non classifiées afin que les nouvelles classes ne puissent pas être ignorées silencieusement.
