---
title: "Référence de configuration de la mémoire"
summary: "Référence de configuration complète pour la recherche de mémoire OpenClaw, les fournisseurs d'embeddings, le backend QMD, la recherche hybride et la mémoire multimodale"
read_when:
  - You want to configure memory search providers or embedding models
  - You want to set up the QMD backend
  - You want to tune hybrid search, MMR, or temporal decay
  - You want to enable multimodal memory indexing
---

# Référence de configuration de la mémoire

Cette page couvre la surface de configuration complète pour la recherche de mémoire OpenClaw. Pour
un aperçu conceptuel (disposition des fichiers, outils de mémoire, quand écrire en mémoire et le
vidage automatique), voir [Mémoire](/fr/concepts/memory).

## Valeurs par défaut de la recherche de mémoire

- Activée par défaut.
- Surveille les fichiers de mémoire pour détecter les modifications (avec débounce).
- Configurez la recherche de mémoire sous `agents.defaults.memorySearch` (pas au niveau
  `memorySearch` de haut niveau).
- Utilise les embeddings distants par défaut. Si `memorySearch.provider` n'est pas défini, OpenClaw sélectionne automatiquement :
  1. `local` si un `memorySearch.local.modelPath` est configuré et le fichier existe.
  2. `openai` si une clé OpenAI peut être résolue.
  3. `gemini` si une clé Gemini peut être résolue.
  4. `voyage` si une clé Voyage peut être résolue.
  5. `mistral` si une clé Mistral peut être résolue.
  6. Sinon, la recherche de mémoire reste désactivée jusqu'à sa configuration.
- Le mode local utilise node-llama-cpp et peut nécessiter `pnpm approve-builds`.
- Utilise sqlite-vec (quand disponible) pour accélérer la recherche vectorielle dans SQLite.
- `memorySearch.provider = "ollama"` est également supporté pour les embeddings Ollama locaux/auto-hébergés
  (`/api/embeddings`), mais n'est pas sélectionné automatiquement.

Les embeddings distants **nécessitent** une clé API pour le fournisseur d'embeddings. OpenClaw
résout les clés à partir des profils d'authentification, `models.providers.*.apiKey`, ou des variables
d'environnement. Codex OAuth couvre uniquement chat/completions et ne satisfait **pas**
les embeddings pour la recherche de mémoire. Pour Gemini, utilisez `GEMINI_API_KEY` ou
`models.providers.google.apiKey`. Pour Voyage, utilisez `VOYAGE_API_KEY` ou
`models.providers.voyage.apiKey`. Pour Mistral, utilisez `MISTRAL_API_KEY` ou
`models.providers.mistral.apiKey`. Ollama ne nécessite généralement pas une vraie clé API
(un placeholder comme `OLLAMA_API_KEY=ollama-local` suffit si nécessaire par la politique locale).
Lors de l'utilisation d'un endpoint personnalisé compatible OpenAI,
définissez `memorySearch.remote.apiKey` (et optionnellement `memorySearch.remote.headers`).

## Backend QMD (expérimental)

Définissez `memory.backend = "qmd"` pour remplacer l'indexeur SQLite intégré par
[QMD](https://github.com/tobi/qmd) : un sidecar de recherche local-first qui combine
BM25 + vecteurs + reclassement. Markdown reste la source de vérité ; OpenClaw
appelle QMD pour la récupération. Points clés :

### Prérequis

- Désactivé par défaut. Opt-in par configuration (`memory.backend = "qmd"`).
- Installez le CLI QMD séparément (`bun install -g https://github.com/tobi/qmd` ou téléchargez
  une version) et assurez-vous que le binaire `qmd` est sur le `PATH` de la passerelle.
- QMD a besoin d'une build SQLite qui permet les extensions (`brew install sqlite` sur
  macOS).
- QMD s'exécute entièrement localement via Bun + `node-llama-cpp` et télécharge automatiquement les modèles GGUF
  depuis HuggingFace à la première utilisation (aucun daemon Ollama séparé requis).
- La passerelle exécute QMD dans un home XDG autonome sous
  `~/.openclaw/agents/<agentId>/qmd/` en définissant `XDG_CONFIG_HOME` et
  `XDG_CACHE_HOME`.
- Support OS : macOS et Linux fonctionnent directement une fois Bun + SQLite
  installés. Windows est mieux supporté via WSL2.

### Comment le sidecar s'exécute

- La passerelle écrit un home QMD autonome sous
  `~/.openclaw/agents/<agentId>/qmd/` (config + cache + base de données sqlite).
- Les collections sont créées via `qmd collection add` à partir de `memory.qmd.paths`
  (plus les fichiers de mémoire d'espace de travail par défaut), puis `qmd update` + `qmd embed` s'exécutent
  au démarrage et à un intervalle configurable (`memory.qmd.update.interval`,
  par défaut 5 m).
- La passerelle initialise maintenant le gestionnaire QMD au démarrage, donc les minuteurs de mise à jour périodique
  sont armés même avant le premier appel `memory_search`.
- L'actualisation au démarrage s'exécute maintenant en arrière-plan par défaut pour que le démarrage du chat ne soit pas
  bloqué ; définissez `memory.qmd.update.waitForBootSync = true` pour conserver le comportement
  bloquant précédent.
- Les recherches s'exécutent via `memory.qmd.searchMode` (par défaut `qmd search --json` ; supporte aussi
  `vsearch` et `query`). Si le mode sélectionné rejette les drapeaux sur votre
  build QMD, OpenClaw réessaie avec `qmd query`. Si QMD échoue ou le binaire est
  manquant, OpenClaw bascule automatiquement vers le gestionnaire SQLite intégré pour que
  les outils de mémoire continuent de fonctionner.
- OpenClaw n'expose pas le tuning de la taille de batch d'embeddings QMD aujourd'hui ; le comportement de batch est
  contrôlé par QMD lui-même.
- **La première recherche peut être lente** : QMD peut télécharger des modèles GGUF locaux (reclasseur/expansion de requête)
  à la première exécution de `qmd query`.
  - OpenClaw définit `XDG_CONFIG_HOME`/`XDG_CACHE_HOME` automatiquement quand il exécute QMD.
  - Si vous voulez pré-télécharger les modèles manuellement (et réchauffer le même index qu'OpenClaw
    utilise), exécutez une requête unique avec les répertoires XDG de l'agent.

    L'état QMD d'OpenClaw vit sous votre **répertoire d'état** (par défaut `~/.openclaw`).
    Vous pouvez pointer `qmd` vers le même index en exportant les mêmes variables XDG
    qu'OpenClaw utilise :

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

### Surface de configuration (`memory.qmd.*`)

- `command` (par défaut `qmd`) : remplacez le chemin de l'exécutable.
- `searchMode` (par défaut `search`) : choisissez quelle commande QMD soutient
  `memory_search` (`search`, `vsearch`, `query`).
- `includeDefaultMemory` (par défaut `true`) : indexez automatiquement `MEMORY.md` + `memory/**/*.md`.
- `paths[]` : ajoutez des répertoires/fichiers supplémentaires (`path`, `pattern` optionnel, `name`
  stable optionnel).
- `sessions` : opt-in pour l'indexation JSONL de session (`enabled`, `retentionDays`,
  `exportDir`).
- `update` : contrôle la cadence d'actualisation et l'exécution de la maintenance :
  (`interval`, `debounceMs`, `onBoot`, `waitForBootSync`, `embedInterval`,
  `commandTimeoutMs`, `updateTimeoutMs`, `embedTimeoutMs`).
- `limits` : limitez la charge utile de rappel (`maxResults`, `maxSnippetChars`,
  `maxInjectedChars`, `timeoutMs`).
- `scope` : même schéma que [`session.sendPolicy`](/fr/gateway/configuration-reference#session).
  Par défaut, DM uniquement (`deny` tous, `allow` chats directs) ; assouplissez-le pour afficher les
  résultats QMD dans les groupes/canaux.
  - `match.keyPrefix` correspond à la clé de session **normalisée** (minuscules, avec tout
    `agent:<id>:` de début supprimé). Exemple : `discord:channel:`.
  - `match.rawKeyPrefix` correspond à la clé de session **brute** (minuscules), incluant
    `agent:<id>:`. Exemple : `agent:main:discord:`.
  - Héritage : `match.keyPrefix: "agent:..."` est toujours traité comme un préfixe de clé brute,
    mais préférez `rawKeyPrefix` pour la clarté.
- Quand `scope` refuse une recherche, OpenClaw enregistre un avertissement avec le
  `channel`/`chatType` dérivé pour que les résultats vides soient plus faciles à déboguer.
- Les snippets provenant en dehors de l'espace de travail apparaissent comme
  `qmd/<collection>/<relative-path>` dans les résultats `memory_search` ; `memory_get`
  comprend ce préfixe et lit à partir de la racine de collection QMD configurée.
- Quand `memory.qmd.sessions.enabled = true`, OpenClaw exporte les transcriptions de session
  assainies (tours User/Assistant) dans une collection QMD dédiée sous
  `~/.openclaw/agents/<id>/qmd/sessions/`, donc `memory_search` peut rappeler les conversations récentes
  sans toucher à l'index SQLite intégré.
- Les snippets `memory_search` incluent maintenant un pied de page `Source: <path#line>` quand
  `memory.citations` est `auto`/`on` ; définissez `memory.citations = "off"` pour garder
  les métadonnées de chemin internes (l'agent reçoit toujours le chemin pour
  `memory_get`, mais le texte du snippet omet le pied de page et le message système
  avertit l'agent de ne pas le citer).

### Exemple QMD

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

### Citations et fallback

- `memory.citations` s'applique quel que soit le backend (`auto`/`on`/`off`).
- Quand `qmd` s'exécute, nous marquons `status().backend = "qmd"` pour que les diagnostics montrent quel
  moteur a servi les résultats. Si le sous-processus QMD se termine ou la sortie JSON ne peut pas être
  analysée, le gestionnaire de recherche enregistre un avertissement et retourne le fournisseur intégré
  (embeddings Markdown existants) jusqu'à ce que QMD se rétablisse.

## Chemins de mémoire supplémentaires

Si vous voulez indexer des fichiers Markdown en dehors de la disposition d'espace de travail par défaut, ajoutez
des chemins explicites :

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

## Fichiers de mémoire multimodale (image + audio Gemini)

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
- `memory_get` lit toujours Markdown uniquement ; les fichiers binaires sont consultables mais ne sont pas retournés comme contenus de fichier bruts.

## Intégrations d'embeddings Gemini (natives)

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

### Gemini Embedding 2 (aperçu)

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "gemini",
      model: "gemini-embedding-2-preview",
      outputDimensionality: 3072,  // optional: 768, 1536, or 3072 (default)
      remote: {
        apiKey: "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

> **Réindexation requise :** Le passage de `gemini-embedding-001` (768 dimensions)
> à `gemini-embedding-2-preview` (3072 dimensions) modifie la taille du vecteur. Il en va de même si vous
> modifiez `outputDimensionality` entre 768, 1536 et 3072.
> OpenClaw réindexera automatiquement lorsqu'il détectera un changement de modèle ou de dimension.

## Point de terminaison personnalisé compatible OpenAI

Si vous souhaitez utiliser un point de terminaison personnalisé compatible OpenAI (OpenRouter, vLLM ou un proxy),
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

Si vous ne souhaitez pas définir une clé API, utilisez `memorySearch.provider = "local"` ou définissez
`memorySearch.fallback = "none"`.

### Secours

- `memorySearch.fallback` peut être `openai`, `gemini`, `voyage`, `mistral`, `ollama`, `local` ou `none`.
- Le fournisseur de secours n'est utilisé que lorsque le fournisseur d'embeddings principal échoue.

### Indexation par lot (OpenAI + Gemini + Voyage)

- Désactivée par défaut. Définissez `agents.defaults.memorySearch.remote.batch.enabled = true` pour l'activer pour l'indexation de grands corpus (OpenAI, Gemini et Voyage).
- Le comportement par défaut attend la fin du lot ; ajustez `remote.batch.wait`, `remote.batch.pollIntervalMs` et `remote.batch.timeoutMinutes` si nécessaire.
- Définissez `remote.batch.concurrency` pour contrôler le nombre de tâches par lot que nous soumettons en parallèle (par défaut : 2).
- Le mode par lot s'applique lorsque `memorySearch.provider = "openai"` ou `"gemini"` et utilise la clé API correspondante.
- Les tâches par lot Gemini utilisent le point de terminaison par lot d'embeddings asynchrones et nécessitent la disponibilité de l'API Batch de Gemini.

Pourquoi OpenAI batch est rapide et bon marché :

- Pour les grands remplissages, OpenAI est généralement l'option la plus rapide que nous supportons car nous pouvons soumettre de nombreuses demandes d'embeddings dans une seule tâche par lot et laisser OpenAI les traiter de manière asynchrone.
- OpenAI offre une tarification réduite pour les charges de travail de l'API Batch, donc les grandes exécutions d'indexation sont généralement moins chères que l'envoi des mêmes demandes de manière synchrone.
- Consultez la documentation et la tarification de l'API Batch d'OpenAI pour plus de détails :
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

## Comment fonctionnent les outils de mémoire

- `memory_search` recherche sémantiquement des fragments Markdown (~400 tokens cibles, chevauchement de 80 tokens) à partir de `MEMORY.md` + `memory/**/*.md`. Il retourne le texte du fragment (limité à ~700 caractères), le chemin du fichier, la plage de lignes, le score, le fournisseur/modèle et si nous avons basculé des embeddings locaux aux embeddings distants. Aucune charge utile de fichier complet n'est retournée.
- `memory_get` lit un fichier Markdown de mémoire spécifique (relatif à l'espace de travail), optionnellement à partir d'une ligne de départ et pour N lignes. Les chemins en dehors de `MEMORY.md` / `memory/` sont rejetés.
- Les deux outils ne sont activés que lorsque `memorySearch.enabled` se résout à true pour l'agent.

## Ce qui est indexé (et quand)

- Type de fichier : Markdown uniquement (`MEMORY.md`, `memory/**/*.md`).
- Stockage d'index : SQLite par agent à `~/.openclaw/memory/<agentId>.sqlite` (configurable via `agents.defaults.memorySearch.store.path`, supporte le token `{agentId}`).
- Fraîcheur : observateur sur `MEMORY.md` + `memory/` marque l'index comme obsolète (débounce 1,5s). La synchronisation est programmée au démarrage de la session, lors de la recherche ou à un intervalle et s'exécute de manière asynchrone. Les transcriptions de session utilisent des seuils delta pour déclencher la synchronisation en arrière-plan.
- Déclencheurs de réindexation : l'index stocke le **fournisseur/modèle d'embeddings + empreinte digitale du point de terminaison + paramètres de chunking**. Si l'un de ces éléments change, OpenClaw réinitialise et réindexe automatiquement l'ensemble du magasin.

## Recherche hybride (BM25 + vecteur)

Lorsqu'elle est activée, OpenClaw combine :

- **Similarité vectorielle** (correspondance sémantique, la formulation peut différer)
- **Pertinence des mots-clés BM25** (jetons exacts comme les IDs, variables d'env, symboles de code)

Si la recherche en texte intégral n'est pas disponible sur votre plateforme, OpenClaw bascule vers une recherche vectorielle uniquement.

### Pourquoi hybride

La recherche vectorielle excelle à "cela signifie la même chose" :

- "Mac Studio gateway host" vs "la machine exécutant la passerelle"
- "debounce file updates" vs "éviter l'indexation à chaque écriture"

Mais elle peut être faible sur les jetons exacts et à haut signal :

- IDs (`a828e60`, `b3b9895a...`)
- symboles de code (`memorySearch.query.hybrid`)
- chaînes d'erreur ("sqlite-vec unavailable")

BM25 (texte intégral) est l'inverse : fort sur les jetons exacts, plus faible sur les paraphrases.
La recherche hybride est le juste milieu pragmatique : **utiliser les deux signaux de récupération** pour obtenir
de bons résultats à la fois pour les requêtes en "langage naturel" et les requêtes "chercher une aiguille dans une botte de foin".

### Comment nous fusionnons les résultats (la conception actuelle)

Esquisse de l'implémentation :

1. Récupérez un pool de candidats des deux côtés :

- **Vecteur** : top `maxResults * candidateMultiplier` par similarité cosinus.
- **BM25** : top `maxResults * candidateMultiplier` par rang BM25 FTS5 (plus bas est mieux).

2. Convertissez le rang BM25 en un score 0..1 :

- `textScore = 1 / (1 + max(0, bm25Rank))`

3. Unissez les candidats par ID de chunk et calculez un score pondéré :

- `finalScore = vectorWeight * vectorScore + textWeight * textScore`

Notes :

- `vectorWeight` + `textWeight` est normalisé à 1.0 lors de la résolution de la configuration, donc les poids se comportent comme des pourcentages.
- Si les embeddings ne sont pas disponibles (ou le fournisseur retourne un vecteur zéro), nous exécutons toujours BM25 et retournons les correspondances par mots-clés.
- Si FTS5 ne peut pas être créé, nous conservons la recherche vectorielle uniquement (pas d'échec dur).

Ce n'est pas "parfait selon la théorie RI", mais c'est simple, rapide, et tend à améliorer le rappel/la précision sur les vraies notes.
Si nous voulons devenir plus sophistiqués plus tard, les prochaines étapes courantes sont Reciprocal Rank Fusion (RRF) ou la normalisation des scores
(min/max ou z-score) avant de mélanger.

### Pipeline de post-traitement

Après fusion des scores vectoriels et par mots-clés, deux étapes de post-traitement optionnelles
affinent la liste des résultats avant qu'elle n'atteigne l'agent :

```
Vecteur + Mots-clés -> Fusion pondérée -> Décroissance temporelle -> Tri -> MMR -> Résultats Top-K
```

Les deux étapes sont **désactivées par défaut** et peuvent être activées indépendamment.

### Réclassement MMR (diversité)

Lorsque la recherche hybride retourne des résultats, plusieurs chunks peuvent contenir du contenu similaire ou chevauchant.
Par exemple, chercher "home network setup" pourrait retourner cinq extraits presque identiques
de différentes notes quotidiennes qui mentionnent tous la même configuration de routeur.

**MMR (Maximal Marginal Relevance)** réclasse les résultats pour équilibrer pertinence et diversité,
en s'assurant que les meilleurs résultats couvrent différents aspects de la requête au lieu de répéter les mêmes informations.

Comment cela fonctionne :

1. Les résultats sont notés par leur pertinence d'origine (score pondéré vecteur + BM25).
2. MMR sélectionne itérativement les résultats qui maximisent : `lambda x pertinence - (1-lambda) x max_similarité_aux_sélectionnés`.
3. La similarité entre les résultats est mesurée en utilisant la similarité Jaccard sur le contenu tokenisé.

Le paramètre `lambda` contrôle le compromis :

- `lambda = 1.0` -- pertinence pure (pas de pénalité de diversité)
- `lambda = 0.0` -- diversité maximale (ignore la pertinence)
- Par défaut : `0.7` (équilibré, léger biais de pertinence)

**Exemple -- requête : "home network setup"**

Étant donné ces fichiers mémoire :

```
memory/2026-02-10.md  -> "Configured Omada router, set VLAN 10 for IoT devices"
memory/2026-02-08.md  -> "Configured Omada router, moved IoT to VLAN 10"
memory/2026-02-05.md  -> "Set up AdGuard DNS on 192.168.10.2"
memory/network.md     -> "Router: Omada ER605, AdGuard: 192.168.10.2, VLAN 10: IoT"
```

Sans MMR -- top 3 résultats :

```
1. memory/2026-02-10.md  (score: 0.92)  <- routeur + VLAN
2. memory/2026-02-08.md  (score: 0.89)  <- routeur + VLAN (quasi-doublon !)
3. memory/network.md     (score: 0.85)  <- document de référence
```

Avec MMR (lambda=0.7) -- top 3 résultats :

```
1. memory/2026-02-10.md  (score: 0.92)  <- routeur + VLAN
2. memory/network.md     (score: 0.85)  <- document de référence (diversifié !)
3. memory/2026-02-05.md  (score: 0.78)  <- AdGuard DNS (diversifié !)
```

Le quasi-doublon du 8 février disparaît, et l'agent obtient trois informations distinctes.

**Quand l'activer :** Si vous remarquez que `memory_search` retourne des extraits redondants ou quasi-dupliqués,
en particulier avec des notes quotidiennes qui répètent souvent des informations similaires sur plusieurs jours.

### Décroissance temporelle (boost de récence)

Les agents avec des notes quotidiennes accumulent des centaines de fichiers datés au fil du temps. Sans décroissance,
une note bien formulée d'il y a six mois peut surclasser la mise à jour d'hier sur le même sujet.

**La décroissance temporelle** applique un multiplicateur exponentiel aux scores en fonction de l'âge de chaque résultat,
de sorte que les souvenirs récents se classent naturellement plus haut tandis que les anciens s'estompent :

```
scoreAvecDecroissance = score x e^(-lambda x ageEnJours)
```

où `lambda = ln(2) / halfLifeDays`.

Avec la demi-vie par défaut de 30 jours :

- Notes d'aujourd'hui : **100%** du score d'origine
- Il y a 7 jours : **~84%**
- Il y a 30 jours : **50%**
- Il y a 90 jours : **12.5%**
- Il y a 180 jours : **~1.6%**

**Les fichiers persistants ne sont jamais décroissants :**

- `MEMORY.md` (fichier mémoire racine)
- Fichiers non datés dans `memory/` (par ex. `memory/projects.md`, `memory/network.md`)
- Ceux-ci contiennent des informations de référence durables qui doivent toujours se classer normalement.

**Fichiers quotidiens datés** (`memory/YYYY-MM-DD.md`) utilisent la date extraite du nom de fichier.
D'autres sources (par ex. transcriptions de session) reviennent à l'heure de modification du fichier (`mtime`).

**Exemple -- requête : "quel est l'horaire de travail de Rod ?"**

Étant donné ces fichiers mémoire (aujourd'hui est le 10 février) :

```
memory/2025-09-15.md  -> "Rod works Mon-Fri, standup at 10am, pairing at 2pm"  (148 jours)
memory/2026-02-10.md  -> "Rod has standup at 14:15, 1:1 with Zeb at 14:45"    (aujourd'hui)
memory/2026-02-03.md  -> "Rod started new team, standup moved to 14:15"        (7 jours)
```

Sans décroissance :

```
1. memory/2025-09-15.md  (score: 0.91)  <- meilleure correspondance sémantique, mais obsolète !
2. memory/2026-02-10.md  (score: 0.82)
3. memory/2026-02-03.md  (score: 0.80)
```

Avec décroissance (halfLife=30) :

```
1. memory/2026-02-10.md  (score: 0.82 x 1.00 = 0.82)  <- aujourd'hui, pas de décroissance
2. memory/2026-02-03.md  (score: 0.80 x 0.85 = 0.68)  <- 7 jours, décroissance légère
3. memory/2025-09-15.md  (score: 0.91 x 0.03 = 0.03)  <- 148 jours, presque disparu
```

La note obsolète de septembre tombe au bas malgré la meilleure correspondance sémantique brute.

**Quand l'activer :** Si votre agent a des mois de notes quotidiennes et que vous trouvez que les anciennes
informations obsolètes surclassent le contexte récent. Une demi-vie de 30 jours fonctionne bien pour
les flux de travail basés sur des notes quotidiennes ; augmentez-la (par ex. 90 jours) si vous référencez souvent des notes plus anciennes.

### Configuration de la recherche hybride

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
          // Récence : augmenter les souvenirs plus récents
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

- **MMR uniquement** -- utile quand vous avez beaucoup de notes similaires mais l'âge n'a pas d'importance.
- **Décroissance temporelle uniquement** -- utile quand la récence a de l'importance mais vos résultats sont déjà diversifiés.
- **Les deux** -- recommandé pour les agents avec un grand historique de notes quotidiennes longues.

## Cache d'embedding

OpenClaw peut mettre en cache les **embeddings de chunks** dans SQLite afin que la réindexation et les mises à jour fréquentes (en particulier les transcriptions de session) ne réembeddent pas le texte inchangé.

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

## Recherche de mémoire de session (expérimental)

Vous pouvez optionnellement indexer les **transcriptions de session** et les afficher via `memory_search`.
Ceci est protégé par un drapeau expérimental.

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
- Les mises à jour de session sont débouclées et **indexées de manière asynchrone** une fois qu'elles franchissent les seuils delta (meilleur effort).
- `memory_search` ne bloque jamais sur l'indexation ; les résultats peuvent être légèrement obsolètes jusqu'à ce que la synchronisation en arrière-plan se termine.
- Les résultats incluent toujours des extraits uniquement ; `memory_get` reste limité aux fichiers mémoire.
- L'indexation de session est isolée par agent (seuls les journaux de session de cet agent sont indexés).
- Les journaux de session vivent sur le disque (`~/.openclaw/agents/<agentId>/sessions/*.jsonl`). Tout processus/utilisateur ayant accès au système de fichiers peut les lire, donc traitez l'accès au disque comme la limite de confiance. Pour une isolation plus stricte, exécutez les agents sous des utilisateurs ou des hôtes OS séparés.

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

## Accélération vectorielle SQLite (sqlite-vec)

Lorsque l'extension sqlite-vec est disponible, OpenClaw stocke les embeddings dans une
table virtuelle SQLite (`vec0`) et effectue des requêtes de distance vectorielle dans la
base de données. Cela maintient la recherche rapide sans charger chaque embedding en JS.

Configuration (optionnelle) :

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

- `enabled` est par défaut true ; quand désactivé, la recherche revient à la similarité cosinus
  en processus sur les embeddings stockés.
- Si l'extension sqlite-vec est manquante ou échoue à charger, OpenClaw enregistre l'
  erreur et continue avec le fallback JS (pas de table vectorielle).
- `extensionPath` remplace le chemin sqlite-vec fourni (utile pour les builds personnalisés
  ou les emplacements d'installation non standard).

## Téléchargement automatique d'embedding local

- Modèle d'embedding local par défaut : `hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf` (~0.6 GB).
- Quand `memorySearch.provider = "local"`, `node-llama-cpp` résout `modelPath` ; si le GGUF est manquant il **télécharge automatiquement** vers le cache (ou `local.modelCacheDir` s'il est défini), puis le charge. Les téléchargements reprennent à la nouvelle tentative.
- Exigence de build natif : exécutez `pnpm approve-builds`, choisissez `node-llama-cpp`, puis `pnpm rebuild node-llama-cpp`.
- Fallback : si la configuration locale échoue et `memorySearch.fallback = "openai"`, nous basculons automatiquement vers les embeddings distants (`openai/text-embedding-3-small` sauf si remplacé) et enregistrons la raison.

## Exemple de point de terminaison compatible OpenAI personnalisé

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
