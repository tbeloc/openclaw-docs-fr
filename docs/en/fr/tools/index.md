---
summary: "Agent tool surface for OpenClaw (browser, canvas, nodes, message, cron) replacing legacy `openclaw-*` skills"
read_when:
  - Adding or modifying agent tools
  - Retiring or changing `openclaw-*` skills
title: "Tools"
---

# Tools (OpenClaw)

OpenClaw expose des **outils d'agent de première classe** pour browser, canvas, nodes et cron.
Ils remplacent les anciennes compétences `openclaw-*` : les outils sont typés, pas de shell,
et l'agent doit s'y fier directement.

## Désactiver les outils

Vous pouvez autoriser/refuser globalement les outils via `tools.allow` / `tools.deny` dans `openclaw.json`
(deny l'emporte). Cela empêche les outils non autorisés d'être envoyés aux fournisseurs de modèles.

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

Exemple (messaging par défaut, autoriser aussi les outils Slack + Discord) :

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

Exemple (profil coding global, agent support messaging uniquement) :

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
il ne peut donc que réduire l'ensemble des outils.
Les clés de fournisseur acceptent soit `provider` (par exemple `google-antigravity`) soit
`provider/model` (par exemple `openai/gpt-5.2`).

Exemple (conserver le profil coding global, mais outils minimaux pour Google Antigravity) :

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

Exemple (liste d'autorisation spécifique au fournisseur/modèle pour un endpoint instable) :

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

Exemple (autoriser uniquement les outils de fichiers + browser) :

```json5
{
  tools: {
    allow: ["group:fs", "browser"],
  },
}
```

## Plugins + outils

Les plugins peuvent enregistrer des **outils supplémentaires** (et des commandes CLI) au-delà de l'ensemble principal.
Voir [Plugins](/fr/tools/plugin) pour l'installation + configuration, et [Skills](/fr/tools/skills) pour savoir comment
les conseils d'utilisation des outils sont injectés dans les invites. Certains plugins livrent leurs propres compétences
aux côtés des outils (par exemple, le plugin d'appel vocal).

Outils de plugin optionnels :

- [Lobster](/fr/tools/lobster) : runtime de workflow typé avec approbations reprises (nécessite la CLI Lobster sur l'hôte gateway).
- [LLM Task](/fr/tools/llm-task) : étape LLM JSON uniquement pour la sortie de workflow structurée (validation de schéma optionnelle).
- [Diffs](/fr/tools/diffs) : visionneuse de diff en lecture seule et rendu de fichier PNG ou PDF pour les patches texte avant/après ou unifiés.

## Inventaire des outils

### `apply_patch`

Appliquer des correctifs structurés sur un ou plusieurs fichiers. À utiliser pour les modifications multi-sections.
Expérimental : activer via `tools.exec.applyPatch.enabled` (modèles OpenAI uniquement).
`tools.exec.applyPatch.workspaceOnly` par défaut à `true` (contenu de l'espace de travail). Définir à `false` uniquement si vous souhaitez intentionnellement que `apply_patch` écrive/supprime en dehors du répertoire de l'espace de travail.

### `exec`

Exécuter des commandes shell dans l'espace de travail.

Paramètres principaux :

- `command` (obligatoire)
- `yieldMs` (arrière-plan automatique après délai d'attente, par défaut 10000)
- `background` (arrière-plan immédiat)
- `timeout` (secondes ; tue le processus s'il est dépassé, par défaut 1800)
- `elevated` (booléen ; exécuter sur l'hôte si le mode élevé est activé/autorisé ; change le comportement uniquement lorsque l'agent est en sandbox)
- `host` (`sandbox | gateway | node`)
- `security` (`deny | allowlist | full`)
- `ask` (`off | on-miss | always`)
- `node` (id/nom du nœud pour `host=node`)
- Besoin d'un vrai TTY ? Définir `pty: true`.

Remarques :

- Retourne `status: "running"` avec un `sessionId` lorsqu'il est en arrière-plan.
- Utiliser `process` pour interroger/enregistrer/écrire/tuer/effacer les sessions en arrière-plan.
- Si `process` est interdit, `exec` s'exécute de manière synchrone et ignore `yieldMs`/`background`.
- `elevated` est contrôlé par `tools.elevated` plus tout remplacement `agents.list[].tools.elevated` (les deux doivent autoriser) et est un alias pour `host=gateway` + `security=full`.
- `elevated` change le comportement uniquement lorsque l'agent est en sandbox (sinon c'est une non-opération).
- `host=node` peut cibler une application compagnon macOS ou un hôte de nœud sans interface graphique (`openclaw node run`).
- Approbations gateway/node et listes blanches : [Approbations Exec](/fr/tools/exec-approvals).

### `process`

Gérer les sessions exec en arrière-plan.

Actions principales :

- `list`, `poll`, `log`, `write`, `kill`, `clear`, `remove`

Remarques :

- `poll` retourne la nouvelle sortie et le statut de sortie une fois terminé.
- `log` supporte `offset`/`limit` basés sur les lignes (omettre `offset` pour récupérer les N dernières lignes).
- `process` est limité par agent ; les sessions d'autres agents ne sont pas visibles.

### `loop-detection` (garde-fous de boucle d'appels d'outils)

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

- `genericRepeat` : motif d'appel répété avec les mêmes outils et paramètres.
- `knownPollNoProgress` : répétition d'outils de type sondage avec des sorties identiques.
- `pingPong` : motifs alternés `A/B/A/B` sans progrès.
- Remplacement par agent : `agents.list[].tools.loopDetection`.

### `web_search`

Rechercher sur le web en utilisant Perplexity, Brave, Gemini, Grok ou Kimi.

Paramètres principaux :

- `query` (obligatoire)
- `count` (1–10 ; par défaut depuis `tools.web.search.maxResults`)

Remarques :

- Nécessite une clé API pour le fournisseur choisi (recommandé : `openclaw configure --section web`).
- Activer via `tools.web.search.enabled`.
- Les réponses sont mises en cache (par défaut 15 min).
- Voir [Outils Web](/fr/tools/web) pour la configuration.

### `web_fetch`

Récupérer et extraire le contenu lisible d'une URL (HTML → markdown/texte).

Paramètres principaux :

- `url` (obligatoire)
- `extractMode` (`markdown` | `text`)
- `maxChars` (tronquer les longues pages)

Remarques :

- Activer via `tools.web.fetch.enabled`.
- `maxChars` est limité par `tools.web.fetch.maxCharsCap` (par défaut 50000).
- Les réponses sont mises en cache (par défaut 15 min).
- Pour les sites lourds en JavaScript, préférer l'outil navigateur.
- Voir [Outils Web](/fr/tools/web) pour la configuration.
- Voir [Firecrawl](/fr/tools/firecrawl) pour le secours anti-bot optionnel.

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
- `delete-profile` — arrêter le navigateur, supprimer les données utilisateur, retirer de la configuration (local uniquement)
- `reset-profile` — tuer le processus orphelin sur le port du profil (local uniquement)

Paramètres courants :

- `profile` (optionnel ; par défaut `browser.defaultProfile`)
- `target` (`sandbox` | `host` | `node`)
- `node` (optionnel ; choisit un id/nom de nœud spécifique)

Remarques :

- Nécessite `browser.enabled=true` (par défaut `true` ; définir à `false` pour désactiver).
- Toutes les actions acceptent un paramètre `profile` optionnel pour le support multi-instance.
- Omettre `profile` pour le défaut sûr : navigateur isolé géré par OpenClaw (`openclaw`).
- Utiliser `profile="user"` pour le vrai navigateur hôte local lorsque les connexions/cookies existants importent et que l'utilisateur est présent pour cliquer/approuver tout message d'attachement.
- Utiliser `profile="chrome-relay"` uniquement pour le flux d'attachement de l'extension Chrome / bouton de barre d'outils.
- `profile="user"` et `profile="chrome-relay"` sont hôte uniquement ; ne pas les combiner avec les cibles sandbox/node.
- Lorsque `profile` est omis, utilise `browser.defaultProfile` (par défaut `openclaw`).
- Noms de profil : alphanumériques minuscules + tirets uniquement (max 64 caractères).
- Plage de ports : 18800-18899 (~100 profils max).
- Les profils distants sont attachement uniquement (pas de start/stop/reset).
- Si un nœud capable de navigateur est connecté, l'outil peut le router automatiquement (sauf si vous épinglez `target`).
- `snapshot` par défaut à `ai` lorsque Playwright est installé ; utiliser `aria` pour l'arborescence d'accessibilité.
- `snapshot` supporte également les options de snapshot de rôle (`interactive`, `compact`, `depth`, `selector`) qui retournent des références comme `e12`.
- `act` nécessite `ref` depuis `snapshot` (numérique `12` depuis les snapshots AI, ou `e12` depuis les snapshots de rôle) ; utiliser `evaluate` pour les besoins rares de sélecteur CSS.
- Éviter `act` → `wait` par défaut ; l'utiliser uniquement dans les cas exceptionnels (pas d'état UI fiable sur lequel attendre).
- `upload` peut optionnellement passer une `ref` pour auto-cliquer après armement.
- `upload` supporte également `inputRef` (ref aria) ou `element` (sélecteur CSS) pour définir `<input type="file">` directement.

### `canvas`

Piloter le Canvas du nœud (présenter, évaluer, snapshot, A2UI).

Actions principales :

- `present`, `hide`, `navigate`, `eval`
- `snapshot` (retourne un bloc image + `MEDIA:<path>`)
- `a2ui_push`, `a2ui_reset`

Remarques :

- Utilise `node.invoke` de la passerelle sous le capot.
- Si aucun `node` n'est fourni, l'outil en choisit un par défaut (nœud unique connecté ou nœud mac local).
- A2UI est v0.8 uniquement (pas de `createSurface`) ; la CLI rejette v0.9 JSONL avec erreurs de ligne.
- Test rapide : `openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"`.

### `nodes`

Découvrir et cibler les nœuds appairés ; envoyer des notifications ; capturer la caméra/écran.

Actions principales :

- `status`, `describe`
- `pending`, `approve`, `reject` (appairage)
- `notify` (macOS `system.notify`)
- `run` (macOS `system.run`)
- `camera_list`, `camera_snap`, `camera_clip`, `screen_record`
- `location_get`, `notifications_list`, `notifications_action`
- `device_status`, `device_info`, `device_permissions`, `device_health`

Remarques :

- Les commandes caméra/écran nécessitent que l'application du nœud soit au premier plan.
- Les images retournent des blocs image + `MEDIA:<path>`.
- Les vidéos retournent `FILE:<path>` (mp4).
- L'emplacement retourne une charge JSON (lat/lon/accuracy/timestamp).
- Paramètres `run` : tableau argv `command` ; optionnel `cwd`, `env` (`KEY=VAL`), `commandTimeoutMs`, `invokeTimeoutMs`, `needsScreenRecording`.

Exemple (`run`) :

```json
{
  "action": "run",
  "node": "office-mac",
  "command": ["echo", "Hello"],
  "env": ["FOO=bar"],
  "commandTimeoutMs": 12000,
  "invokeTimeoutMs": 45000,
  "needsScreenRecording": false
}
```

### `image`

Analyser une image avec le modèle d'image configuré.

Paramètres principaux :

- `image` (chemin ou URL obligatoire)
- `prompt` (optionnel ; par défaut "Describe the image.")
- `model` (remplacement optionnel)
- `maxBytesMb` (limite de taille optionnelle)

Remarques :

- Disponible uniquement lorsque `agents.defaults.imageModel` est configuré (principal ou secours), ou lorsqu'un modèle d'image implicite peut être déduit de votre modèle par défaut + authentification configurée (meilleur effort).
- Utilise le modèle d'image directement (indépendant du modèle de chat principal).

### `pdf`

Analyser un ou plusieurs documents PDF.

Pour le comportement complet, les limites, la configuration et les exemples, voir [Outil PDF](/fr/tools/pdf).

### `message`

Envoyer des messages et des actions de canal sur Discord/Google Chat/Slack/Telegram/WhatsApp/Signal/iMessage/MS Teams.

Actions principales :

- `send` (texte + média optionnel ; MS Teams supporte également `card` pour les Cartes Adaptatives)
- `poll` (sondages WhatsApp/Discord/MS Teams)
- `react` / `reactions` / `read` / `edit` / `delete`
- `pin` / `unpin` / `list-pins`
- `permissions`
- `thread-create` / `thread-list` / `thread-reply`
- `search`
- `sticker`
- `member-info` / `role-info`
- `emoji-list` / `emoji-upload` / `sticker-upload`
- `role-add` / `role-remove`
- `channel-info` / `channel-list`
- `voice-status`
- `event-list` / `event-create`
- `timeout` / `kick` / `ban`

Remarques :

- `send` route WhatsApp via la Passerelle ; les autres canaux vont directement.
- `poll` utilise la Passerelle pour WhatsApp et MS Teams ; les sondages Discord vont directement.
- Lorsqu'un appel d'outil de message est lié à une session de chat active, les envois sont limités à la cible de cette session pour éviter les fuites de contexte croisé.

### `cron`

Gérer les tâches cron de la Passerelle et les réveils.

Actions principales :

- `status`, `list`
- `add`, `update`, `remove`, `run`, `runs`
- `wake` (mettre en file d'attente l'événement système + battement de cœur immédiat optionnel)

Remarques :

- `add` attend un objet de tâche cron complet (même schéma que `cron.add` RPC).
- `update` utilise `{ jobId, patch }` (`id` accepté pour compatibilité).

### `gateway`

Redémarrer ou appliquer des mises à jour au processus Gateway en cours d'exécution (sur place).

Actions principales :

- `restart` (autorise + envoie `SIGUSR1` pour redémarrage en processus ; `openclaw gateway` redémarrage sur place)
- `config.schema.lookup` (inspecter un chemin de configuration à la fois sans charger le schéma complet dans le contexte d'invite)
- `config.get`
- `config.apply` (valider + écrire la configuration + redémarrer + réveiller)
- `config.patch` (fusionner la mise à jour partielle + redémarrer + réveiller)
- `update.run` (exécuter la mise à jour + redémarrer + réveiller)

Remarques :

- `config.schema.lookup` attend un chemin de configuration ciblé tel que `gateway.auth` ou `agents.list.*.heartbeat`.
- Les chemins peuvent inclure des ids de plugin délimités par des barres obliques lors de l'adressage de `plugins.entries.<id>`, par exemple `plugins.entries.pack/one.config`.
- Utiliser `delayMs` (par défaut 2000) pour éviter d'interrompre une réponse en vol.
- `config.schema` reste disponible pour les flux Control UI internes et n'est pas exposé via l'outil `gateway` de l'agent.
- `restart` est activé par défaut ; définir `commands.restart: false` pour le désactiver.

### `sessions_list` / `sessions_history` / `sessions_send` / `sessions_spawn` / `session_status`

Lister les sessions, inspecter l'historique des transcriptions ou envoyer à une autre session.

Paramètres principaux :

- `sessions_list` : `kinds?`, `limit?`, `activeMinutes?`, `messageLimit?` (0 = aucun)
- `sessions_history` : `sessionKey` (ou `sessionId`), `limit?`, `includeTools?`
- `sessions_send` : `sessionKey` (ou `sessionId`), `message`, `timeoutSeconds?` (0 = tirer et oublier)
- `sessions_spawn` : `task`, `label?`, `runtime?`, `agentId?`, `model?`, `thinking?`, `cwd?`, `runTimeoutSeconds?`, `thread?`, `mode?`, `cleanup?`, `sandbox?`, `streamTo?`, `attachments?`, `attachAs?`
- `session_status` : `sessionKey?` (par défaut courant ; accepte `sessionId`), `model?` (`default` efface le remplacement)

Remarques :

- `main` est la clé directe-chat canonique ; global/inconnu sont masqués.
- `messageLimit > 0` récupère les N derniers messages par session (messages d'outils filtrés).
- Le ciblage de session est contrôlé par `tools.sessions.visibility` (par défaut `tree` : session courante + sessions de sous-agent générées). Si vous exécutez un agent partagé pour plusieurs utilisateurs, envisager de définir `tools.sessions.visibility: "self"` pour empêcher la navigation entre sessions.
- `sessions_send` attend l'achèvement final lorsque `timeoutSeconds > 0`.
- La livraison/annonce se produit après l'achèvement et est au mieux ; `status: "ok"` confirme que l'exécution de l'agent s'est terminée, pas que l'annonce a été livrée.
- `sessions_spawn` supporte `runtime: "subagent" | "acp"` (par défaut `subagent`). Pour le comportement du runtime ACP, voir [Agents ACP](/fr/tools/acp-agents).
- Pour le runtime ACP, `streamTo: "parent"` route les résumés de progrès d'exécution initial vers la session du demandeur en tant qu'événements système au lieu de livraison enfant directe.
- `sessions_spawn` démarre une exécution de sous-agent et publie une réponse d'annonce vers le chat du demandeur.
  - Supporte le mode ponctuel (`mode: "run"`) et le mode persistant lié au fil (`mode: "session"` avec `thread: true`).
  - Si `thread: true` et `mode` est omis, le mode par défaut est `session`.
  - `mode: "session"` nécessite `thread: true`.
  - Si `runTimeoutSeconds` est omis, OpenClaw utilise `agents.defaults.subagents.runTimeoutSeconds` lorsqu'il est défini ; sinon le délai d'attente par défaut est `0` (pas de délai d'attente).
  - Les flux liés au fil Discord dépendent de `session.threadBindings.*` et `channels.discord.threadBindings.*`.
  - Le format de réponse inclut `Status`, `Result` et des statistiques compactes.
  - `Result` est le texte d'achèvement de l'assistant ; s'il manque, le dernier `toolResult` est utilisé comme secours.
- Les générations manuelles en mode achèvement envoient directement en premier, avec secours en file d'attente et nouvelle tentative en cas d'échecs transitoires (`status: "ok"` signifie que l'exécution s'est terminée, pas que l'annonce a été livrée).
- `sessions_spawn` supporte les pièces jointes de fichiers en ligne pour le runtime de sous-agent uniquement (ACP les rejette). Chaque pièce jointe a `name`, `content` et optionnel `encoding` (`utf8` ou `base64`) et `mimeType`. Les fichiers sont matérialisés dans l'espace de travail enfant à `.openclaw/attachments/<uuid>/` avec un fichier de métadonnées `.manifest.json`. L'outil retourne un reçu avec `count`, `totalBytes`, par fichier `sha256` et `relDir`. Le contenu des pièces jointes est automatiquement masqué de la persistance des transcriptions.
  - Configurer les limites via `tools.sessions_spawn.attachments` (`enabled`, `maxTotalBytes`, `maxFiles`, `maxFileBytes`, `retainOnSessionKeep`).
  - `attachAs.mountPath` est un indice réservé pour les implémentations de montage futures.
- `sessions_spawn` est non-bloquant et retourne `status: "accepted"` immédiatement.
- Les réponses ACP `streamTo: "parent"` peuvent inclure `streamLogPath` (session-scoped `*.acp-stream.jsonl`) pour suivre l'historique de progrès.
- `sessions_send` exécute un ping-pong de réponse (répondre `REPLY_SKIP` pour arrêter ; max tours via `session.agentToAgent.maxPingPongTurns`, 0–5).
- Après le ping-pong, l'agent cible exécute une **étape d'annonce** ; répondre `ANNOUNCE_SKIP` pour supprimer l'annonce.
- Pince sandbox : lorsque la session courante est en sandbox et `agents.defaults.sandbox.sessionToolsVisibility: "spawned"`, OpenClaw pince `tools.sessions.visibility` à `tree`.

### `agents_list`

Lister les ids d'agent que la session courante peut cibler avec `sessions_spawn`.

Remarques :

- Le résultat est restreint aux listes blanches par agent (`agents.list[].subagents.allowAgents`).
- Lorsque `["*"]` est configuré, l'outil inclut tous les agents configurés et marque `allowAny: true`.

## Paramètres (communs)

Outils soutenus par passerelle (`canvas`, `nodes`, `cron`) :

- `gatewayUrl` (par défaut `ws://127.0.0.1:18789`)
- `gatewayToken` (si l'authentification est activée)
- `timeoutMs`

Remarque : lorsque `gatewayUrl` est défini, incluez `gatewayToken` explicitement. Les outils n'héritent pas de la configuration ou des identifiants d'environnement pour les remplacements, et les identifiants explicites manquants constituent une erreur.

Outil navigateur :

- `profile` (optionnel ; par défaut `browser.defaultProfile`)
- `target` (`sandbox` | `host` | `node`)
- `node` (optionnel ; épingler un ID/nom de nœud spécifique)
- Guides de dépannage :
  - Problèmes de démarrage/CDP Linux : [Dépannage du navigateur (Linux)](/fr/tools/browser-linux-troubleshooting)
  - Passerelle WSL2 + Chrome CDP distant Windows : [Dépannage WSL2 + Windows + Chrome CDP distant](/fr/tools/browser-wsl2-windows-remote-cdp-troubleshooting)

## Flux d'agent recommandés

Automatisation du navigateur :

1. `browser` → `status` / `start`
2. `snapshot` (ai ou aria)
3. `act` (click/type/press)
4. `screenshot` si vous avez besoin d'une confirmation visuelle

Rendu du canevas :

1. `canvas` → `present`
2. `a2ui_push` (optionnel)
3. `snapshot`

Ciblage des nœuds :

1. `nodes` → `status`
2. `describe` sur le nœud choisi
3. `notify` / `run` / `camera_snap` / `screen_record`

## Sécurité

- Évitez `system.run` direct ; utilisez `nodes` → `run` uniquement avec le consentement explicite de l'utilisateur.
- Respectez le consentement de l'utilisateur pour la capture de caméra/écran.
- Utilisez `status/describe` pour assurer les permissions avant d'invoquer les commandes multimédias.

## Comment les outils sont présentés à l'agent

Les outils sont exposés sur deux canaux parallèles :

1. **Texte du message système** : une liste lisible par l'homme + conseils.
2. **Schéma d'outil** : les définitions de fonction structurées envoyées à l'API du modèle.

Cela signifie que l'agent voit à la fois « quels outils existent » et « comment les appeler ». Si un outil n'apparaît pas dans le message système ou le schéma, le modèle ne peut pas l'appeler.
