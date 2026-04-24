---
summary: "Configuration des outils (politique, basculements expérimentaux, outils soutenus par des fournisseurs) et configuration personnalisée des fournisseurs/URL de base"
read_when:
  - Configuration de la politique `tools.*`, listes blanches ou fonctionnalités expérimentales
  - Enregistrement de fournisseurs personnalisés ou remplacement des URL de base
  - Configuration des points de terminaison auto-hébergés compatibles avec OpenAI
title: "Configuration — outils et fournisseurs personnalisés"
---

Clés de configuration `tools.*` et configuration personnalisée des fournisseurs / URL de base. Pour les agents,
les canaux et autres clés de configuration de haut niveau, voir
[Référence de configuration](/fr/gateway/configuration-reference).

## Outils

### Profils d'outils

`tools.profile` définit une liste d'autorisation de base avant `tools.allow`/`tools.deny` :

Les configurations locales par défaut des nouveaux paramètres locaux sont définies sur `tools.profile: "coding"` lorsqu'elles ne sont pas définies (les profils explicites existants sont conservés).

| Profil      | Inclut                                                                                                                      |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- |
| `minimal`   | `session_status` uniquement                                                                                                 |
| `coding`    | `group:fs`, `group:runtime`, `group:web`, `group:sessions`, `group:memory`, `cron`, `image`, `image_generate`, `video_generate` |
| `messaging` | `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`                                   |
| `full`      | Aucune restriction (identique à non défini)                                                                                 |

### Groupes d'outils

| Groupe             | Outils                                                                                                                  |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `group:runtime`    | `exec`, `process`, `code_execution` (`bash` est accepté comme alias pour `exec`)                                         |
| `group:fs`         | `read`, `write`, `edit`, `apply_patch`                                                                                  |
| `group:sessions`   | `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `sessions_yield`, `subagents`, `session_status` |
| `group:memory`     | `memory_search`, `memory_get`                                                                                           |
| `group:web`        | `web_search`, `x_search`, `web_fetch`                                                                                   |
| `group:ui`         | `browser`, `canvas`                                                                                                     |
| `group:automation` | `cron`, `gateway`                                                                                                       |
| `group:messaging`  | `message`                                                                                                               |
| `group:nodes`      | `nodes`                                                                                                                 |
| `group:agents`     | `agents_list`                                                                                                           |
| `group:media`      | `image`, `image_generate`, `video_generate`, `tts`                                                                      |
| `group:openclaw`   | Tous les outils intégrés (exclut les plugins de fournisseur)                                                             |

### `tools.allow` / `tools.deny`

Politique d'autorisation/refus d'outils globale (le refus l'emporte). Insensible à la casse, supporte les caractères génériques `*`. Appliqué même lorsque le bac à sable Docker est désactivé.

```json5
{
  tools: { deny: ["browser", "canvas"] },
}
```

### `tools.byProvider`

Restreindre davantage les outils pour des fournisseurs ou modèles spécifiques. Ordre : profil de base → profil de fournisseur → allow/deny.

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
      "openai/gpt-5.4": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

### `tools.elevated`

Contrôle l'accès exec élevé en dehors du bac à sable :

```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        whatsapp: ["+15555550123"],
        discord: ["1234567890123", "987654321098765432"],
      },
    },
  },
}
```

- Le remplacement par agent (`agents.list[].tools.elevated`) ne peut que restreindre davantage.
- `/elevated on|off|ask|full` stocke l'état par session ; les directives en ligne s'appliquent à un seul message.
- L'`exec` élevé contourne le bac à sable et utilise le chemin d'échappement configuré (`gateway` par défaut, ou `node` lorsque la cible exec est `node`).

### `tools.exec`

```json5
{
  tools: {
    exec: {
      backgroundMs: 10000,
      timeoutSec: 1800,
      cleanupMs: 1800000,
      notifyOnExit: true,
      notifyOnExitEmptySuccess: false,
      applyPatch: {
        enabled: false,
        allowModels: ["gpt-5.5"],
      },
    },
  },
}
```

### `tools.loopDetection`

Les vérifications de sécurité des boucles d'outils sont **désactivées par défaut**. Définissez `enabled: true` pour activer la détection.
Les paramètres peuvent être définis globalement dans `tools.loopDetection` et remplacés par agent à `agents.list[].tools.loopDetection`.

```json5
{
  tools: {
    loopDetection: {
      enabled: true,
      historySize: 30,
      warningThreshold: 10,
      criticalThreshold: 20,
      globalCircuitBreakerThreshold: 30,
      detectors: {
        genericRepeat: true,
        knownPollNoProgress: true,
        pingPong: true,
      },
    },
  },
}
```

- `historySize` : historique maximal des appels d'outils conservé pour l'analyse des boucles.
- `warningThreshold` : seuil de motif sans progression répétée pour les avertissements.
- `criticalThreshold` : seuil de répétition plus élevé pour bloquer les boucles critiques.
- `globalCircuitBreakerThreshold` : seuil d'arrêt dur pour toute exécution sans progression.
- `detectors.genericRepeat` : avertir sur les appels répétés du même outil/mêmes arguments.
- `detectors.knownPollNoProgress` : avertir/bloquer sur les outils d'interrogation connus (`process.poll`, `command_status`, etc.).
- `detectors.pingPong` : avertir/bloquer sur les motifs de paires alternées sans progression.
- Si `warningThreshold >= criticalThreshold` ou `criticalThreshold >= globalCircuitBreakerThreshold`, la validation échoue.

### `tools.web`

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "brave_api_key", // ou BRAVE_API_KEY env
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
      fetch: {
        enabled: true,
        provider: "firecrawl", // optionnel ; omettez pour la détection automatique
        maxChars: 50000,
        maxCharsCap: 50000,
        maxResponseBytes: 2000000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        readability: true,
        userAgent: "custom-ua",
      },
    },
  },
}
```

### `tools.media`

Configure la compréhension des médias entrants (image/audio/vidéo) :

```json5
{
  tools: {
    media: {
      concurrency: 2,
      asyncCompletion: {
        directSend: false, // opt-in : envoyer la musique/vidéo asynchrone terminée directement au canal
      },
      audio: {
        enabled: true,
        maxBytes: 20971520,
        scope: {
          default: "deny",
          rules: [{ action: "allow", match: { chatType: "direct" } }],
        },
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          { type: "cli", command: "whisper", args: ["--model", "base", "{{MediaPath}}"] },
        ],
      },
      video: {
        enabled: true,
        maxBytes: 52428800,
        models: [{ provider: "google", model: "gemini-3-flash-preview" }],
      },
    },
  },
}
```

<Accordion title="Champs d'entrée du modèle média">

**Entrée de fournisseur** (`type: "provider"` ou omis) :

- `provider` : identifiant du fournisseur API (`openai`, `anthropic`, `google`/`gemini`, `groq`, etc.)
- `model` : remplacement de l'identifiant du modèle
- `profile` / `preferredProfile` : sélection du profil `auth-profiles.json`

**Entrée CLI** (`type: "cli"`) :

- `command` : exécutable à exécuter
- `args` : arguments modélisés (supporte `{{MediaPath}}`, `{{Prompt}}`, `{{MaxChars}}`, etc.)

**Champs communs :**

- `capabilities` : liste optionnelle (`image`, `audio`, `video`). Valeurs par défaut : `openai`/`anthropic`/`minimax` → image, `google` → image+audio+vidéo, `groq` → audio.
- `prompt`, `maxChars`, `maxBytes`, `timeoutSeconds`, `language` : remplacements par entrée.
- Les défaillances reviennent à l'entrée suivante.

L'authentification du fournisseur suit l'ordre standard : `auth-profiles.json` → variables d'environnement → `models.providers.*.apiKey`.

**Champs d'achèvement asynchrone :**

- `asyncCompletion.directSend` : lorsque `true`, les tâches `music_generate`
  et `video_generate` asynchrones terminées tentent d'abord la livraison directe au canal. Par défaut : `false`
  (chemin hérité de réveil de session demandeur/livraison de modèle).

</Accordion>

### `tools.agentToAgent`

```json5
{
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },
}
```

### `tools.sessions`

Contrôle les sessions qui peuvent être ciblées par les outils de session (`sessions_list`, `sessions_history`, `sessions_send`).

Par défaut : `tree` (session actuelle + sessions générées par celle-ci, comme les sous-agents).

```json5
{
  tools: {
    sessions: {
      // "self" | "tree" | "agent" | "all"
      visibility: "tree",
    },
  },
}
```

Notes :

- `self` : uniquement la clé de session actuelle.
- `tree` : session actuelle + sessions générées par la session actuelle (sous-agents).
- `agent` : toute session appartenant à l'identifiant d'agent actuel (peut inclure d'autres utilisateurs si vous exécutez des sessions par expéditeur sous le même identifiant d'agent).
- `all` : toute session. Le ciblage inter-agents nécessite toujours `tools.agentToAgent`.
- Serrage du bac à sable : lorsque la session actuelle est en bac à sable et `agents.defaults.sandbox.sessionToolsVisibility="spawned"`, la visibilité est forcée à `tree` même si `tools.sessions.visibility="all"`.

### `tools.sessions_spawn`

Contrôle le support des pièces jointes en ligne pour `sessions_spawn`.

```json5
{
  tools: {
    sessions_spawn: {
      attachments: {
        enabled: false, // opt-in : définissez true pour autoriser les pièces jointes de fichiers en ligne
        maxTotalBytes: 5242880, // 5 Mo au total sur tous les fichiers
        maxFiles: 50,
        maxFileBytes: 1048576, // 1 Mo par fichier
        retainOnSessionKeep: false, // conserver les pièces jointes lorsque cleanup="keep"
      },
    },
  },
}
```

Notes :

- Les pièces jointes ne sont supportées que pour `runtime: "subagent"`. Le runtime ACP les rejette.
- Les fichiers sont matérialisés dans l'espace de travail enfant à `.openclaw/attachments/<uuid>/` avec un `.manifest.json`.
- Le contenu des pièces jointes est automatiquement masqué de la persistance des transcriptions.
- Les entrées Base64 sont validées avec des vérifications strictes d'alphabet/remplissage et une garde de taille pré-décodage.
- Les permissions des fichiers sont `0700` pour les répertoires et `0600` pour les fichiers.
- Le nettoyage suit la politique `cleanup` : `delete` supprime toujours les pièces jointes ; `keep` les conserve uniquement lorsque `retainOnSessionKeep: true`.

<a id="toolsexperimental"></a>

### `tools.experimental`

Drapeaux d'outils intégrés expérimentaux. Désactivé par défaut sauf si une règle d'activation automatique GPT-5 strictement agentique s'applique.

```json5
{
  tools: {
    experimental: {
      planTool: true, // activer la mise à jour expérimentale du plan
    },
  },
}
```

Notes :

- `planTool` : active l'outil structuré `update_plan` pour le suivi du travail multi-étapes non trivial.
- Par défaut : `false` sauf si `agents.defaults.embeddedPi.executionContract` (ou un remplacement par agent) est défini sur `"strict-agentic"` pour une exécution de famille GPT-5 OpenAI ou OpenAI Codex. Définissez `true` pour forcer l'outil en dehors de cette portée, ou `false` pour le maintenir désactivé même pour les exécutions GPT-5 strictement agentiques.
- Lorsqu'activé, l'invite système ajoute également des conseils d'utilisation pour que le modèle ne l'utilise que pour un travail substantiel et conserve au maximum une étape `in_progress`.

### `agents.defaults.subagents`

```json5
{
  agents: {
    defaults: {
      subagents: {
        allowAgents: ["research"],
        model: "minimax/MiniMax-M2.7",
        maxConcurrent: 8,
        runTimeoutSeconds: 900,
        archiveAfterMinutes: 60,
      },
    },
  },
}
```

- `model` : modèle par défaut pour les sous-agents générés. S'il est omis, les sous-agents héritent du modèle de l'appelant.
- `allowAgents` : liste d'autorisation par défaut des identifiants d'agent cible pour `sessions_spawn` lorsque l'agent demandeur ne définit pas son propre `subagents.allowAgents` (`["*"]` = n'importe lequel ; par défaut : même agent uniquement).
- `runTimeoutSeconds` : délai d'expiration par défaut (secondes) pour `sessions_spawn` lorsque l'appel d'outil omet `runTimeoutSeconds`. `0` signifie pas de délai d'expiration.
- Politique d'outils par sous-agent : `tools.subagents.tools.allow` / `tools.subagents.tools.deny`.

## Fournisseurs personnalisés et URLs de base

OpenClaw utilise le catalogue de modèles intégré. Ajoutez des fournisseurs personnalisés via `models.providers` dans la configuration ou `~/.openclaw/agents/<agentId>/agent/models.json`.

```json5
{
  models: {
    mode: "merge", // merge (default) | replace
    providers: {
      "custom-proxy": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "LITELLM_KEY",
        api: "openai-completions", // openai-completions | openai-responses | anthropic-messages | google-generative-ai
        models: [
          {
            id: "llama-3.1-8b",
            name: "Llama 3.1 8B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            contextTokens: 96000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

- Utilisez `authHeader: true` + `headers` pour les besoins d'authentification personnalisés.
- Remplacez la racine de la configuration de l'agent avec `OPENCLAW_AGENT_DIR` (ou `PI_CODING_AGENT_DIR`, un alias de variable d'environnement hérité).
- Ordre de précédence de fusion pour les ID de fournisseur correspondants :
  - Les valeurs `baseUrl` non vides dans `models.json` de l'agent gagnent.
  - Les valeurs `apiKey` non vides de l'agent gagnent uniquement lorsque ce fournisseur n'est pas géré par SecretRef dans le contexte de configuration/profil d'authentification actuel.
  - Les valeurs `apiKey` du fournisseur gérées par SecretRef sont actualisées à partir des marqueurs source (`ENV_VAR_NAME` pour les références env, `secretref-managed` pour les références fichier/exec) au lieu de persister les secrets résolus.
  - Les valeurs d'en-tête du fournisseur gérées par SecretRef sont actualisées à partir des marqueurs source (`secretref-env:ENV_VAR_NAME` pour les références env, `secretref-managed` pour les références fichier/exec).
  - Les `apiKey`/`baseUrl` vides ou manquants de l'agent reviennent à `models.providers` dans la configuration.
  - Les `contextWindow`/`maxTokens` du modèle correspondant utilisent la valeur la plus élevée entre les valeurs de configuration explicites et les valeurs du catalogue implicite.
  - Les `contextTokens` du modèle correspondant préservent un plafond d'exécution explicite lorsqu'il est présent ; utilisez-le pour limiter le contexte effectif sans modifier les métadonnées du modèle natif.
  - Utilisez `models.mode: "replace"` lorsque vous souhaitez que la configuration réécrive complètement `models.json`.
  - La persistance des marqueurs est source-autoritaire : les marqueurs sont écrits à partir de l'instantané de configuration source actif (pré-résolution), et non à partir des valeurs de secret d'exécution résolues.

### Détails des champs du fournisseur

- `models.mode` : comportement du catalogue du fournisseur (`merge` ou `replace`).
- `models.providers` : carte de fournisseur personnalisé indexée par ID de fournisseur.
  - Modifications sûres : utilisez `openclaw config set models.providers.<id> '<json>' --strict-json --merge` ou `openclaw config set models.providers.<id>.models '<json-array>' --strict-json --merge` pour les mises à jour additives. `config set` refuse les remplacements destructifs sauf si vous passez `--replace`.
- `models.providers.*.api` : adaptateur de requête (`openai-completions`, `openai-responses`, `anthropic-messages`, `google-generative-ai`, etc).
- `models.providers.*.apiKey` : identifiant du fournisseur (préférez la substitution SecretRef/env).
- `models.providers.*.auth` : stratégie d'authentification (`api-key`, `token`, `oauth`, `aws-sdk`).
- `models.providers.*.injectNumCtxForOpenAICompat` : pour Ollama + `openai-completions`, injectez `options.num_ctx` dans les requêtes (par défaut : `true`).
- `models.providers.*.authHeader` : forcez le transport des identifiants dans l'en-tête `Authorization` lorsque requis.
- `models.providers.*.baseUrl` : URL de base de l'API en amont.
- `models.providers.*.headers` : en-têtes statiques supplémentaires pour le routage proxy/locataire.
- `models.providers.*.request` : remplacements de transport pour les requêtes HTTP modèle-fournisseur.
  - `request.headers` : en-têtes supplémentaires (fusionnés avec les valeurs par défaut du fournisseur). Les valeurs acceptent SecretRef.
  - `request.auth` : remplacement de la stratégie d'authentification. Modes : `"provider-default"` (utiliser l'authentification intégrée du fournisseur), `"authorization-bearer"` (avec `token`), `"header"` (avec `headerName`, `value`, `prefix` optionnel).
  - `request.proxy` : remplacement du proxy HTTP. Modes : `"env-proxy"` (utiliser les variables d'environnement `HTTP_PROXY`/`HTTPS_PROXY`), `"explicit-proxy"` (avec `url`). Les deux modes acceptent un sous-objet `tls` optionnel.
  - `request.tls` : remplacement TLS pour les connexions directes. Champs : `ca`, `cert`, `key`, `passphrase` (tous acceptent SecretRef), `serverName`, `insecureSkipVerify`.
  - `request.allowPrivateNetwork` : lorsque `true`, autorisez HTTPS vers `baseUrl` lorsque DNS se résout en plages privées, CGNAT ou similaires, via la garde de récupération HTTP du fournisseur (opt-in de l'opérateur pour les points de terminaison OpenAI-compatibles auto-hébergés de confiance). WebSocket utilise le même `request` pour les en-têtes/TLS mais pas cette porte SSRF de récupération. Par défaut `false`.
- `models.providers.*.models` : entrées du catalogue de modèles explicites du fournisseur.
- `models.providers.*.models.*.contextWindow` : métadonnées de fenêtre de contexte du modèle natif.
- `models.providers.*.models.*.contextTokens` : plafond de contexte d'exécution optionnel. Utilisez ceci lorsque vous souhaitez un budget de contexte effectif plus petit que le `contextWindow` natif du modèle.
- `models.providers.*.models.*.compat.supportsDeveloperRole` : indice de compatibilité optionnel. Pour `api: "openai-completions"` avec un `baseUrl` non vide et non natif (hôte pas `api.openai.com`), OpenClaw force ceci à `false` à l'exécution. Un `baseUrl` vide/omis conserve le comportement OpenAI par défaut.
- `models.providers.*.models.*.compat.requiresStringContent` : indice de compatibilité optionnel pour les points de terminaison de chat OpenAI-compatibles acceptant uniquement des chaînes. Lorsque `true`, OpenClaw aplatit les tableaux `messages[].content` de texte pur en chaînes simples avant d'envoyer la requête.
- `plugins.entries.amazon-bedrock.config.discovery` : racine des paramètres de découverte automatique Bedrock.
- `plugins.entries.amazon-bedrock.config.discovery.enabled` : activez/désactivez la découverte implicite.
- `plugins.entries.amazon-bedrock.config.discovery.region` : région AWS pour la découverte.
- `plugins.entries.amazon-bedrock.config.discovery.providerFilter` : filtre d'ID de fournisseur optionnel pour la découverte ciblée.
- `plugins.entries.amazon-bedrock.config.discovery.refreshInterval` : intervalle d'interrogation pour l'actualisation de la découverte.
- `plugins.entries.amazon-bedrock.config.discovery.defaultContextWindow` : fenêtre de contexte de secours pour les modèles découverts.
- `plugins.entries.amazon-bedrock.config.discovery.defaultMaxTokens` : jetons de sortie maximaux de secours pour les modèles découverts.

### Exemples de fournisseurs

<Accordion title="Cerebras (GLM 4.6 / 4.7)">

```json5
{
  env: { CEREBRAS_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: {
        primary: "cerebras/zai-glm-4.7",
        fallbacks: ["cerebras/zai-glm-4.6"],
      },
      models: {
        "cerebras/zai-glm-4.7": { alias: "GLM 4.7 (Cerebras)" },
        "cerebras/zai-glm-4.6": { alias: "GLM 4.6 (Cerebras)" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "zai-glm-4.7", name: "GLM 4.7 (Cerebras)" },
          { id: "zai-glm-4.6", name: "GLM 4.6 (Cerebras)" },
        ],
      },
    },
  },
}
```

Utilisez `cerebras/zai-glm-4.7` pour Cerebras ; `zai/glm-4.7` pour Z.AI direct.

</Accordion>

<Accordion title="OpenCode">

```json5
{
  agents: {
    defaults: {
      model: { primary: "opencode/claude-opus-4-6" },
      models: { "opencode/claude-opus-4-6": { alias: "Opus" } },
    },
  },
}
```

Définissez `OPENCODE_API_KEY` (ou `OPENCODE_ZEN_API_KEY`). Utilisez les références `opencode/...` pour le catalogue Zen ou les références `opencode-go/...` pour le catalogue Go. Raccourci : `openclaw onboard --auth-choice opencode-zen` ou `openclaw onboard --auth-choice opencode-go`.

</Accordion>

<Accordion title="Z.AI (GLM-4.7)">

```json5
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-4.7" },
      models: { "zai/glm-4.7": {} },
    },
  },
}
```

Définissez `ZAI_API_KEY`. Les alias `z.ai/*` et `z-ai/*` sont acceptés. Raccourci : `openclaw onboard --auth-choice zai-api-key`.

- Point de terminaison général : `https://api.z.ai/api/paas/v4`
- Point de terminaison de codage (par défaut) : `https://api.z.ai/api/coding/paas/v4`
- Pour le point de terminaison général, définissez un fournisseur personnalisé avec le remplacement d'URL de base.

</Accordion>

<Accordion title="Moonshot AI (Kimi)">

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.6" },
      models: { "moonshot/kimi-k2.6": { alias: "Kimi K2.6" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2.6",
            name: "Kimi K2.6",
            reasoning: false,
            input: ["text", "image"],
            cost: { input: 0.95, output: 4, cacheRead: 0.16, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 262144,
          },
        ],
      },
    },
  },
}
```

Pour le point de terminaison China : `baseUrl: "https://api.moonshot.cn/v1"` ou `openclaw onboard --auth-choice moonshot-api-key-cn`.

Les points de terminaison Moonshot natifs annoncent la compatibilité d'utilisation du streaming sur le transport partagé `openai-completions`, et OpenClaw les clés qui désactivent les capacités du point de terminaison plutôt que l'ID de fournisseur intégré seul.

</Accordion>

<Accordion title="Kimi Coding">

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi/kimi-code" },
      models: { "kimi/kimi-code": { alias: "Kimi Code" } },
    },
  },
}
```

Compatible avec Anthropic, fournisseur intégré. Raccourci : `openclaw onboard --auth-choice kimi-code-api-key`.

</Accordion>

<Accordion title="Synthetic (Compatible avec Anthropic)">

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.5" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.5": { alias: "MiniMax M2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

L'URL de base doit omettre `/v1` (le client Anthropic l'ajoute). Raccourci : `openclaw onboard --auth-choice synthetic-api-key`.

</Accordion>

<Accordion title="MiniMax M2.7 (direct)">

```json5
{
  agents: {
    defaults: {
      model: { primary: "minimax/MiniMax-M2.7" },
      models: {
        "minimax/MiniMax-M2.7": { alias: "Minimax" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.7",
            name: "MiniMax M2.7",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0.3, output: 1.2, cacheRead: 0.06, cacheWrite: 0.375 },
            contextWindow: 204800,
            maxTokens: 131072,
          },
        ],
      },
    },
  },
}
```

Définissez `MINIMAX_API_KEY`. Raccourcis :
`openclaw onboard --auth-choice minimax-global-api` ou
`openclaw onboard --auth-choice minimax-cn-api`.
Le catalogue de modèles utilise par défaut M2.7 uniquement.
Sur le chemin de streaming compatible Anthropic, OpenClaw désactive la réflexion MiniMax par défaut sauf si vous la définissez explicitement vous-même. `/fast on` ou `params.fastMode: true` réécrit `MiniMax-M2.7` en `MiniMax-M2.7-highspeed`.

</Accordion>

<Accordion title="Modèles locaux (LM Studio)">

Voir [Modèles locaux](/fr/gateway/local-models). TL;DR : exécutez un grand modèle local via l'API Responses de LM Studio sur du matériel sérieux ; conservez les modèles hébergés fusionnés pour la solution de secours.

</Accordion>

---

## Connexes

- [Référence de configuration](/fr/gateway/configuration-reference) — autres clés de niveau supérieur
- [Configuration — agents](/fr/gateway/config-agents)
- [Configuration — canaux](/fr/gateway/config-channels)
- [Outils et plugins](/fr/tools)
