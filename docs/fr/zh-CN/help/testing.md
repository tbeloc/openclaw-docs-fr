# Tester

OpenClaw inclut trois suites de tests Vitest (unité/intégration, bout en bout, en direct) ainsi qu'un petit ensemble d'exécuteurs Docker.

Ce document est un guide "comment nous testons" :

- Ce que couvre chaque suite (et ce qu'elle *ne couvre intentionnellement pas*)
- Quelles commandes exécuter pour les flux de travail courants (local, avant push, débogage)
- Comment les tests en direct découvrent les identifiants et sélectionnent les modèles/fournisseurs
- Comment ajouter des tests de régression pour les problèmes réels de modèles/fournisseurs

## Démarrage rapide

Utilisation quotidienne :

- Vérification complète (flux attendu avant push) : `pnpm build && pnpm check && pnpm test`

Quand vous modifiez les tests ou avez besoin de plus de confiance :

- Vérification de couverture : `pnpm test:coverage`
- Suite bout en bout : `pnpm test:e2e`

Débogage de vrais fournisseurs/modèles (nécessite de vrais identifiants) :

- Suite en direct (modèles + outils Gateway/sonde d'image) : `pnpm test:live`

Conseil : quand vous n'avez besoin que d'un cas d'échec, il est recommandé d'utiliser les variables d'environnement de liste blanche décrites ci-dessous pour réduire la portée des tests en direct.

## Suites de tests (où exécuter quoi)

Ces suites peuvent être comprises comme "réalisme progressivement croissant" (et instabilité/coût progressivement croissants) :

### Tests unitaires/intégration (par défaut)

- Commande : `pnpm test`
- Configuration : `vitest.config.ts`
- Fichiers : `src/**/*.test.ts`
- Portée :
  - Tests unitaires purs
  - Tests d'intégration en processus (authentification Gateway, routage, outils, analyse, configuration)
  - Tests de régression déterministes pour les problèmes connus
- Attentes :
  - Exécution en CI
  - Pas besoin de vraies clés
  - Devrait être rapide et stable

### Tests bout en bout (tests de fumée Gateway)

- Commande : `pnpm test:e2e`
- Configuration : `vitest.e2e.config.ts`
- Fichiers : `src/**/*.e2e.test.ts`
- Portée :
  - Comportement bout en bout multi-instances Gateway
  - Interfaces WebSocket/HTTP, appairage de nœuds et opérations réseau plus lourdes
- Attentes :
  - Exécution en CI (quand activé dans le pipeline)
  - Pas besoin de vraies clés
  - Plus de pièces mobiles que les tests unitaires (peut être plus lent)

### Tests en direct (vrais fournisseurs + vrais modèles)

- Commande : `pnpm test:live`
- Configuration : `vitest.live.config.ts`
- Fichiers : `src/**/*.live.test.ts`
- Par défaut : **activé** via `pnpm test:live` (définit `OPENCLAW_LIVE_TEST=1`)
- Portée :
  - "Ce fournisseur/modèle fonctionne-t-il réellement *aujourd'hui* avec de vrais identifiants ?"
  - Capture les changements de format des fournisseurs, les bizarreries d'appels d'outils, les problèmes d'authentification et le comportement des limites de débit
- Attentes :
  - Par conception, ne convient pas à une exécution stable en CI (réseau réel, vraies politiques de fournisseurs, quotas, pannes)
  - Coûte de l'argent/utilise les limites de débit
  - Recommandé d'exécuter un sous-ensemble réduit plutôt que "tout"
  - L'exécution en direct charge `~/.profile` pour les clés API manquantes
  - Rotation des clés Anthropic : définissez `OPENCLAW_LIVE_ANTHROPIC_KEYS="sk-...,sk-..."` (ou `OPENCLAW_LIVE_ANTHROPIC_KEY=sk-...`) ou plusieurs variables `ANTHROPIC_API_KEY*` ; les tests réessaient en cas de limite de débit

## Quelle suite dois-je exécuter ?

Utilisez ce tableau de décision :

- Édition de logique/tests : exécutez `pnpm test` (ajoutez `pnpm test:coverage` si les changements sont importants)
- Implique le réseau Gateway/protocole WS/appairage : ajoutez `pnpm test:e2e`
- Débogage "mon bot est cassé"/défaillance spécifique au fournisseur/appel d'outil : exécutez `pnpm test:live` réduit

## Tests en direct : tests de fumée de modèles (clés de fichier de configuration)

Les tests en direct sont divisés en deux couches pour isoler les défaillances :

- "Modèle direct" nous dit si le fournisseur/modèle répond correctement avec la clé donnée.
- "Test de fumée Gateway" nous dit si le pipeline complet Gateway + agent fonctionne correctement pour ce modèle (sessions, historique, outils, politiques de bac à sable, etc.).

### Couche 1 : complétions de modèles directs (sans Gateway)

- Test : `src/agents/models.profiles.live.test.ts`
- Objectifs :
  - Énumérer les modèles découverts
  - Utiliser `getApiKeyForModel` pour sélectionner les modèles pour lesquels vous avez des identifiants
  - Exécuter une petite complétion pour chaque modèle (et des tests de régression ciblés si nécessaire)
- Comment activer :
  - `pnpm test:live` (ou utilisez `OPENCLAW_LIVE_TEST=1` lors de l'appel direct de Vitest)
- Définissez `OPENCLAW_LIVE_MODELS=modern` (ou `all`, alias de modern) pour exécuter réellement cette suite ; sinon elle est ignorée pour garder `pnpm test:live` concentré sur les tests de fumée Gateway
- Comment sélectionner les modèles :
  - `OPENCLAW_LIVE_MODELS=modern` exécute la liste blanche moderne (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.1, Grok 4)
  - `OPENCLAW_LIVE_MODELS=all` est un alias de la liste blanche moderne
  - Ou `OPENCLAW_LIVE_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-5,..."` (liste blanche séparée par des virgules)
- Comment sélectionner les fournisseurs :
  - `OPENCLAW_LIVE_PROVIDERS="google,google-antigravity,google-gemini-cli"` (liste blanche séparée par des virgules)
- Sources de clés :
  - Par défaut : stockage de fichier de configuration et secours aux variables d'environnement
  - Définissez `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` pour forcer **utiliser uniquement le stockage de fichier de configuration**
- Pourquoi ce test existe :
  - Séparer "l'API du fournisseur est cassée/clé invalide" de "le pipeline d'agent Gateway est cassé"
  - Inclut de petits tests de régression isolés (par exemple : relecture de réponses OpenAI/Codex + flux d'appels d'outils)

### Couche 2 : test de fumée Gateway + agent de développement ("ce que @openclaw fait réellement")

- Test : `src/gateway/gateway-models.profiles.live.test.ts`
- Objectifs :
  - Démarrer une Gateway en processus
  - Créer/patcher une session `agent:dev:*` (couvre les modèles à chaque exécution)
  - Itérer sur les modèles pour lesquels vous avez des clés et affirmer :
    - Réponses "sensées" (pas d'outils)
    - Les vrais appels d'outils fonctionnent correctement (sonde de lecture)
    - Sondes d'outils supplémentaires optionnelles (sonde exec+lecture)
    - Le chemin de régression OpenAI (appels d'outils uniquement → suivi) reste fonctionnel
- Détails des sondes (pour que vous puissiez expliquer rapidement les défaillances) :
  - Sonde `read` : le test écrit un fichier avec un nombre aléatoire dans l'espace de travail, demande à l'agent de le `read` et d'écho le nombre.
  - Sonde `exec+read` : le test demande à l'agent d'`exec` pour écrire le nombre dans un fichier temporaire, puis de le `read`.
  - Sonde d'image : le test joint un PNG généré (chat + code aléatoire), s'attend à ce que le modèle retourne `cat <CODE>`.
  - Référence d'implémentation : `src/gateway/gateway-models.profiles.live.test.ts` et `src/gateway/live-image-probe.ts`.
- Comment activer :
  - `pnpm test:live` (ou utilisez `OPENCLAW_LIVE_TEST=1` lors de l'appel direct de Vitest)
- Comment sélectionner les modèles :
  - Par défaut : liste blanche moderne (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.1, Grok 4)
  - `OPENCLAW_LIVE_GATEWAY_MODELS=all` est un alias de la liste blanche moderne
  - Ou définissez `OPENCLAW_LIVE_GATEWAY_MODELS="provider/model"` (ou liste séparée par des virgules) pour réduire
- Comment sélectionner les fournisseurs (éviter "OpenRouter tout") :
  - `OPENCLAW_LIVE_GATEWAY_PROVIDERS="google,google-antigravity,google-gemini-cli,openai,anthropic,zai,minimax"` (liste blanche séparée par des virgules)
- Les sondes d'outils + d'image sont toujours activées dans ce test en direct :
  - Sonde `read` + sonde `exec+read` (test de stress des outils)
  - Sonde d'image exécutée quand le modèle déclare le support d'entrée d'image
  - Flux (haut niveau) :
    - Le test génère un petit PNG avec "CAT" + code aléatoire (`src/gateway/live-image-probe.ts`)
    - Envoyé via `agent` `attachments: [{ mimeType: "image/png", content: "<base64>" }]`
    - Gateway analyse les pièces jointes en `images[]` (`src/gateway/server-methods/agent.ts` + `src/gateway/chat-attachments.ts`)
    - L'agent intégré transmet le message utilisateur multimodal au modèle
    - Affirmer : la réponse contient `cat` + code (tolérance OCR : erreurs légères autorisées)

Conseil : pour voir ce qui peut être testé sur votre machine (et les ID exacts `provider/model`), exécutez :

```bash
openclaw models list
openclaw models list --json
```

## Tests en direct : test de fumée de jeton de configuration Anthropic

- Test : `src/agents/anthropic.setup-token.live.test.ts`
- Objectif : vérifier que le jeton de configuration Claude Code CLI (ou la configuration du jeton de configuration collée) peut compléter les invites Anthropic.
- Activation :
  - `pnpm test:live` (ou utilisez `OPENCLAW_LIVE_TEST=1` lors de l'appel direct de Vitest)
  - `OPENCLAW_LIVE_SETUP_TOKEN=1`
- Sources de jetons (choisissez-en une) :
  - Fichier de configuration : `OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test`
  - Jeton brut : `OPENCLAW_LIVE_SETUP_TOKEN_VALUE=sk-ant-oat01-...`
- Couverture de modèles (optionnel) :
  - `OPENCLAW_LIVE_SETUP_TOKEN_MODEL=anthropic/claude-opus-4-5`

Exemple de configuration :

```bash
openclaw models auth paste-token --provider anthropic --profile-id anthropic:setup-token-test
OPENCLAW_LIVE_SETUP_TOKEN=1 OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test pnpm test:live src/agents/anthropic.setup-token.live.test.ts
```

## Tests en direct : test de fumée du backend CLI (Claude Code CLI ou autre CLI local)

- Test : `src/gateway/gateway-cli-backend.live.test.ts`
- Objectif : vérifier le pipeline Gateway + agent avec un backend CLI local sans affecter votre configuration par défaut.
- Activation :
  - `pnpm test:live` (ou utilisez `OPENCLAW_LIVE_TEST=1` lors de l'appel direct de Vitest)
  - `OPENCLAW_LIVE_CLI_BACKEND=1`
- Valeurs par défaut :
  - Modèle : `claude-cli/claude-sonnet-4-5`
  - Commande : `claude`
  - Arguments : `["-p","--output-format","json","--dangerously-skip-permissions"]`
- Remplacements (optionnel) :
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-opus-4-5"`
  - `OPENCLAW_LIVE_CLI_BACKEND_MODEL="codex-cli/gpt-5.2-codex"`
  - `OPENCLAW_LIVE_CLI_BACKEND_COMMAND="/full/path/to/claude"`
  - `OPENCLAW_LIVE_CLI_BACKEND_ARGS='["-p","--output-format","json","--permission-mode","bypassPermissions"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_CLEAR_ENV='["ANTHROPIC_API_KEY","ANTHROPIC_API_KEY_OLD"]'`
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_PROBE=1` envoie de vraies pièces jointes d'image (chemin injecté dans l'invite).
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_ARG="--image"` transmet le chemin du fichier image comme argument CLI plutôt que par injection d'invite.
  - `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_MODE="repeat"` (ou `"list"`) contrôle comment les arguments d'image sont transmis quand `IMAGE_ARG` est défini.
  - `OPENCLAW_LIVE_CLI_BACKEND_RESUME_PROBE=1` envoie un deuxième tour et vérifie le flux de reprise.
- `OPENC
