---
summary: "Valeurs par défaut des agents, routage multi-agent, session, messages et configuration talk"
read_when:
  - Ajustement des valeurs par défaut des agents (modèles, réflexion, espace de travail, battement cardiaque, médias, compétences)
  - Configuration du routage et des liaisons multi-agent
  - Ajustement du comportement de la session, de la livraison des messages et du mode talk
title: "Configuration — agents"
---

Clés de configuration au niveau de l'agent sous `agents.*`, `multiAgent.*`, `session.*`,
`messages.*`, et `talk.*`. Pour les canaux, les outils, le runtime de la passerelle et autres
clés de niveau supérieur, voir [Référence de configuration](/fr/gateway/configuration-reference).

## Valeurs par défaut des agents

### `agents.defaults.workspace`

Par défaut : `~/.openclaw/workspace`.

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

### `agents.defaults.repoRoot`

Racine du référentiel optionnelle affichée dans la ligne Runtime de l'invite système. Si non défini, OpenClaw détecte automatiquement en remontant à partir de l'espace de travail.

```json5
{
  agents: { defaults: { repoRoot: "~/Projects/openclaw" } },
}
```

### `agents.defaults.skills`

Liste de compétences par défaut optionnelle pour les agents qui ne définissent pas
`agents.list[].skills`.

```json5
{
  agents: {
    defaults: { skills: ["github", "weather"] },
    list: [
      { id: "writer" }, // hérite de github, weather
      { id: "docs", skills: ["docs-search"] }, // remplace les valeurs par défaut
      { id: "locked-down", skills: [] }, // aucune compétence
    ],
  },
}
```

- Omettez `agents.defaults.skills` pour des compétences sans restriction par défaut.
- Omettez `agents.list[].skills` pour hériter des valeurs par défaut.
- Définissez `agents.list[].skills: []` pour aucune compétence.
- Une liste `agents.list[].skills` non vide est l'ensemble final pour cet agent ; elle ne fusionne pas avec les valeurs par défaut.

### `agents.defaults.skipBootstrap`

Désactive la création automatique des fichiers d'amorçage de l'espace de travail (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`).

```json5
{
  agents: { defaults: { skipBootstrap: true } },
}
```

### `agents.defaults.contextInjection`

Contrôle quand les fichiers d'amorçage de l'espace de travail sont injectés dans l'invite système. Par défaut : `"always"`.

- `"continuation-skip"` : les tours de continuation sûrs (après une réponse d'assistant complétée) ignorent la réinjection d'amorçage de l'espace de travail, réduisant la taille de l'invite. Les exécutions de battement cardiaque et les nouvelles tentatives post-compaction reconstruisent toujours le contexte.

```json5
{
  agents: { defaults: { contextInjection: "continuation-skip" } },
}
```

### `agents.defaults.bootstrapMaxChars`

Nombre maximum de caractères par fichier d'amorçage de l'espace de travail avant troncature. Par défaut : `12000`.

```json5
{
  agents: { defaults: { bootstrapMaxChars: 12000 } },
}
```

### `agents.defaults.bootstrapTotalMaxChars`

Nombre maximum total de caractères injectés dans tous les fichiers d'amorçage de l'espace de travail. Par défaut : `60000`.

```json5
{
  agents: { defaults: { bootstrapTotalMaxChars: 60000 } },
}
```

### `agents.defaults.bootstrapPromptTruncationWarning`

Contrôle le texte d'avertissement visible par l'agent quand le contexte d'amorçage est tronqué.
Par défaut : `"once"`.

- `"off"` : ne jamais injecter de texte d'avertissement dans l'invite système.
- `"once"` : injecter l'avertissement une fois par signature de troncature unique (recommandé).
- `"always"` : injecter l'avertissement à chaque exécution quand une troncature existe.

```json5
{
  agents: { defaults: { bootstrapPromptTruncationWarning: "once" } }, // off | once | always
}
```

### Carte de propriété du budget de contexte

OpenClaw dispose de plusieurs budgets d'invite/contexte à haut volume, et ils sont intentionnellement divisés par sous-système au lieu de tous circuler à travers un seul bouton générique.

- `agents.defaults.bootstrapMaxChars` /
  `agents.defaults.bootstrapTotalMaxChars` :
  injection d'amorçage d'espace de travail normal.
- `agents.defaults.startupContext.*` :
  prélude de démarrage unique `/new` et `/reset`, incluant les fichiers `memory/*.md` quotidiens récents.
- `skills.limits.*` :
  la liste compacte des compétences injectée dans l'invite système.
- `agents.defaults.contextLimits.*` :
  extraits d'exécution limités et blocs injectés appartenant à l'exécution.
- `memory.qmd.limits.*` :
  taille d'injection et d'extrait de recherche de mémoire indexée.

Utilisez la substitution par agent correspondante uniquement quand un agent a besoin d'un budget différent :

- `agents.list[].skillsLimits.maxSkillsPromptChars`
- `agents.list[].contextLimits.*`

#### `agents.defaults.startupContext`

Contrôle le prélude de démarrage du premier tour injecté sur les exécutions `/new` et `/reset` nues.

```json5
{
  agents: {
    defaults: {
      startupContext: {
        enabled: true,
        applyOn: ["new", "reset"],
        dailyMemoryDays: 2,
        maxFileBytes: 16384,
        maxFileChars: 1200,
        maxTotalChars: 2800,
      },
    },
  },
}
```

#### `agents.defaults.contextLimits`

Valeurs par défaut partagées pour les surfaces de contexte d'exécution limité.

```json5
{
  agents: {
    defaults: {
      contextLimits: {
        memoryGetMaxChars: 12000,
        memoryGetDefaultLines: 120,
        toolResultMaxChars: 16000,
        postCompactionMaxChars: 1800,
      },
    },
  },
}
```

- `memoryGetMaxChars` : plafond d'extrait `memory_get` par défaut avant l'ajout des métadonnées de troncature et de l'avis de continuation.
- `memoryGetDefaultLines` : fenêtre de ligne `memory_get` par défaut quand `lines` est omis.
- `toolResultMaxChars` : plafond de résultat d'outil en direct utilisé pour les résultats persistants et la récupération de débordement.
- `postCompactionMaxChars` : plafond d'extrait AGENTS.md utilisé lors de l'injection d'actualisation post-compaction.

#### `agents.list[].contextLimits`

Substitution par agent pour les boutons `contextLimits` partagés. Les champs omis héritent de `agents.defaults.contextLimits`.

```json5
{
  agents: {
    defaults: {
      contextLimits: {
        memoryGetMaxChars: 12000,
        toolResultMaxChars: 16000,
      },
    },
    list: [
      {
        id: "tiny-local",
        contextLimits: {
          memoryGetMaxChars: 6000,
          toolResultMaxChars: 8000,
        },
      },
    ],
  },
}
```

#### `skills.limits.maxSkillsPromptChars`

Plafond global pour la liste compacte des compétences injectée dans l'invite système. Cela n'affecte pas la lecture des fichiers `SKILL.md` à la demande.

```json5
{
  skills: {
    limits: {
      maxSkillsPromptChars: 18000,
    },
  },
}
```

#### `agents.list[].skillsLimits.maxSkillsPromptChars`

Substitution par agent pour le budget d'invite des compétences.

```json5
{
  agents: {
    list: [
      {
        id: "tiny-local",
        skillsLimits: {
          maxSkillsPromptChars: 6000,
        },
      },
    ],
  },
}
```

### `agents.defaults.imageMaxDimensionPx`

Taille maximale en pixels pour le côté le plus long de l'image dans les blocs d'image de transcription/outil avant les appels du fournisseur.
Par défaut : `1200`.

Les valeurs plus basses réduisent généralement l'utilisation des jetons de vision et la taille de la charge utile de la demande pour les exécutions riches en captures d'écran.
Les valeurs plus élevées préservent plus de détails visuels.

```json5
{
  agents: { defaults: { imageMaxDimensionPx: 1200 } },
}
```

### `agents.defaults.userTimezone`

Fuseau horaire pour le contexte de l'invite système (pas les horodatages des messages). Revient au fuseau horaire de l'hôte.

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

### `agents.defaults.timeFormat`

Format d'heure dans l'invite système. Par défaut : `auto` (préférence du système d'exploitation).

```json5
{
  agents: { defaults: { timeFormat: "auto" } }, // auto | 12 | 24
}
```

### `agents.defaults.model`

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "minimax/MiniMax-M2.7": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.7"],
      },
      imageModel: {
        primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        fallbacks: ["openrouter/google/gemini-2.0-flash-vision:free"],
      },
      imageGenerationModel: {
        primary: "openai/gpt-image-2",
        fallbacks: ["google/gemini-3.1-flash-image-preview"],
      },
      videoGenerationModel: {
        primary: "qwen/wan2.6-t2v",
        fallbacks: ["qwen/wan2.6-i2v"],
      },
      pdfModel: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5.4-mini"],
      },
      params: { cacheRetention: "long" }, // paramètres du fournisseur par défaut global
      embeddedHarness: {
        runtime: "auto", // auto | pi | id de harnais enregistré, par ex. codex
        fallback: "pi", // pi | none
      },
      pdfMaxBytesMb: 10,
      pdfMaxPages: 20,
      thinkingDefault: "low",
      verboseDefault: "off",
      elevatedDefault: "on",
      timeoutSeconds: 600,
      mediaMaxMb: 5,
      contextTokens: 200000,
      maxConcurrent: 3,
    },
  },
}
```

- `model` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - La forme chaîne définit uniquement le modèle principal.
  - La forme objet définit le modèle principal plus les modèles de basculement ordonnés.
- `imageModel` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - Utilisé par le chemin d'outil `image` comme sa configuration de modèle de vision.
  - Également utilisé comme routage de secours quand le modèle sélectionné/par défaut ne peut pas accepter d'entrée d'image.
- `imageGenerationModel` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - Utilisé par la capacité de génération d'image partagée et toute surface d'outil/plugin future qui génère des images.
  - Valeurs typiques : `google/gemini-3.1-flash-image-preview` pour la génération d'image Gemini native, `fal/fal-ai/flux/dev` pour fal, ou `openai/gpt-image-2` pour OpenAI Images.
  - Si vous sélectionnez un fournisseur/modèle directement, configurez également l'authentification du fournisseur correspondant (par exemple `GEMINI_API_KEY` ou `GOOGLE_API_KEY` pour `google/*`, `OPENAI_API_KEY` ou OpenAI Codex OAuth pour `openai/gpt-image-2`, `FAL_KEY` pour `fal/*`).
  - Si omis, `image_generate` peut toujours déduire une valeur par défaut du fournisseur soutenue par l'authentification. Il essaie d'abord le fournisseur par défaut actuel, puis les fournisseurs de génération d'image enregistrés restants dans l'ordre des id de fournisseur.
- `musicGenerationModel` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - Utilisé par la capacité de génération de musique partagée et l'outil `music_generate` intégré.
  - Valeurs typiques : `google/lyria-3-clip-preview`, `google/lyria-3-pro-preview`, ou `minimax/music-2.5+`.
  - Si omis, `music_generate` peut toujours déduire une valeur par défaut du fournisseur soutenue par l'authentification. Il essaie d'abord le fournisseur par défaut actuel, puis les fournisseurs de génération de musique enregistrés restants dans l'ordre des id de fournisseur.
  - Si vous sélectionnez un fournisseur/modèle directement, configurez également la clé d'authentification/API du fournisseur correspondant.
- `videoGenerationModel` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - Utilisé par la capacité de génération de vidéo partagée et l'outil `video_generate` intégré.
  - Valeurs typiques : `qwen/wan2.6-t2v`, `qwen/wan2.6-i2v`, `qwen/wan2.6-r2v`, `qwen/wan2.6-r2v-flash`, ou `qwen/wan2.7-r2v`.
  - Si omis, `video_generate` peut toujours déduire une valeur par défaut du fournisseur soutenue par l'authentification. Il essaie d'abord le fournisseur par défaut actuel, puis les fournisseurs de génération de vidéo enregistrés restants dans l'ordre des id de fournisseur.
  - Si vous sélectionnez un fournisseur/modèle directement, configurez également la clé d'authentification/API du fournisseur correspondant.
  - Le fournisseur de génération de vidéo Qwen fourni supporte jusqu'à 1 vidéo de sortie, 1 image d'entrée, 4 vidéos d'entrée, 10 secondes de durée, et les options `size`, `aspectRatio`, `resolution`, `audio`, et `watermark` au niveau du fournisseur.
- `pdfModel` : accepte soit une chaîne (`"provider/model"`) soit un objet (`{ primary, fallbacks }`).
  - Utilisé par l'outil `pdf` pour le routage du modèle.
  - Si omis, l'outil PDF revient à `imageModel`, puis au modèle de session/par défaut résolu.
- `pdfMaxBytesMb` : limite de taille PDF par défaut pour l'outil `pdf` quand `maxBytesMb` n'est pas passé au moment de l'appel.
- `pdfMaxPages` : nombre maximum de pages par défaut considérées par le mode de secours d'extraction dans l'outil `pdf`.
- `verboseDefault` : niveau de verbosité par défaut pour les agents. Valeurs : `"off"`, `"on"`, `"full"`. Par défaut : `"off"`.
- `elevatedDefault` : niveau de sortie élevée par défaut pour les agents. Valeurs : `"off"`, `"on"`, `"ask"`, `"full"`. Par défaut : `"on"`.
- `model.primary` : format `provider/model` (par ex. `openai/gpt-5.4` pour l'accès par clé API ou `openai-codex/gpt-5.5` pour Codex OAuth). Si vous omettez le fournisseur, OpenClaw essaie d'abord un alias, puis une correspondance de fournisseur configuré unique pour cet id de modèle exact, et seulement ensuite revient au fournisseur par défaut configuré (comportement de compatibilité déprécié, donc préférez `provider/model` explicite). Si ce fournisseur n'expose plus le modèle par défaut configuré, OpenClaw revient au premier `provider/model` configuré au lieu de surfacer une valeur par défaut de fournisseur supprimée obsolète.
- `models` : le catalogue de modèles configuré et la liste d'autorisation pour `/model`. Chaque entrée peut inclure `alias` (raccourci) et `params` (spécifique au fournisseur, par exemple `temperature`, `maxTokens`, `cacheRetention`, `context1m`, `responsesServerCompaction`, `responsesCompactThreshold`).
  - Éditions sûres : utilisez `openclaw config set agents.defaults.models '<json>' --strict-json --merge` pour ajouter des entrées. `config set` refuse les remplacements qui supprimeraient les entrées de liste d'autorisation existantes à moins que vous ne passiez `--replace`.
  - Les flux de configuration/intégration scoped au fournisseur fusionnent les modèles de fournisseur sélectionnés dans cette carte et préservent les fournisseurs non liés déjà configurés.
  - Pour les modèles OpenAI Responses directs, la compaction côté serveur est activée automatiquement. Utilisez `params.responsesServerCompaction: false` pour arrêter l'injection de `context_management`, ou `params.responsesCompactThreshold` pour remplacer le seuil. Voir [Compaction côté serveur OpenAI](/fr/providers/openai#server-side-compaction-responses-api).
- `params` : paramètres du fournisseur par défaut global appliqués à tous les modèles. Défini à `agents.defaults.params` (par ex. `{ cacheRetention: "long" }`).
- `params` fusion de précédence (config) : `agents.defaults.params` (base globale) est remplacée par `agents.defaults.models["provider/model"].params` (par modèle), puis `agents.list[].params` (id d'agent correspondant) remplace par clé. Voir [Mise en cache des invites](/fr/reference/prompt-caching) pour les détails.
- `embeddedHarness` : politique de runtime d'agent intégré de bas niveau par défaut. Utilisez `runtime: "auto"` pour laisser les harnais de plugin enregistrés réclamer les modèles supportés, `runtime: "pi"` pour forcer le harnais PI intégré, ou un id de harnais enregistré tel que `runtime: "codex"`. Définissez `fallback: "none"` pour désactiver le secours PI automatique.
- Les rédacteurs de config qui mutent ces champs (par exemple `/models set`, `/models set-image`, et les commandes d'ajout/suppression de secours) sauvegardent la forme d'objet canonique et préservent les listes de secours existantes quand c'est possible.
- `maxConcurrent` : exécutions d'agent parallèles maximales entre les sessions (chaque session toujours sérialisée). Par défaut : 4.

### `agents.defaults.embeddedHarness`

`embeddedHarness` contrôle quel exécuteur de bas niveau exécute les tours d'agent intégrés.
La plupart des déploiements doivent conserver la valeur par défaut `{ runtime: "auto", fallback: "pi" }`.
Utilisez-le quand un plugin de confiance fournit un harnais natif, comme le harnais d'app-server Codex fourni.

```json5
{
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
      embeddedHarness: {
        runtime: "codex",
        fallback: "none",
      },
    },
  },
}
```

- `runtime` : `"auto"`, `"pi"`, ou un id de harnais de plugin enregistré. Le plugin Codex fourni enregistre `codex`.
- `fallback` : `"pi"` ou `"none"`. `"pi"` garde le harnais PI intégré comme secours de compatibilité quand aucun harnais de plugin n'est sélectionné. `"none"` fait échouer la sélection de harnais de plugin manquant ou non supporté au lieu d'utiliser silencieusement PI. Les défaillances de harnais de plugin sélectionné surfacent toujours directement.
- Substitutions d'environnement : `OPENCLAW_AGENT_RUNTIME=<id|auto|pi>` remplace `runtime` ; `OPENCLAW_AGENT_HARNESS_FALLBACK=none` désactive le secours PI pour ce processus.
- Pour les déploiements Codex uniquement, définissez `model: "openai/gpt-5.5"`, `embeddedHarness.runtime: "codex"`, et `embeddedHarness.fallback: "none"`.
- Le choix du harnais est épinglé par id de session après la première exécution intégrée. Les modifications de config/env affectent les sessions nouvelles ou réinitialisées, pas une transcription existante. Les sessions héritées avec historique de transcription mais sans épingle enregistrée sont traitées comme épinglées à PI. `/status` affiche les ids de harnais non-PI tels que `codex` à côté de `Fast`.
- Cela contrôle uniquement le harnais de chat intégré. La génération de médias, la vision, le PDF, la musique, la vidéo et la TTS utilisent toujours leurs paramètres de fournisseur/modèle.

**Raccourcis d'alias intégrés** (s'appliquent uniquement quand le modèle est dans `agents.defaults.models`) :

| Alias               | Modèle                                             |
| ------------------- | -------------------------------------------------- |
| `opus`              | `anthropic/claude-opus-4-6`                        |
| `sonnet`            | `anthropic/claude-sonnet-4-6`                      |
| `gpt`               | `openai/gpt-5.4` ou GPT-5.5 Codex OAuth configuré |
| `gpt-mini`          | `openai/gpt-5.4-mini`                              |
| `gpt-nano`          | `openai/gpt-5.4-nano`                              |
| `gemini`            | `google/gemini-3.1-pro-preview`                    |
| `gemini-flash`      | `google/gemini-3-flash-preview`                    |
| `gemini-flash-lite` | `google/gemini-3.1-flash-lite-preview`             |

Vos alias configurés gagnent toujours sur les valeurs par défaut.

Les modèles Z.AI GLM-4.x activent automatiquement le mode de réflexion à moins que vous ne définissiez `--thinking off` ou `agents.defaults.models["zai/<model>"].params.thinking` vous-même.
Les modèles Z.AI activent `tool_stream` par défaut pour le streaming d'appels d'outil. Définissez `agents.defaults.models["zai/<model>"].params.tool_stream` à `false` pour le désactiver.
Les modèles Anthropic Claude 4.6 utilisent par défaut la réflexion `adaptive` quand aucun niveau de réflexion explicite n'est défini.

### `agents.defaults.cliBackends`

Backends CLI optionnels pour les exécutions de secours texte uniquement (pas d'appels d'outil). Utile comme sauvegarde quand les fournisseurs API échouent.

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "codex-cli": {
          command: "/opt/homebrew/bin/codex",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
        },
      },
    },
  },
}
```

- Les backends CLI sont texte-first ; les outils sont toujours désactivés.
- Sessions supportées quand `sessionArg` est défini.
- Passage d'image supporté quand `imageArg` accepte les chemins de fichier.

### `agents.defaults.systemPromptOverride`

Remplacez l'invite système assemblée par OpenClaw entière par une chaîne fixe. Défini au niveau par défaut (`agents.defaults.systemPromptOverride`) ou par agent (`agents.list[].systemPromptOverride`). Les valeurs par agent prennent précédence ; une valeur vide ou contenant uniquement des espaces est ignorée. Utile pour les expériences d'invite contrôlées.

```json5
{
  agents: {
    defaults: {
      systemPromptOverride: "You are a helpful assistant.",
    },
  },
}
```

### `agents.defaults.promptOverlays`

Superpositions d'invite indépendantes du fournisseur appliquées par famille de modèle. Les id de modèle de la famille GPT-5 reçoivent le contrat de comportement partagé entre les fournisseurs ; `personality` contrôle uniquement la couche de style d'interaction amical.

```json5
{
  agents: {
    defaults: {
      promptOverlays: {
        gpt5: {
          personality: "friendly", // friendly | on | off
        },
      },
    },
  },
}
```

- `"friendly"` (par défaut) et `"on"` activent la couche de style d'interaction amical.
- `"off"` désactive uniquement la couche amical ; le contrat de comportement GPT-5 étiqueté reste activé.
- L'héritage `plugins.entries.openai.config.personality` est toujours lu quand ce paramètre partagé n'est pas défini.

### `agents.defaults.heartbeat`

Exécutions de battement cardiaque périodiques.

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // 0m désactive
        model: "openai/gpt-5.4-mini",
        includeReasoning: false,
        includeSystemPromptSection: true, // par défaut : true ; false omet la section Heartbeat de l'invite système
        lightContext: false, // par défaut : false ; true garde uniquement HEARTBEAT.md des fichiers d'amorçage de l'espace de travail
        isolatedSession: false, // par défaut : false ; true exécute chaque battement cardiaque dans une session fraîche (pas d'historique de conversation)
        session: "main",
        to: "+15555550123",
        directPolicy: "allow", // allow (par défaut) | block
        target: "none", // par défaut : none | options : last | whatsapp | telegram | discord | ...
        prompt: "Read HEARTBEAT.md if it exists...",
        ackMaxChars: 300,
        suppressToolErrorWarnings: false,
        timeoutSeconds: 45,
      },
    },
  },
}
```

- `every` : chaîne de durée (ms/s/m/h). Par défaut : `30m` (authentification par clé API) ou `1h` (authentification OAuth). Définissez à `0m` pour désactiver.
- `includeSystemPromptSection` : quand false, omet la section Heartbeat de l'invite système et ignore l'injection `HEARTBEAT.md` dans le contexte d'amorçage. Par défaut : `true`.
- `suppressToolErrorWarnings` : quand true, supprime les charges utiles d'avertissement d'erreur d'outil pendant les exécutions de battement cardiaque.
- `timeoutSeconds` : temps maximum en secondes autorisé pour un tour d'agent de battement cardiaque avant qu'il ne soit interrompu. Laissez non défini pour utiliser `agents.defaults.timeoutSeconds`.
- `directPolicy` : politique de livraison directe/DM. `allow` (par défaut) permet la livraison à cible directe. `block` supprime la livraison à cible directe et émet `reason=dm-blocked`.
- `lightContext` : quand true, les exécutions de battement cardiaque utilisent un contexte d'amorçage léger et gardent uniquement `HEARTBEAT.md` des fichiers d'amorçage de l'espace de travail.
- `isolatedSession` : quand true, chaque battement cardiaque s'exécute dans une session fraîche sans historique de conversation antérieur. Même modèle d'isolation que cron `sessionTarget: "isolated"`. Réduit le coût de jetons par battement cardiaque d'environ 100K à 2-5K jetons.
- Par agent : définissez `agents.list[].heartbeat`. Quand un agent définit `heartbeat`, **seuls ces agents** exécutent les battements cardiaques.
- Les battements cardiaques exécutent des tours d'agent complets — les intervalles plus courts consomment plus de jetons.

### `agents.defaults.compaction`

```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard", // default | safeguard
        provider: "my-provider", // id d'un plugin fournisseur de compaction enregistré (optionnel)
        timeoutSeconds: 900,
        reserveTokensFloor: 24000,
        identifierPolicy: "strict", // strict | off | custom
        identifierInstructions: "Preserve deployment IDs, ticket IDs, and host:port pairs exactly.", // utilisé quand identifierPolicy=custom
        postCompactionSections: ["Session Startup", "Red Lines"], // [] désactive la réinjection
        model: "openrouter/anthropic/claude-sonnet-4-6", // substitution de modèle optionnelle pour compaction uniquement
        notifyUser: true, // envoyer de brefs avis quand la compaction commence et se termine (par défaut : false)
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 6000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with the exact silent token NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

- `mode` : `default` ou `safeguard` (résumé par chunking pour les longs historiques). Voir [Compaction](/fr/concepts/compaction).
- `provider` : id d'un plugin fournisseur de compaction enregistré. Quand défini, la `summarize()` du fournisseur est appelée au lieu de la résumé LLM intégrée. Revient à la résumé intégrée en cas d'échec. Définir un fournisseur force `mode: "safeguard"`. Voir [Compaction](/fr/concepts/compaction).
- `timeoutSeconds` : secondes maximales autorisées pour une seule opération de compaction avant qu'OpenClaw l'interrompe. Par défaut : `900`.
- `identifierPolicy` : `strict` (par défaut), `off`, ou `custom`. `strict` ajoute des conseils intégrés de rétention d'identifiant opaque au début pendant la résumé de compaction.
- `identifierInstructions` : texte optionnel de préservation d'identifiant personnalisé utilisé quand `identifierPolicy=custom`.
- `postCompactionSections` : noms de section H2/H3 AGENTS.md optionnels à réinjecter après compaction. Par défaut `["Session Startup", "Red Lines"]` ; définissez `[]` pour désactiver la réinjection. Quand non défini ou explicitement défini à cette paire par défaut, les anciens titres `Every Session`/`Safety` sont également acceptés comme secours hérité.
- `model` : substitution optionnelle `provider/model-id` pour la résumé de compaction uniquement. Utilisez ceci quand la session principale doit garder un modèle mais les résumés de compaction doivent s'exécuter sur un autre ; quand non défini, la compaction utilise le modèle principal de la session.
- `notifyUser` : quand `true`, envoie de brefs avis à l'utilisateur quand la compaction commence et quand elle se termine (par exemple, "Compacting context..." et "Compaction complete"). Désactivé par défaut pour garder la compaction silencieuse.
- `memoryFlush` : tour agentic silencieux avant la compaction automatique pour stocker les mémoires durables. Ignoré quand l'espace de travail est en lecture seule.

### `agents.defaults.contextPruning`

Élague les **anciens résultats d'outil** du contexte en mémoire avant d'envoyer au LLM. Ne modifie **pas** l'historique de session sur disque.

```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "cache-ttl", // off | cache-ttl
        ttl: "1h", // durée (ms/s/m/h), unité par défaut : minutes
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
        hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
        tools: { deny: ["browser", "canvas"] },
      },
    },
  },
}
```

<Accordion title="Comportement du mode cache-ttl">

- `mode: "cache-ttl"` active les passes d'élagage.
- `ttl` contrôle la fréquence à laquelle l'élagage peut s'exécuter à nouveau (après le dernier toucher du cache).
- L'élagage coupe d'abord les résultats d'outil surdimensionnés, puis efface les anciens résultats d'outil si nécessaire.

**Coupe douce** garde le début + la fin et insère `...` au milieu.

**Effacement dur** remplace le résultat d'outil entier par l'espace réservé.

Notes :

- Les blocs d'image ne sont jamais coupés/effacés.
- Les ratios sont basés sur les caractères (approximatifs), pas les comptes de jetons exacts.
- Si moins de `keepLastAssistants` messages d'assistant existent, l'élagage est ignoré.

</Accordion>

Voir [Élagage de session](/fr/concepts/session-pruning) pour les détails de comportement.

### Streaming de bloc

```json5
{
  agents: {
    defaults: {
      blockStreamingDefault: "off", // on | off
      blockStreamingBreak: "text_end", // text_end | message_end
      blockStreamingChunk: { minChars: 800, maxChars: 1200 },
      blockStreamingCoalesce: { idleMs: 1000 },
      humanDelay: { mode: "natural" }, // off | natural | custom (utilisez minMs/maxMs)
    },
  },
}
```

- Les canaux non-Telegram nécessitent `*.blockStreaming: true` explicite pour activer les réponses de bloc.
- Substitutions de canal : `channels.<channel>.blockStreamingCoalesce` (et variantes par compte). Signal/Slack/Discord/Google Chat utilisent par défaut `minChars: 1500`.
- `humanDelay` : pause aléatoire entre les réponses de bloc. `natural` = 800–2500ms. Substitution par agent : `agents.list[].humanDelay`.

Voir [Streaming](/fr/concepts/streaming) pour les détails de comportement + chunking.

### Indicateurs de saisie

```json5
{
  agents: {
    defaults: {
      typingMode: "instant", // never | instant | thinking | message
      typingIntervalSeconds: 6,
    },
  },
}
```

- Valeurs par défaut : `instant` pour les chats directs/mentions, `message` pour les chats de groupe non mentionnés.
- Substitutions par session : `session.typingMode`, `session.typingIntervalSeconds`.

Voir [Indicateurs de saisie](/fr/concepts/typing-indicators).

<a id="agentsdefaultssandbox"></a>

### `agents.defaults.sandbox`

Sandboxing optionnel pour l'agent intégré. Voir [Sandboxing](/fr/gateway/sandboxing) pour le guide complet.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        backend: "docker", // docker | ssh | openshell
        scope: "agent", // session | agent | shared
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          containerPrefix: "openclaw-sbx-",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          pidsLimit: 256,
          memory: "1g",
          memorySwap: "2g",
          cpus: 1,
          ulimits: {
            nofile: { soft: 1024, hard: 2048 },
            nproc: 256,
          },
          seccompProfile: "/path/to/seccomp.json",
          apparmorProfile: "openclaw-sandbox",
          dns: ["1.1.1.1", "8.8.8.8"],
          extraHosts: ["internal.service:10.0.0.5"],
          binds: ["/home/user/source:/source:rw"],
        },
        ssh: {
          target: "user@gateway-host:22",
          command: "ssh",
          workspaceRoot: "/tmp/openclaw-sandboxes",
          strictHostKeyChecking: true,
          updateHostKeys: true,
          identityFile: "~/.ssh/id_ed25519",
          certificateFile: "~/.ssh/id_ed25519-cert.pub",
          knownHostsFile: "~/.ssh/known_hosts",
          // SecretRefs / contenus en ligne également supportés :
          // identityData: { source: "env", provider: "default", id: "SSH_IDENTITY" },
          // certificateData: { source: "env", provider: "default", id: "SSH_CERTIFICATE" },
          // knownHostsData: { source: "env", provider: "default", id: "SSH_KNOWN_HOSTS" },
        },
        browser: {
          enabled: false,
          image: "openclaw-sandbox-browser:bookworm-slim",
          network: "openclaw-sandbox-browser",
          cdpPort: 9222,
          cdpSourceRange: "172.21.0.1/32",
          vncPort: 5900,
          noVncPort: 6080,
          headless: false,
          enableNoVnc: true,
          allowHostControl: false,
          autoStart: true,
          autoStartTimeoutMs: 12000,
        },
        prune: {
          idleHours: 24,
          maxAgeDays: 7,
        },
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: [
          "exec",
          "process",
          "read",
          "write",
          "edit",
          "apply_patch",
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "session_status",
        ],
        deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
      },
    },
  },
}
```

<Accordion title="Détails du sandbox">

**Backend :**

- `docker` : runtime Docker local (par défaut)
- `ssh` : runtime distant générique soutenu par SSH
- `openshell` : runtime OpenShell

Quand `backend: "openshell"` est sélectionné, les paramètres spécifiques au runtime se déplacent vers `plugins.entries.openshell.config`.

**Configuration du backend SSH :**

- `target` : cible SSH sous la forme `user@host[:port]`
- `command` : commande client SSH (par défaut : `ssh`)
- `workspaceRoot` : racine distante absolue utilisée pour les espaces de travail par scope
- `identityFile` / `certificateFile` / `knownHostsFile` : fichiers locaux existants passés à OpenSSH
- `identityData` / `certificateData` / `knownHostsData` : contenus en ligne ou SecretRefs qu'OpenClaw matérialise dans des fichiers temporaires au runtime
- `strictHostKeyChecking` / `updateHostKeys` : boutons de politique de clé d'hôte OpenSSH

**Précédence d'authentification SSH :**

- `identityData` gagne sur `identityFile`
- `certificateData` gagne sur `certificateFile`
- `knownHostsData` gagne sur `knownHostsFile`
- Les valeurs `*Data` soutenues par SecretRef sont résolues à partir de l'instantané du runtime de secrets actif avant le démarrage de la session de sandbox

**Comportement du backend SSH :**

- amorce l'espace de travail distant une fois après la création ou la recréation
- puis garde l'espace de travail SSH distant canonique
- achemine `exec`, les outils de fichier, et les chemins de médias sur SSH
- ne synchronise pas automatiquement les modifications distantes vers l'hôte
- ne supporte pas les conteneurs de navigateur sandbox

**Accès à l'espace de travail :**

- `none` : espace de travail sandbox par scope sous `~/.openclaw/sandboxes`
- `ro` : espace de travail sandbox à `/workspace`, espace de travail d'agent monté en lecture seule à `/agent`
- `rw` : espace de travail d'agent monté en lecture/écriture à `/workspace`

**Scope :**

- `session` : conteneur + espace de travail par session
- `agent` : un conteneur + espace de travail par agent (par défaut)
- `shared` : conteneur et espace de travail partagés (pas d'isolation entre sessions)

**Configuration du plugin OpenShell :**

```json5
{
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          mode: "mirror", // mirror | remote
          from: "openclaw",
          remoteWorkspaceDir: "/sandbox",
          remoteAgentWorkspaceDir: "/agent",
          gateway: "lab", // optionnel
          gatewayEndpoint: "https://lab.example", // optionnel
          policy: "strict", // id de politique OpenShell optionnel
          providers: ["openai"], // optionnel
          autoProviders: true,
          timeoutSeconds: 120,
        },
      },
    },
  },
}
```

**Mode OpenShell :**

- `mirror` : amorce distant à partir du local avant exec, synchronise en arrière après exec ; l'espace de travail local reste canonique
- `remote` : amorce distant une fois quand le sandbox est créé, puis garde l'espace de travail distant canonique

En mode `remote`, les éditions locales à l'hôte faites en dehors d'OpenClaw ne sont pas synchronisées dans le sandbox automatiquement après l'étape d'amorçage.
Le transport est SSH dans le sandbox OpenShell, mais le plugin possède le cycle de vie du sandbox et la synchronisation optionnelle de miroir.

**`setupCommand`** s'exécute une fois après la création du conteneur (via `sh -lc`). Nécessite l'accès réseau sortant, la racine inscriptible, l'utilisateur root.

**Les conteneurs utilisent par défaut `network: "none"`** — définissez à `"bridge"` (ou un réseau bridge personnalisé) si l'agent a besoin d'accès sortant.
`"host"` est bloqué. `"container:<id>"` est bloqué par défaut à moins que vous ne définissiez explicitement
`sandbox.docker.dangerouslyAllowContainerNamespaceJoin: true` (break-glass).

**Les pièces jointes entrantes** sont mises en scène dans `media/inbound/*` dans l'espace de travail actif.

**`docker.binds`** monte des répertoires d'hôte supplémentaires ; les liaisons globales et par agent sont fusionnées.

**Navigateur sandboxé** (`sandbox.browser.enabled`) : Chromium + CDP dans un conteneur. URL noVNC injectée dans l'invite système. Ne nécessite pas `browser.enabled` dans `openclaw.json`.
L'accès observateur noVNC utilise l'authentification VNC par défaut et OpenClaw émet une URL de jeton de courte durée (au lieu d'exposer le mot de passe dans l'URL partagée).

- `allowHostControl: false` (par défaut) bloque les sessions sandboxées de cibler le navigateur hôte.
- `network` utilise par défaut `openclaw-sandbox-browser` (réseau bridge dédié). Définissez à `bridge` uniquement quand vous voulez explicitement la connectivité bridge globale.
- `cdpSourceRange` restreint optionnellement l'entrée CDP au bord du conteneur à une plage CIDR (par exemple `172.21.0.1/32`).
- `sandbox.browser.binds` monte des répertoires d'hôte supplémentaires dans le conteneur de navigateur sandbox uniquement. Quand défini (y compris `[]`), il remplace `docker.binds` pour le conteneur de navigateur.
- Les valeurs par défaut de lancement sont définies dans `scripts/sandbox-browser-entrypoint.sh` et ajustées pour les hôtes de conteneur :
  - `--remote-debugging-address=127.0.0.1`
  - `--remote-debugging-port=<dérivé de OPENCLAW_BROWSER_CDP_PORT>`
  - `--user-data-dir=${HOME}/.chrome`
  - `--no-first-run`
  - `--no-default-browser-check`
  - `--disable-3d-apis`
  - `--disable-gpu`
  - `--disable-software-rasterizer`
  - `--disable-dev-shm-usage`
  - `--disable-background-networking`
  - `--disable-features=TranslateUI`
  - `--disable-breakpad`
  - `--disable-crash-reporter`
  - `--renderer-process-limit=2`
  - `--no-zygote`
  - `--metrics-recording-only`
  - `--disable-extensions` (activé par défaut)
  - `--disable-3d-apis`, `--disable-software-rasterizer`, et `--disable-gpu` sont
    activés par défaut et peuvent être désactivés avec
    `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` si l'utilisation de WebGL/3D le nécessite.
  - `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` réactive les extensions si votre flux de travail
    en dépend.
  - `--renderer-process-limit=2` peut être modifié avec
    `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>` ; définissez `0` pour utiliser la
    limite de processus par défaut de Chromium.
  - plus `--no-sandbox` et `--disable-setuid-sandbox` quand `noSandbox` est activé.
  - Les valeurs par défaut sont la ligne de base de l'image du conteneur ; utilisez une image de navigateur personnalisée avec un point d'entrée personnalisé pour modifier les valeurs par défaut du conteneur.

</Accordion>

Le sandboxing du navigateur et `sandbox.docker.binds` sont Docker uniquement.

Construire les images :

```bash
scripts/sandbox-setup.sh           # image sandbox principale
scripts/sandbox-browser-setup.sh   # image navigateur optionnelle
```

### `agents.list` (substitutions par agent)

```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        name: "Main Agent",
        workspace: "~/.openclaw/workspace",
        agentDir: "~/.openclaw/agents/main/agent",
        model: "anthropic/claude-opus-4-6", // ou { primary, fallbacks }
        thinkingDefault: "high", // substitution du niveau de réflexion par agent
        reasoningDefault: "on", // substitution de la visibilité du raisonnement par agent
        fastModeDefault: false, // substitution du mode rapide par agent
        embeddedHarness: { runtime: "auto", fallback: "pi" },
        params: { cacheRetention: "none" }, // remplace les paramètres defaults.models correspondants par clé
        skills: ["docs-search"], // remplace agents.defaults.skills quand défini
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
        groupChat: { mentionPatterns: ["@openclaw"] },
        sandbox: { mode: "off" },
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
        subagents: { allowAgents: ["*"] },
        tools: {
          profile: "coding",
          allow: ["browser"],
          deny: ["canvas"],
          elevated: { enabled: true },
        },
      },
    ],
  },
}
```

- `id` : id d'agent stable (requis).
- `default` : quand plusieurs sont définis, le premier gagne (avertissement enregistré). Si aucun défini, la première entrée de liste est par défaut.
- `model` : la forme chaîne remplace `primary` uniquement ; la forme objet `{ primary, fallbacks }` remplace les deux (`[]` désactive les secours globaux). Les travaux cron qui remplacent uniquement `primary` héritent toujours des secours par défaut à moins que vous ne définissiez `fallbacks: []`.
- `params` : paramètres de flux par agent fusionnés sur l'entrée de modèle sélectionnée dans `agents.defaults.models`. Utilisez ceci pour les substitutions spécifiques à l'agent comme `cacheRetention`, `temperature`, ou `maxTokens` sans dupliquer le catalogue de modèles entier.
- `skills` : liste de compétences optionnelle par agent. Si omis, l'agent hérite de `agents.defaults.skills` quand défini ; une liste explicite remplace les valeurs par défaut au lieu de fusionner, et `[]` signifie aucune compétence.
- `thinkingDefault` : niveau de réflexion par défaut optionnel par agent (`off | minimal | low | medium | high | xhigh | adaptive | max`). Remplace `agents.defaults.thinkingDefault` pour cet agent quand aucune substitution par message ou session n'est définie.
- `reasoningDefault` : visibilité du raisonnement par défaut optionnelle par agent (`on | off | stream`). S'applique quand aucune substitution de raisonnement par message ou session n'est définie.
- `fastModeDefault` : mode rapide par défaut optionnel par agent (`true | false`). S'applique quand aucune substitution de mode rapide par message ou session n'est définie.
- `embeddedHarness` : substitution optionnelle de politique de harnais de bas niveau par agent. Utilisez `{ runtime: "codex", fallback: "none" }` pour rendre un agent Codex uniquement tandis que d'autres agents gardent le secours PI par défaut.
- `runtime` : descripteur de runtime optionnel par agent. Utilisez `type: "acp"` avec les valeurs par défaut `runtime.acp` (`agent`, `backend`, `mode`, `cwd`) quand l'agent doit utiliser par défaut les sessions de harnais ACP.
- `identity.avatar` : chemin relatif à l'espace de travail, URL `http(s)`, ou URI `data:`.
- `identity` dérive les valeurs par défaut : `ackReaction` à partir de `emoji`, `mentionPatterns` à partir de `name`/`emoji`.
- `subagents.allowAgents` : liste d'autorisation des ids d'agent pour `sessions_spawn` (`["*"]` = n'importe lequel ; par défaut : même agent uniquement).
- Garde de protection d'héritage de sandbox : si la session du demandeur est sandboxée, `sessions_spawn` rejette les cibles qui s'exécuteraient sans sandbox.
- `subagents.requireAgentId` : quand true, bloquer les appels `sessions_spawn` qui omettent `agentId` (force la sélection de profil explicite ; par défaut : false).

## Routage multi-agent

Exécutez plusieurs agents isolés dans une seule Gateway. Voir [Multi-Agent](/fr/concepts/multi-agent).

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

### Champs de correspondance de liaison

- `type` (optionnel) : `route` pour le routage normal (le type manquant par défaut à route), `acp` pour les liaisons de conversation ACP persistantes.
- `match.channel` (requis)
- `match.accountId` (optionnel ; `*` = tout compte ; omis = compte par défaut)
- `match.peer` (optionnel ; `{ kind: direct|group|channel, id }`)
- `match.guildId` / `match.teamId` (optionnel ; spécifique au canal)
- `acp` (optionnel ; uniquement pour `type: "acp"`) : `{ mode, label, cwd, backend }`

**Ordre de correspondance déterministe :**

1. `match.peer`
2. `match.guildId`
3. `match.teamId`
4. `match.accountId` (exact, sans peer/guild/team)
5. `match.accountId: "*"` (à l'échelle du canal)
6. Agent par défaut

Dans chaque niveau, la première entrée `bindings` correspondante gagne.

Pour les entrées `type: "acp"`, OpenClaw résout par identité de conversation exacte (`match.channel` + compte + `match.peer.id`) et n'utilise pas l'ordre de niveau de liaison de route ci-dessus.

### Profils d'accès par agent

<Accordion title="Accès complet (pas de sandbox)">

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

</Accordion>

<Accordion title="Outils et espace de travail en lecture seule">

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
        tools: {
          allow: [
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}
```

</Accordion>

<Accordion title="Pas d'accès au système de fichiers (messagerie uniquement)">

```json5
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "none" },
        tools: {
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
            "gateway",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}
```

</Accordion>

Voir [Multi-Agent Sandbox & Tools](/fr/tools/multi-agent-sandbox-tools) pour les détails de précédence.

---

## Session

```json5
{
  session: {
    scope: "per-sender",
    dmScope: "main", // main | per-peer | per-channel-peer | per-account-channel-peer
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      mode: "daily", // daily | idle
      atHour: 4,
      idleMinutes: 60,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetTriggers: ["/new", "/reset"],
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    parentForkMaxTokens: 100000, // skip parent-thread fork above this token count (0 disables)
    maintenance: {
      mode: "warn", // warn | enforce
      pruneAfter: "30d",
      maxEntries: 500,
      rotateBytes: "10mb",
      resetArchiveRetention: "30d", // duration or false
      maxDiskBytes: "500mb", // optional hard budget
      highWaterBytes: "400mb", // optional cleanup target
    },
    threadBindings: {
      enabled: true,
      idleHours: 24, // default inactivity auto-unfocus in hours (`0` disables)
      maxAgeHours: 0, // default hard max age in hours (`0` disables)
    },
    mainKey: "main", // legacy (runtime always uses "main")
    agentToAgent: { maxPingPongTurns: 5 },
    sendPolicy: {
      rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }],
      default: "allow",
    },
  },
}
```

<Accordion title="Détails des champs de session">

- **`scope`** : stratégie de regroupement de session de base pour les contextes de chat de groupe.
  - `per-sender` (par défaut) : chaque expéditeur obtient une session isolée dans un contexte de canal.
  - `global` : tous les participants dans un contexte de canal partagent une seule session (à utiliser uniquement lorsqu'un contexte partagé est prévu).
- **`dmScope`** : comment les DM sont regroupés.
  - `main` : tous les DM partagent la session principale.
  - `per-peer` : isoler par ID d'expéditeur sur les canaux.
  - `per-channel-peer` : isoler par canal + expéditeur (recommandé pour les boîtes de réception multi-utilisateurs).
  - `per-account-channel-peer` : isoler par compte + canal + expéditeur (recommandé pour multi-compte).
- **`identityLinks`** : mapper les ID canoniques aux pairs préfixés par fournisseur pour le partage de session entre canaux.
- **`reset`** : politique de réinitialisation principale. `daily` réinitialise à `atHour` heure locale ; `idle` réinitialise après `idleMinutes`. Lorsque les deux sont configurés, celui qui expire en premier gagne.
- **`resetByType`** : remplacements par type (`direct`, `group`, `thread`). L'alias `dm` hérité accepté pour `direct`.
- **`parentForkMaxTokens`** : max `totalTokens` de session parent autorisé lors de la création d'une session de thread forké (par défaut `100000`).
  - Si `totalTokens` parent est au-dessus de cette valeur, OpenClaw démarre une nouvelle session de thread au lieu d'hériter de l'historique de transcription parent.
  - Définissez `0` pour désactiver cette protection et toujours autoriser le forking parent.
- **`mainKey`** : champ hérité. Le runtime utilise toujours `"main"` pour le bucket de chat direct principal.
- **`agentToAgent.maxPingPongTurns`** : nombre maximum de tours de réponse entre agents lors d'échanges agent-à-agent (entier, plage : `0`–`5`). `0` désactive le chaînage ping-pong.
- **`sendPolicy`** : correspondance par `channel`, `chatType` (`direct|group|channel`, avec alias hérité `dm`), `keyPrefix`, ou `rawKeyPrefix`. Le premier refus gagne.
- **`maintenance`** : nettoyage du magasin de session + contrôles de rétention.
  - `mode` : `warn` émet uniquement des avertissements ; `enforce` applique le nettoyage.
  - `pruneAfter` : seuil d'âge pour les entrées obsolètes (par défaut `30d`).
  - `maxEntries` : nombre maximum d'entrées dans `sessions.json` (par défaut `500`).
  - `rotateBytes` : faire pivoter `sessions.json` lorsqu'il dépasse cette taille (par défaut `10mb`).
  - `resetArchiveRetention` : rétention pour les archives de transcription `*.reset.<timestamp>`. Par défaut `pruneAfter` ; définissez `false` pour désactiver.
  - `maxDiskBytes` : budget disque optionnel du répertoire des sessions. En mode `warn`, il enregistre les avertissements ; en mode `enforce`, il supprime d'abord les artefacts/sessions les plus anciens.
  - `highWaterBytes` : cible optionnelle après nettoyage du budget. Par défaut `80%` de `maxDiskBytes`.
- **`threadBindings`** : valeurs par défaut globales pour les fonctionnalités de session liées aux threads.
  - `enabled` : commutateur par défaut maître (les fournisseurs peuvent remplacer ; Discord utilise `channels.discord.threadBindings.enabled`)
  - `idleHours` : inactivité par défaut auto-unfocus en heures (`0` désactive ; les fournisseurs peuvent remplacer)
  - `maxAgeHours` : âge maximum par défaut en heures (`0` désactive ; les fournisseurs peuvent remplacer)

</Accordion>

---

## Messages

```json5
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions", // group-mentions | group-all | direct | all
    removeAckAfterReply: false,
    queue: {
      mode: "collect", // steer | followup | collect | steer-backlog | steer+backlog | queue | interrupt
      debounceMs: 1000,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: {
        whatsapp: "collect",
        telegram: "collect",
      },
    },
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
      },
    },
  },
}
```

### Préfixe de réponse

Remplacements par canal/compte : `channels.<channel>.responsePrefix`, `channels.<channel>.accounts.<id>.responsePrefix`.

Résolution (le plus spécifique gagne) : compte → canal → global. `""` désactive et arrête la cascade. `"auto"` dérive `[{identity.name}]`.

**Variables de modèle :**

| Variable          | Description            | Exemple                     |
| ----------------- | ---------------------- | --------------------------- |
| `{model}`         | Nom court du modèle    | `claude-opus-4-6`           |
| `{modelFull}`     | Identifiant complet du modèle | `anthropic/claude-opus-4-6` |
| `{provider}`      | Nom du fournisseur     | `anthropic`                 |
| `{thinkingLevel}` | Niveau de réflexion actuel | `high`, `low`, `off`        |
| `{identity.name}` | Nom d'identité de l'agent | (identique à `"auto"`)      |

Les variables sont insensibles à la casse. `{think}` est un alias pour `{thinkingLevel}`.

### Réaction d'accusé de réception

- Par défaut, l'emoji `identity.emoji` de l'agent actif, sinon `"👀"`. Définissez `""` pour désactiver.
- Remplacements par canal : `channels.<channel>.ackReaction`, `channels.<channel>.accounts.<id>.ackReaction`.
- Ordre de résolution : compte → canal → `messages.ackReaction` → fallback d'identité.
- Portée : `group-mentions` (par défaut), `group-all`, `direct`, `all`.
- `removeAckAfterReply` : supprime l'accusé de réception après réponse sur Slack, Discord et Telegram.
- `messages.statusReactions.enabled` : active les réactions de statut du cycle de vie sur Slack, Discord et Telegram.
  Sur Slack et Discord, non défini maintient les réactions de statut activées lorsque les réactions d'accusé de réception sont actives.
  Sur Telegram, définissez-le explicitement sur `true` pour activer les réactions de statut du cycle de vie.

### Debounce entrant

Regroupe les messages texte rapides du même expéditeur en un seul tour d'agent. Les médias/pièces jointes se vident immédiatement. Les commandes de contrôle contournent le debouncing.

### TTS (synthèse vocale)

```json5
{
  messages: {
    tts: {
      auto: "always", // off | always | inbound | tagged
      mode: "final", // final | all
      provider: "elevenlabs",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: { enabled: true },
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
      openai: {
        apiKey: "openai_api_key",
        baseUrl: "https://api.openai.com/v1",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
    },
  },
}
```

- `auto` contrôle le mode TTS automatique par défaut : `off`, `always`, `inbound`, ou `tagged`. `/tts on|off` peut remplacer les préférences locales, et `/tts status` affiche l'état effectif.
- `summaryModel` remplace `agents.defaults.model.primary` pour le résumé automatique.
- `modelOverrides` est activé par défaut ; `modelOverrides.allowProvider` par défaut à `false` (opt-in).
- Les clés API reviennent à `ELEVENLABS_API_KEY`/`XI_API_KEY` et `OPENAI_API_KEY`.
- `openai.baseUrl` remplace le point de terminaison TTS OpenAI. L'ordre de résolution est config, puis `OPENAI_TTS_BASE_URL`, puis `https://api.openai.com/v1`.
- Lorsque `openai.baseUrl` pointe vers un point de terminaison non-OpenAI, OpenClaw le traite comme un serveur TTS compatible OpenAI et assouplit la validation du modèle/voix.

## Talk

Valeurs par défaut pour le mode Talk (macOS/iOS/Android).

```json5
{
  talk: {
    provider: "elevenlabs",
    providers: {
      elevenlabs: {
        voiceId: "elevenlabs_voice_id",
        voiceAliases: {
          Clawd: "EXAVITQu4vr4xnSDxMaL",
          Roger: "CwhRBWXzGAHq8TQ4Fs17",
        },
        modelId: "eleven_v3",
        outputFormat: "mp3_44100_128",
        apiKey: "elevenlabs_api_key",
      },
    },
    silenceTimeoutMs: 1500,
    interruptOnSpeech: true,
  },
}
```

- `talk.provider` doit correspondre à une clé dans `talk.providers` lorsque plusieurs fournisseurs Talk sont configurés.
- Les clés Talk héritées et plates (`talk.voiceId`, `talk.voiceAliases`, `talk.modelId`, `talk.outputFormat`, `talk.apiKey`) sont réservées à la compatibilité et sont automatiquement migrées vers `talk.providers.<provider>`.
- Les ID de voix se rabattent sur `ELEVENLABS_VOICE_ID` ou `SAG_VOICE_ID`.
- `providers.*.apiKey` accepte les chaînes en texte brut ou les objets SecretRef.
- Le repli `ELEVENLABS_API_KEY` s'applique uniquement lorsqu'aucune clé API Talk n'est configurée.
- `providers.*.voiceAliases` permet aux directives Talk d'utiliser des noms conviviaux.
- `silenceTimeoutMs` contrôle la durée pendant laquelle le mode Talk attend après le silence de l'utilisateur avant d'envoyer la transcription. Non défini conserve la fenêtre de pause par défaut de la plateforme (`700 ms sur macOS et Android, 900 ms sur iOS`).

---

## Connexes

- [Référence de configuration](/fr/gateway/configuration-reference) — toutes les autres clés de configuration
- [Configuration](/fr/gateway/configuration) — tâches courantes et configuration rapide
- [Exemples de configuration](/fr/gateway/configuration-examples)
