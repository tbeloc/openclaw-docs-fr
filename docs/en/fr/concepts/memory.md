---
title: "Mémoire"
summary: "Comment fonctionne la mémoire OpenClaw (fichiers d'espace de travail + vidage automatique de la mémoire)"
read_when:
  - You want the memory file layout and workflow
  - You want to tune the automatic pre-compaction memory flush
---

# Mémoire

La mémoire OpenClaw est du **Markdown simple dans l'espace de travail de l'agent**. Les fichiers sont la
source de vérité ; le modèle ne « se souvient » que de ce qui est écrit sur le disque.

Les outils de recherche de mémoire sont fournis par le plugin de mémoire actif (par défaut :
`memory-core`). Désactivez les plugins de mémoire avec `plugins.slots.memory = "none"`.

## Fichiers de mémoire (Markdown)

La disposition d'espace de travail par défaut utilise deux couches de mémoire :

- `memory/YYYY-MM-DD.md`
  - Journal quotidien (ajout uniquement).
  - Lire aujourd'hui + hier au démarrage de la session.
- `MEMORY.md` (optionnel)
  - Mémoire à long terme organisée.
  - Si `MEMORY.md` et `memory.md` existent tous les deux à la racine de l'espace de travail, OpenClaw ne charge que `MEMORY.md`.
  - Le fichier minuscule `memory.md` n'est utilisé que comme solution de secours quand `MEMORY.md` est absent.
  - **Charger uniquement dans la session principale et privée** (jamais dans les contextes de groupe).

Ces fichiers se trouvent sous l'espace de travail (`agents.defaults.workspace`, par défaut
`~/.openclaw/workspace`). Voir [Agent workspace](/fr/concepts/agent-workspace) pour la disposition complète.

## Outils de mémoire

OpenClaw expose deux outils orientés agent pour ces fichiers Markdown :

- `memory_search` — rappel sémantique sur des extraits indexés.
- `memory_get` — lecture ciblée d'un fichier Markdown spécifique ou d'une plage de lignes.

`memory_get` **se dégrade maintenant gracieusement quand un fichier n'existe pas** (par exemple,
le journal quotidien d'aujourd'hui avant la première écriture). Le gestionnaire intégré et le
backend QMD retournent tous les deux `{ text: "", path }` au lieu de lever `ENOENT`, afin que les agents puissent
gérer « rien d'enregistré pour le moment » et continuer leur flux de travail sans envelopper l'appel
d'outil dans une logique try/catch.

## Quand écrire la mémoire

- Les décisions, préférences et faits durables vont dans `MEMORY.md`.
- Les notes quotidiennes et le contexte en cours vont dans `memory/YYYY-MM-DD.md`.
- Si quelqu'un dit « souviens-toi de ceci », écris-le (ne le garde pas en RAM).
- Ce domaine est encore en évolution. Il est utile de rappeler au modèle de stocker les mémoires ; il saura quoi faire.
- Si vous voulez que quelque chose persiste, **demandez au bot de l'écrire** dans la mémoire.

## Vidage automatique de la mémoire (ping de pré-compaction)

Quand une session est **proche de la compaction automatique**, OpenClaw déclenche un **tour
agentic silencieux** qui rappelle au modèle d'écrire la mémoire durable **avant** que le
contexte ne soit compacté. Les invites par défaut disent explicitement que le modèle _peut répondre_,
mais généralement `NO_REPLY` est la réponse correcte afin que l'utilisateur ne voie jamais ce tour.

Ceci est contrôlé par `agents.defaults.compaction.memoryFlush` :

```json5
{
  agents: {
    defaults: {
      compaction: {
        reserveTokensFloor: 20000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

Détails :

- **Seuil souple** : le vidage se déclenche quand l'estimation du jeton de session franchit
  `contextWindow - reserveTokensFloor - softThresholdTokens`.
- **Silencieux** par défaut : les invites incluent `NO_REPLY` afin que rien ne soit livré.
- **Deux invites** : une invite utilisateur plus une invite système ajoutent le rappel.
- **Un vidage par cycle de compaction** (suivi dans `sessions.json`).
- **L'espace de travail doit être accessible en écriture** : si la session s'exécute en bac à sable avec
  `workspaceAccess: "ro"` ou `"none"`, le vidage est ignoré.

Pour le cycle de vie complet de la compaction, voir
[Session management + compaction](/fr/reference/session-management-compaction).

## Recherche vectorielle en mémoire

OpenClaw peut construire un petit index vectoriel sur `MEMORY.md` et `memory/*.md` pour que les requêtes sémantiques trouvent des notes connexes même quand la formulation diffère.

Valeurs par défaut :

- Activé par défaut.
- Surveille les fichiers de mémoire pour détecter les modifications (avec débounce).
- Configurez la recherche en mémoire sous `agents.defaults.memorySearch` (pas au niveau supérieur `memorySearch`).
- Utilise les embeddings distants par défaut. Si `memorySearch.provider` n'est pas défini, OpenClaw sélectionne automatiquement :
  1. `local` si un `memorySearch.local.modelPath` est configuré et le fichier existe.
  2. `openai` si une clé OpenAI peut être résolue.
  3. `gemini` si une clé Gemini peut être résolue.
  4. `voyage` si une clé Voyage peut être résolue.
  5. `mistral` si une clé Mistral peut être résolue.
  6. Sinon, la recherche en mémoire reste désactivée jusqu'à configuration.
- Le mode local utilise node-llama-cpp et peut nécessiter `pnpm approve-builds`.
- Utilise sqlite-vec (quand disponible) pour accélérer la recherche vectorielle dans SQLite.
- `memorySearch.provider = "ollama"` est également supporté pour les embeddings Ollama locaux/auto-hébergés (`/api/embeddings`), mais n'est pas sélectionné automatiquement.

Les embeddings distants **nécessitent** une clé API pour le fournisseur d'embeddings. OpenClaw résout les clés à partir des profils d'authentification, `models.providers.*.apiKey`, ou des variables d'environnement. Codex OAuth couvre uniquement chat/completions et ne satisfait **pas** les embeddings pour la recherche en mémoire. Pour Gemini, utilisez `GEMINI_API_KEY` ou `models.providers.google.apiKey`. Pour Voyage, utilisez `VOYAGE_API_KEY` ou `models.providers.voyage.apiKey`. Pour Mistral, utilisez `MISTRAL_API_KEY` ou `models.providers.mistral.apiKey`. Ollama ne nécessite généralement pas de vraie clé API (un placeholder comme `OLLAMA_API_KEY=ollama-local` suffit si nécessaire par la politique locale).
Lors de l'utilisation d'un endpoint compatible OpenAI personnalisé, définissez `memorySearch.remote.apiKey` (et optionnellement `memorySearch.remote.headers`).

### Backend QMD (expérimental)

Définissez `memory.backend = "qmd"` pour remplacer l'indexeur SQLite intégré par [QMD](https://github.com/tobi/qmd) : un sidecar de recherche local-first qui combine BM25 + vecteurs + reclassement. Markdown reste la source de vérité ; OpenClaw appelle QMD pour la récupération. Points clés :

**Prérequis**

- Désactivé par défaut. Opt-in par configuration (`memory.backend = "qmd"`).
- Installez le CLI QMD séparément (`bun install -g https://github.com/tobi/qmd` ou téléchargez une version) et assurez-vous que le binaire `qmd` est sur le `PATH` de la passerelle.
- QMD a besoin d'une build SQLite qui permet les extensions (`brew install sqlite` sur macOS).
- QMD s'exécute entièrement localement via Bun + `node-llama-cpp` et télécharge automatiquement les modèles GGUF depuis HuggingFace à la première utilisation (aucun daemon Ollama séparé requis).
- La passerelle exécute QMD dans un home XDG auto-contenu sous `~/.openclaw/agents/<agentId>/qmd/` en définissant `XDG_CONFIG_HOME` et `XDG_CACHE_HOME`.
- Support OS : macOS et Linux fonctionnent directement une fois Bun + SQLite installés. Windows est mieux supporté via WSL2.

**Comment le sidecar s'exécute**

- La passerelle écrit un home QMD auto-contenu sous `~/.openclaw/agents/<agentId>/qmd/` (config + cache + DB sqlite).
- Les collections sont créées via `qmd collection add` à partir de `memory.qmd.paths` (plus les fichiers de mémoire workspace par défaut), puis `qmd update` + `qmd embed` s'exécutent au démarrage et à un intervalle configurable (`memory.qmd.update.interval`, par défaut 5 m).
- La passerelle initialise maintenant le gestionnaire QMD au démarrage, donc les minuteurs de mise à jour périodique sont armés même avant le premier appel `memory_search`.
- L'actualisation au démarrage s'exécute maintenant en arrière-plan par défaut pour que le démarrage du chat ne soit pas bloqué ; définissez `memory.qmd.update.waitForBootSync = true` pour conserver le comportement bloquant précédent.
- Les recherches s'exécutent via `memory.qmd.searchMode` (par défaut `qmd search --json` ; supporte aussi `vsearch` et `query`). Si le mode sélectionné rejette les flags sur votre build QMD, OpenClaw réessaie avec `qmd query`. Si QMD échoue ou le binaire est manquant, OpenClaw bascule automatiquement vers le gestionnaire SQLite intégré pour que les outils de mémoire continuent de fonctionner.
- OpenClaw n'expose pas le tuning de la taille de batch d'embedding QMD aujourd'hui ; le comportement de batch est contrôlé par QMD lui-même.
- **La première recherche peut être lente** : QMD peut télécharger les modèles GGUF locaux (reclasseur/expansion de requête) à la première exécution `qmd query`.
  - OpenClaw définit `XDG_CONFIG_HOME`/`XDG_CACHE_HOME` automatiquement quand il exécute QMD.
  - Si vous voulez pré-télécharger les modèles manuellement (et réchauffer le même index qu'OpenClaw utilise), exécutez une requête unique avec les répertoires XDG de l'agent.

    L'état QMD d'OpenClaw vit sous votre **répertoire d'état** (par défaut `~/.openclaw`).
    Vous pouvez pointer `qmd` vers le même index en exportant les mêmes variables XDG qu'OpenClaw utilise :

    ```bash
    # Choisissez le même répertoire d'état qu'OpenClaw utilise
    STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"

    export XDG_CONFIG_HOME="$STATE_DIR/agents/main/qmd/xdg-config"
    export XDG_CACHE_HOME="$STATE_DIR/agents/main/qmd/xdg-cache"

    # (Optionnel) forcer une actualisation d'index + embeddings
    qmd update
    qmd embed

    # Réchauffer / déclencher les téléchargements de modèles pour la première fois
    qmd query "test" -c memory-root --json >/dev/null 2>&1
    ```

**Surface de configuration (`memory.qmd.*`)**

- `command` (par défaut `qmd`) : remplacez le chemin de l'exécutable.
- `searchMode` (par défaut `search`) : choisissez quelle commande QMD soutient `memory_search` (`search`, `vsearch`, `query`).
- `includeDefaultMemory` (par défaut `true`) : indexez automatiquement `MEMORY.md` + `memory/**/*.md`.
- `paths[]` : ajoutez des répertoires/fichiers supplémentaires (`path`, `pattern` optionnel, `name` stable optionnel).
- `sessions` : opt-in pour l'indexation JSONL de session (`enabled`, `retentionDays`, `exportDir`).
- `update` : contrôle la cadence d'actualisation et l'exécution de la maintenance :
  (`interval`, `debounceMs`, `onBoot`, `waitForBootSync`, `embedInterval`,
  `commandTimeoutMs`, `updateTimeoutMs`, `embedTimeoutMs`).
- `limits` : limitez la charge utile de rappel (`maxResults`, `maxSnippetChars`, `maxInjectedChars`, `timeoutMs`).
- `scope` : même schéma que [`session.sendPolicy`](/fr/gateway/configuration#session).
  Par défaut DM uniquement (`deny` tous, `allow` chats directs) ; assouplissez-le pour afficher les résultats QMD dans les groupes/canaux.
  - `match.keyPrefix` correspond à la clé de session **normalisée** (minuscules, avec tout `agent:<id>:` initial supprimé). Exemple : `discord:channel:`.
  - `match.rawKeyPrefix` correspond à la clé de session **brute** (minuscules), y compris `agent:<id>:`. Exemple : `agent:main:discord:`.
  - Héritage : `match.keyPrefix: "agent:..."` est toujours traité comme un préfixe de clé brute, mais préférez `rawKeyPrefix` pour la clarté.
- Quand `scope` refuse une recherche, OpenClaw enregistre un avertissement avec le `channel`/`chatType` dérivé pour que les résultats vides soient plus faciles à déboguer.
- Les snippets provenant en dehors de l'espace de travail apparaissent comme `qmd/<collection>/<relative-path>` dans les résultats `memory_search` ; `memory_get` comprend ce préfixe et lit à partir de la racine de collection QMD configurée.
- Quand `memory.qmd.sessions.enabled = true`, OpenClaw exporte les transcriptions de session assainies (tours Utilisateur/Assistant) dans une collection QMD dédiée sous `~/.openclaw/agents/<id>/qmd/sessions/`, pour que `memory_search` puisse rappeler les conversations récentes sans toucher à l'index SQLite intégré.
- Les snippets `memory_search` incluent maintenant un pied de page `Source: <path#line>` quand `memory.citations` est `auto`/`on` ; définissez `memory.citations = "off"` pour garder les métadonnées de chemin internes (l'agent reçoit toujours le chemin pour `memory_get`, mais le texte du snippet omet le pied de page et le prompt système avertit l'agent de ne pas le citer).

**Exemple**

```json5
memory: {
  backend: "qmd",
  citations: "auto",
  qmd: {
    includeDefaultMemory: true,
    update: { interval: "5m", debounceMs: 15000 },
    limits: { maxResults: 6, timeoutMs: 4000 },
    scope: {
      default: "deny",
      rules: [
        { action: "allow", match: { chatType: "direct" } },
        // Préfixe de clé de session normalisé (supprime `agent:<id>:`).
        { action: "deny", match: { keyPrefix: "discord:channel:" } },
        // Préfixe de clé de session brut (inclut `agent:<id>:`).
        { action: "deny", match: { rawKeyPrefix: "agent:main:discord:" } },
      ]
    },
    paths: [
      { name: "docs", path: "~/notes", pattern: "**/*.md" }
    ]
  }
}
```

**Citations & fallback**

- `memory.citations` s'applique quel que soit le backend (`auto`/`on`/`off`).
- Quand `qmd` s'exécute, nous marquons `status().backend = "qmd"` pour que les diagnostics montrent quel moteur a servi les résultats. Si le sous-processus QMD se termine ou la sortie JSON ne peut pas être analysée, le gestionnaire de recherche enregistre un avertissement et retourne le fournisseur intégré (embeddings Markdown existants) jusqu'à ce que QMD se rétablisse.

### Chemins de mémoire supplémentaires

Si vous voulez indexer des fichiers Markdown en dehors de la disposition d'espace de travail par défaut, ajoutez des chemins explicites :

```json5
agents: {
  defaults: {
    memorySearch: {
      extraPaths: ["../team-docs", "/srv/shared-notes/overview.md"]
    }
  }
}
```

Notes :

- Les chemins peuvent être absolus ou relatifs à l'espace de travail.
- Les répertoires sont analysés récursivement pour les fichiers `.md`.
- Par défaut, seuls les fichiers Markdown sont indexés.
- Si `memorySearch.multimodal.enabled = true`, OpenClaw indexe également les fichiers image/audio supportés sous `extraPaths` uniquement. Les racines de mémoire par défaut (`MEMORY.md`, `memory.md`, `memory/**/*.md`) restent Markdown uniquement.
- Les liens symboliques sont ignorés (fichiers ou répertoires).

### Fichiers de mémoire multimodaux (image + audio Gemini)

OpenClaw peut indexer les fichiers image et audio à partir de `memorySearch.extraPaths` lors de l'utilisation de Gemini embedding 2 :

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "gemini",
      model: "gemini-embedding-2-preview",
      extraPaths: ["assets/reference", "voice-notes"],
      multimodal: {
        enabled: true,
        modalities: ["image", "audio"], // ou ["all"]
        maxFileBytes: 10000000
      },
      remote: {
        apiKey: "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

Notes :

- La mémoire multimodale est actuellement supportée uniquement pour `gemini-embedding-2-preview`.
- L'indexation multimodale s'applique uniquement aux fichiers découverts via `memorySearch.extraPaths`.
- Modalités supportées dans cette phase : image et audio.
- `memorySearch.fallback` doit rester `"none"` tandis que la mémoire multimodale est activée.
- Les octets de fichier image/audio correspondants sont téléchargés vers le endpoint d'embedding Gemini configuré lors de l'indexation.
- Extensions d'image supportées : `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.heic`, `.heif`.
- Extensions audio supportées : `.mp3`, `.wav`, `.ogg`, `.opus`, `.m4a`, `.aac`, `.flac`.
- Les requêtes de recherche restent du texte, mais Gemini peut comparer ces requêtes textuelles contre les embeddings image/audio indexés.
- `memory_get` lit toujours Markdown uniquement ; les fichiers binaires sont consultables mais ne sont pas retournés comme contenu de fichier brut.

### Embeddings Gemini (natif)

Définissez le fournisseur sur `gemini` pour utiliser directement l'API d'embeddings Gemini :

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "gemini",
      model: "gemini-embedding-001",
      remote: {
        apiKey: "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

Notes :

- `remote.baseUrl` est optionnel (par défaut l'URL de base de l'API Gemini).
- `remote.headers` vous permet d'ajouter des en-têtes supplémentaires si nécessaire.
- Modèle par défaut : `gemini-embedding-001`.
- `gemini-embedding-2-preview` est également supporté : limite de 8192 tokens et dimensions configurables (768 / 1536 / 3072, par défaut 3072).

#### Gemini Embedding 2 (aperçu)

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "gemini",
      model: "gemini-embedding-2-preview",
      outputDimensionality: 3072,  // optionnel : 768, 1536, ou 3072 (par défaut)
      remote: {
        apiKey: "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

> **⚠️ Réindexation requise :** Passer de `gemini-embedding-001` (768 dimensions)
> à `gemini-embedding-2-preview` (3072 dimensions) change la taille du vecteur. Il en va de même si vous
> changez `outputDimensionality` entre 768, 1536 et 3072.
> OpenClaw réindexera automatiquement quand il détecte un changement de modèle ou de dimension.

Si vous voulez utiliser un **endpoint compatible OpenAI personnalisé** (OpenRouter, vLLM, ou un proxy),
vous pouvez utiliser la configuration `remote` avec le fournisseur OpenAI :

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      remote: {
        baseUrl: "https://api.example.com/v1/",
        apiKey: "YOUR_OPENAI_COMPAT_API_KEY",
        headers: { "X-Custom-Header": "value" }
      }
    }
  }
}
```

Si vous ne voulez pas définir une clé API, utilisez `memorySearch.provider = "local"` ou définissez `memorySearch.fallback = "none"`.

Fallbacks :

- `memorySearch.fallback` peut être `openai`, `gemini`, `voyage`, `mistral`, `ollama`, `local`, ou `none`.
- Le fournisseur de fallback n'est utilisé que quand le fournisseur d'embedding principal échoue.

Indexation par batch (OpenAI + Gemini + Voyage) :

- Désactivée par défaut. Définissez `agents.defaults.memorySearch.remote.batch.enabled = true` pour activer l'indexation de corpus volumineux (OpenAI, Gemini et Voyage).
- Le comportement par défaut attend la fin du batch ; ajustez `remote.batch.wait`, `remote.batch.pollIntervalMs` et `remote.batch.timeoutMinutes` si nécessaire.
- Définissez `remote.batch.concurrency` pour contrôler combien de jobs batch nous soumettons en parallèle (par défaut : 2).
- Le mode batch s'applique quand `memorySearch.provider = "openai"` ou `"gemini"` et utilise la clé API correspondante.
- Les jobs batch Gemini utilisent le endpoint d'embeddings batch asynchrone et nécessitent la disponibilité de l'API Batch Gemini.

Pourquoi OpenAI batch est rapide + bon marché :

- Pour les grands remplissages, OpenAI est généralement l'option la plus rapide que nous supportons car nous pouvons soumettre de nombreuses requêtes d'embedding dans un seul job batch et laisser OpenAI les traiter de manière asynchrone.
- OpenAI offre une tarification réduite pour les charges de travail de l'API Batch, donc les grandes exécutions d'indexation sont généralement moins chères que l'envoi des mêmes requêtes de manière synchrone.
- Consultez les docs et la tarification de l'API Batch OpenAI pour plus de détails :
  - [https://platform.openai.com/docs/api-reference/batch](https://platform.openai.com/docs/api-reference/batch)
  - [https://platform.openai.com/pricing](https://platform.openai.com/pricing)

Exemple de configuration :

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      fallback: "openai",
      remote: {
        batch: { enabled: true, concurrency: 2 }
      },
      sync: { watch: true }
    }
  }
}
```

Outils :

- `memory_search` — retourne des snippets avec fichier + plages de lignes.
- `memory_get` — lire le contenu du fichier de mémoire par chemin.

Mode local :

- Définissez `agents.defaults.memorySearch.provider = "local"`.
- Fournissez `agents.defaults.memorySearch.local.modelPath` (GGUF ou URI `hf:`).
- Optionnel : définissez `agents.defaults.memorySearch.fallback = "none"` pour éviter le fallback distant.

### Comment fonctionnent les outils de mémoire

- `memory_search` recherche sémantiquement des chunks Markdown (~400 tokens cible, 80 tokens de chevauchement) à partir de `MEMORY.md` + `memory/**/*.md`. Il retourne le texte du snippet (limité ~700 caractères), le chemin du fichier, la plage de lignes, le score, le fournisseur/modèle, et si nous avons basculé de embeddings locaux → distants. Aucune charge utile de fichier complet n'est retournée.
- `memory_get` lit un fichier Markdown de mémoire spécifique (relatif à l'espace de travail), optionnellement à partir d'une ligne de départ et pour N lignes. Les chemins en dehors de `MEMORY.md` / `memory/` sont rejetés.
- Les deux outils ne sont activés que quand `memorySearch.enabled` se résout à true pour l'agent.

### Ce qui est indexé (et quand)

- Type de fichier : Markdown uniquement (`MEMORY.md`, `memory/**/*.md`).
- Stockage d'index : SQLite par agent à `~/.openclaw/memory/<agentId>.sqlite` (configurable via `agents.defaults.memorySearch.store.path`, supporte le token `{agentId}`).
- Fraîcheur : observateur sur `MEMORY.md` + `memory/` marque l'index comme sale (débounce 1.5s). La synchronisation est programmée au démarrage de la session, à la recherche, ou à un intervalle et s'exécute de manière asynchrone. Les transcriptions de session utilisent des seuils delta pour déclencher la synchronisation en arrière-plan.
- Déclencheurs de réindexation : l'index stocke le **fournisseur/modèle d'embedding + empreinte digitale d'endpoint + paramètres de chunking**. Si l'un de ceux-ci change, OpenClaw réinitialise et réindexe automatiquement l'ensemble du magasin.

### Recherche hybride (BM25 + vecteur)

Quand activée, OpenClaw combine :

- **Similarité vectorielle** (correspondance sémantique, la formulation peut différer)
- **Pertinence de mot-clé BM25** (tokens exacts comme les IDs, variables d'env, symboles de code)

Si la recherche en texte intégral n'est pas disponible sur votre plateforme, OpenClaw bascule vers la recherche vectorielle uniquement.

#### Pourquoi hybride ?

La recherche vectorielle est excellente pour "cela signifie la même chose" :

- "Mac Studio gateway host" vs "la machine exécutant la passerelle"
- "debounce file updates" vs "éviter l'indexation à chaque écriture"

Mais elle peut être faible sur les tokens exacts et à haut signal :

- IDs (`a828e60`, `b3b9895a…`)
- symboles de code (`memorySearch.query.hybrid`)
- chaînes d'erreur ("sqlite-vec unavailable")

BM25 (texte intégral) est l'opposé : fort sur les tokens exacts, plus faible sur les paraphrases.
La recherche hybride est le juste milieu pragmatique : **utilisez les deux signaux de récupération** pour obtenir de bons résultats pour les requêtes "langage naturel" et "chercher une aiguille dans une botte de foin".

#### Comment nous fusionnons les résultats (la conception actuelle)

Esquisse d'implémentation :

1. Récupérez un pool de candidats des deux côtés :

- **Vecteur** : top `maxResults * candidateMultiplier` par similarité cosinus.
- **BM25** : top `maxResults * candidateMultiplier` par rang FTS5 BM25 (plus bas est mieux).

2. Convertissez le rang BM25 en score 0..1-ish :

- `textScore = 1 / (1 + max(0, bm25Rank))`

3. Unissez les candidats par ID de chunk et calculez un score pondéré :

- `finalScore = vectorWeight * vectorScore + textWeight * textScore`

Notes :

- `vectorWeight` + `textWeight` est normalisé à 1.0 dans la résolution de configuration, donc les poids se comportent comme des pourcentages.
- Si les embeddings ne sont pas disponibles (ou le fournisseur retourne un vecteur zéro), nous exécutons toujours BM25 et retournons les correspondances de mots-clés.
- Si FTS5 ne peut pas être créé, nous gardons la recherche vectorielle uniquement (pas d'échec dur).

Ce n'est pas "parfait en théorie RI", mais c'est simple, rapide, et tend à améliorer le rappel/la précision sur les vraies notes.
Si nous voulons devenir plus sophistiqués plus tard, les prochaines étapes courantes sont Reciprocal Rank Fusion (RRF) ou la normalisation des scores (min/max ou z-score) avant de mélanger.

#### Pipeline de post-traitement

Après fusion des scores vectoriels et de mots-clés, deux étapes de post-traitement optionnelles affinent la liste de résultats avant qu'elle n'atteigne l'agent :

```
Vecteur + Mot-clé → Fusion pondérée → Décroissance temporelle → Tri → MMR → Résultats Top-K
```

Les deux étapes sont **désactivées par défaut** et peuvent être activées indépendamment.

#### Reclassement MMR (diversité)

Quand la recherche hybride retourne des résultats, plusieurs chunks peuvent contenir du contenu similaire ou chevauchant.
Par exemple, chercher "home network setup" pourrait retourner cinq snippets presque identiques de différentes notes quotidiennes qui mentionnent tous la même configuration de routeur.

**MMR (Maximal Marginal Relevance)** reclasse les résultats pour équilibrer la pertinence avec la diversité,
en s'assurant que les meilleurs résultats couvrent différents aspects de la requête au lieu de répéter les mêmes informations.

Comment ça fonctionne :

1. Les résultats sont notés par leur pertinence originale (score pondéré vecteur + BM25).
2. MMR sélectionne itérativement les résultats qui maximisent : `λ × pertinence − (1−λ) × max_similarité_aux_sélectionnés`.
3. La similarité entre les résultats est mesurée en utilisant la similarité Jaccard sur le contenu tokenisé.

Le paramètre `lambda` contrôle le compromis :

- `lambda = 1.0` → pertinence pure (pas de pénalité de diversité)
- `lambda = 0.0` → diversité maximale (ignore la pertinence)
- Par défaut : `0.7` (équilibré, léger biais de pertinence)

**Exemple — requête : "home network setup"**

Étant donné ces fichiers de mémoire :

```
memory/2026-02-10.md  → "Configured Omada router, set VLAN 10 for IoT devices"
memory/2026-02-08.md  → "Configured Omada router, moved IoT to VLAN 10"
memory/2026-02-05.md  → "Set up AdGuard DNS on 192.168.10.2"
memory/network.md     → "Router: Omada ER605, AdGuard: 192.168.10.2, VLAN 10: IoT"
```

Sans MMR — top 3 résultats :

```
1. memory/2026-02-10.md  (score: 0.92)  ← routeur + VLAN
2. memory/2026-02-08.md  (score: 0.89)  ← routeur + VLAN (quasi-doublon !)
3. memory/network.md     (score: 0.85)  ← doc de référence
```

Avec MMR (λ=0.7) — top 3 résultats :

```
1. memory/2026-02-10.md  (score: 0.92)  ← routeur + VLAN
2. memory/network.md     (score: 0.85)  ← doc de référence (diversifié !)
3. memory/2026-02-05.md  (score: 0.78)  ← AdGuard DNS (diversifié !)
```

Le quasi-doublon du 8 février disparaît, et l'agent obtient trois informations distinctes.

**Quand activer :** Si vous remarquez que `memory_search` retourne des snippets redondants ou quasi-dupliqués,
surtout avec des notes quotidiennes qui répètent souvent des informations similaires sur plusieurs jours.

#### Décroissance temporelle (boost de récence)

Les agents avec des notes quotidiennes accumulent des centaines de fichiers datés au fil du temps. Sans décroissance,
une note bien formulée d'il y a six mois peut surclasser la mise à jour d'hier sur le même sujet.

**La décroissance temporelle** applique un multiplicateur exponentiel aux scores en fonction de l'âge de chaque résultat,
pour que les souvenirs récents se classent naturellement plus haut tandis que les anciens s'estompent :

```
decayedScore = score × e^(-λ × ageInDays)
```

où `λ = ln(2) / halfLifeDays`.

Avec la demi-vie par défaut de 30 jours :

- Notes d'aujourd'hui : **100%** du score original
- Il y a 7 jours : **~84%**
- Il y a 30 jours : **50%**
- Il y a 90 jours : **12.5%**
- Il y a 180 jours : **~1.6%**

**Les fichiers persistants ne sont jamais décayés :**

- `MEMORY.md` (fichier de mémoire racine)
- Fichiers non datés dans `memory/` (par ex. `memory/projects.md`, `memory/network.md`)
- Ceux-ci contiennent des informations de référence durables qui devraient toujours se classer normalement.

**Fichiers quotidiens datés** (`memory/YYYY-MM-DD.md`) utilisent la date extraite du nom de fichier.
D'autres sources (par ex. transcriptions de session) se rabattent sur le temps de modification du fichier (`mtime`).

**Exemple — requête : "quel est l'horaire de travail de Rod ?"**

Étant donné ces fichiers de mémoire (aujourd'hui est le 10 février) :

```
memory/2025-09-15.md  → "Rod works Mon-Fri, standup at 10am, pairing at 2pm"  (148 jours)
memory/2026-02-10.md  → "Rod has standup at 14:15, 1:1 with Zeb at 14:45"    (aujourd'hui)
memory/2026-02-03.md  → "Rod started new team, standup moved to 14:15"        (7 jours)
```

Sans décroissance :

```
1. memory/2025-09-15.md  (score: 0.91)  ← meilleure correspondance sémantique, mais obsolète !
2. memory/2026-02-10.md  (score: 0.82)
3. memory/2026-02-03.md  (score: 0.80)
```

Avec décroissance (halfLife=30) :

```
1. memory/2026-02-10.md  (score: 0.82 × 1.00 = 0.82)  ← aujourd'hui, pas de décroissance
2. memory/2026-02-03.md  (score: 0.80 × 0.85 = 0.68)  ← 7 jours, décroissance légère
3. memory/2025-09-15.md  (score: 0.91 × 0.03 = 0.03)  ← 148 jours, presque disparu
```

La note obsolète de septembre tombe au bas malgré avoir la meilleure correspondance sémantique brute.

**Quand activer :** Si votre agent a des mois de notes quotidiennes et vous trouvez que les anciennes informations obsolètes surclassent le contexte récent. Une demi-vie de 30 jours fonctionne bien pour les flux de travail lourds en notes quotidiennes ; augmentez-la (par ex. 90 jours) si vous référencez souvent les notes plus anciennes.

#### Configuration

Les deux fonctionnalités sont configurées sous `memorySearch.query.hybrid` :

```json5
agents: {
  defaults: {
    memorySearch: {
      query: {
        hybrid: {
          enabled: true,
          vectorWeight: 0.7,
          textWeight: 0.3,
          candidateMultiplier: 4,
          // Diversité : réduire les résultats redondants
          mmr: {
            enabled: true,    // par défaut : false
            lambda: 0.7       // 0 = max diversité, 1 = max pertinence
          },
          // Récence : boost les souvenirs plus récents
          temporalDecay: {
            enabled: true,    // par défaut : false
            halfLifeDays: 30  // le score est divisé par deux tous les 30 jours
          }
        }
      }
    }
  }
}
```

Vous pouvez activer l'une ou l'autre fonctionnalité indépendamment :

- **MMR uniquement** — utile quand vous avez beaucoup de notes similaires mais l'âge n'a pas d'importance.
- **Décroissance temporelle uniquement** — utile quand la récence a de l'importance mais vos résultats sont déjà diversifiés.
- **Les deux** — recommandé pour les agents avec de grands historiques de notes quotidiennes longues.

### Cache d'embeddings

OpenClaw peut mettre en cache les **embeddings de chunks** dans SQLite pour que la réindexation et les mises à jour fréquentes (surtout les transcriptions de session) ne réembeddent pas le texte inchangé.

Configuration :

```json5
agents: {
  defaults: {
    memorySearch: {
      cache: {
        enabled: true,
        maxEntries: 50000
      }
    }
  }
}
```

### Recherche en mémoire de session (expérimental)

Vous pouvez optionnellement indexer les **transcriptions de session** et les afficher via `memory_search`.
Ceci est contrôlé par un flag expérimental.

```json5
agents: {
  defaults: {
    memorySearch: {
      experimental: { sessionMemory: true },
      sources: ["memory", "sessions"]
    }
  }
}
```

Notes :

- L'indexation de session est **opt-in** (désactivée par défaut).
- Les mises à jour de session sont débounced et **indexées de manière asynchrone** une fois qu'elles franchissent les seuils delta (meilleur effort).
- `memory_search` ne bloque jamais sur l'indexation ; les résultats peuvent être légèrement obsolètes jusqu'à ce que la synchronisation en arrière-plan se termine.
- Les résultats incluent toujours uniquement des snippets ; `memory_get` reste limité aux fichiers de mémoire.
- L'indexation de session est isolée par agent (seuls les journaux de session de cet agent sont indexés).
- Les journaux de session vivent sur le disque (`~/.openclaw/agents/<agentId>/sessions/*.jsonl`). Tout processus/utilisateur avec accès au système de fichiers peut les lire, donc traitez l'accès au disque comme la limite de confiance. Pour une isolation plus stricte, exécutez les agents sous des utilisateurs OS ou des hôtes séparés.

Seuils delta (valeurs par défaut affichées) :

```json5
agents: {
  defaults: {
    memorySearch: {
      sync: {
        sessions: {
          deltaBytes: 100000,   // ~100 KB
          deltaMessages: 50     // lignes JSONL
        }
      }
    }
  }
}
```

### Accélération vectorielle SQLite (sqlite-vec)

Quand l'extension sqlite-vec est disponible, OpenClaw stocke les embeddings dans une table virtuelle SQLite (`vec0`) et effectue des requêtes de distance vectorielle dans la base de données. Cela garde la recherche rapide sans charger chaque embedding en JS.

Configuration (optionnel) :

```json5
agents: {
  defaults: {
    memorySearch: {
      store: {
        vector: {
          enabled: true,
          extensionPath: "/path/to/sqlite-vec"
        }
      }
    }
  }
}
```

Notes :

- `enabled` par défaut à true ; quand désactivé, la recherche bascule vers la similarité cosinus en processus sur les embeddings stockés.
- Si l'extension sqlite-vec est manquante ou échoue à charger, OpenClaw enregistre l'erreur et continue avec le fallback JS (pas de table vectorielle).
- `extensionPath` remplace le chemin sqlite-vec fourni (utile pour les builds personnalisés ou les emplacements d'installation non standard).

### Téléchargement automatique d'embeddings locaux

- Modèle d'embedding local par défaut : `hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf` (~0.6 GB).
- Quand `memorySearch.provider = "local"`, `node-llama-cpp` résout `modelPath` ; si le GGUF est manquant il **télécharge automatiquement** vers le cache (ou `local.modelCacheDir` si défini), puis le charge. Les téléchargements reprennent à la nouvelle tentative.
- Exigence de build native : exécutez `pnpm approve-builds`, choisissez `node-llama-cpp`, puis `pnpm rebuild node-llama-cpp`.
- Fallback : si la configuration locale échoue et `memorySearch.fallback = "openai"`, nous basculons automatiquement vers les embeddings distants (`openai/text-embedding-3-small` sauf si remplacé) et enregistrons la raison.

### Exemple d'endpoint compatible OpenAI personnalisé

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      remote: {
        baseUrl: "https://api.example.com/v1/",
        apiKey: "YOUR_REMOTE_API_KEY",
        headers: {
          "X-Organization": "org-id",
          "X-Project": "project-id"
        }
      }
    }
  }
}
```

Notes :

- `remote.*` a la priorité sur `models.providers.openai.*`.
- `remote.headers` fusionnent avec les en-têtes OpenAI ; remote gagne en cas de conflit de clé. Omettez `remote.headers` pour utiliser les valeurs par défaut OpenAI.
