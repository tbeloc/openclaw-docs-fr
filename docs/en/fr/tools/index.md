---
summary: "Surface d'outils agent pour OpenClaw (navigateur, canvas, nœuds, message, cron) remplaçant les anciennes compétences `openclaw-*`"
read_when:
  - Adding or modifying agent tools
  - Retiring or changing `openclaw-*` skills
title: "Tools"
---

# Tools (OpenClaw)

OpenClaw expose des **outils agent de première classe** pour le navigateur, canvas, nœuds et cron.
Ils remplacent les anciennes compétences `openclaw-*` : les outils sont typés, pas de shell,
et l'agent doit s'y fier directement.

## Désactiver les outils

Vous pouvez autoriser/refuser globalement les outils via `tools.allow` / `tools.deny` dans `openclaw.json`
(deny gagne). Cela empêche les outils non autorisés d'être envoyés aux fournisseurs de modèles.

```json5
{
  tools: { deny: ["browser"] },
}
```

Notes :

- La correspondance est insensible à la casse.
- Les caractères génériques `*` sont supportés (`"*"` signifie tous les outils).
- Si `tools.allow` ne référence que des noms d'outils de plugin inconnus ou non chargés, OpenClaw enregistre un avertissement et ignore la liste d'autorisation pour que les outils principaux restent disponibles.

## Profils d'outils (liste d'autorisation de base)

`tools.profile` définit une **liste d'autorisation d'outils de base** avant `tools.allow`/`tools.deny`.
Remplacement par agent : `agents.list[].tools.profile`.

Profils :

- `minimal` : `session_status` uniquement
- `coding` : `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`
- `messaging` : `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`
- `full` : pas de restriction (identique à non défini)

Exemple (messagerie uniquement par défaut, autoriser aussi les outils Slack + Discord) :

```json5
{
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

Exemple (profil de codage, mais refuser exec/process partout) :

```json5
{
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

Exemple (profil de codage global, agent de support messagerie uniquement) :

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

## Politique d'outils spécifique au fournisseur

Utilisez `tools.byProvider` pour **restreindre davantage** les outils pour des fournisseurs spécifiques
(ou un seul `provider/model`) sans modifier vos paramètres par défaut globaux.
Remplacement par agent : `agents.list[].tools.byProvider`.

Ceci est appliqué **après** le profil d'outil de base et **avant** les listes d'autorisation/refus,
donc il ne peut que réduire l'ensemble d'outils.
Les clés de fournisseur acceptent soit `provider` (par ex. `google-antigravity`) soit
`provider/model` (par ex. `openai/gpt-5.2`).

Exemple (conserver le profil de codage global, mais outils minimaux pour Google Antigravity) :

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

Exemple (liste d'autorisation spécifique au fournisseur/modèle pour un point de terminaison instable) :

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

Exemple (remplacement spécifique à l'agent pour un seul fournisseur) :

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

Les politiques d'outils (global, agent, sandbox) supportent les entrées `group:*` qui se développent en plusieurs outils.
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
- `group:openclaw` : tous les outils OpenClaw intégrés (exclut les plugins de fournisseur)

Exemple (autoriser uniquement les outils de fichiers + navigateur) :

```json5
{
  tools: {
    allow: ["group:fs", "browser"],
  },
}
```

## Plugins + outils

Les plugins peuvent enregistrer des **outils supplémentaires** (et des commandes CLI) au-delà de l'ensemble principal.
Voir [Plugins](/tools/plugin) pour l'installation + configuration, et [Skills](/tools/skills) pour comment
les conseils d'utilisation d'outils sont injectés dans les invites. Certains plugins livrent leurs propres compétences
aux côtés des outils (par exemple, le plugin d'appel vocal).

Outils de plugin optionnels :

- [Lobster](/tools/lobster) : runtime de flux de travail typé avec approbations reprises (nécessite la CLI Lobster sur l'hôte de passerelle).
- [LLM Task](/tools/llm-task) : étape LLM JSON uniquement pour la sortie de flux de travail structuré (validation de schéma optionnelle).
- [Diffs](/tools/diffs) : visionneuse de diff en lecture seule et rendu de fichier PNG ou PDF pour les correctifs texte avant/après ou unifiés.

## Inventaire des outils

### `apply_patch`

Appliquer des correctifs structurés sur un ou plusieurs fichiers. À utiliser pour les éditions multi-hunks.
Expérimental : activer via `tools.exec.applyPatch.enabled` (modèles OpenAI uniquement).
`tools.exec.applyPatch.workspaceOnly` par défaut à `true` (contenu dans l'espace de travail). Définissez-le à `false` uniquement si vous voulez intentionnellement que `apply_patch` écrive/supprime en dehors du répertoire de l'espace de travail.

### `exec`

Exécuter des commandes shell dans l'espace de travail.

Paramètres principaux :

- `command` (requis)
- `yieldMs` (arrière-plan automatique après délai d'attente, par défaut 10000)
- `background` (arrière-plan immédiat)
- `timeout` (secondes ; tue le processus s'il est dépassé, par défaut 1800)
- `elevated` (bool ; exécuter sur l'hôte si le mode élevé est activé/autorisé ; change uniquement le comportement lorsque l'agent est en sandbox)
- `host` (`sandbox | gateway | node`)
- `security` (`deny | allowlist | full`)
- `ask` (`off | on-miss | always`)
- `node` (id/nom du nœud pour `host=node`)
- Besoin d'un vrai TTY ? Définissez `pty: true`.

Notes :

- Retourne `status: "running"` avec un `sessionId` lorsqu'il est en arrière-plan.
- Utilisez `process` pour interroger/enregistrer/écrire/tuer/effacer les sessions en arrière-plan.
- Si `process` est refusé, `exec` s'exécute de manière synchrone et ignore `yieldMs`/`background`.
- `elevated` est contrôlé par `tools.elevated` plus tout remplacement `agents.list[].tools.elevated` (les deux doivent autoriser) et est un alias pour `host=gateway` + `security=full`.
- `elevated` change uniquement le comportement lorsque l'agent est en sandbox (sinon c'est un no-op).
- `host=node` peut cibler une application compagnon macOS ou un hôte de nœud sans tête (`openclaw node run`).
- approbations gateway/node et listes d'autorisation : [Exec approvals](/tools/exec-approvals).

### `process`

Gérer les sessions exec en arrière-plan.

Actions principales :

- `list`, `poll`, `log`, `write`, `kill`, `clear`, `remove`

Notes :

- `poll` retourne la nouvelle sortie et le statut de sortie une fois terminé.
- `log` supporte `offset`/`limit` basé sur les lignes (omettez `offset` pour récupérer les N dernières lignes).
- `process` est limité par agent ; les sessions d'autres agents ne sont pas visibles.

### `loop-detection` (garde-fous de boucle d'appel d'outil)

OpenClaw suit l'historique récent des appels d'outils et bloque ou avertit lorsqu'il détecte des boucles répétitives sans progrès.
Activer avec `tools.loopDetection.enabled: true` (par défaut `false`).

```json5
{
  tools: {
    loopDetection: {
      enabled: true,
      warningThreshold: 10,
      criticalThreshold: 20,
      globalCircuitBreakerThreshold: 30,
      historySize: 30,
      detectors: {
        genericRepeat: true,
        knownPollNoProgress: true,
        pingPong: true,
      },
    },
  },
}
```

- `genericRepeat` : motif d'appel répété du même outil + mêmes paramètres.
- `knownPollNoProgress` : répétition d'outils de type sondage avec des sorties identiques.
- `pingPong` : motifs alternés `A/B/A/B` sans progrès.
- Remplacement par agent : `agents.list[].tools.loopDetection`.

### `web_search`

Rechercher le web en utilisant Perplexity, Brave, Gemini, Grok ou Kimi.

Paramètres principaux :

- `query` (requis)
- `count` (1–10 ; par défaut de `tools.web.search.maxResults`)

Notes :

- Nécessite une clé API pour le fournisseur choisi (recommandé : `openclaw configure --section web`).
- Activer via `tools.web.search.enabled`.
- Les réponses sont mises en cache (par défaut 15 min).
- Voir [Web tools](/tools/web) pour la configuration.

### `web_fetch`

Récupérer et extraire le contenu lisible d'une URL (HTML → markdown/texte).

Paramètres principaux :

- `url` (requis)
- `extractMode` (`markdown` | `text`)
- `maxChars` (tronquer les longues pages)

Notes :

- Activer via `tools.web.fetch.enabled`.
- `maxChars` est limité par `tools.web.fetch.maxCharsCap` (par défaut 50000).
- Les réponses sont mises en cache (par défaut 15 min).
- Pour les sites lourds en JS, préférez l'outil navigateur.
- Voir [Web tools](/tools/web) pour la configuration.
- Voir [Firecrawl](/tools/firecrawl) pour le secours anti-bot optionnel.

### `browser`

Contrôler le navigateur dédié géré par OpenClaw.

Actions principales :

- `status`, `start`, `stop`, `tabs`, `open`, `focus`, `close`
- `snapshot` (aria/ai)
- `screenshot` (retourne un bloc image + `MEDIA:<path>`)
- `act` (actions UI : click/type/press/hover/drag/select/fill/resize/wait/evaluate)
- `navigate`, `console`, `pdf`, `upload`, `dialog`

Gestion des profils :

- `profiles` — lister tous les profils de navigateur avec statut
- `create-profile` — créer un nouveau profil avec port auto-alloué (ou `cdpUrl`)
- `delete-profile` — arrêter le navigateur, supprimer les données utilisateur, supprimer de la config (local uniquement)
- `reset-profile` — tuer le processus orphelin sur le port du profil (local uniquement)

Paramètres courants :

- `profile` (optionnel ; par défaut `browser.defaultProfile`)
- `target` (`sandbox` | `host` | `node`)
- `node` (optionnel ; choisir un id/nom de nœud spécifique)
  Notes :
- Nécessite `browser.enabled=true` (par défaut `true` ; définissez `false` pour désactiver).
- Toutes les actions acceptent un paramètre `profile` optionnel pour le support multi-instance.
- Lorsque `profile` est omis, utilise `browser.defaultProfile` (par défaut "chrome").
- Noms de profil : alphanumériques minuscules + tirets uniquement (max 64 caractères).
- Plage de ports : 18800-18899 (~100 profils max).
- Les profils distants sont en pièce jointe uniquement (pas de start/stop/reset).
- Si un nœud capable de navigateur est connecté, l'outil peut le router automatiquement (sauf si vous épinglez `target`).
- `snapshot` par défaut à `ai` lorsque Playwright est installé ; utilisez `aria` pour l'arborescence d'accessibilité.
- `snapshot` supporte également les options de snapshot de rôle (`interactive`, `compact`, `depth`, `selector`) qui retournent des refs comme `e12`.
- `act` nécessite `ref` de `snapshot` (numérique `12` des snapshots AI, ou `e12` des snapshots de rôle) ; utilisez `evaluate` pour les rares besoins de sélecteur CSS.
- Évitez `act` → `wait` par défaut ; utilisez-le uniquement dans les cas exceptionnels (pas d'état UI fiable à attendre).
- `upload` peut optionnellement passer un `ref` pour auto-cliquer après armement.
- `upload` supporte également `inputRef` (
