---
read_when:
  - Ajouter ou modifier les outils d'agent
  - Désactiver ou modifier les `openclaw-*` Skills
summary: Interfaces d'outils d'agent OpenClaw (browser, canvas, nodes, message, cron), remplaçant les anciens `openclaw-*` Skills
title: Outils
x-i18n:
  generated_at: "2026-02-03T10:12:41Z"
  model: claude-opus-4-5
  provider: pi
  source_hash: a1ec62a9c9bea4c1d2cebfb88509739a3b48b451ab3e378193c620832e2aa07b
  source_path: tools/index.md
  workflow: 15
---

# Outils (OpenClaw)

OpenClaw expose des **outils d'agent de première classe** pour browser, canvas, nodes et cron.
Ces outils remplacent les anciens `openclaw-*` Skills : les outils sont typés, ne nécessitent pas d'appels shell,
et les agents doivent en dépendre directement.

## Désactiver les outils

Vous pouvez autoriser/refuser globalement les outils via `tools.allow` / `tools.deny` dans `openclaw.json`
(deny a la priorité). Cela empêche les outils non autorisés d'être envoyés au fournisseur de modèles.

```json5
{
  tools: { deny: ["browser"] },
}
```

Remarques :

- La correspondance n'est pas sensible à la casse.
- Les caractères génériques `*` sont supportés (`"*"` signifie tous les outils).
- Si `tools.allow` ne référence que des noms d'outils de plugin inconnus ou non chargés, OpenClaw enregistre un avertissement et ignore la liste d'autorisation pour s'assurer que les outils principaux restent disponibles.

## Profil de configuration des outils (liste d'autorisation de base)

`tools.profile` établit une **liste d'autorisation d'outils de base** avant `tools.allow`/`tools.deny`.
Remplacez par agent : `agents.list[].tools.profile`.

Profils :

- `minimal` : uniquement `session_status`
- `coding` : `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`
- `messaging` : `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`
- `full` : sans restriction (identique à non défini)

Exemple (par défaut uniquement la messagerie, tout en autorisant les outils Slack + Discord) :

```json5
{
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

Exemple (profil coding, mais refuser exec/process partout) :

```json5
{
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

Exemple (profil coding global, agent support avec messagerie uniquement) :

```json5
{
  tools: { profile: "coding" },
  agents: {
    list: [
      {
        id: "support",
        tools: { profile: "messaging", allow: ["slack"] },
      },
    ],
  },
}
```

## Stratégie d'outils spécifique au fournisseur

Utilisez `tools.byProvider` pour **restreindre davantage** les outils pour des fournisseurs spécifiques (ou un `provider/model` individuel),
sans modifier vos valeurs par défaut globales.
Remplacez par agent : `agents.list[].tools.byProvider`.

Ceci s'applique après le profil de configuration d'outils de base **et avant** la liste d'autorisation/refus,
donc il ne peut que réduire l'ensemble d'outils.
Les clés de fournisseur acceptent `provider` (par exemple `google-antigravity`) ou
`provider/model` (par exemple `openai/gpt-5.2`).

Exemple (conserver le profil coding global, mais Google Antigravity utilise les outils minimaux) :

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```

Exemple (liste d'autorisation spécifique à provider/model pour un endpoint instable) :

```json5
{
  tools: {
    allow: ["group:fs", "group:runtime", "sessions_list"],
    byProvider: {
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

Exemple (remplacement spécifique à l'agent pour un fournisseur unique) :

```json5
{
  agents: {
    list: [
      {
        id: "support",
        tools: {
          byProvider: {
            "google-antigravity": { allow: ["message", "sessions_list"] },
          },
        },
      },
    ],
  },
}
```

## Groupes d'outils (raccourcis)

Les stratégies d'outils (globale, agent, sandbox) supportent les entrées `group:*`, qui se développent en plusieurs outils.
Utilisez-les dans `tools.allow` / `tools.deny`.

Groupes disponibles :

- `group:runtime` : `exec`, `bash`, `process`
- `group:fs` : `read`, `write`, `edit`, `apply_patch`
- `group:sessions` : `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory` : `memory_search`, `memory_get`
- `group:web` : `web_search`, `web_fetch`
- `group:ui` : `browser`, `canvas`
- `group:automation` : `cron`, `gateway`
- `group:messaging` : `message`
- `group:nodes` : `nodes`
- `group:openclaw` : tous les outils OpenClaw intégrés (à l'exclusion des outils de plugin de fournisseur)

Exemple (autoriser uniquement les outils de fichiers + browser) :

```json5
{
  tools: {
    allow: ["group:fs", "browser"],
  },
}
```

## Plugins + Outils

Les plugins peuvent enregistrer des **outils supplémentaires** (et des commandes CLI) au-delà de l'ensemble principal.
Voir [Plugins](/tools/plugin) pour l'installation + configuration, et [Skills](/tools/skills) pour
savoir comment les conseils d'utilisation des outils sont injectés dans les invites. Certains plugins fournissent leurs propres Skills
avec les outils (par exemple, le plugin voice-call).

Outils de plugin optionnels :

- [Lobster](/tools/lobster) : runtime de flux de travail typé avec approbations reprises (nécessite Lobster CLI sur l'hôte Gateway).
- [LLM Task](/tools/llm-task) : étape LLM JSON uniquement pour la sortie de flux de travail structurée (validation de schéma optionnelle).

## Inventaire des outils

### `apply_patch`

Appliquer des correctifs structurés sur un ou plusieurs fichiers. Utilisé pour les modifications multi-blocs.
Expérimental : activé via `tools.exec.applyPatch.enabled` (modèles OpenAI uniquement).

### `exec`

Exécuter une commande shell dans l'espace de travail.

Paramètres principaux :

- `command` (obligatoire)
- `yieldMs` (exécution automatique en arrière-plan après délai d'expiration, par défaut 10000)
- `background` (exécution immédiate en arrière-plan)
- `timeout` (secondes ; terminer le processus si dépassé, par défaut 1800)
- `elevated` (booléen ; exécuter sur l'hôte si le mode élevé est activé/autorisé ; change uniquement le comportement si l'agent est en sandbox)
- `host` (`sandbox | gateway | node`)
- `security` (`deny | allowlist | full`)
- `ask` (`off | on-miss | always`)
- `node` (id/nom du nœud quand `host=node`)
- Besoin d'un vrai TTY ? Définir `pty: true`.

Remarques :

- En exécution en arrière-plan, retourne `status: "running"` avec `sessionId`.
- Utiliser `process` pour interroger/journaliser/écrire/terminer/effacer les sessions en arrière-plan.
- Si `process` n'est pas autorisé, `exec` s'exécute de manière synchrone et ignore `yieldMs`/`background`.
- `elevated` est contrôlé par `tools.elevated` plus tout remplacement `agents.list[].tools.elevated` (les deux doivent autoriser), alias pour `host=gateway` + `security=full`.
- `elevated` change uniquement le comportement si l'agent est en sandbox (sinon c'est une opération vide).
- `host=node` peut cibler les applications compagnon macOS ou les hôtes de nœuds sans tête (`openclaw node run`).
- Approbations et listes d'autorisation Gateway/nœud : [Approbations d'exécution](/tools/exec-approvals).

### `process`

Gérer les sessions exec en arrière-plan.

Opérations principales :

- `list`, `poll`, `log`, `write`, `kill`, `clear`, `remove`

Remarques :

- `poll` retourne la nouvelle sortie, retourne le statut de sortie à la fin.
- `log` supporte `offset`/`limit` basé sur les lignes (omettre `offset` pour obtenir les N dernières lignes).
- `process` est limité par agent ; les sessions d'autres agents ne sont pas visibles.

### `web_search`

Rechercher le web en utilisant l'API Brave Search.

Paramètres principaux :

- `query` (obligatoire)
- `count` (1-10 ; par défaut depuis `tools.web.search.maxResults`)

Remarques :

- Nécessite une clé API Brave (recommandé : `openclaw configure --section web`, ou définir `BRAVE_API_KEY`).
- Activé via `tools.web.search.enabled`.
- Les réponses sont mises en cache (par défaut 15 minutes).
- Voir [Outils Web](/tools/web) pour la configuration.

### `web_fetch`

Récupérer et extraire le contenu lisible d'une URL (HTML → markdown/texte).

Paramètres principaux :

- `url` (obligatoire)
- `extractMode` (`markdown` | `text`)
- `maxChars` (tronquer les longues pages)

Remarques :

- Activé via `tools.web.fetch.enabled`.
- Les réponses sont mises en cache (par défaut 15 minutes).
- Pour les sites web intensifs en JS, préférer l'outil browser.
- Voir [Outils Web](/tools/web) pour la configuration.
- Voir [Firecrawl](/tools/firecrawl) pour le secours anti-bot optionnel.

### `browser`

Contrôler un navigateur dédié géré par OpenClaw.

Opérations principales :

- `status`, `start`, `stop`, `tabs`, `open`, `focus`, `close`
- `snapshot` (aria/ai)
- `screenshot` (retourne un bloc d'image + `MEDIA:<path>`)
- `act` (opérations UI : click/type/press/hover/drag/select/fill/resize/wait/evaluate)
- `navigate`, `console`, `pdf`, `upload`, `dialog`

Gestion des profils :

- `profiles` — lister tous les profils de navigateur et leur statut
- `create-profile` — créer un nouveau profil avec port auto-assigné (ou `cdpUrl`)
- `delete-profile` — arrêter le navigateur, supprimer les données utilisateur, retirer de la configuration (local uniquement)
- `reset-profile` — terminer les processus orphelins sur le port du profil (local uniquement)

Paramètres courants :

- `profile` (optionnel ; par défaut `browser.defaultProfile`)
- `target` (`sandbox` | `host` | `node`)
- `node` (optionnel ; sélectionner un id/nom de nœud spécifique)

Remarques :

- Nécessite `browser.enabled=true` (par défaut `true` ; définir à `false` pour désactiver).
- Toutes les opérations acceptent un paramètre `profile` optionnel pour supporter plusieurs instances.
- Quand `profile` est omis, utiliser `browser.defaultProfile` (par défaut "chrome").
- Noms de profils : uniquement alphanumériques minuscules + tirets (max 64 caractères).
- Plage de ports : 18800-18899 (environ 100 profils max).
- Les profils distants supportent uniquement l'attachement (pas de start/stop/reset).
- Si un nœud supportant le navigateur est connecté, l'outil peut automatiquement le router vers lui (sauf si vous avez fixé `target`).
- `snapshot` par défaut à `ai` quand Playwright est installé ; utiliser `aria` pour l'arborescence d'accessibilité.
- `snapshot` supporte aussi les options de snapshot de rôle (`interactive`, `compact`, `depth`, `selector`), retournant des références comme `e12`.
- `act` nécessite un `ref` depuis `snapshot` (nombre `12` dans snapshot AI, ou `e12` dans snapshot aria) ; utiliser `evaluate` pour les besoins rares de sélecteur CSS.
- Par défaut éviter `act` → `wait` ; utiliser uniquement dans les cas spéciaux (pas d'état UI fiable à attendre).
- `upload` peut optionnellement passer `ref` pour cliquer automatiquement après la préparation.
- `upload` supporte aussi `inputRef` (référence aria) ou `element` (sélecteur CSS) pour définir directement `<input type="file">`.

### `canvas`

Piloter Canvas de nœud (present, eval, snapshot, A2UI).

Opérations principales :

- `present`, `hide`, `navigate`, `eval`
- `snapshot` (retourne un bloc d'image + `MEDIA:<path>`)
- `a2ui_push`, `a2ui_reset`

Remarques :

- Utilise en arrière-plan `node.invoke` de Gateway.
- Si `node` n'est pas fourni, l'outil sélectionne une valeur par défaut (nœud unique connecté ou nœud mac local).
- A2UI limité à v0.8 (pas de `createSurface`) ; CLI rejette v0.9 JSONL avec erreur de ligne.
- Test de fumée rapide : `openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"`.

### `nodes`

Découvrir et localiser les nœuds appairés ; envoyer des notifications ; capturer caméra/écran.

Opérations principales :

- `status`, `describe`
- `pending`, `approve`, `reject` (appairage)
- `notify` (macOS `system.notify`)
- `run` (macOS `system.run
