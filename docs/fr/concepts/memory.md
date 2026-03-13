---
title: "Mémoire"
summary: "Comment fonctionne la mémoire OpenClaw (fichiers d'espace de travail + vidage automatique de la mémoire)"
read_when:
  - Vous voulez connaître la disposition et le flux de travail des fichiers de mémoire
  - Vous voulez ajuster le vidage automatique de la mémoire avant compaction
---

# Mémoire

La mémoire OpenClaw est **du Markdown brut dans l'espace de travail de l'agent**. Les fichiers sont la
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
  - **Charger uniquement dans la session principale et privée** (jamais dans les contextes de groupe).

Ces fichiers se trouvent dans l'espace de travail (`agents.defaults.workspace`, par défaut
`~/.openclaw/workspace`). Voir [Agent workspace](/concepts/agent-workspace) pour la disposition complète.

## Outils de mémoire

OpenClaw expose deux outils destinés aux agents pour ces fichiers Markdown :

- `memory_search` — rappel sémantique sur des extraits indexés.
- `memory_get` — lecture ciblée d'un fichier Markdown spécifique ou d'une plage de lignes.

`memory_get` **se dégrade gracieusement quand un fichier n'existe pas** (par exemple,
le journal quotidien d'aujourd'hui avant la première écriture). Le gestionnaire intégré et le
backend QMD retournent tous deux `{ text: "", path }` au lieu de lever `ENOENT`, de sorte que les agents peuvent
gérer « rien d'enregistré pour l'instant » et continuer leur flux de travail sans envelopper l'appel
de l'outil dans une logique try/catch.

## Quand écrire la mémoire

- Les décisions, préférences et faits durables vont dans `MEMORY.md`.
- Les notes quotidiennes et le contexte courant vont dans `memory/YYYY-MM-DD.md`.
- Si quelqu'un dit « souviens-toi de ceci », écris-le (ne le garde pas en RAM).
- Ce domaine évolue encore. Il aide de rappeler au modèle de stocker les souvenirs ; il saura quoi faire.
- Si vous voulez que quelque chose persiste, **demandez au bot de l'écrire** dans la mémoire.

## Vidage automatique de la mémoire (ping avant compaction)

Quand une session est **proche de la compaction automatique**, OpenClaw déclenche un **tour
agentic silencieux** qui rappelle au modèle d'écrire la mémoire durable **avant** que le
contexte soit compacté. Les invites par défaut disent explicitement que le modèle _peut répondre_,
mais généralement `NO_REPLY` est la bonne réponse pour que l'utilisateur ne voie jamais ce tour.

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

- **Seuil logiciel** : le vidage se déclenche quand l'estimation des jetons de la session franchit
  `contextWindow - reserveTokensFloor - softThresholdTokens`.
- **Silencieux** par défaut : les invites incluent `NO_REPLY` pour que rien ne soit livré.
- **Deux invites** : une invite utilisateur plus une invite système ajoutent le rappel.
- **Un vidage par cycle de compaction** (suivi dans `sessions.json`).
- **L'espace de travail doit être accessible en écriture** : si la session s'exécute en bac à sable avec
  `workspaceAccess: "ro"` ou `"none"`, le vidage est ignoré.

Pour le cycle de vie complet de la compaction, voir
[Session management + compaction](/reference/session-management-compaction).

## Recherche de mémoire vectorielle

OpenClaw peut construire un petit index vectoriel sur `MEMORY.md` et `memory/*.md` pour que
les requêtes sémantiques puissent trouver des notes connexes même quand la formulation diffère.

Valeurs par défaut :

- Activé par défaut.
- Surveille les fichiers de mémoire pour les modifications (avec rebond).
- Configurez la recherche de mémoire sous `agents.defaults.memorySearch` (pas au niveau supérieur
  `memorySearch`).
- Utilise les embeddings distants par défaut. Si `memorySearch.provider` n'est pas défini, OpenClaw sélectionne automatiquement :
  1. `local` si un `memorySearch.local.modelPath` est configuré et le fichier existe.
  2. `openai` si une clé OpenAI peut être résolue.
  3. `gemini` si une clé Gemini peut être résolue.
  4. `voyage` si une clé Voyage peut être résolue.
  5. `mistral` si une clé Mistral peut être résolue.
  6. Sinon la recherche de mémoire reste désactivée jusqu'à configuration.
- Le mode local utilise node-llama-cpp et peut nécessiter `pnpm approve-builds`.
- Utilise sqlite-vec (quand disponible) pour accélérer la recherche vectorielle dans SQLite.
- `memorySearch.provider = "ollama"` est également supporté pour les embeddings Ollama locaux/auto-hébergés
  (`/api/embeddings`), mais n'est pas sélectionné automatiquement.

Les embeddings distants **nécessitent** une clé API pour le fournisseur d'embeddings. OpenClaw
résout les clés à partir des profils d'authentification, `models.providers.*.apiKey`, ou des variables
d'environnement. Codex OAuth couvre uniquement chat/completions et **ne satisfait pas** les embeddings
pour la recherche de mémoire. Pour Gemini, utilisez `GEMINI_API_KEY` ou
`models.providers.google.apiKey`. Pour Voyage, utilisez `VOYAGE_API_KEY` ou
`models.providers.voyage.apiKey`. Pour Mistral, utilisez `MISTRAL_API_KEY` ou
`models.providers.mistral.apiKey`. Ollama ne nécessite généralement pas une vraie clé API
(un placeholder comme `OLLAMA_API_KEY=ollama-local` suffit quand nécessaire par la politique locale).
Quand vous utilisez un point de terminaison compatible OpenAI personnalisé,
définissez `memorySearch.remote.apiKey` (et optionnellement `memorySearch.remote.headers`).

### Backend QMD (expérimental)

Définissez `memory.backend = "qmd"` pour remplacer l'indexeur SQLite intégré par
[QMD](https://github.com/tobi/qmd) : un sidécar de recherche local-first qui combine
BM25 + vecteurs + reclassement. Le Markdown reste la source de vérité ; OpenClaw appelle
QMD pour la récupération. Points clés :

**Prérequis**

- Désactivé par défaut. Activez par configuration (`memory.backend = "qmd"`).
- Installez le CLI QMD séparément (`bun install -g https://github.com/tobi/qmd` ou téléchargez
  une version) et assurez-vous que le binaire `qmd` est sur le `PATH` de la passerelle.
- QMD a besoin d'une compilation SQLite qui permet les extensions (`brew install sqlite` sur
  macOS).
- QMD s'exécute entièrement localement via Bun + `node-llama-cpp` et télécharge automatiquement les modèles GGUF
  depuis HuggingFace à la première utilisation (aucun daemon Ollama séparé requis).
- La passerelle exécute QMD dans un répertoire personnel XDG autonome sous
  `~/.openclaw/agents/<agentId>/qmd/` en définissant `XDG_CONFIG_HOME` et
  `XDG_CACHE_HOME`.
- Support OS : macOS et Linux fonctionnent directement une fois Bun + SQLite
  installés. Windows est mieux supporté via WSL2.

**Comment le sidécar s'exécute**

- La passerelle écrit un répertoire personnel QMD autonome sous
  `~/.openclaw/agents/<agentId>/qmd/` (config + cache + base de données sqlite).
- Les collections sont créées via `qmd collection add` à partir de `memory.qmd.paths`
  (plus les fichiers de mémoire d'espace de travail par défaut), puis `qmd update` + `qmd embed` s'exécutent
  au démarrage et à un intervalle configurable (`memory.qmd.update.interval`,
  par défaut 5 m).
- La passerelle initialise maintenant le gestionnaire QMD au démarrage, de sorte que les minuteurs de mise à jour périodique
  sont armés même avant le premier appel `memory_search`.
- L'actualisation au démarrage s'exécute maintenant en arrière-plan par défaut pour que le démarrage du chat ne soit pas
  bloqué ; définissez `memory.qmd.update.waitForBootSync = true` pour conserver le comportement
  bloquant précédent.
- Les recherches s'exécutent via `memory.qmd.searchMode` (par défaut `qmd search --json` ; supporte aussi
  `vsearch` et `query`). Si le mode sélectionné rejette les drapeaux sur votre
  compilation QMD, OpenClaw réessaie avec `qmd query`. Si QMD échoue ou le binaire est
  manquant, OpenClaw bascule automatiquement vers le gestionnaire SQLite intégré pour que
  les outils de mémoire continuent de fonctionner.
- OpenClaw n'expose pas le réglage de la taille de lot d'embeddings QMD aujourd'hui ; le comportement de lot est
  contrôlé par QMD lui-même.
- **La première recherche peut être lente** : QMD peut télécharger les modèles GGUF locaux (reclasseur/expansion de requête)
  à la première exécution de `qmd query`.
  - OpenClaw définit `XDG_CONFIG_HOME`/`XDG_CACHE_HOME` automatiquement quand il exécute QMD.
  - Si vous voulez pré-télécharger les modèles manuellement (et réchauffer le même index qu'OpenClaw
    utilise), exécutez une requête unique avec les répertoires XDG de l'agent.

    L'état QMD d'OpenClaw se trouve sous votre **répertoire d'état** (par défaut `~/.openclaw`).
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

**Surface de configuration (`memory.qmd.*`)**

- `command` (par défaut `qmd`) : remplacez le chemin de l'exécutable.
- `searchMode` (par défaut `search`) : choisissez quelle commande QMD soutient
  `memory_search` (`search`, `vsearch`, `query`).
- `includeDefaultMemory` (par défaut `true`) : indexez automatiquement `MEMORY.md` + `memory/**/*.md`.
- `paths[]` : ajoutez des répertoires/fichiers supplémentaires (`path`, `pattern` optionnel, `name`
  stable optionnel).
- `sessions` : activez l'indexation JSONL de session (`enabled`, `retentionDays`,
  `exportDir`).
- `update` : contrôle la cadence d'actualisation et l'exécution de la maintenance :
  (`interval`, `debounceMs`, `onBoot`, `waitForBootSync`, `embedInterval`,
  `commandTimeoutMs`, `updateTimeoutMs`, `embedTimeoutMs`).
- `limits` : limitez la charge de rappel (`maxResults`, `maxSnippetChars`,
  `maxInjectedChars`, `timeoutMs`).
- `scope` : même schéma que [`session.sendPolicy`](/gateway/configuration#session).
  Par défaut DM uniquement (`deny` tous, `allow` chats directs) ; assouplissez-le pour afficher les résultats QMD
  dans les groupes/canaux.
  - `match.keyPrefix` correspond à la **clé de session normalisée** (minuscules, avec tout
    `agent:<id>:` initial supprimé). Exemple : `discord:channel:`.
  - `match.rawKeyPrefix` correspond à la **clé de session brute** (minuscules), incluant
    `agent:<id>:`. Exemple : `agent:main:discord:`.
  - Héritage : `match.keyPrefix: "agent:..."` est toujours traité comme un préfixe de clé brute,
    mais préférez `rawKeyPrefix` pour la clarté.
- Quand `scope` refuse une recherche, OpenClaw enregistre un avertissement avec le
  `channel`/`chatType` dérivé pour que les résultats vides soient plus faciles à déboguer.
- Les extraits provenant en dehors de l'espace de travail apparaissent comme
  `qmd/<collection>/<relative-path>` dans les résultats `memory_search` ; `memory_get`
  comprend ce préfixe et lit à partir de la racine de collection QMD configurée.
- Quand `memory
