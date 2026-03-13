---
read_when:
  - Vous voulez comprendre la disposition des fichiers de mémoire et les flux de travail
  - Vous voulez ajuster l'actualisation de la mémoire avant la compression automatique
summary: Comment fonctionne la mémoire OpenClaw (fichiers d'espace de travail + actualisation automatique de la mémoire)
title: Mémoire
x-i18n:
  generated_at: "2026-02-03T07:47:38Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: f3a7f5d9f61f9742eb3a8adbc3ccaddeadb7e48ceccdfb595327d6d1f55cd00e
  source_path: concepts/memory.md
  workflow: 15
---

# Mémoire

La mémoire OpenClaw est **un fichier Markdown pur dans l'espace de travail de l'agent**. Ces fichiers sont la source unique de vérité ; le modèle ne « se souvient » que de ce qui est écrit sur le disque.

L'outil de recherche de mémoire est fourni par le plugin de mémoire actif (par défaut : `memory-core`). Désactivez le plugin de mémoire avec `plugins.slots.memory = "none"`.

## Fichiers de mémoire (Markdown)

La disposition de l'espace de travail par défaut utilise deux couches de mémoire :

- `memory/YYYY-MM-DD.md`
  - Journal quotidien (ajout uniquement).
  - Le contenu d'aujourd'hui et d'hier est lu au début de la session.
- `MEMORY.md` (optionnel)
  - Mémoire à long terme soigneusement organisée.
  - **Chargé uniquement dans les sessions privées principales** (jamais dans les contextes de groupe).

Ces fichiers se trouvent sous l'espace de travail (`agents.defaults.workspace`, par défaut `~/.openclaw/workspace`). Voir [Espace de travail de l'agent](/concepts/agent-workspace) pour la disposition complète.

## Quand écrire en mémoire

- Les décisions, préférences et faits persistants sont écrits dans `MEMORY.md`.
- Les notes quotidiennes et le contexte d'exécution sont écrits dans `memory/YYYY-MM-DD.md`.
- Si quelqu'un dit « mémorise ceci », écrivez-le (ne le gardez pas seulement en mémoire).
- Ce domaine est encore en évolution. Rappeler au modèle de stocker la mémoire est utile ; il saura quoi faire.
- Si vous voulez que quelque chose persiste, **demandez au robot de l'écrire** en mémoire.

## Actualisation automatique de la mémoire (déclenchée avant la compression)

Lorsqu'une session **approche de la compression automatique**, OpenClaw déclenche un **tour d'agent silencieux** qui rappelle au modèle d'écrire la mémoire persistante **avant** que le contexte ne soit compressé. L'invite par défaut indique clairement que le modèle *peut répondre*, mais généralement `NO_REPLY` est la bonne réponse, donc l'utilisateur ne verra jamais ce tour.

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

- **Seuil logiciel** : L'actualisation est déclenchée lorsque l'estimation des tokens de la session dépasse `contextWindow - reserveTokensFloor - softThresholdTokens`.
- **Silencieux par défaut** : L'invite contient `NO_REPLY`, donc rien n'est envoyé.
- **Deux invites** : Une invite utilisateur plus un rappel système supplémentaire.
- **Une actualisation par cycle de compression** (suivi dans `sessions.json`).
- **L'espace de travail doit être accessible en écriture** : L'actualisation est ignorée si la session s'exécute en bac à sable avec `workspaceAccess: "ro"` ou `"none"`.

Voir [Gestion des sessions + Compression](/reference/session-management-compaction) pour le cycle de vie complet de la compression.

## Recherche de mémoire vectorielle

OpenClaw peut construire un petit index vectoriel sur `MEMORY.md` et `memory/*.md` (ainsi que sur tout répertoire ou fichier supplémentaire auquel vous adhérez) afin que les requêtes sémantiques puissent trouver des notes pertinentes, même si la formulation est différente.

Valeurs par défaut :

- Activé par défaut.
- Surveille les modifications des fichiers de mémoire (avec rebond).
- Utilise l'intégration à distance par défaut. Si `memorySearch.provider` n'est pas défini, OpenClaw choisit automatiquement :
  1. `local` si `memorySearch.local.modelPath` est configuré et le fichier existe.
  2. `openai` si une clé OpenAI peut être résolue.
  3. `gemini` si une clé Gemini peut être résolue.
  4. Sinon, la recherche de mémoire reste désactivée jusqu'à la configuration.
- Le mode local utilise node-llama-cpp, ce qui peut nécessiter d'exécuter `pnpm approve-builds`.
- Utilise sqlite-vec (si disponible) pour accélérer la recherche vectorielle dans SQLite.

Les intégrations à distance **nécessitent** une clé API du fournisseur d'intégration. OpenClaw résout les clés à partir du fichier de configuration d'authentification, `models.providers.*.apiKey` ou des variables d'environnement. OAuth Codex couvre uniquement le chat/la complétion, **ne** satisfait **pas** les besoins d'intégration pour la recherche de mémoire. Pour Gemini, utilisez `GEMINI_API_KEY` ou `models.providers.google.apiKey`. Lors de l'utilisation d'un point de terminaison personnalisé compatible OpenAI, définissez `memorySearch.remote.apiKey` (et optionnellement `memorySearch.remote.headers`).

### Chemins de mémoire supplémentaires

Si vous souhaitez indexer des fichiers Markdown en dehors de la disposition de l'espace de travail par défaut, ajoutez des chemins explicites :

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
- Seuls les fichiers Markdown sont indexés.
- Les liens symboliques sont ignorés (fichiers ou répertoires).

### Intégrations Gemini (natives)

Définissez le fournisseur sur `gemini` pour utiliser directement l'API d'intégration Gemini :

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

Si vous souhaitez utiliser un **point de terminaison personnalisé compatible OpenAI** (OpenRouter, vLLM ou un proxy), vous pouvez utiliser la configuration `remote` avec le fournisseur OpenAI :

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

Si vous ne souhaitez pas configurer une clé API, utilisez `memorySearch.provider = "local"` ou définissez `memorySearch.fallback = "none"`.

Secours :

- `memorySearch.fallback` peut être `openai`, `gemini`, `local` ou `none`.
- Le fournisseur de secours n'est utilisé que si le fournisseur d'intégration principal échoue.

Indexation par lot (OpenAI + Gemini) :

- Les intégrations OpenAI et Gemini sont activées par défaut. Définissez `agents.defaults.memorySearch.remote.batch.enabled = false` pour désactiver.
- Le comportement par défaut attend la fin du traitement par lot ; vous pouvez ajuster `remote.batch.wait`, `remote.batch.pollIntervalMs` et `remote.batch.timeoutMinutes` si nécessaire.
- Définissez `remote.batch.concurrency` pour contrôler le nombre de travaux de traitement par lot que nous soumettons en parallèle (par défaut : 2).
- Le mode par lot s'applique lorsque `memorySearch.provider = "openai"` ou `"gemini"` et utilise la clé API correspondante.
- Les travaux de traitement par lot Gemini utilisent le point de terminaison asynchrone de traitement par lot d'intégration, qui nécessite que l'API Batch Gemini soit disponible.

Pourquoi le traitement par lot OpenAI est rapide et bon marché :

- Pour les remplissages importants, OpenAI est généralement l'option la plus rapide que nous supportons, car nous pouvons soumettre de nombreuses demandes d'intégration dans un seul travail de traitement par lot et laisser OpenAI les traiter de manière asynchrone.
- OpenAI offre une tarification réduite pour les charges de travail de l'API Batch, donc les exécutions d'indexation importantes coûtent généralement moins cher que l'envoi synchrone des mêmes demandes.
- Voir la documentation et la tarification de l'API Batch OpenAI pour plus de détails :
  - https://platform.openai.com/docs/api-reference/batch
  - https://platform.openai.com/pricing

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

- `memory_search` — Retourne des fragments avec chemin de fichier + plages de lignes.
- `memory_get` — Lit le contenu du fichier de mémoire par chemin.

Mode local :

- Définissez `agents.defaults.memorySearch.provider = "local"`.
- Fournissez `agents.defaults.memorySearch.local.modelPath` (URI GGUF ou `hf:`).
- Optionnel : définissez `agents.defaults.memorySearch.fallback = "none"` pour éviter le secours à distance.

### Comment fonctionnent les outils de mémoire

- `memory_search` effectue une recherche sémantique de blocs Markdown à partir de `MEMORY.md` + `memory/**/*.md` (cible environ 400 tokens, chevauchement de 80 tokens). Il retourne le texte du fragment (limité à environ 700 caractères), le chemin du fichier, les plages de lignes, le score, le fournisseur/modèle, et si nous avons basculé de l'intégration locale à distance. Ne retourne pas le contenu complet du fichier.
- `memory_get` lit un fichier Markdown de mémoire spécifique (chemin relatif à l'espace de travail), en option en lisant N lignes à partir d'une ligne de départ. Les chemins en dehors de `MEMORY.md` / `memory/` ne sont autorisés que s'ils sont explicitement listés dans `memorySearch.extraPaths`.
- Les deux outils ne sont activés que si `memorySearch.enabled` de l'agent se résout en true.

### Contenu indexé (et quand)

- Types de fichiers : Markdown uniquement (`MEMORY.md`, `memory/**/*.md`, et tout fichier `.md` sous `memorySearch.extraPaths`).
- Stockage d'index : SQLite par agent à `~/.openclaw/memory/<agentId>.sqlite` (configurable via `agents.defaults.memorySearch.store.path`, supporte le jeton `{agentId}`).
- Fraîcheur : Un moniteur surveille `MEMORY.md`, `memory/` et `memorySearch.extraPaths`, marquant l'index comme sale (rebond de 1,5 seconde). La synchronisation se produit au démarrage de la session, lors de la recherche ou selon un calendrier d'intervalle, et s'exécute de manière asynchrone. Les enregistrements de session déclenchent une synchronisation en arrière-plan avec un seuil delta.
- Déclencheurs de réindexation : L'index stocke l'**empreinte du fournisseur/modèle + point de terminaison + paramètres de chunking**. Si l'un d'eux change, OpenClaw réinitialise et réindexe automatiquement l'ensemble du stockage.

### Recherche hybride (BM25 + vectorielle)

Lorsqu'elle est activée, OpenClaw combine :

- **Similarité vectorielle** (correspondance sémantique, la formulation peut être différente)
- **Pertinence des mots-clés BM25** (tokens exacts comme les ID, les variables d'environnement, les symboles de code)

Si la recherche en texte intégral n'est pas disponible sur votre plateforme, OpenClaw revient à la recherche vectorielle pure.

#### Pourquoi utiliser la recherche hybride ?

La recherche vectorielle excelle à "cela signifie la même chose" :

- "Mac Studio gateway host" vs "machine exécutant la passerelle"
- "debounce file updates" vs "éviter d'indexer à chaque écriture"

Mais elle peut être plus faible sur les tokens exacts à haut signal :

- ID (`a828e60`, `b3b9895a…`)
- Symboles de code (`memorySearch.query.hybrid`)
- Chaînes d'erreur ("sqlite-vec unavailable")

BM25 (texte intégral) est exactement l'inverse : excelle sur les tokens exacts, faible
