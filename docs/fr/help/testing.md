---
summary: "Kit de test : suites unit/e2e/live, exécuteurs Docker, et ce que chaque test couvre"
read_when:
  - Exécution de tests localement ou en CI
  - Ajout de régressions pour les bugs de modèle/fournisseur
  - Débogage du comportement de la passerelle + agent
title: "Tests"
---

# Tests

OpenClaw dispose de trois suites Vitest (unit/intégration, e2e, live) et d'un petit ensemble d'exécuteurs Docker.

Ce document est un guide "comment nous testons" :

- Ce que chaque suite couvre (et ce qu'elle ne couvre délibérément _pas_)
- Quelles commandes exécuter pour les workflows courants (local, pré-push, débogage)
- Comment les tests live découvrent les identifiants et sélectionnent les modèles/fournisseurs
- Comment ajouter des régressions pour les problèmes réels de modèle/fournisseur

## Démarrage rapide

La plupart des jours :

- Portail complet (attendu avant le push) : `pnpm build && pnpm check && pnpm test`

Quand vous touchez aux tests ou voulez plus de confiance :

- Portail de couverture : `pnpm test:coverage`
- Suite E2E : `pnpm test:e2e`

Lors du débogage de fournisseurs/modèles réels (nécessite des identifiants réels) :

- Suite live (modèles + sondes d'outil/image de passerelle) : `pnpm test:live`

Conseil : quand vous n'avez besoin que d'un seul cas défaillant, préférez réduire les tests live via les variables d'environnement de liste blanche décrites ci-dessous.

## Suites de test (ce qui s'exécute où)

Pensez aux suites comme "réalisme croissant" (et instabilité/coût croissants) :

### Unit / intégration (par défaut)

- Commande : `pnpm test`
- Config : `scripts/test-parallel.mjs` (exécute `vitest.unit.config.ts`, `vitest.extensions.config.ts`, `vitest.gateway.config.ts`)
- Fichiers : `src/**/*.test.ts`, `extensions/**/*.test.ts`
- Portée :
  - Tests unitaires purs
  - Tests d'intégration en processus (authentification de passerelle, routage, outillage, analyse, config)
  - Régressions déterministes pour les bugs connus
- Attentes :
  - S'exécute en CI
  - Aucune clé réelle requise
  - Doit être rapide et stable
- Note sur le pool :
  - OpenClaw utilise Vitest `vmForks` sur Node 22/23 pour des shards unitaires plus rapides.
  - Sur Node 24+, OpenClaw revient automatiquement à `forks` réguliers pour éviter les erreurs de liaison VM Node (`ERR_VM_MODULE_LINK_FAILURE` / `module is already linked`).
  - Remplacez manuellement avec `OPENCLAW_TEST_VM_FORKS=0` (forcer `forks`) ou `OPENCLAW_TEST_VM_FORKS=1` (forcer `vmForks`).

### E2E (fumée de passerelle)

- Commande : `pnpm test:e2e`
- Config : `vitest.e2e.config.ts`
- Fichiers : `src/**/*.e2e.test.ts`
- Valeurs par défaut du runtime :
  - Utilise Vitest `vmForks` pour un démarrage de fichier plus rapide.
  - Utilise des workers adaptatifs (CI : 2-4, local : 4-8).
  - S'exécute en mode silencieux par défaut pour réduire la surcharge d'E/S console.
- Remplacements utiles :
  - `OPENCLAW_E2E_WORKERS=<n>` pour forcer le nombre de workers (limité à 16).
  - `OPENCLAW_E2E_VERBOSE=1` pour réactiver la sortie console détaillée.
- Portée :
  - Comportement end-to-end de passerelle multi-instance
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
  - "Ce fournisseur/modèle fonctionne-t-il réellement _aujourd'hui_ avec des identifiants réels ?"
  - Détecter les changements de format de fournisseur, les bizarreries d'appel d'outil, les problèmes d'authentification et le comportement des limites de débit
- Attentes :
  - Non stable en CI par conception (réseaux réels, politiques réelles de fournisseur, quotas, pannes)
  - Coûte de l'argent / utilise les limites de débit
  - Préférez exécuter des sous-ensembles réduits au lieu de "tout"
  - Les exécutions live vont sourcer `~/.profile` pour récupérer les clés API manquantes
- Rotation de clé API (spécifique au fournisseur) : définissez `*_API_KEYS` avec format virgule/point-virgule ou `*_API_KEY_1`, `*_API_KEY_2` (par exemple `OPENAI_API_KEYS`, `ANTHROPIC_API_KEYS`, `GEMINI_API_KEYS`) ou remplacez live via `OPENCLAW_LIVE_*_KEY` ; les tests réessaient sur les réponses de limite de débit.

## Quelle suite dois-je exécuter ?

Utilisez ce tableau de décision :

- Édition de logique/tests : exécutez `pnpm test` (et `pnpm test:coverage` si vous avez beaucoup changé)
- Toucher au réseautage de passerelle / protocole WS / appairage : ajoutez `pnpm test:e2e`
- Débogage "mon bot est en panne" / défaillances spécifiques au fournisseur / appel d'outil : exécutez un `pnpm test:live` réduit

## Live : balayage de capacité de nœud Android

- Test : `src/gateway/android-node.capabilities.live.test.ts`
- Script : `pnpm android:test:integration`
- Objectif : invoquer **chaque commande actuellement annoncée** par un nœud Android connecté et affirmer le comportement du contrat de commande.
- Portée :
  - Configuration précondition/manuelle (la suite n'installe/n'exécute/n'appaire pas l'application).
  - Validation `node.invoke` de passerelle commande par commande pour le nœud Android sélectionné.
- Configuration préalable requise :
  - Application Android déjà connectée + appairée à la passerelle.
  - Application maintenue au premier plan.
  - Permissions/consentement de capture accordés pour les capacités que vous vous attendez à réussir.
- Remplacements de cible optionnels :
  - `OPENCLAW_ANDROID_NODE_ID` ou `OPENCLAW_ANDROID_NODE_NAME`.
  - `OPENCLAW_ANDROID_GATEWAY_URL` / `OPENCLAW_ANDROID_GATEWAY_TOKEN` / `OPENCLAW_ANDROID_GATEWAY_PASSWORD`.
- Détails complets de configuration Android : [Application Android](/platforms/android)

## Live : fumée de modèle (clés de profil)

Les tests live sont divisés en deux couches pour que nous puissions isoler les défaillances :

- "Modèle direct" nous dit que le fournisseur/modèle peut répondre du tout avec la clé donnée.
- "Fumée de passerelle" nous dit que le pipeline complet passerelle+agent fonctionne pour ce modèle (sessions, historique, outils, politique sandbox, etc.).

### Couche 1 : Complétion de modèle direct (pas de passerelle)

- Test : `src/agents/models.profiles.live.test.ts`
- Objectif :
  - Énumérer les modèles découverts
  - Utiliser `getApiKeyForModel` pour sélectionner les modèles pour lesquels vous avez des identifiants
  - Exécuter une petite complétion par modèle (et des régressions ciblées si nécessaire)
- Comment activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
- Définissez `OPENCLAW_LIVE_MODELS=modern` (ou `all`, alias pour modern) pour exécuter réellement cette suite ; sinon elle saute pour garder `pnpm test:live` concentré sur la fumée de passerelle
- Comment sélectionner les modèles :
  - `OPENCLAW_LIVE_MODELS=modern` pour exécuter la liste blanche moderne (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.5, Grok 4)
  - `OPENCLAW_LIVE_MODELS=all` est un alias pour la liste blanche moderne
  - ou `OPENCLAW_LIVE_MODELS="openai/gpt-5.2,anthropic/claude-opus-4-6,..."` (liste blanche virgule)
- Comment sélectionner les fournisseurs :
  - `OPENCLAW_LIVE_PROVIDERS="google,google-antigravity,google-gemini-cli"` (liste blanche virgule)
- D'où viennent les clés :
  - Par défaut : magasin de profil et replis env
  - Définissez `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` pour appliquer **magasin de profil** uniquement
- Pourquoi cela existe :
  - Sépare "l'API du fournisseur est cassée / la clé est invalide" de "le pipeline d'agent de passerelle est cassé"
  - Contient de petites régressions isolées (exemple : OpenAI Responses/Codex Responses relecture de raisonnement + flux d'appel d'outil)

### Couche 2 : Fumée de passerelle + agent dev (ce que "@openclaw" fait réellement)

- Test : `src/gateway/gateway-models.profiles.live.test.ts`
- Objectif :
  - Démarrer une passerelle en processus
  - Créer/corriger une session `agent:dev:*` (modèle remplacé par exécution)
  - Itérer les modèles-avec-clés et affirmer :
    - "réponse significative" (pas d'outils)
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
- Comment sélectionner les fournisseurs (éviter "OpenRouter tout") :
  - `OPENCLAW_LIVE_GATEWAY_PROVIDERS="google,google-antigravity,google-gemini-cli,openai,anthropic,zai,minimax"` (liste blanche virgule)
- Les sondes d'outil + image sont toujours activées dans ce test live :
  - sonde `read` + sonde `exec+read` (stress d'outil)
  - la sonde d'image s'exécute quand le modèle annonce le support d'entrée d'image
  - Flux (haut niveau) :
    - Le test génère un petit PNG avec "CAT" + code aléatoire (`src/gateway/live-image-probe.ts`)
    - L'envoie via `agent` `attachments: [{ mimeType: "image/png", content: "<base64>" }]`
    - La passerelle analyse les pièces jointes en `images[]` (`src/gateway/server-methods/agent.ts` + `src/gateway/chat-attachments.ts`)
    - L'agent intégré transmet un message utilisateur multimodal au modèle
    - Assertion : la réponse contient `cat` + le code (tolérance OCR : les petites erreurs sont autorisées)

Conseil : pour voir ce que vous pouvez tester sur votre machine (et les identifiants exacts `provider/model`), exécutez :

```bash
openclaw models list
openclaw models list --json
```

## Live : fumée de jeton de configuration Anthropic

- Test : `src/agents/anthropic.setup-token.live.test.ts`
- Objectif : vérifier que le jeton de configuration Claude Code CLI (ou un profil de jeton de configuration collé) peut compléter une invite Anthropic.
- Activer :
  - `pnpm test:live` (ou `OPENCLAW_LIVE_TEST=1` si vous invoquez Vitest directement)
  - `OPENCLAW_LIVE_SETUP_TOKEN=1`
- Sources de jeton (choisissez-en une) :
  - Profil : `
