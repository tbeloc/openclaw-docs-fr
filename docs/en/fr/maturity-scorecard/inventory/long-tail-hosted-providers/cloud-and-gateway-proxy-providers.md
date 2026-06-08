---
title: "Fournisseurs hébergés long-tail - Note de maturité des fournisseurs Cloud et Gateway"
version: 3
last_refreshed: 2026-05-30
last_refreshed_by: codex
---

# Fournisseurs hébergés long-tail - Note de maturité des fournisseurs Cloud et Gateway

## Résumé

Les fournisseurs de proxy cloud et gateway sont en Alpha. Les manifestes de fournisseurs et la documentation couvrent la surface, et GitHub Copilot/OpenCode ont des chemins actifs, mais Bedrock, Cloudflare AI Gateway, Vercel AI Gateway, LiteLLM et les proxies similaires ont des preuves d'exécution plus minces et plus d'ambiguïté concernant les identifiants et les routes.

## Portée de la catégorie

Cette note couvre Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway, LiteLLM, Microsoft Foundry, GitHub Copilot, OpenCode, OpenCode Go et Kilo Gateway.

Hors de portée : OpenRouter en tant qu'agrégateur hébergé noté séparément, les fournisseurs de proxy locaux tels que LM Studio/vLLM/SGLang locaux, et les fournisseurs OpenAI/Anthropic de première partie.

## Fonctionnalités

- Configuration de Bedrock : Couvre la configuration de Bedrock sur Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway et le comportement des fournisseurs cloud et gateway associés.
- Routage Gateway/proxy : Couvre le routage Gateway/proxy sur Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway et le comportement des fournisseurs cloud et gateway associés.
- Accès hébergé Copilot/OpenCode : Couvre l'accès hébergé Copilot/OpenCode sur Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway et le comportement des fournisseurs cloud et gateway associés.
- Diagnostics de capacité proxy : Couvre les diagnostics de capacité proxy sur Amazon Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway et le comportement des fournisseurs cloud et gateway associés.

## Fraîcheur de l'archive

- gitcrawl : `gitcrawl doctor --json` a réussi avec `version=0.2.1`, `last_sync_at=2026-05-28T19:09:52.784704Z`, `repository_count=2`, `thread_count=29810`, `open_thread_count=11181`, `cluster_count=18594`, `db_path=/Users/kevinlin/.config/gitcrawl/stores/gitcrawl-store/data/openclaw__openclaw.sync.db`, `api_supported=false`, `github_token_present=false` et `openai_key_present=true`.
- discrawl : `discrawl status --json` a réussi avec `state=current`, `generated_at=2026-05-30T14:10:20Z`, `last_sync_at=2026-05-29T19:27:40Z`, `messages=1487536`, `channels=25831`, `threads=25603`, `embedding_backlog=0`, `database_path=/Users/kevinlin/Library/Application Support/discrawl/discrawl.db`, `database_bytes=8035926016`, `share.remote=git@github.com-personal:openclaw/discord-store.git` et `share.needs_update=true`.

## Score de couverture

- Score : `Alpha (58%)`
- Signaux positifs :
  - Le répertoire des fournisseurs et la documentation des modèles-fournisseurs listent Bedrock, Bedrock Mantle, Cloudflare AI Gateway, LiteLLM, Vercel AI Gateway, GitHub Copilot, Kilo Gateway et OpenCode/OpenCode Go.
  - Des manifestes existent pour Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway, LiteLLM, Microsoft Foundry, GitHub Copilot, OpenCode, OpenCode Go et Kilo.
  - GitHub Copilot a un chemin actif de token/modèle.
  - OpenCode a un chemin texte hébergé actif et une documentation de configuration de modèle.
  - La couverture unitaire existe pour Bedrock, Bedrock Mantle, Cloudflare AI Gateway, Vercel AI Gateway, LiteLLM, GitHub Copilot, OpenCode et Kilo.
- Signaux négatifs :
  - Les fournisseurs de proxy cloud/gateway ne partagent pas une seule voie de smoke actif récurrente.
  - Bedrock et les proxies gateway ont une preuve de bout en bout plus faible que les adaptateurs de fournisseurs hébergés directs.
  - Le succès des proxies cloud/gateway dépend souvent de la sélection de route en amont, des identifiants, de l'URL de base et de la politique de compte en dehors d'OpenClaw.

## Score de qualité

- Score : `Alpha (56%)`
- Bonnes qualités :
  - La documentation sépare les plugins de fournisseurs groupés de la configuration personnalisée de proxy/URL de base `models.providers`.
  - Bedrock est représenté comme un plugin de fournisseur et comme métadonnées de catalogue externe officiel.
  - Les chemins GitHub Copilot et OpenCode sont plus matures que le reste de ce composant.
  - La documentation des fournisseurs explique le comportement du gateway/proxy et les attentes en matière d'identifiants.
- Mauvaises qualités :
  - Les fournisseurs de proxy/gateway composent les défaillances de la configuration OpenClaw, des identifiants de fournisseur, du routage du gateway en amont, de la capacité du modèle en amont et de l'état du compte distant.
  - La chaîne d'identifiants AWS SDK de Bedrock ne se comporte pas comme les fournisseurs de clé API normaux, et l'historique du support Discord montre que cela nécessite un diagnostic explicite.
  - Cloudflare AI Gateway, Vercel AI Gateway, LiteLLM et Microsoft Foundry ont une documentation moins uniforme des identifiants, des routes et du comportement du compte que les chemins Copilot/OpenCode plus forts.
- Exclus de la qualité :
  - Les preuves unitaires, d'intégration et actives ont été utilisées uniquement pour le score de couverture.

## Score de complétude

- Score : `Alpha (58%)`
- Instructions de surface : évaluées par rapport à `references/completeness/long-tail-hosted-providers.md`.
- Signaux positifs : les preuves archivées, source, test, Gitcrawl et Discrawl couvrent la portée de la taxonomie pour la configuration de Bedrock, le routage Gateway/proxy, l'accès hébergé Copilot/OpenCode, les diagnostics de capacité proxy.
- Signaux négatifs : la note archivée a précédé le score de complétude de la version 3 du processus, donc ce score est initialisé à partir de la même largeur de preuve et du registre des lacunes connues utilisé pour le score de couverture archivé.
- Branches de capacité manquantes : voir `## Lacunes connues` et `## Preuves` ci-dessous pour les branches manquantes enregistrées et les avertissements visibles par l'opérateur.

## Lacunes connues

- Ajouter un smoke de fournisseur actif pour Bedrock, Vercel AI Gateway, Cloudflare AI Gateway, LiteLLM et Microsoft Foundry avec des contrôles d'identifiants d'opt-in clairs.
- Ajouter une page de diagnostic proxy/gateway qui sépare les erreurs de configuration OpenClaw des erreurs de gateway en amont, de profil AWS et de capacité de modèle.
- Ajouter un tableau de route/capacité pour les fournisseurs de proxy couvrant le comportement des outils, images, raisonnement et fallback.

## Preuves

### Docs

- `/Users/kevinlin/code/openclaw/docs/providers/index.md:28` : le répertoire des fournisseurs lie Amazon Bedrock.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:29` : le répertoire des fournisseurs lie Amazon Bedrock Mantle.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:36` : le répertoire des fournisseurs lie Cloudflare AI Gateway.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:43` : le répertoire des fournisseurs lie GitHub Copilot.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:49` : le répertoire des fournisseurs lie Kilo.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:50` : le répertoire des fournisseurs lie LiteLLM.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:58` : le répertoire des fournisseurs lie OpenCode.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:59` : le répertoire des fournisseurs lie OpenCode Go.
- `/Users/kevinlin/code/openclaw/docs/providers/index.md:72` : le répertoire des fournisseurs lie Vercel AI Gateway.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:343` : la documentation explique `models.providers` pour les fournisseurs personnalisés et les proxies compatibles OpenAI/Anthropic.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:345` : la documentation dit que de nombreux plugins de fournisseurs groupés publient déjà un catalogue par défaut, et les entrées explicites `models.providers` sont pour les remplacements.
- `/Users/kevinlin/code/openclaw/docs/concepts/model-providers.md:263` : la documentation lie les références de configuration Z.AI et Vercel AI Gateway.

### Source

- `/Users/kevinlin/code/openclaw/extensions/amazon-bedrock/openclaw.plugin.json:2` : le manifeste du fournisseur Amazon Bedrock existe.
- `/Users/kevinlin/code/openclaw/extensions/amazon-bedrock-mantle/openclaw.plugin.json:2` : le manifeste du fournisseur Amazon Bedrock Mantle existe.
- `/Users/kevinlin/code/openclaw/extensions/cloudflare-ai-gateway/openclaw.plugin.json:2` : le manifeste du fournisseur Cloudflare AI Gateway existe.
- `/Users/kevinlin/code/openclaw/extensions/vercel-ai-gateway/openclaw.plugin.json:2` : le manifeste du fournisseur Vercel AI Gateway existe.
- `/Users/kevinlin/code/openclaw/extensions/litellm/openclaw.plugin.json:2` : le manifeste du fournisseur LiteLLM existe.
- `/Users/kevinlin/code/openclaw/extensions/microsoft-foundry/openclaw.plugin.json:2` : le manifeste du fournisseur Microsoft Foundry existe.
- `/Users/kevinlin/code/openclaw/extensions/github-copilot/openclaw.plugin.json:2` : le manifeste du fournisseur GitHub Copilot existe.
- `/Users/kevinlin/code/openclaw/extensions/opencode/openclaw.plugin.json:2` : le manifeste du fournisseur OpenCode existe.
- `/Users/kevinlin/code/openclaw/extensions/opencode-go/openclaw.plugin.json:2` : le manifeste du fournisseur OpenCode Go existe.
- `/Users/kevinlin/code/openclaw/extensions/kilocode/openclaw.plugin.json:2` : le manifeste du fournisseur Kilo existe.

### Tests d'intégration

- `/Users/kevinlin/code/openclaw/extensions/github-copilot/connection-bound-ids.live.test.ts:148` : le test actif GitHub Copilot démarre l'échange de token et les vérifications d'accès au modèle.
- `/Users/kevinlin/code/openclaw/extensions/opencode/opencode.live.test.ts:18` : le test actif OpenCode configure la configuration du modèle hébergé actif DeepSeek pour le chemin du fournisseur hébergé.
- `/Users/kevinlin/code/openclaw/extensions/opencode/opencode.live.test.ts:60` : le test actif OpenCode couvre la relecture de la réflexion après le contexte d'appel d'outil.
- `/Users/kevinlin/code/openclaw/docs/help/testing-live.md:414` : la documentation liste OpenRouter et OpenCode parmi les agrégateurs et les gateways alternatifs à inclure lorsque les clés sont activées.

### Tests unitaires

- `/Users/kevinlin/code/openclaw/extensions/amazon-bedrock/index.test.ts` : couverture unitaire du comportement du fournisseur Bedrock.
- `/Users/kevinlin/code/openclaw/extensions/amazon-bedrock-mantle/index.test.ts` : couverture unitaire du comportement du fournisseur Bedrock Mantle.
- `/Users/kevinlin/code/openclaw/extensions/cloudflare-ai-gateway/index.test.ts` : couverture unitaire du comportement de Cloudflare AI Gateway.
- `/Users/kevinlin/code/openclaw/extensions/vercel-ai-gateway/provider-catalog.test.ts` : couverture unitaire du comportement du catalogue des fournisseurs Vercel AI Gateway.
- `/Users/kevinlin/code/openclaw/extensions/litellm/index.test.ts` : couverture unitaire du comportement du fournisseur LiteLLM.
- `/Users/kevinlin/code/openclaw/extensions/github-copilot/index.test.ts` : couverture unitaire du comportement du fournisseur GitHub Copilot.
- `/Users/kevinlin/code/openclaw/extensions/kilocode/index.test.ts` : couverture unitaire du comportement du fournisseur Kilo.

### Requêtes Gitcrawl

- `gitcrawl --json search issues -R openclaw/openclaw "Bedrock Cloudflare Vercel LiteLLM provider"` a retourné `[]`.
- `gitcrawl --json search prs -R openclaw/openclaw "Bedrock Cloudflare Vercel LiteLLM provider"` a retourné uniquement #87202, qui est une preuve adjacente et faible.
- `gitcrawl --json search prs -R openclaw/openclaw "provider metadata model catalog"` a retourné des changements de métadonnées/catalogue incluant #85345, #83292 et #43493 qui sont pertinents pour le changement de métadonnées/catalogue du fournisseur/gateway.

### Requêtes Discrawl

- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "Bedrock Cloudflare Vercel LiteLLM provider" --limit 5` a retourné une réponse d'assistance listant Bedrock, LiteLLM, Vercel AI Gateway et Cloudflare AI Gateway comme options, et notant que les couches de gateway peuvent aider au routage, aux tentatives et à l'observabilité.
- `env DISCRAWL_NO_AUTO_UPDATE=1 discrawl --json search "provider auth setup env vars" --limit 5` a retourné des conseils de support Bedrock expliquant que Bedrock utilise la chaîne d'identifiants AWS SDK et que les erreurs AWS signifient que le Gateway ne peut pas voir les identifiants AWS.
